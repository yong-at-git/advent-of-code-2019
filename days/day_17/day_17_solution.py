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

    def get_solution_2(self):
        in_dict = self.get_original_input_dict()
        grid = self.build_grid_from_inputs(in_dict)
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

    def build_path(self, in_dict):
        computer = IntcodeComputer()
        computer.inputs_dict = in_dict
        grid = {}
        x = 0
        y = 0
        while not computer.is_halted:
            computer.perform_operation()

            if computer.is_waiting:
                print("waiting")
                return

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

    def get_neighor_count(self, grid, pos):
        pos_2d = Type2D.from_tuple(pos)

        right = pos_2d.clone().right_move().as_tuple()
        left = pos_2d.clone().left_move().as_tuple()
        up = pos_2d.clone().up_move_by_minus_y().as_tuple()
        down = pos_2d.clone().down_move_by_plus_y().as_tuple()

        return len(list(filter(lambda p: grid.get(p, '') == '#', [right, left, up, down])))

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
            return right, ArrowDirection.RIGHT.value, TurnStr.LEFT.value
        else:
            print("Warn facing up, potential backtracking at=", current_pos)
            return current_pos, ArrowDirection.UP.value, None

    def get_direction(self, pos, grid, current_direction):
        pos_2d = Type2D(pos[0], pos[1])
        right = pos_2d.clone().change_x_by_step(1).as_tuple()
        left = pos_2d.clone().change_x_by_step(-1).as_tuple()
        up = pos_2d.clone().change_y_by_step(1).as_tuple()
        down = pos_2d.clone().change_y_by_step(-1).as_tuple()

        if current_direction == ArrowDirection.UP.value:
            if up in grid and grid[up] == '#':
                return ArrowDirection.UP.value
            elif right in grid and grid[right] == '#':
                return ArrowDirection.RIGHT.value
            elif left in grid and grid[left] == '#':
                return ArrowDirection.LEFT.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == ArrowDirection.RIGHT.value:
            if right in grid and grid[right] == '#':
                return ArrowDirection.RIGHT.value
            elif up in grid and grid[up] == '#':
                return ArrowDirection.UP.value
            elif down in grid and grid[down] == '#':
                return ArrowDirection.DOWN.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == ArrowDirection.DOWN.value:
            if down in grid and grid[down] == '#':
                return ArrowDirection.DOWN.value
            elif left in grid and grid[left] == '#':
                return ArrowDirection.LEFT.value
            elif right in grid and grid[right] == '#':
                return ArrowDirection.RIGHT.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == ArrowDirection.LEFT.value:
            if left in grid and grid[left] == '#':
                return ArrowDirection.LEFT.value
            elif up in grid and grid[up] == '#':
                return ArrowDirection.UP.value
            elif down in grid and grid[down] == '#':
                return ArrowDirection.DOWN.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        else:
            print("unknown")


def is_starting_pos_mark(mark):
    return mark in [ArrowDirection.UP.value, ArrowDirection.DOWN.value, ArrowDirection.LEFT.value,
                    ArrowDirection.RIGHT.value]


if __name__ == "__main__":
    today = Day17()

    # print("Solution 1=", today.get_solution_1())
    today.get_solution_2()
