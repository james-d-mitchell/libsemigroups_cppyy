"""
This file contains the interface to libsemigroups Todd-Coxeter; see

https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__congruence__toddcoxeter.html#classlibsemigroups_1_1congruence_1_1_todd_coxeter

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
import cppyy.ll as ll


def ToddCoxeter(t):
    if not isinstance(t, str):
        raise TypeError("Expected a string as the argument")
    if t == "right":
        t = cppyy.gbl.libsemigroups.congruence_type.right
    elif t == "left":
        t = cppyy.gbl.libsemigroups.congruence_type.left
    elif t == "twosided":
        t = cppyy.gbl.libsemigroups.congruence_type.twosided
    else:
        raise ValueError('Expected one of "right", "left" and "twosided"')

    tc_type = cppyy.gbl.libsemigroups.congruence.ToddCoxeter

    def nr_gens_str(x):
        undef = ll.static_cast["size_t"](cppyy.gbl.libsemigroups.UNDEFINED)
        if x.nr_generators() == undef:
            return "-"
        else:
            return str(x.nr_generators())

    tc_type.__repr__ = (
        lambda x: "<ToddCoxeter object: %s generator" % (nr_gens_str(x))
        + "s"[: x.nr_generators() != 1]
        + " and %d pair" % (x.nr_generating_pairs())
        + "s"[: x.nr_generating_pairs() != 1]
        + ">"
    )

    def wrap_strategy(*args):
        if len(args) == 1:
            return [args[0]], ""
        overload = "libsemigroups::congruence::ToddCoxeter::policy::strategy"
        if len(args) != 2:
            raise TypeError("Expected exactly 1 argument")
        if not isinstance(args[1], str):
            raise TypeError("Expected a string as the argument")
        if args[1] == "felsch":
            return [args[0], tc_type.policy.strategy.felsch], overload
        elif args[1] == "hlt":
            return [args[0], tc_type.policy.strategy.hlt], overload
        elif args[1] == "random":
            return [args[0], tc_type.policy.strategy.random], overload
        else:
            raise ValueError('Expected one of "felsch", "hlt" and "random"')

    def wrap_standardize(*args):
        if len(args) == 0:
            return [None], ""
        # overload is the type of the parameter of the cpp overload
        overload = "libsemigroups::congruence::ToddCoxeter::order"
        if len(args) != 1:
            raise TypeError("Expected exactly 1 argument")
        if not isinstance(args[0], str):
            raise TypeError("Expected a string as the argument")
        if args[0] == "lex":
            return [tc_type.order.lex], overload
        elif args[0] == "shortlex":
            return [tc_type.order.shortlex], overload
        elif args[0] == "recursive":
            return [tc_type.order.recursive], overload
        else:
            raise ValueError('Expected "lex" as argument')

    def int_to_kind(self, n):
        if n == 0:
            return "left"
        elif n == 1:
            return "right"
        else:
            return "twosided"

    def int_to_strategy(self, n):
        if isinstance(n, cppyy.gbl.libsemigroups.congruence.ToddCoxeter):
            return n
        elif n == 0:
            return "hlt"
        elif n == 1:
            return "felsch"
        elif n == 2:
            return "random"
        else:
            assert False

    def fp_repr_method(self):  # from froidure_pin.py
        try:
            element_type_str = "<%s>" % type(self).element_type.short_name
        except AttributeError:
            element_type_str = ""
        plural = "s" if self.nr_generators() > 1 else ""
        return "<FroidurePin{0} object with {1} generator{2} at {3}>".format(
            element_type_str, self.nr_generators(), plural, hex(id(self))
        )

    detail.wrap_overload_params_and_unwrap_return_value(
        tc_type, tc_type.strategy, wrap_strategy, int_to_strategy
    )

    detail.wrap_overload_params(tc_type, tc_type.standardize, wrap_standardize)

    detail.unwrap_return_value(tc_type, tc_type.kind, int_to_kind)
    detail.unwrap_return_value(
        tc_type, tc_type.class_index_to_word, lambda self, x: list(x)
    )

    return tc_type(t)
