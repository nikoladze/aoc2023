#!/usr/bin/env python

from collections import Counter
from itertools import product
import sys
from pathlib import Path

from aoc import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [line.split() for line in raw_data.strip().splitlines()]

# PART 1
@measure_time
def solve1(data):
    STRENGTHS = {k: i for i, k in enumerate("AKQJT98765432")}
    cards = []
    for hand, bid in data:
        counts = Counter(hand)
        if any(count == 5 for count in counts.values()):
            t = 0
        elif any(count == 4 for count in counts.values()):
            t = 1
        elif any(count == 3 for count in counts.values()) and any(count == 2 for count in counts.values()):
            t = 2
        elif any(count == 3 for count in counts.values()):
            t = 3
        elif sum(count == 2 for count in counts.values()) == 2:
            t = 4
        elif any(count == 2 for count in counts.values()):
            t = 5
        else:
            t = 6
        cards.append({"hand": hand, "counts": counts, "type": t, "bid": int(bid), "strengths": tuple(STRENGTHS[k] for k in hand)})
    cards.sort(key=lambda card: (card["type"], card["strengths"]), reverse=True)
    return sum(rank * card["bid"] for rank, card in enumerate(cards, start=1))


def get_type(counts):
    if any(count == 5 for count in counts.values()):
        return 0
    if any(count == 4 for count in counts.values()):
        return 1
    if any(count == 3 for count in counts.values()) and any(count == 2 for count in counts.values()):
        return 2
    if any(count == 3 for count in counts.values()):
        return 3
    if sum(count == 2 for count in counts.values()) == 2:
        return 4
    if any(count == 2 for count in counts.values()):
        return 5
    return 6


# PART 2
@measure_time
def solve2(data):
    STRENGTHS = {k: i for i, k in enumerate("AKQT98765432J")}
    non_jokers = "AKQT98765432"
    cards = []
    for hand, bid in data:
        n_jokers = hand.count("J")
        arg_jokers = [i for i, c in enumerate(hand) if c == "J"]
        t = 6
        new_hand = list(hand)
        for replacements in product(*[non_jokers for _ in range(n_jokers)]):
            for i, replacement in zip(arg_jokers, replacements):
                new_hand[i] = replacement
            counts = Counter(new_hand)
            new_t = get_type(counts)
            if new_t < t:
                t = new_t
        cards.append({"hand": hand, "counts": counts, "type": t, "bid": int(bid), "strengths": tuple(STRENGTHS[k] for k in hand)})
    cards.sort(key=lambda card: (card["type"], card["strengths"]), reverse=True)
    from pprint import pprint
    pprint(cards)
    return sum(rank * card["bid"] for rank, card in enumerate(cards, start=1))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

