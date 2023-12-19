#!/usr/bin/env python

import sys
from functools import reduce
from operator import mul
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    workflows_raw, ratings = raw_data.strip().split("\n\n")
    workflows = {}
    for workflow in workflows_raw.splitlines():
        name, instructions = workflow.split("{")
        instructions = instructions[:-1].split(",")
        instructions = [ins.split(":") for ins in instructions]
        workflows[name] = instructions
    ratings = [
        dict(fields.split("=") for fields in rating[1:-1].split(","))
        for rating in ratings.splitlines()
    ]
    ratings = [{k: int(v) for k, v in rating.items()} for rating in ratings]
    return workflows, ratings


def run_workflow(workflows, name, part):
    workflow = workflows[name]
    for ins in workflow:
        match ins:
            case (expr, res):
                if not eval(expr, {}, dict(part)):
                    continue
            case (res,):
                pass
        match res:
            case "A":
                return True
            case "R":
                return False
            case other:
                return run_workflow(workflows, other, part)
    return False


# PART 1
@measure_time
def solve1(data):
    workflows, ratings = data
    solution = 0
    for part in ratings:
        if run_workflow(workflows, "in", part):
            solution += sum(part.values())
    return solution


def find_bounds(workflows, name, bounds, leaves):
    workflow = workflows[name]
    for ins in workflow:
        bounds = {k: list(v) for k, v in bounds.items()}
        bounds_else = bounds
        match ins:
            case (expr, res):
                key = expr[0]
                op = expr[1]
                val = int(expr[2:])
                lower, upper = bounds[key]
                lower_else, upper_else = lower, upper
                if op == "<":
                    # (lower, upper) < val
                    if lower >= val:
                        continue
                    upper = val - 1
                    lower_else = val
                elif op == ">":
                    # (lower, upper) > val
                    if val >= upper:
                        continue
                    lower = val + 1
                    upper_else = val
                else:
                    assert False
                bounds[key] = (lower, upper)
                bounds_else = {k: list(v) for k, v in bounds.items()}
                bounds_else[key] = (lower_else, upper_else)
            case (res,):
                pass
        match res:
            case "A":
                leaves.append(bounds)
            case "R":
                pass
            case other:
                find_bounds(workflows, other, bounds, leaves=leaves)
        bounds = bounds_else


# PART 2
@measure_time
def solve2(data):
    workflows, _ = data
    bounds = {key: (1, 4000) for key in "xmas"}
    leaves = []
    find_bounds(workflows, "in", bounds, leaves=leaves)
    return sum(
        reduce(mul, ((upper - lower) + 1 for lower, upper in l.values()))
        for l in leaves
    )


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
