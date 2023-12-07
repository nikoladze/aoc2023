import pytest
from solver import parse, solve1, solve2

TESTDATA = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    # asserts go here


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 5905
