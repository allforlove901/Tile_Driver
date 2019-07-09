# Name:         Brett Nelson
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Tile Driver Part 1
# Term:         Winter 2019

import queue
import math
import random

# function to determine if puzzle is solvable given a state
def is_solvable(tiles):
    # get values needed to set up conditionals
    width = len(tiles)
    blank_pos = tiles.index(0)
    dim = int(math.sqrt(len(tiles)))
    tiles_arr = []
    for i in range(len(tiles)):
        if tiles[i] != 0:
            tiles_arr.append(tiles[i])

    num_inversions = count_inversions(tiles_arr, 0)

    if (width % 2 != 0):
        return (num_inversions % 2 == 0)
    else:
        if ((blank_pos // dim) % 2 == 0):
            return (num_inversions % 2 == 0)
        else:
            return (num_inversions % 2 > 0)


# function to count number of inversions in a list of tiles
def count_inversions(tiles_arr, inversions):
    if len(tiles_arr) > 1:
        mid = len(tiles_arr) // 2
        left = tiles_arr[:mid]
        right = tiles_arr[mid:]

        inversions += count_inversions(left, 0)
        inversions += count_inversions(right, 0)
        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                tiles_arr[k] = left[i]
                i += 1
            else:
                tiles_arr[k] = right[j]
                j += 1
                # inversions calculation
                inversions += len(left) - i
            k += 1

        # Checking if any element was left
        while i < len(left):
            tiles_arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            tiles_arr[k] = right[j]
            j += 1
            k += 1
    return inversions


# function to shuffle tiles into a difficult-to-solve state
def shuffle_tiles(width, min_len, get_len = None, get_lc = None):
    # call hill_climbing
    return tuple(hill_climbing(width * width, min_len))


# function to find puzzle with min_lc number of conflicts
def conflict_tiles(width, min_lc, get_lc = None):
    # call beam_search method
    return tuple(beam_search(width * width, min_lc))


# function to run beam search to generate conflict tiles result
def beam_search(width, min_lc):
    # branching factor to use in search
    BRANCH_FACTOR = 100
    random_states = []
    frontier = []
    for i in range(BRANCH_FACTOR):
        random_states.append(get_random_solvable_state(width))

    # get frontier and check for solution
    for rs in random_states:
        # get frontier states
        f_states = get_frontier_states(rs)

        # for each state, check if satisfies min_lc and add to frontier
        for fs in f_states:
            fs_conflicts = count_conflicts(fs.tiles)
            if fs_conflicts >= min_lc:
                return fs.tiles
            frontier.append((fs, fs_conflicts))

    while True:
        most_conflicts = get_n_most_conflicts(frontier, BRANCH_FACTOR)
        count = len(most_conflicts)
        for i in range(BRANCH_FACTOR):
            new_random = get_random_solvable_state(width)
            new_conflicts = count_conflicts(new_random.tiles)
            most_conflicts.append((new_random, new_conflicts))


        new_frontier = []
        # get new frontier from most_conflicts and check for solution
        for mc in most_conflicts:
            # get frontier states
            f_states = get_frontier_states(mc[0])

            # for each state, check if satisfies min_lc and add to frontier
            for fs in f_states:
                fs_conflicts = count_conflicts(fs.tiles)
                if fs_conflicts >= min_lc:
                    return fs.tiles
                new_frontier.append((fs, fs_conflicts))
        # set new frontier
        frontier = new_frontier


# function to get n states with most conflicts
def get_n_most_conflicts(frontier, n):
    sort_by_conflicts(frontier)
    if n == 0:
        return []
    elif n >= len(frontier):
        return frontier
    else:
        output = []
        for i in range(n):
            output.append(frontier[i])
            print("i: {}, conflicts: {}, tiles: {}".format(i, frontier[i][1], frontier[i][0].tiles))
        return output


# function to get best n states from list of states based on conflicts
def sort_by_conflicts(frontier):
    if len(frontier) > 1:
        mid = len(frontier) // 2
        left = frontier[:mid]
        right = frontier[mid:]

        sort_by_conflicts(left)
        sort_by_conflicts(right)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(left) and j < len(right):
            if left[i][1] > right[j][1]:
                frontier[k] = left[i]
                i += 1
            else:
                frontier[k] = right[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left):
            frontier[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            frontier[k] = right[j]
            j += 1
            k += 1

# function to run simulated annealing search for conflict tiles state
def sim_annealing(width, min_lc):
    # get a random state and run anneal search on it
    random_state = get_random_solvable_state(width)
    anneal_result = anneal_search(random_state, min_lc)

    # repeat this process until a puzzle with enough conflicts found
    while anneal_result == None:
        random_state = get_random_solvable_state(width)
        anneal_result = anneal_search(random_state, min_lc)

    # puzzle with satisfactory min_lc found, return its tiles
    return anneal_result.tiles


# function to anneal search until goal or limit reached
def anneal_search(state, min_lc):
    p = 1.0
    reduction_rate = 0.9

    # set current state and current conflicts values
    current_state = state
    current_conflicts = count_conflicts(current_state.tiles)
    print("conflicts: {}".format(current_conflicts))
    print("p: {}".format(p))

    # check if enough conflicts found
    if current_conflicts >= min_lc:
        return current_state.tiles

    # set a count
    i = 0

    while True:
        # get frontier states
        f_states = get_frontier_states(current_state)
        result = get_random_with_p(f_states, p, current_conflicts)

        # if result is none, anneal has finished cooling, return
        if result == None:
            return None

        # get next state and conflicts
        next_state = result[0]
        next_conflicts = result[1]

        # check if enough conflicts found
        if next_conflicts > min_lc:
            return next_state

        # update current state and conflicts
        current_state = next_state
        current_conflicts = next_conflicts

        i += 1

        # reduce p by reduction_rate
        if i % 100 == 0:
            p = p * reduction_rate
        print("conflicts: {}".format(current_conflicts))
        print("p: {}".format(p))


# function to pick random state from frontier states given a probability
# function returns tuple with format: (next_state, next_conflicts)
def get_random_with_p(states, p, current_conflicts):
    print("num of f states: {}".format(len(states)))
    adjusted_p = 0
    while len(states) > 0:
        next_state = random.choice(states)
        next_conflicts = count_conflicts(next_state.tiles)
        if next_conflicts > current_conflicts:
            return (next_state, next_conflicts)
        if next_conflicts == current_conflicts:
            adjusted_p = p
        else:
            adjusted_p = p

        roll = random.random()
        print("roll: {}, adjusted_p: {}".format(roll, adjusted_p))

        if roll < adjusted_p:
            return (next_state, next_conflicts)
        else:
            states.remove(next_state)
    # no state found, return None
    print("out of states")
    return None


# funciton to conduct hill climbing search
def hill_climbing(width, min_len):

    # get a random state to begin hill climb
    random_state = get_random_solvable_state(width)

    # get best state and length
    best_state = climb_hill(random_state)
    longest_path = solve_puzzle(best_state.tiles)
    longest_path_length = len(longest_path)

    # return or save peak if possible
    if longest_path_length >= min_len:
        return best_state.tiles

    # keep climbing hills from random states until minimum length path found
    while True:
        # get a random state to begin hill climb
        random_state = get_random_solvable_state(width)

        # get peak state and length
        peak = climb_hill(random_state)
        peak_path = solve_puzzle(peak.tiles)
        peak_path_length = len(peak_path)

        # return or save peak if possible
        if peak_path_length >= min_len:
            return peak.tiles
        if peak_path_length > longest_path_length:
            best_state = peak
            longest_path = peak_path
            longest_path_length = peak_path_length


# function to climb hill to next peak state
def climb_hill(state):
    PLATEAU_MAX = 5
    current_plateau = 0
    highest = state

    # begin hill climb search for long path
    while True:
        # get frontier states to highest
        f_states = get_frontier_states(highest)
        # begin hill climb search for long path
        f_highest = get_highest_state(f_states)

        if f_highest.distance < highest.distance:
            return highest
        elif f_highest.distance == highest.distance:
            if current_plateau == PLATEAU_MAX:
                return highest
            current_plateau += 1
            highest = f_highest
        else:
            highest = f_highest


# function to get next state based on distance
def get_highest_state(f_states):
    max_state = f_states[0]
    max_distance = max_state.distance
    for f_state in f_states:
        if f_state.distance > max_state.distance:
            max_state = f_state
            max_distance = f_state.distance
    return max_state


# function to get a random solvable state
def get_random_solvable_state(width):
    # keep generating random states until one is solvable
    while True:
        available = []
        tmp = []
        # add tiles to available
        for i in range(width):
            available.append(i)
        # pick random tile to add
        for i in range(width):
            tile = random.choice(available)
            tmp.append(tile)
            available.remove(tile)
        tiles = tuple(tmp)
        # check if resulting puzzle is solvable
        if is_solvable(tiles):
            # get new state's elements
            conflicts = count_conflicts(tiles)
            md = get_manhattan_distance(tiles)
            return State(tiles, "", md + 2 * conflicts, 0)


# function to check if a move is valid
# move: a string representing a move
# tiles: a tuple (0, 1, 2, 3, 4, 5, 6, 7, 8)
def is_valid_move(tiles, move):
    allowed = "HJKL"
    blank = tiles.index(0)
    dim = int(math.sqrt(len(tiles)))
    if (blank % dim == 0):
        allowed = allowed.replace("L", "")
    if (blank < dim):
        allowed = allowed.replace("J", "")
    if (blank % dim == dim - 1):
        allowed = allowed.replace("H", "")
    if (blank >= len(tiles) - dim):
        allowed = allowed.replace("K", "")

    return move in allowed


# function to get manahattan distance from a given state
def get_manhattan_distance(tiles):
    dim = int(math.sqrt(len(tiles)))
    md = 0
    for i in range(len(tiles)):
        if not (tiles[i] == 0 or tiles[i] == i):
            md += get_distance(dim, tiles[i], i)
    return md


# get distance that a number is away from its correct position
def get_distance(dim, num, pos):
    distance = 0
    if (num > pos):
        while num // dim > pos // dim:
            distance += 1
            pos += dim
        if (num > pos):
            while num > pos:
                distance += 1
                pos += 1
        if (num < pos):
            while num < pos:
                distance += 1
                pos -= 1
    else:
        while pos // dim > num // dim:
            distance += 1
            pos -= dim
        if (num > pos):
            while num > pos:
                distance += 1
                pos += 1
        if (num < pos):
            while num < pos:
                distance += 1
                pos -= 1
    return distance


# function to count number of conflicts in a given state
def count_conflicts(tiles):
    # base cases
    if (len(tiles) <= 1):
        return 0

    dim = int(math.sqrt(len(tiles)))
    conflicts = 0
    for i in range(dim):
        row = []
        col = []
        for j in range(dim):
            row.append(tiles[i * dim + j])
            col.append(tiles[i + dim * j])
        conflicts += get_conflicts(dim, "row", i * dim, row)
        conflicts += get_conflicts(dim, "col", i, col)
    return conflicts

# gets number of conflicts in a row
def get_conflicts(dim, type, start, values):
    removed = []
    conflicts = 0
    conflicts_per = []
    increment_val = 0
    for i in range(len(values)):
        conflicts_per.append(0)

    if (type == "row"):
        increment_val = 1
    else:
        increment_val = dim

    while True:
        # count conflicts for each tile in row/column
        for i in range(len(values)):
            position = start + i * increment_val
            if (correct_line(dim, values[i], position, type)
                    and (not (values[i] in removed))):
                for j in range(len(values)):
                    position = start + j * increment_val
                    if (correct_line(dim, values[j], position, type)
                            and (not (values[j] in removed))):
                        if (j < i and values[j] > values[i]):
                            conflicts_per[i] += 1
                        elif (j > i and values[j] < values[i]):
                            conflicts_per[i] += 1

        # find tile with most conflicts, if zero, break while loop
        max_index = get_max(conflicts_per)
        if (conflicts_per[max_index] == 0):
            break
        removed.append(values[max_index])
        conflicts += 1
        # zero out conflicts_per list
        for i in range(len(conflicts_per)):
            conflicts_per[i] = 0
    return conflicts


# function to return index of max value in list
def get_max(list):
    max = list[0]
    max_index = 0
    for i in range(len(list)):
        if (list[i] > max):
            max = list[i]
            max_index = i
    return max_index


# function to check if a tile is in correct row
def correct_line(dim, num, pos, type):
    if (num == 0):
        return False
    if (type == "row"):
        return (num // dim == pos // dim)
    else:
        return (num % dim == pos % dim)


# function to solve tile puzzle
def solve_puzzle(tiles):
    pq = queue.PriorityQueue()
    i = 0
    while True:
        i += 1
        state = None
        if (pq.empty()):
            conflicts = count_conflicts(tiles)
            md = get_manhattan_distance(tiles)
            state = State(tiles, "", md + 2 * conflicts, 0)
        else:
            state = pq.get()

        frontier_states = get_frontier_states(state)
        for f_state in frontier_states:
            if (f_state.distance == 0):
                return f_state.moves
            pq.put(f_state)
    return "FAILURE"


# function to get new frontier states
def get_frontier_states(state):
    moves = "HJKL"
    reverse_moves = "LKJH"
    frontier_states = []
    # get rid of last move from move options
    if (len(state.moves) > 0):
        last_move = state.moves[len(state.moves) - 1:]
        reverse_move = reverse_moves[moves.find(last_move)]
        moves = moves.replace(reverse_move, "")

    for move in moves:
        if (is_valid_move(state.tiles, move)):
            next_state = get_state_from_move(state, move)
            frontier_states.append(next_state)
    return frontier_states


# function to get state from a move
def get_state_from_move(state, move):
    dim = int(math.sqrt(len(state.tiles)))
    new_tiles = []
    blank = 0
    # copy list and find the blank position
    for i in range(len(state.tiles)):
        if (state.tiles[i] == 0):
            blank = i
        new_tiles.append(state.tiles[i])

    # swap tiles based on move
    if (move == "H"):
        temp = new_tiles[blank + 1]
        new_tiles[blank + 1] = 0
        new_tiles[blank] = temp
    elif (move == "J"):
        temp = new_tiles[blank - dim]
        new_tiles[blank - dim] = 0
        new_tiles[blank] = temp
    elif (move == "K"):
        temp = new_tiles[blank + dim]
        new_tiles[blank + dim] = 0
        new_tiles[blank] = temp
    else:
        temp = new_tiles[blank - 1]
        new_tiles[blank - 1] = 0
        new_tiles[blank] = temp

    new_distance = get_manhattan_distance(new_tiles)
    conflicts = count_conflicts(new_tiles)

    total_distance = new_distance + conflicts * 2

    # add current path to estimated distance to get do a* search
    path_cost = total_distance + len(state.moves)
    new_moves = state.moves + move
    return State(new_tiles, new_moves, total_distance, path_cost)


# class to represent state objects
class State(object):
    tiles = []
    moves = ""
    distance = 0
    path_cost = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, tiles, moves, distance, path_cost):
        self.tiles = tiles
        self.moves = moves
        self.distance = distance
        self.path_cost = path_cost

    # make State objects comparable
    def __lt__(self, other):
        selfPriority = (self.path_cost)
        otherPriority = (other.path_cost)
        return selfPriority < otherPriority
