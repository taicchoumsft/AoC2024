import sys

dirs = [(0, 1), (1, 0), (0, -1),  (-1, 0)]

def inside(dim_i, dim_j, i, j):
    return i >= 0 and i < dim_i and j >= 0 and j < dim_j

def solution1(arr):
    dim_i, dim_j = len(arr), len(arr[0])

    def f(ch, i, j, seen, perims):
        if (i, j) in seen:
            return (0, 0)
        seen.add((i, j))

        area = 1
        perim = 0

        for dir_i, dir_j in dirs:
            n_i, n_j = i + dir_i, j + dir_j

            if inside(dim_i, dim_i, n_i, n_j) and \
                arr[n_i][n_j] == ch:
                n_a, n_p = f(ch, n_i, n_j, seen, perims)
                area += n_a
                perim += n_p

            if not inside(dim_i, dim_j, n_i, n_j) or \
                (inside(dim_i, dim_i, n_i, n_j) and arr[n_i][n_j] != ch):
                perims.add((arr[i][j], i, j, dir_i, dir_j))
                perim += 1
        return (area, perim)

    seen = set()
    total = 0
    data = []

    for i in range(dim_i):
        for j in range(dim_j):
            if (i, j) not in seen:
                perims = set() # store perims for solution 2
                a, p = f(arr[i][j], i, j, seen, perims)
                data.append((arr[i][j], a, p, perims))
                total += a * p
    return total, data

def orthogonal(dir_i, _):
    if dir_i != 0:
        return [(0, -1), (0, 1)]
    else:
        return [(1, 0), (-1, 0)]

def solution2(arr, data):
    dim_i, dim_j = len(arr), len(arr[0])

    # had to scratch my head for awhile
    # idea here is to simulate walking the perimeter
    # we preserve the perimeter from solution 1, and the "direction" of the perimeter
    # which identifies which side of the grid we're looking at
    # then we keep only one of the items from the perimeter if they're connected and
    # looking at the same direction
    total = 0
    for ch, a, p, perims in data:
        # now start with any perim value, save it, then walk in orthogonal direction to the perimeter, and remove
        # those values from the perim set
        to_erase = set()
        to_save = set()
        for ch, i,j, dir_i, dir_j in perims:
            if (ch, i, j, dir_i, dir_j) in to_erase: continue
            to_save.add((i, j, dir_i, dir_j))

            for dir_i2, dir_j2 in orthogonal(dir_i, dir_j):
                n_i, n_j = i, j
                while inside(dim_i, dim_j, n_i, n_j) and \
                        arr[n_i][n_j] == ch and \
                        (ch, n_i, n_j, dir_i, dir_j) in perims:
                    to_erase.add((ch, n_i, n_j, dir_i, dir_j))
                    n_i += dir_i2
                    n_j += dir_j2
        total += a * len(to_save)
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [line.strip()]

    sol1, data = solution1(arr)
    print("Solution 1: ", sol1)
    print("Solution 2: ", solution2(arr, data))


