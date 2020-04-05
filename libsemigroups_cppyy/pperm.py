"""
This file contains the interface to libsemigroups partial perms; see

    https://libsemigroups.readthedocs.io/en/latest/api/pperm.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.adapters import Degree, Product


def PartialPerm(*args):
    if len(args) == 1:
        pperm_type = cppyy.gbl.libsemigroups.PPermHelper(len(args[0])).type
        ## Workaround CPPYY issue
        if pperm_type.__module__ == "cppyy.gbl.HPCombi":
            images = list(args[0])
            images += range(len(images), 16)
            ret = pperm_type(images)
        else:
            ret = pperm_type(*args)
    elif len(args) == 3:
        if not isinstance(args[2], int):
            raise TypeError("the third parameter must be an integer")
        pperm_type = cppyy.gbl.libsemigroups.PPermHelper(args[2]).type
        ret = pperm_type(*args)
    else:
        raise TypeError(
            "wrong number of arguments, there must 1 or 3, found %d" % len(args)
        )

    pperm_type.__pow__ = detail.generic_pow
    pperm_type.__mul__ = Product
    pperm_type.dom = lambda x: [y for y in range(Degree(x)) if ord(x[y]) != 255]
    pperm_type.ran = lambda x: [ord(x[y]) for y in range(Degree(x)) if ord(x[y]) != 255]
    pperm_type.__repr__ = lambda x: "PartialPerm(%s, %s, %d)" % (
        x.dom(),
        x.ran(),
        Degree(x),
    )
    if pperm_type.__module__ == "cppyy.gbl.HPCombi":
        pperm_type.rank = pperm_type.rank
    else:
        pperm_type.rank = pperm_type.crank
    pperm_type.short_name = "PartialPerm"
    return ret
