#! /usr/bin/env python3
from days.commons.data_types import Type2D
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
from days.commons.intcode_computer import IntcodeComputer
from days.commons.outputs_utils import print_grid, print_int_grid


class Day19:
    def get_inputs_dict(self):
        return get_single_line_and_parse_to_dicts("day_19.input")

    def get_output_for_pos(self, inputs_dict, pos_2d):
        computer = IntcodeComputer()
        computer.inputs_dict = inputs_dict.copy()

        while not computer.is_halted:
            computer.perform_operation()

            if computer.is_waiting:
                computer.predefined_values_for_input_instruction.append(pos_2d.x)
                computer.predefined_values_for_input_instruction.append(pos_2d.y)

            if len(computer.outputs) == 1:
                ut = computer.outputs[0]
                return ut

    def get_solution_1(self):

        grid = {}
        inputs_dict = self.get_inputs_dict()

        for y in range(0, 50):
            for x in range(0, 50):
                grid[(x, y)] = self.get_output_for_pos(inputs_dict, Type2D(x, y))

        print_int_grid(grid)

        return len(list(filter(lambda v: v == 1, grid.values())))

    def test(self):
        grid = {}
        inputs_dict = self.get_inputs_dict()

        for y in range(955, 1056):
            for x in range(530, 802):
                grid[(x, y)] = self.get_output_for_pos(inputs_dict, Type2D(x, y))

        print_int_grid(grid)

    def get_top_right_pos_2d(self):
        inputs_dict = self.get_inputs_dict()

        current_pos_2d = Type2D(2, 3)

        while 1:
            right_down = current_pos_2d.clone().down_move_by_plus_y()
            down_right = current_pos_2d.clone().down_move_by_plus_y().right_move()

            down_left = current_pos_2d.clone().change_y_by_step(99).change_x_by_step(-99)
            down_left_ut = self.get_output_for_pos(inputs_dict, down_left)

            if down_left_ut == 1:
                print("Found! Current_pos=", current_pos_2d.as_tuple())
                return current_pos_2d

            down_right_ut = self.get_output_for_pos(inputs_dict, down_right)

            current_pos_2d = down_right if down_right_ut == 1 else right_down

    def get_solution_2(self):
        tr_2d = self.get_top_right_pos_2d()
        square_left_top_x = tr_2d.clone().change_x_by_step(-99).x
        return 10000 * square_left_top_x + tr_2d.y


if __name__ == "__main__":
    today = Day19()

    # print("Solution 1=", today.get_solution_1())
    # today.test()
    print("Solution 2=", today.get_solution_2())
