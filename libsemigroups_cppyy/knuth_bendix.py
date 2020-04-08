"""
This file contains the interface to libsemigroups KnuthBendix; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__fpsemigroup__knuthbendix.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail

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
    # FIXME these don't work
    # detail.unwrap(kb_type, kb_type.cbegin_rules, lambda self, x: iter(x))
    # detail.unwrap(kb_type, kb_type.cend_rules, lambda self, x: iter(x))
    detail.unwrap_return_value(
        kb_type,
        kb_type.froidure_pin,
        lambda self, x: cppyy.gbl.libsemigroups_cppyy.knuth_bendix_froidure_pin(x),
    )

    return kb_type()
