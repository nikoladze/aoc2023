#!/usr/bin/env python

import sys
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    blocks = raw_data.strip().split("\n\n")
    seeds = [int(x) for x in blocks[0].split(": ")[1].split()]
    mappings = []
    for block in blocks[1:]:
        block = block.splitlines()
        header = block[0]
        mappings.append((header, [tuple(map(int, line.split())) for line in block[1:]]))
    return seeds, mappings


# PART 1
@measure_time
def solve1(data):
    seeds, mappings = data

    def get_mapping(n, mapping):
        for dst, src, rangelen in mapping:
            if src <= n < src + rangelen:
                return dst + (n - src)
        return n

    out = []
    for seed in seeds:
        n = seed
        for header, mapping in mappings:
            n = get_mapping(n, mapping)
        out.append(n)
    return min(out)


# PART 2
@measure_time
def solve2(data):
    seeds, mappings = data

    def get_mapping_ranges(inp_list, mapping):
        out = []
        for dst, src, map_rangelen in mapping:
            new_inp = []
            for inp, inp_rangelen in inp_list:
                boundaries = sorted(
                    set([inp, inp + inp_rangelen, src, src + map_rangelen])
                )
                splits = []
                for bound in boundaries:
                    if bound < inp or bound > inp + inp_rangelen:
                        continue
                    splits.append(bound)
                for start, stop in zip(splits, splits[1:]):
                    if (
                        src <= start < src + map_rangelen
                        and src < stop < src + map_rangelen
                    ):
                        # inside
                        out.append((dst + (start - src), stop - start))
                    else:
                        # outside
                        new_inp.append(
                            (start, stop - start)
                        )  # <- goes to input for next step
            inp_list = new_inp
        out += inp_list  # add left over inputs
        return out

    inp = list(zip(seeds, seeds[1:]))
    for header, mapping in mappings:
        n_before = sum(x for _, x in inp)
        inp = get_mapping_ranges(inp, mapping)
        assert n_before == sum(x for _, x in inp)
    return min(x for x, _ in inp)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
