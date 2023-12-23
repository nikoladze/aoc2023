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
    #input()
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

        # print_grid(data, seen, (i, j))
        # print((i, j), end)

        if (i, j) == end:
            lens.append(len(seen))
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            new_i, new_j = (i + di, j + dj)
            if not (0 <= new_i < len(data)):
                continue
            if not (0 <= new_j < len(data[0])):
                continue
            c = data[new_i][new_j]
            if c == "#":
                continue
            if c in vmap and vmap[c] != (di, dj):
                continue
            if (new_i, new_j) in seen:
                continue
            q.append((seen | {(new_i, new_j)}, (new_i, new_j)))

    return max(lens)

# PART 2
@measure_time
def solve2(data):
    # q = [(frozenset(), (0, 1))]
    # end = (len(data) - 1, len(data[0]) - 2)
    # lens = []
    # while q:
    #     seen, (i, j) = q.pop()

    #     # import os
    #     # os.system("clear")
    #     # print_grid(data, seen, (i, j))

    #     if (i, j) == end:
    #         lens.append(len(seen))
    #         continue
    #     for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
    #         new_i, new_j = (i + di, j + dj)
    #         if not (0 <= new_i < len(data)):
    #             continue
    #         if not (0 <= new_j < len(data[0])):
    #             continue
    #         c = data[new_i][new_j]
    #         if c == "#":
    #             continue
    #         if (new_i, new_j) in seen:
    #             continue
    #         q.append((seen | {(new_i, new_j)}, (new_i, new_j)))

    # return max(lens)
    #

    # should never run outside grid (because of walls)

    end = (len(data) - 1, len(data[0]) - 2)
    q = [((0, 1), (1, 1))]
    seen = set([(0, 1)])
    graph = defaultdict(set)
    junctions = set()
    while q:
        from_pos, (i, j) = q.pop()
        if (i, j) == end:
            continue
        seen.add((i, j))
        n = 0
        while True:
            #input()
            #print_grid(data, seen, (i, j))
            #print(f"{(i, j)=}")
            if (i, j) == end:
                graph[from_pos].add(((i, j), n))
                break
            options = []
            for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                new_i, new_j = (i + di, j + dj)
                if data[new_i][new_j] == "#":
                    continue
                if (new_i, new_j) == from_pos:
                    continue
                if (new_i, new_j) in seen and (new_i, new_j) not in junctions:
                    continue
                options.append((new_i, new_j))
            if not options:
                # deadend
                break
            if len(options) == 1:
                # go to only possible direction
                i, j = options.pop()
                seen.add((i, j))
                n += 1
                if (i, j) in junctions:
                    #print(f"junction at {(i, j, n)=} reachable {from_pos=}")
                    graph[from_pos].add(((i, j), n))
                    break
                continue
            if len(options) > 1:
                # reached a junction
                #print(f"junction at {(i, j, n)=} reachable {from_pos=}")
                junctions.add((i, j))
                graph[from_pos].add(((i, j), n))
                for next_pos in options:
                    q.append(((i, j), next_pos))
                break

    #print(graph)
    for from_pos, dsts in list(graph.items()):
        for dst, n in list(dsts):
            graph[dst].add((from_pos, n))

    q = [(frozenset(), (0, 1), 0)]
    lens = []
    while q:
        seen, (i, j), tot = q.pop()
        if (i, j) == end:
            lens.append(tot)
        for dst, n in graph[i, j]:
            if dst in seen:
                continue
            q.append((seen | {dst}, dst, tot + n + 1))

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

