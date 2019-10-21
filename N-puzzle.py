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



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help="file with puzzle")
    parser.add_argument("-s", "--solvable", action="store_true", default=False, help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")

    args = parser.parse_args()

    print(f'file: {args.file}')

