import pytest
from solver import parse, solve1, solve2, parse_line

TESTDATA1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

TESTDATA2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

@pytest.fixture
def parsed_data1():
    return parse(TESTDATA1)


@pytest.fixture
def parsed_data2():
    return parse(TESTDATA2)

def test_parse_line():
    assert parse_line("onesevensixseven") == 17
    assert parse_line("oneight") == 18


def test_parse():
    data = parse(TESTDATA1)
    # asserts go here


# PART 1
def test_solve1(parsed_data1):
    solution = solve1(parsed_data1)
    assert solution == 142


# PART 2
def test_solve2(parsed_data2):
    solution = solve2(parsed_data2)
    assert solution == 281
