import unittest
from days.day_16.day_16_solution import Day16


class MyTestCase(unittest.TestCase):
    def test_case_1(self):
        today = Day16()
        init_list = today.get_digits_list_from_num(12345678)

        self.assertEqual('48226158', today.get_output_as_str(init_list, 1))
        self.assertEqual('34040438', today.get_output_as_str(init_list, 2))
        self.assertEqual('03415518', today.get_output_as_str(init_list, 3))
        self.assertEqual('01029498', today.get_output_as_str(init_list, 4))

    def test_case_2(self):
        today = Day16()
        init_list = today.get_digits_list_from_num(80871224585914546619083218645595)

        self.assertEqual('24176176', today.get_output_as_str(init_list, 100)[0:8])

    def test_case_3(self):
        today = Day16()
        init_list = today.get_digits_list_from_num(19617804207202209144916044189917)

        self.assertEqual('73745418', today.get_output_as_str(init_list, 100)[0:8])

    def test_case_4(self):
        today = Day16()
        init_list = today.get_digits_list_from_num(69317163492948606335995924319873)

        self.assertEqual('52432133', today.get_output_as_str(init_list, 100)[0:8])

    def test_solution_1(self):
        today = Day16()
        self.assertEqual('34841690', today.get_solution_1())


if __name__ == '__main__':
    unittest.main()
