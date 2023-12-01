#!/usr/bin/env python

import sys
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


# PART 1
@measure_time
def solve1(data):
    solution = 0
    for line in data:
        digs = []
        for c in line:
            if c.isnumeric():
                digs.append(c)
        solution += int(digs[0] + digs[-1])
    return solution


NAMES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def parse_line(line):
    digs = []
    for i, c in enumerate(line):
        if c.isnumeric():
            digs.append((i, c))
    for i, name in enumerate(NAMES, start=1):
        sub = line
        pos = 0
        while (subpos := sub.find(name)) != -1:
            pos += subpos
            digs.append((pos, str(i)))
            sub = line[pos + len(name) :]
            pos += len(name)
    digs.sort(key=lambda x: x[0])
    return int(digs[0][1] + digs[-1][1])


# PART 2
@measure_time
def solve2(data):
    return sum(map(parse_line, data))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
