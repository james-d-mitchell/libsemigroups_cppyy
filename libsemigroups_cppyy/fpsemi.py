"""
This file contains the interface to libsemigroups FpSemigroup; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__fpsemigroup.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.detail import (
    RandomAccessRange,
    wrap_params_and_unwrap_return_value,
)
from libsemigroups_cppyy.fpsemi_intf import replace_normal_form
from libsemigroups_cppyy.froidure_pin import install_froidure_pin_methods
from libsemigroups_cppyy.knuth_bendix import install_knuth_bendix_methods

cppyy.gbl
cppyy.gbl.libsemigroups

cppyy.cppdef(
    """
namespace libsemigroups_cppyy {
  libsemigroups::FroidurePin<libsemigroups::detail::TCE>&
  todd_coxeter_froidure_pin(
      std::shared_ptr<libsemigroups::FroidurePinBase> fp) {
    return static_cast<libsemigroups::FroidurePin<libsemigroups::detail::TCE>&>(
        *fp);
  }
}  // namespace libsemigroups_cppyy
"""
)


def FpSemigroup(*args):
    fpsemi_type = cppyy.gbl.libsemigroups.FpSemigroup
    FroidurePin = cppyy.gbl.libsemigroups.FroidurePin
    if len(args) > 1:
        raise TypeError(
            "wrong number of arguments, there must be 0 or 1, found %d" % len(args)
        )
    if len(args) == 1 and not (
        hasattr(args[0], "__iter__")
        and isinstance(args[0], FroidurePin(type(args[0][0])))
    ):
        raise TypeError(
            "the argument must be a FroidurePin object, not %s" % type(args[0]).__name__
        )

    fpsemi_type.__repr__ = lambda x: "<FpSemigroup: %d letters and %d rules>" % (
        len(x.alphabet()),
        x.nr_rules(),
    )
    fpsemi_type.rules = lambda self: [
        [x.first, x.second]
        for x in RandomAccessRange(self.cbegin_rules(), self.cend_rules())
    ]

    detail.unwrap_return_value(
        fpsemi_type, fpsemi_type.string_to_word, lambda self, x: list(x)
    )

    replace_normal_form(fpsemi_type)

    def froidure_pin_unwrapper(self, x):
        self.run()
        if self.has_knuth_bendix():
            out = cppyy.gbl.libsemigroups_cppyy.knuth_bendix_froidure_pin(x)
        elif self.has_todd_coxeter():
            out = cppyy.gbl.libsemigroups_cppyy.todd_coxeter_froidure_pin(x)
        else:
            raise RuntimeError("Cannot determine the FroidurePin type!")

        install_froidure_pin_methods(type(out))
        return out

    detail.unwrap_return_value(
        fpsemi_type, fpsemi_type.froidure_pin, froidure_pin_unwrapper
    )

    def knuth_bendix_unwrapper(self, x):
        install_knuth_bendix_methods(type(x))
        return x

    detail.unwrap_return_value(
        fpsemi_type, fpsemi_type.knuth_bendix, knuth_bendix_unwrapper
    )

    # TODO todd_coxeter_unwrapper

    return fpsemi_type(*args)
