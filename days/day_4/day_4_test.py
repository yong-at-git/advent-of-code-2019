#! /usr/bin/env python3
from unittest import TestCase
from days.day_4.day_4_solution import is_valid_number, is_matching_extra_condition_in_solution_2, get_solution_1, \
    get_solution_2


class Test(TestCase):
    def test_is_valid_number(self):
        self.assertTrue(is_valid_number(str(111111)))
        self.assertFalse(is_valid_number(str(223450)))
        self.assertFalse(is_valid_number(str(123789)))

    def test_solution_1(self):
        self.assertEqual(1079, get_solution_1())

    def test_is_matching_extra_condition_in_solution_2(self):
        self.assertTrue(is_matching_extra_condition_in_solution_2(str(112233)))
        self.assertFalse(is_matching_extra_condition_in_solution_2(str(123444)))
        self.assertTrue(is_matching_extra_condition_in_solution_2(str(111122)))

    def test_solution_2(self):
        self.assertEqual(699, get_solution_2())
