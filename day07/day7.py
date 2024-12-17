import sys

def solution1(mp):
    def f(arr, target, idx, cur):
        if idx == len(arr):
            return cur == target

        add = f(arr, target, idx + 1, cur + arr[idx])
        mul = f(arr, target, idx + 1, cur * arr[idx])

        return add or mul

    total = 0
    for k, arr in mp:
        if f(arr, k, 1, arr[0]):
            total += k
    return total

def solution2(mp):
    def f(arr, target, idx, cur):
        if idx == len(arr):
            return cur == target

        add = f(arr, target, idx + 1, cur + arr[idx])
        mul = f(arr, target, idx + 1, cur * arr[idx])
        comb = f(arr, target, idx + 1, int(str(cur) + str(arr[idx])))

        return add or mul or comb

    total = 0
    for k, arr in mp:
        if f(arr, k, 1, arr[0]):
            total += k
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Need file name")

    arr = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            k, vs = line.split(": ")
            vs = [int(v) for v in vs.split()]
            arr += [(int(k), vs)]

    print(f"Solution 1: {solution1(arr)}")
    print(f"Solution 2: {solution2(arr)}")

