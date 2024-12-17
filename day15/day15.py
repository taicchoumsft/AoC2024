import sys
from collections import defaultdict
import copy

def inside(dim_i, dim_j, i, j):
    return i >= 0 and i < dim_i and j >= 0 and j < dim_j

path_mp = {'<': (0, -1), '^': (-1, 0), 'v': (1, 0), '>': (0, 1)}

def can_move(grid, i, j, dir_i, dir_j):
    if grid[i][j] == '.':
        return True, (i, j)
    elif grid[i][j] == '#':
        return False, None
    else:
        n_i, n_j = i + dir_i, j + dir_j
        return can_move(grid, n_i, n_j, dir_i, dir_j)

def print_grid(grid):
    for row in grid:
        print("".join(row))

def solution1(grid, path):
    dim_i, dim_j = len(grid), len(grid[0])

    start_pos = None
    for i in range(dim_i):
        for j in range(dim_j):
            if grid[i][j] == '@':
                start_pos = (i, j)

    i, j = start_pos
    for p in path:
        dir_i, dir_j = path_mp[p]

        n_i, n_j = i + dir_i, j + dir_j

        if grid[n_i][n_j] == '.':
            grid[i][j] = '.'
            i, j = n_i, n_j
            grid[i][j] = '@'
        elif grid[n_i][n_j] == 'O':
            # move the O box, but if the next box (and so on) is also a 'O', push until we hit the '#'
            # move the last box to l_i, l_j
            can, last_free =  can_move(grid, n_i, n_j, dir_i, dir_j)

            if can:
                l_i, l_j = last_free
                grid[l_i][l_j] = 'O'
                grid[n_i][n_j] = '@'
                grid[i][j] = '.'
                i, j = n_i, n_j

    total = 0
    for i in range(dim_i):
        for j in range(dim_j):
            if grid[i][j] == 'O':
                total += 100 * i + j
    return total

# as we move, we grow the row from start_j to end_j. Anything
# impeding start_j to end_j essentially causes us to stop
#    []  #
#   [][][]
#    [][]
#     []
def move_vertical(grid, row, dir_i, dir_j):
    # all selected blocks in a row must be able to move together, or be blocked together?
    # that's the current assumption

    new_row = set() # just store [ side

    can_all_move = True
    for i, j in row:
        n_i, n_j = i + dir_i, j + dir_j
        if grid[n_i][n_j] == '[':
            new_row.add((n_i, n_j))
        elif grid[n_i][n_j] == ']':
            new_row.add((n_i, n_j - 1))
        elif grid[n_i][n_j] == '#':
            can_all_move = False

        s_n_i, s_n_j = i + dir_i, j + dir_j + 1
        if grid[s_n_i][s_n_j] == '[':
            new_row.add((s_n_i, s_n_j))
        elif grid[s_n_i][s_n_j] == '#':
            can_all_move = False

    if not can_all_move:
        return False

    if not new_row:
        # move all previous row items up to this level
        for i, j in row:
            grid[i + dir_i][j] = '['
            grid[i + dir_i][j + 1] = ']'
            grid[i][j] = '.'
            grid[i][j + 1] = '.'
        return True

    if move_vertical(grid, new_row, dir_i, dir_j):
        for i, j in row:
            grid[i + dir_i][j] = '['
            grid[i + dir_i][j + 1] = ']'
            grid[i][j] = '.'
            grid[i][j + 1] = '.'
        return True


def solution2(grid, path):
    new_grid = []
    for row in grid:
        new_row = []
        for i in row:
            if i == '#':
                new_row += ['#', '#']
            elif i == 'O':
                new_row += ['[', ']']
            elif i == '.':
                new_row += ['.', '.']
            else:
                new_row += ['@', '.']
        new_grid += [new_row]

    grid = new_grid

    dim_i, dim_j = len(grid), len(grid[0])

    start_pos = None
    for i in range(dim_i):
        for j in range(dim_j):
            if grid[i][j] == '@':
                start_pos = (i, j)

    i, j = start_pos
    for p in path:
        dir_i, dir_j = path_mp[p]

        n_i, n_j = i + dir_i, j + dir_j

        if grid[n_i][n_j] == '.':
            grid[i][j] = '.'
            i, j = n_i, n_j
            grid[i][j] = '@'
        elif grid[n_i][n_j] in ['[', ']']:
            # move the O box, but if the next box (and so on) is also a 'O', push until we hit the '#'
            # move the last box to l_i, l_j

            # now we need directional knowledge as well, if pushing left or right, we just shift all our blocks
            if p in ['<', '>']:
                # take care of the easier horizontal movement - can repurpose some logic from soln to do thi
                can, last_free =  can_move(grid, n_i, n_j, dir_i, dir_j)
                if can:
                    l_i, l_j = last_free
                    alternate = ['[', ']']
                    altId = 0
                    if p == '>':
                        for k in range(n_j + 1, l_j + 1):
                            grid[l_i][k] = alternate[altId]
                            altId = (altId + 1) % 2
                    elif p == '<':
                        for k in range(l_j, n_j):
                            grid[l_i][k] = alternate[altId]
                            altId = (altId + 1) % 2
                    grid[n_i][n_j] = '@'
                    grid[i][j] = '.'
                    i, j = n_i, n_j
            else:
                # harder vertical movement
                if grid[n_i][n_j] == '[':
                    row = {(n_i, n_j)}
                elif grid[n_i][n_j] == ']':
                    row = {(n_i, n_j - 1)}
                if move_vertical(grid, row, dir_i, dir_j):
                    grid[n_i][n_j] = '@'
                    grid[i][j] = '.'
                    i, j = n_i, n_j
    print_grid(grid)

    total = 0
    for i in range(dim_i):
        for j in range(dim_j):
            if grid[i][j] == '[':
                total += 100 * i + j
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Need file name")

    grid = []
    path = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            if line.startswith("#"):
                grid += [list(line.strip())]
            elif line:
                path += [line.strip()]
    path = ''.join(path)

    print(f"Solution 1: {solution1(copy.deepcopy(grid), path)}")
    print(f"Solution 2: {solution2(grid, path)}")
