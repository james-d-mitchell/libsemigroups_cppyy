"""
This file contains some internal stuff for the cppyy bindings.
"""

import cppyy

from libsemigroups_cppyy.adapters import One
from libsemigroups_cppyy.exception import LibsemigroupsCppyyException


def unwrap_return_value(type_nm, cpp_mem_fn, unwrap_return_fn):
    """
    This function unbinds the method cpp_mem_fn from its name
    cpp_mem_fn.__name__ and installs a new method called cpp_mem_fn.__name__
    that calls the original cpp_mem_fn, and then the function unwrap_return_fn on its
    return value.
    """

    # make up a new name for "cpp_mem_fn"
    cpp_mem_fn_new_name = "__" + type_nm.__name__ + "_" + cpp_mem_fn.__name__

    def call_and_catch(*args):
        try:
            # The next line is extra complicated for some reason, it must be like
            # this though
            return unwrap_return_fn(
                args[0], getattr(args[0], cpp_mem_fn_new_name)(*args[1:])
            )
        except TypeError as e:
            raise LibsemigroupsCppyyException(e) from None

    # bind the "cpp_mem_fn" to its new name "cpp_mem_fn_new_name"
    setattr(type_nm, cpp_mem_fn_new_name, cpp_mem_fn)
    # install new version of "cpp_mem_fn.__name__" that calls the original
    # version stored in "cpp_mem_fn_new_name"
    setattr(type_nm, cpp_mem_fn.__name__, call_and_catch)


def unwrap_return_value_to_int(type_nm, cpp_mem_fn):
    unwrap_return_value(
        type_nm, cpp_mem_fn, lambda self, x: x if isinstance(x, int) else ord(x)
    )


def generic_pow(self, n):
    message = "the argument (power) must be a non-negative integer"
    if not isinstance(n, int):
        raise TypeError(message)
    elif n < 0:
        raise ValueError(message)

    if n == 0:
        return One(self)
    g = self
    if n % 2 == 1:
        x = self  # x = x * g
    else:
        x = One(self)
    while n > 1:
        g *= g
        n //= 2
        if n % 2 == 1:
            x *= g
    return x


def runner__iter__(self):
    self.run()
    self.it = self.cbegin()
    return self


def runner__next__(self):
    if self.it != self.cend():
        out = self.it.__deref__()
        cppyy.gbl.std.advance(self.it, 1)
        return out
    else:
        raise StopIteration


class RandomAccessRange:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.size = cppyy.gbl.std.distance(self.first, self.last)

    def __repr__(self):
        return "<random access range of size {1} at {0}>".format(
            hex(id(self)), len(self)
        )

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        if isinstance(i, slice):
            return [self[j] for j in range(self.size)[i]]
        elif isinstance(i, int):
            if i < -1 * self.size or i >= self.size:
                raise IndexError(
                    "index out of range, must be in the range [%d, %d), but found %d"
                    % (-1 * self.size, self.size, i)
                )
            return self.first[i % self.size]
        else:
            raise TypeError(
                "random access iterator indices must be integers or slices, not "
                + type(i).__name__
            )

    def __iter__(self):
        self.it = self.first
        return self

    def __next__(self):
        if self.it != self.last:
            out = self.it.__deref__()
            cppyy.gbl.std.advance(self.it, 1)
            return out
        else:
            raise StopIteration


def method_causes_segfault(type_nm, nm):
    def throw(*args):
        raise LibsemigroupsCppyyException(
            "the member function %s causes python to crash and is not currently supported"
            % nm
        )

    setattr(type_nm, nm, throw)
