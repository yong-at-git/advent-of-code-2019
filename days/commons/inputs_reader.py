#! /usr/bin/env python3


def get_single_line_and_parse_to_int_list(filename):
    with open(filename) as inputs:
        return list(map(int, inputs.readline().split(",")))


def get_fist_line_as_raw_str(filename):
    with open(filename) as inputs:
        return inputs.readline()


def get_list_of_raw_lines(filename):
    with open(filename) as lines:
        return [line for line in lines]


def get_single_line_and_parse_to_dicts(filename):
    list_inputs = get_single_line_and_parse_to_int_list(filename)

    dicts = {}
    for address in range(len(list_inputs)):
        dicts[address] = list_inputs[address]
    return dicts


if __name__ == "__main__":
    print()
