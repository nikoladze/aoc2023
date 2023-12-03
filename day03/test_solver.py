import pytest
from solver import parse, solve1, solve2, find_numbers, has_symbol_neighbor

TESTDATA = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here

def test_find_numbers(parsed_data):
    numbers = find_numbers(parsed_data)
    assert numbers[:3] == [((0, 0), 467), ((0, 5), 114), ((2, 2), 35)]
    assert len(numbers) == 10
    assert [n for _, n in numbers] == [467, 114, 35, 633, 617, 58, 592, 755, 664, 598]


def test_has_symbol_neighbor(parsed_data):
    assert has_symbol_neighbor(parsed_data, 4, 2)
    assert has_symbol_neighbor(parsed_data, 0, 2)

# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 4361


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 467835
