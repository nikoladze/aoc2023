#!/usr/bin/env python

from itertools import product
from collections import defaultdict
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        start, end = line.split("~")
        start, end = [list(map(int, x.split(","))) for x in [start, end]]
        out.append((start, end))
    return out


def let_fall(data):
    brick_for_coord = {}
    coords_for_brick = defaultdict(list)
    for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(data):
        for coord in product(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1)):
            brick_for_coord[coord] = i
            coords_for_brick[i].append(coord)

    while True:
        any_move = False
        for i, coords in sorted(
            list(map(list, coords_for_brick.items())),
            key=lambda x: sum(z for _, _, z in x[1]),
        ):
            for x, y, z in coords:
                if z == 1:
                    # reached bottom
                    break
                if brick_for_coord.get((x, y, z - 1), i) != i:
                    # hit other brick
                    break
            else:
                coords = list(coords)
                any_move = True
                coords_for_brick[i].clear()
                for x, y, z in coords:
                    del brick_for_coord[x, y, z]
                    coord = x, y, z - 1
                    brick_for_coord[coord] = i
                    coords_for_brick[i].append(coord)
        if not any_move:
            return brick_for_coord, coords_for_brick


def get_supporting_structure(brick_for_coord, coords_for_brick):
    supporting = defaultdict(set)
    supported_by = defaultdict(set)
    for i, coords in coords_for_brick.items():
        for x, y, z in coords:
            if (j := brick_for_coord.get((x, y, z + 1), i)) != i:
                supporting[i].add(j)
                supported_by[j].add(i)
    return supporting, supported_by


# PART 1
@measure_time
def solve1(data):
    brick_for_coord, coords_for_brick = let_fall(data)
    supporting, supported_by = get_supporting_structure(
        brick_for_coord, coords_for_brick
    )
    return sum(
        all(len(supported_by[j]) > 1 for j in supporting[i]) for i in coords_for_brick
    )


# PART 2
@measure_time
def solve2(data):
    supporting, supported_by = get_supporting_structure(*let_fall(data))

    def count_supporting(i):
        total = 0
        disintegrated = set()

        def count(i):
            nonlocal total
            disintegrated.add(i)
            for j in supporting[i]:
                if any(ji not in disintegrated for ji in supported_by[j]):
                    continue
                total += 1
                count(j)

        count(i)
        return total

    return sum(count_supporting(i) for i in list(supporting.keys()))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
