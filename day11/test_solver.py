import pytest
from solver import parse, solve1, solve2, solve

TESTDATA = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
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
    assert solution == 374


# PART 2
def test_solve2(parsed_data):
    assert solve(parsed_data, 10) == 1030
    assert solve(parsed_data, 100) == 8410
