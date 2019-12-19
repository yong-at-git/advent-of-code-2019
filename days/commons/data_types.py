#! /usr/bin/env python3
from enum import Enum


class TurnStr(Enum):
    LEFT = 'L'
    RIGHT = 'R'


class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'


class Type2D:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __repr__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    @staticmethod
    def from_tuple(t):
        return Type2D(t[0], t[1])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def as_tuple(self):
        return self.x, self.y

    def clone(self):
        return Type2D(self.x, self.y)

    def change_x_by_step(self, step=1):
        self._x = self._x + step
        return self

    def change_y_by_step(self, step=1):
        self._y = self._y + step
        return self

    def up_move_by_minus_y(self):
        return self.change_y_by_step(-1)

    def left_move(self):
        return self.change_x_by_step(-1)

    def right_move(self):
        return self.change_x_by_step(1)

    def down_move_by_plus_y(self):
        return self.change_y_by_step(1)


class Type3D:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value


if __name__ == "__main__":
    print()
