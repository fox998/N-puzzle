#! C:\Users\afokin\AppData\Local\Programs\Python\Python38-32\python.exe

# Windows - C:\Users\afokin\AppData\Local\Programs\Python\Python38-32\python.exe
# Mac - /usr/bin/env python

import argparse
from make_goal import make_goal


class Puzzle:
    def __init__(self, arr: list):
        arr_len = len(arr)
        self.size = int(arr_len**0.5)
        self.arr = arr
        assert(self.size**2 == arr_len)

    def get_value(self, x: int, y: int) -> int:
        return self.arr[x + y * self.size]

    def set_value(self, x: int, y:int, value: int) -> None:
        self.arr[x + y * self.size] = value

    def get_value_pos(self, value: int) -> list:
        assert(value < len(self.arr))
        index = self.arr.index(value)

        return [index % self.size, index // self.size]


def format_line(line):
    line = line[:line.find('#')]
    return line

def get_formated_lines(lines_arr):
    return [format_line(line) for line in lines_arr]


def get_puzzle_data_lines_from_file(file: str) -> str:
    f = open(file,"r+")
    
    lines = [line for line in get_formated_lines(f.readlines()) if len(line) > 0]
    lines_len = len(lines)

    assert(lines_len > 1 or int(lines[0]) + 1 != lines_len , "Wrong number of lines")
    # Puzzle format
    # 3
    # 6 8 0
    # 2 7 4
    # 3 1 5

    return lines



def get_puzzle_from_file(file: str)-> Puzzle:

    puzzle_lines = get_puzzle_data_lines_from_file(file)
    puzzle_size = int(puzzle_lines[0])

    puzzle_arr = []
    for line in puzzle_lines[1:]:
        puzzle_row = [int(number) for number in line.split(' ')]
        assert(len(puzzle_row) != puzzle_size, f'Wrong number of values in a row: {puzzle_row}')
        puzzle_arr.append(*puzzle_row)

    return Puzzle(puzzle_arr)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help="file with puzzle")
    parser.add_argument("-s", "--solvable", action="store_true", default=False, help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")

    args = parser.parse_args()

    print(f'file: {args.file}')
    print (get_puzzle_from_file(args.file))

