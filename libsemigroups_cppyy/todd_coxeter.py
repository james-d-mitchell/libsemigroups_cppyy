"""
This file contains the interface to libsemigroups Todd-Coxeter; see

https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__congruence__toddcoxeter.html#classlibsemigroups_1_1congruence_1_1_todd_coxeter

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
import cppyy.ll as ll


def ToddCoxeter(*args):
    tc_type = cppyy.gbl.libsemigroups.congruence.ToddCoxeter
    fp_type = cppyy.gbl.libsemigroups.FroidurePin
    kb_type = cppyy.gbl.libsemigroups.fpsemigroup.KnuthBendix
    undef = ll.static_cast["size_t"](cppyy.gbl.libsemigroups.UNDEFINED)

    if len(args) > 2 or len(args) == 0:
        raise TypeError(
            "wrong number of arguments, there must be 1 or 2, found %d" % len(args)
        )
    if len(args) == 1 and not isinstance(args[0], str):
        raise TypeError(
            "invalid argument, expected a string as first argument, not %s"
            % type(args[0]).__name__
        )
    if len(args) == 2:
        if not (
            (
                hasattr(args[1], "__iter__")
                and isinstance(args[1], fp_type(type(args[1][0])))
            )
            or isinstance(args[1], kb_type)  # and len(args[1].alphabet()) > 0)
            or isinstance(args[1], tc_type)  # and args[1].nr_generators() > 0)
        ):
            raise TypeError(
                "the second argument must be a FroidurePin object, ToddCoxeter object with at least one generator, or a KnuthBendix object with non-empty alphabet, not %s"
                % type(args[1]).__name__
            )
        if isinstance(args[1], kb_type) and len(args[1].alphabet()) == 0:
            raise TypeError(
                "invalid argument, the KnuthBendix object provided as the second argument must have non-empty alphabet"
            )
        if isinstance(args[1], tc_type):
            if args[1].kind() != "twosided" and args[1].kind() != args[0]:
                raise TypeError(
                    "allowable combinations between first argument and handedness of the ToddCoxeter object of the second object are: left/twosided, right/twosided, twosided/twosided, left/left, right/right, found {0}/{1}".format(
                        args[0], args[1].kind()
                    )
                )
            if args[1].nr_generators() == undef:
                raise TypeError(
                    "the ToddCoxeter object of the second argument must have at least one generator set"
                )

    if args[0] == "right":
        t = cppyy.gbl.libsemigroups.congruence_type.right
    elif args[0] == "left":
        t = cppyy.gbl.libsemigroups.congruence_type.left
    elif args[0] == "twosided":
        t = cppyy.gbl.libsemigroups.congruence_type.twosided
    else:
        raise ValueError(
            'invalid argument, expected one of "right", "left" and "twosided", found %s'
            % args[0]
        )

    tc_type.__repr__ = lambda x: "<ToddCoxeter object {0} generator{1} and {2} pair{3} at {4}>".format(
        x.nr_generators() if x.nr_generators() != undef else "-",
        "s"[: x.nr_generators() != 1],
        x.nr_generating_pairs(),
        "s"[: x.nr_generating_pairs() != 1],
        hex(id(x)),
    )

    def wrap_strategy(self, *args):
        if len(args) == 0:
            return tuple(), ""
        overload = "libsemigroups::congruence::ToddCoxeter::policy::strategy"
        if len(args) != 1:
            raise TypeError("invalid argument, expected 0 or 1 arguments")
        if not isinstance(args[0], str):
            raise TypeError("invalid argument, expected a string or no argument")
        if args[0] == "felsch":
            return (tc_type.policy.strategy.felsch,), overload
        elif args[0] == "hlt":
            return (tc_type.policy.strategy.hlt,), overload
        elif args[0] == "random":
            return (tc_type.policy.strategy.random,), overload
        else:
            raise ValueError(
                'invalid argument, expected one of "felsch", "hlt" and "random", but found %s'
                % args[0]
            )

    def wrap_froidure_pin_policy(self, *args):
        if len(args) == 0:
            return tuple(), ""
        overload = "libsemigroups::congruence::ToddCoxeter::policy::froidure_pin"
        if len(args) != 1:
            raise TypeError("invalid argument, expected 0 or 1 arguments")
        if not isinstance(args[0], str):
            raise TypeError("invalid argument, expected a string or no argument")
        if args[0] == "none":
            return (tc_type.policy.froidure_pin.none,), overload
        elif args[0] == "use_relations":
            return (tc_type.policy.froidure_pin.use_relations,), overload
        elif args[0] == "use_cayley_graph":
            return (tc_type.policy.froidure_pin.use_cayley_graph,), overload
        else:
            raise ValueError(
                'invalid argument, expected one of "none", "use_relations" and "use_cayley_graph", but found %s'
                % args[0]
            )

    def wrap_standardize(self, x):
        if isinstance(x, str):
            # overload is the type of the parameter of the cpp overload
            overload = "libsemigroups::congruence::ToddCoxeter::order"
            if x == "lex":
                return (tc_type.order.lex,), overload
            elif x == "shortlex":
                return (tc_type.order.shortlex,), overload
            elif x == "recursive":
                return (tc_type.order.recursive,), overload
            else:
                raise ValueError(
                    'expected one of "lex", "shortlex" and "recursive", but found %s'
                    % x
                )
        elif isinstance(x, bool):
            return (x,), "bool"
        else:
            raise TypeError("expected a string or bool, not %s" % type(x).__name__)

    def int_to_kind(self, n):
        if n == 0:
            return "left"
        elif n == 1:
            return "right"
        elif n == 2:
            return "twosided"
        else:
            assert False

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

    def int_to_froidure_pin_policy(self, n):
        if isinstance(n, tc_type):
            return n
        elif n == 0:
            return "none"
        elif n == 1:
            return "use_relations"
        elif n == 2:
            return "use_cayley_graph"
        else:
            assert False

    detail.wrap_overload_params_and_unwrap_return_value(
        tc_type, tc_type.strategy, wrap_strategy, int_to_strategy
    )

    detail.wrap_overload_params_and_unwrap_return_value(
        tc_type,
        tc_type.froidure_pin_policy,
        wrap_froidure_pin_policy,
        int_to_froidure_pin_policy,
    )

    detail.wrap_overload_params(tc_type, tc_type.standardize, wrap_standardize)

    detail.unwrap_return_value(tc_type, tc_type.kind, int_to_kind)
    detail.unwrap_return_value(
        tc_type, tc_type.class_index_to_word, lambda self, x: list(x)
    )

    tc_type.generating_pairs = lambda self: [
        [list(x.first), list(x.second)]
        for x in detail.RandomAccessRange(
            self.cbegin_generating_pairs(), self.cend_generating_pairs()
        )
    ]

    tc_type.normal_forms = lambda self: [
        list(x)
        for x in detail.RandomAccessRange(
            self.cbegin_normal_forms(), self.cend_normal_forms()
        )
    ]

    tc_type.non_trivial_classes = lambda self: [
        [list(y) for y in list(x)]
        for x in detail.RandomAccessRange(self.cbegin_ntc(), self.cend_ntc())
    ]

    if len(args) == 1:
        return tc_type(t)
    else:
        return tc_type(t, args[1])
