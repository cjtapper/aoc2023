# https://adventofcode.com/2023/day/6
from __future__ import annotations

import math
from typing import Generator, NamedTuple

import pytest

import support


class Race(NamedTuple):
    duration: int
    record_distance: int


def solve_for(input_data: str) -> int:
    races = parse_races(input_data)
    acc = 1
    for race in races:
        hold_range = calculate_hold_range(race)
        acc *= len(hold_range)

    return acc


def parse_races(s: str) -> Generator[Race, None, None]:
    unparsed_durations, unparsed_distances = s.splitlines()
    durations = unparsed_durations.split(":")[1].split()
    distances = unparsed_distances.split(":")[1].split()

    return (
        Race(int(duration), int(distance))
        for duration, distance in zip(durations, distances)
    )


def calculate_hold_range(race: Race) -> range:
    """
    This problem can be modeled as:

    distance_travelled == (race_duration - hold_time) * hold_time

    If we set distance_travelled to the record_distance + 1, this can be
    rearranged to a quadratic equation and solved with the quadratic
    formula. The two solutions represent the minimum and maximum hold
    times to beat the record.


    record_distance + 1 == (race_duration - hold_time) * hold_time

    -1 * hold_time**2 + race_duration * hold_time - (record_distance + 1) == 0

    """
    min_hold, max_hold = solve_quadratic_equation(
        -1, race.duration, -1 * (race.record_distance + 1)
    )
    return range(math.ceil(min_hold), math.floor(max_hold) + 1)


def solve_quadratic_equation(a: float, b: float, c: float) -> tuple[float, float]:
    # Solves for x:
    #
    # a * x**2 + b * x + c == 0
    return (
        (-1 * b + math.sqrt(b**2 - 4 * a * c)) / (2 * a),
        (-1 * b - math.sqrt(b**2 - 4 * a * c)) / (2 * a),
    )


EXAMPLE_1 = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED_1 = 288


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
