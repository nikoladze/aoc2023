#!/usr/bin/env python

import sys
from collections import defaultdict
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().splitlines()


def print_grid(data, seen, cur):
    print()
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if (i, j) == cur:
                print("X", end="")
            elif (i, j) in seen:
                print("O", end="")
            else:
                print(c, end="")
        print()


# PART 1
@measure_time
def solve1(data):
    q = [(frozenset(), (0, 1))]
    end = (len(data) - 1, len(data[0]) - 2)
    vmap = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    lens = []
    while q:
        seen, (i, j) = q.pop()
        if (i, j) == end:
            lens.append(len(seen))
            continue
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            new_i, new_j = (i + di, j + dj)
            c = data[new_i][new_j]
            if c == "#":
                continue
            if c in vmap and vmap[c] != (di, dj):
                continue
            if (new_i, new_j) in seen:
                continue
            q.append((seen | {(new_i, new_j)}, (new_i, new_j)))
    return max(lens)


def get_graph(data):
    end = (len(data) - 1, len(data[0]) - 2)
    q = [((0, 1), (1, 1), 1)]
    seen = set([(0, 1)])
    graph = defaultdict(set)
    junctions = set()
    while q:
        from_pos, (i, j), n = q.pop()
        seen.add((i, j))
        options = []
        junction = None
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if (i, j) == end:
                continue
            new_i, new_j = (i + di, j + dj)
            if data[new_i][new_j] == "#":
                continue
            if (new_i, new_j) in junctions:
                junction = (new_i, new_j)
            if (new_i, new_j) in seen:
                continue
            options.append((new_i, new_j))
        if len(options) > 1:
            junctions.add((i, j))
        if not options or len(options) > 1:
            # reached a junction or dead end
            if junction:
                # move to junction if we are just before one
                i, j = junction
                n += 1
            graph[from_pos].add(((i, j), n))
            from_pos = (i, j)
            n = 0
        for new_i, new_j in options:
            q.append((from_pos, (new_i, new_j), n + 1))

    # make graph symmetric
    for from_pos, dsts in list(graph.items()):
        for dst, n in list(dsts):
            graph[dst].add((from_pos, n))

    return graph


# PART 2
@measure_time
def solve2(data):
    graph = get_graph(data)
    end = (len(data) - 1, len(data[0]) - 2)
    q = [(frozenset(), (0, 1), 0)]
    lens = []
    while q:
        seen, (i, j), tot = q.pop()
        if (i, j) == end:
            lens.append(tot)
        for dst, n in graph[i, j]:
            if dst in seen:
                continue
            q.append((seen | {dst}, dst, tot + n))
    return max(lens)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
