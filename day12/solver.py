#!/usr/bin/env python

from functools import cache
from itertools import product
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        springs, counts = line.split()
        counts = list(map(int, counts.split(",")))
        out.append((springs, counts))
    return out


# PART 1
@measure_time
def solve1(data):
    return
    solution = 0
    for line, counts in data:
        pos = []
        for i, c in enumerate(line):
            if c == "?":
                pos.append(i)
        line = list(line)
        for chars in product(*[[".", "#"] for _ in pos]):
            for c, i in zip(chars, pos):
                line[i] = c
            found = []
            n = 0
            for c in line:
                if c == "#":
                    n += 1
                if c == "." and n != 0:
                    found.append(n)
                    n = 0
            if n:
                found.append(n)
            if found == counts:
                solution += 1
    return solution


def count_possibilities(line, counts):
    line = list(line)
    total = 0
    def solve():
        nonlocal total
        #print("->", "".join(line))
        count_iter = iter(counts)
        n = 0
        next_count = next(count_iter)
        for i, c in enumerate(line):
            if c == "#":
                n += 1
                continue
            if c == "." and n != 0:
                if n != next_count:
                    return
                try:
                    next_count = next(count_iter)
                except StopIteration:
                    next_count = 0
                n = 0
                continue
            if c != "?":
                continue

            assert c == "?"
            for val in [".", "#"]:
                if val == "#" and n >= next_count:
                    continue
                if val == "." and n != 0 and n < next_count:
                    continue
                line[i] = val
                # print(i)
                # print("".join(line))
                solve()
                #print("rollback")
                line[i] = "?"
            return

        if next_count == n:
            #print("".join(line))
            total += 1

    solve()
    return total

cache = {}

def _total_count(pattern, counts, rest=0):
    total = 0
    for i, c in enumerate(pattern):
        try:
            if c == "#":
                rest += 1
                if rest > counts[0]:
                    return 0
            if c == ".":
                if rest != 0:
                    if rest != counts[0]:
                        return 0
                    else:
                        counts = counts[1:]
                        rest = 0
        except IndexError:
            return 0

        if c == "?":
            for cnew in [".", "#"]:
                total += total_count(cnew+pattern[i+1:], counts, rest)
            return total

    if counts and counts[0] != rest or len(counts) > 1:
        # left over counts
        # -> not possible
        return 0
    else:
        if counts:
            assert counts[0] == rest
        assert len(counts) < 2
        # this is possible
        return 1


def total_count(pattern, counts, rest=0):
    counts = tuple(counts)
    key = (pattern, counts, rest)
    if key in cache:
        #print("hit!")
        return cache[key]
    result = _total_count(*key)
    cache[key] = result
    return result


# PART 2
@measure_time
def solve2(data):
    solution = 0
    for line, counts in data:
        line = "?".join([line]*5)
        counts = counts*5
        total = total_count(line, counts)
        solution += total
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

