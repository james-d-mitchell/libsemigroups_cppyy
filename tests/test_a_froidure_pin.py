import unittest
from libsemigroups_cppyy import (
    FroidurePin,
    Transformation,
    PartialPerm,
    ReportGuard,
    LibsemigroupsCppyyException,
    milliseconds,
    LibsemigroupsException,
    libsemigroups_version,
    compare_version_numbers,
)
import cppyy.gbl.std as std


class TestFroidurePin(unittest.TestCase):
    def test_init(self):
        ReportGuard(False)
        FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))

        with self.assertRaises(KeyError):
            FroidurePin()

        with self.assertRaises(ValueError):
            FroidurePin(PartialPerm([1, 2], [0, 1], 3), Transformation([0, 1]))

        with self.assertRaises(TypeError):
            FroidurePin({2, 3})

    def test_idempotents(self):
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        S.run()
        self.assertEqual(
            std.distance(S.cbegin_idempotents(), S.cend_idempotents()),
            S.nr_idempotents(),
        )

        self.assertEqual(
            list(S.idempotents()),
            [
                Transformation([0, 0, 0]),
                Transformation([0, 1, 0]),
                Transformation([1, 1, 1]),
            ],
        )

    def test_iterator(self):
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        self.assertEqual(
            list(S),
            [
                Transformation([1, 0, 1]),
                Transformation([0, 0, 0]),
                Transformation([0, 1, 0]),
                Transformation([1, 1, 1]),
            ],
        )

    def test_sorted_elements(self):
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        expected = [
            Transformation([0, 0, 0]),
            Transformation([0, 1, 0]),
            Transformation([1, 0, 1]),
            Transformation([1, 1, 1]),
        ]
        self.assertEqual(list(S.sorted_elements()), expected)
        self.assertEqual(S.sorted_elements()[:2], expected[:2])
        self.assertEqual(S.sorted_elements()[::-1], expected[::-1])

    def test_copy_constructor(self):
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        T = S
        self.assertTrue(T is S)
        self.assertTrue(S is T)
        T = FroidurePin(S)
        self.assertFalse(S is T)
        self.assertFalse(T is S)
        self.assertEqual(T.size(), 4)
        self.assertEqual(S.current_size(), 2)

    def test_factorisation(self):
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        self.assertEqual(S.size(), 4)
        self.assertEqual(std.distance(S.cbegin(), S.cend()), S.size())
        self.assertEqual(
            [S.factorisation(x) for x in range(S.size())], [[0], [1], [0, 0], [1, 0]]
        )
        with self.assertRaises(LibsemigroupsCppyyException):
            S.factorisation(4)
        # check again because of some bug in an early version of
        # unwrap(_return_value)
        self.assertEqual(
            [S.factorisation(x) for x in range(S.size())], [[0], [1], [0, 0], [1, 0]]
        )
        with self.assertRaises(LibsemigroupsCppyyException):
            S.factorisation(Transformation([1, 1, 2]))
        self.assertEqual(std.distance(S.cbegin(), S.cend()), S.size())
        self.assertEqual([S.factorisation(x) for x in S], [[0], [1], [0, 0], [1, 0]])

    def test_settings(self):
        S = FroidurePin(Transformation([1, 0, 1]))

        self.assertTrue(isinstance(S.batch_size(), int))
        S.batch_size(10)
        self.assertEqual(S.batch_size(), 10)

        self.assertTrue(isinstance(S.concurrency_threshold(), int))
        S.concurrency_threshold(10)
        self.assertEqual(S.concurrency_threshold(), 10)

        self.assertFalse(S.immutable())

        self.assertTrue(isinstance(S.max_threads(), int))
        S.max_threads(1)
        self.assertEqual(S.max_threads(), 1)

    def test_add_generator(self):
        ReportGuard(False)
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        self.assertEqual(S.size(), 4)
        S.add_generator(Transformation([1, 2, 0]))
        self.assertEqual(S.size(), 24)

    def test_deleted_methods(self):
        S = FroidurePin(Transformation([1, 0, 1]))
        with self.assertRaises(LibsemigroupsCppyyException):
            S.add_generators()
        with self.assertRaises(LibsemigroupsCppyyException):
            S.copy_add_generators()
        with self.assertRaises(LibsemigroupsCppyyException):
            S.closure()
        with self.assertRaises(LibsemigroupsCppyyException):
            S.copy_closure()

    def test_run_for(self):
        ReportGuard(False)
        S = FroidurePin(Transformation([1, 0] + list(range(2, 10))))
        S.add_generator(Transformation(list(range(1, 10)) + [0]))
        S.run_for(milliseconds(10))

    def test_run_until(self):
        if compare_version_numbers(libsemigroups_version(), "1.0.8"):
            ReportGuard(False)
            S = FroidurePin(Transformation([1, 0] + list(range(2, 10))))
            S.add_generator(Transformation(list(range(1, 10)) + [0]))
            S.run_until(lambda: S.current_size() > 10)
            self.assertFalse(S.finished())
            self.assertTrue(S.current_size() > 10)
            S.run_until(lambda: S.current_nr_rules() > 100)
            self.assertFalse(S.finished())
            self.assertTrue(S.current_nr_rules() > 100)

    def test_attributes(self):
        ReportGuard(False)
        S = FroidurePin(Transformation(list(range(1, 10)) + [0]))
        self.assertEqual(S.current_nr_rules(), 0)
        self.assertEqual(S.current_size(), 1)
        self.assertEqual(S.degree(), 10)

        self.assertEqual(S.size(), 10)

        self.assertTrue(S.is_idempotent(9))
        for i in range(8):
            self.assertFalse(S.is_idempotent(i))

        with self.assertRaises(LibsemigroupsException):
            S.is_idempotent(10)

        self.assertTrue(S.is_monoid())
        self.assertEqual(S.nr_generators(), 1)
        self.assertEqual(S.nr_idempotents(), 1)

    def test_cayley_graphs(self):
        ReportGuard(False)
        S = FroidurePin(Transformation(list(range(1, 10)) + [0]))
        S.run()
        for i in range(S.size()):
            self.assertEqual(S.left(i, 0), S.right(i, 0))
        for i in range(S.size()):
            self.assertEqual(S.left_cayley_graph().get(i, 0), S.left(i, 0))
            self.assertEqual(S.right_cayley_graph().get(i, 0), S.right(i, 0))

    def test_factorisation_and_relations(self):
        ReportGuard(False)
        S = FroidurePin(Transformation(list(range(1, 10)) + [0]))
        self.assertEqual(S.length_const(0), 1)

        with self.assertRaises(LibsemigroupsException):
            S.length_const(1)

        self.assertEqual(S.current_max_word_length(), 1)
        S.run()
        self.assertEqual(S.current_max_word_length(), 10)

        self.assertTrue(S.equal_to([0, 0], [0, 0]))
        self.assertFalse(S.equal_to([0], [0, 0]))
        self.assertFalse(S.equal_to([0] * 10, [0]))

        with self.assertRaises(LibsemigroupsException):
            self.assertFalse(S.equal_to([0] * 10, [1]))
        with self.assertRaises(LibsemigroupsException):
            self.assertFalse(S.equal_to([1], [0] * 10))

        for i in range(S.size()):
            self.assertEqual(S.length_const(i), i + 1)
            self.assertEqual(S.length_non_const(i), i + 1)

        with self.assertRaises(LibsemigroupsException):
            S.length_non_const(10)

        self.assertEqual(S.letter_to_pos(0), 0)
        with self.assertRaises(LibsemigroupsException):
            S.letter_to_pos(1)

        S.add_generator(Transformation([1, 0] + list(range(2, 10))))
        self.assertEqual(S.letter_to_pos(1), 10)
        S.add_generator(Transformation(list(range(1, 10)) + [0]))
        self.assertEqual(S.letter_to_pos(2), 0)
        self.assertEqual(
            [S.minimal_factorisation(x) for x in range(10)],
            [
                [0],
                [0, 0],
                [0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1],
            ],
        )

        with self.assertRaises(LibsemigroupsCppyyException):
            S.next_relation()

        S = FroidurePin(Transformation(list(range(1, 5)) + [0]))
        S.add_generator(Transformation([1, 0] + list(range(2, 5))))
        self.assertEqual(S.current_nr_rules(), 0)
        self.assertEqual(S.word_to_pos([0, 1, 0, 1]), 18446744073709551615)

        self.assertEqual(S.nr_rules(), 25)
        self.assertEqual(
            S.word_to_element([0, 1, 0, 1]), Transformation([0, 3, 4, 1, 2])
        )
        self.assertEqual(S.word_to_pos([0, 1, 0, 1]), 15)
        
        S = FroidurePin(Transformation([1, 0, 1]), Transformation([0, 0, 0]))
        S.run()
        if compare_version_numbers(libsemigroups_version(), "1.1.0"):
            self.assertEqual(
                S.rules(),
                [[[0, 1], [1]], [[1, 1], [1]], [[0, 0, 0], [0]], [[1, 0, 0], [1]]],
            )


    def test_prefixes_and_suffixes(self):
        S = FroidurePin(Transformation(list(range(1, 5)) + [0]))
        self.assertEqual(S.prefix(0), 18446744073709551615)
        for i in range(1, S.size()):
            self.assertEqual(S.prefix(i), i - 1)
            self.assertEqual(S.suffix(i), i - 1)
            self.assertEqual(S.first_letter(i), 0)
            self.assertEqual(S.final_letter(i), 0)

    def test_products(self):
        S = FroidurePin(Transformation(list(range(1, 5)) + [0]))
        S.run()
        for i in range(5):
            for j in range(5):
                self.assertEqual(S.fast_product(i, j), ((i + j + 1) % 5))
                self.assertEqual(S.product_by_reduction(i, j), ((i + j + 1) % 5))

    def test_membership(self):
        S = FroidurePin(Transformation(list(range(1, 5)) + [0]))
        S.add_generator(Transformation([1, 0] + list(range(2, 5))))
        if compare_version_numbers(libsemigroups_version(), "1.0.8"):
            self.assertEqual(
                S.current_position(Transformation([2, 0, 3, 4, 1])),
                18446744073709551615,
            )

        self.assertEqual(S.at(10), Transformation([2, 0, 3, 4, 1]))
        with self.assertRaises(Exception):
            S.at(120)
        with self.assertRaises(Exception):
            S[120]

        self.assertTrue(S.contains(Transformation([2, 0, 3, 4, 1])))
        self.assertEqual(S.position(Transformation([2, 0, 3, 4, 1])), 10)
        self.assertEqual(S.sorted_position(Transformation([2, 0, 3, 4, 1])), 51)
        self.assertEqual(S.sorted_at(51), Transformation([2, 0, 3, 4, 1]))

        if compare_version_numbers(libsemigroups_version(), "1.0.8"):
            self.assertEqual(S.current_position(Transformation([2, 0, 3, 4, 1])), 10)

    def test_state(self):
        ReportGuard(False)
        S = FroidurePin(Transformation([1, 0] + list(range(2, 10))))
        S.add_generator(Transformation(list(range(1, 10)) + [0]))
        self.assertFalse(S.started())
        S.run_for(milliseconds(10))
        self.assertTrue(S.started())
        self.assertTrue(S.timed_out())
        self.assertTrue(S.stopped())
        self.assertFalse(S.finished())
