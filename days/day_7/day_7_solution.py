#! /usr/bin/env python3

from itertools import permutations
from days.day_5.day_5_solution import run_program, perform_operation
from queue import Queue, Empty


def get_phase_setting_sequences(possible_values, sequence_length):
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
    possible_values = [0, 1, 2, 3, 4]
    sequence_length = 5

    for phase_setting_sequence in get_phase_setting_sequences(possible_values, sequence_length):
        input_signal = 0
        for phase_value in phase_setting_sequence:
            inputs = get_inputs()
            input_signal = get_output_from_amplifier(phase_value, input_signal, inputs)
        final_output_signals.append(input_signal)

    return max(final_output_signals)


def get_solution_1_oop():
    final_output_signals = []
    possible_values = [0, 1, 2, 3, 4]
    sequence_length = 5

    for phase_setting_sequence in get_phase_setting_sequences(possible_values, sequence_length):
        amplifiers = []
        for label in ['a', 'b', 'c', 'd', 'e']:
            amplifier = Amplifier(label)
            amplifier.inputs = get_inputs()
            amplifiers.append(amplifier)

        for i in range(5):
            amplifiers[i].phase_value = phase_setting_sequence[i]

        input_signal = 0

        while len(list(filter(lambda amp: not amp.is_halted, amplifiers))) == 5:
            for i in range(5):
                input_signal = amplifiers[i].run(input_signal)[-1]

        final_output_signals.append(input_signal)

    return max(final_output_signals)


################################# solution 2
class Amplifier:
    def __init__(self, label):
        self._label = label
        self._inputs = []
        self._is_halted = False
        self._phase_value = None
        self._address_to_start_execution = None
        self._outputs = []

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def is_halted(self):
        return self._is_halted

    @is_halted.setter
    def is_halted(self, value):
        self._is_halted = value

    @property
    def phase_value(self):
        return self._phase_value

    @phase_value.setter
    def phase_value(self, value):
        self._phase_value = value

    @property
    def address_to_start_execution(self):
        return self._address_to_start_execution

    @address_to_start_execution.setter
    def address_to_start_execution(self, value):
        self._address_to_start_execution = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        self._outputs = value

    def run(self, input_signal):
        values_for_input_instruction = Queue(2)
        if self.address_to_start_execution is None:
            # phase_value is only needed for the 1st run
            values_for_input_instruction.put(self.phase_value)
        values_for_input_instruction.put(input_signal)

        running_position = 0 if self.address_to_start_execution is None else self.address_to_start_execution

        try:
            self.address_to_start_execution = running_position
            next_running_position = perform_operation(values_for_input_instruction, self._inputs, self._outputs,
                                                      running_position)

            while next_running_position != running_position:
                running_position = next_running_position
                self.address_to_start_execution = running_position
                next_running_position = perform_operation(values_for_input_instruction, self._inputs, self._outputs,
                                                          next_running_position)
        except Empty:
            return self.outputs

        self.is_halted = True
        return self.outputs


def get_solution_2_with_init_inputs(inputs):
    final_output_signals = []
    possible_values = [5, 6, 7, 8, 9]
    sequence_length = 5

    for phase_setting_sequence in get_phase_setting_sequences(possible_values, sequence_length):
        amplifiers = []
        for label in ['a', 'b', 'c', 'd', 'e']:
            amplifier = Amplifier(label)
            amplifier.inputs = list(inputs)
            amplifiers.append(amplifier)

        for i in range(5):
            amplifiers[i].phase_value = phase_setting_sequence[i]

        input_signal = 0

        while len(list(filter(lambda amp: not amp.is_halted, amplifiers))) == 5:
            for i in range(5):
                input_signal = amplifiers[i].run(input_signal)[-1]

        final_output_signals.append(input_signal)

    return max(final_output_signals)


def get_solution_2():
    return get_solution_2_with_init_inputs(get_inputs())


if __name__ == "__main__":
    print("Solution 1=", get_solution_1())
    print("Solution 2=", get_solution_2())
