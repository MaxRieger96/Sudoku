"""
This module allows to solve sudokus.
At first it tries to apply some heuristics, to find values for empty cells.
If the heuristics do not provide a full solution, the rest of the sudoku is solved via backtracking.
"""

def get_fields(sudoku):
    """
    returns the 9 3x3 fields of the sudoku
    """
    res = []
    for i in range(3):
        for j in range(3):
            current = sudoku[i * 3:(i + 1) * 3]
            current = [element[j * 3:(j + 1) * 3] for element in current]
            res.append(current)
    return res


def get_field(i, j, sudoku, flatten=True):
    """
    gets the field surrounding element [i,j]
    """
    res = get_fields(sudoku)[(i // 3) * 3 + (j // 3)]
    if flatten:
        return [elem for row in res for elem in row]
    else:
        return res


def get_row(i, sudoku):
    return sudoku[i]


def get_column(j, sudoku):
    return [row[j] for row in sudoku]


def get_possible_values(i, j, sudoku):
    """
    determines the possible values of field [i,j] in sudoku
    """
    ref = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    ref -= set(get_field(i, j, sudoku))
    ref -= set(get_row(i, sudoku))
    ref -= set(get_column(j, sudoku))
    return ref


def get_possibilities(sudoku):
    """
    determines the sets of possible values for each empty field in the sudoku
    """
    ref = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    result = [[0] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] not in ref:
                result[i][j] = get_possible_values(i, j, sudoku)
            else:
                result[i][j] = set()
    return result


def can_be_placed_elsewhere(i, j, nr, poss):
    """
    checks if nr can be placed in another field than at [i,j]
    """
    def other_contains(iterable, index, item):
        for i_curr, set_curr in enumerate(iterable):
            if type(set_curr) == set and i_curr != index and item in set_curr:
                return True
        return False

    def can_be_placed_in_row():
        return other_contains(get_row(i, poss), j, nr)

    def can_be_placed_in_column():
        return other_contains(get_column(j, poss), i, nr)

    def can_be_placed_in_field():
        return other_contains(get_field(i, j, poss), (i % 3) * 3 + (j % 3), nr)

    return can_be_placed_in_column() and can_be_placed_in_row() and can_be_placed_in_field()


def find_next_steps(sudoku):
    """
    finds determined values for given sudoku
    """
    poss = get_possibilities(sudoku)
    res = []
    for i in range(9):
        for j in range(9):
            current = poss[i][j]
            if type(current) == set:
                if len(current) == 1:
                    res.append((i, j, next(iter(current))))
                else:
                    for number in current:
                        if not can_be_placed_elsewhere(i, j, number, poss):
                            res.append((i, j, number))
                            break
    return res


def perform_steps(steps, sudoku):
    """
    applies all given steps to the sudoku
    """
    for step in steps:
        i, j, nr = step
        sudoku[i][j] = nr


def solve(sudoku, outputs=False):
    """
    tries to solve sudoku with some incomplete solving methods
    falls back to brute force, if these do not provide any new numbers
    """
    step_counter = 0
    while True:
        step_counter += 1
        steps = find_next_steps(sudoku)
        if len(steps) == 0:
            break
        perform_steps(steps, sudoku)
        if outputs:
            print_sudoku(sudoku)
            print()
    if outputs:
        if is_valid(sudoku):
            print("found solution in {} iterations".format(step_counter))
        else:
            print("no simple steps were found after {} iterations".format(step_counter))
            print("going on with brute force")
    if not is_valid(sudoku):
        brute_force(sudoku)


def brute_force(sudoku):
    """
    simple backtracking algorithm to solve a sudoku without heuristics
    """
    ref = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def next_step(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] not in ref:
                    return (i, j, get_possible_values(i, j, sudoku))
        return None

    def try_combinations(sudoku):
        step = next_step(sudoku)
        if step is None:
            return is_valid(sudoku)
        else:
            i, j, nrs = step
            for nr in nrs:
                sudoku[i][j] = nr
                if try_combinations(sudoku):
                    return True
            sudoku[i][j] = 0
            return False

    return try_combinations(sudoku)


def is_valid(sudoku):
    """
    checks if a sudoku is a valid solution
    """
    ref = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    arr = sudoku
    for i in arr:
        if set(i) != ref:
            return False
    for i in [list(x) for x in zip(*arr)]:
        if set(i) != ref:
            return False
    for i in get_fields(arr):
        flat = [item for sublist in i for item in sublist]
        if set(flat) != ref:
            return False
    return True


def parse_sudoku(sudoku):
    """
    parses a sudoku in string form to an array of integers
    """
    ref = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    ref = {str(elem) for elem in ref}
    for i in sudoku:
        for j, elem in enumerate(i):
            if elem in ref:
                i[j] = int(elem)
            else:
                i[j] = 0
    return sudoku


def print_sudoku(sudoku):
    """
    prints the sudoku
    """
    for row in sudoku:
        print(row)
    print()


def equality(s1, s2):
    """
    checks if two sudokus are the same
    """
    for i in range(9):
        for j in range(9):
            if s1[i][j] != s2[i][j]:
                return False
    return True


def convert_string_to_array(string):
    """
    converts a sudoku of compressed form to an array of strings
    """
    res = []
    curr = []
    for index, char in enumerate(string):
        curr.append(char)
        if index % 9 == 8:
            res.append(curr)
            curr = []
    return res


if __name__ == '__main__':
    # read sudoku from string
    string = "7...54..1.1.9.6....64....39....3.5...3..2..1...6.9....87....24....5.9.8.4..28...3"
    zs = parse_sudoku(convert_string_to_array(string))
    # print unsolved sudoku
    print_sudoku(zs)
    # solve sudoku and print every step
    solve(zs, True)
    # print solved sudoku
    print_sudoku(zs)
