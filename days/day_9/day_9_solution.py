#! /usr/bin/env python3
from days.commons.intcode_computer import IntcodeComputer


def get_inputs_list():
    with open("day_9.input") as inputs:
        return list(map(int, inputs.readline().split(",")))


def get_list_1():
    return [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]


def get_list_2():
    return [1102, 34915192, 34915192, 7, 4, 7, 99, 0]


def get_list_3():
    return [104, 1125899906842624, 99]


def get_inputs():
    inputs_list = get_inputs_list()

    inputs_dict = {}
    for i in range(len(inputs_list)):
        inputs_dict[i] = inputs_list[i]

    return inputs_dict


def get_solution_1():
    intcode_computer = IntcodeComputer(0)
    intcode_computer.predefined_values_for_input_instruction.append(1)
    intcode_computer.inputs_dict = get_inputs()
    intcode_computer.run_program()

    return intcode_computer.outputs[-1]


def get_solution_2():
    intcode_computer = IntcodeComputer(0)
    intcode_computer.predefined_values_for_input_instruction.append(2)
    intcode_computer.inputs_dict = get_inputs()
    intcode_computer.run_program()

    return intcode_computer.outputs[-1]


if __name__ == "__main__":
    print("Solution 1=", get_solution_1())
    print("Solution 2=", get_solution_2())
