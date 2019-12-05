#! /usr/bin/env python3
from enum import Enum


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class ParamMode(Enum):
    POSITION = 0  # param value is address to final value
    IMMEDIATE = 1  # param value is final value


def perform_input(op_zero_based_position, inputs, param_modes):
    raw_input_value = input("Please give a value:")
    pos_to_update = inputs[op_zero_based_position + 1]
    inputs[pos_to_update] = int(raw_input_value)
    return op_zero_based_position + 2


def perform_output(op_zero_based_position, inputs, param_modes):
    pos_to_get_value = inputs[op_zero_based_position + 1]
    value = inputs[pos_to_get_value]
    print("Output value:", value)
    return op_zero_based_position + 2


def perform_add(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]
    output_pos = inputs[op_zero_based_position + 3]
    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos
    inputs[output_pos] = input_1 + input_2

    return op_zero_based_position + 4


def perform_multiply(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]
    output_pos = inputs[op_zero_based_position + 3]
    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos
    inputs[output_pos] = input_1 * input_2

    return op_zero_based_position + 4


def perform_jump_if_true(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]

    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos

    return input_2 if input_1 != 0 else op_zero_based_position + 3


def perform_jump_if_false(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]

    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos

    return input_2 if input_1 == 0 else op_zero_based_position + 3


def perform_less_than(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]
    output_pos = inputs[op_zero_based_position + 3]

    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos

    if input_1 < input_2:
        inputs[output_pos] = 1
    else:
        inputs[output_pos] = 0

    return op_zero_based_position + 4


def perform_equals(op_zero_based_position, inputs, param_modes):
    input_1_pos = inputs[op_zero_based_position + 1]
    input_2_pos = inputs[op_zero_based_position + 2]
    output_pos = inputs[op_zero_based_position + 3]

    input_1 = inputs[input_1_pos] if param_modes[0] == ParamMode.POSITION.value else input_1_pos
    input_2 = inputs[input_2_pos] if param_modes[1] == ParamMode.POSITION.value else input_2_pos

    if input_1 == input_2:
        inputs[output_pos] = 1
    else:
        inputs[output_pos] = 0

    return op_zero_based_position + 4


def perform_halt(op_zero_based_position, inputs, param_modes):
    return op_zero_based_position


def get_op_and_actions():
    return {
        Opcode.HALT.value: perform_halt,
        Opcode.ADD.value: perform_add,
        Opcode.MULTIPLY.value: perform_multiply,
        Opcode.INPUT.value: perform_input,
        Opcode.OUTPUT.value: perform_output,
        Opcode.JUMP_IF_TRUE.value: perform_jump_if_true,
        Opcode.JUMP_IF_FALSE.value: perform_jump_if_false,
        Opcode.LESS_THAN.value: perform_less_than,
        Opcode.EQUALS.value: perform_equals
    }


def perform_operation(inputs, op_zero_based_pos):
    opcode_info_str = str(inputs[op_zero_based_pos])
    (op_code, param_modes) = parse_opcode_and_param_mode(opcode_info_str)
    return get_op_and_actions()[op_code](op_zero_based_pos, inputs, param_modes)


def parse_opcode_and_param_mode(opcode_info_str):
    op_code = int(opcode_info_str[-2:])

    ordered_param_modes_str = (opcode_info_str[:-2])[::-1]

    return op_code, get_param_modes(op_code, ordered_param_modes_str)


def get_param_modes(op_code, ordered_param_modes_str):
    if op_code in [Opcode.ADD.value, Opcode.MULTIPLY.value, Opcode.LESS_THAN.value, Opcode.EQUALS.value]:
        param_modes_str = "{:0<3}".format(ordered_param_modes_str)
    elif op_code in [Opcode.JUMP_IF_FALSE.value, Opcode.JUMP_IF_TRUE.value]:
        param_modes_str = "{:0<2}".format(ordered_param_modes_str)
    elif op_code in [Opcode.INPUT.value, Opcode.OUTPUT.value]:
        param_modes_str = "{:0<1}".format(ordered_param_modes_str)
    else:
        param_modes_str = ""

    return [int(mode) for mode in param_modes_str]


def run_program(inputs):
    previous_op_position = 0

    next_op_position = perform_operation(inputs, previous_op_position)
    while next_op_position != previous_op_position:
        previous_op_position = next_op_position
        next_op_position = perform_operation(inputs, next_op_position)

    return inputs


def get_inputs():
    with open("day_5.input") as inputs:
        return list(map(lambda v: int(v), inputs.readline().split(",")))


def solution_1():
    run_program(get_inputs())


if __name__ == "__main__":
    solution_1()
