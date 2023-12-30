#!/usr/bin/env python

from collections import deque
from itertools import count
from pathlib import Path
import sys
import math

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    out = []
    for line in raw_data.strip().splitlines():
        src, dst = line.split(" -> ")
        dst = dst.split(", ")
        out.append((src, dst))
    return out


class FlipFlop:
    def __init__(self):
        self.on = False

    def process(self, key, val):
        if val:
            return
        else:
            self.on = not self.on
            return self.on


class Conjunction:
    debug = False

    def __init__(self):
        self.prev = {}

    def add_input(self, key):
        self.prev[key] = False

    def process(self, key, val):
        self.prev[key] = val
        if all(self.prev.values()):
            return False
        else:
            return True


class Broadcaster:
    def process(self, key, val):
        return val



# PART 1
@measure_time
def solve1(data):
    modules = {}
    for src, dst in data:
        modname = src
        if src != "broadcaster":
            modname = src[1:]
        if src.startswith("%"):
            mod = FlipFlop()
        elif src.startswith("&"):
            mod = Conjunction()
        elif src == "broadcaster":
            mod = Broadcaster()
        else:
            assert False
        modules[modname] = (mod, dst)


    for src, dst in data:
        srcname = src[1:] if src != "broadcaster" else src
        for dst_name in dst:
            if not dst_name in modules:
                continue
            mod = modules[dst_name][0]
            if isinstance(mod, Conjunction):
                mod.add_input(srcname)

    nlow = 0
    nhigh = 0
    for i in range(1000):
        q = deque([("button", "broadcaster", False)])
        while q:
            src, modname, val = q.popleft()
            if val:
                nhigh += 1
            else:
                nlow += 1
            # input()
            # print(f"{src} -{'high' if val else 'low'}-> {modname}", end="")
            if not modname in modules:
                # ends here
                continue
            mod, dst = modules[modname]
            result = mod.process(src, val)
            for dst_name in dst:
                if result is None:
                    continue
                q.append((modname, dst_name, result))

    return nlow * nhigh


def get_first_low_and_cycle(modules, name):
    c = count()
    first = None
    prev = None
    while True:
        i = next(c)
        q = deque([("button", "broadcaster", False)])
        while q:
            src, modname, val = q.popleft()
            if src == name and modname == "dg" and val == True:
                if first is None:
                    first = i
                if prev is not None:
                    cycle = i - prev
                    return first, cycle
                prev = i
            if not modname in modules:
                # ends here
                continue
            mod, dst = modules[modname]
            result = mod.process(src, val)
            for dst_name in dst:
                if result is None:
                    continue
                q.append((modname, dst_name, result))

# PART 2
@measure_time
def solve2(data):
    modules = {}
    for src, dst in data:
        modname = src
        if src != "broadcaster":
            modname = src[1:]
        if src.startswith("%"):
            mod = FlipFlop()
        elif src.startswith("&"):
            mod = Conjunction()
        elif src == "broadcaster":
            mod = Broadcaster()
        else:
            assert False
        modules[modname] = (mod, dst)


    for src, dst in data:
        srcname = src[1:] if src != "broadcaster" else src
        for dst_name in dst:
            if not dst_name in modules:
                continue
            mod = modules[dst_name][0]
            if isinstance(mod, Conjunction):
                mod.add_input(srcname)


    off1, cycle1 = get_first_low_and_cycle(modules, "xt")
    off2, cycle2 = get_first_low_and_cycle(modules, "sp")
    off3, cycle3 = get_first_low_and_cycle(modules, "zv")
    off4, cycle4 = get_first_low_and_cycle(modules, "lk")

    # don't understand why i can ignore the offsets ...
    return math.lcm(cycle1, cycle2, cycle3, cycle4)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
