import unittest
from libsemigroups_cppyy import (
    KnuthBendix,
    LibsemigroupsException,
    ReportGuard,
    LibsemigroupsCppyyException,
    FroidurePin,
    Transformation,
    milliseconds,
)
import cppyy.ll as ll
from fpsemi_intf import (
    check_validation,
    check_initialisation,
    check_operators,
    check_attributes,
    check_converters,
)


class TestKnuth(unittest.TestCase):
    def test_one(self):
        ReportGuard(False)
        kb = KnuthBendix()

        kb.set_alphabet("abcd")
        kb.add_rule("cacac", "aacaa")
        kb.add_rule("acaca", "ccacc")
        kb.add_rule("ada", "bbcbb")
        kb.add_rule("bcb", "aadaa")
        kb.add_rule("aaaa", "")
        kb.add_rule("ab", "")
        kb.add_rule("ba", "")
        kb.add_rule("cd", "")
        kb.add_rule("dc", "")
        kb.run()

        self.assertTrue(kb.confluent())
        self.assertEqual(kb.nr_active_rules(), 10)
        self.assertEqual(
            kb.active_rules(),
            [
                ["ab", ""],
                ["ba", ""],
                ["bb", "aa"],
                ["ca", "bd"],
                ["cb", "ad"],
                ["cd", ""],
                ["da", "bc"],
                ["db", "ac"],
                ["dc", ""],
                ["aaa", "b"],
            ],
        )
        self.assertEqual(
            kb.rewrite("abbbbbbbbbbbadddddddddddddddacccccccccccc"),
            "aaccccccccccccccccccccccccccc",
        )

        self.assertFalse(kb.equal_to("abbbbbbbbbbbadddddddddddddddacccccccccccc", "a"))

    def test_two(self):
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("ab")
        kb.add_rule("aaa", "a")
        kb.add_rule("bbbb", "b")
        kb.add_rule("ba", "aab")

        self.assertEqual(kb.froidure_pin().size(), 11)
        # work around change in libsemigroups
        try:
            self.assertEqual(kb.froidure_pin()[10].string(kb), "babb")
        except:
            self.assertEqual(
                ll.static_cast["std::string"](kb.froidure_pin()[10]), "babb"
            )

    def test_validation(self):
        check_validation(self, KnuthBendix)

    def test_converters(self):
        check_converters(self, KnuthBendix)

    def test_initialisation(self):
        check_initialisation(self, KnuthBendix)

        kb = KnuthBendix()
        kb.set_alphabet("abB")
        kb.set_identity("")
        kb.set_inverses("aBb")

        kb.add_rule("bb", "B")
        kb.add_rule("BaBa", "abab")
        self.assertEqual(kb.size(), 24)

    def test_attributes(self):
        # Check FpSemigroupInterface general attributes
        check_attributes(self, KnuthBendix)
        # Check KnuthBendix specific attributes
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("abB")
        kb.set_identity("")
        kb.set_inverses("aBb")

        kb.add_rule("bb", "B")
        kb.add_rule("BaBa", "abab")

        self.assertFalse(kb.confluent())
        kb.run()
        self.assertTrue(kb.confluent())

        self.assertEqual(
            kb.active_rules(),
            [
                ["BB", "b"],
                ["Bb", ""],
                ["aa", ""],
                ["bB", ""],
                ["bb", "B"],
                ["BaBa", "abab"],
                ["baba", "aBaB"],
                ["BabaB", "baBab"],
                ["Babab", "baBa"],
                ["baBaB", "Baba"],
                ["baBaba", "abaBab"],
            ],
        )
        self.assertEqual(kb.nr_active_rules(), 11)

    def test_settings(self):
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("abB")
        kb.set_identity("")
        kb.set_inverses("aBb")

        kb.add_rule("bb", "B")
        kb.add_rule("BaBa", "abab")
        self.assertEqual(kb.check_confluence_interval(10), kb)
        self.assertEqual(kb.max_overlap(10), kb)

        with self.assertRaises(ValueError):
            kb.max_overlap(-10)

        kb = KnuthBendix()
        kb.set_alphabet("abc")

        kb.add_rule("aa", "")
        kb.add_rule("bc", "")
        kb.add_rule("bbb", "")
        kb.add_rule("ababababababab", "")
        kb.add_rule("abacabacabacabacabacabacabacabac", "")

        kb.max_rules(100)
        kb.run()
        self.assertGreaterEqual(kb.nr_active_rules(), 100)
        self.assertEqual(kb.overlap_policy("ABC"), kb)
        self.assertEqual(kb.overlap_policy("AB_BC"), kb)
        self.assertEqual(kb.overlap_policy("MAX_AB_BC"), kb)

        with self.assertRaises(TypeError):
            kb.overlap_policy(-10)

        with self.assertRaises(ValueError):
            kb.overlap_policy("AVC")

    def test_running_and_state(self):
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("abc")
        kb.add_rule("aa", "")
        kb.add_rule("bc", "")
        kb.add_rule("bbb", "")
        kb.add_rule("ababababababab", "")
        kb.add_rule("abacabacabacabacabacabacabacabac", "")
        kb.run_for(milliseconds(500))

        self.assertTrue(kb.stopped())
        self.assertFalse(kb.finished())
        self.assertFalse(kb.running())
        self.assertTrue(kb.started())
        self.assertFalse(kb.stopped_by_predicate())
        self.assertTrue(kb.timed_out())

        kb = KnuthBendix()
        kb.set_alphabet("abc")
        kb.add_rule("aa", "")
        kb.add_rule("bc", "")
        kb.add_rule("bbb", "")
        kb.add_rule("ababababababab", "")
        kb.add_rule("abacabacabacabacabacabacabacabac", "")

        kb.run_until(lambda: kb.nr_active_rules() > 100)

        self.assertTrue(kb.stopped())
        self.assertFalse(kb.finished())
        self.assertFalse(kb.running())
        self.assertTrue(kb.started())
        self.assertTrue(kb.stopped_by_predicate())
        self.assertFalse(kb.timed_out())

    def test_operators(self):
        check_operators(self, KnuthBendix)
