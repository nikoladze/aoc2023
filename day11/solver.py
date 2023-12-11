#!/usr/bin/env python

from itertools import combinations
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [line for line in raw_data.strip().splitlines()]


def solve(data, expansion):
    coords = set()
    actual_i = 0
    for i, row in enumerate(data):
        actual_j = 0
        for j, field in enumerate(row):
            if field == "#":
                coords.add((actual_i, actual_j))
            if not any(data[k][j] == "#" for k in range(len(data))):
                actual_j += expansion
            else:
                actual_j += 1
        if not any(field == "#" for field in row):
            actual_i += expansion
        else:
            actual_i += 1

    return sum(
        abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) for c1, c2 in combinations(coords, 2)
    )


# PART 1
@measure_time
def solve1(data):
    return solve(data, 2)


# PART 2
@measure_time
def solve2(data):
    return solve(data, 1000000)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
