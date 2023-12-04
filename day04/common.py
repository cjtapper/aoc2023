from __future__ import annotations

from dataclasses import dataclass
from typing import Generator


@dataclass(frozen=True)
class Card:
    id: int
    winning_numbers: frozenset[int]
    numbers: tuple[int, ...]

    @property
    def points(self) -> int:
        num_matching = len(self.matching_numbers)
        return 2**num_matching >> 1

    @property
    def matching_numbers(self) -> list[int]:
        return [number for number in self.numbers if number in self.winning_numbers]


def parse_card(line: str) -> Card:
    card, numbers = line.split(":")
    _, card_id = card.split()

    winning_numbers_raw, card_numbers_raw = numbers.split("|")
    winning_numbers = parse_numbers(winning_numbers_raw)
    card_numbers = parse_numbers(card_numbers_raw)

    return Card(
        id=int(card_id),
        numbers=tuple(card_numbers),
        winning_numbers=frozenset(winning_numbers),
    )


def parse_numbers(s: str) -> Generator[int, None, None]:
    return (int(number) for number in s.split())
