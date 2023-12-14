#!/usr/bin/env python

from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def find_rocks(data, symbol="O"):
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == symbol:
                yield i, j


def roll(grid, rocks, di, dj):
    if di != 0:
        rocks = sorted(rocks, key=lambda x: x[0])
    elif dj != 0:
        rocks = sorted(rocks, key=lambda x: x[1])
    if di > 0 or dj > 0:
        rocks = reversed(rocks)
    for i, j in rocks:
        while True:
            new_i, new_j = i + di, j + dj
            if new_i < 0 or new_j < 0:
                break
            if new_i >= len(grid) or new_j >= len(grid[0]):
                break
            if grid[new_i][new_j] != ".":
                break
            grid[i][j] = "."
            grid[new_i][new_j] = "O"
            i, j = new_i, new_j


# PART 1
@measure_time
def solve1(data):
    grid = list(map(list, data))
    roll(grid, find_rocks(grid), di=-1, dj=0)
    return sum(len(grid) - i for i, _ in find_rocks(grid))


def print_grid(grid):
    print()
    print("\n".join(["".join(_line) for _line in grid]))


def roll_cycle(grid):
    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        roll(grid, find_rocks(grid), di=di, dj=dj)


# PART 2
@measure_time
def solve2(data, ncycles=1000000000):
    grid = list(map(list, data))
    seen = {}
    for cycle in range(ncycles):
        rocks = frozenset(find_rocks(grid))
        if rocks in seen:
            break
        seen[rocks] = cycle
        roll_cycle(grid)
    loop_offset = seen[rocks]
    loop_len = cycle - loop_offset
    n_loops = ncycles // loop_len
    n_todo = loop_offset + (ncycles - loop_offset) % loop_len
    grid = list(map(list, data))
    for cycle in range(n_todo):
        roll_cycle(grid)
    return sum(len(grid) - i for i, _ in find_rocks(grid))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
