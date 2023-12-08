#!/usr/bin/env python

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
    return sequence, network


# PART 1
@measure_time
def solve1(data):
    sequence, network = data
    graph = {}
    for src, dst in network:
        graph[src] = dst
    steps = 0
    pos = "AAA"
    for ins in cycle(sequence):
        index = 0 if ins == "L" else 1
        pos = graph[pos][index]
        steps += 1
        if pos == "ZZZ":
            break
    return steps


# PART 2
@measure_time
def solve2(data):
    sequence, network = data
    graph = {}
    for src, dst in network:
        graph[src] = dst
    def run():
        steps = 0
        pos = [node for node in graph if node.endswith("A")]
        tracker = [set() for _ in pos]
        cycles = [False for _ in pos]
        while True:
            for i, ins in enumerate(sequence):
                index = 0 if ins == "L" else 1
                pos = [graph[node][index] for node in pos]
                steps += 1
                for j, (seen, node) in enumerate(zip(tracker, pos)):
                    key = (i, node)
                    if key in seen and not cycles[j]:
                        cycles[j] = (key, steps)
                        print(f"cycle for {j=}, {key=}")
                    seen.add(key)

                if all(cycles):
                    print(cycles)
                    import math
                    print(math.lcm(*[_steps for _, _steps in cycles]))
                    return

                if any(node.endswith("Z") for node in pos):
                    print(pos)
                    print([node.endswith("Z") for node in pos])
                if all(node.endswith("Z") for node in pos):
                    break

    #run()

    def find_cycle(node):
        pos = node
        steps_since = 0
        for ins in cycle(sequence):
            index = 0 if ins == "L" else 1
            pos = graph[pos][index]
            if pos.endswith("Z"):
                return steps_since
            else:
                steps_since += 1

    starts = [node for node in graph if node.endswith("A")]
    import math
    return math.lcm(*[find_cycle(start) + 1 for start in starts])

    #return steps


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

