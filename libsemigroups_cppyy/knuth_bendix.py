"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__fpsemigroup__knuthbendix.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail


def KnuthBendix():
    kb_type = cppyy.gbl.libsemigroups.fpsemigroup.KnuthBendix
    kb_type.__repr__ = lambda x: "<KnuthBendix: %d letters and %d rules>" % (
        len(x.alphabet()),
        x.nr_active_rules(),
    )
    detail.unwrap(kb_type, kb_type.active_rules, lambda x: [list(y) for y in list(x)])
    detail.unwrap(kb_type, kb_type.cbegin_rules, lambda x: iter(x))
    detail.unwrap(kb_type, kb_type.cend_rules, lambda x: iter(x))

    return kb_type()
