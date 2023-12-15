import pytest
from solver import parse, solve1, solve2

TESTDATA = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
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
    assert solution == 1320


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 145
