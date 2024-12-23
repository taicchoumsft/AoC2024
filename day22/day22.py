from collections import defaultdict
import sys

MOD = 16777216

def solution1(arr, to=10):
    total = 0
    for s in arr:
        for _ in range(to):
            s ^= s * 64
            s %= MOD
            s ^= s // 32
            s %= MOD
            s ^= s * 2048
            s %= MOD
        total += s
    return total

def solution2(arr, to=2000):

    def gen_seq(s, to):
        fwd = [0] * to
        seq = [0] * to

        fwd[0] = None
        seq[0] = s % 10

        for i in range(1, to):
            s ^= s * 64
            s %= MOD
            s ^= s // 32
            s %= MOD
            s ^= s * 2048
            s %= MOD
            fwd[i] = (s % 10) - seq[i-1]
            seq[i] = s % 10
        return fwd, seq

    total_mp = defaultdict(int)

    for a in arr:
        fwd, seq = gen_seq(a, to)
        mp = {}
        for i in range(4, len(fwd)):
            key = tuple(fwd[i-3:i + 1])
            val = seq[i]
            if key not in mp:
                mp[key] = val

        # merge the total with the mp
        for k, v in mp.items():
            total_mp[k] += v

    # naive approach - create a large dict of 4 tuples to the seq
    # Sum the map through all iterations
    mx = 0
    best_key = None
    for k, v in total_mp.items():
        if v > mx:
            mx = v
            best_key = k

    return best_key, mx

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            arr += [int(line.strip())]

    print("Solution 1: ", solution1(arr, 2000))
    print("Solution 2: ", solution2(arr, 2001)) # off by one


