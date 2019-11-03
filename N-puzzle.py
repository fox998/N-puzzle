#! /usr/bin/env python

# Windows - C:\Users\afokin\AppData\Local\Programs\Python\Python38-32\python.exe
# Mac - /usr/bin/env python

import argparse
from make_goal import (make_goal, make_puzzle)
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
        neighbor[zero_index], neighbor[zero_index + p.size] = neighbor[zero_index + p.size], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    # up
    if zero_pos_y > 0:
        neighbor = p.arr[:]
        neighbor[zero_index], neighbor[zero_index - p.size] = neighbor[zero_index - p.size], neighbor[zero_index]
        neighbors.append(Puzzle(neighbor))

    return neighbors


def get_arr_hash(arr: list)->int:
    arr_hash = 0
    arr_len = len(arr)
    for val in arr:
        arr_hash = arr_hash * arr_len + int(val)

    return arr_hash


def print_arr_from_hash(puzzle_hash: int, size: int):
    puzzle_arr = []
    step = size ** 2
    power = 1
    while power <= puzzle_hash or '0' not in puzzle_arr:
        new_power = power * step
        puzzle_arr.append(str(puzzle_hash % new_power // power))
        power = new_power

    puzzle_arr = puzzle_arr[::-1]

    for i in range(size):
        print(*puzzle_arr[i * size: (i + 1) * size])
    print('')


def get_path(best_scores : dict, from_hash: int, puzzle_size):
        current_state = from_hash
        states = []
        while current_state is not None:
            states.append(current_state)
            current_state = best_scores[current_state].parent

        # for state in states[::-1]:
        #     print_arr_from_hash(state, puzzle_size)
        return states[::-1]





class MetaData:
    def __init__(self):
        self.states_number = None
        self.max_number_of_states = None
        self.number_of_moves = None
        self.is_solvable = None


def a_star_algorithm(start: Puzzle, goal: Puzzle, heuristic_function):
    
    heuristic = heuristic_function(start, goal, 0)
    best_scores = dict({ get_arr_hash(start.arr): BestScore(0, None)})
    
    open_queue = PriorityQueue()
    open_queue.put((heuristic, start))

    max_number_of_states = 0
    while not open_queue.empty():
        value = open_queue.get()
        puzzle = value[1]

        parent_score = best_scores[ get_arr_hash(puzzle.arr)].distance
        parent_hash = get_arr_hash(puzzle.arr)

        if puzzle.arr == goal.arr:
            m = MetaData()
            m.states_number = len(best_scores)
            m.max_number_of_states = max_number_of_states
            m.number_of_moves = parent_score
            m.path = get_path(best_scores, get_arr_hash(goal.arr), goal.size)
            m.is_solvable = True
            return m

        for neighbor in get_neighbors(puzzle):
            neighbor_distance = parent_score + 1

            neighbor_hash = get_arr_hash(neighbor.arr)
            if neighbor_hash not in best_scores.keys():
                best_scores[neighbor_hash] = BestScore(neighbor_distance, parent_hash)
                neighbor_score = heuristic_function(neighbor, goal, neighbor_distance)
                open_queue.put((neighbor_score, neighbor))
                max_number_of_states = max(max_number_of_states, len(best_scores) + open_queue.qsize())
            elif neighbor_distance < best_scores[neighbor_hash].distance:
                best_scores[neighbor_hash] = BestScore(neighbor_distance, parent_hash)

    m = MetaData()
    m.states_number = len(best_scores)
    m.max_number_of_states = max_number_of_states
    m.number_of_moves = parent_score
    m.path = get_path(best_scores, get_arr_hash(goal.arr), goal.size)
    m.is_solvable = False
    return m


class SearchMetadata:
    def __init__(self, best_scores : dict, max_number_of_states : int, goal : Puzzle):

        self.checked_states = len(best_scores)
        self.max_number_of_states = max_number_of_states
        
        self.path = []
        current_state = get_arr_hash(goal.arr)
        while current_state is not None:
            self.path.append(current_state)
            current_state = best_scores[current_state].parent


def heuristic_match(current: Puzzle, goal: Puzzle, distance_from_start : int)->int:
    matches_number = 0
    for first, second  in zip(current.arr, goal.arr):
        if first == second:
            matches_number += 1

    return (goal.size**2 - matches_number)


def heuristic_square(current: Puzzle, goal: Puzzle, distance_from_start : int)->int:
    score = 0
    for val  in current.arr:
        first_pos = current.get_value_pos(val)
        second_pos = goal.get_value_pos(val)
        distance_to_goal = (first_pos[0] - second_pos[0])**2 + (first_pos[1] - second_pos[1])**2
        score += distance_to_goal

    return score


def heuristic_pow(current: Puzzle, goal: Puzzle, distance_fromstart : int):
    march_score = heuristic_match(current, goal, distance_fromstart)
    square_score = heuristic_square(current, goal, distance_fromstart)
    return (march_score ** square_score + distance_fromstart) if square_score > 0 else 0



def get_puzzle(args)-> Puzzle:
    if args.file != 'r':
        print(f'from: {args.file}')
        return get_puzzle_from_file(args.file)
    else :
        print(f'create random puzzle')
        return Puzzle(make_puzzle(args.size, not args.unsolvable, 1000))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help="File with puzzle or 'r' for rundoming the puzzle")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle. By default puzzle is solvable")
    parser.add_argument("-s", "--size", type=int, default=3, help="Size of randomed puzzle. 3 by default")
    parser.add_argument("-t", "--tests", action="store_true", default=False, help="Run the tests")
    parser.add_argument("--heuristic", type=int, default=0, help="choce heuristic function 0 - 2")

    args = parser.parse_args()

    p = get_puzzle(args)
    

    heuristic_functions = [heuristic_pow, heuristic_match, heuristic_square]
    heuristic = heuristic_functions[args.heuristic]

    print('Starting puzzle:')
    print_puzzle(p)

    goal = Puzzle(make_goal(p.size))
    print(f'Goal:')
    print_puzzle(goal)

    print(f'\n{heuristic.__name__}')
    meta_data = a_star_algorithm(p, goal, heuristic)
    print(res)

    # print('\nheuristic_match')
    # res = a_star_algorithm(p, goal, heuristic)
    # print(res)

    # print('\nheuristic_square')
    # res = a_star_algorithm(p, goal, heuristic)
    # print(res)


