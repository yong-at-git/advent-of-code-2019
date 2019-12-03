#! /usr/bin/env python3


def get_answer_for_question_1():
    input_paths = get_input_paths()
    return get_distance_of_closest_intersection(input_paths[0], input_paths[1])


def get_input_paths():
    with open("day_3.input") as inputs:
        path_1 = inputs.readline().split(",")
        path_2 = inputs.readline().split(",")

    return [path_1, path_2]


def get_distance_of_closest_intersection(path_1, path_2):
    coordinates_1 = to_coordinates(path_1)
    coordinates_2 = to_coordinates(path_2)

    return get_distance_of_closest_coordinate(get_intersection(coordinates_1, coordinates_2))


def to_coordinates(path):
    init_coordinate = (0, 0)
    path_of_coordinates = []

    for movement in path:
        current_coordinate = init_coordinate if len(path_of_coordinates) == 0 else path_of_coordinates[-1]
        movement_to_coordinates(current_coordinate, movement, path_of_coordinates)

    return path_of_coordinates


def movement_to_coordinates(current_coordinate, movement, path_of_coordinates):
    direction = movement[0]
    steps = int(movement[1:])

    horizontal_pos = current_coordinate[0]
    vertical_pos = current_coordinate[1]

    if direction == 'R':
        for step in range(steps):
            new_coordinate = (horizontal_pos + step + 1, vertical_pos)
            path_of_coordinates.append(new_coordinate)
    elif direction == 'U':
        for step in range(steps):
            new_coordinate = (horizontal_pos, vertical_pos + step + 1)
            path_of_coordinates.append(new_coordinate)
    elif direction == 'L':
        for step in range(steps):
            new_coordinate = (horizontal_pos - (step + 1), vertical_pos)
            path_of_coordinates.append(new_coordinate)
    elif direction == 'D':
        for step in range(steps):
            new_coordinate = (horizontal_pos, vertical_pos - (step + 1))
            path_of_coordinates.append(new_coordinate)
    else:
        print("Unknown direction in movement=" + movement)


def get_intersection(list_a, list_b):
    return set(list_a) & set(list_b)


def get_distance(coordinate):
    return abs(coordinate[0]) + abs(coordinate[1])


def get_distance_of_closest_coordinate(intersection_coordinates):
    return min(list(map(lambda coordinate: get_distance(coordinate), intersection_coordinates)))


if __name__ == "__main__":
    print(get_answer_for_question_1())
