"""
This file contains some internal stuff for the cppyy bindings.
"""

import cppyy
from libsemigroups_cppyy.adapters import One

# TODO
# 1. add operator** to BMat8
# 2. add operator<= to BMat8
# 3. add operator>= to BMat8


def unwrap(type_nm, cpp_mem_fn, unwrap_fn):
    actual = "__" + type_nm.__name__ + "_" + cpp_mem_fn.__name__
    setattr(type_nm, actual, cpp_mem_fn)
    actual = getattr(type_nm, actual)
    setattr(type_nm, cpp_mem_fn.__name__, lambda *args: unwrap_fn(actual(*args)))


def wrap_input(type_nm, cpp_mem_fn, wrap_fn):
    #assert(not isinstance(cpp_mem_fn, cppyy.CPPOverload))
    actual = "__" + type_nm.__name__ + "_" + cpp_mem_fn.__name__
    setattr(type_nm, actual, cpp_mem_fn)
    actual = getattr(type_nm, actual)
    setattr(type_nm, cpp_mem_fn.__name__, lambda *args: actual(args[0],wrap_fn(*args[1:])))


def wrap_overload_input(type_nm, cpp_overload, wrap_fn):
    #assert(isinstance(cpp_overload, cppyy.CPPOverload))
    actual = "__" + type_nm.__name__ + "_" + cpp_overload.__name__
    setattr(type_nm, actual, cpp_overload)
    actual = getattr(type_nm, actual)

    def inner(*args):
        wrapped_args, overload = wrap_fn(*args[1:])
        assert(isinstance(overload, str))
        return actual.__overload__(overload)(args[0], *wrapped_args)

    setattr(type_nm, cpp_overload.__name__, inner)


def unwrap_int(type_nm, cpp_mem_fn):
    unwrap(type_nm, cpp_mem_fn, lambda x: x if isinstance(x, int) else ord(x))


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
