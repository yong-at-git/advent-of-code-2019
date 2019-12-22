#! /usr/bin/env python3
from days.commons.inputs_reader import get_list_of_raw_lines
import string


class Day20:
    def __init__(self):
        self._grid = {}

    @property
    def grid(self):
        return self._grid

    def get_raw_grid(self):
        lines = get_list_of_raw_lines("day_20.input")
        raw_grid = {}
        x = 0
        y = 0

        for line in lines:
            for c in line:
                raw_grid[(x, y)] = c
                x += 1
            y += 1
        return raw_grid

    def get_chars(self):
        raw_grid = self.get_raw_grid()
        char_list = list(filter(lambda item: item[1] in string.ascii_uppercase, raw_grid.items()))
        return char_list

    def get_labels(self):
        raw_grid = self.get_raw_grid()
        chars = self.get_chars()




    def get_solution_1(self):
        return self.get_chars()


if __name__ == "__main__":
    today = Day20()

    print("Solution 1=", today.get_solution_1())
