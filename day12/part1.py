# https://adventofcode.com/2023/day/12
from __future__ import annotations

import pytest

import support

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"


def solve_for(input_data: str) -> int:
    values = (parse_line(line) for line in input_data.splitlines())
    for v in values:
        pass

    # TODO: implement solution here!
    return 0


def parse_line(line: str) -> str:
    return line


EXAMPLE_1 = """\
#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
"""
EXPECTED_1 = 0


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
    ],
)
def test_example(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
