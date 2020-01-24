import unittest
from libsemigroups_cppyy import Permutation

# TODO write more tests


class TestPerm(unittest.TestCase):
    def test_init(self):
        Permutation([])
        Permutation([0, 1])
        Permutation([0, 1, 2, 3])

    def test_one(self):
        self.assertEqual(Permutation([1, 0, 2]) ** 2, Permutation([0, 1, 2]))
        self.assertEqual(Permutation([1, 0, 2]).ran(), [1, 0, 2])
