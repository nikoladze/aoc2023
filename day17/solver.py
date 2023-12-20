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


def search_min_cost(data, min_steps, max_steps):
    bottom_right = len(data) - 1, len(data[0]) - 1
    q = [(0, 0, 0, 0, 0, 0)]
    min_cost = {(0, 0, 0): {(0, 0): 0}}
    while q:
        cost, n, di, dj, i, j = heapq.heappop(q)
        for new_di, new_dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            new_n = 0
            if (di, dj) != (0, 0):
                if (new_di * di < 0) or (new_dj * dj < 0):
                    # no 180 degree turns
                    continue
                if (new_di, new_dj) != (di, dj) and n < (min_steps - 1):
                    # nope, need to move longer in that direction
                    continue
                if (new_di, new_dj) == (di, dj):
                    if n >= (max_steps - 1):
                        # already came here with too many steps in same direction
                        continue
                    new_n = n + 1
            new_i, new_j = i + new_di, j + new_dj
            if (new_i, new_j) == bottom_right and n < (min_steps - 1):
                # don't, stop, me, noooow!
                continue
            if not (0 <= new_i < len(data)):
                continue
            if not (0 <= new_j < len(data[0])):
                continue

            new_cost = cost + int(data[new_i][new_j])
            this_min_cost = min_cost.setdefault((new_di, new_dj, new_n), {})
            try:
                if this_min_cost[new_i, new_j] <= new_cost:
                    continue
            except KeyError:
                pass
            min_cost[new_di, new_dj, new_n][new_i, new_j] = new_cost

            heapq.heappush(q, (new_cost, new_n, new_di, new_dj, new_i, new_j))

    return min(
        filter(
            lambda x: x is not None,
            (c.get(bottom_right, None) for c in min_cost.values()),
        )
    )


@measure_time
def solve1(data):
    return search_min_cost(data, min_steps=1, max_steps=3)


# PART 2
@measure_time
def solve2(data):
    return search_min_cost(data, min_steps=4, max_steps=10)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
