#! /usr/bin/env python3
from unittest import TestCase
from days.day_3.day_3_solution import get_distance_of_closest_intersection


class TestDay3(TestCase):
    def test_get_distance_of_closest_coordinate_example_1(self):
        path_1 = ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"]
        path_2 = ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]

        self.assertEqual(159, get_distance_of_closest_intersection(path_1, path_2))

    def test_get_distance_of_closest_coordinate_example_2(self):
        path_1 = ["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"]
        path_2 = ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]

        self.assertEqual(135, get_distance_of_closest_intersection(path_1, path_2))
