from collections import defaultdict
import heapq
import math
import sys

def inside(dim_i, dim_j, i, j):
    return 0 <= i < dim_i and 0 <= j < dim_j

def get_start_stop(grid):
    start = None
    stop = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                start = i, j
            elif grid[i][j] == "E":
                stop = i, j
    return start, stop

# build initial solution and cost of path
def djikstra(grid):
    start, stop = get_start_stop(grid)

    q = [(0, start)]
    parent = defaultdict(tuple)
    dp = defaultdict(lambda: math.inf)
    dp[start] = 0

    while q:
        c, (i, j) = heapq.heappop(q)

        if (i, j) == stop:
            path_mp = defaultdict(int)
            path = []

            i, j = stop
            while (i, j) != start:
                path_mp[(i, j)] = c
                path.append((i, j))
                c -= 1
                (i, j) = parent[(i, j)]
            path_mp[start] = 0
            path.append(start)

            return path[::-1], path_mp

        for d_i, d_j in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            n_i, n_j = i + d_i, j + d_j

            if grid[n_i][n_j] != '#' and \
                c + 1 < dp[(n_i,n_j)]:
                dp[(n_i, n_j)] = c + 1
                parent[(n_i, n_j)] = (i, j)
                heapq.heappush(q, (dp[(n_i, n_j)], (n_i, n_j)))
    return {}

def savings(path, mp, allowed, target):
    total = 0
    for i, j in path:
        for dir_i in range(-allowed, allowed + 1):
            for dir_j in range(-allowed, allowed + 1):
                dist = abs(dir_i) + abs(dir_j)
                if dist > allowed: continue

                n_i, n_j = i + dir_i, j + dir_j
                if (n_i, n_j) in mp:
                    if mp[(n_i, n_j)] - mp[(i, j)] - dist >= target:
                        total += 1
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [line.strip()]

    path, mp = djikstra(arr)
    print("Solution 1: ", savings(path, mp, 2, 100))
    print("Solution 2: ", savings(path, mp, 20, 100))


