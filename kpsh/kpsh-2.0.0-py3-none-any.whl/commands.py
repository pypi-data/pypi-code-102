# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2019 Michał Góral.

import sys
import os
import argparse
import subprocess
import time
import fnmatch
import shlex
import string
import secrets
import collections


class CommandError(Exception):
    pass


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


class reraise_as:
    def __init__(self, eout, msg="{}", eins=None):
        self.eout = eout
        self.msg = msg

        if eins is None or isinstance(eins, (list, tuple)):
            self.eins = eins
        else:
            self.eins = [eins]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type and (not self.eins or exc_type in self.eins):
            s = str(exc_val).strip("'\"")
            raise self.eout(self.msg.format(s))
        return False


def prepare_command_parser():
    cp = ThrowingArgumentParser(prog="", add_help=False)
    sp = cp.add_subparsers(required=True)

    parsers = {}
    parsers[None] = cp

    # helper function which automatically creates help-friendly parsers
    def add_parser(command, *a, **kw):
        kw["add_help"] = False

        descr = kw.get("description")
        if descr:
            kw["description"] = "{}\n\n{}".format(kw["help"], descr)
        else:
            kw["description"] = kw["help"]

        parser = sp.add_parser(command, *a, **kw)
        parsers[command] = parser
        return parser

    ######### open
    open_sp = add_parser("open", help="Change currently opened database.")
    open_sp.add_argument("filepath", help="path to database file.")
    open_sp.set_defaults(func=open_)

    ######### unlock
    unlock_sp = add_parser("unlock", help="Unlock currently opened database.")
    unlock_sp.add_argument(
        "--keyfile", default="", help="key file used for unlocking database"
    )
    unlock_sp.set_defaults(func=unlock)

    ######### lock
    lock_sp = add_parser("lock", help="Lock a database.")
    lock_sp.set_defaults(func=lock)

    ######### db
    db_sp = add_parser("db", help="Query opened database info.")
    db_sp.set_defaults(func=db)

    ######### ls
    ls_sp = add_parser("ls", help="List contents of database.")
    ls_sp.add_argument(
        "glob",
        nargs="?",
        default="*",
        help="display only entries which match glob expression",
    )
    ls_sp.set_defaults(func=ls)

    ######### show
    show_sp = add_parser(
        "show", help="Show contents of entry.", description="Search is case-sensitive."
    )
    show_sp.add_argument("path", help="path which should be shown")
    show_sp.add_argument("fields", nargs="*", help="only display certain fields")
    show_sp.add_argument(
        "-n",
        "--no-field-name",
        action="store_true",
        help="hide field name when printing entry fields.",
    )
    show_sp.set_defaults(func=show)

    ######### add/edit
    add_sp = add_parser(
        "add",
        help="Add a new entry if it doesn't exist yet.",
        description="New entry can be in form 'group/name'. In that case, "
        "it will be added as a member of existing group or the new "
        "group will be created",
    )
    edit_sp = add_parser("edit", help="Edit existing entry")

    for spr in (add_sp, edit_sp):
        spr.add_argument("path", help="entry path")
        spr.add_argument("-u", "--username", help="username")
        spr.add_argument("-p", "--password", help="password")

        if spr is edit_sp:
            spr.add_argument(
                "--askpass",
                action="store_true",
                help="interactively ask for password; input will be hidden",
            )

        spr.add_argument("-U", "--url", help="URL")
        spr.add_argument(
            "-n",
            "--note",
            action="append",
            dest="notes",
            help="add a note. One note takes one line. Many notes can be added "
            "by using -n more than once",
        )

        if spr is edit_sp:
            spr.add_argument(
                "-N",
                "--delete-note",
                dest="delnotes",
                metavar="NOTES",
                help="delete note. Notes are accessed by their index. Range of "
                "notes can be deleted by passing e.g. '-N 2-5', or all notes can "
                "be deleted by passing '-N *'",
            )

        spr.add_argument(
            "-s",
            "--autotype-sequence",
            metavar="KEYS",
            help="key sequence used for autotyping",
        )

        property_help = "set custom property named PROPERTY to the value VALUE."
        if spr is edit_sp:
            property_help += " If PROPERTY is empty ('property='), it will be"
            property_help += " deleted."
        property_help += " Spaces around name and value are preserved, so"
        property_help += " 'name=val' and 'name = val' are different entries."
        spr.add_argument(
            "-t",
            "--property",
            action="append",
            dest="properties",
            metavar="PROPERTY=VALUE",
            help=property_help,
        )

        sp_gen = spr.add_argument_group("password generation")
        sp_gen.add_argument(
            "-g",
            "--generate-password",
            dest="pw_gen",
            action="store_const",
            const="interactive",
            help="enable interactive password generation if --password is not "
            "set. By default password is generated from ASCII letters and "
            "digits. New password must be accepted before it is saved",
        )
        sp_gen.add_argument(
            "-G",
            "--generate-password-no-confirm",
            dest="pw_gen",
            action="store_const",
            const="noninteractive",
            help="same as --generate-password, but kpsh will automatically"
            "save generated password, without any user confirmation",
        )
        sp_gen.add_argument(
            "--letters",
            dest="charset",
            action="append_const",
            const=string.ascii_letters,
            help="use ASCII letters in generated password: a-z, A-Z",
        )
        sp_gen.add_argument(
            "--digits",
            dest="charset",
            action="append_const",
            const=string.digits,
            help="use digits in generated password: 0-9",
        )
        sp_gen.add_argument(
            "--logograms",
            dest="charset",
            action="append_const",
            const="#$%&@^`~",
            help="use logograms in generated password: #$%%&@^`~",
        )
        sp_gen.add_argument(
            "--punctuation",
            dest="charset",
            action="append_const",
            const=string.punctuation,
            help=f"use punctuation symbols in generated password: !#,.:; etc.",
        )
        sp_gen.add_argument(
            "--characters",
            help="characters which should be used for password generation. "
            "Setting this option overrides usage of --letters, --digits and "
            "--punct.",
        )
        sp_gen.add_argument(
            "-l",
            "--length",
            metavar="N",
            type=int,
            default=20,
            help="length of generated password (default: 20)",
        )

    add_sp.set_defaults(func=add)
    edit_sp.set_defaults(func=edit)

    ######### delete
    del_sp = add_parser("delete", help="Delete entry from database")
    del_sp.add_argument("paths", nargs="+", help="path of entry to remove")
    del_sp.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="delete groups and their contents recursively.",
    )
    del_sp.set_defaults(func=delete)

    ######### move
    del_sp = add_parser("move", help="Move entry to the new path.")
    del_sp.add_argument("source", help="path to be moved")
    del_sp.add_argument("dest", help="new path")
    del_sp.set_defaults(func=move)

    ######### autotype
    at_sp = add_parser(
        "autotype",
        help="Auto-type sequence of entry fields.",
        description="This simulates keypresses to any currently open window. "
        "It's particularily useful when kpsh is run from a script "
        "or keypress in non-interactive mode (`-c` switch). If "
        "`-s` is given, it will be used as auto-type sequence. "
        "Otherwise sequence defined for selected entry will be "
        "used or the default one if there is none (`-d`).",
    )
    at_sp.add_argument("path", help="path of entry to auto-type")
    at_sp.add_argument("-s", "--sequence", help="override auto-type sequence")
    at_sp.add_argument(
        "-d",
        "--default",
        default="{USERNAME}{TAB}{PASSWORD}{ENTER}",
        help="default auto-type sequence used when entry doesn't specify "
        "sequence itself.",
    )
    at_sp.add_argument(
        "-D", "--delay", type=int, default=40, help="delay beteen simulated keypresses"
    )
    at_sp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force auto-type for entries for which auto-type was disabled",
    )
    at_sp.add_argument(
        "-b",
        "--backend",
        choices=("xdotool", "ydotool", "wtype"),
        help="force usage of backend program for typing",
    )
    at_sp.add_argument(
        "-B",
        "--backend-command",
        help="command which will be run before autotype to detect backend. It "
        "should print the backend name (see --backend) to the standard "
        "output.",
    )
    at_sp.set_defaults(func=autotype)

    ######### exit
    exit_sp = add_parser("exit", help="Exit shell.")
    exit_sp.set_defaults(func=exit)

    ######### echo
    echo_sp = add_parser("echo", help="Display a message.")
    echo_sp.add_argument("message", nargs="*", help="message to be displayed")
    echo_sp.set_defaults(func=echo)

    ######### sleep
    sleep_sp = add_parser(
        "sleep",
        help="Sleep for a given number of seconds.",
        description="Seconds might be a floating number when fractions of "
        "second are needed.",
    )
    sleep_sp.add_argument("secs", type=float, help="seconds to sleep")
    sleep_sp.set_defaults(func=sleep)

    ######### help
    help_sp = add_parser("help", help="Show help for any message.")
    help_sp.add_argument("command", nargs="?")
    help_sp.set_defaults(func=lambda *a, parsers=parsers: help_(*a, parsers))

    return cp, parsers


