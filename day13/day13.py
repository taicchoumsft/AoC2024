import sys
import re

# bruteforce
def solution1(A, B, Prize):
    total = 0
    for a, b, prize in zip(A, B, Prize):

        best = 0
        for i in range(100):
            for j in range(100):
                x_a = a[0] * i
                x_b = b[0] * j
                y_a = a[1] * i
                y_b = b[1] * j
                x = x_a + x_b
                y = y_a + y_b
                if x == prize[0] and y == prize[1]:
                    best = i * 3 + j
        total += best
    return total

def solution2(A, B, Prize, to_add = 0):
    # ultimately, this is a system of 2 diophantine equations
    # that needs a minimum solution
    # e.g. first sample,
    # 1) 94x + 22y = 8400
    # 2) 34x + 67y = 5400
    # constrained by (a + b) should be as small as possible
    # to solve manually:
    # Let:
    # a1.x + b1.y = p0
    # a2.x + b2.y = p1
    # Then
    # y = (a2.p0 - p1.a1) / (a2.b1 - b2.a1)
    # x = (p0 - b1.y) / a1
    # there is only 1 solution ever for this system, but could be non
    # integer solution, which must filter out
    total = 0

    for a, b, p in zip(A, B, Prize):
        p0 = p[0] + to_add
        p1 = p[1] + to_add
        y = (a[1] * p0 - p1 * a[0])
        y_b = (a[1] * b[0] - b[1] * a[0])
        if y % y_b == 0:
            y = y // y_b
            x = (p0 - b[0] * y)
            x_b = a[0]
            if x % x_b == 0:
                x = x // x_b
                total += x * 3 + y
    return total
    # also a sympy version here, which I started with
    # from sympy import symbols, Eq, solve
    # to_add = 10000000000000
    # total = 0
    # for a, b, prize in zip(A, B, Prize):
    #     x, y = symbols('x y', real = True, integer=True)
    #     eq1 = Eq(a[0] * x + b[0] * y, prize[0] + to_add)
    #     eq2 = Eq(a[1] * x + b[1] * y, prize[1] + to_add)
    #     solutions = solve((eq1, eq2), (x, y), dict=True)
    #     # Find the solution where a + b is minimal, if more than 1 solution exists
    #     min_sum = float('inf')
    #     min_solution = None
    #     for sol in solutions:
    #         current_sum = 3 * sol[x] + sol[y]
    #         if current_sum < min_sum:
    #             min_sum = current_sum
    #             min_solution = sol
    #     if min_solution:
    #         total += min_sum
    # return total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    a = []
    b = []
    prize = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            if line.startswith("Button A"):
                m = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line)
                a.append((int(m.group(1)), int(m.group(2))))
            elif line.startswith("Button B"):
                m = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line)
                b.append((int(m.group(1)), int(m.group(2))))
            elif line.startswith("Prize"):
                m = re.match(r"Prize: X\=(\d+), Y\=(\d+)", line)
                prize.append((int(m.group(1)), int(m.group(2))))

    print("Solution 1: ", solution2(a, b, prize))
    print("Solution 2: ", solution2(a, b, prize, 10000000000000))


