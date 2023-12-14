#!/usr/bin/env python

from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [
        [line for line in block.splitlines()]
        for block in raw_data.strip().split("\n\n")
    ]


def find_lines(block):
    for i in range(1, len(block) + 1):
        prev = block[:i]
        rest = block[i:]
        if len(prev) > len(rest):
            prev = prev[len(prev) - len(rest) :]
        if len(rest) > len(prev):
            rest = rest[: len(prev)]
        # print(prev, rest[::-1])
        if len(prev) == 0:
            return
        if prev == rest[::-1]:
            yield i


def transpose(lines):
    return [[lines[i][j] for i in range(len(lines))] for j in range(len(lines[0]))]


# PART 1
@measure_time
def solve1(data):
    solution = 0
    for block in data:
        rows = block
        cols = transpose(block)
        for c in find_lines(cols):
            solution += c
            break
        for r in find_lines(rows):
            solution += 100 * r
            break
    return solution


def find_lines_with_fix(block):
    for y in range(len(block)):
        for x in range(len(block[0])):
            new_block = [list(line) for line in block]
            new_block[y][x] = "." if new_block[y][x] == "#" else "#"
            for pos in find_lines(new_block):
                yield pos


# PART 2
@measure_time
def solve2(data):
    solution = 0
    for block in data:
        rows = block
        cols = transpose(block)
        c_ref = None
        for c_ref in find_lines(cols):
            pass
        r_ref = None
        for r_ref in find_lines(rows):
            pass
        for c in find_lines_with_fix(cols):
            if c not in [None, c_ref]:
                solution += c
                break
        for r in find_lines_with_fix(rows):
            if r not in [None, r_ref]:
                solution += 100 * r
                break
    return solution


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
