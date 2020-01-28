import unittest
from libsemigroups_cppyy import FpSemigroup, ReportGuard


class TestFpSemigroup(unittest.TestCase):
    def test_all(self):
        ReportGuard(False)
        S = FpSemigroup()
        S.set_alphabet("abcde")
        S.set_identity("e")
        S.add_rule("cacac", "aacaa")
        S.add_rule("acaca", "ccacc")
        S.add_rule("ada", "bbcbb")
        S.add_rule("bcb", "aadaa")
        S.add_rule("aaaa", "e")
        S.add_rule("ab", "e")
        S.add_rule("ba", "e")
        S.add_rule("cd", "e")
        S.add_rule("dc", "e")
        S.run()

        self.assertEqual(S.nr_rules(), 18)
        # self.assertEqual()
        self.assertTrue(
            S.equal_to("abbbbbbbbbbbadddddddddddddddacccccccccccc",
            "aaccccccccccccccccccccccccccc"),
        )

        self.assertFalse(S.equal_to("abbbbbbbbbbbadddddddddddddddacccccccccccc", "a"))
