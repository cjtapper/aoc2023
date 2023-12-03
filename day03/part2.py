# https://adventofcode.com/2023/day/3

from __future__ import annotations

import re
from collections import defaultdict
from typing import TypeAlias

import pytest

import support

NUMBER_PATTERN = re.compile(r"[0-9]+")

Position: TypeAlias = tuple[int, int]


def solve_for(input_data: str) -> int:
    grid = input_data.splitlines()
    gear_position_partnums = defaultdict(list)

    for row_index, row in enumerate(grid):
        for match in NUMBER_PATTERN.finditer(row):
            for gear_position in find_adjacent_gears(match, grid, row_index):
                gear_position_partnums[gear_position].append(int(match[0]))

    return sum(
        gear_ratio(*partnums)
        for partnums in gear_position_partnums.values()
        if len(partnums) == 2
    )


def is_gear(char: str) -> bool:
    return char == "*"


def gear_ratio(part_number_1: int, part_number_2: int) -> int:
    return part_number_1 * part_number_2


def find_adjacent_gears(
    match: re.Match[str], grid: list[str], row_index: int
) -> list[Position]:
    start, stop = match.span()
    adjacent_gear_positions = []

    start_row_index = max(row_index - 1, 0)
    col_start = max(start - 1, 0)
    for y, surrounding_row in enumerate(
        grid[start_row_index : row_index + 2], start_row_index
    ):
        for x, c in enumerate(surrounding_row[col_start : stop + 1], col_start):
            if is_gear(c):
                adjacent_gear_positions.append((x, y))
    return adjacent_gear_positions


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
EXPECTED_1 = 467835


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
