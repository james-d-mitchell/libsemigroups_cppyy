"""
This file contains the interface to libsemigroups boolean matrices, see:

    https://libsemigroups.readthedocs.io/en/latest/bmat.html

for further details.
"""

import cppyy
from cppyy.gbl import std
import libsemigroups_cppyy.detail as detail

cppyy.gbl
cppyy.gbl.libsemigroups

from cppyy.gbl.libsemigroups import BMat8
from cppyy.gbl.libsemigroups import BMatHelper


def __bits(n):
    return [int(digit) for digit in format(n, "#010b")[2:]]


BMat8.__repr__ = lambda x: cppyy.gbl.libsemigroups.detail.to_string(x)
detail.unwrap_return_value(
    BMat8, BMat8.rows, lambda self, x: [__bits(ord(y)) for y in x]
)


def BooleanMat(mat):
    out = std.vector(std.vector("bool"))()
    for row in mat:
        v = std.vector("bool")()
        for x in row:
            v.push_back(x)
        out.push_back(v)
    bmat_type = cppyy.gbl.libsemigroups.BMatHelper(len(mat)).type
    bmat_type.short_name = "BooleanMat"
    bmat_type.__pow__ = detail.generic_pow
    return bmat_type(out)
