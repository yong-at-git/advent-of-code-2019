#! /usr/bin/env python3
from enum import Enum
from days.commons.intcode_computer import IntcodeComputer


class PanelColor(Enum):
    BLACK = 0
    WHITE = 1


class Turn(Enum):
    LEFT = 0
    RIGHT = 1


class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'


class Day11Solution:
    def __init__(self):
        self._painted_panels = {}
        self._current_position = (0, 0)
        self._current_direction = Direction.UP

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, value):
        self._current_position = value

    @property
    def painted_panels(self):
        return self._painted_panels

    @property
    def current_direction(self):
        return self._current_direction

    @current_direction.setter
    def current_direction(self, value):
        self._current_direction = value

    def get_inputs(self):
        with open("day_11.input") as inputs:
            return list(map(int, inputs.readline().split(",")))

    def do_complete_painting(self):
        inputs_list = self.get_inputs()
        inputs_dict = {}
        for i in range(len(inputs_list)):
            inputs_dict[i] = inputs_list[i]
        computer = IntcodeComputer(0)
        computer.inputs_dict = inputs_dict
        is_waiting_color_output = True
        while not computer.is_halted:
            computer.perform_operation()
            if computer.is_waiting:
                if self.current_position not in self.painted_panels:
                    computer.predefined_values_for_input_instruction.append(PanelColor.BLACK.value)
                else:
                    use_color = self.painted_panels[self.current_position]
                    computer.predefined_values_for_input_instruction.append(use_color)

            if len(computer.outputs) == 1:
                if is_waiting_color_output:
                    color_value_to_paint = computer.outputs[0]
                    self.painted_panels[self.current_position] = color_value_to_paint
                    del computer.outputs[0]
                    is_waiting_color_output = False
                else:
                    direction_value = computer.outputs[0]
                    self.adjust_direction_and_move(direction_value)
                    del computer.outputs[0]
                    is_waiting_color_output = True

    def adjust_direction_and_move(self, output_value_for_direction):
        if output_value_for_direction == Turn.LEFT.value:
            if self.current_direction == Direction.UP:
                self.current_direction = Direction.LEFT
                self.current_position = (self.current_position[0] - 1, self.current_position[1])
            elif self.current_direction == Direction.LEFT:
                self.current_direction = Direction.DOWN
                self.current_position = (self.current_position[0], self.current_position[1] - 1)
            elif self.current_direction == Direction.RIGHT:
                self.current_direction = Direction.UP
                self.current_position = (self.current_position[0], self.current_position[1] + 1)
            else:  # currently facing down
                self.current_direction = Direction.RIGHT
                self.current_position = (self.current_position[0] + 1, self.current_position[1])

        if output_value_for_direction == Turn.RIGHT.value:
            if self.current_direction == Direction.UP:
                self.current_direction = Direction.RIGHT
                self.current_position = (self.current_position[0] + 1, self.current_position[1])
            elif self.current_direction == Direction.LEFT:
                self.current_direction = Direction.UP
                self.current_position = (self.current_position[0], self.current_position[1] + 1)
            elif self.current_direction == Direction.RIGHT:
                self.current_direction = Direction.DOWN
                self.current_position = (self.current_position[0], self.current_position[1] - 1)
            else:  # currently facing down
                self.current_direction = Direction.LEFT
                self.current_position = (self.current_position[0] - 1, self.current_position[1])

    def get_solution_1(self):
        self.do_complete_painting()

        return len(self.painted_panels.keys())

    def get_solution_2(self):
        self.painted_panels[(0, 0)] = PanelColor.WHITE.value
        self.do_complete_painting()

        x_values = []
        y_values = []
        for x, y in self.painted_panels.keys():
            x_values.append(x)
            y_values.append(y)

        for x in range(min(x_values), max(x_values) + 1):
            row_str = ""
            for y in range(min(y_values), max(y_values) + 1):
                if (x, y) in self.painted_panels:
                    if self.painted_panels[(x, y)] == PanelColor.WHITE.value:
                        row_str += "1"
                    else:
                        row_str += " "
                else:
                    row_str += " "
            print(row_str)


if __name__ == "__main__":
    solution = Day11Solution()

    print("Solution 1=", solution.get_solution_1())

    solution = Day11Solution()
    solution.get_solution_2()
