import unittest
from days.day_12.day_12_solution import Moon, Position, Velocity, Day12


def get_test_data_1():
    return [
        Moon("Io", Position(-1, 0, 2), Velocity(0, 0, 0)),
        Moon("Europa", Position(2, -10, -7), Velocity(0, 0, 0)),
        Moon("Ganymede", Position(4, -8, 8), Velocity(0, 0, 0)),
        Moon("Callisto", Position(3, 5, -1), Velocity(0, 0, 0))
    ]


def get_test_data_2():
    return [
        Moon("Io", Position(-8, -10, 0), Velocity(0, 0, 0)),
        Moon("Europa", Position(5, 5, 10), Velocity(0, 0, 0)),
        Moon("Ganymede", Position(2, -7, 3), Velocity(0, 0, 0)),
        Moon("Callisto", Position(9, -8, -3), Velocity(0, 0, 0))
    ]


class MyTestCase(unittest.TestCase):
    def test_with_test_data_1(self):
        today = Day12()

        for moon in get_test_data_1():
            today.add_moon_and_update_neighbour_list(moon)

        today.move_with_steps(10)

        self.assertEqual(179, today.get_total_energy())

    def test_with_test_data_2(self):
        today = Day12()

        for moon in get_test_data_2():
            today.add_moon_and_update_neighbour_list(moon)

        today.move_with_steps(100)

        self.assertEqual(1940, today.get_total_energy())

    def test_solution_2_with_test_data_1(self):
        today = Day12()

        for moon in get_test_data_1():
            today.add_moon_and_update_neighbour_list(moon)

        step = today.get_solution_2()

        self.assertEqual(2772, step)

    def test_solution_2_with_test_data_2(self):
        today = Day12()

        for moon in get_test_data_2():
            today.add_moon_and_update_neighbour_list(moon)

        step = today.get_solution_2()

        self.assertEqual(4686774924, step)


if __name__ == '__main__':
    unittest.main()
