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
        self._entrance = None
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
    def entrance(self):
        return self._entrance

    @entrance.setter
    def entrance(self, value):
        self._entrance = value

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
                    self.entrance = pos.as_tuple()
                    self._standing_position_2d = Type2D(x, y)
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
        while len(self.collected_keys) < len(self.keys_positions):
            try_pos = self.standing_position_2d.clone()

            up = try_pos.clone().up_move_by_minus_y().as_tuple()
            right = try_pos.clone().right_move().as_tuple()
            down = try_pos.clone().down_move_by_plus_y().as_tuple()
            left = try_pos.clone().left_move().as_tuple()

            #         print("Me at=", self.standing_position_2d.as_tuple(), ", value=",
            #              self.grid[self.standing_position_2d.as_tuple()], ", neighbors=", self.grid[up], self.grid[right],
            #             self.grid[down], self.grid[left])

            # collect the 1st encountering key clockwise and move there
            if up in self.keys_positions:
                self.collect_key(up)
                continue
            elif right in self.keys_positions:
                self.collect_key(right)
                continue
            elif down in self.keys_positions:
                self.collect_key(down)
                continue
            elif left in self.keys_positions:
                self.collect_key(left)
                continue

            # try opening any door and making move, via clockwise checking
            has_blocking_door = False
            if up in self.doors_positions:
                if self.har_key(up):
                    self.open_door(up)
                    continue
                else:
                    has_blocking_door = True
            elif right in self.doors_positions:
                if self.har_key(right):
                    self.open_door(right)
                    continue
                else:
                    has_blocking_door = True
            elif down in self.doors_positions:
                if self.har_key(down):
                    self.open_door(down)
                    continue
                else:
                    has_blocking_door = True
            elif left in self.doors_positions:
                if self.har_key(left):
                    self.open_door(left)
                    continue
                else:
                    has_blocking_door = True

            # try any unvisited passage, via clockwise checking
            if up in self.passages_positions and up not in self.visited:
                self.standing_position_2d.up_move_by_minus_y()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                self.visited.append(self.standing_position_2d.as_tuple())
                continue
            elif right in self.passages_positions and right not in self.visited:
                self.standing_position_2d.right_move()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                self.visited.append(self.standing_position_2d.as_tuple())
                continue
            elif down in self.passages_positions and down not in self.visited:
                self.standing_position_2d.down_move_by_plus_y()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                self.visited.append(self.standing_position_2d.as_tuple())
                continue
            elif left in self.passages_positions and left not in self.visited:
                self.standing_position_2d.left_move()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                self.visited.append(self.standing_position_2d.as_tuple())
                continue

            # try any passage, via clockwise checking
            if up in self.passages_positions:
                self.standing_position_2d.up_move_by_minus_y()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                continue
            elif right in self.passages_positions:
                self.standing_position_2d.right_move()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                continue
            elif down in self.passages_positions:
                self.standing_position_2d.down_move_by_plus_y()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                continue
            elif left in self.passages_positions:
                self.standing_position_2d.left_move()
                if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
                    self.mark_as_wall(self.standing_position_2d.as_tuple())
                continue
            else:
                print("impossible 2")

            print(self.standing_position_2d.as_tuple(), self.grid[self.standing_position_2d.as_tuple()])
        print("Done!")

    def collect_key(self, key_pos):
        self.collected_keys.append(self.grid[key_pos])
        self.grid[key_pos] = Mark.PASSAGE.value
        self.passages_positions.append(key_pos)
        self.visited.append(key_pos)
        self.standing_position_2d = Type2D.from_tuple(key_pos)
        if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
            self.mark_as_wall(self.standing_position_2d.as_tuple())

    def open_door(self, door_pos):
        self.grid[door_pos] = Mark.PASSAGE.value
        self.passages_positions.append(door_pos)
        self.visited.append(door_pos)
        self.standing_position_2d = Type2D.from_tuple(door_pos)
        if self.should_be_marked_as_wall(self.standing_position_2d.as_tuple()):
            self.mark_as_wall(self.standing_position_2d.as_tuple())

    def har_key(self, door_pos):
        door = self.grid[door_pos]
        matching_key = self.get_key_marks()[self.get_door_marks().index(door)]
        return matching_key in self.collect_key()

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
    print(len(today.keys_positions))
