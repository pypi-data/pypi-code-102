"""Replace a function's default values with objects unique to each function call"""


import inspect
from collections import namedtuple
from functools import wraps

_replacement = namedtuple("_replacement", "position name")

def unique_defaults(intercept_types):
    """A decorator that will replace any default parameter value of the
    types given with a new intance of its type

    intercept_types is a collection of types that are looked for in the
    function signature. Types given should be able to be initiallized
    with no arguments
    """
    def capture_defaults(func):
        func_signature = inspect.signature(func)
        to_replace = []
        for position, param in enumerate(func_signature.parameters):
            if isinstance(func_signature.parameters[param].default, intercept_types):
                if func_signature.parameters[param].kind == func_signature.parameters[param].POSITIONAL_ONLY:
                    raise TypeError(f"function {func.__module__}.{func.__qualname__} contains a "
                                    f"position-only argument {func_signature.parameters[param]} with "
                                    "mutable defaults which cannot be guaranteed to be replaced at call"
                                    " time")
                to_replace.append(_replacement(position, param))

        @wraps(func)
        def inner(*args, **kwargs):
            for replace in to_replace:
                if len(args) <= replace.position and replace.name not in kwargs:
                    kwargs[replace.name] = func_signature.parameters[replace.name].default.__class__()

            return func(*args, **kwargs)

        return inner

    return capture_defaults


unique_bytearrays = unique_defaults((bytearray,))
unique_dicts = unique_defaults((dict,))
unique_lists = unique_defaults((list,))
unique_sets = unique_defaults((set,))
unique_builtins = unique_defaults((bytearray, dict, list, set))
