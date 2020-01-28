"""
This file contains the interface to libsemigroups FpSemigroup; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__fpsemigroup.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail

cppyy.gbl
cppyy.gbl.libsemigroups


def FpSemigroup():
    fpsemi_type = cppyy.gbl.libsemigroups.FpSemigroup
    fpsemi_type.__repr__ = lambda x: "<FpSemigroup: %d letters and %d rules>" % (
        len(x.alphabet()),
        x.nr_rules(),
    )
    return fpsemi_type()
