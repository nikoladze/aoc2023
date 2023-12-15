#!/usr/bin/env python

from pathlib import Path
import sys

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return raw_data.strip().replace("\n", "").split(",")

def HASH(chars):
    cur = 0
    for c in chars:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


# PART 1
@measure_time
def solve1(data):
    return sum(map(HASH, data))


# PART 2
@measure_time
def solve2(data):
    boxes = [[] for _ in range(256)]
    for ins in data:
        if ins.endswith("-"):
            label = ins[:-1]
            box = boxes[HASH(label)]
            found = False
            for i, content in enumerate(box):
                blabel, flen = content
                if blabel == label:
                    found = True
                    break
            if found:
                box.pop(i)
        else:
            label, flen = ins.split("=")
            box = boxes[HASH(label)]
            for i, content in enumerate(box):
                blabel, bflen = content
                if blabel == label:
                    content[1] = flen
                    break
            else:
                box.append([label, flen])
    solution = 0
    for ibox, box in enumerate(boxes):
        for islot, (label, flen) in enumerate(box):
            solution += (ibox + 1) * (islot + 1) * int(flen)
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

