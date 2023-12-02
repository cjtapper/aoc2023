from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Game:
    id: int
    rounds: list[CubeCollection]

    def is_valid_for(self, bag: CubeCollection) -> bool:
        return all(bag.contains(round) for round in self.rounds)


@dataclass
class CubeCollection:
    red: int = 0
    green: int = 0
    blue: int = 0

    @property
    def power(self):
        return self.red * self.green * self.blue

    def contains(self, other_cubes: CubeCollection) -> bool:
        return (
            (other_cubes.red <= self.red)
            and (other_cubes.green <= self.green)
            and (other_cubes.blue <= self.blue)
        )


def parse_game(input: str) -> Game:
    raw_game, _, raw_rounds = input.partition(":")

    game_id = int(raw_game.split()[1])

    rounds = []
    for raw_round in raw_rounds.split(";"):
        cubes_seen = {}
        for cube_count in raw_round.split(","):
            count, colour = cube_count.strip().split()
            cubes_seen[colour] = int(count)
        rounds.append(CubeCollection(**cubes_seen))

    return Game(id=game_id, rounds=rounds)
