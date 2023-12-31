import pytest
from solver import parse, solve1, solve2

TESTDATA = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data, 6)
    assert solution == 16


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
