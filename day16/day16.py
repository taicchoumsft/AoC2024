import sys
import math
import heapq
from collections import defaultdict

def next_dirs(dir):
    if dir[0] == 0:
        return [(1, 0), (-1, 0)]
    return [(0, 1), (0, -1)]

dirs = [(0, 1), (1,0), (-1, 0), (0, -1)]

def print_grid(grid):
    for row in grid:
        print("".join(row))

def get_start_stop(grid):
    dim_i, dim_j = len(grid), len(grid[0])

    start, stop = None, None
    for i in range(dim_i):
        for j in range(dim_j):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                stop = (i, j)
    return start, stop

def solution1(grid):
    start, stop = get_start_stop(grid)

    q = [(0, start, (0, 1))]

    parents = defaultdict(set)
    dp = defaultdict(lambda: math.inf)
    dp[(start, (0, 1))] = 0

    while q:
        score, pos, dir = heapq.heappop(q)
        if grid[pos[0]][pos[1]] == '#': continue

        # just go straight
        # for second part, store parent paths Many best paths exist
        # use <= instead of traditional < to allow more than
        # one best result.  There's probably some subtle bug here, but it gives correct output
        if score + 1 <= dp[((pos[0] + dir[0], pos[1] + dir[1]), dir)]:
            dp[((pos[0] + dir[0], pos[1] + dir[1]), dir)] = score + 1

            if score + 1 < dp[((pos[0] + dir[0], pos[1] + dir[1]), dir)]:
                parents[(pos[0] + dir[0], pos[1] + dir[1])] = set((pos, dir))
            else:
                parents[(pos[0] + dir[0], pos[1] + dir[1])].add((pos, dir))

            heapq.heappush(q, (score + 1, (pos[0] + dir[0], pos[1] + dir[1]), dir))

        # bend
        for next_dir in next_dirs(dir):
            if score + 1000 <= dp[(pos, next_dir)]:
                dp[(pos, next_dir)] = score + 1000
                heapq.heappush(q, (score + 1000, pos, next_dir))

    best = min(dp[stop, d] for d in dirs)
    return best, parents

def solution2(grid, score, parents):
    start, stop = get_start_stop(grid)
    seen = set()

    # up to now, we only have parent links, but they might not all sum up to the best score.
    # Backtrack and filter out
    def backtrack(current_node, cur_dir, cur_score):
        if current_node == start:
            # start dir is always facing East, so account for this
            if cur_dir == (0, 1) and cur_score == score or cur_score + 1000 == score:
                return [[start]]

        paths = []
        if current_node in seen: return set()
        seen.add(current_node)

        for prev, prev_dir in parents[current_node]:
            add = 1 if prev_dir == cur_dir else 1001

            for path in backtrack(prev, prev_dir, cur_score + add):
                paths.append(path + [current_node])

        seen.remove(current_node)
        return paths

    all_paths = []
    for dir in dirs:
        all_paths += backtrack(stop, dir, 0)

    result = set()
    for p in all_paths:
        result |= set(p)

    return len(result)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    grid = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            grid += [list(line.strip())]

    score, parents = solution1(grid)
    print("Solution 1: ", score)
    print("Solution 2: ", solution2(grid, score, parents))

