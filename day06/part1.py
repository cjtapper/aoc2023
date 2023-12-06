# https://adventofcode.com/2023/day/6

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
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED_1 = 288


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
