#! /usr/bin/env python3
from enum import Enum
from queue import Queue


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99


class ParamMode(Enum):
    POSITION = 0  # param value is address to final value
    IMMEDIATE = 1  # param value is final value
    RELATIVE = 2  # param value is address relative to base address


class IntcodeComputer:
    def __init__(self, init_address, num_of_values_for_input_instructions):
        self._predefined_values_for_input_instruction = Queue(num_of_values_for_input_instructions)
        self._inputs = {}
        self._outputs = []
        self._current_address = init_address
        self._is_halted = False
        self._is_waiting = False
        self._relative_base = 0

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def outputs(self):
        return self._outputs

    @property
    def current_address(self):
        return self._current_address

    @property
    def predefined_values_for_input_instruction(self):
        return self._predefined_values_for_input_instruction

    @property
    def is_halted(self):
        return self._is_halted

    @property
    def is_waiting(self):
        return self._is_waiting

    def get_input(self, address):
        return self.inputs[address] if address in self.inputs else 0

    def perform_input(self):
        if self.predefined_values_for_input_instruction.empty():
            self._is_waiting = True
            return

        raw_input_value = self.predefined_values_for_input_instruction.get(block=False)
        input_1_address = self.get_input(self.current_address + 1)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            target_address = input_1_address
        elif self.get_param_modes()[0] == ParamMode.RELATIVE.value:
            target_address = input_1_address + self._relative_base
        else:
            print("Unsupported mode for INPUT, ", self.get_param_modes()[0])

        self.inputs[target_address] = raw_input_value

        self._current_address += 2

    def perform_output(self):
        input_1_address = self.get_input(self.current_address + 1)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        self.outputs.append(input_1)

        self._current_address += 2

    def perform_add(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)
        output_address = self.get_input(self.current_address + 3)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if self.get_param_modes()[2] == ParamMode.POSITION.value:
            target_address = output_address
        elif self.get_param_modes()[2] == ParamMode.RELATIVE.value:
            target_address = output_address + self._relative_base
        else:
            print("Unsupported mode, ", self.get_param_modes()[0])

        self.inputs[target_address] = input_1 + input_2

        self._current_address += 4

    def perform_multiply(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)
        output_address = self.get_input(self.current_address + 3)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if self.get_param_modes()[2] == ParamMode.POSITION.value:
            target_address = output_address
        elif self.get_param_modes()[2] == ParamMode.RELATIVE.value:
            target_address = output_address + self._relative_base
        else:
            print("Unsupported mode, ", self.get_param_modes()[0])

        self.inputs[target_address] = input_1 * input_2

        self._current_address += 4

    def perform_jump_if_true(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if input_1 != 0:
            self._current_address = input_2
        else:
            self._current_address += 3

    def perform_jump_if_false(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if input_1 == 0:
            self._current_address = input_2
        else:
            self._current_address += 3

    def perform_less_than(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)
        output_address = self.get_input(self.current_address + 3)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if self.get_param_modes()[2] == ParamMode.POSITION.value:
            target_address = output_address
        elif self.get_param_modes()[2] == ParamMode.RELATIVE.value:
            target_address = output_address + self._relative_base
        else:
            print("Unsupported mode, ", self.get_param_modes()[0])

        if input_1 < input_2:
            self.inputs[target_address] = 1
        else:
            self.inputs[target_address] = 0

        self._current_address += 4

    def perform_equals(self):
        input_1_address = self.get_input(self.current_address + 1)
        input_2_address = self.get_input(self.current_address + 2)
        output_address = self.get_input(self.current_address + 3)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        if self.get_param_modes()[1] == ParamMode.POSITION.value:
            input_2 = self.get_input(input_2_address)
        elif self.get_param_modes()[1] == ParamMode.IMMEDIATE.value:
            input_2 = input_2_address
        else:
            input_2 = self.get_input(self._relative_base + input_2_address)

        if self.get_param_modes()[2] == ParamMode.POSITION.value:
            target_address = output_address
        elif self.get_param_modes()[2] == ParamMode.RELATIVE.value:
            target_address = output_address + self._relative_base
        else:
            print("Unsupported mode, ", self.get_param_modes()[0])

        if input_1 == input_2:
            self.inputs[target_address] = 1
        else:
            self.inputs[target_address] = 0

        self._current_address += 4

    def perform_adjust_relative_base(self):
        input_1_address = self.get_input(self.current_address + 1)

        if self.get_param_modes()[0] == ParamMode.POSITION.value:
            input_1 = self.get_input(input_1_address)
        elif self.get_param_modes()[0] == ParamMode.IMMEDIATE.value:
            input_1 = input_1_address
        else:
            input_1 = self.get_input(self._relative_base + input_1_address)

        self._relative_base += input_1

        self._current_address += 2

    def perform_halt(self):
        self._is_halted = True
        self._current_address += 1

    def get_op_and_actions(self):
        return {
            Opcode.HALT.value: self.perform_halt,
            Opcode.ADD.value: self.perform_add,
            Opcode.MULTIPLY.value: self.perform_multiply,
            Opcode.INPUT.value: self.perform_input,
            Opcode.OUTPUT.value: self.perform_output,
            Opcode.JUMP_IF_TRUE.value: self.perform_jump_if_true,
            Opcode.JUMP_IF_FALSE.value: self.perform_jump_if_false,
            Opcode.LESS_THAN.value: self.perform_less_than,
            Opcode.EQUALS.value: self.perform_equals,
            Opcode.ADJUST_RELATIVE_BASE.value: self.perform_adjust_relative_base
        }

    def perform_operation(self):
        opcode = self.get_input(self.current_address) % 100
        return self.get_op_and_actions()[opcode]()

    def get_param_modes(self):
        revered_modes = str(self.get_input(self.current_address) // 100)
        modes_in_correct_order = revered_modes[::-1]
        modes_with_zeros = "{:0<3}".format(modes_in_correct_order)

        return [int(mode) for mode in modes_with_zeros]

    def run_program(self):
        while not self.is_halted:
            self.perform_operation()
