#!/usr/bin/env python

import sys
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


EIGHT_NEIGHBORS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def find_numbers(data):
    numbers = []
    for i, line in enumerate(data):
        digits = []
        start = 0
        for j, c in enumerate(line):
            if not c.isnumeric():
                if digits:
                    numbers.append(((i, start), int("".join(digits))))
                    digits = []
                start = j + 1
            else:
                digits.append(c)
        if digits:
            numbers.append(((i, start), int("".join(digits))))
    return numbers


def has_symbol_neighbor(data, i, j):
    for di, dj in EIGHT_NEIGHBORS:
        ii, jj = i + di, j + dj
        if not (0 <= ii < len(data[0])):
            continue
        if not (0 <= jj < len(data[0])):
            continue
        nc = data[ii][jj]
        if nc == ".":
            continue
        if nc.isnumeric():
            continue
        return True
    return False


# PART 1
@measure_time
def solve1(data):
    total = 0
    for (i, start), n in find_numbers(data):
        for j in range(start, start + len(str(n))):
            if has_symbol_neighbor(data, i, j):
                total += n
                break
    return total


# PART 2
@measure_time
def solve2(data):
    numbers = {}
    for (i, start), n in find_numbers(data):
        for j in range(start, start + len(str(n))):
            numbers[i, j] = ((i, start), n)

    total = 0
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c != "*":
                continue
            adj = set()
            for di, dj in EIGHT_NEIGHBORS:
                ii, jj = (i + di, j + dj)
                if (ii, jj) in numbers:
                    adj.add(numbers[ii, jj])
            if len(adj) == 2:
                total += adj.pop()[1] * adj.pop()[1]
    return total


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
