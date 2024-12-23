from functools import lru_cache
import math
import sys

numeric_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]
directional_keypad = [["#", "^", "A"], ["<", "v", ">"]]
dirs = [(">", 0, 1), ("v", 1, 0), ("^", -1, 0), ("<", 0, -1)]

def inside(dim_i, dim_j, i, j):
    return i >= 0 and i < dim_i and j >= 0 and j < dim_j

def coord_lookup(value, keypad_type):
    keypad = numeric_keypad if keypad_type == 0 else directional_keypad

    for i in range(len(keypad)):
        for j in range(len(keypad[0])):
            if keypad[i][j] == value:
                return (i, j)
    return None

# no need to traverse all paths - the "obvious" shorter paths
# have to be as straight as possible - so there are only at most 2 paths
# if the path goes through a *, one of the 2 paths have to be pruned
# def all_paths(frm, to, keypad_type):
#     keypad = numeric_keypad if keypad_type == 0 else directional_keypad
#     q = [(frm, [])]
#     cnt = 0
#     results = []
#     seen = set()
#     if frm == to:
#         return ["A"]

#     while q:
#         sz = len(q)
#         while sz > 0:
#             (i, j), path = q.pop(0)

#             if (i, j) == to:
#                 sz -= 1
#                 results.append("".join(path) + "A")
#                 continue

#             if (i, j) in seen:
#                 sz -= 1
#                 continue
#             seen.add((i, j))

#             for ch, di, dj in dirs:
#                 ni, nj = i + di, j + dj
#                 if inside(len(keypad), len(keypad[0]), ni, nj) and \
#                     keypad[ni][nj] != '#':
#                     q += [((ni, nj), path + [ch])]
#             sz -= 1
#         cnt += 1

#     return results

def all_paths(frm, to, keypad_type):
    (i1, j1), (i2, j2) = frm, to

    i_path = "v" * (i2 - i1) if i2 > i1 else "^" * (i1 - i2)
    j_path = ">" * (j2 - j1) if j2 > j1 else "<" * (j1 - j2)

    # we have to check if we hit the bottom left pocket
    # if we're looking at the numeric keypad
    if keypad_type == 0 and (i2 == 3 and j1 == 0):
        # if going 1st column to last row, impossible to use the i_path first
        return [j_path + i_path + "A"]
    elif keypad_type == 0 and (i1 == 3 and j2 == 0):
        # going from last row to first column, cannot use j_path first
        return [i_path + j_path + "A"]
    elif keypad_type == 1 and (i1 == 0 and j2 == 0):
        return [i_path + j_path + "A"]
    elif keypad_type == 1 and (j1 == 0 and i2 == 0):
        return [j_path + i_path + "A"]
    else:
        return [i_path + j_path + "A", j_path + i_path + "A"]

# idea here is instead of returning the output of each
# bot first, then calculating the output of the next bot etc
# we do all the layers of bots per character (up to the A)
# all at once
def solution2(arr, bots = 3):
    @lru_cache
    def f(idx, chars):
        if idx == bots: return len(chars)

        keypad_type = 0 if idx == 0 else 1
        start = (3, 2) if idx == 0 else (0, 2)

        total = 0
        for ch in chars:
            end = coord_lookup(ch, keypad_type)

            best = math.inf

            for nbrs in all_paths(start, end, keypad_type):
                best = min(best, f(idx + 1, nbrs))

            start = end
            total += best
        return total

    total = 0
    for a in arr:
        total += f(0, a) * int(a[:-1])
    return total

# # generate the numeric to first directional
# # keypad type 0 is numeric, keypad type 1 is directional
# # brute force solution, takes too long for both solutions
# @lru_cache
# def gen(target, nk, keypad_type):
#     if not target: return [""]

#     results = []
#     for a in all_paths(nk, coord_lookup(target[0], keypad_type), keypad_type):
#         for b in gen(target[1:], coord_lookup(target[0], keypad_type), keypad_type):
#             results += [a + b]

#     #filter results to just minimum
#     mn_len = min([len(a) for a in results])
#     return [r for r in results if len(r) == mn_len]
#     #return results


# def solution1(arr):
#     total = 0
#     for a in arr:
#         results = []
#         for kp1 in gen(a, (3,2), 0):
#             for kp2 in gen(kp1, (0,2), 1):
#                 for kp3 in gen(kp2, (0,2), 1):
#                     results.append(kp3)

#         mn_len = min([len(r) for r in results])
#         print(f"{a}: {mn_len} * {int(a[:-1])}: {mn_len * int(a[:-1])}")

#         total += mn_len * int(a[:-1])

#     return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr.append(line.strip())

    print("Solution 1: ", solution2(arr, 3))
    print("Solution 2: ", solution2(arr, 26))

