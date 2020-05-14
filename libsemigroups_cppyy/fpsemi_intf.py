"""
This module contains common wrapping/unwrapping methods for classes derived
from FpSemigroupInterface.
"""

from libsemigroups_cppyy.detail import (
    wrap_overload_params_and_unwrap_return_value,
    std_if_required,
)


def __normal_form_unwrap(self, x):
    if isinstance(x, str):
        return x
    return list(x)


def __normal_form_wrap(self, x):
    if isinstance(x, list):
        return (x,), "const %svector<unsigned long>&" % std_if_required()
    return (x,), "const %sstring&" % std_if_required()


def replace_normal_form(fpsemi_intf_type):
    wrap_overload_params_and_unwrap_return_value(
        fpsemi_intf_type,
        fpsemi_intf_type.normal_form,
        __normal_form_wrap,
        __normal_form_unwrap,
    )
