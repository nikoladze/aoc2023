import pytest
from solver import parse, solve1, solve2

TESTDATA = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
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
    assert solution == 114


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 2
