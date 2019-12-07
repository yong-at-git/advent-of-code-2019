#! /usr/bin/env python3

from itertools import permutations
from days.day_5.day_5_solution import run_program
from queue import Queue


def get_phase_setting_sequences():
    possible_values = [0, 1, 2, 3, 4]
    sequence_length = 5

    return permutations(possible_values, sequence_length)


def get_inputs():
    with open("day_7.input") as inputs:
        return list(map(lambda v: int(v), inputs.readline().split(",")))


def get_output_from_amplifier(phase_value, input_signal, inputs):
    values_for_input_instruction = Queue(2)
    values_for_input_instruction.put(phase_value)
    values_for_input_instruction.put(input_signal)
    return run_program(values_for_input_instruction, inputs)[-1]


def get_solution_1():
    final_output_signals = []
    for phase_setting_sequence in get_phase_setting_sequences():
        input_signal = 0
        for phase_value in phase_setting_sequence:
            inputs = get_inputs()
            input_signal = get_output_from_amplifier(phase_value, input_signal, inputs)
        final_output_signals.append(input_signal)

    return max(final_output_signals)


if __name__ == "__main__":
    print("Solution 1=", get_solution_1())
