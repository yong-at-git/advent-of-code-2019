#! /usr/bin/env python3


def print_grid(grid, my_pos=(0, 0)):
    x_values = []
    y_values = []
    for x, y in grid.keys():
        x_values.append(x)
        y_values.append(y)

    for y in range(min(y_values), max(y_values) + 1):
        row_str = ""
        for x in range(min(x_values), max(x_values) + 1):
            row_str += grid.get((x, y), ' ')
        print(row_str)


def print_int_grid(grid, my_pos=(0, 0)):
    x_values = []
    y_values = []
    for x, y in grid.keys():
        x_values.append(x)
        y_values.append(y)

    for y in range(min(y_values), max(y_values) + 1):
        row_str = ""
        for x in range(min(x_values), max(x_values) + 1):
            if (x, y) in grid:
                if grid[(x, y)] == 1:
                    row_str += '#'
                else:
                    row_str += '.'
            else:
                row_str += ' '
        print(row_str)


if __name__ == "__main__":
    print()
