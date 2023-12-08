#!/usr/bin/env python

import math
import sys
from itertools import cycle
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    sequence, network = raw_data.strip().split("\n\n")
    network = [line.split(" = ") for line in network.splitlines()]
    network = [(src, dst.strip("()").split(", ")) for src, dst in network]
    graph = {}
    for src, dst in network:
        graph[src] = dst
    return sequence, graph


def steps(graph, node, sequence):
    steps = 0
    for ins in cycle(sequence):
        node = graph[node][0 if ins == "L" else 1]
        steps += 1
        if node.endswith("Z"):
            return steps


# PART 1
@measure_time
def solve1(data):
    sequence, graph = data
    return steps(graph, "AAA", sequence)


# PART 2
@measure_time
def solve2(data):
    sequence, graph = data
    starts = (node for node in graph if node.endswith("A"))
    return math.lcm(*[steps(graph, start, sequence) for start in starts])


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
