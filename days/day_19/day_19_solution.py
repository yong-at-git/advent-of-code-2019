#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer
from days.commons.outputs_utils import print_grid, print_int_grid


class Day19:
    def get_inputs_dict(self):
        return get_single_line_and_parse_to_dicts("day_19.input")

    def get_solution_1(self):

        grid = {}

        for y in range(0, 50):
            for x in range(0, 50):
                computer = IntcodeComputer()
                computer.inputs_dict = self.get_inputs_dict()

                while not computer.is_halted:
                    computer.perform_operation()

                    if computer.is_waiting:
                        computer.predefined_values_for_input_instruction.append(x)
                        computer.predefined_values_for_input_instruction.append(y)

                    if len(computer.outputs) == 1:
                        grid[(x, y)] = computer.outputs[0]
                        del computer.outputs[0]

        return len(list(filter(lambda v: v == 1, grid.values())))


if __name__ == "__main__":
    today = Day19()

    print("Solution 1=", today.get_solution_1())
