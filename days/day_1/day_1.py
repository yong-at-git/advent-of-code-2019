#! /usr/bin/env python3


def get_base_fuel_for_mass(mass):
    return mass // 3 - 2


def get_complete_fuel_for_fuel(fuel_mass):
    additional_fuels = []

    while fuel_mass > 0:
        additional_fuel = get_base_fuel_for_mass(fuel_mass)
        if additional_fuel > 0:
            additional_fuels.append(additional_fuel)

        fuel_mass = additional_fuel

    return sum(additional_fuels)


def get_complete_fuel_for_mass(mass):
    base_fuel = get_base_fuel_for_mass(mass)
    complete_fuel_for_fuel = get_complete_fuel_for_fuel(base_fuel)

    return base_fuel + complete_fuel_for_fuel


def get_sum_of_fuel_for_all_modules():
    fuel_masses = []

    with open("masses_of_modules") as masses_of_modules:
        for module_mass in masses_of_modules:
            fuel_masses.append(get_complete_fuel_for_mass(int(module_mass)))

    return sum(fuel_masses)


if __name__ == "__main__":
    print(get_sum_of_fuel_for_all_modules())
