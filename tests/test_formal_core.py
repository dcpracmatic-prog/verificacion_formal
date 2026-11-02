"""Unit tests for the formal verification primitives and arithmetic lemmas."""
import unittest

from fvcore.exhaustive import DomainTooLarge, forall
from fvcore.intervals import Interval, poly_identity
from lemmas import all_lemmas


class ExhaustiveTests(unittest.TestCase):
    def test_forall_proves_entire_declared_domain(self):
        proof = forall("nonnegative squares", {"x": range(-3, 4)}, lambda x: x * x >= 0)

        self.assertTrue(proof.ok())
        self.assertEqual(proof.status, "PROVEN")
        self.assertEqual(proof.cases, 7)
        self.assertIsNone(proof.counterexample)

    def test_forall_reports_counterexample(self):
        proof = forall("positive values", {"x": range(-2, 3)}, lambda x: x > 0)

        self.assertFalse(proof.ok())
        self.assertEqual(proof.status, "REFUTED")
        self.assertEqual(proof.counterexample["x"], -2)

    def test_forall_rejects_domains_over_limit(self):
        with self.assertRaises(DomainTooLarge):
            forall("too many cases", {"x": range(11)}, lambda x: True, max_cases=10)


class IntervalTests(unittest.TestCase):
    def test_interval_arithmetic_and_signed_fit(self):
        interval = Interval(-2, 3)

        self.assertEqual(interval + Interval(4, 5), Interval(2, 8))
        self.assertEqual(interval * Interval(-2, 4), Interval(-8, 12))
        self.assertTrue(Interval(-(1 << 31), (1 << 31) - 1).fits(32, True))
        self.assertFalse(Interval(-1, 1).fits(32, False))

    def test_polynomial_identity(self):
        self.assertTrue(
            poly_identity(
                lambda x, y: (x + y) ** 2,
                lambda x, y: x * x + 2 * x * y + y * y,
                nvars=2,
                deg=2,
            )
        )

    def test_repository_arithmetic_lemmas_are_proven(self):
        lemmas = all_lemmas()

        self.assertEqual(len(lemmas), 8)
        self.assertTrue(all(proof.ok() for proof in lemmas))


if __name__ == "__main__":
    unittest.main()
