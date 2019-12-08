#! /usr/bin/env python3
from textwrap import TextWrapper
from enum import Enum


class PixelColor(Enum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


class ImageLayer:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._rows = []

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def rows(self):
        return self._rows

    def parse_layer_from_digits_series(self, digits_series):
        textwrap = TextWrapper()
        textwrap.width = self.width
        for digits_in_each_row in textwrap.wrap(digits_series):
            self._rows.append(list(map(int, digits_in_each_row)))

    def get_elem_count(self, elem):
        total_count = 0
        for row in self.rows:
            total_count += row.count(elem)
        return total_count

    def display(self):
        for row in self.rows:
            raw_str = "".join(map(str, row))
            print(raw_str.replace("0", " "))

    def apply_layer(self, back_layer):
        for row_num in range(self.height):
            for col_num in range(self.width):
                my_current_pixel = self.rows[row_num][col_num]
                your_pixel = back_layer.rows[row_num][col_num]
                result_pixel = ImageLayer.get_pixel_value(my_current_pixel, your_pixel)
                self.rows[row_num][col_num] = result_pixel

    @staticmethod
    def get_pixel_value(front_layer_pixel_value, back_layer_pixel_value):
        if front_layer_pixel_value != PixelColor.TRANSPARENT.value:
            return front_layer_pixel_value
        else:
            return back_layer_pixel_value


class SpaceImage:
    def __init__(self, width, height):
        self._layers = []
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def layers(self):
        return self._layers

    def parse_layers_from_digits_series(self, digits_series):
        textwrap = TextWrapper()
        textwrap.width = self.height * self.width

        for digits_in_each_layer in textwrap.wrap(digits_series):
            layer = ImageLayer(self.width, self.height)
            layer.parse_layer_from_digits_series(digits_in_each_layer)
            self.layers.append(layer)

    def get_ordered_layers(self, elem):
        layers_copy = self.layers.copy()
        layers_copy.sort(key=lambda layer1: layer1.get_elem_count(elem))
        return layers_copy

    def get_final_image(self):
        final_layer = self.layers[0]
        for layer in self.layers:
            final_layer.apply_layer(layer)
        return final_layer


def get_input():
    with open("day_8.input") as inputs:
        return inputs.readline().rstrip()


def set_up_image():
    image_width = 25
    image_height = 6

    space_image = SpaceImage(image_width, image_height)
    space_image.parse_layers_from_digits_series(get_input())

    return space_image


def get_solution_1():
    space_image = set_up_image()
    order_layers_by_elem = 0
    target_layer = space_image.get_ordered_layers(order_layers_by_elem)[0]

    ones = target_layer.get_elem_count(1)
    twos = target_layer.get_elem_count(2)

    return ones * twos


def get_solution_2():
    space_image = set_up_image()
    space_image.get_final_image().display()


if __name__ == "__main__":
    print("Solution 1: ", get_solution_1())
    print("Solution 2: ")
    get_solution_2()
