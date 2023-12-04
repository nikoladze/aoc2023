#!/usr/bin/env python

import sys
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        header, content = line.split(": ")
        winning, have = content.split(" | ")
        winning, have = [[int(xi) for xi in x.strip().split()] for x in [winning, have]]
        out.append((header, winning, have))
    return out


# PART 1
@measure_time
def solve1(data):
    total = 0
    for header, winning, have in data:
        n = len(set(winning).intersection(set(have))) - 1
        if n >= 0:
            total += 2**n
    return total


# PART 2
@measure_time
def solve2(data):
    copies = {}
    total = 0
    for header, winning, have in data:
        cardnum = int(header.split()[1])
        copies.setdefault(cardnum, 1)
        n = len(set(winning).intersection(set(have)))
        for other in range(cardnum + 1, cardnum + 1 + n):
            copies.setdefault(other, 1)
            copies[other] += copies[cardnum]
    return sum(copies.values())


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
