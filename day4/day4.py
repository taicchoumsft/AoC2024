import sys
import itertools

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [line.strip()]

    dim_i, dim_j = len(arr), len(arr[0])

    def check(t, i, j, dir_i, dir_j, idx = 0):
        if idx == len(t): return 1
        if i >= 0 and i < dim_i and \
            j >= 0 and j < dim_j and \
                arr[i][j] == t[idx]:
            return check(t, i + dir_i, j + dir_j, dir_i, dir_j, idx + 1)
        return 0

    def solution1():
        t = "XMAS"
        total = 0
        for i, j, dir_i, dir_j in itertools.product(range(dim_i), range(dim_j), range(-1, 2), range(-1, 2)):
            if dir_i == 0 and dir_j == 0: continue
            total += check(t, i, j, dir_i, dir_j)
        return total

    def solution2():
        t = "MAS"
        # check target and pass dir (probably easier to check center coordinate tbh)
        total = 0
        for i, j in itertools.product(range(dim_i - len(t) + 1), range(dim_j - len(t) + 1)):
            total += (check(t, i, j, 1, 1) or \
                check(t, i + 2, j + 2, -1, -1)) and \
                (check(t, i + 2, j, -1, 1) or \
                check(t, i, j + 2, 1, -1))
        return total

    print("Solution 1: ", solution1())
    print("Solution 2: ", solution2())
