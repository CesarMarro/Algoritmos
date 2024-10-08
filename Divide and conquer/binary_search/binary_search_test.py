import unittest
from binary_search import binary_search


class TestBinarySearch(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(binary_search([], 1), -1)

    def test_single_element_found(self):
        self.assertEqual(binary_search([1], 1), 0)

    def test_single_element_not_found(self):
        self.assertEqual(binary_search([1], 2), -1)

    def test_first_element(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 1), 0)

    def test_last_element(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 5), 4)

    def test_middle_element(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 3), 2)

    def test_element_not_present(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 6), -1)

    def test_multiple_occurrences(self):
        # Retorna el índice de una de las ocurrencias
        arr = [1, 2, 2, 2, 3]
        result = binary_search(arr, 2)
        self.assertIn(result, [1, 2, 3])

    def test_negative_numbers(self):
        self.assertEqual(binary_search([-5, -3, -1, 0, 2, 4], -3), 1)

    def test_large_numbers(self):
        arr = list(range(0, 1000000, 2))  # Lista de números pares
        self.assertEqual(binary_search(arr, 500000), 250000)
        self.assertEqual(binary_search(arr, 500001), -1)


if __name__ == "__main__":
    unittest.main()
