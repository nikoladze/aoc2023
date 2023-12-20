#!/usr/bin/env python

import heapq
from collections import deque
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


testpath = """
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
""".strip().splitlines()


@measure_time
def solve1(data):
    #q = deque([(0, 0, 0, 0, 0, 0)])
    q = [(0, 0, 0, 0, 0, 0, 0)]
    min_cost = {(0, 0, 0): {(0, 0): 0}}
    history = {} # tuple(pos, cost) -> tuple(pos, cost) # maps to previous
    maxi = 0
    maxj = 0
    maxij = 0
    while q:
        #n, cost, di, dj, i, j = q.popleft()
        heur, cost, n, di, dj, i, j = heapq.heappop(q)

        # DEBUG
        if i > maxi:
            maxi = i
            print(i, j)
        if j > maxj:
            maxj = j
            print(i, j)
        if i + j > maxij:
            maxij = i + j
            print(i, j)

        min_cost[di, dj, n][i, j] = cost

        for new_di, new_dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if (new_di * di < 0) or (new_dj * dj < 0):
                # no 180 degree turns!
                continue
            new_n = 0
            if (new_di, new_dj) == (di, dj):
                if n >= 2:
                    # already came here with 3 steps in same direction
                    continue
                new_n = n + 1
            new_i, new_j = i + new_di, j + new_dj
            if not (0 <= new_i < len(data)):
                continue
            if not (0 <= new_j < len(data[0])):
                continue

            # DEBUG
            # if testpath[new_i][new_j].isnumeric():
            #     continue

            new_cost = cost + int(data[new_i][new_j])

            new_heur = new_cost + abs(i - j)

            # if abs(i - j) > 10:
            #     # fun heuristic :P
            #     continue

            min_cost.setdefault((new_di, new_dj, new_n), {})
            if (new_i, new_j) in min_cost[new_di, new_dj, new_n]:
                if min_cost[new_di, new_dj, new_n][new_i, new_j] <= new_cost:
                    continue
            else:
                min_cost[new_di, new_dj, new_n][new_i, new_j] = new_cost

            # if min_cost.setdefault((new_di, new_dj, new_n), {}).setdefault((new_i, new_j), new_cost) <= new_cost:
            #     continue

            # if new_cost > (new_i + new_j) * 9:
            #     # not sure if it helps anything though
            #     continue  # should not happen, i think (i can go zigzag)

            # history[new_n, new_cost, new_di, new_dj, new_i, new_j] = (n, cost, di, dj, i, j)

            #q.append((new_n, new_cost, new_di, new_dj, new_i, new_j))
            heapq.heappush(q, (new_heur, new_cost, new_n, new_di, new_dj, new_i, new_j))

    MAXCOST = 1 << 64

    # i, j = len(data) - 1, len(data[0]) - 1
    # key = min(((n, cost_dict.get((i, j), MAXCOST), di, dj, i, j) for (di, dj, n), cost_dict in min_cost.items()), key=lambda x: x[1])

    # print("history")
    # n, cost, di, dj, i, j = key
    # while (i, j) != (0, 0):
    #     print(i, j, di, dj)
    #     n, cost, di, dj, i, j = history[n, cost, di, dj, i, j]

    return min(
        c.get((len(data) - 1, len(data[0]) - 1), MAXCOST) for c in min_cost.values()
    )


# PART 2
@measure_time
def solve2(data):
    #q = deque([(0, 0, 0, 0, 0, 0)])
    q = [(0, 0, 0, 0, 0, 0, 0)]
    min_cost = {(0, 0, 0): {(0, 0): 0}}
    history = {} # tuple(pos, cost) -> tuple(pos, cost) # maps to previous
    maxi = 0
    maxj = 0
    maxij = 0
    while q:
        #n, cost, di, dj, i, j = q.popleft()
        heur, cost, n, di, dj, i, j = heapq.heappop(q)

        # DEBUG
        if i > maxi:
            maxi = i
            print(i, j)
        if j > maxj:
            maxj = j
            print(i, j)
        if i + j > maxij:
            maxij = i + j
            print(i, j)

        min_cost[di, dj, n][i, j] = cost
        #print(di, dj, n, i, j, cost, min_cost)

        for new_di, new_dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            new_n = 0
            if (di, dj) != (0, 0):
                if (new_di * di < 0) or (new_dj * dj < 0):
                    # no 180 degree turns!
                    continue
                if (new_di, new_dj) != (di, dj) and n < 3:
                    # nope, need to move longer in that direction
                    #print("need to move longer")
                    continue
                if (new_di, new_dj) == (di, dj):
                    if n >= 9:
                        #print("already too long")
                        # already came here with 10 steps in same direction
                        continue
                    new_n = n + 1
                    #print(f"{new_n=}")
            new_i, new_j = i + new_di, j + new_dj
            if (new_i, new_j) == (len(data) - 1, len(data[0]) - 1) and n < 3:
                #print("don't stop me now")
                # don't stop me now!
                continue
            if not (0 <= new_i < len(data)):
                continue
            if not (0 <= new_j < len(data[0])):
                continue

            #print("try this")
            # DEBUG
            # if testpath[new_i][new_j].isnumeric():
            #     continue

            new_cost = cost + int(data[new_i][new_j])

            new_heur = new_cost + abs(i - j)

            # if abs(i - j) > 10:
            #     # fun heuristic :P
            #     continue

            min_cost.setdefault((new_di, new_dj, new_n), {})
            if (new_i, new_j) in min_cost[new_di, new_dj, new_n]:
                if min_cost[new_di, new_dj, new_n][new_i, new_j] <= new_cost:
                    continue
            else:
                min_cost[new_di, new_dj, new_n][new_i, new_j] = new_cost

            # if min_cost.setdefault((new_di, new_dj, new_n), {}).setdefault((new_i, new_j), new_cost) <= new_cost:
            #     continue

            # if new_cost > (new_i + new_j) * 9:
            #     # not sure if it helps anything though
            #     continue  # should not happen, i think (i can go zigzag)

            # history[new_n, new_cost, new_di, new_dj, new_i, new_j] = (n, cost, di, dj, i, j)

            #q.append((new_n, new_cost, new_di, new_dj, new_i, new_j))
            heapq.heappush(q, (new_heur, new_cost, new_n, new_di, new_dj, new_i, new_j))

    MAXCOST = 1 << 64

    # i, j = len(data) - 1, len(data[0]) - 1
    # key = min(((n, cost_dict.get((i, j), MAXCOST), di, dj, i, j) for (di, dj, n), cost_dict in min_cost.items()), key=lambda x: x[1])

    # print("history")
    # n, cost, di, dj, i, j = key
    # while (i, j) != (0, 0):
    #     print(i, j, di, dj)
    #     n, cost, di, dj, i, j = history[n, cost, di, dj, i, j]

    #print(min_cost)
    return min(
        c.get((len(data) - 1, len(data[0]) - 1), MAXCOST) for c in min_cost.values()
    )


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
