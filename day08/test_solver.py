import pytest
from solver import parse, solve1, solve2

TESTDATA = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# # PART 1
# def test_solve1(parsed_data):
#     solution = solve1(parsed_data)
#     # asserts go here


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 6
