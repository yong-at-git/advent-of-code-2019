#! /usr/bin/env python3
from unittest import TestCase

from days.day_1.day_1 import get_base_fuel_for_mass, get_complete_fuel_for_mass, get_sum_of_fuel_for_all_modules, \
    get_complete_fuel_for_fuel


class Test(TestCase):
    def test_get_base_fuel_for_mass(self):
        self.assertEqual(get_base_fuel_for_mass(12), 2)
        self.assertEqual(get_base_fuel_for_mass(14), 2)
        self.assertEqual(get_base_fuel_for_mass(1969), 654)
        self.assertEqual(get_base_fuel_for_mass(100756), 33583)

    def test_get_complete_fuel_for_mass(self):
        self.assertEqual(get_complete_fuel_for_mass(14), 2)
        self.assertEqual(get_complete_fuel_for_mass(1969), 966)
        self.assertEqual(get_complete_fuel_for_mass(100756), 50346)

    def test_get_fuel_for_fuel(self):
        self.assertEqual(get_complete_fuel_for_fuel(2), 0)
        self.assertEqual(get_complete_fuel_for_fuel(654), 312)
        self.assertEqual(get_complete_fuel_for_fuel(33583), 16763)

    def test_get_sum_of_fuel_for_all_modules(self):
        self.assertEqual(get_sum_of_fuel_for_all_modules(), 5132379)
