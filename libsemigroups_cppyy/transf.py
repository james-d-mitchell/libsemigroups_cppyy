"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/api/transf.html

for further details.
"""

import cppyy

import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.adapters import Degree, Product


def Transformation(images):
    transf_type = cppyy.gbl.libsemigroups.TransfHelper(len(images)).type
    transf_type.__pow__ = detail.generic_pow
    transf_type.__mul__ = Product
    transf_type.__repr__ = lambda x: "Transformation(%s)" % (x.ran())
    transf_type.short_name = "Transformation"
    transf_type.ran = lambda x: [
        x[y] if isinstance(x[y], int) else ord(x[y]) for y in range(Degree(x))
    ]
    ## Workaround CPPYY issue
    if transf_type.__module__ == "cppyy.gbl.HPCombi":
        images = list(images)
        images += range(len(images), 16)
    return transf_type(images)
