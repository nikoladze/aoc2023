#!/usr/bin/env python

import sys
from functools import cache
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        springs, counts = line.split()
        counts = list(map(int, counts.split(",")))
        out.append((springs, counts))
    return out


@cache
def total_count(pattern, counts, rest=0):
    total = 0
    for i, c in enumerate(pattern):
        try:
            if c == "#":
                rest += 1
                if rest > counts[0]:
                    return 0
            if c == ".":
                if rest != 0:
                    if rest != counts[0]:
                        return 0
                    else:
                        counts = counts[1:]
                        rest = 0
        except IndexError:
            return 0

        if c == "?":
            for cnew in [".", "#"]:
                total += total_count(cnew + pattern[i + 1 :], counts, rest)
            return total

    if counts and counts[0] != rest or len(counts) > 1:
        # left over counts
        # -> not possible
        return 0
    else:
        if counts:
            assert counts[0] == rest
        assert len(counts) < 2
        # this is possible
        return 1


# PART 1
@measure_time
def solve1(data):
    solution = 0
    for line, counts in data:
        solution += total_count(line, tuple(counts))
    return solution


# PART 2
@measure_time
def solve2(data):
    solution = 0
    for line, counts in data:
        line = "?".join([line] * 5)
        counts = counts * 5
        solution += total_count(line, tuple(counts))
    return solution


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
