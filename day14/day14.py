import sys
import re

# changes for sample vs input
# dim_i, dim_j = 7, 11
dim_i, dim_j = 103, 101

def solution1(P, V, cycles = 100):
    arr = []
    for p, v in zip(P, V):
        i, j = p
        dir_i, dir_j = v

        new_i = (i + cycles * dir_i) % dim_i
        new_j = (j + cycles * dir_j) % dim_j
        arr.append((new_i, new_j))

    cnt = [0] * 4
    for i, j in arr:
        if 0 <= i < dim_i //2:
            if 0 <= j < dim_j // 2:
                cnt[0] += 1
            elif dim_j // 2 < j < dim_j:
                cnt[1] += 1
        elif dim_i // 2 < i < dim_i:
            if 0 <= j < dim_j // 2:
                cnt[2] += 1
            elif dim_j // 2 < j < dim_j:
                cnt[3] += 1

    total = 1
    for c in cnt:
        total *= c
    return total

def print_grid(arr):
    grid = [[' ' for _ in range(dim_j)] for _ in range(dim_i)]

    for i, j in arr:
        grid[i][j] = '\u2764'

    for row in grid:
        print("".join(row))


def solution2(P, V):
    # spotted a pattern at cycle 28, repeating every 101 cycles
    # amazingly, just visually tracking these cycles in a text editor, gives the tree at cycle 7502 for my input
    for cycles in range(28, 100000, 101):
        print(f"CYCLE {cycles}")
        arr = []
        for p, v in zip(P, V):
            i, j = p
            dir_i, dir_j = v

            new_i = (i + cycles * dir_i) % dim_i
            new_j = (j + cycles * dir_j) % dim_j
            arr.append((new_i, new_j))

        print_grid(arr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    p = []
    v = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            m = re.match(r"p\=(-?\d+),(-?\d+) v\=(-?\d+),(-?\d+)", line)
            p.append((int(m.group(2)), int(m.group(1))))
            v.append((int(m.group(4)), int(m.group(3))))

    #print("Solution 1: ", solution1(p, v, 100))
    print("Solution 2: ", solution2(p, v))