def tokenize(seq):
    tokens = []

    i = 0
    while i < len(seq):
        start = seq.find("{", i)

        if start != -1:
            if i < start:
                tokens.append(seq[i:start])

            end = seq.find("}", start)
            nend = end + 1

            if end == -1:
                end = len(seq) - 1
            elif end == start + 1 and len(seq) > nend and seq[nend] == "}":  # {}}
                end = nend

            tokens.append(seq[start : end + 1])
            i = end + 1
        else:
            tokens.append(seq[i:])
            i = len(seq)

    return tokens


def autotype_environment(backend, backend_command, ioh):
    def _xdotool():
        from kpsh.autotype.xdotoolkeys import XDOTOOL_KEYS
        from kpsh.autotype.commands import xdotool_type, xdotool_key

        return xdotool_type, xdotool_key, XDOTOOL_KEYS

    def _ydotool():
        from kpsh.autotype.ydotoolkeys import YDOTOOL_KEYS
        from kpsh.autotype.commands import ydotool_type, ydotool_key

        return ydotool_type, ydotool_key, YDOTOOL_KEYS

    def _wtype():
        from kpsh.autotype.wtypekeys import WTYPE_KEYS
        from kpsh.autotype.commands import wtype_type, wtype_key

        return wtype_type, wtype_key, WTYPE_KEYS

    # backend_command will not return anything; instead it will set backend
    # variable. This way we'll avoid validating backend_command's output twice
    if not backend and backend_command:
        cmd = shlex.split(backend_command)
        try:
            cp = subprocess.run(cmd, capture_output=True, text=True)
            if cp.returncode == 0:
                backend = cp.stdout.strip().lower()
        except:
            ioh.eprint("Failed to run backend-cmd: {}".format(backend_command))
            pass

    if backend and backend == "xdotool":
        return _xdotool()
    elif backend and backend == "ydotool":
        return _ydotool()
    elif backend and backend == "wtype":
        return _wtype()
    elif os.environ.get("XDG_SESSION_TYPE", "") == "wayland":
        return _ydotool()
    return _xdotool()


