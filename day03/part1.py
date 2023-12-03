# https://adventofcode.com/2023/day/3

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property
from typing import NamedTuple

import pytest

import support

NUMBER_OR_SYMBOL = re.compile(r"([0-9]+|[^.])")


@dataclass
class SchematicNumber:
    value: int
    bounding_box: Box

    def is_adjacent_to(self, symbol: SchematicSymbol) -> bool:
        return self._adjacency_box.contains(symbol.position)

    @cached_property
    def _adjacency_box(self) -> Box:
        return Box(
            position=Point(
                x=self.bounding_box.position.x - 1,
                y=self.bounding_box.position.y - 1,
            ),
            width=self.bounding_box.width + 2,
            height=self.bounding_box.height + 2,
        )


@dataclass
class SchematicSymbol:
    position: Point


@dataclass
class Box:
    position: Point
    width: int
    height: int

    @property
    def x_min(self) -> int:
        return self.position.x

    @property
    def x_max(self) -> int:
        return self.position.x + self.width - 1

    @property
    def y_min(self) -> int:
        return self.position.y

    @property
    def y_max(self) -> int:
        return self.position.y + self.height - 1

    def contains(self, point: Point) -> bool:
        return (
            self.x_min <= point.x <= self.x_max and self.y_min <= point.y <= self.y_max
        )


class Point(NamedTuple):
    x: int
    y: int


def solve_for(input_data: str) -> int:
    numbers, symbols = parse_schematic(input_data)
    acc = 0

    for number in numbers:
        if any(number.is_adjacent_to(symbol) for symbol in symbols):
            acc += number.value

    return acc


def parse_schematic(
    schematic: str,
) -> tuple[list[SchematicNumber], list[SchematicSymbol]]:
    numbers = []
    symbols = []
    for row_index, row in enumerate(schematic.splitlines()):
        for match in NUMBER_OR_SYMBOL.finditer(row):
            position = Point(x=match.start(), y=row_index)
            if match[0].isdigit():
                numbers.append(
                    SchematicNumber(
                        value=int(match[0]),
                        bounding_box=Box(
                            position=position, width=len(match[0]), height=1
                        ),
                    )
                )
            elif is_symbol(match[0]):
                symbols.append(SchematicSymbol(position=position))
    return numbers, symbols


def is_symbol(char: str) -> bool:
    return not (char == "." or char.isdigit())


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
