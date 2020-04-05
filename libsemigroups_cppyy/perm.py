"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/api/perm.html

for further details.
"""

import cppyy

import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.adapters import Degree, Product


def Permutation(images):
    perm_type = cppyy.gbl.libsemigroups.PermHelper(len(images)).type
    perm_type.__pow__ = detail.generic_pow
    perm_type.__mul__ = Product
    perm_type.__repr__ = lambda x: "Permutation(%s)" % (x.ran())
    perm_type.ran = lambda x: [
        x[y] if isinstance(x[y], int) else ord(x[y]) for y in range(Degree(x))
    ]
    ## Workaround CPPYY issue
    if perm_type.__module__ == "cppyy.gbl.HPCombi":
        images = list(images)
        images += range(len(images), 16)
    perm_type.short_name = "Permutation"
    return perm_type(images)
