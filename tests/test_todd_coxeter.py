import unittest
from libsemigroups_cppyy import ToddCoxeter

class TestToddCoxeter(unittest.TestCase):
    def test_constructors(self):
        try:
            ToddCoxeter("left")
        except:
            self.fail("Unexpected exception thrown")
        try:
            ToddCoxeter("right")
        except:
            self.fail("Unexpected exception thrown")
        try:
            ToddCoxeter("twosided")
        except:
            self.fail("Unexpected exception thrown")

        with self.assertRaises(TypeError):
            ToddCoxeter(45)
        with self.assertRaises(ValueError):
            ToddCoxeter("lft")
        
        tc = ToddCoxeter("left")
        tc.set_nr_generators(1)
        tc.add_pair([0, 0, 0, 0, 0, 0], [0, 0, 0])
        self.assertEqual(tc.nr_classes(), 5)
        self.assertEqual(tc.contains([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]), True)
        self.assertEqual(tc.contains([0, 0, 0], [0, 0]), False)
