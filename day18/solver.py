#!/usr/bin/env python

from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        ins, n, color = line.split()
        n = int(n)
        out.append((ins, n, color))
    return out


DIRECTIONS = {"R": (1, 0), "L": (-1, 0), "D": (0, -1), "U": (0, 1)}


def count_area(instructions):
    area = 0
    trench = 0
    x, y = (0, 0)
    for ins, n in instructions:
        dx, dy = DIRECTIONS[ins]
        x, y = x + n * dx, y + n * dy
        area -= x * n * dy
        trench += n
    return area + trench // 2 + 1


# PART 1
@measure_time
def solve1(data):
    return count_area((ins, n) for ins, n, _ in data)


# PART 2
@measure_time
def solve2(data):
    def instructions():
        for ins, n, color in data:
            color = color[2:-1]
            n = int(color[:-1], 16)
            ins = "RDLU"[int(color[-1])]
            yield ins, n

    return count_area(instructions())


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
