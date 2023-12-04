# https://adventofcode.com/2023/day/4
from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

import pytest

import support


@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    numbers: list[int]

    @property
    def points(self) -> int:
        winners = sum(1 for number in self.numbers if number in self.winning_numbers)
        return 2**winners >> 1


def solve_for(input_data: str) -> int:
    cards = (parse_card(line) for line in input_data.splitlines())

    return sum(card.points for card in cards)


def parse_card(line: str) -> Card:
    card, numbers = line.split(":")
    _, card_id = card.split()

    winning_numbers_raw, card_numbers_raw = numbers.split("|")
    winning_numbers = parse_numbers(winning_numbers_raw)
    card_numbers = parse_numbers(card_numbers_raw)

    return Card(
        id=int(card_id),
        numbers=list(card_numbers),
        winning_numbers=set(winning_numbers),
    )


def parse_numbers(s: str) -> Generator[int, None, None]:
    return (int(number) for number in s.split())


EXAMPLE_1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED_1 = 13


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
