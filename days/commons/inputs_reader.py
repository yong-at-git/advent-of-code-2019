#! /usr/bin/env python3


def get_single_line_and_parse_to_int_list(filename):
    with open(filename) as inputs:
        return list(map(int, inputs.readline().split(",")))


def get_single_line_and_parse_to_dicts(filename):
    list_inputs = get_single_line_and_parse_to_int_list(filename)

    dicts = {}
    for address in range(len(list_inputs)):
        dicts[address] = list_inputs[address]
    return dicts


if __name__ == "__main__":
    print()
