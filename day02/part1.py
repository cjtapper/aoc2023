# https://adventofcode.com/2023/day/2

from __future__ import annotations

from dataclasses import dataclass

import pytest

import support


@dataclass
class Game:
    id: int
    reveals: list[Reveal]

    def is_valid_for(self, bag_contents: Bag) -> bool:
        return all(bag_contents.contains(reveal) for reveal in self.reveals)


@dataclass
class Reveal:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Bag:
    red: int
    green: int
    blue: int

    def contains(self, reveal: Reveal) -> bool:
        return (
            (reveal.red <= self.red)
            and (reveal.green <= self.green)
            and (reveal.blue <= reveal.blue)
        )


def solve_for(input_data: str) -> int:
    bag = Bag(red=12, green=13, blue=14)

    games = (parse_game(line) for line in input_data.splitlines())
    return sum(game.id for game in games if game.is_valid_for(bag))


def parse_game(input: str) -> Game:
    raw_game, _, raw_reveals = input.partition(":")

    game_id = int(raw_game.split()[1])

    reveals = []
    for raw_reveal in raw_reveals.split(";"):
        cubes_seen = {}
        for cube_count in raw_reveal.split(","):
            count, colour = cube_count.strip().split()
            cubes_seen[colour] = int(count)
        reveals.append(Reveal(**cubes_seen))

    return Game(id=game_id, reveals=reveals)


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
