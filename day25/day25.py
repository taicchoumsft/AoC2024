import sys

def solution1(locks, keys):
    def check(lock, key):
        return all([l + k <= 5 for l, k in zip(lock, key)])

    return sum(1 for l in locks for k in keys if check(l, k))

def parse_grid(grid):
    dim_i, dim_j = len(grid), len(grid[0])

    arr = []
    for j in range(dim_j):
        total = 0
        for i in range(1, dim_i - 1):
            if grid[i][j] == '#':
                total += 1
        arr += [total]
    return arr

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    keys = []
    locks = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            if line in ['\n', '\r\n']:
                if '#' in arr[0]:
                    locks += [parse_grid(arr)]
                else:
                    keys += [parse_grid(arr)]
                arr = []
            else:
                arr += [line.strip()]

    print("Solution 1: ", solution1(locks, keys))


