#! /usr/bin/env python3
from days.commons.inputs_reader import get_list_of_raw_lines


class Day14:
    def __init__(self):
        self._formulas = {}

    ORE = 'ORE'

    @property
    def formulas(self):
        return self._formulas

    @staticmethod
    def parse_in_materials(in_materials):
        in_names_and_units = {}

        for material_str in in_materials.split(','):
            name = material_str.strip().split(' ')[1].strip()
            unit = int(material_str.strip().split(' ')[0].strip())
            in_names_and_units[name] = unit

        return in_names_and_units

    @staticmethod
    def parse_out_material(out_material):
        return out_material.split(' ')[1].strip(), int(out_material.split(' ')[0].strip())

    @staticmethod
    def parse_formula(formula_str):
        in_materials = formula_str.split('=>')[0].strip()
        out_material = formula_str.split('=>')[1].strip()
        out_name, out_unit = Day14.parse_out_material(out_material)
        in_names_and_units = Day14.parse_in_materials(in_materials)

        return {'in': in_names_and_units, 'out': {'name': out_name, 'unit': out_unit}}

    @staticmethod
    def get_apply_times(expected_total_count, unit_count, leftover_count):
        dividend = expected_total_count - leftover_count
        divisor = unit_count
        return dividend // divisor + (0 if dividend % divisor == 0 else 1)

    def parse_inputs(self):
        for formula_str in get_list_of_raw_lines("day_14.input"):
            formula = Day14.parse_formula(formula_str)
            self.formulas[formula['out']['name']] = formula

    def get_raw_chemical_count(self, expected_out, list_of_raw, leftover):
        expected_out_name = expected_out['name']
        expected_out_unit = expected_out['unit']

        formula = self.formulas[expected_out_name]
        formula_out_unit = formula['out']['unit']

        if expected_out_name in leftover and leftover[expected_out_name] > expected_out_unit:
            leftover[expected_out_name] -= expected_out_unit
            return
        else:
            count_in_leftover = 0 if expected_out_name not in leftover else leftover[expected_out_name]

            time_to_apply_formula = Day14.get_apply_times(expected_out_unit, formula_out_unit, count_in_leftover)
            # print("time*****", expected_out_unit, formula_out_unit, time_to_apply_formula)

            if expected_out_name in leftover:
                # print("one time to apply,", time_to_apply_formula, ", fou=", formula_out_unit, ", eou=",
                #      expected_out_unit)
                leftover[expected_out_name] += (time_to_apply_formula * formula_out_unit - expected_out_unit)
            else:
                # print("two time to apply,", time_to_apply_formula, ", fou=", formula_out_unit, ", eou=",
                #      expected_out_unit)
                leftover[expected_out_name] = (time_to_apply_formula * formula_out_unit - expected_out_unit)
            # print("on=", expected_out, ", after=", leftover)

        for in_elem in formula['in'].items():
            required_unit = in_elem[1] * time_to_apply_formula
            if in_elem[0] == Day14.ORE:
                list_of_raw.append(required_unit)
            else:
                expected_out = {'name': in_elem[0], 'unit': required_unit}
                self.get_raw_chemical_count(expected_out, list_of_raw, leftover)

    def get_solution_1(self):
        self.parse_inputs()
        expected_out = {'name': 'FUEL', 'unit': 1}
        list_of_raw = []
        leftovers = {}
        self.get_raw_chemical_count(expected_out, list_of_raw, leftovers)

        return sum(list_of_raw)

    def get_solution_2(self):
        self.parse_inputs()

        should_continue = 1
        fuel_count = 8193610  # Solution is to try with a big num and big step; then narrow down the area by adjusting their values.
        step = 1
        while should_continue:
            expected_out = {'name': 'FUEL', 'unit': fuel_count}
            list_of_raw = []
            leftovers = {}
            self.get_raw_chemical_count(expected_out, list_of_raw, leftovers)
            ore_count = sum(list_of_raw)
            print("before compare, fuel=", fuel_count)
            if ore_count > 1000000000000:
                return fuel_count

            fuel_count += step


if __name__ == "__main__":
    today = Day14()

    print("solution 1=", today.get_solution_1())
    print("solution 2=", today.get_solution_2())
