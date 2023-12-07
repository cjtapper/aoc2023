# https://adventofcode.com/2023/day/7
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cached_property
from typing import Literal

import pytest

import support

Card = Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

# ordered by strength
CARDS = ("J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A")


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


@dataclass(frozen=True)
class Hand:
    cards: tuple[Card, Card, Card, Card, Card]

    @cached_property
    def type(self) -> HandType:
        card_counts = Counter[Card](self.cards)

        if len(card_counts) > 1:
            joker_count = card_counts.pop("J", 0)
            card_counts.update({card_counts.most_common(1)[0][0]: joker_count})

        match card_counts.most_common():
            case (_, 5), *_:
                return HandType.FIVE_OF_A_KIND
            case (_, 4), *_:
                return HandType.FOUR_OF_A_KIND
            case (_, 3), (_, 2), *_:
                return HandType.FULL_HOUSE
            case (_, 3), *_:
                return HandType.THREE_OF_A_KIND
            case (_, 2), (_, 2), *_:
                return HandType.TWO_PAIR
            case (_, 2), *_:
                return HandType.ONE_PAIR
            case _:
                return HandType.HIGH_CARD

    def __eq__(self, other: object) -> bool:
        return self.type == other.type and self.cards == other.cards

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return super().__lt__(other)
        if self.type == other.type:
            for card, other_card in zip(self.cards, other.cards):
                if card != other_card:
                    return card_strength(card) < card_strength(other_card)

        return self.type < other.type


def solve_for(input_data: str) -> int:
    hand_bids = [parse_hand_and_bid(line) for line in input_data.splitlines()]
    hand_bids.sort(key=lambda hb: hb[0])
    return sum(rank * hand_bid[1] for rank, hand_bid in enumerate(hand_bids, 1))


def parse_hand_and_bid(line: str) -> tuple(Hand, int):
    hand, bid = line.split()

    return Hand(cards=tuple([*hand])), int(bid)


def card_strength(card: Card) -> int:
    return CARDS.index(card)


EXAMPLE_1 = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
EXPECTED_1 = 5905


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
