# https://adventofcode.com/2023/day/3

from __future__ import annotations

import pytest

import support

from . import common


def solve_for(input_data: str) -> int:
    numbers, symbols = common.parse_schematic(input_data)
    acc = 0

    for number in numbers:
        if any(number.is_adjacent_to(symbol) for symbol in symbols):
            acc += number.value

    return acc


EXAMPLE_1 = """\
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
EXPECTED_1 = 4361


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
