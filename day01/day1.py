import sys
from collections import Counter

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr1 = []
    arr2 = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            l1, l2 = [int(l) for l in line.split()]
            arr1.append(l1)
            arr2.append(l2)

    print("Solution 1:", sum([abs(a1 - a2) for a1, a2 in zip(sorted(arr1), sorted(arr2))]))

    cnt2 = Counter(arr2)
    print("Solution 2:", sum([a * cnt2[a] for a in arr1]))
