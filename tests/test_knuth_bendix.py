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
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("ab")

        with self.assertRaises(TypeError):
            kb.validate_letter("c")
        try:
            kb.validate_letter("a")
        except Exception as e:
            self.fail(
                "unexpected exception raised for KnuthBendix::validate_letter: " + e
            )

        with self.assertRaises(LibsemigroupsException):
            kb.validate_letter(3)
        try:
            kb.validate_letter(0)
        except Exception as e:
            self.fail(
                "unexpected exception raised for KnuthBendix::validate_letter: " + e
            )

        with self.assertRaises(TypeError):
            kb.validate_word("abc")
        try:
            kb.validate_word("abab")
        except Exception as e:
            self.fail(
                "unexpected exception raised for KnuthBendix::validate_letter: " + e
            )

        with self.assertRaises(TypeError):
            kb.validate_word([0, 1, 2])
        try:
            kb.validate_word([0, 1, 0, 1])
        except Exception as e:
            self.fail(
                "unexpected exception raised for KnuthBendix::validate_letter: " + e
            )

    def test_converters(self):
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("ba")
        self.assertEqual(kb.char_to_uint(ord("a")), 1)
        self.assertEqual(kb.char_to_uint(ord("b")), 0)

        self.assertEqual(kb.string_to_word("ab"), [1, 0])
        self.assertEqual(kb.string_to_word("aaaaaa"), [1] * 6)
        with self.assertRaises(LibsemigroupsCppyyException):
            kb.string_to_word("c")

        self.assertEqual(kb.uint_to_char(0), "b")
        self.assertEqual(kb.uint_to_char(1), "a")
        with self.assertRaises(LibsemigroupsException):
            kb.uint_to_char(2)

        self.assertEqual(kb.word_to_string([1, 0]), "ab")
        self.assertEqual(kb.word_to_string([1] * 6), "a" * 6)
        with self.assertRaises(LibsemigroupsException):
            kb.word_to_string([2])

    def test_initialisation(self):
        ReportGuard(False)
        kb = KnuthBendix()
        kb.set_alphabet("ba")
        kb.add_rule([0, 1], [1, 0])

        with self.assertRaises(TypeError):
            kb.add_rule([0, 1], [2])

        S = FroidurePin(Transformation([1, 2, 0]), Transformation([1, 0, 2]))
        kb.add_rules(S)
        self.assertEqual(kb.size(), 2)

        kb = KnuthBendix()
        kb.set_alphabet("abB")
        kb.set_identity("")
        kb.set_inverses("aBb")

        kb.add_rule("bb", "B")
        kb.add_rule("BaBa", "abab")
        self.assertEqual(kb.size(), 24)

        kb = KnuthBendix()
        kb.set_alphabet(1)
        kb.set_identity(0)
        self.assertEqual(kb.size(), 1)

    def test_attributes(self):
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
            kb.rules(),
            [
                ["aa", ""],
                ["aa", ""],
                ["bB", ""],
                ["Bb", ""],
                ["Bb", ""],
                ["bB", ""],
                ["bb", "B"],
                ["BaBa", "abab"],
            ],
        )

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
        self.assertEqual(kb.alphabet(), "abB")
        self.assertFalse(kb.has_froidure_pin())
        self.assertEqual(kb.froidure_pin().size(), 24)
        self.assertEqual(kb.identity(), "")
        self.assertEqual(kb.inverses(), "aBb")
        self.assertFalse(kb.is_obviously_infinite())
        self.assertTrue(kb.is_obviously_finite())
        self.assertEqual(kb.nr_active_rules(), 11)
        self.assertEqual(kb.nr_rules(), 8)
        self.assertEqual(kb.size(), 24)

        # TBA in v1.1.0 of libsemigroups
        # self.assertEqual(kb.alphabet(0), "a")
        # self.assertEqual(kb.alphabet(1), "b")
        # self.assertEqual(kb.alphabet(2), "B")
        # with self.assertRaises(TypeError):
        #     self.assertEqual(kb.alphabet(3), "B")

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
        kb = KnuthBendix()
        kb.set_alphabet("abB")
        kb.set_identity("")
        kb.set_inverses("aBb")

        kb.add_rule("bb", "B")
        kb.add_rule("BaBa", "abab")
        kb.run()
        self.assertTrue(kb.equal_to("bb", "B"))
        self.assertTrue(kb.equal_to([1, 1], [2]))

        with self.assertRaises(TypeError):
            kb.equal_to([1, 1], [3])
        with self.assertRaises(TypeError):
            kb.equal_to("aa", "z")

        self.assertEqual(kb.normal_form("bb"), "B")
        self.assertEqual(kb.normal_form("B"), "B")
        self.assertEqual(kb.normal_form([1, 1]), [2])
        self.assertEqual(kb.normal_form([0, 0]), [])

        with self.assertRaises(LibsemigroupsCppyyException):
            kb.normal_form([1, 3])
        with self.assertRaises(LibsemigroupsCppyyException):
            kb.normal_form("z")

        self.assertEqual(kb.rewrite("aa"), "")
        self.assertEqual(kb.rewrite("bb"), "B")

        with self.assertRaises(TypeError):
            self.assertEqual(kb.rewrite("z"))
