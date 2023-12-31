# https://adventofcode.com/2023/day/5#part2

# FIXME: Note - currently incomplete. Tests pass, but unable to work
# with the real data within a reasonable amount of time

from __future__ import annotations

import itertools
from typing import Generator

import pytest

import support

from . import common


def solve_for(input_data: str) -> int:
    almanac = common.parse_almanac(input_data)
    seed_ranges = parse_seed_ranges(input_data)

    locations = []
    for seed_range in seed_ranges:
        locations.extend(
            almanac.find_dest_by_range(
                src_category="seed",
                src_range=seed_range,
                dest_category="location",
            )
        )

    return min(location.start for location in locations)


def parse_seed_ranges(s: str) -> Generator[range, None, None]:
    _, *seeds = s.splitlines()[0].split()
    for start, range_length in itertools.batched(seeds, 2):
        yield range(int(start), int(start) + int(range_length))


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
EXPECTED_1 = 46


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
