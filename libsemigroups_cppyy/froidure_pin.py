"""
This file contains the interface to the FroidurePin class in libsemigroups; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__froidurepin.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
import networkx

from libsemigroups_cppyy.detail import RandomAccessRange, ForwardRange
from libsemigroups_cppyy.detail import method_causes_segfault

from cppyy.gbl.std import vector


def install_froidure_pin_methods(froidure_pin_type):
    detail.unwrap_return_value_to_int(froidure_pin_type, froidure_pin_type.left)
    detail.unwrap_return_value_to_int(froidure_pin_type, froidure_pin_type.right)
    detail.unwrap_return_value_to_int(
        froidure_pin_type, froidure_pin_type.nr_generators
    )
    froidure_pin_type.__iter__ = detail.runner__iter__
    froidure_pin_type.__next__ = detail.runner__next__
    froidure_pin_type.idempotents = lambda self: RandomAccessRange(
        self.cbegin_idempotents(), self.cend_idempotents()
    )
    froidure_pin_type.sorted_elements = lambda self: RandomAccessRange(
        self.cbegin_sorted(), self.cend_sorted()
    )
    detail.unwrap_return_value(
        froidure_pin_type, froidure_pin_type.factorisation, lambda self, x: list(x)
    )
    detail.unwrap_return_value(
        froidure_pin_type,
        froidure_pin_type.minimal_factorisation,
        lambda self, x: list(x),
    )
    # operator[] with an out of bounds value causes a seg fault
    froidure_pin_type.__getitem__ = froidure_pin_type.at

    def repr_method(self):
        try:
            element_type_str = "<%s>" % type(self).element_type.short_name
        except AttributeError:
            element_type_str = ""
        plural = "s" if self.nr_generators() > 1 else ""
        return "<FroidurePin{0} object with {1} generator{2} at {3}>".format(
            element_type_str, self.nr_generators(), plural, hex(id(self))
        )

    froidure_pin_type.__repr__ = repr_method

    froidure_pin_type.rules = lambda self: [
        [list(x.first), list(x.second)]
        for x in ForwardRange(self.cbegin_rules(), self.cend_rules())
    ]

    # JDM the following didn't work for whatever reason:
    method_causes_segfault(froidure_pin_type, "add_generators")
    method_causes_segfault(froidure_pin_type, "copy_add_generators")
    method_causes_segfault(froidure_pin_type, "closure")
    method_causes_segfault(froidure_pin_type, "copy_closure")
    method_causes_segfault(froidure_pin_type, "next_relation")


def FroidurePin(*args):
    if len(args) == 1 and isinstance(args[0], cppyy.gbl.libsemigroups.FroidurePinBase):
        return type(args[0])(args[0])
    elif len(args) == 1 and isinstance(args[0], list):
        gens = args[0]
    else:
        gens = [*args]

    types = {type(g) for g in gens}
    if len(types) > 1:
        raise ValueError("the generators are not all of the same type")
    # TODO the following can result in python seg faulting if it isn't possible
    # to create an object of this type. Fix this somehow?
    froidure_pin_type = cppyy.gbl.libsemigroups.FroidurePin(types.pop())
    install_froidure_pin_methods(froidure_pin_type)
    return froidure_pin_type(gens)


def right_cayley(S):
    G = networkx.DiGraph()
    for i in range(S.size()):
        for j in range(S.nr_generators()):
            G.add_edge(str(S.factorisation(i)), str(S.factorisation(S.right(i, j))))
    return G


def left_cayley(S):
    G = networkx.DiGraph()
    for i in range(S.size()):
        for j in range(S.nr_generators()):
            G.add_edge(str(S.factorisation(i)), str(S.factorisation(S.left(i, j))))
    return G
