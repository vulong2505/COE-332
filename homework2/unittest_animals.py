#!/usr/bin/env python3
import unittest

from read_animals import print_animal
from read_animals import mean_median_mode_appendages
from read_animals import head_count
from read_animals import body_count
from read_animals import mode_count


class test_read_animals(unittest.TestCase):

    def test_print_animal(self):
        self.assertRaises(TypeError, print_animal, 'A')
        self.assertRaises(TypeError, print_animal, ['A', 'A'])

    def test_mean_median_mode_appendages(self):
        self.assertRaises(TypeError, mean_median_mode_appendages(), 1)
        self.assertRaises(TypeError, mean_median_mode_appendages(), 'A')
        self.assertRaises(TypeError, mean_median_mode_appendages(), True)
        self.assertRaises(TypeError, mean_median_mode_appendages(), ['A', 'A'])

    # Similar to body_count
    def test_head_count(self):
        self.assertRaises(TypeError, head_count(), 1)
        self.assertRaises(TypeError, head_count(), 'A')
        self.assertRaises(TypeError, head_count(), True)
        self.assertRaises(TypeError, head_count(), ['A', 'A'])

    def test_body_count(self):
        self.assertRaises(TypeError, body_count(), 1)
        self.assertRaises(TypeError, body_count(), 'A')
        self.assertRaises(TypeError, body_count(), True)
        self.assertRaises(TypeError, body_count(), ['A', 'A'])

    def test_mode_count(self):
        ex_count_list1 = [0, 1, 5, 2, 4]
        ex_count_list2 = [0, 1, 5, 5, 4]
        self.assertEqual(mode_count(ex_count_list1), 2)  # index 2 has most counts
        self.assertEqual(mode_count(ex_count_list2), 0)  # index 0 is the error msg
        self.assertRaises(TypeError, mode_count, 1)
        self.assertRaises(TypeError, mode_count, 'A')
        self.assertRaises(TypeError, mode_count, True)


if __name__ == '__main__':
    unittest.main()
