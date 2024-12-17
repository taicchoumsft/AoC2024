import sys
from collections import defaultdict

def inside(dim_i, dim_j, i, j):
    return i >= 0 and i < dim_i and j >= 0 and j < dim_j

def solution1(arr):
    dim_i, dim_j = len(arr), len(arr[0])
    mp = defaultdict(list)

    for i in range(dim_i):
        for j in range(dim_j):
            if arr[i][j] != '.':
                mp[arr[i][j]].append((i, j))

    antinodes = set()
    for k, arr in mp.items():
        for idx1, (i1, j1) in enumerate(arr):
            for idx2, (i2, j2) in enumerate(arr):
                if idx1 == idx2: continue
                diff_i, diff_j = i2 - i1, j2 - j1

                a_i, a_j = i2 + diff_i, j2 + diff_j
                if inside(dim_i, dim_j, a_i, a_j):
                    antinodes.add((a_i, a_j))

    return len(antinodes)

def solution2(arr):
    dim_i, dim_j = len(arr), len(arr[0])
    mp = defaultdict(list)

    for i in range(dim_i):
        for j in range(dim_j):
            if arr[i][j] != '.':
                mp[arr[i][j]].append((i, j))

    antinodes = set()
    for k, arr in mp.items():
        for idx1, (i1, j1) in enumerate(arr):
            for idx2, (i2, j2) in enumerate(arr):
                if idx1 == idx2: continue
                diff_i, diff_j = i2 - i1, j2 - j1

                tmp_i, tmp_j = i2, j2
                while inside(dim_i, dim_j, tmp_i + diff_i, tmp_j + diff_j):
                    tmp_i += diff_i
                    tmp_j += diff_j
                    antinodes.add((tmp_i, tmp_j))

                antinodes.add((i1, j1))
                antinodes.add((i2, j2))

    return len(antinodes)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Need file name")

    arr = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            arr += [line.strip()]

    print(f"Solution 1: {solution1(arr)}")
    print(f"Solution 2: {solution2(arr)}")
