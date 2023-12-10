#!/usr/bin/env python

from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def move(dx, dy, tile):
    if tile == ".":
        return False
    if tile == "|":
        if dx != 0:
            return False
        return (0, dy)
    if tile == "-":
        if dy != 0:
            return False
        return (dx, 0)
    if tile == "L":
        if dx == -1:
            return (0, 1)
        if dy == -1:
            return (1, 0)
        return False
    if tile == "J":
        if dx == 1:
            return (0, 1)
        if dy == -1:
            return (-1, 0)
        return False
    if tile == "7":
        if dx == 1:
            return (0, -1)
        if dy == 1:
            return (-1, 0)
        return False
    if tile == "F":
        if dy == 1:
            return (1, 0)
        if dx == -1:
            return (0, -1)
        return False
    raise NotImplementedError(f"Unknown tile {tile}")


# PART 1
@measure_time
def solve1(data):
    def find_start():
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile == "S":
                    return x, y

    x, y = find_start()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        tile = data[y - dy][x + dx]
        if new := move(dx, dy, tile):
            x, y = x + dx, y - dy
            break
    dx, dy = new
    steps = 1
    while True:
        x, y = x + dx, y - dy
        tile = data[y][x]
        if tile == "S":
            break
        dx, dy = move(dx, dy, tile)
        steps += 1
    return steps // 2 + 1


def leftright(dx, dy, tile):
    if tile == "|":
        # l|r
        l, r = ((-1, 0),), ((1, 0),)
        return (l, r) if dy == 1 else (r, l)
    if tile == "-":
        # l
        # -
        # r
        l, r = ((0, 1),), ((0, -1),)
        return (l, r) if dx == 1 else (r, l)
    if tile == "L":
        # lL
        # ll
        l, r = ((0, -1), (-1, -1), (-1, 0)), ()
        return (l, r) if dx == -1 else (r, l)
    if tile == "J":
        # Jr
        # rr
        l, r = (), ((-1, 0), (1, -1), (1, 0))
        return (l, r) if dx == 1 else (r, l)
    if tile == "7":
        # rr
        # 7r
        l, r = (), ((1, 0), (1, 1), (0, 1))
        return (l, r) if dy == 1 else (r, l)
    if tile == "F":
        # ll
        # lF
        l, r = ((-1, 0), (-1, 1), (0, 1)), ()
        return (l, r) if dy == 1 else (r, l)
    raise NotImplementedError(f"Unknown tile {tile}")


# PART 2
@measure_time
def solve2(data, start_tile="L"):
    def find_start():
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile == "S":
                    return x, y

    on_path = set()
    x, y = find_start()
    on_path.add((x, y))

    def first_move(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            tile = data[y - dy][x + dx]
            if move(dx, dy, tile):
                return dx, dy

    # fill path set
    dx, dy = first_move(x, y)
    while True:
        x, y = x + dx, y - dy
        on_path.add((x, y))
        tile = data[y][x]
        if tile == "S":
            break
        dx, dy = move(dx, dy, tile)

    # find adjacent left and right tiles
    # TODO: what is left and right of start?
    x, y = find_start()
    dx, dy = first_move(x, y)
    lefts, rights = set(), set()
    do_break = False
    while True:
        x, y = x + dx, y - dy
        tile = data[y][x]
        if tile == "S":
            tile = start_tile
            do_break = True
        l, r = leftright(dx, dy, tile)
        for lr, dst in [(l, lefts), (r, rights)]:
            for dxx, dyy in lr:
                coords = (x + dxx, y - dyy)
                if coords not in on_path:
                    dst.add(coords)
        if do_break:
            break
        dx, dy = move(dx, dy, tile)

    #print(lefts, rights)

    # find everything connected to left and right
    def expand(coords):
        def _expand(x, y):
            if (x, y) in coords:
                return
            if (x, y) in on_path:
                return
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                xx, yy = x + dx, y - dy
                if (xx, yy) in coords:
                    continue
                if (xx, yy) in on_path:
                    continue
                _expand(xx, yy)

        for x, y in coords:
            _expand(x, y)

    expand(lefts)
    expand(rights)

    # decide where outside is ;)
    # -> for now just use smaller number as inside :P

    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            coord = (x, y)
            if coord in lefts:
                print("l", end="")
            elif coord in rights:
                print("r", end="")
            else:
                print(tile, end="")
        print("")
    print()

    #return len(on_path) // 2
    return min(len(lefts), len(rights))


# if __name__ == "__main__":
if True:
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
