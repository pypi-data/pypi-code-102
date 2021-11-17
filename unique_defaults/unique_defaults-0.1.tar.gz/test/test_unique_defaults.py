from types import SimpleNamespace

import pytest

from unique_defaults import (
    unique_builtins, unique_bytearrays, unique_defaults, unique_dicts, unique_lists, unique_sets
)


def test_list():
    @unique_lists
    def test(a=[]):
        return a

    assert test() is not test()


def test_dict():
    @unique_dicts
    def test(a={}):
        return a

    assert test() is not test()


def test_set():
    @unique_sets
    def test(a=set()):
        return a

    assert test() is not test()


def test_bytearray():
    @unique_bytearrays
    def test(a=bytearray()):
        return a

    assert test() is not test()


def test_all_builtins():
    @unique_builtins
    def test(a=bytearray(), b={}, c=[], d=set()):
        return a, b, c, d

    result1 = test()
    result2 = test()
    assert result1[0] is not result2[0]
    assert result1[1] is not result2[1]
    assert result1[2] is not result2[2]
    assert result1[3] is not result2[3]


def test_custom_default():
    @unique_defaults(SimpleNamespace)
    def test(a=SimpleNamespace()):
        return a

    assert test() is not test()


def test_passed_arguments():
    @unique_builtins
    def test(a=[]):
        return a

    assert test(None) is None
    assert test([1, 2]) == [1, 2]


def test_with_arg():
    @unique_builtins
    def test(a, b=[]):
        return b

    assert test(...) is not test(...)


def test_with_kwarg():
    @unique_builtins
    def test(a="spam", b=[]):
        return b

    assert test() is not test()


def test_several_mutable_defaults():
    @unique_builtins
    def test(a=[], b="spam", c=[], d=42, e={}):
        return a, c, e

    result1 = test()
    result2 = test()
    assert result1[0] is not result2[0]
    assert result1[1] is not result2[1]
    assert result1[2] is not result2[2]


def test_no_posonly():
    with pytest.raises(TypeError):
        @unique_builtins
        def test(a=[], /, b=[]):
            return a, b


def test_kwargonly():
    @unique_builtins
    def test(a=[], *, b=[]):
        return a, b

    result1 = test()
    result2 = test()
    assert result1[0] is not result2[0]
    assert result1[1] is not result2[1]


def test_early_args():
    @unique_builtins
    def test(*args, b=[]):
        return b

    assert test() is not test()


def test_late_args():
    @unique_builtins
    def test(b=[], *args):
        return b

    assert test() is not test()


def test_kwargs():
    @unique_builtins
    def test(b=[], **kwargs):
        return b

    assert test() is not test()
