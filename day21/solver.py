#!/usr/bin/env python

from collections import deque
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


# PART 1
@measure_time
def solve1(data, steps=64):
    solution = 0
    def get_start():
        for i, row in enumerate(data):
            for j, c in enumerate(row):
                if c == "S":
                    return i, j
    i, j = get_start()
    n = 0
    q = deque([(i, j, n)])
    seen = set() # not valid here?
    finals = set()
    while q:
        i, j, n = q.popleft()
        print(n)
        if n == steps:
            finals.add((i, j))
            continue
        if (i, j, n) in seen:
             continue
        seen.add((i, j, n))
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = (i + di), (j + dj)
            if not (0 <= new_i < len(data)):
                continue
            if not (0 <= new_j < len(data[0])):
                continue
            if data[new_i][new_j] not in ".S":
                continue
            new_n = n + 1
            # if (new_i, new_j) in seen:
            #     continue
            if new_n > steps:
                assert False
            q.append((new_i, new_j, new_n))

    # print()
    # for i, row in enumerate(data):
    #     for j, c in enumerate(row):
    #         if (i, j) in finals:
    #             print("O", end="")
    #         else:
    #             print(c, end="")
    #     print()

    return len(finals)


# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

