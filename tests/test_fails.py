import unittest
from libsemigroups_cppyy import FroidurePin, FpSemigroup, Transformation, ReportGuard
import cppyy.gbl.std as std


class TestBug(unittest.TestCase):
    def test_bug1_works_yes(self):
        ReportGuard(False)
        # S = FpSemigroup()
        # S.set_alphabet("01")

        # S.add_rule("000", "0")
        # S.add_rule("1111", "1")
        # S.add_rule("01110", "00")
        # S.add_rule("1001", "11")
        # S.add_rule("001010101010", "00")
        # S.run()
        # S.rules()

        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        S.run()
        self.assertEqual(std.distance(S.cbegin(), S.cend()), S.size())

    def test_bug1_works_zno(self):
        S = FpSemigroup()
        S.set_alphabet("01")

        S.add_rule("000", "0")
        S.add_rule("1111", "1")
        S.add_rule("01110", "00")
        S.add_rule("1001", "11")
        S.add_rule("001010101010", "00")
        S.run()
        S.rules()

        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        self.assertEqual(S.size(), 4)
        self.assertEqual(std.distance(S.cbegin(), S.cend()), S.size())
