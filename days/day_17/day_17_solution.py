#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer
from days.commons.outputs_utils import print_grid


class Day17:
    NEW_LINE = 'n'

    @staticmethod
    def ascii_to_mark(ascii_value):
        marks = {
            35: '#',
            46: '.',
            10: Day17.NEW_LINE
        }
        return marks[ascii_value]

    @staticmethod
    def is_intersection(pos, grid):
        (x, y) = pos
        return (x - 1, y) in grid and grid[(x - 1, y)] == '#' and (x + 1, y) in grid and grid[(x + 1, y)] == '#' and (
            x, y - 1) in grid and grid[(x, y - 1)] == '#' and (x, y + 1) in grid and grid[(x, y + 1)] == '#'

    @staticmethod
    def get_sum_of_alignment_params(grid):
        scaffold_dict = {k: v for k, v in grid.items() if v == '#'}

        intersections = list(filter(lambda pos: Day17.is_intersection(pos, grid), scaffold_dict.keys()))

        return sum(list(map(lambda k: k[0] * k[1], intersections)))

    def get_solution_1(self):
        grid = self.build_grid_from_inputs()
        return Day17.get_sum_of_alignment_params(grid)

    def build_grid_from_inputs(self):
        in_dict = get_single_line_and_parse_to_dicts("day_17.input")
        computer = IntcodeComputer()
        computer.inputs_dict = in_dict
        grid = {}
        x = 0
        y = 0
        while not computer.is_halted:
            computer.perform_operation()

            if computer.has_output_ready():
                ascii_value = computer.outputs[0]
                del computer.outputs[0]

                if ascii_value not in [10, 35, 46]:
                    print('not used key for Solution 1=', ascii_value)
                else:
                    grid_mark = Day17.ascii_to_mark(ascii_value)
                    if grid_mark != Day17.NEW_LINE:
                        grid[(x, y)] = grid_mark
                        x += 1
                    else:
                        y += 1
                        x = 0
        return grid


if __name__ == "__main__":
    today = Day17()

    print("Solution 1=", today.get_solution_1())
