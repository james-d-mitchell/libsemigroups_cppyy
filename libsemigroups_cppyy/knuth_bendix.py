"""
This file contains the interface to libsemigroups KnuthBendix; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__fpsemigroup__knuthbendix.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.detail import RandomAccessRange
from libsemigroups_cppyy.detail import std_if_required
from libsemigroups_cppyy.froidure_pin import install_froidure_pin_methods

cppyy.cppdef(
    """
namespace libsemigroups_cppyy {
  libsemigroups::FroidurePin<libsemigroups::detail::KBE>&
  knuth_bendix_froidure_pin(
      std::shared_ptr<libsemigroups::FroidurePinBase> fp) {
    return static_cast<libsemigroups::FroidurePin<libsemigroups::detail::KBE>&>(
        *fp);
  }
}  // namespace libsemigroups_cppyy
"""
)


def KnuthBendix():
    kb_type = cppyy.gbl.libsemigroups.fpsemigroup.KnuthBendix
    kb_type.__repr__ = lambda x: "<KnuthBendix: %d letters and %d rules>" % (
        len(x.alphabet()),
        x.nr_active_rules(),
    )
    detail.unwrap_return_value(
        kb_type, kb_type.active_rules, lambda self, x: [list(y) for y in list(x)]
    )

    def froidure_pin_unwrapper(self, x):
        out = cppyy.gbl.libsemigroups_cppyy.knuth_bendix_froidure_pin(x)
        install_froidure_pin_methods(type(out))
        return out

    detail.unwrap_return_value(kb_type, kb_type.froidure_pin, froidure_pin_unwrapper)
    detail.unwrap_return_value(kb_type, kb_type.string_to_word, lambda self, x: list(x))

    kb_type.rules = lambda self: [
        [x.first, x.second]
        for x in RandomAccessRange(self.cbegin_rules(), self.cend_rules())
    ]

    def overlap_policy_wrapper(self, t):
        if not isinstance(t, str):
            raise TypeError("the argument must be a str, not " + type(t).__name__)
        elif t == "ABC":
            return cppyy.gbl.libsemigroups.congruence_type.right
        elif t == "AB_BC":
            return cppyy.gbl.libsemigroups.congruence_type.left
        elif t == "MAX_AB_BC":
            return cppyy.gbl.libsemigroups.congruence_type.twosided
        else:
            raise ValueError('expected one of "ABC", "AB_BC", or "MAX_AB_BC"')

    def normal_form_unwrap(self, x):
        if isinstance(x, str):
            return x
        return list(x)

    def normal_form_wrap(self, x):
        if isinstance(x, list):
            return (x,), "const %svector<unsigned long>&" % std_if_required()
        return (x,), "const %sstring&" % std_if_required()

    detail.wrap_params(kb_type, kb_type.overlap_policy, overlap_policy_wrapper)
    detail.wrap_overload_params_and_unwrap_return_value(
        kb_type, kb_type.normal_form, normal_form_wrap, normal_form_unwrap
    )

    return kb_type()
