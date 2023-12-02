import pytest
from solver import parse, solve1, solve2

TESTDATA = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    assert data[1] == [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}]
    assert data[2] == [{'blue': 1, 'green': 2}, {'green': 3, 'blue': 4, 'red': 1}, {'green': 1, 'blue': 1}]
    assert data[3] == [{'green': 8, 'blue': 6, 'red': 20}, {'blue': 5, 'red': 4, 'green': 13}, {'green': 5, 'red': 1}]
    assert data[4] == [{'green': 1, 'red': 3, 'blue': 6}, {'green': 3, 'red': 6}, {'green': 3, 'blue': 15, 'red': 14}]
    assert data[5] == [{'red': 6, 'blue': 1, 'green': 3}, {'blue': 2, 'red': 1, 'green': 2}]


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 8


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 2286
