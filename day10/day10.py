import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [[int(l) for l in line.strip()]]

    dim_i, dim_j = len(arr), len(arr[0])

    def inside(i, j):
        return i >= 0 and i < dim_i and j >= 0 and j < dim_j

    def dfs(i, j, cur, seen):
        if (i, j) in seen: return 0
        seen.add((i, j))

        if cur == 9:
            return 1

        total = 0
        for dir_i, dir_j in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_i, new_j = i + dir_i, j + dir_j
            if inside(new_i, new_j) and \
                arr[new_i][new_j] == cur + 1:
                total += dfs(new_i, new_j, cur + 1, seen)
        return total

    def backtrack(i, j, cur, seen):
        if cur == 9:
            return 1

        total = 0
        for dir_i, dir_j in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_i, new_j = i + dir_i, j + dir_j
            if inside(new_i, new_j) and \
                (new_i, new_j) not in seen and \
                arr[new_i][new_j] == cur + 1:
                seen.add((new_i, new_j))
                total += backtrack(new_i, new_j, cur + 1, seen)
                seen.remove((new_i, new_j))

        return total

    total = 0
    total2 = 0
    for i in range(dim_i):
        for j in range(dim_j):
            if arr[i][j] == 0:
                total += dfs(i, j, 0, set())
                total2 += backtrack(i, j, 0, set())

    print("Solution 1: ", total)
    print("Solution 2: ", total2)
