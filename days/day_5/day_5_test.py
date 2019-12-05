import unittest
from days.day_5.day_5_solution import run_program


class MyTestCase(unittest.TestCase):
    def test_something(self):
        inputs = [3, 0, 4, 0, 99]
        run_program(inputs)
        # The output should be whatever you typed from terminal
        self.assertEqual(True, True)
