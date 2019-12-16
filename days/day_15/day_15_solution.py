#! /usr/bin/env python3
from enum import Enum

from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.outputs_utils import print_grid
from days.commons.intcode_computer import IntcodeComputer
from days.commons.data_types import Type2D


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Status(Enum):
    HIT_WALL = 0
    MOVED = 1
    FOUND = 2


class Area(Enum):
    WALL = '#'
    OK = '.'
    OXYGEN = '*'


class Day15:
    @staticmethod
    def get_inputs():
        return get_single_line_and_parse_to_dicts("day_15.input")

    def get_solution_1(self):
        grid = {}
        true_grid = {}
        return self.get_solution_1_with_populated_grid(grid, true_grid)

    def get_solution_1_with_populated_grid(self, grid, true_grid):
        computer = IntcodeComputer()
        computer.inputs_dict = Day15.get_inputs()

        standing_position = Type2D(0, 0)
        current_direction = None
        total_movements = []
        oxygen_position = None

        found_oxygen_already = False

        while not computer.is_halted:
            if found_oxygen_already:
                # print(standing_position.as_tuple())
                if standing_position.as_tuple() == (0, 0):
                    print(true_grid[(0, 0)])
                    print_grid(grid, standing_position)
                    print()
                    print_grid(true_grid, standing_position)
                    return true_grid, oxygen_position
            computer.perform_operation()

            if computer.is_waiting:
                if current_direction is None:
                    current_direction = Direction.NORTH.value
                else:
                    if current_direction == Direction.NORTH.value:
                        current_direction = self.get_direction_on_possible_move_north(grid, standing_position)
                    elif current_direction == Direction.EAST.value:
                        current_direction = self.get_direction_on_possible_move_east(grid, standing_position)
                    elif current_direction == Direction.SOUTH.value:
                        current_direction = self.get_direction_on_possible_move_south(grid, standing_position)
                    else:
                        current_direction = self.get_direction_on_possible_move_west(grid, standing_position)

                computer.predefined_values_for_input_instruction.append(current_direction)
                # print_grid(grid, standing_position.as_tuple())
                # print()
            elif len(computer.outputs) == 1:
                status_value = computer.outputs[0]
                # print(standing_position.as_tuple(), current_direction)

                if status_value == Status.HIT_WALL.value:
                    if current_direction == Direction.NORTH.value:
                        grid[standing_position.clone().change_y_by_step(1).as_tuple()] = Area.WALL.value
                        true_grid[standing_position.clone().change_y_by_step(1).as_tuple()] = Area.WALL.value

                        current_direction = self.get_direction_after_hitting_north_wall(grid, standing_position)
                    elif current_direction == Direction.EAST.value:
                        grid[standing_position.clone().change_x_by_step(1).as_tuple()] = Area.WALL.value
                        true_grid[standing_position.clone().change_x_by_step(1).as_tuple()] = Area.WALL.value

                        current_direction = self.get_direction_after_hitting_east_wall(grid, standing_position)
                    elif current_direction == Direction.SOUTH.value:
                        grid[standing_position.clone().change_y_by_step(-1).as_tuple()] = Area.WALL.value
                        true_grid[standing_position.clone().change_y_by_step(-1).as_tuple()] = Area.WALL.value

                        current_direction = self.get_direction_after_hitting_south_wall(grid, standing_position)
                    else:
                        grid[standing_position.clone().change_x_by_step(-1).as_tuple()] = Area.WALL.value
                        true_grid[standing_position.clone().change_x_by_step(-1).as_tuple()] = Area.WALL.value

                        current_direction = self.get_direction_after_hitting_west_wall(grid, standing_position)
                elif status_value == Status.MOVED.value:
                    self.standing_position_wall_mark_check(grid, current_direction, standing_position)

                    if current_direction == Direction.NORTH.value:
                        standing_position.change_y_by_step(1)
                    elif current_direction == Direction.EAST.value:
                        standing_position.change_x_by_step(1)
                    elif current_direction == Direction.SOUTH.value:
                        standing_position.change_y_by_step(-1)
                    else:
                        standing_position.change_x_by_step(-1)
                    grid[standing_position.as_tuple()] = Area.OK.value
                    true_grid[standing_position.as_tuple()] = Area.OK.value
                    total_movements.append(1)
                else:
                    # print_grid(grid, standing_position.as_tuple())
                    # print()
                    if current_direction == Direction.NORTH.value:
                        standing_position.change_y_by_step(1)
                    elif current_direction == Direction.EAST.value:
                        standing_position.change_x_by_step(1)
                    elif current_direction == Direction.SOUTH.value:
                        standing_position.change_y_by_step(-1)
                    else:
                        standing_position.change_x_by_step(-1)

                    if found_oxygen_already:
                        print_grid(true_grid, standing_position)
                        return

                    grid[standing_position.as_tuple()] = Area.WALL.value
                    true_grid[standing_position.as_tuple()] = Area.OXYGEN.value
                    found_oxygen_already = True
                    oxygen_position = standing_position.clone()
                    # print_grid(true_grid, standing_position.as_tuple())
                    # print()
                    # return grid

                del computer.outputs[0]

    def get_solution_2(self):
        true_grid, oxygen_position = self.get_solution_1()
        oxygen_count = len(list(filter(lambda area: area == Area.OK.value, true_grid.values())))
        oxygen_list = [oxygen_position.as_tuple()]
        minute = 0
        while len(oxygen_list) != oxygen_count:
            minute += 1
            copy_list = oxygen_list.copy()
            for oxygen_position in copy_list:
                north = Type2D(oxygen_position[0], oxygen_position[1]).change_y_by_step(1).as_tuple()
                south = Type2D(oxygen_position[0], oxygen_position[1]).change_y_by_step(-1).as_tuple()
                east = Type2D(oxygen_position[0], oxygen_position[1]).change_x_by_step(1).as_tuple()
                west = Type2D(oxygen_position[0], oxygen_position[1]).change_x_by_step(-1).as_tuple()

                if true_grid[north] == Area.OK.value and north not in oxygen_list:
                    oxygen_list.append(north)

                if true_grid[east] == Area.OK.value and east not in oxygen_list:
                    oxygen_list.append(east)

                if true_grid[south] == Area.OK.value and south not in oxygen_list:
                    oxygen_list.append(south)

                if true_grid[west] == Area.OK.value and west not in oxygen_list:
                    oxygen_list.append(west)

            print(minute, len(oxygen_list), oxygen_count)
        return minute

    def get_direction_on_possible_move_north(self, grid, standing_position):
        north = standing_position.clone().change_y_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        west = standing_position.clone().change_x_by_step(-1)

        if north.as_tuple() not in grid:
            if east.as_tuple() in grid and grid[east.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if east.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if west.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[east.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[west.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if grid[north.as_tuple()] == Area.WALL.value and grid[west.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if grid[north.as_tuple()] == Area.OK.value:
            return Direction.NORTH.value

        if grid[east.as_tuple()] == Area.OK.value:
            return Direction.EAST.value

        if grid[west.as_tuple()] == Area.OK.value:
            return Direction.WEST.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.SOUTH.value

    def get_direction_on_possible_move_east(self, grid, standing_position):
        north = standing_position.clone().change_y_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        west = standing_position.clone().change_x_by_step(-1)

        if east.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if north.as_tuple() not in grid:
            if east.as_tuple() in grid and grid[east.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if south.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and grid[
                east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            west.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[west.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if grid[east.as_tuple()] == Area.OK.value:
            return Direction.EAST.value

        if grid[north.as_tuple()] == Area.OK.value:
            return Direction.NORTH.value

        if grid[south.as_tuple()] == Area.OK.value:
            return Direction.SOUTH.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.WEST.value

    def get_direction_on_possible_move_south(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        south = standing_position.clone().change_y_by_step(-1)
        north = standing_position.clone().change_y_by_step(1)
        east = standing_position.clone().change_x_by_step(1)

        if south.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and grid[
                east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if east.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if west.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[east.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            east.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[east.as_tuple()] == Area.OK.value:
            return Direction.EAST.value

        if grid[south.as_tuple()] == Area.OK.value:
            return Direction.SOUTH.value

        if grid[west.as_tuple()] == Area.OK.value:
            return Direction.WEST.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.NORTH.value

    def get_direction_on_possible_move_west(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        north = standing_position.clone().change_y_by_step(1)

        if west.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[east.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if north.as_tuple() not in grid:
            if east.as_tuple() in grid and grid[east.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if south.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and west.as_tuple() in grid and \
                    grid[west.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and grid[
                east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[east.as_tuple()] == Area.WALL.value and grid[
            south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if grid[west.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
            east.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[west.as_tuple()] == Area.OK.value:
            return Direction.WEST.value

        if grid[north.as_tuple()] == Area.OK.value:
            return Direction.NORTH.value

        if grid[south.as_tuple()] == Area.OK.value:
            return Direction.SOUTH.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.EAST.value

    def get_direction_after_hitting_west_wall(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        north = standing_position.clone().change_y_by_step(1)

        if north.as_tuple() not in grid:
            if south.as_tuple() in grid and grid[south.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[
                        east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if south.as_tuple() not in grid:
            if north.as_tuple() in grid and grid[north.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[
                        east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[north.as_tuple()] == Area.WALL.value and grid[south.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if grid[north.as_tuple()] == Area.OK.value:
            return Direction.NORTH.value

        if grid[south.as_tuple()] == Area.OK.value:
            return Direction.SOUTH.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.EAST.value

    def get_direction_after_hitting_south_wall(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        north = standing_position.clone().change_y_by_step(1)

        if east.as_tuple() not in grid:
            if west.as_tuple() in grid and grid[west.as_tuple()] == Area.WALL.value and east.as_tuple() in grid and \
                    grid[east.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if west.as_tuple() not in grid:
            if east.as_tuple() in grid and grid[east.as_tuple()] == Area.WALL.value and north.as_tuple() in grid and \
                    grid[north.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[west.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if grid[east.as_tuple()] == Area.OK.value:
            return Direction.EAST.value

        if grid[west.as_tuple()] == Area.OK.value:
            return Direction.WEST.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.NORTH.value

    def get_direction_after_hitting_east_wall(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        north = standing_position.clone().change_y_by_step(1)

        if north.as_tuple() not in grid:
            if west.as_tuple() in grid and grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and \
                    grid[south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.NORTH.value

        if south.as_tuple() not in grid:
            if west.as_tuple() in grid and grid[west.as_tuple()] == Area.WALL.value and north.as_tuple() in grid and \
                    grid[north.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[south.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[north.as_tuple()] == Area.OK.value:
            return Direction.NORTH.value

        if grid[south.as_tuple()] == Area.OK.value:
            return Direction.SOUTH.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.WEST.value

    def get_direction_after_hitting_north_wall(self, grid, standing_position):
        west = standing_position.clone().change_x_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)

        if east.as_tuple() not in grid:
            if west.as_tuple() in grid and grid[west.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and \
                    grid[south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.EAST.value

        if west.as_tuple() not in grid:
            if east.as_tuple() in grid and grid[east.as_tuple()] == Area.WALL.value and south.as_tuple() in grid and \
                    grid[south.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.WEST.value

        if grid[east.as_tuple()] == Area.WALL.value and grid[west.as_tuple()] == Area.WALL.value:
            grid[standing_position.as_tuple()] = Area.WALL.value
            return Direction.SOUTH.value

        if grid[east.as_tuple()] == Area.OK.value:
            return Direction.EAST.value

        if grid[west.as_tuple()] == Area.OK.value:
            return Direction.WEST.value

        grid[standing_position.as_tuple()] = Area.WALL.value
        return Direction.SOUTH.value

    def standing_position_wall_mark_check(self, grid, current_direction, standing_position):
        north = standing_position.clone().change_y_by_step(1)
        south = standing_position.clone().change_y_by_step(-1)
        east = standing_position.clone().change_x_by_step(1)
        west = standing_position.clone().change_x_by_step(-1)

        if current_direction == Direction.NORTH.value:
            if south.as_tuple() in grid and east.as_tuple() in grid and west.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value and grid[east.as_tuple()] == Area.WALL.value and grid[
                west.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
        elif current_direction == Direction.EAST.value:
            if south.as_tuple() in grid and north.as_tuple() in grid and west.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value and grid[north.as_tuple()] == Area.WALL.value and grid[
                west.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
        elif current_direction == Direction.SOUTH.value:
            if north.as_tuple() in grid and east.as_tuple() in grid and west.as_tuple() in grid and grid[
                north.as_tuple()] == Area.WALL.value and grid[east.as_tuple()] == Area.WALL.value and grid[
                west.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value
        else:
            if south.as_tuple() in grid and east.as_tuple() in grid and north.as_tuple() in grid and grid[
                south.as_tuple()] == Area.WALL.value and grid[east.as_tuple()] == Area.WALL.value and grid[
                north.as_tuple()] == Area.WALL.value:
                grid[standing_position.as_tuple()] = Area.WALL.value


if __name__ == "__main__":
    today = Day15()
    # today.get_solution_1()

    print("Solution 2=", today.get_solution_2())
