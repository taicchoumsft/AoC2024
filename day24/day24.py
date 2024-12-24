from collections import defaultdict
import sys

def solution1(init, unknown):
    def f(node):
        if node in init:
            return init[node]

        op, l, r = unknown[node]

        l_val = f(l)
        r_val = f(r)
        if op == "XOR":
            return l_val ^ r_val
        elif op == "AND":
            return l_val & r_val
        elif op == "OR":
            return l_val | r_val

    idx = 0
    result = 0
    while (key:=f"z{idx:02d}") in unknown:
        val = f(key)
        result |= (val << idx)
        idx += 1
    return result

def solution2(init, unknown):
    # we have only 3 ops
    # z00: (x00 XOR y00), carry: (x00 AND y00)
    # z01: (x01 XOR y01) XOR (x00 AND y00, the previous carry (pC)), new carry: (pC AND current output) OR (y01 AND x01)
    # Cannot figure out a general solution, so this is a solution based purely on input and observation
    # 1) Notice this is a set of adders stacked together (half adder to start and stop the sequence, full adders in between)
    # 2) Use graphviz or any viz tool to observe the patterns, the pattern thankfully doesn't
    #   change across adder blocks - they are always the same adder repeated over and over again
    #   The swaps also only occur inside the adder blocks.
    #   By coloring the nodes, and then creating a second diagram, we can see the full output and
    #  make the swaps by hand so that all the carry and adder states are propagated properly.

    import graphviz

    dot = graphviz.Digraph()
    for k, (op, l, r) in unknown.items():
        color = "GREEN" # OR
        if op == "XOR":
            color = "RED"
        elif op == "AND":
            color = "BLUE"

        dot.node(k, color=color)
        dot.node(l)
        dot.node(r)
        dot.edge(l, k)
        dot.edge(r, k)

    dot.render('output.gv').replace('\\', '/')

    dot2 = graphviz.Digraph()

    # known swaps for current input
    mp = {
          "qnw": "z15", "z15": "qnw", # correct 90 % confidence
          "ncd": "nfj", "nfj": "ncd",
          "cqr": "z20", "z20": "cqr", # correct (90% confidence)
          "vkg": "z37", "z37": "vkg"} # correct (100%)

    for k, (op, l, r) in unknown.items():
        color = "GREEN" # OR
        if op == "XOR":
            color = "RED"
        elif op == "AND":
            color = "BLUE"

        # only output node needs to change, as per the question
        if k in mp:
            k = mp[k]

        dot2.node(k, color=color)
        dot2.node(l)
        dot2.node(r)
        dot2.edge(l, k)
        dot2.edge(r, k)

    dot2.render('output2.gv').replace('\\', '/')

    return ",".join(sorted(mp.keys()))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    init = defaultdict(int)
    unknown = defaultdict(tuple)

    with open(sys.argv[1], "r") as file:
        for line in file:
            if ":" in line:
                key, val = line.strip().split(": ")
                init[key] = int(val)
            elif "->" in line:
                left, key = line.strip().split(" -> ")
                l, op, r = left.split(" ")
                unknown[key] = (op, l, r)

    print("Solution 1: ", solution1(init, unknown))
    print("Solution 2: ", solution2(init, unknown))


