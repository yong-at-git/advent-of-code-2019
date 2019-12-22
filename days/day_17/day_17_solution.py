#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer
from days.commons.outputs_utils import print_grid
from days.commons.data_types import TurnStr, ArrowDirection, Type2D

from enum import Enum


class Marks(Enum):
    SCAFOLLD = '#'
    SPACE = '.'


class Day17:
    @staticmethod
    def is_intersection(pos, grid):
        pos_2d = Type2D.from_tuple(pos)

        left = pos_2d.clone().left_move().as_tuple()
        right = pos_2d.clone().right_move().as_tuple()
        up = pos_2d.up_move_by_minus_y().as_tuple()
        down = pos_2d.down_move_by_plus_y().as_tuple()

        return grid.get(left, '') == '#' and grid.get(right, '') == '#' and grid.get(up, '') == '#' \
               and grid.get(down, '') == '#'

    @staticmethod
    def get_sum_of_alignment_params(grid):
        scaffold_dict = {k: v for k, v in grid.items() if v == '#'}

        intersections = list(filter(lambda pos: Day17.is_intersection(pos, grid), scaffold_dict.keys()))

        return sum(list(map(lambda k: k[0] * k[1], intersections)))

    def get_solution_1(self):
        in_dict = self.get_original_input_dict()
        grid = self.build_grid_from_inputs(in_dict)
        return Day17.get_sum_of_alignment_params(grid)

    def get_solution_2_prepare(self):
        in_dict = self.get_original_input_dict()
        grid = self.build_grid_from_inputs(in_dict)
        print_grid(grid)
        current_pos = self.get_start_point_pos(grid)
        current_direction = grid[current_pos]
        path = []

        while True:
            n_pos, n_direction, n_turn = self.get_next_movement_info(grid, current_pos, current_direction)

            if n_pos == current_pos:
                print("Visited all nodes. Stop.")
                break

            if n_turn:
                path.append((n_turn, [n_pos]))
            else:
                path[-1][1].append(n_pos)

            current_pos = n_pos
            current_direction = n_direction

        path_str = list(map(lambda st: (st[0], len(st[1])), path))
        print(path_str)

    def get_solution_2(self):
        in_dict = self.get_original_input_dict()
        computer = IntcodeComputer()
        in_dict[0] = 2

        computer.inputs_dict = in_dict

        strs = get_solution_2_path_strs_ascii()

        while not computer.is_halted:
            computer.perform_operation()

            if computer.is_waiting:
                ascii_str = strs[0]
                del strs[0]
                for c in ascii_str:
                    computer.predefined_values_for_input_instruction.append(ord(c))
                computer.predefined_values_for_input_instruction.append(10)

            if len(computer.outputs) > 0:
                c = computer.outputs[0]
                del computer.outputs[0]

        return c

    def get_original_input_dict(self):
        return get_single_line_and_parse_to_dicts("day_17.input")

    def build_grid_from_inputs(self, in_dict):
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

                if ascii_value != 10:
                    grid[(x, y)] = chr(ascii_value)
                    x += 1
                else:
                    y += 1
                    x = 0

        return grid

    def get_start_point_pos(self, grid):
        return next((item[0] for item in grid.items() if is_starting_pos_mark(item[1])))

    def get_init_direction(self):
        return ArrowDirection.UP.value

    def get_next_movement_info(self, grid, current_pos, current_direction):
        """
        :param current_pos:
        :param grid:
        :param current_direction:
        :return: (pos, direction, turn)
        """
        pos_2d = Type2D.from_tuple(current_pos)

        right = pos_2d.clone().right_move().as_tuple()
        left = pos_2d.clone().left_move().as_tuple()
        up = pos_2d.clone().up_move_by_minus_y().as_tuple()
        down = pos_2d.clone().down_move_by_plus_y().as_tuple()

        if current_direction == ArrowDirection.UP.value:
            return self.now_facing_up_but_what_next(current_pos, grid, down, left, right, up)
        elif current_direction == ArrowDirection.RIGHT.value:
            return self.now_facing_right_but_what_next(current_pos, grid, down, left, right, up)
        elif current_direction == ArrowDirection.DOWN.value:
            return self.now_facing_down_but_what_next(current_pos, grid, down, left, right, up)
        elif current_direction == ArrowDirection.LEFT.value:
            return self.now_facing_left_but_what_next(current_pos, grid, down, left, right, up)
        else:
            print("Unknown. Eat or sleep.")

    def now_facing_left_but_what_next(self, current_pos, grid, down, left, right, up):
        if grid.get(left, '') == '#':
            return left, ArrowDirection.LEFT.value, None
        elif grid.get(up, '') == '#':
            return up, ArrowDirection.UP.value, TurnStr.RIGHT.value
        elif grid.get(down, '') == '#':
            return down, ArrowDirection.DOWN.value, TurnStr.LEFT.value
        else:
            print("Warn facing left, potential backtracking at=", current_pos)
            return current_pos, ArrowDirection.LEFT.value, None

    def now_facing_down_but_what_next(self, current_pos, grid, down, left, right, up):
        if grid.get(down, '') == '#':
            return down, ArrowDirection.DOWN.value, None
        elif grid.get(left, '') == '#':
            return left, ArrowDirection.LEFT.value, TurnStr.RIGHT.value
        elif grid.get(right, '') == '#':
            return right, ArrowDirection.RIGHT.value, TurnStr.LEFT.value
        else:
            print("Warn facing down, potential backtracking at=", current_pos)
            return current_pos, ArrowDirection.DOWN.value, None

    def now_facing_right_but_what_next(self, current_pos, grid, down, left, right, up):
        if grid.get(right, '') == '#':
            return right, ArrowDirection.RIGHT.value, None
        elif grid.get(up, '') == '#':
            return up, ArrowDirection.UP.value, TurnStr.LEFT.value
        elif grid.get(down, '') == '#':
            return down, ArrowDirection.DOWN.value, TurnStr.RIGHT.value
        else:
            print("Warn facing right, potential backtracking at=", current_pos)
            return current_pos, ArrowDirection.RIGHT.value, None

    def now_facing_up_but_what_next(self, current_pos, grid, down, left, right, up):
        if grid.get(up, '') == '#':
            return up, ArrowDirection.UP.value, None
        elif grid.get(left, '') == '#':
            return left, ArrowDirection.LEFT.value, TurnStr.LEFT.value
        elif grid.get(right, '') == '#':
            return right, ArrowDirection.RIGHT.value, TurnStr.RIGHT.value
        else:
            print("Warn facing up, potential backtracking at=", current_pos)
            return current_pos, ArrowDirection.UP.value, None


def is_starting_pos_mark(mark):
    return mark in [ArrowDirection.UP.value, ArrowDirection.DOWN.value, ArrowDirection.LEFT.value,
                    ArrowDirection.RIGHT.value]


def get_solution_2_path_strs_ascii():
    main_routine = 'A,B,B,C,C,A,A,B,B,C'
    func_a = 'L,12,R,4,R,4'
    func_b = 'R,12,R,4,L,12'
    func_c = 'R,12,R,4,L,6,L,8,L,8'
    y_n = 'n'

    return [main_routine, func_a, func_b, func_c, y_n]


if __name__ == "__main__":
    today = Day17()

    print("Solution 1=", today.get_solution_1())

    """
    Solution 2 pattern
    A,B,B,C,C,A,A,B,B,C
A = ('L', 12), ('R', 4), ('R', 4)
B = ('R', 12), ('R', 4), ('L', 12)
C = ('R', 12), ('R', 4), ('L', 6), ('L', 8), ('L', 8)
    """
    print("Solution 2=", today.get_solution_2())

    # cmd_str = ','.join(list(map(str, get_solution_2_path_strs_ascii())))
    # print(cmd_str)
