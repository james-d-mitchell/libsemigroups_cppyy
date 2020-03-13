"""
This file contains the interface to libsemigroups Todd-Coxeter; see

https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__congruence__toddcoxeter.html#classlibsemigroups_1_1congruence_1_1_todd_coxeter

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail

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
    return cppyy.gbl.libsemigroups.congruence.ToddCoxeter(t)
