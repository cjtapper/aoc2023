# https://adventofcode.com/2023/day/6#part2
from __future__ import annotations

import math
from typing import NamedTuple

import pytest

import support


class Race(NamedTuple):
    duration: int
    record_distance: int


def solve_for(input_data: str) -> int:
    race = parse_race(input_data)
    hold_range = calculate_hold_range(race)
    num_possible_record_holds = hold_range.stop - hold_range.start

    return num_possible_record_holds


def parse_race(s: str) -> Race:
    unparsed_durations, unparsed_distances = s.splitlines()
    duration = unparsed_durations.split(":")[1].replace(" ", "")
    distance = unparsed_distances.split(":")[1].replace(" ", "")

    return Race(int(duration), int(distance))


def calculate_hold_range(race: Race) -> range:
    min_hold, max_hold = solve_quadratic_formula(
        -1, race.duration, -1 * (race.record_distance + 1)
    )
    return range(math.ceil(min_hold), math.floor(max_hold) + 1)


def solve_quadratic_formula(a: float, b: float, c: float) -> tuple[float, float]:
    return (
        (-1 * b + math.sqrt(b**2 - 4 * a * c)) / (2 * a),
        (-1 * b - math.sqrt(b**2 - 4 * a * c)) / (2 * a),
    )


EXAMPLE_1 = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED_1 = 71503


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
