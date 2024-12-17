import sys
from collections import defaultdict

# problem simpler than I made it at first.
# the most important sentence is "within each update, the ordering rules that involve missing page numbers are not used."
# instead, filter out the needed edges first. Then build the solution on the
# smaller graphs

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please provide input file")

    mp = defaultdict(set)
    arr = []
    ingress = defaultdict(int)
    all_nodes = set()

    with open(sys.argv[1], "r") as file:
        for line in file:
            if line.find("|") > -1:
                a, b = line.split("|")
                mp[int(a)].add(int(b))
                ingress[int(b)] += 1
                all_nodes.add(int(a))
                all_nodes.add(int(b))
            elif line.find(",") > -1:
                row = [int(a) for a in line.split(",")]
                arr += [row]

    def recurse(row, idx, seen):
        if idx == len(row) - 1:
            return True

        if row[idx] in seen: return False
        seen.add(row[idx])

        res = False
        for nbr in mp[row[idx]]:
            if idx + 1 < len(row) and nbr == row[idx + 1]:
                res |= recurse(row, idx + 1, seen)

        return res

    total1 = 0
    bad_rows = []
    for row in arr:
        if recurse(row, 0, set()):
            middle = len(row) // 2
            total1 += row[middle]
        else:
            bad_rows += [row]

    print("Solution 1: ", total1)

    # try topo sorting the thing
    # as we finish the ordering, just filter the final result?
    # q = []
    # ordering = []

    # for i in all_nodes:
    #     if ingress[i] == 0:
    #         q.append(i)

    # while q:
    #     node = q.pop(0)
    #     ordering.append(node)

    #     for nbr in mp[node]:
    #         ingress[nbr] -= 1
    #         if ingress[nbr] == 0:
    #             q.append(nbr)

    # print("Ordering: ", ordering)
    # total2 = 0
    # for row in bad_rows:
    #     print("bad row: ", row)
    #     st = set(row)
    #     filtered = []
    #     for o in ordering:
    #         if o in st:
    #             filtered += [o]
    #     total2 += filtered[len(filtered) // 2]

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

    def backtrack(node, nodes, cur, result, seen = set()):
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

        for nbr in mp[node]:
            if nbr not in nodes: continue
            if backtrack(nbr, nodes, cur, result, seen):
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
            tmp = set(row)
            if backtrack(i, tmp, [], result, set()):
                for r in result:
                    if recurse(r, 0, set()):
                        print("found ordering: ", r)
                        total2 += r[len(r) // 2]
                        break

    print("Solution 2: ", total2)


