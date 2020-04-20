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
        raise TypeError('Expected a string as the argument')
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
        lambda x: "<ToddCoxeter object: %s generator" % (nr_gens_str(x)) +
        "s"[:x.nr_generators() != 1] + " and %d pair" % (x.nr_generating_pairs()) +
        "s"[:x.nr_generating_pairs() != 1] + ">"
    )

    def wrap_strategy(*args):
        if len(args) == 0:
            return [None], "";
        overload = "libsemigroups::congruence::ToddCoxeter::policy::strategy"
        if len(args) != 1:
            raise TypeError('Expected exactly 1 argument')
        if not isinstance(args[0], str):
            raise TypeError('Expected a string as the argument')
        if args[0] == "felsch":
            return [tc_type.policy.strategy.felsch], overload
        elif args[0] == "hlt":
            return [tc_type.policy.strategy.hlt], overload
        elif args[0] == "random":
            return [tc_type.policy.strategy.random], overload
        else:
            raise ValueError('Expected one of "felsch", "hlt" and "random"')

    def wrap_standardize(*args):
        if len(args) == 0:
            return [None], "";
        overload = "libsemigroups::congruence::ToddCoxeter::order"
        if len(args) != 1:
            raise TypeError('Expected exactly 1 argument')
        if not isinstance(args[0], str):
            raise TypeError('Expected a string as the argument')
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

    detail.wrap_overload_input(
        tc_type, tc_type.strategy, wrap_strategy
    )
    detail.wrap_overload_input(
        tc_type, tc_type.standardize, wrap_standardize
    )
    
    detail.unwrap_return_value(
        tc_type, tc_type.kind, int_to_kind
    )
    detail.unwrap_return_value(
        tc_type, tc_type.class_index_to_word, lambda self, x: list(x)
    )
    return tc_type(t)
