#! /usr/bin/env python3
from unittest import TestCase
from days.day_11.day_11_solution import Day11Solution


class Test(TestCase):
    def test_get_solution_1(self):
        solution = Day11Solution()
        self.assertEqual(2343, solution.get_solution_1())
