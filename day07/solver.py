#!/usr/bin/env python

import sys
from collections import Counter
from itertools import product
from pathlib import Path

from aoc import utils

measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [line.split() for line in raw_data.strip().splitlines()]


def any_n(counts, n):
    return any(count == n for count in counts.values())


def get_type(counts):
    if any_n(counts, 5):
        # Five of a kind
        return 0
    if any_n(counts, 4):
        # Four of a kind
        return 1
    if any_n(counts, 3) and any_n(counts, 2):
        # Full House
        return 2
    if any_n(counts, 3):
        # Three of a kind
        return 3
    if sum(count == 2 for count in counts.values()) == 2:
        # Two pair
        return 4
    if any_n(counts, 2):
        # One pair
        return 5
    # High card
    return 6


# PART 1
@measure_time
def solve1(data):
    strengths = {k: i for i, k in enumerate("AKQJT98765432")}
    cards = []
    for hand, bid in data:
        counts = Counter(hand)
        cards.append(
            {
                "hand": hand,
                "counts": counts,
                "type": get_type(counts),
                "bid": int(bid),
                "strengths": tuple(strengths[k] for k in hand),
            }
        )
    cards.sort(key=lambda card: (card["type"], card["strengths"]), reverse=True)
    return sum(rank * card["bid"] for rank, card in enumerate(cards, start=1))


# PART 2
@measure_time
def solve2(data):
    strengths = {k: i for i, k in enumerate("AKQT98765432J")}
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
        cards.append(
            {
                "hand": hand,
                "counts": counts,
                "type": t,
                "bid": int(bid),
                "strengths": tuple(strengths[k] for k in hand),
            }
        )
    cards.sort(key=lambda card: (card["type"], card["strengths"]), reverse=True)
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