def generate_password(characters, length):
    unique_chars = list(set(characters))
    password = "".join(secrets.choice(unique_chars) for i in range(length))
    return password


def generate_password_confirm(characters, length, ioh, confirm):
    while True:
        password = generate_password(characters, length)

        if not confirm:
            return password

        ioh.print(f"Generated password: {password}")
        repl = prompt_repeat(ioh, "[A]ccept/[N]ext/[C]ancel", "aAnNcC").lower()

        if repl == "a":
            return password
        elif repl == "c":
            return None


def askpass(ioh, prompt="Password"):
    return ioh.prompt("{}: ".format(prompt), is_password=True)


def prompt_repeat(ioh, prompt, allowed_replies, case_sensitive=True):
    while True:
        repl = ioh.prompt(f"{prompt}: ")
        if repl and repl in allowed_replies:
            return repl


def autotype(kp, args, ioh):
    from kpsh.autotype.placeholders import replace_placeholder
    from kpsh.autotype.commands import run_command

    delay = str(args.delay)
    entry = _get(args.path, kp)

    if not entry.autotype_enabled and not args.force:
        ioh.eprint(
            "Autotype disabled for {}. " "Use -f to force autotype.".format(args.path)
        )
        return

    sequence = args.sequence if args.sequence else entry.autotype_sequence
    if not sequence:
        sequence = args.default

    typecmd, keycmd, TOOL_KEYS = autotype_environment(
        args.backend, args.backend_command, ioh
    )

    for token in tokenize(sequence):
        if token.startswith("{") and token.endswith("}"):
            if run_command(token):
                continue

            placeholder = replace_placeholder(entry, token)
            if placeholder is not None:
                typecmd(delay, placeholder)
                continue

            specialkey = TOOL_KEYS.get(token)
            if specialkey is not None:
                keycmd(delay, specialkey)
                continue

            ioh.eprint("Unsupported keyword: {}".format(token))
        else:
            typecmd(delay, token)


def notes_deleter(spec):
    def _delete_all(notes):
        return []

    # range is inclusive on both sides, so for example range 1-3 will delete
    # notes 1, 2 and 3
    def _delete_range(notes, start, end):
        return [note for i, note in enumerate(notes) if (i < start or i > end)]

    if spec == "*":
        return _delete_all

    if "-" in spec:
        start, _, end = spec.partition("-")
        start = int(start.strip())
        end = int(end.strip())
    else:
        start = int(spec.strip())
        end = start

    if start <= 0 or end <= 0:
        raise ValueError("Invalid range (must be > 0): {} - {}".format(start, end))

    return lambda notes: _delete_range(notes, start - 1, end - 1)


