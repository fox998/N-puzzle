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

    def __lt__(self, other):
        return self.arr < other.arr

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
        puzzle_row = [int(number) for number in line.split(' ') if len(number) > 0]
        assert len(puzzle_row) == puzzle_size, f'Wrong number of values in a row: {puzzle_row}, row size must be {puzzle_size}'
        puzzle_arr += puzzle_row

    return Puzzle(puzzle_arr)


class BestScore:
    def __init__(self, distance: int, parent: Puzzle):
        self.distance = distance
        self.parent = parent


#TODO: implement get_neighbors
def get_neighbors(p: Puzzle)-> list:
    neighbors = []
    zero_index = p.arr.index(0)
    zero_pos_x = zero_index % p.size
    zero_pos_y = zero_index // p.size

    # right
    if zero_pos_x < p.size - 1:
        neighbor = p.arr[:]
        neighbor[zero_index], neighbor[zero_index + 1] = neighbor[zero_index + 1], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    # left
    if zero_pos_x > 0:
        neighbor = p.arr[:]
        neighbor[zero_index], neighbor[zero_index - 1] = neighbor[zero_index - 1], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    # down
    if zero_pos_y < p.size - 1:
        neighbor = p.arr[:]
        neighbor[zero_index], neighbor[zero_index + p.size - 1] = neighbor[zero_index + p.size - 1], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    # up
    if zero_pos_y > 0:
        neighbor = p.arr[:]
        neighbor[zero_index], neighbor[zero_index - p.size - 1] = neighbor[zero_index - p.size - 1], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    return neighbors


def get_arr_hash(arr: list)->int:
    arr_hash = 0
    arr_len = len(arr)
    for val in arr:
        arr_hash = arr_hash * arr_len + int(val)

    return arr_hash


def a_star_algorithm(start: Puzzle, goal: Puzzle, heuristic_function):
    
    heuristic = heuristic_function(start, goal)
    best_scores = dict({ get_arr_hash(start.arr): BestScore(0, None)})
    
    open_queue = PriorityQueue()
    open_queue.put((heuristic, start))

    while not open_queue.empty():
        value = open_queue.get()
        puzzle = value[1]

        if puzzle.arr == goal.arr:
            print(f'states number: {len(best_scores)}')
            print(f'puzzle')
            print_puzzle(puzzle)
            return True

        parent_score = best_scores[ get_arr_hash(puzzle.arr)].distance
        for neighbor in get_neighbors(puzzle):
            neighbor_distance = parent_score + 1

            neighbor_hash = get_arr_hash(neighbor.arr)
            if neighbor_hash not in best_scores.keys():
                best_scores[neighbor_hash] = BestScore(neighbor_distance, puzzle)
                neighbor_score = heuristic_function(neighbor, goal)
                open_queue.put((neighbor_score, neighbor))
            elif neighbor_distance < best_scores[neighbor_hash].distance:
                best_scores[neighbor_hash] = BestScore(neighbor_distance, puzzle)

    return False


def heuristic_match(current: Puzzle, goal: Puzzle)->int:
    matches_number = 0
    for first, second  in zip(current.arr, goal.arr):
        if first == second:
            matches_number += 1

    return goal.size**2 - matches_number


def heuristic_square(current: Puzzle, goal: Puzzle)->int:
    score = 0
    for val  in current.arr:
        first_pos = current.get_value_pos(val)
        second_pos = goal.get_value_pos(val)
        distance_to_goal = (first_pos[0] - second_pos[0])**2 + (first_pos[1] - second_pos[1])**2
        score += distance_to_goal

    return score


def heuristic_pow(current: Puzzle, goal: Puzzle):
    return heuristic_match(current, goal) ** heuristic_square(current, goal)


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()

    # parser.add_argument("file", type=str, help="File with puzzle or 'r' for rundoming the puzzle")
    # parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle. By default puzzle is solvable")
    # parser.add_argument("--size", type=int, default=3, help="Size of randomed puzzle. 3 by default")
    # parser.add_argument("-t", "--tests", action="store_true", default=False, help="Run the tests")

    # args = parser.parse_args()

    # print(f'file: {args.file}')
    p = get_puzzle_from_file('test_puzzle')
    print(p.arr)
    print_puzzle(p)

    print('\nheuristic_square')
    res = a_star_algorithm(p, Puzzle(make_goal(p.size)), heuristic_pow)
    print(res)

    print('\nheuristic_match')
    res = a_star_algorithm(p, Puzzle(make_goal(p.size)), heuristic_match)
    print(res)

    print('\nheuristic_square')
    res = a_star_algorithm(p, Puzzle(make_goal(p.size)), heuristic_square)
    print(res)


