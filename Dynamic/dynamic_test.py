import unittest
from fibonacci_dynamic import fibonacci


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self):
        """
        Verifica que fibonacci(0) retorne 0.
        """
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_one(self):
        """
        Verifica que fibonacci(1) retorne 1.
        """
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_five(self):
        """
        Verifica que fibonacci(5) retorne 5.
        """
        self.assertEqual(fibonacci(5), 5)

    def test_fibonacci_ten(self):
        """
        Verifica que fibonacci(10) retorne 55.
        """
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_large_number(self):
        """
        Verifica que fibonacci(20) retorne 6765.
        """
        self.assertEqual(fibonacci(20), 6765)


if __name__ == "__main__":
    unittest.main()