def show(kp, args, ioh):
    def _print_single(spec, attr):
        ioh.print(spec.format(name=attr.name, value=attr.value))

    def _print_multi(spec, attr):
        for i, elem in enumerate(attr.value.splitlines()):
            indexed_name = "{name}[{i}]".format(name=attr.name, i=i + 1)
            ioh.print(spec.format(name=indexed_name, value=elem))

    entry = _get(args.path, kp)
    Attr = collections.namedtuple("Data", ("name", "value", "printer"))

    attrs = [
        Attr("path", args.path, _print_single),
        Attr("username", entry.username, _print_single),
        Attr("password", entry.password, _print_single),
        Attr("url", entry.url, _print_single),
        Attr("autotype_sequence", entry.autotype_sequence, _print_single),
        Attr("notes", entry.notes, _print_multi),
    ]

    for pname, pval in entry.custom_properties.items():
        attrs.append(Attr(f"p:{pname}", pval, _print_multi))

    def find_attr(name):
        # This function tries to find fields intelligently. Users can prefix
        # field names with e.g. "p:" to indicate a property, but if they don't,
        # the function will search for unmarked properties anyway, when their
        # names don't collide with regular fields.
        pname = name if name.startswith("p:") else f"p:{name}"
        possible_property = None

        for attr in attrs:
            if attr.name == name:
                return attr
            if attr.name == pname:
                possible_property = attr
        return possible_property

    fields = args.fields if args.fields else [a.name for a in attrs]

    for field in fields:
        attr = find_attr(field)
        if attr is None:
            ioh.eprint("Unknown attribute: {}".format(field))
            continue

        if attr.value is None:
            continue

        spec = "{value}" if args.no_field_name else "{name}: {value}"
        attr.printer(spec, attr)


def _field_changed(entry, field, newval):
    oldval = getattr(entry, field, None)
    # Rules:
    # 1. disallow setting fields to None; even though most of PyKeePass' fields
    #    have it as a default value, PyKeePass does little to no validation when
    #    writing XML and fails miserably when None is used.
    # 2. some empty fields (like notes) can be either None or empty string, so
    #    changing from None to empty string should return False
    return newval is not None and newval != oldval and (bool(newval) or bool(oldval))


def _set_entry_fields(entry, **fields):
    edited = False
    for field, val in fields.items():
        if _field_changed(entry, field, val):
            setattr(entry, field, val)
            edited = True
    return edited


def _set_custom_properties(entry, properties, delete_empty_value=False):
    if not properties:
        return False

    edited = False
    for prop in properties:
        key, delim, val = prop.partition("=")

        if not key:
            raise KeyError(f"Custom property '{prop}' must have a name.")

        if not delim:
            raise KeyError(
                f"Custom property '{key}' must be constructed as name=value."
            )

        if val:
            val = val.replace("\\n", "\n").replace("\\r", "\r")
            entry.set_custom_property(key, val)
            edited = True
        elif delete_empty_value:
            try:
                entry.delete_custom_property(key)
                edited = True
            except AttributeError:
                pass

    return edited


def add(kp, args, ioh):
    if args.path in kp.entries:
        raise CommandError("entry already exists: {}".format(args.path))

    groupname, _, title = args.path.rpartition("/")

    if not title:
        raise CommandError("Empty titles are not allowed")

    group = kp.add_group(groupname) if groupname else kp.root_group

    if not group:
        raise CommandError("Failed adding a new group: {}".format(groupname))

    entry_args = {"username": args.username if args.username else ""}
    if args.password:
        entry_args["password"] = args.password
    elif args.pw_gen:
        characters = None
        if args.characters:
            characters = args.characters
        elif args.charset:
            characters = "".join(args.charset)
        else:
            characters = string.ascii_letters + string.digits
        confirm = args.pw_gen == "interactive"
        entry_args["password"] = generate_password_confirm(
            characters, args.length, ioh, confirm
        )
    else:
        prompt = "Password for {}".format(title)
        entry_args["password"] = askpass(ioh, prompt)

    if not entry_args["password"]:
        raise CommandError("Setting a password is necessary for a new entry")

    with reraise_as(CommandError):
        with kp.no_reload():
            entry = kp.add_entry(group, title, **entry_args)

    notes = "\n".join(args.notes) if args.notes else None
    _set_entry_fields(entry, url=args.url, notes=notes)

    with reraise_as(CommandError, eins=[KeyError]):
        _set_custom_properties(entry, args.properties)

    # This overwrites autotype_sequence set by PyKeePass, which incorrectly
    # sets it to a string 'None'.
    # See: https://github.com/libkeepass/pykeepass/issues/284
    entry.autotype_sequence = args.autotype_sequence

    kp.save()


