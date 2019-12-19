#! /usr/bin/env python3
from days.commons.inputs_reader import get_list_of_raw_lines
from days.commons.outputs_utils import print_grid
from days.commons.data_types import Direction, TurnStr, Type2D
from enum import Enum
import string


class Mark(Enum):
    ENTRANCE = '@'
    PASSAGE = '.'
    WALL = '#'


class Day18:
    def __init__(self):
        self._collected_keys = []
        self._keys_positions = []
        self._doors_positions = []
        self._passages_positions = []
        self._grid = {}
        self._entrance_2d = None
        self._standing_position_2d = None
        self._blocking_doors = []
        self._visited = []

    @property
    def visited(self):
        return self._visited

    @property
    def collected_keys(self):
        return self._collected_keys

    @property
    def keys_positions(self):
        return self._keys_positions

    @property
    def doors_positions(self):
        return self._doors_positions

    @property
    def passages_positions(self):
        return self._passages_positions

    @property
    def entrance_2d(self):
        return self._entrance_2d

    @entrance_2d.setter
    def entrance_2d(self, value):
        self._entrance_2d = value

    @property
    def standing_position_2d(self):
        return self._standing_position_2d

    @standing_position_2d.setter
    def standing_position_2d(self, value):
        self._standing_position_2d = value

    @property
    def grid(self):
        return self._grid

    @property
    def blocking_doors(self):
        return self._blocking_doors

    @staticmethod
    def get_key_marks():
        return [c for c in string.ascii_lowercase]

    @staticmethod
    def get_door_marks():
        return [c for c in string.ascii_uppercase]

    def parse_inputs(self):
        x = y = 0
        for line in self.get_raw_inputs_lines():
            for c in line:
                pos = Type2D(x, y)

                self.grid[pos.as_tuple()] = c

                if c == Mark.ENTRANCE.value:
                    self.entrance_2d = pos.clone()
                    self.standing_position_2d = pos.clone()
                elif c in Day18.get_key_marks():
                    self.keys_positions.append(pos.as_tuple())
                elif c in Day18.get_door_marks():
                    self.doors_positions.append(pos.as_tuple())
                elif c == Mark.PASSAGE.value:
                    self.passages_positions.append(pos.as_tuple())

                x += 1

            x = 0
            y += 1

    def get_raw_inputs_lines(self):
        return get_list_of_raw_lines("day_18.input")

    def move(self):
        self.grid[self.entrance_2d.as_tuple()] = Mark.PASSAGE.value
        self.visited.append(self.entrance_2d.as_tuple())

        while len(self.collected_keys) < len(self.keys_positions):
            next_pos = self.get_next_pos()

            if self.is_key(next_pos):
                self.collect_key(next_pos)
            elif self.is_openable_door(next_pos):
                self.open_door(next_pos)
            elif self.is_new_passage(next_pos):
                self.visit_new_passage(next_pos)
            elif self.is_passage(next_pos):
                self.revisit_passage(next_pos)
            else:
                print("Error on making move")

            #print(self.standing_position_2d.as_tuple())

        print("Done!")

    def collect_key(self, pos):
        self.grid[pos] = Mark.PASSAGE.value
        self.collected_keys.append(self.grid[pos])
        self.visited.append(pos)

        if self.should_be_marked_as_wall(pos):
            self.mark_as_wall(pos)

        self.standing_position_2d = Type2D.from_tuple(pos)

    def open_door(self, pos):
        self.grid[pos] = Mark.PASSAGE.value
        self.visited.append(pos)

        if self.should_be_marked_as_wall(pos):
            self.mark_as_wall(pos)

        self.standing_position_2d = Type2D.from_tuple(pos)

    def visit_new_passage(self, pos):
        self.visited.append(pos)

        if self.should_be_marked_as_wall(pos):
            self.mark_as_wall(pos)

        self.standing_position_2d = Type2D.from_tuple(pos)

    def revisit_passage(self, pos):
        if self.should_be_marked_as_wall(pos):
            self.mark_as_wall(pos)

        self.standing_position_2d = Type2D.from_tuple(pos)

    def har_key(self, door_pos):
        door_mark = self.grid[door_pos]
        matching_key = self.get_key_marks()[self.get_door_marks().index(door_mark)]
        return matching_key in self.collected_keys

    def is_openable_door(self, pos):
        return pos in self.doors_positions and self.har_key(pos)

    def is_key(self, pos):
        return pos in self.keys_positions

    def is_passage(self, pos):
        return pos in self.grid and self.grid[pos] == Mark.PASSAGE.value

    def is_new_passage(self, pos):
        return pos not in self.visited and self.is_passage(pos)

    def get_next_pos(self):
        return self.get_next_pos_method_1()

    def get_next_pos_method_1(self):
        up = self.standing_position_2d.clone().up_move_by_minus_y().as_tuple()
        right = self.standing_position_2d.clone().right_move().as_tuple()
        down = self.standing_position_2d.clone().down_move_by_plus_y().as_tuple()
        left = self.standing_position_2d.clone().left_move().as_tuple()

        # 1. clockwise to find the 1st key
        key_pos = next(filter(self.is_key, [up, right, down, left]), None)
        if key_pos:
            return key_pos

        # 2. clockwise to find the 1st door that can be opened
        door_pos = next(filter(self.is_openable_door, [up, right, down, left]), None)
        if door_pos:
            return door_pos

        # 3. clockwise to find the first not visited passage
        new_passage = next(filter(self.is_new_passage, [up, right, down, left]), None)
        if new_passage:
            return new_passage

        # 4. clockwise to find the first passage
        visited_passage = next(filter(self.is_passage, [up, right, down, left]), None)
        if visited_passage:
            return visited_passage
        else:
            print("ERROR, no move pos for=", self.standing_position_2d.as_tuple)

    def should_be_marked_as_wall(self, pos):
        try_pos = Type2D.from_tuple(pos)

        up = try_pos.clone().up_move_by_minus_y().as_tuple()
        right = try_pos.clone().right_move().as_tuple()
        down = try_pos.clone().down_move_by_plus_y().as_tuple()
        left = try_pos.clone().left_move().as_tuple()

        # boundary checking
        neigbor_count = len(list(filter(lambda pos: pos in self.grid, [up, right, down, left])))
        if neigbor_count != 4:
            return True

        # 3 wall checking
        wall_neighbor_count = len(list(filter(lambda pos: self.grid[pos] == Mark.WALL.value, [up, right, down, left])))
        return wall_neighbor_count == 3

    def mark_as_wall(self, pos):
        self.grid[pos] = Mark.WALL.value
        self.passages_positions.remove(pos)

    def get_solution_1(self):
        self.parse_inputs()
        self.move()
        # print_grid(self.grid)


if __name__ == "__main__":
    today = Day18()

    today.get_solution_1()
    # print(len(today.keys_positions), len(today.doors_positions))
