#! /usr/bin/env python3
from unittest import TestCase
from days.day_7.day_7_solution import get_solution_1, get_solution_2, get_solution_2_with_init_inputs


class Test(TestCase):
    def test_get_solution_1(self):
        self.assertEqual(38500, get_solution_1())

    def test_get_solution_2_a(self):
        inputs = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                  27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]

        self.assertEqual(139629729, get_solution_2_with_init_inputs(list(map(lambda v: int(v), inputs))))

    def test_get_solution_2_b(self):
        inputs = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                  -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                  53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]

        self.assertEqual(18216, get_solution_2_with_init_inputs(inputs))

    def test_get_solution_2(self):
        self.assertEqual(33660560, get_solution_2())
