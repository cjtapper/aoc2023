# https://adventofcode.com/2023/day/11
from __future__ import annotations

import itertools
from typing import NamedTuple

import pytest

import support

Image = list[str]


class Coordinate(NamedTuple):
    x: int
    y: int


def solve_for(input_data: str) -> int:
    image = input_data.splitlines()
    galaxies = find_galaxies(image)
    empty_rows = find_empty_rows(image)
    empty_cols = find_empty_cols(image)
    acc = 0

    for a, b in itertools.combinations(galaxies, 2):
        result = space_distance(a, b, empty_rows, empty_cols)
        acc += result

    # TODO: implement solution here!
    return acc


def parse_line(line: str) -> str:
    return line


def find_galaxies(image: Image) -> tuple[Coordinate, ...]:
    result = []
    for y, row in enumerate(image):
        for x, char in enumerate(row):
            if char == "#":
                result.append(Coordinate(x, y))
    return tuple(result)


def find_empty_rows(image: Image) -> tuple[int, ...]:
    return tuple(index for index, row in enumerate(image) if is_empty(row))


def find_empty_cols(image: Image) -> tuple[int, ...]:
    cols: list[tuple[str]] = list(zip(*image))
    return tuple(index for index, col in enumerate(cols) if is_empty(col))


def is_empty(row: str | tuple[str]) -> bool:
    return all(c == "." for c in row)


def manhattan_distance(a: Coordinate, b: Coordinate) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def space_distance(
    a: Coordinate,
    b: Coordinate,
    empty_rows: tuple[int, ...],
    empty_cols: tuple[int, ...],
) -> int:
    flat_distance = manhattan_distance(a, b)
    empty_rows_between = sum(
        1 for row in empty_rows if row in range(min(a.y, b.y), max(a.y, b.y))
    )
    empty_cols_between = sum(
        1 for col in empty_cols if col in range(min(a.x, b.x), max(a.x, b.x))
    )
    return flat_distance + empty_rows_between + empty_cols_between


EXAMPLE_1 = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
EXPECTED_1 = 374


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
