# https://adventofcode.com/2023/day/4
from __future__ import annotations

from collections import Counter

import pytest

import support

from . import common


def solve_for(input_data: str) -> int:
    cards = [common.parse_card(line) for line in input_data.splitlines()]
    card_counts = Counter(card.id for card in cards)

    for card_id in card_counts:
        count = card_counts[card_id]
        num_matching = len(cards[card_id - 1].matching_numbers)
        card_counts.update(
            {
                id: count
                for id in range(
                    card_id + 1, min(len(cards), card_id + num_matching + 1)
                )
            }
        )

    return card_counts.total()


EXAMPLE_1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED_1 = 30


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
