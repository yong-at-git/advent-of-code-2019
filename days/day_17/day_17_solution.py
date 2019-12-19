#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer
from days.commons.outputs_utils import print_grid
from days.commons.data_types import TurnStr, Direction, Type2D

from enum import Enum


class ASCII(Enum):
    HASH = 35
    DOT = 46
    NEW_LINE = 10
    COMMA = 44


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
        in_dict = self.get_original_input_dict()
        grid = self.build_grid_from_inputs(in_dict)
        return Day17.get_sum_of_alignment_params(grid)

    def get_solution_2(self):
        in_dict = self.get_original_input_dict()
        grid = self.build_grid_from_inputs(in_dict)
        print_grid(grid)
        pos = self.get_start_point(grid)
        pos = (pos[0] + 1, pos[1])
        direction = self.get_init_direction()
        path = [(direction, [pos])]

        while True:
            n_pos, n_direction = self.get_next_pos_and_direction(pos, grid, direction)
            if n_pos == pos:
                break
            else:
                pos = n_pos
                direction = n_direction
                if direction == path[-1][0]:
                    path[-1][1].append(pos)
                else:
                    path.append((direction, [pos]))

        # print('Path=', path)
        turns = list(map(lambda st: (st[0], len(st[1])), path))
        tt = []
        for i in range(len(turns)):
            nu = turns[i][0]
            previous = turns[i - 1][0]
            if previous == Direction.UP.value:
                if nu == Direction.RIGHT.value:
                    tt.append(TurnStr.RIGHT.value)
                    tt.append(turns[i][1])
                elif nu == Direction.LEFT.value:
                    tt.append(TurnStr.LEFT.value)
                    tt.append(turns[i][1])
                else:
                    print("Sleep")
            elif previous == Direction.RIGHT.value:
                if nu == Direction.UP.value:
                    tt.append(TurnStr.LEFT.value)
                    tt.append(turns[i][1])
                elif nu == Direction.DOWN.value:
                    tt.append(TurnStr.RIGHT.value)
                    tt.append(turns[i][1])
                else:
                    print("Sleep")
            elif previous == Direction.DOWN.value:
                if nu == Direction.RIGHT.value:
                    tt.append(TurnStr.LEFT.value)
                    tt.append(turns[i][1])
                elif nu == Direction.LEFT.value:
                    tt.append(TurnStr.RIGHT.value)
                    tt.append(turns[i][1])
                else:
                    print("Sleep")
            elif previous == Direction.LEFT.value:
                if nu == Direction.UP.value:
                    tt.append(TurnStr.RIGHT.value)
                    tt.append(turns[i][1])
                elif nu == Direction.DOWN.value:
                    tt.append(TurnStr.LEFT.value)
                    tt.append(turns[i][1])
                else:
                    print("Sleep")
            else:
                print("Sleep")

        tt_str = list(map(str, tt))
        print(",".join(tt_str))

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

                if ascii_value not in [10, 35, 46]:
                    print('not used key for Solution 1=', ascii_value)
                    grid[(x, y)] = 'X'
                else:
                    grid_mark = Day17.ascii_to_mark(ascii_value)
                    if grid_mark != Day17.NEW_LINE:
                        grid[(x, y)] = grid_mark
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
        pos_2d = Type2D(pos[0], pos[1])
        right = pos_2d.clone().change_x_by_step(1).as_tuple()
        left = pos_2d.clone().change_x_by_step(-1).as_tuple()
        up = pos_2d.clone().change_y_by_step(-1).as_tuple()
        down = pos_2d.clone().change_y_by_step(1).as_tuple()
        possibles = [right, left, up, down]
        return len(list(filter(lambda p: p in grid and grid[p] == '#', possibles)))

    def get_start_point(self, grid):
        scaffold_dict = {k: v for k, v in grid.items() if v == '#'}

        return list(filter(lambda k: self.get_neighor_count(grid, k) == 1, scaffold_dict.keys()))[0]

    def get_init_direction(self):
        return Direction.UP.value

    def get_next_pos_and_direction(self, pos, grid, current_direction):
        pos_2d = Type2D(pos[0], pos[1])
        right = pos_2d.clone().change_x_by_step(1).as_tuple()
        left = pos_2d.clone().change_x_by_step(-1).as_tuple()
        up = pos_2d.clone().change_y_by_step(-1).as_tuple()
        down = pos_2d.clone().change_y_by_step(1).as_tuple()

        if current_direction == Direction.UP.value:
            if up in grid and grid[up] == '#':
                return up, Direction.UP.value
            elif right in grid and grid[right] == '#':
                return right, Direction.RIGHT.value
            elif left in grid and grid[left] == '#':
                return left, Direction.LEFT.value
            else:
                print('Pos no turn at=', pos, ', direction=', current_direction)
                return pos, current_direction
        elif current_direction == Direction.RIGHT.value:
            if right in grid and grid[right] == '#':
                return right, Direction.RIGHT.value
            elif up in grid and grid[up] == '#':
                return up, Direction.UP.value
            elif down in grid and grid[down] == '#':
                return down, Direction.DOWN.value
            else:
                print('Pos no turn at=', pos, ', direction=', current_direction)
                return pos, current_direction
        elif current_direction == Direction.DOWN.value:
            if down in grid and grid[down] == '#':
                return down, Direction.DOWN.value
            elif left in grid and grid[left] == '#':
                return left, Direction.LEFT.value
            elif right in grid and grid[right] == '#':
                return right, Direction.RIGHT.value
            else:
                print('Pos no turn at=', pos, ', direction=', current_direction)
                return pos, current_direction
        elif current_direction == Direction.LEFT.value:
            if left in grid and grid[left] == '#':
                return left, Direction.LEFT.value
            elif up in grid and grid[up] == '#':
                return up, Direction.UP.value
            elif down in grid and grid[down] == '#':
                return down, Direction.DOWN.value
            else:
                print('Pos no turn at=', pos, ', direction=', current_direction)
                return pos, current_direction
        else:
            print("unknown")

    def get_direction(self, pos, grid, current_direction):
        pos_2d = Type2D(pos[0], pos[1])
        right = pos_2d.clone().change_x_by_step(1).as_tuple()
        left = pos_2d.clone().change_x_by_step(-1).as_tuple()
        up = pos_2d.clone().change_y_by_step(1).as_tuple()
        down = pos_2d.clone().change_y_by_step(-1).as_tuple()

        if current_direction == Direction.UP.value:
            if up in grid and grid[up] == '#':
                return Direction.UP.value
            elif right in grid and grid[right] == '#':
                return Direction.RIGHT.value
            elif left in grid and grid[left] == '#':
                return Direction.LEFT.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == Direction.RIGHT.value:
            if right in grid and grid[right] == '#':
                return Direction.RIGHT.value
            elif up in grid and grid[up] == '#':
                return Direction.UP.value
            elif down in grid and grid[down] == '#':
                return Direction.DOWN.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == Direction.DOWN.value:
            if down in grid and grid[down] == '#':
                return Direction.DOWN.value
            elif left in grid and grid[left] == '#':
                return Direction.LEFT.value
            elif right in grid and grid[right] == '#':
                return Direction.RIGHT.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        elif current_direction == Direction.LEFT.value:
            if left in grid and grid[left] == '#':
                return Direction.LEFT.value
            elif up in grid and grid[up] == '#':
                return Direction.UP.value
            elif down in grid and grid[down] == '#':
                return Direction.DOWN.value
            else:
                print('Pos impossible no turn at=', pos, ', direction=', current_direction)
        else:
            print("unknown")


if __name__ == "__main__":
    today = Day17()

    # print("Solution 1=", today.get_solution_1())
    today.get_solution_2()
