#! /usr/bin/env python3
import time

from days.commons.data_types import Type2D
from days.commons.intcode_computer import IntcodeComputer
from days.commons.inputs_reader import get_single_line_and_parse_to_dicts
import threading


class NonBlockingComputer(IntcodeComputer):
    def __init__(self, start_address=0):
        super().__init__(start_address)
        self._is_idle = False
        self._empty_pull_count = 0

    @property
    def is_idle(self):
        return self._is_idle

    @is_idle.setter
    def is_idle(self, value):
        self._is_idle = value

    @property
    def has_pulled_from_empty_queue_without_sending(self):
        return self._has_pulled_from_empty_queue_without_sending

    def perform_input(self):
        if len(self.predefined_values_for_input_instruction) == 0:
            if self._empty_pull_count == 2:
                self._is_idle = True
            self.predefined_values_for_input_instruction.append(-1)
            self._empty_pull_count += 1
        super().perform_input()

    def perform_output(self):
        self._empty_pull_count = 0
        self._is_idle = False
        super().perform_output()


screen_lock = threading.Semaphore(value=1)


class Day23:
    def __init__(self):
        self._computers = []
        self._nat_value = Type2D(0, 0)
        self._pushed_idel_ys = []

    @property
    def computers(self):
        return self._computers

    @property
    def nat_value(self):
        return self._nat_value

    def get_inputs_dict(self):
        return get_single_line_and_parse_to_dicts("day_23.input")

    def get_solution_2(self):
        self.get_solution_1()
        t = threading.Thread(target=self.idle_handling)
        t.start()

    def get_solution_1(self):
        inputs_dict = self.get_inputs_dict()
        for i in range(0, 50):
            computer = NonBlockingComputer()
            computer.inputs_dict = inputs_dict.copy()
            computer.predefined_values_for_input_instruction.append(i)
            self.computers.append(computer)

        for computer in self.computers:
            t = threading.Thread(target=self.run_computer, args=(computer,))
            t.start()

    def run_computer(self, me: NonBlockingComputer):
        while not me.is_halted:
            me.perform_operation()

            if len(me.outputs) == 3:
                addr = me.outputs[0]
                x = me.outputs[1]
                y = me.outputs[2]

                del me.outputs[0]
                del me.outputs[0]
                del me.outputs[0]

                if addr == 255:
                    screen_lock.acquire()
                    print("Updating nat x=", x, ", y=", y)
                    screen_lock.release()
                    self.nat_value.x = x
                    self.nat_value.y = y

                if addr in range(0, 50):
                    self.computers[addr].predefined_values_for_input_instruction.append(x)
                    self.computers[addr].predefined_values_for_input_instruction.append(y)

    def idle_handling(self):
        while True:
            is_idle = True

            for i in range(3):
                for computer in self.computers:
                    is_idle = is_idle and computer.is_idle

            if is_idle:
                x = self.nat_value.x
                y = self.nat_value.y
                screen_lock.acquire()
                print("Network idle. Send to zero with x=", x, ", y=", y)
                screen_lock.release()
                self.computers[0].predefined_values_for_input_instruction.append(x)
                self.computers[0].predefined_values_for_input_instruction.append(y)
                time.sleep(2)
                if len(self._pushed_idel_ys) == 2:
                    if self._pushed_idel_ys[1] == y:
                        print("Found y=", y)
                    del self._pushed_idel_ys[0]
                    self._pushed_idel_ys.append(y)

                else:
                    self._pushed_idel_ys.append(y)

            time.sleep(1)


if __name__ == "__main__":
    today = Day23()

    # today.get_solution_1()
    today.get_solution_2()
    print()
