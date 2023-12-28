import pytest
from solver import parse, solve1, solve2, total_count

TESTDATA = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


@pytest.mark.parametrize(
    "pattern,counts,value",
    [
        ("???.###", [1, 1, 3], 1),
        (".??..??...?##.", [1, 1, 3], 4),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], 1),
        ("????.#...#...", [4, 1, 1], 1),
        ("????.######..#####.", [1, 6, 5], 4),
        ("?###????????", [3, 2, 1], 10),
    ],
)
def test_total_count_1(pattern, counts, value):
    assert total_count(pattern, counts) == value


@pytest.mark.parametrize(
    "pattern,counts,value",
    [
        ("???.###", [1, 1, 3], 1),
        ("???.###", [1, 1, 3], 1),
        (".??..??...?##.", [1, 1, 3], 16384),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], 1),
        ("????.#...#...", [4, 1, 1], 16),
        ("????.######..#####.", [1, 6, 5], 2500),
        ("?###????????", [3, 2, 1], 506250),
    ],
)
def test_total_count_5(pattern, counts, value):
    pattern = "?".join([pattern] * 5)
    counts = 5 * counts
    assert total_count(pattern, counts) == value


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 21


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 525152
