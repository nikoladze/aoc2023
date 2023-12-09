#!/usr/bin/env python

import sys
from collections import deque
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [list(map(int, line.split())) for line in raw_data.strip().splitlines()]


# PART 1
@measure_time
def solve1(data):
    solution = 0
    for history in data:
        seqs = [history]
        while not all(val == 0 for val in seqs[-1]):
            seq = seqs[-1]
            seqs.append([r - l for l, r in zip(seq, seq[1:])])
        seqs[-1].append(0)
        for i in reversed(range(len(seqs) - 1)):
            seqs[i].append(seqs[i][-1] + seqs[i + 1][-1])
        solution += seqs[0][-1]
    return solution



# PART 2
@measure_time
def solve2(data):
    solution = 0
    for history in data:
        seqs = [deque(history)]
        while not all(val == 0 for val in seqs[-1]):
            seq = seqs[-1]
            seqs.append(deque([r - l for l, r in zip(list(seq), list(seq)[1:])]))
        seqs[-1].appendleft(0)
        for i in reversed(range(len(seqs) - 1)):
            seqs[i].appendleft(seqs[i][0] - seqs[i + 1][0])
        solution += seqs[0][0]
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

