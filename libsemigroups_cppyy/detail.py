"""
This file contains some internal stuff for the cppyy bindings.
"""

import cppyy

from libsemigroups_cppyy.adapters import One
from libsemigroups_cppyy.exception import LibsemigroupsCppyyException

__STD = ""
__STD_DEFINED = False


def std_if_required():
    global __STD, __STD_DEFINED
    if not __STD_DEFINED:
        __STD_DEFINED = True
        if not cppyy.cppdef("void dummy(std::string) {}"):
            cppyy.cppdef("void dummy(string) {}")
        try:
            cppyy.gbl.dummy.__overload__("std::string")
            __STD = "std::"
        except:
            pass
        del cppyy.gbl.dummy
    return __STD


def __new_cpp_mem_fn_name(type_nm, cpp_mem_fn):
    # make up a new name for "cpp_mem_fn"
    return "__" + type_nm.__name__ + "_" + cpp_mem_fn.__name__


def __call_and_catch(type_nm, wrap_params_fn, cpp_mem_fn, unwrap_return_fn):
    def the_function(*args):
        wrapped_params = wrap_params_fn(*args)
        # TODO add check that wrapped_params is a tuple
        if not hasattr(wrapped_params, "__iter__"):
            wrapped_params = [wrapped_params]
        try:
            return unwrap_return_fn(
                args[0],
                getattr(args[0], __new_cpp_mem_fn_name(type_nm, cpp_mem_fn))(
                    *wrapped_params
                ),
            )
        except Exception as e:
            raise LibsemigroupsCppyyException(e) from None

    return the_function


def __call_overload_and_catch(type_nm, wrap_params_fn, cpp_mem_fn, unwrap_return_fn):
    def the_function(*args):
        wrapped_params, overload = wrap_params_fn(*args)
        if not isinstance(wrapped_params, tuple):
            raise TypeError("the function wrapping parameters must return a tuple")
        try:
            return unwrap_return_fn(
                args[0],
                getattr(
                    args[0], __new_cpp_mem_fn_name(type_nm, cpp_mem_fn)
                ).__overload__(overload)(*wrapped_params),
            )
        except Exception as e:
            raise LibsemigroupsCppyyException(e) from None

    return the_function


def __do_nothing_to_params(self, *args):
    return args


def __do_nothing_to_return_value(self, args):
    return args


def __replace_mem_fn(type_nm, cpp_mem_fn, replacement_fn):
    """
    """
    cpp_mem_fn_new_name = __new_cpp_mem_fn_name(type_nm, cpp_mem_fn)
    # bind the "cpp_mem_fn" to its new name "cpp_mem_fn_new_name"
    setattr(type_nm, cpp_mem_fn_new_name, cpp_mem_fn)
    # install new version of "cpp_mem_fn.__name__" that calls the original
    # version stored in "cpp_mem_fn_new_name"
    setattr(type_nm, cpp_mem_fn.__name__, replacement_fn)


def unwrap_return_value(type_nm, cpp_mem_fn, unwrap_return_fn):
    __replace_mem_fn(
        type_nm,
        cpp_mem_fn,
        __call_and_catch(type_nm, __do_nothing_to_params, cpp_mem_fn, unwrap_return_fn),
    )


def wrap_params_and_unwrap_return_value(
    type_nm, cpp_mem_fn, wrap_params_fn, unwrap_return_fn
):
    __replace_mem_fn(
        type_nm,
        cpp_mem_fn,
        __call_and_catch(type_nm, wrap_params_fn, cpp_mem_fn, unwrap_return_fn),
    )


def wrap_params(type_nm, cpp_mem_fn, wrap_params_fn):
    __replace_mem_fn(
        type_nm,
        cpp_mem_fn,
        __call_and_catch(
            type_nm, wrap_params_fn, cpp_mem_fn, __do_nothing_to_return_value
        ),
    )


def wrap_overload_params(type_nm, cpp_mem_fn, wrap_params_fn):
    __replace_mem_fn(
        type_nm,
        cpp_mem_fn,
        __call_overload_and_catch(
            type_nm, wrap_params_fn, cpp_mem_fn, __do_nothing_to_return_value
        ),
    )


def wrap_overload_params_and_unwrap_return_value(
    type_nm, cpp_mem_fn, wrap_params_fn, unwrap_return_fn
):
    __replace_mem_fn(
        type_nm,
        cpp_mem_fn,
        __call_overload_and_catch(
            type_nm, wrap_params_fn, cpp_mem_fn, unwrap_return_fn
        ),
    )


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


class ForwardRange:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def __repr__(self):
        return "<forward range at {0}>".format(hex(id(self)), len(self))

    def __iter__(self):
        self.it = self.first
        return self

    def __next__(self):
        if self.it != self.last:
            reference = self.it.__deref__()
            # copy "reference" since it may be a reference
            # Can't currently check this because
            # cppyy.gbl.std.is_reference(S.cbegin_rules().__deref__()).value
            # returns 0 at present
            out = type(reference)(reference)
            cppyy.gbl.std.advance(self.it, 1)
            return out
        else:
            raise StopIteration


class RandomAccessRange:
    # TODO subclass ForwardRange?
    # TODO add keyword arg unwrap_return_value for KnuthBendix::rules
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
