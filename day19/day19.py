from functools import lru_cache
import sys

def solution1(patterns, arr):
    def f(s):
        if s == "": return True
        for p in patterns:
            if s.startswith(p):
                if f(s[len(p):]):
                    return True
        return False

    return sum([f(a) for a in arr])

def solution2(patterns, arr):
    @lru_cache(None)
    def f(s):
        if s == "": return 1
        total = 0
        for p in patterns:
            if s.startswith(p):
                total += f(s[len(p):])
        return total

    return sum([f(a) for a in arr])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    patterns = None
    with open(sys.argv[1], "r") as file:
        patterns = file.readline().strip().split(", ")
        file.readline()
        for line in file:
            arr += [line.strip()]

    print("Solution 1: ", solution1(patterns, arr))
    print("Solution 2: ", solution2(patterns, arr))


