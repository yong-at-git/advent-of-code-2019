#! /usr/bin/env python3


def get_solution_1():
    return len(get_valid_numbers_for_solution_1())


def get_valid_numbers_for_solution_1():
    (lower_bound, upper_bound) = get_lower_and_upper_bounds()
    return get_valid_numbers(lower_bound, upper_bound)


def get_solution_2():
    return len(list(filter(is_matching_extra_condition_in_solution_2, get_valid_numbers_for_solution_1())))


def is_matching_extra_condition_in_solution_2(num):
    c_to_count = {}

    for c in str(num):
        if c in c_to_count:
            c_to_count[c] += 1
        else:
            c_to_count[c] = 1

    return 2 in c_to_count.values()


def get_lower_and_upper_bounds():
    with open("day_4.input") as inputs:
        lower_bound = int(inputs.readline())
        upper_bound = int(inputs.readline())
    return lower_bound, upper_bound


def is_valid_number(number_str):
    if len(number_str) != 6:
        return False

    has_adjacent_same_digits = False

    for idx in range(len(number_str) - 1):
        if number_str[idx + 1] < number_str[idx]:
            return False
        if number_str[idx] == number_str[idx + 1]:
            has_adjacent_same_digits = True

    return has_adjacent_same_digits


def get_valid_numbers(lower_bound, upper_bound):
    valid_ones = []
    for number in range(lower_bound, upper_bound):
        if is_valid_number(str(number)):
            valid_ones.append(number)

    return valid_ones


if __name__ == "__main__":
    print("Solution 1 is:", get_solution_1())
    print("Solution 2 is:", get_solution_2())
