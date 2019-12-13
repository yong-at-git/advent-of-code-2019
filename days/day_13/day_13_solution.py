#! /usr/bin/env python3
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from enum import Enum
from days.commons.intcode_computer import IntcodeComputer
import matplotlib.pyplot as plt


class TileId(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4


class JoyStickPosition(Enum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


class Day13:
    def __init__(self):
        pass

    @staticmethod
    def get_solution_1():
        dict_inputs = get_single_line_and_parse_to_dicts("day_13.input")
        computer = IntcodeComputer()
        computer.debug = False
        computer.inputs_dict = dict_inputs

        block_count = 0
        while not computer.is_halted:
            computer.perform_operation()

            if len(computer.outputs) == 3:
                if computer.outputs[2] == TileId.BLOCK.value:
                    block_count += 1

                del computer.outputs[2]
                del computer.outputs[1]
                del computer.outputs[0]

        return block_count

    @staticmethod
    def get_solution_2():
        dict_inputs = get_single_line_and_parse_to_dicts("day_13.input")
        computer = IntcodeComputer()
        computer.debug = False
        dict_inputs[0] = 2
        computer.inputs_dict = dict_inputs
        grid = {}

        score = 0
        while not computer.is_halted:
            computer.perform_operation()

            if computer.is_waiting:
                ball_position = Day13.find_ball(grid)
                paddle_position = Day13.find_paddle(grid)
                joystick_move = Day13.get_joystick_move(ball_position, paddle_position)
                computer.predefined_values_for_input_instruction.append(joystick_move)
            elif len(computer.outputs) == 3:
                grid[(computer.outputs[0], computer.outputs[1])] = computer.outputs[2]
                if computer.outputs[0] == -1 and computer.outputs[1] == 0:
                    score = computer.outputs[2]
                del computer.outputs[2]
                del computer.outputs[1]
                del computer.outputs[0]

        return score

    @staticmethod
    def find_ball(grid):
        return list(grid.keys())[list(grid.values()).index(TileId.BALL.value)]

    @staticmethod
    def find_paddle(grid):
        return list(grid.keys())[list(grid.values()).index(TileId.HORIZONTAL_PADDLE.value)]

    @staticmethod
    def get_joystick_move(ball_pos, paddle_pos):
        if paddle_pos[0] > ball_pos[0]:
            return -1
        elif paddle_pos[0] < ball_pos[0]:
            return 1
        else:
            return 0


if __name__ == "__main__":
    today = Day13()

    print("Solution 1=", today.get_solution_1())
    print("Solution 2=", today.get_solution_2())
