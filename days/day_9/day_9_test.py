#! /usr/bin/env python3
import unittest
from days.day_9.day_9_solution import get_solution_1, get_solution_2


class MyTestCase(unittest.TestCase):
    def test_solution_1(self):
        self.assertEqual(3839402290, get_solution_1())

    def test_solution_2(self):
        self.assertEqual(35734, get_solution_2())
