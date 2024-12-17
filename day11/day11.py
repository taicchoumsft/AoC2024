import sys
from functools import lru_cache

# brute force, slow of course
def solution1(arr, b):
    while b > 0:
        ln = len(arr)
        for idx in range(ln):
            a = arr[idx]
            if a == 0:
                arr[idx] = 1
            elif len(str(a)) % 2 == 0:
                half = len(str(a)) // 2
                p1, p2 = str(a)[:half], str(a)[half:]
                arr[idx] = int(p1)
                arr.append(int(p2))
            else:
                arr[idx] *= 2024
        b -= 1
    return len(arr)

def solution2(arr, blink):
    # count only the new stones that were added.
    # add back original stones length for full answer
    @lru_cache(None)
    def recurse(a, b):
        if b == 0: return 0
        elif a == 0:
            return recurse(1, b - 1)
        elif len(str(a)) % 2 == 0:
            half = len(str(a)) // 2
            p1, p2 = str(a)[:half], str(a)[half:]
            return 1 + recurse(int(p1), b - 1) + recurse(int(p2), b - 1)
        else:
            return recurse(a * 2024, b - 1)

    return sum(recurse(a, blink) for a in arr) + len(arr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [int(l) for l in line.split()]

    print("Solution 1: ", solution2(arr[:], 25))
    print("Solution 2: ", solution2(arr[:], 75))


