#! /usr/bin/env python3
from days.commons.intcode_computer import IntcodeComputer
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
import threading


class NonBlockingComputer(IntcodeComputer):
    def perform_input(self):
        if len(self.predefined_values_for_input_instruction) == 0:
            self.predefined_values_for_input_instruction.append(-1)
        super().perform_input()


class Day23:
    def __init__(self):
        self._computers = []

    @property
    def computers(self):
        return self._computers

    def get_inputs_dict(self):
        return get_single_line_and_parse_to_dicts("day_23.input")

    def get_solution_1(self):
        inputs_dict = self.get_inputs_dict()
        for i in range(0, 50):
            computer = IntcodeComputer()
            computer.inputs_dict = inputs_dict.copy()
            computer.predefined_values_for_input_instruction.append(i)
            self.computers.append(computer)

        for computer in self.computers:
            t = threading.Thread(target=self.run_computer, args=(computer,))
            t.start()

    def run_computer(self, me: IntcodeComputer):
        while not me.is_halted:
            me.perform_operation()

            if len(me.outputs) == 3:
                addr = me.outputs[0]
                x = me.outputs[1]
                y = me.outputs[2]
                del me.outputs[2]
                del me.outputs[1]
                del me.outputs[0]

                if addr == 255:
                    print("Address=", addr, ", x=", x, ", y=", y)

                if addr in range(0, 50):
                    self.computers[addr].predefined_values_for_input_instruction.append(x)
                    self.computers[addr].predefined_values_for_input_instruction.append(y)


if __name__ == "__main__":
    today = Day23()

    today.get_solution_1()
    print()
