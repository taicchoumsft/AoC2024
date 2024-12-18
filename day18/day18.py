import sys

dim_i, dim_j = 71, 71

dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

def inside(i, j):
    return i >= 0 and i < dim_i and j >= 0 and j < dim_j

def print_grid(grid):
    for row in grid:
        print("".join(row))

def bfs(grid):
    start = (0, 0)
    stop = (dim_i - 1, dim_j - 1)
    q = [start]

    cnt = 0
    seen = set()
    while q:
        sz = len(q)
        while sz > 0:
            i, j = q.pop(0)

            if (i, j) == stop:
                return cnt

            if (i, j) in seen:
                sz -= 1
                continue
            seen.add((i, j))

            for d_i, d_j in dirs:
                n_i, n_j = i + d_i, j + d_j
                if inside(n_i, n_j) and \
                    grid[n_i][n_j] != '#':
                    q.append((n_i, n_j))

            sz -= 1

        cnt += 1
    return -1

def solution1(arr, fallen):
    grid = [['.' for _ in range(dim_j)] for _ in range(dim_i)]
    for (i, j) in arr[:fallen]:
        grid[i][j] = '#'

    print_grid(grid)

    return bfs(grid)

def solution2(arr):
    grid = [['.' for _ in range(dim_j)] for _ in range(dim_i)]

    for (i, j) in arr:
        grid[i][j] = '#'
        if bfs(grid) == -1:
            return f"{j},{i}"
    return -1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            j, i = [int(l) for l in line.strip().split(",")]
            arr += [(i, j)]

    print("Solution 1: ", solution1(arr, 1024))
    print("Solution 2: ", solution2(arr))


