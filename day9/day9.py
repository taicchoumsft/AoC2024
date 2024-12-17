import sys

def solution1(arr):
    # just follow instructions, easier than coming up with a fancy repr
    input_string = arr
    disk = []

    cur = 0
    for idx, ch in enumerate(input_string):
        if idx & 1:
            disk += '.' * int(ch)
        else:
            disk += [cur] * int(ch)
            cur += 1

    all_dots = [idx for idx, d in enumerate(disk) if d == '.']
    cur = 0
    for idx, p in enumerate(disk[::-1]):
        if p == '.': continue
        if cur < len(all_dots):
            if (all_dots[cur] > (len(disk) - idx - 1)): break
            disk[all_dots[cur]] = p
            disk[len(disk) - idx - 1] = '.'
            cur += 1

    total = 0
    for idx, d in enumerate(disk):
        if d == '.': break
        total += idx * d
    return total

def solution2(arr):
    # have to treat each id as taking 1 char
    input_string = arr

    free = []
    used = []
    for idx, ch in enumerate(input_string):
        if idx & 1:
            free += [[int(ch), []]] # encode # free bits, and the bits themselves when moved
        else:
            used += [[idx // 2, int(ch)]] # encode id, number of used bits

    for u_id, u_len in used[::-1]:
        for f_idx in range(u_id):
            if free[f_idx][0] >= u_len:
                free[f_idx][1] += [u_id] * u_len
                free[f_idx][0] -= u_len
                used[u_id][0] = '.'
                break

    res = []
    free += [[0, []]] # all the sample input, free is less than used by 1
    for u, f in zip(used, free):
        res += [u[0]] * u[1] # add the used bits first
        res += f[1] # add the shifted bits if any
        res += ['.'] * f[0] # add remaining free space if any

    total = 0
    for idx, d in enumerate(res):
        if d == '.': continue
        total += (idx * int(d))
    return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    with open(sys.argv[1], "r") as file:
        arr = file.readline()

        print("Solution 1: ", solution1(arr))
        print("Solution 2: ", solution2(arr))
