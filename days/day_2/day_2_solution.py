#! /usr/bin/env python3
from enum import Enum


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    HALT = 99


def get_raw_inputs():
    with open("day_2.input") as inputs:
        str_inputs = inputs.readline().split(",")

    return list(map(lambda str_input: int(str_input), str_inputs))


def get_updated_inputs():
    raw_inputs = get_raw_inputs()
    raw_inputs[1] = 12
    raw_inputs[2] = 2
    return raw_inputs


def perform_operation(inputs, op_zero_based_position):
    op_code = inputs[op_zero_based_position]
    if op_code == Opcode.HALT.value:
        return op_zero_based_position

    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]
    output_pos = inputs[op_zero_based_position + 3]
    input_1 = inputs[input_1_pos]
    input_2 = inputs[input_2_pos]

    if op_code == Opcode.ADD.value:
        inputs[output_pos] = input_1 + input_2
        return op_zero_based_position + 4
    elif op_code == Opcode.MULTIPLY.value:
        inputs[output_pos] = input_1 * input_2
        return op_zero_based_position + 4


def run_program(inputs):
    previous_op_position = 0

    next_op_position = perform_operation(inputs, previous_op_position)
    while next_op_position != previous_op_position:
        previous_op_position = next_op_position
        next_op_position = perform_operation(inputs, next_op_position)

    return inputs


def find_param_combination(expected_value_at_address_0):
    for noun in range(100):
        for verb in range(100):
            inputs = get_raw_inputs()
            inputs[1] = noun
            inputs[2] = verb
            outputs = run_program(inputs)
            print(noun, verb, outputs[0])
            if outputs[0] == expected_value_at_address_0:
                print(100 * noun + verb)
                return


if __name__ == "__main__":
    find_param_combination(19690720)
