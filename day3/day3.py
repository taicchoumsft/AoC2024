import sys
import re

def solution1(arr):
    total = 0
    for a in arr:
        x = re.findall("mul\\([0-9]{1,3},[0-9]{1,3}\\)", a)
        for p in x:
            first, second = p.split(",")
            first = int(first[4:])
            second = int(second[:-1])
            total += first * second
    return total

def solution2(arr):
    total = 0
    take = True
    for a in arr:
        x = re.findall("mul\\([0-9]{1,3},[0-9]{1,3}\\)|do\\(\\)|don\'t\\(\\)", a)
        for p in x:
            if p == "don't()":
                take = False
            elif p == "do()":
                take = True
            else:
                first, second = p.split(",")
                first = int(first[4:])
                second = int(second[:-1])
                if take: total += first * second
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [line]

    print("Solution 1: ", solution1(arr))
    print("Solution 2: ", solution2(arr))


