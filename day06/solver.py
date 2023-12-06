#!/usr/bin/env python

import sys
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    times, distances = [
        list(map(int, line.split(":")[1].strip().split()))
        for line in raw_data.strip().splitlines()
    ]
    return times, distances


# PART 1
@measure_time
def solve1(data):
    times, distances = data
    solution = 1
    for time, record in zip(times, distances):
        n = 0
        for hold in range(time):
            v = hold
            x = v * (time - hold)
            if x > record:
                n += 1
        solution *= n
    return solution


# PART 2
@measure_time
def solve2(data):
    time, record = [int("".join(map(str, x))) for x in data]
    n = 0
    for hold in range(time):
        v = hold
        x = v * (time - hold)
        if x > record:
            n += 1
    return n


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
