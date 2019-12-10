#! /usr/bin/env python3
import functools
from math import gcd
import collections


class Day10:
    def __init__(self):
        self._map = {}
        self._depth = 0
        self._width = 0

    ASTEROID_MARK = '#'

    @property
    def map(self):
        return self._map

    @property
    def depth(self):
        return self._depth

    @property
    def width(self):
        return self._width

    def load_inputs(self):
        width_idx = 0
        depth_idx = 0

        with open("day_10.input") as lines:
            for line in lines:
                width_idx = 0
                for c in line.rstrip():
                    self.map[(width_idx, depth_idx)] = c
                    width_idx += 1
                depth_idx += 1

        self._width = width_idx + 1
        self._depth = depth_idx + 1

    def get_asteroid_positions(self):
        return dict(filter(lambda item: item[1] == Day10.ASTEROID_MARK, self.map.items())).keys()

    @staticmethod
    def get_angel(remote_position, local_position):
        x_diff = remote_position[0] - local_position[0]
        y_diff = remote_position[1] - local_position[1]

        gcd_of_diff = gcd(abs(x_diff), abs(y_diff))
        return x_diff // gcd_of_diff, y_diff // gcd_of_diff

    def get_angle_and_detected_asteroids_mappings(self, current_position):
        angle_and_detected_asteroids = {}

        for asteroid_position in self.get_asteroid_positions():
            if asteroid_position != current_position:
                angle = Day10.get_angel(asteroid_position, current_position)
                if angle not in angle_and_detected_asteroids:
                    angle_and_detected_asteroids[angle] = [asteroid_position]
                else:
                    angle_and_detected_asteroids[angle].append(asteroid_position)

        return angle_and_detected_asteroids

    def get_num_of_detected_asteroids(self, current_position):
        return len(self.get_angle_and_detected_asteroids_mappings(current_position).keys())

    def get_position_and_detectable_counts(self):
        position_to_counts = {}

        for position in self.get_asteroid_positions():
            position_to_counts[position] = self.get_num_of_detected_asteroids(position)

        return position_to_counts

    def get_position_with_max_detectable_count(self):
        position_to_counts = self.get_position_and_detectable_counts()
        best_position = max(position_to_counts, key=position_to_counts.get)
        return best_position, position_to_counts[best_position]

    def get_solution_1(self):
        return self.get_position_with_max_detectable_count()

    ############################### Solution 2
    @staticmethod
    def compare_angle(angle1, angle2):
        normalized_x_1 = angle1[0] * angle2[1]
        normalized_x_2 = angle2[0] * angle1[1]
        return normalized_x_1 - normalized_x_2

    def get_first_quarter_lists_ordered_by_angle(self, angle_and_detected_asteroids):
        unordered = {k: v for (k, v) in angle_and_detected_asteroids.items() if k[0] > 0 and k[1] < 0}
        unordered_angles = unordered.keys()
        ordered_angles = sorted(unordered_angles, key=functools.cmp_to_key(Day10.compare_angle), reverse=True)
        ordered_position_lists = []
        for angel in ordered_angles:
            ordered_position_lists.append(angle_and_detected_asteroids[angel])
        return ordered_position_lists

    def get_second_quarter_lists_ordered_by_angle(self, angle_and_detected_asteroids):
        unordered = {k: v for (k, v) in angle_and_detected_asteroids.items() if k[0] > 0 and k[1] > 0}
        unordered_angles = unordered.keys()
        ordered_angles = sorted(unordered_angles, key=functools.cmp_to_key(Day10.compare_angle), reverse=True)
        ordered_position_lists = []
        for angel in ordered_angles:
            ordered_position_lists.append(angle_and_detected_asteroids[angel])
        return ordered_position_lists

    def get_third_quarter_lists_ordered_by_angle(self, angle_and_detected_asteroids):
        unordered = {k: v for (k, v) in angle_and_detected_asteroids.items() if k[0] < 0 and k[1] > 0}
        unordered_angles = unordered.keys()
        ordered_angles = sorted(unordered_angles, key=functools.cmp_to_key(Day10.compare_angle), reverse=True)
        ordered_position_lists = []
        for angel in ordered_angles:
            ordered_position_lists.append(angle_and_detected_asteroids[angel])
        return ordered_position_lists

    def get_fourth_quarter_lists_ordered_by_angle(self, angle_and_detected_asteroids):
        unordered = {k: v for (k, v) in angle_and_detected_asteroids.items() if k[0] < 0 and k[1] < 0}
        unordered_angles = unordered.keys()
        ordered_angles = sorted(unordered_angles, key=functools.cmp_to_key(Day10.compare_angle), reverse=True)
        ordered_position_lists = []
        for angel in ordered_angles:
            ordered_position_lists.append(angle_and_detected_asteroids[angel])
        return ordered_position_lists

    def get_solution_2(self):
        angle_and_detected_asteroids = self.get_angle_and_detected_asteroids_mappings((20, 20))
        total_position_lists_ordered_clockwise = []

        clock_twelve_ones = []
        if (0, -1) in angle_and_detected_asteroids:
            clock_twelve_ones = angle_and_detected_asteroids[(0, -1)]
        total_position_lists_ordered_clockwise.append(clock_twelve_ones)

        first_quarter_ones_order = self.get_first_quarter_lists_ordered_by_angle(angle_and_detected_asteroids)
        for first_quarter_one in first_quarter_ones_order:
            total_position_lists_ordered_clockwise.append(first_quarter_one)

        clock_three_ones = []
        if (1, 0) in angle_and_detected_asteroids:
            clock_three_ones = angle_and_detected_asteroids[(1, 0)]
        total_position_lists_ordered_clockwise.append(clock_three_ones)

        second_quarter_ones_order = self.get_second_quarter_lists_ordered_by_angle(angle_and_detected_asteroids)
        for second_quarter_one in second_quarter_ones_order:
            total_position_lists_ordered_clockwise.append(second_quarter_one)

        clock_six_ones = []
        if (0, 1) in angle_and_detected_asteroids:
            clock_six_ones = angle_and_detected_asteroids[(0, 1)]
        total_position_lists_ordered_clockwise.append(clock_six_ones)

        third_quarter_ones_order = self.get_third_quarter_lists_ordered_by_angle(angle_and_detected_asteroids)
        for third_quarter_one in third_quarter_ones_order:
            total_position_lists_ordered_clockwise.append(third_quarter_one)

        clock_nine_ones = []
        if (-1, 0) in angle_and_detected_asteroids:
            clock_nine_ones = angle_and_detected_asteroids[(-1, 0)]
        total_position_lists_ordered_clockwise.append(clock_nine_ones)

        forth_quarter_ones_order = self.get_fourth_quarter_lists_ordered_by_angle(angle_and_detected_asteroids)
        for forth_quarter_one in forth_quarter_ones_order:
            total_position_lists_ordered_clockwise.append(forth_quarter_one)

        for position_list in total_position_lists_ordered_clockwise:
            print(position_list)

        counter = 1
        last_deleted = None
        for position_list in total_position_lists_ordered_clockwise:
            if len(position_list) != 0:
                print(position_list)
                last_deleted = position_list[-1]
                del position_list[-1]
                if counter == 200:
                    break
                counter += 1
        return last_deleted[0] * 100 + last_deleted[1]


if __name__ == "__main__":
    day_10 = Day10()
    day_10.load_inputs()
    print("Solution 1=", day_10.get_solution_1())
    print("Solution 2=", day_10.get_solution_2())
