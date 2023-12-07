# https://adventofcode.com/2023/day/5

from __future__ import annotations

import pytest

import support

from . import common


def solve_for(input_data: str) -> int:
    seeds = parse_seeds(input_data)
    almanac = common.parse_almanac(input_data)

    locations = []
    for seed in seeds:
        locations.append(almanac.find_dest("seed", seed, "location"))

    return min(locations)


def parse_seeds(s: str) -> list[int]:
    _, *seeds = s.splitlines()[0].split()
    return [int(seed) for seed in seeds]


EXAMPLE_1 = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED_1 = 35


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