def edit(kp, args, ioh):
    entry = _get(args.path, kp)

    password = None
    if args.password:
        password = args.password
    elif args.askpass:
        prompt = "New password for {}".format(entry.title)
        password = askpass(ioh, prompt)
    elif args.pw_gen:
        characters = None
        if args.characters:
            characters = args.characters
        elif args.charset:
            characters = "".join(args.charset)
        else:
            characters = string.ascii_letters + string.digits
        confirm = args.pw_gen == "interactive"
        password = generate_password_confirm(characters, args.length, ioh, confirm)
        if password is None:
            return

    old_notes = entry.notes or ""
    old_notes_list = old_notes.splitlines()

    if args.delnotes:
        with reraise_as(
            CommandError,
            msg=f"Invalid value for -N: {args.delnotes}",
            eins=(ValueError, TypeError),
        ):
            deleter = notes_deleter(args.delnotes)
            old_notes_list = deleter(old_notes_list)

    new_notes = args.notes or []
    notes = old_notes_list + new_notes
    notes = "\n".join(notes) if notes else ""

    entry.save_history()

    edited = []
    edited.append(
        _set_entry_fields(
            entry,
            username=args.username,
            password=password,
            url=args.url,
            notes=notes,
            autotype_sequence=args.autotype_sequence,
        )
    )

    with reraise_as(CommandError, eins=[KeyError]):
        edited.append(
            _set_custom_properties(entry, args.properties, delete_empty_value=True)
        )

    if any(edited):
        entry.touch(modify=True)
        kp.save()
    else:
        _delete_last_history(entry)


def delete(kp, args, ioh):
    deleted = False
    groups = kp.groups
    with kp.no_reload():
        for path in args.paths:
            path = path.rstrip("/")
            if path in kp.entries:
                entry = kp.delete_entry(path)
                deleted |= bool(entry)
            elif path in kp.groups:
                if not args.recursive:
                    ioh.eprint(
                        f"Cannot delete group {path}. Use --recursive to delete it."
                    )
                    continue

                deleted |= kp.delete_group(path)
            else:
                ioh.eprint(f"Cannot delete {path}: path doesn't exist in database.")

    if deleted:
        kp.save()


def move(kp, args, ioh):
    title = args.source.rsplit("/")[-1]
    group = kp.find_group(args.dest)
    dest_path = f"{args.dest}/{title}" if group else args.dest

    entry = _get(args.source, kp)
    entry.save_history()

    try:
        moved = kp.move_entry(args.source, dest_path)
    except AttributeError as e:
        _delete_last_history(entry)
        raise CommandError(str(e))

    moved.touch(modify=True)
    kp.save()


def echo(kp, args, ioh):
    ioh.print(*args.message)


def sleep(kp, args, ioh):
    time.sleep(args.secs)


def ls(kp, args, ioh):
    for path in fnmatch.filter(kp.iter_paths(), args.glob):
        ioh.print(path)


def help_(kp, args, ioh, parsers):
    parser = parsers.get(args.command)
    if parser is None:
        ioh.eprint("No such command: {}".format(args.command))
        parser = parsers.get(None)

    parser.print_help()


def exit(kp, args, ioh):
    ioh.stop()


def open_(kp, args, ioh):
    fp = os.path.expanduser(args.filepath)
    kp.change_db(fp)


def unlock(kp, args, ioh):
    if not kp.locked:
        return

    kf = os.path.expanduser(args.keyfile) if args.keyfile else None
    if kf:
        kp.change_credentials(keyfile=kf)

    kp.unlock()


def lock(kp, args, ioh):
    kp.lock()


def db(kp, args, ioh):
    ioh.print(kp.db)
    ioh.print("Locked: {}".format(kp.locked))


# TODO: replace with entry.delete_history(last) when pykeepass releases
# a version with this method (mg, 2021-11-16)
# entry.delete_history(last)
def _delete_last_history(entry):
    last = entry.history[-1]
    entry._element.find("History").remove(last._element)


def _get(path, kp):
    entry = kp.entries.get(path)
    if not entry:
        raise CommandError("Entry not found: {}".format(path))
    return entry
