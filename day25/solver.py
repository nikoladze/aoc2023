#!/usr/bin/env python

from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        src, dsts = line.strip().split(": ")
        out.append((src, dsts.split()))
    return out


def disconnected(graph, node1, node2):
    graph = {k: set(v) for k, v in graph.items()}
    for src, dsts in graph.items():
        for dst in list(dsts):
            if src == node1 and dst == node2:
                dsts.remove(node2)
            if dst == node1 and src == node2:
                dsts.remove(node1)
    return graph


def try_partition(graph, node1, node2):
    cluster1, cluster2 = set(), set()
    q = deque([(node1, cluster1), (node2, cluster2)])
    seen = set()
    while q:
        node, cluster = q.popleft()
        if node in seen:
            continue
        seen.add(node)
        cluster.add(node)
        if not node in graph:
            continue
        for child in graph[node]:
            if child in seen:
                continue
            q.append((child, cluster))
    return cluster1, cluster2


# PART 1
@measure_time
def solve1(data):
    graph = defaultdict(set)
    edges = set()
    nodes = set()
    for src, dsts in data:
        graph[src] |= set(dsts)
        for dst in dsts:
            nodes.add(src)
            nodes.add(dst)
            graph[dst].add(src)
            if not (dst, src) in edges:
                edges.add((src, dst))

    ncon_list = []
    for src, dst in edges:
        for src, dst in [
            (src, dst),
            (dst, src),
        ]:  # this makes a difference because of order of iteration
            cluster1, cluster2 = try_partition(disconnected(graph, src, dst), src, dst)
            if len(cluster1) == 1 or len(cluster2) == 1:
                # not a valid situation
                continue
            n_connecting_edges = sum(
                (n1 in cluster1 and n2 in cluster2)
                or (n2 in cluster1 and n1 in cluster2)
                for n1, n2 in edges
            )
            ncon_list.append((n_connecting_edges, (src, dst)))
            if n_connecting_edges == 3:
                # already found a solution
                return len(cluster1) * len(cluster2)

    # if not, try combinations, starting with most promising edges first
    promising = []
    seen = set()
    for _, (src, dst) in sorted(ncon_list):
        if (src, dst) in seen or (dst, src) in seen:
            continue
        promising.append((src, dst))
        seen.add((src, dst))

    seen = set()
    for n in range(3, len(promising)):
        for comb in combinations(promising[:n], 3):
            if comb in seen:
                continue
            seen.add(comb)
            (s1, d1), (s2, d2), (s3, d3) = comb
            dis_graph = disconnected(
                disconnected(disconnected(graph, s1, d1), s2, d2), s3, d3
            )
            cluster1, cluster2 = try_partition(dis_graph, s1, d1)
            if len(cluster1) == 1 or len(cluster2) == 1:
                # not a valid situation
                continue
            edges_without = [
                (s, d) for s, d in edges if (s, d) not in comb and not (d, s) in comb
            ]
            if not any(
                (n1 in cluster1 and n2 in cluster2)
                or (n2 in cluster1 and n1 in cluster2)
                for n1, n2 in edges_without
            ):
                # found solution
                return len(cluster1) * len(cluster2)


# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
