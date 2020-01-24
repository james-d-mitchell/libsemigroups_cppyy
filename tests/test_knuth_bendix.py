import unittest
from libsemigroups_cppyy import KnuthBendix


class TestKnuth(unittest.TestCase):
    def test_all(self):
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
