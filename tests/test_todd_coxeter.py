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
