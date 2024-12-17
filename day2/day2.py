import sys

def test(arr):
    prev = arr[0]
    for a in arr[1:]:
        diff = a - prev
        if diff < 1 or diff > 3: return 0
        prev = a
    return 1

def solution1(arr):
    return sum([(test(row) or test(row[::-1])) for row in arr])

def solution2(arr):
    total = 0
    for row in arr:
        for i in range(len(row)):
            new_row = row[:i] + row[i+1:]
            if (test(new_row) or test(new_row[::-1])):
                total += 1
                break
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [[int(l) for l in line.split()]]

    print("Solution 1: ", solution1(arr))
    print("Solution 2: ", solution2(arr))
