#!/usr/bin/env python

import sys
from functools import reduce
from operator import mul
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    games = {}
    for line in raw_data.strip().splitlines():
        id_str, rest = line.split(": ")
        game_id = int(id_str.split()[1])
        for cube_set_str in rest.split("; "):
            cube_set = {}
            for cube_str in cube_set_str.split(", "):
                n, color = cube_str.split()
                n = int(n)
                cube_set[color] = n
            games.setdefault(game_id, []).append(cube_set)
    return games


def check(cube_sets, available):
    for cube_set in cube_sets:
        for key in available:
            if cube_set.get(key, 0) > available[key]:
                return False
    return True


# PART 1
@measure_time
def solve1(data):
    available = {"red": 12, "green": 13, "blue": 14}
    return sum(
        game_id for game_id, cube_sets in data.items() if check(cube_sets, available)
    )


# PART 2
@measure_time
def solve2(data):
    out = 0
    for game_id, cube_sets in data.items():
        out += reduce(
            mul,
            [
                max(cube_set.get(key, 1) for cube_set in cube_sets)
                for key in ["red", "green", "blue"]
            ],
        )
    return out


# if __name__ == "__main__":
data = parse(open(Path(__file__).parent / "input.txt").read())
print("Part 1: {}".format(solve1(data)))
print("Part 2: {}".format(solve2(data)))

print("\nTime taken:")
for func, time in measure_time.times:
    print(f"{func:8}{time}s")
print("----------------")
print("total   {}s".format(sum(t for _, t in measure_time.times)))
