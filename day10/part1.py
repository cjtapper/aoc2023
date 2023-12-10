# https://adventofcode.com/2023/day/10

from __future__ import annotations

import pytest

import support


def solve_for(input_data: str) -> int:
    values = (parse_line(line) for line in input_data.splitlines())
    for v in values:
        pass

    # TODO: implement solution here!
    return 0


def parse_line(line: str) -> str:
    return line


EXAMPLE_1 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""
EXPECTED_1 = 4

EXAMPLE_2 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""
EXPECTED_2 = 8


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
        (EXAMPLE_2, EXPECTED_2),
    ],
)
def test_example(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
