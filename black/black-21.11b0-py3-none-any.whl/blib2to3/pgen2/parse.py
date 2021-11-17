# Copyright 2004-2005 Elemental Security, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Parser engine for the grammar tables generated by pgen.

The grammar table must be loaded first.

See Parser/parser.c in the Python distribution for additional info on
how this parsing engine works.

"""
import copy
from contextlib import contextmanager

# Local imports
from . import grammar, token, tokenize
from typing import (
    cast,
    Any,
    Optional,
    Text,
    Union,
    Tuple,
    Dict,
    List,
    Iterator,
    Callable,
    Set,
    TYPE_CHECKING,
)
from blib2to3.pgen2.grammar import Grammar
from blib2to3.pytree import convert, NL, Context, RawNode, Leaf, Node

if TYPE_CHECKING:
    from blib2to3.driver import TokenProxy


Results = Dict[Text, NL]
Convert = Callable[[Grammar, RawNode], Union[Node, Leaf]]
DFA = List[List[Tuple[int, int]]]
DFAS = Tuple[DFA, Dict[int, int]]


def lam_sub(grammar: Grammar, node: RawNode) -> NL:
    assert node[3] is not None
    return Node(type=node[0], children=node[3], context=node[2])


class Recorder:
    def __init__(self, parser: "Parser", ilabels: List[int], context: Context) -> None:
        self.parser = parser
        self._ilabels = ilabels
        self.context = context  # not really matter

        self._dead_ilabels: Set[int] = set()
        self._start_point = copy.deepcopy(self.parser.stack)
        self._points = {ilabel: copy.deepcopy(self._start_point) for ilabel in ilabels}

    @property
    def ilabels(self) -> Set[int]:
        return self._dead_ilabels.symmetric_difference(self._ilabels)

    @contextmanager
    def switch_to(self, ilabel: int) -> Iterator[None]:
        self.parser.stack = self._points[ilabel]
        try:
            yield
        except ParseError:
            self._dead_ilabels.add(ilabel)
        finally:
            self.parser.stack = self._start_point

    def add_token(self, tok_type: int, tok_val: Text, raw: bool = False) -> None:
        func: Callable[..., Any]
        if raw:
            func = self.parser._addtoken
        else:
            func = self.parser.addtoken

        for ilabel in self.ilabels:
            with self.switch_to(ilabel):
                args = [tok_type, tok_val, self.context]
                if raw:
                    args.insert(0, ilabel)
                func(*args)

    def determine_route(self, value: Text = None, force: bool = False) -> Optional[int]:
        alive_ilabels = self.ilabels
        if len(alive_ilabels) == 0:
            *_, most_successful_ilabel = self._dead_ilabels
            raise ParseError("bad input", most_successful_ilabel, value, self.context)

        ilabel, *rest = alive_ilabels
        if force or not rest:
            return ilabel
        else:
            return None


class ParseError(Exception):
    """Exception to signal the parser is stuck."""

    def __init__(
        self, msg: Text, type: Optional[int], value: Optional[Text], context: Context
    ) -> None:
        Exception.__init__(
            self, "%s: type=%r, value=%r, context=%r" % (msg, type, value, context)
        )
        self.msg = msg
        self.type = type
        self.value = value
        self.context = context


class Parser(object):
    """Parser engine.

    The proper usage sequence is:

    p = Parser(grammar, [converter])  # create instance
    p.setup([start])                  # prepare for parsing
    <for each input token>:
        if p.addtoken(...):           # parse a token; may raise ParseError
            break
    root = p.rootnode                 # root of abstract syntax tree

    A Parser instance may be reused by calling setup() repeatedly.

    A Parser instance contains state pertaining to the current token
    sequence, and should not be used concurrently by different threads
    to parse separate token sequences.

    See driver.py for how to get input tokens by tokenizing a file or
    string.

    Parsing is complete when addtoken() returns True; the root of the
    abstract syntax tree can then be retrieved from the rootnode
    instance variable.  When a syntax error occurs, addtoken() raises
    the ParseError exception.  There is no error recovery; the parser
    cannot be used after a syntax error was reported (but it can be
    reinitialized by calling setup()).

    """

    def __init__(self, grammar: Grammar, convert: Optional[Convert] = None) -> None:
        """Constructor.

        The grammar argument is a grammar.Grammar instance; see the
        grammar module for more information.

        The parser is not ready yet for parsing; you must call the
        setup() method to get it started.

        The optional convert argument is a function mapping concrete
        syntax tree nodes to abstract syntax tree nodes.  If not
        given, no conversion is done and the syntax tree produced is
        the concrete syntax tree.  If given, it must be a function of
        two arguments, the first being the grammar (a grammar.Grammar
        instance), and the second being the concrete syntax tree node
        to be converted.  The syntax tree is converted from the bottom
        up.

        **post-note: the convert argument is ignored since for Black's
        usage, convert will always be blib2to3.pytree.convert. Allowing
        this to be dynamic hurts mypyc's ability to use early binding.
        These docs are left for historical and informational value.

        A concrete syntax tree node is a (type, value, context, nodes)
        tuple, where type is the node type (a token or symbol number),
        value is None for symbols and a string for tokens, context is
        None or an opaque value used for error reporting (typically a
        (lineno, offset) pair), and nodes is a list of children for
        symbols, and None for tokens.

        An abstract syntax tree node may be anything; this is entirely
        up to the converter function.

        """
        self.grammar = grammar
        # See note in docstring above. TL;DR this is ignored.
        self.convert = convert or lam_sub

    def setup(self, proxy: "TokenProxy", start: Optional[int] = None) -> None:
        """Prepare for parsing.

        This *must* be called before starting to parse.

        The optional argument is an alternative start symbol; it
        defaults to the grammar's start symbol.

        You can use a Parser instance to parse any number of programs;
        each time you call setup() the parser is reset to an initial
        state determined by the (implicit or explicit) start symbol.

        """
        if start is None:
            start = self.grammar.start
        # Each stack entry is a tuple: (dfa, state, node).
        # A node is a tuple: (type, value, context, children),
        # where children is a list of nodes or None, and context may be None.
        newnode: RawNode = (start, None, None, [])
        stackentry = (self.grammar.dfas[start], 0, newnode)
        self.stack: List[Tuple[DFAS, int, RawNode]] = [stackentry]
        self.rootnode: Optional[NL] = None
        self.used_names: Set[str] = set()
        self.proxy = proxy

    def addtoken(self, type: int, value: Text, context: Context) -> bool:
        """Add a token; return True iff this is the end of the program."""
        # Map from token to label
        ilabels = self.classify(type, value, context)
        assert len(ilabels) >= 1

        # If we have only one state to advance, we'll directly
        # take it as is.
        if len(ilabels) == 1:
            [ilabel] = ilabels
            return self._addtoken(ilabel, type, value, context)

        # If there are multiple states which we can advance (only
        # happen under soft-keywords), then we will try all of them
        # in parallel and as soon as one state can reach further than
        # the rest, we'll choose that one. This is a pretty hacky
        # and hopefully temporary algorithm.
        #
        # For a more detailed explanation, check out this post:
        # https://tree.science/what-the-backtracking.html

        with self.proxy.release() as proxy:
            counter, force = 0, False
            recorder = Recorder(self, ilabels, context)
            recorder.add_token(type, value, raw=True)

            next_token_value = value
            while recorder.determine_route(next_token_value) is None:
                if not proxy.can_advance(counter):
                    force = True
                    break

                next_token_type, next_token_value, *_ = proxy.eat(counter)
                if next_token_type == tokenize.OP:
                    next_token_type = grammar.opmap[next_token_value]

                recorder.add_token(next_token_type, next_token_value)
                counter += 1

            ilabel = cast(int, recorder.determine_route(next_token_value, force=force))
            assert ilabel is not None

        return self._addtoken(ilabel, type, value, context)

    def _addtoken(self, ilabel: int, type: int, value: Text, context: Context) -> bool:
        # Loop until the token is shifted; may raise exceptions
        while True:
            dfa, state, node = self.stack[-1]
            states, first = dfa
            arcs = states[state]
            # Look for a state with this label
            for i, newstate in arcs:
                t = self.grammar.labels[i][0]
                if t >= 256:
                    # See if it's a symbol and if we're in its first set
                    itsdfa = self.grammar.dfas[t]
                    itsstates, itsfirst = itsdfa
                    if ilabel in itsfirst:
                        # Push a symbol
                        self.push(t, itsdfa, newstate, context)
                        break  # To continue the outer while loop

                elif ilabel == i:
                    # Look it up in the list of labels
                    # Shift a token; we're done with it
                    self.shift(type, value, newstate, context)
                    # Pop while we are in an accept-only state
                    state = newstate
                    while states[state] == [(0, state)]:
                        self.pop()
                        if not self.stack:
                            # Done parsing!
                            return True
                        dfa, state, node = self.stack[-1]
                        states, first = dfa
                    # Done with this token
                    return False

            else:
                if (0, state) in arcs:
                    # An accepting state, pop it and try something else
                    self.pop()
                    if not self.stack:
                        # Done parsing, but another token is input
                        raise ParseError("too much input", type, value, context)
                else:
                    # No success finding a transition
                    raise ParseError("bad input", type, value, context)

    def classify(self, type: int, value: Text, context: Context) -> List[int]:
        """Turn a token into a label.  (Internal)

        Depending on whether the value is a soft-keyword or not,
        this function may return multiple labels to choose from."""
        if type == token.NAME:
            # Keep a listing of all used names
            self.used_names.add(value)
            # Check for reserved words
            if value in self.grammar.keywords:
                return [self.grammar.keywords[value]]
            elif value in self.grammar.soft_keywords:
                assert type in self.grammar.tokens
                return [
                    self.grammar.soft_keywords[value],
                    self.grammar.tokens[type],
                ]

        ilabel = self.grammar.tokens.get(type)
        if ilabel is None:
            raise ParseError("bad token", type, value, context)
        return [ilabel]

    def shift(self, type: int, value: Text, newstate: int, context: Context) -> None:
        """Shift a token.  (Internal)"""
        dfa, state, node = self.stack[-1]
        rawnode: RawNode = (type, value, context, None)
        newnode = convert(self.grammar, rawnode)
        assert node[-1] is not None
        node[-1].append(newnode)
        self.stack[-1] = (dfa, newstate, node)

    def push(self, type: int, newdfa: DFAS, newstate: int, context: Context) -> None:
        """Push a nonterminal.  (Internal)"""
        dfa, state, node = self.stack[-1]
        newnode: RawNode = (type, None, context, [])
        self.stack[-1] = (dfa, newstate, node)
        self.stack.append((newdfa, 0, newnode))

    def pop(self) -> None:
        """Pop a nonterminal.  (Internal)"""
        popdfa, popstate, popnode = self.stack.pop()
        newnode = convert(self.grammar, popnode)
        if self.stack:
            dfa, state, node = self.stack[-1]
            assert node[-1] is not None
            node[-1].append(newnode)
        else:
            self.rootnode = newnode
            self.rootnode.used_names = self.used_names
