import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [line]

    def solution1():
        pass

    def solution2():
        pass

    print("Solution 1: ", solution1())
    print("Solution 2: ", solution2())


