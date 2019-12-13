#! /usr/bin/env python3

class Type3D:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    def get_sum_of_abs_axes(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def add_each_axis(self, you):
        self.x += you.x
        self.y += you.y
        self.z += you.z

    def get_diff_on_each_axis(self, others):
        changes = Type3D(0, 0, 0)
        for you in others:
            if you.x > self.x:
                changes.x += 1
            elif you.x < self.x:
                changes.x -= 1

            if you.y > self.y:
                changes.y += 1
            elif you.y < self.y:
                changes.y -= 1

            if you.z > self.z:
                changes.z += 1
            elif you.z < self.z:
                changes.z -= 1
        return changes

    def equal(self, you):
        return self.x == you.x and self.y == you.y and self.z == you.z

    def clone(self):
        return Type3D(self.x, self.y, self.z)

    def brief(self):
        return str(self.x) + str(self.y) + str(self.z)


class Position(Type3D):
    pass


class Velocity(Type3D):
    pass


class Moon:
    def __init__(self, name, position, velocity):
        self._name = name
        self._position = position
        self._velocity = velocity
        self._neighbours = []

    def __repr__(self):
        return "<position=" + str(self.position) + ", velocity=" + str(self.velocity) + ">"

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def position_before_move(self):
        return self._position_before_move

    @property
    def velocity_before_move(self):
        return self._velocity_before_move

    def update_velocity(self):
        neighbours_positions = tuple(map(lambda neighbour: neighbour.position, self.neighbours))
        position_comparing_result = self.position.get_diff_on_each_axis(neighbours_positions)
        self.velocity.add_each_axis(position_comparing_result)

    def update_position(self):
        self.position.add_each_axis(self.velocity)

    def get_potential_energy(self):
        return self.position.get_sum_of_abs_axes()

    def get_kinetic_energy(self):
        return self.velocity.get_sum_of_abs_axes()

    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

    def equal(self, you):
        return self.position.equal(you.position) and self.velocity.equal(you.velocity)

    def brief(self):
        return self.position.brief() + self.velocity.brief()


class Node:
    def __init__(self, value):
        self._value = value
        self._kids = {}

    @property
    def value(self):
        return self._value

    @property
    def kids(self):
        return self._kids


class Tree:
    def __init__(self, root):
        self._root = root

    @property
    def root(self):
        return self._root


class Day12:
    DEBUG = False

    def __init__(self):
        self._moons = []

    @property
    def moons(self):
        return self._moons

    def add_moon_and_update_neighbour_list(self, moon):
        for neighbour in self.moons:
            neighbour.neighbours.append(moon)
            moon.neighbours.append(neighbour)

        self.moons.append(moon)

    def get_total_energy(self):
        return sum(list(map(lambda moon: moon.get_total_energy(), self.moons)))

    def move(self):
        for moon in self.moons:
            moon.update_velocity()
        for moon in self.moons:
            moon.update_position()

    def move_with_steps(self, steps):
        for step in range(steps):
            self.move()

    def briefs(self):
        return "".join(list(map(lambda moon: moon.brief(), self.moons)))

    def get_solution_1(self):
        self.move_with_steps(1000)
        return self.get_total_energy()

    def possible_insert(self, values, tree):
        added_new_node = False

        current_node = tree.root
        for value in values:
            # print(value)
            if value in current_node.kids:
                current_node = current_node.kids[value]
            else:
                node = Node(value)
                current_node.kids[value] = node
                current_node = node
                added_new_node = True
        # print("done*******")

        return not added_new_node

    def with_pure_dict(self, values, pure_dict):
        added_new_node = False

        current_node = pure_dict
        for value in values:
            # print(value)
            try:
                current_node = current_node[value]
            except KeyError:
                current_node[value] = {}
                current_node = current_node[value]
                added_new_node = True

        # print("done*******")

        return not added_new_node

    def get_solution_2(self):

        one = self.moons[0]
        two = self.moons[1]
        three = self.moons[2]
        four = self.moons[3]

        values = [one.position.x, one.position.y, one.position.z,
                  one.velocity.x, one.velocity.y, one.velocity.z,
                  two.position.x, two.position.y, two.position.z,
                  two.velocity.x, two.velocity.y, two.velocity.z,
                  three.position.x, three.position.y, three.position.z,
                  three.velocity.x, three.velocity.y, three.velocity.z,
                  four.position.x, four.position.y, four.position.z,
                  four.velocity.x, four.velocity.y, four.velocity.z]

        my_dict = {}
        self.with_pure_dict(values, my_dict)

        step = 1
        while 1:
            if step % 100000 == 0:
                print(step)
            self.move()

            one = self.moons[0]
            two = self.moons[1]
            three = self.moons[2]
            four = self.moons[3]

            values = [one.position.x, one.position.y, one.position.z,
                      one.velocity.x, one.velocity.y, one.velocity.z,
                      two.position.x, two.position.y, two.position.z,
                      two.velocity.x, two.velocity.y, two.velocity.z,
                      three.position.x, three.position.y, three.position.z,
                      three.velocity.x, three.velocity.y, three.velocity.z,
                      four.position.x, four.position.y, four.position.z,
                      four.velocity.x, four.velocity.y, four.velocity.z]

            found = self.with_pure_dict(values, my_dict)
            if found:
                return step

            step += 1

    def get_solution_22(self):
        my_dict = {}
        my_dict[self.briefs()] = 1

        step = 1
        while 1:
            if step % 100000 == 0:
                print(step)
            self.move()

            if self.briefs() in my_dict:
                print("found step", step)
            else:
                my_dict[self.briefs()] = 1

            step += 1

    def get_solution_23(self):
        one = self.moons[0]
        two = self.moons[1]
        three = self.moons[2]
        four = self.moons[3]

        my_dict = {}
        energy = self.get_total_energy()
        my_dict[energy] = {
            one.get_total_energy(): {
                one.get_potential_energy(): one.position.brief(),
                one.get_kinetic_energy(): one.velocity.brief()
            },
            two.get_total_energy(): {
                two.get_potential_energy(): two.position.brief(),
                two.get_kinetic_energy(): two.velocity.brief()
            },
            three.get_total_energy(): {
                three.get_potential_energy(): three.position.brief(),
                three.get_kinetic_energy(): three.velocity.brief()
            },
            four.get_total_energy(): {
                four.get_potential_energy(): four.position.brief(),
                four.get_kinetic_energy(): four.velocity.brief()
            },
        }

        step = 1
        while 1:
            if step % 100000 == 0:
                print(step)
            self.move()

            energy = self.get_total_energy()
            if energy in my_dict:
                for moon in self.moons:
                    moon_energy = moon.get_total_energy()
                    if moon_energy in my_dict[energy]:
                        kinetic_energy = moon.get_kinetic_energy()
                        potential_energy = moon.get_potential_energy()
                        if kinetic_energy in my_dict[energy][moon_energy]:
                            if moon.velocity.brief() == my_dict[energy][moon_energy][kinetic_energy]:
                                print("Found=", step)
                                return step
                        else:
                            my_dict[energy][moon_energy] = {
                                potential_energy: four.position.brief(),
                                kinetic_energy: four.velocity.brief()
                            }
                    else:
                        my_dict[energy][moon_energy] = {
                            moon.get_potential_energy(): moon.position.brief(),
                            moon.get_kinetic_energy(): moon.velocity.brief()
                        }
            else:
                my_dict[energy] = {
                    one.get_total_energy(): {
                        one.get_potential_energy(): one.position.brief(),
                        one.get_kinetic_energy(): one.velocity.brief()
                    },
                    two.get_total_energy(): {
                        two.get_potential_energy(): two.position.brief(),
                        two.get_kinetic_energy(): two.velocity.brief()
                    },
                    three.get_total_energy(): {
                        three.get_potential_energy(): three.position.brief(),
                        three.get_kinetic_energy(): three.velocity.brief()
                    },
                    four.get_total_energy(): {
                        four.get_potential_energy(): four.position.brief(),
                        four.get_kinetic_energy(): four.velocity.brief()
                    },
                }

            step += 1


def get_init_moons():
    return [
        Moon("Io", Position(0, 6, 1), Velocity(0, 0, 0)),
        Moon("Europa", Position(4, 4, 19), Velocity(0, 0, 0)),
        Moon("Ganymede", Position(-11, 1, 8), Velocity(0, 0, 0)),
        Moon("Callisto", Position(2, 19, 15), Velocity(0, 0, 0))
    ]


if __name__ == "__main__":
    today = Day12()
    for moon in get_init_moons():
        today.add_moon_and_update_neighbour_list(moon)

    print("Solution 1=", today.get_solution_1())

    today = Day12()
    for moon in get_init_moons():
        today.add_moon_and_update_neighbour_list(moon)
    print("Solution 2=", today.get_solution_23())
