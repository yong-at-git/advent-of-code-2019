#! /usr/bin/env python3


class OrbitObject:
    def __init__(self, label):
        self.label = label
        self.orbiting_to = None

    def set_orbiting_to(self, orbiting_to):
        self.orbiting_to = orbiting_to

    def get_orbiting_to(self):
        return self.orbiting_to

    def get_label(self):
        return self.label


def parse_orbit(orbit):
    orbited_obj_label = orbit.split(")")[0]
    orbiting_obj_label = orbit.split(")")[1].rstrip()

    return orbited_obj_label, orbiting_obj_label


def add_orbit(orbit, orbits_map):
    orbited_obj_label, orbiting_obj_label = parse_orbit(orbit)

    orbited_obj = orbits_map[orbited_obj_label] if orbited_obj_label in orbits_map else OrbitObject(orbited_obj_label)
    orbits_map[orbited_obj_label] = orbited_obj

    orbiting_obj = orbits_map[orbiting_obj_label] if orbiting_obj_label in orbits_map else OrbitObject(
        orbiting_obj_label)
    orbits_map[orbiting_obj_label] = orbiting_obj

    orbiting_obj.set_orbiting_to(orbited_obj)


def get_total_orbits_count(orbits_map):
    total_count = 0
    for orbit_obj in orbits_map.values():
        total_count += get_orbits_count(orbit_obj)
    return total_count


def get_orbits_count(orbit_obj):
    total_count = 0
    checking_obj = orbit_obj
    while checking_obj.get_orbiting_to() is not None:
        total_count += 1
        checking_obj = checking_obj.get_orbiting_to()
    return total_count


def get_orbits_map_from_inputs(inputs):
    orbits_map = {}
    for orbit_str in inputs:
        add_orbit(orbit_str, orbits_map)
    return orbits_map


def get_solution_1_from_inputs(inputs):
    return get_total_orbits_count(get_orbits_map_from_inputs(inputs))


def get_solution_1():
    with open("day_6.input") as orbits:
        return get_solution_1_from_inputs(orbits)


################# solution 2
def get_path_labels_to_center_of_mass(starting_orbit_obj):
    path_labels = []
    checking_obj = starting_orbit_obj

    while checking_obj.get_orbiting_to() is not None:
        path_labels.append(checking_obj.get_orbiting_to().get_label())
        checking_obj = checking_obj.get_orbiting_to()
    return path_labels


def get_first_common_label(labels_a, labels_b):
    for label in labels_a:
        if label in labels_b:
            return label
    return None


def get_first_common_orbit_obj(orbit_obj_a, orbit_obj_b, orbits_map):
    path_labels_a = get_path_labels_to_center_of_mass(orbit_obj_a)
    path_labels_b = get_path_labels_to_center_of_mass(orbit_obj_b)
    first_common_label = get_first_common_label(path_labels_a, path_labels_b)
    return orbits_map[first_common_label]


def get_minimum_orbit_transfer(orbit_obj_a, orbit_obj_b, orbits_map):
    first_common_orbit_obj = get_first_common_orbit_obj(orbit_obj_a, orbit_obj_b, orbits_map)

    orbits_count_from_a_to_cos = get_orbits_count(orbit_obj_a)
    orbits_count_from_b_to_cos = get_orbits_count(orbit_obj_b)
    orbits_count_from_first_common_obj_to_cos = get_orbits_count(first_common_orbit_obj)

    return (orbits_count_from_a_to_cos - orbits_count_from_first_common_obj_to_cos) + (
            orbits_count_from_b_to_cos - orbits_count_from_first_common_obj_to_cos)


def get_solution_2_with_labels(label_a, label_b, inputs):
    orbits_map = get_orbits_map_from_inputs(inputs)
    starting_obj = orbits_map[label_a].get_orbiting_to()
    ending_obj = orbits_map[label_b].get_orbiting_to()

    return get_minimum_orbit_transfer(starting_obj, ending_obj, orbits_map)


def get_solution_2():
    with open("day_6.input") as orbits:
        return get_solution_2_with_labels("YOU", "SAN", orbits)


if __name__ == "__main__":
    print("Solution 1: ", get_solution_1())
    print("Solution 2: ", get_solution_2())
