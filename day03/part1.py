# https://adventofcode.com/2023/day/3

from __future__ import annotations

import re

import pytest

import support

NUMBER_PATTERN = re.compile(r"[0-9]+")


def solve_for(input_data: str) -> int:
    grid = input_data.splitlines()
    acc = 0

    for row_index, row in enumerate(grid):
        for match in NUMBER_PATTERN.finditer(row):
            if is_part_number(match, grid, row_index):
                acc += int(match[0])
    return acc


def is_symbol(char: str) -> bool:
    return not (char == "." or char.isdigit())


def is_part_number(match: re.Match[str], grid: list[str], row_index: int) -> bool:
    start, stop = match.span()
    for surrounding_row in grid[max(row_index - 1, 0) : row_index + 2]:
        for c in surrounding_row[max(start - 1, 0) : stop + 1]:
            if is_symbol(c):
                return True
    return False


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
