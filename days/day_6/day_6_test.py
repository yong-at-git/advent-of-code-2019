#! /usr/bin/env python3
from unittest import TestCase
from days.day_6.day_6_solution import get_solution_1_from_inputs, get_solution_2_with_labels


class Test(TestCase):
    def test_get_solution_1(self):
        orbits = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"]
        self.assertEqual(42, get_solution_1_from_inputs(orbits))

    def test_get_solution_2_with_labels(self):
        orbits = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"]
        self.assertEqual(4, get_solution_2_with_labels("YOU", "SAN", orbits))
