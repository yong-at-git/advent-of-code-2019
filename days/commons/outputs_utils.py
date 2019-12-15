#! /usr/bin/env python3


def print_grid(grid, my_pos):
    x_values = []
    y_values = []
    for x, y in grid.keys():
        x_values.append(x)
        y_values.append(y)

    for y in reversed(range(min(y_values), max(y_values) + 1)):
        row_str = ""
        for x in range(min(x_values), max(x_values) + 1):
            if (x, y) == (0, 0):
                row_str += 'O'
            elif (x, y) == my_pos:
                row_str += 'I'
            elif (x, y) in grid:
                row_str += grid[(x, y)]
            else:
                row_str += ' '
        print(row_str)


if __name__ == "__main__":
    print()
