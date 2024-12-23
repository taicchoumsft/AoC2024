from collections import defaultdict
import sys



def solution1(adj_list):
    soln = set()
    def dfs(node, depth, path):
        if depth == 0 and node == path[0]:
            soln.add(tuple(sorted(path[:-1])))
            return True
        if depth == 0: return False

        for nbr in adj_list[node]:
            dfs(nbr, depth - 1, path + [nbr])
        return False

    for n in adj_list.keys():
        if n.startswith("t"):
            dfs(n, 3, [n])

    return len(soln)

def solution2(adj_list):
    soln = set()

    # reduces to finding the cliques of the graph
    def bron_kerbosch(R, P, X, graph):
        if not P and not X:
            soln.add(tuple(sorted(R)))
            return
        for v in P.copy():
            bron_kerbosch(R.union({v}), P.intersection(graph[v]), X.intersection(graph[v]), graph)
            P.remove(v)
            X.add(v)

    bron_kerbosch(set(), set(adj_list.keys()), set(), adj_list)

    longest = max(soln, key = lambda x: len(x))
    return ",".join(longest)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    edges = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            edges += [line.strip().split("-")]

    adj_list = defaultdict(list)
    for e1, e2 in edges:
        adj_list[e1] += [e2]
        adj_list[e2] += [e1]


    print("Solution 1: ", solution1(adj_list))
    print("Solution 2: ", solution2(adj_list))


