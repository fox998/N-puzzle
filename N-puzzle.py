#! C:\Users\afokin\AppData\Local\Programs\Python\Python38-32\python.exe

# Windows - C:\Users\afokin\AppData\Local\Programs\Python\Python38-32\python.exe
# Mac - /usr/bin/env python

import argparse
from make_goal import make_goal
from queue import PriorityQueue


class Puzzle:
    def __init__(self, arr: list):
        arr_len = len(arr)
        self.size = int(arr_len**0.5)
        self.arr = arr
        assert self.size**2 == arr_len

    def get_value(self, x: int, y: int) -> int:
        return self.arr[x + y * self.size]

    def set_value(self, x: int, y:int, value: int) -> None:
        self.arr[x + y * self.size] = value

    def get_value_pos(self, value: int) -> list:
        assert value < len(self.arr)
        index = self.arr.index(value)

        return [index % self.size, index // self.size]


def print_puzzle(puzzle: Puzzle):
    for i in range(puzzle.size):
        start_pos = i * puzzle.size
        end_pos = start_pos + puzzle.size
        # print one row
        print(*puzzle.arr[start_pos: end_pos])


def format_line(line):
    line = line[:line.find('#')]
    return line

def get_formated_lines(lines_arr):
    return [format_line(line) for line in lines_arr]


def get_puzzle_data_lines_from_file(file: str) -> str:
    f = open(file,"r+")
    
    lines = [line for line in get_formated_lines(f.readlines()) if len(line) > 0]
    lines_len = len(lines)

    assert lines_len > 1 or int(lines[0]) + 1 != lines_len , "Wrong number of lines"
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
        assert len(puzzle_row) == puzzle_size, f'Wrong number of values in a row: {puzzle_row}, row size must be {puzzle_size}'
        puzzle_arr += puzzle_row

    return Puzzle(puzzle_arr)


class BestScore:
    def __init__(self, heuristic: int, parent: Puzzle):
        self.heuristic = heuristic
        self.parent = parent


#TODO: implement get_neighbors
def get_neighbors(p: Puzzle)-> list:
    return []


def a_star_algorithm(start: Puzzle, goal: Puzzle, heuristic_function):
    
    heuristic = heuristic_function(start)
    best_scores = dict({start: BestScore(heuristic, None)})
    
    open_queue = PriorityQueue()
    open_queue.put((heuristic, start))
    
    while not open_queue.empty():
        value = open_queue.get()
        score = value[0]
        puzzle = value[1]
        
        if puzzle == goal:
            return True

        for neighbor in get_neighbors(puzzle):
            neighbor_score = heuristic_function(neighbor) + score + 1
            if neighbor not in best_scores.keys():
                best_scores[neighbor] = BestScore(neighbor_score, puzzle)
                open_queue.put((neighbor_score, neighbor))
            elif neighbor_score < best_scores[neighbor].heuristic:
                best_scores[neighbor] = BestScore(neighbor_score, puzzle)

    return False


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help="File with puzzle or 'r' for rundoming the puzzle")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle. By default puzzle is solvable")
    parser.add_argument("--size", type=int, default=3, help="Size of randomed puzzle. 3 by default")
    parser.add_argument("-t", "--tests", action="store_true", default=False, help="Run the tests")

    args = parser.parse_args()

    print(f'file: {args.file}')
    p = get_puzzle_from_file(args.file)
    print(p.arr)
    print_puzzle(p)

