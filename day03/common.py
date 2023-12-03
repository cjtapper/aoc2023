from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property
from typing import NamedTuple

NUMBER_OR_SYMBOL = re.compile(r"([0-9]+|[^.])")


@dataclass
class Schematic:
    numbers: list[SchematicNumber]
    symbols: list[SchematicSymbol]

    @property
    def part_numbers(self) -> list[SchematicNumber]:
        return [
            number
            for number in self.numbers
            if any(number.is_adjacent_to(symbol) for symbol in self.symbols)
        ]


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


def parse_schematic(
    schematic: str,
) -> Schematic:
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
    return Schematic(numbers, symbols)


def is_symbol(char: str) -> bool:
    return not (char == "." or char.isdigit())
