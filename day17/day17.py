from functools import lru_cache
import sys

def combo(registers, data):
    if 0 <= data <= 3: return data
    elif data == 4: return registers['A']
    elif data == 5: return registers['B']
    elif data == 6: return registers['C']
    else: raise Exception("Combo op 7 not expected")

def solution1(r, program):
    output = []
    ip = 0
    while (ip < len(program)):
        op = program[ip]
        data = program[ip + 1]

        if op == 0:
            num = r['A']
            den = 2 ** combo(r, data)
            r['A'] = num // den
        elif op == 1:
            l = r['B']
            r['B'] = l ^ data
        elif op == 2:
            r['B'] = combo(r, data) % 8
        elif op == 3:
            if r['A'] != 0:
                if ip != data:
                    # jump happened
                    ip = data
                    continue
        elif op == 4:
            r['B'] = r['B'] ^ r['C']
        elif op == 5:
            output += [combo(r, data) % 8]
        elif op == 6:
            num = r['A']
            den = 2 ** combo(r, data)
            r['B'] = num // den
        elif op == 7:
            num = r['A']
            den = 2 ** combo(r, data)
            r['C'] = num // den
        ip += 2

    return ",".join([str(o) for o in output])

def solution2(r, program):
    target = ",".join([str(o) for o in program])

    # too dumb to figure out a general solution
    # instead, this approach relies on just simulating
    # the operations every cycle in reverse.
    #
    # For my input, I have these operations:
    # 1) b = a % 8
    # 2) b = b ^ 2
    # 3) c = a // (2 ** b)
    # 4) b = b ^ c
    # 5) a = a // (2 ** 3) ==> a set only once every cycle
    # 6) b = b ^ 7
    # 7) print b % 8
    # 8) jump 0 if a != 0
    #
    # Things to note for future self:
    # - always jump to the start of the sequence if A != 0
    # - This implies the final octal digit to A is a 0
    # - A is set at op 5 only once every cycle
    # - op 5 divides A by 8 every cycle, that means A
    # shifts one octal to the right for every cycle.
    # - This leads to important conclusion - A can be
    # reconstituted octal by octal
    # - B and C are dependent on A and are recalculated
    # every cycle, so no need to preserve their values.
    # - So let's simulate going in reverse, and
    # checking that the reconstituted digits of A are correct
    # - Finally, preserve minimum solution

    def f(idx, a):
        if idx == -1:
            tmp = {'A': int(a, 8), 'B': 0, 'C': 0}
            if solution1(tmp, program) == target:
                # triple checking the solution
                # this is not strictly necessary.
                return int(a, 8)
            return float('inf')
        best = float('inf')
        for a_ in range(8):
            # a is passed in as octal string
            # switch to decimal to perform calculations
            str_a =  a + str(a_)  # concat
            a_ = int(str_a, 8)

            # simulate the calculation of b as the
            # specific input requires
            b = (a_ % 8) ^ 2
            c = a_ // (2 ** b)
            b = b ^ c
            b ^= 7

            if (b % 8) == program[idx]:
                best = min(best, f(idx - 1, str_a))
        return best
    return f(len(program) - 1, "0")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    arr = []

    with open(sys.argv[1], "r") as file:
        a = int(file.readline().split(": ")[1])
        b = int(file.readline().split(": ")[1])
        c = int(file.readline().split(": ")[1])
        file.readline()
        program = [int(r) for r in file.readline().split(": ")[1].strip().split(",")]

    registers = {"A": a, "B": b, "C": c}
    print("Solution 1: ", solution1(registers, program))
    print("Solution 2: ", solution2(registers, program))


