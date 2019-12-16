#! /usr/bin/env python3
from days.commons.inputs_reader import get_fist_line_as_raw_str
import numpy


class Day16:
    def get_inputs(self):
        return get_fist_line_as_raw_str("day_16.input")

    def get_input_as_list_of_single_digit(self):
        return [int(i) for i in self.get_inputs()]

    def get_digits_list_from_num(self, num):
        return [int(i) for i in str(num)]

    def get_base_pattern(self):
        return [0, 1, 0, -1]

    def get_final_pattern(self, elem_zero_based_position, total_elements_count):
        repeat_times = elem_zero_based_position + 1
        pattern_after_repeat = numpy.repeat(self.get_base_pattern(), repeat_times).tolist()
        while len(pattern_after_repeat) - 1 < total_elements_count:
            pattern_after_repeat.extend(pattern_after_repeat)
        return pattern_after_repeat[1:total_elements_count + 1]

    def get_sum_of_list_products(self, a, b):
        return sum(x * y for x, y in zip(a, b))

    def get_ones_digit(self, nb):
        return abs(nb) % 10

    def get_single_phase_output(self, input_num_list):
        output = []
        input_len = len(input_num_list)
        for i in range(input_len):
            pattern_list = self.get_final_pattern(i, input_len)
            raw_sum = self.get_sum_of_list_products(input_num_list, pattern_list)
            output.append(self.get_ones_digit(raw_sum))
        return output

    def get_output_as_list(self, init_input_num_list, num_of_phases):
        ins = init_input_num_list
        for i in range(num_of_phases):
            ins = self.get_single_phase_output(ins)
        return ins

    def get_output_as_str(self, init_input_num_list, num_of_phases):
        out = self.get_output_as_list(init_input_num_list, num_of_phases)
        return "".join(str(i) for i in out)

    def get_solution_1(self):
        ins = self.get_input_as_list_of_single_digit()
        return self.get_output_as_str(ins, 100)[0:8]


if __name__ == "__main__":
    today = Day16()

    print("Solution 1=", today.get_solution_1())
