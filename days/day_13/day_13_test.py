import unittest
from days.day_13.day_13_solution import Day13


class MyTestCase(unittest.TestCase):
    def test_solution_1(self):
        self.assertEqual(226, Day13.get_solution_1())

    def test_solution_2(self):
        self.assertEqual(10800, Day13.get_solution_2())


if __name__ == '__main__':
    unittest.main()
