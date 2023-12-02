# https://adventofcode.com/2023/day/2

from __future__ import annotations

import pytest

import support

from . import common


def solve_for(input_data: str) -> int:
    bag = common.CubeCollection(red=12, green=13, blue=14)

    games = (common.parse_game(line) for line in input_data.splitlines())
    return sum(game.id for game in games if game.is_valid_for(bag))


EXAMPLE_1 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED_1 = 8


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
    ],
)
def test_example1(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
