import unittest
from days.day_8.day_8_solution import get_solution_1


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1716, get_solution_1())
