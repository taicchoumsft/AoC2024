import sys
from collections import defaultdict

# problem simpler than I made it at first.
# the most important sentence is "within each update, the ordering rules that involve missing page numbers are not used."
# instead, filter out the needed edges first. Then build the solution on the
# smaller graphs

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    all_edges = []

    arr = []
    ingress = defaultdict(int)
    all_nodes = set()

    with open(sys.argv[1], "r") as file:
        for line in file:
            if line.find("|") > -1:
                a, b = [int(l) for l in line.split("|")]
                all_edges.append((a, b))
            elif line.find(",") > -1:
                row = [int(a) for a in line.split(",")]
                arr += [row]

    def filter(nodes, all_nodes):
        return [(e1, e2) for e1, e2 in all_nodes if (nodes[0] == e1 and nodes[1] == e2) or (nodes[0] == e2 and nodes[1] == e1)]

    def create_graph(edges):
        adj_list = defaultdict(list)
        for e1, e2 in edges:
            adj_list[e1].append(e2)
        return adj_list

    def recurse(adj_list, row, idx, seen):
        if idx == len(row) - 1:
            return True

        if row[idx] in seen: return False
        seen.add(row[idx])

        res = False
        for nbr in adj_list[row[idx]]:
            if idx + 1 < len(row) and nbr == row[idx + 1]:
                res |= recurse(adj_list, row, idx + 1, seen)
        return res

    total1 = 0
    bad_rows = []
    adj_list = create_graph(all_edges)
    for row in arr:
        if recurse(adj_list, row, 0, set()):
            middle = len(row) // 2
            total1 += row[middle]
        else:
            bad_rows += [row]
    print("Solution 1: ", total1)

    # try topo sorting the thing
    # as we finish the ordering, just filter the final result?
    def topo_sort(adj_list, row):
        q = []
        ordering = []

        for i in row:
            if ingress[i] == 0:
                q.append(i)

        while q:
            node = q.pop(0)
            ordering.append(node)

            for nbr in adj_list[node]:
                ingress[nbr] -= 1
                if ingress[nbr] == 0:
                    q.append(nbr)

        filtered = []
        st = set(row)
        for o in ordering:
            if o in st:
                filtered += [o]
        return filtered

    def backtrack(adj_list, node, nodes, cur, result, seen = set()):
        #print(cur, seen, nodes)
        if len(cur) == len(nodes):
            result += [cur[:]]
            return True

        if node in seen:
            return False
        seen.add(node)

        removed = False
        if node in nodes:
            removed = True
            cur += [node]

        if len(cur) == len(nodes):
            result += [cur[:]]
            return True

        for nbr in adj_list[node]:
            if nbr not in nodes: continue
            if backtrack(adj_list, nbr, nodes, cur, result, seen):
                return True

        seen.remove(node)

        if removed:
            cur.pop()
        return False

    total2 = 0
    for row in bad_rows:
        result = []
        print("testing: ", row)
        for i in row:
            adj_list = create_graph(filter(row, all_nodes))
            tmp = set(row)
            if backtrack(adj_list, i, tmp, [], result, set()):
                for r in result:
                    if recurse(r, 0, set()):
                        print("found ordering: ", r)
                        total2 += r[len(r) // 2]
                        break


    # def def_invalid(perm):
    #     for p1, p2 in zip(perm[:-1], perm[1:]):
    #         if p1 in mp[p2]:
    #             return False
    #     return True

    # total2 = 0
    # for row in bad_rows:
    #     for perm in permutations(row):
    #         if def_invalid(perm): continue
    #         if recurse(perm, 0, set()):
    #             print("perm worked", perm)
    #             total2 += perm[len(perm) // 2]
    #             break

    # def backtrack(node, nodes, cur, result, seen = set()):
    #     #print(cur, seen, nodes)
    #     if len(cur) == len(nodes):
    #         result += [cur[:]]
    #         return True

    #     if node in seen:
    #         return False
    #     seen.add(node)

    #     removed = False
    #     if node in nodes:
    #         removed = True
    #         cur += [node]

    #     if len(cur) == len(nodes):
    #         result += [cur[:]]
    #         return True

    #     for nbr in mp[node]:
    #         if nbr not in nodes: continue
    #         if backtrack(nbr, nodes, cur, result, seen):
    #             return True

    #     seen.remove(node)

    #     if removed:
    #         cur.pop()
    #     return False

    # total2 = 0
    # for row in bad_rows:
    #     result = []
    #     print("testing: ", row)
    #     for i in row:
    #         tmp = set(row)
    #         if backtrack(i, tmp, [], result, set()):
    #             for r in result:
    #                 if recurse(r, 0, set()):
    #                     print("found ordering: ", r)
    #                     total2 += r[len(r) // 2]
    #                     break

    print("Solution 2: ", total2)


