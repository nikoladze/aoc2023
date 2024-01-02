#!/usr/bin/env python

from itertools import product
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def print_grid(grid, seen):
    grid = list(map(list, grid))
    seen = set((i, j) for i, j, di, dj in seen)
    for i, j in seen:
        grid[i][j] = "#"
    print("\n".join(["".join(_line) for _line in grid]))


def energize(grid, start_xv):
    stack = [start_xv]
    seen = set()
    while stack:
        xv = stack.pop()
        if xv in seen:
            continue
        i, j, di, dj = xv
        if 0 <= i < len(grid) and 0 <= j < len(
            grid[0]
        ):  # don't add start point outside
            seen.add(xv)
        while True:
            i, j = (i + di, j + dj)
            if not (0 <= i < len(grid)):
                break
            if not (0 <= j < len(grid[0])):
                break
            seen.add((i, j, di, dj))
            c = grid[i][j]
            if c == ".":
                continue
            elif c == "\\":
                di, dj = dj, di
                continue
            elif c == "/":
                di, dj = -dj, -di
                continue
            elif c == "-":
                if dj != 0:
                    continue
                assert di != 0
                stack.append((i, j, 0, -1))
                stack.append((i, j, 0, 1))
                break
            elif c == "|":
                if di != 0:
                    continue
                assert dj != 0
                stack.append((i, j, -1, 0))
                stack.append((i, j, 1, 0))
                break
            else:
                assert False
    return len(set((i, j) for i, j, di, dj in seen))


# PART 1
@measure_time
def solve1(data):
    grid = list(map(list, data))
    return energize(data, (0, -1, 0, 1))


# PART 2
@measure_time
def solve2(data):
    nrows = len(data)
    ncols = len(data[0])
    values = []
    for di, dj, irange, jrange in [
        (1, 0, [-1], range(ncols)),  # top row downwards
        (-1, 0, [nrows], range(ncols)),  # bottom row upwards
        (0, 1, range(nrows), [-1]),  # left column to right
        (0, -1, range(nrows), [ncols]),  # right column to left
    ]:
        for i, j in product(irange, jrange):
            values.append(energize(data, (i, j, di, dj)))
    return max(values)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
