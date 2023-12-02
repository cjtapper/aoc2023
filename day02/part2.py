# https://adventofcode.com/2023/day/2#part2

from __future__ import annotations

from dataclasses import dataclass

import pytest

import support


@dataclass
class Game:
    id: int
    reveals: list[Reveal]


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

    @property
    def power(self):
        return self.red * self.green * self.blue


def solve_for(input_data: str) -> int:
    games = (parse_game(line) for line in input_data.splitlines())
    return sum(get_min_bag(game).power for game in games)


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


def get_min_bag(game: Game) -> Bag:
    return Bag(
        red=max(reveal.red for reveal in game.reveals),
        green=max(reveal.green for reveal in game.reveals),
        blue=max(reveal.blue for reveal in game.reveals),
    )


EXAMPLE_1 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED_1 = 2286


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
