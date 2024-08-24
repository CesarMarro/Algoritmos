import unittest
from bubble_sort import bubble_sort


class TestCountingSort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(bubble_sort([]), [])

    def test_single_element_array(self):
        self.assertEqual(bubble_sort([1]), [1])

    def test_sorted_array(self):
        self.assertEqual(bubble_sort([1, 2, 3]), [1, 2, 3])

    def test_unsorted_array(self):
        self.assertEqual(bubble_sort([4, 2, 2, 8, 3, 3, 1]), [1, 2, 2, 3, 3, 4, 8])

    def test_array_whith_duplicates(self):
        self.assertEqual(bubble_sort([5, 5, 5, 1, 1, 1]), [1, 1, 1, 5, 5, 5])
