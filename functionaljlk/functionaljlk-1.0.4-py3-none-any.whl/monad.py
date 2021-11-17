#!/usr/bin/env python3
#
# Copyright 2021 Jonathan Lee Komar
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import sys

class Monad():
    """
    A monad: a function object supporting bind/map.

    username  = Monad(request.form['username']) | validate_username
    email     = Monad(request.form['email']) | validate_email
    
    This monad supports the union of sets SUCCESS, FAILURE
    EMPTY is not yet supported.
    """

    def __init__(self, value, failed=False):
        self.value = value
        self.failed = failed

    def get(self):
        return self.value

    def is_failed(self):
        return self.failed

    def __str__(self):
        return ' '.join([str(self.value), str(self.failed)])

    def bind(self, f):
        """
        This turns this class into a monad.
        """

        if self.failed:
            return self
        try:
            x = f(self.get())
            return Monad(x)
        except:
            e = sys.exc_info()[0]
            return Monad(e, True)

    def __or__(self, f):
        """
        override the or operator (symbol |) to invoke bind

        x = '1'
        y = Failure(x) | int | neg | str
        print(y)
        """
        return self.bind(f)
