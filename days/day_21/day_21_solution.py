#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer


class Day21:
    def get_raw_input_dict(self):
        return get_single_line_and_parse_to_dicts("day_21.input")

    def get_solution_1(self):
        computer = IntcodeComputer()
        raw_dict = self.get_raw_input_dict()
        computer.inputs_dict = raw_dict

        pass


if __name__ == "__main__":
    today = Day21()

    print("Solution 1=", today.get_solution_1())
