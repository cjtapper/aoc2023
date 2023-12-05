# https://adventofcode.com/2023/day/5#part2

# FIXME: Note - currently incomplete. Tests pass, but unable to work
# with the real data within a reasonable amount of time

from __future__ import annotations

import itertools
from dataclasses import dataclass

import pytest

import support


@dataclass
class Almanac:
    target_seeds: list[int]
    maps: dict[str, AlmanacMap]

    def find_dest(self, src_category: str, src: int, dest_category: str) -> int:
        target = src
        while src_category != dest_category:
            map = self.maps[src_category]
            target = map.find_dest(target)
            src_category = map.dest_category
        return target

    def find_dest_ranges(
        self, src_category: str, src_range: range, dest_category: str
    ) -> list[range]:
        return []


@dataclass
class AlmanacMap:
    src_category: str
    dest_category: str

    entries: list[AlmanacMapEntry]

    def find_dest(self, source):
        for entry in self.entries:
            dest = entry.find_dest(source)
            if dest is not None:
                return dest
        return source


@dataclass
class AlmanacMapEntry:
    dest_range_start: int
    src_range_start: int
    range_length: int

    @property
    def src_range(self):
        return range(self.src_range_start, self.src_range_start + self.range_length)

    def find_dest(self, source: int) -> int | None:
        if source in self.src_range:
            return self.dest_range_start + source - self.src_range_start

        return None

    def find_dest_range(self, src_range: range) -> range | None:
        src_intersection = range_intersection(src_range, self.src_range)
        if src_intersection:
            return None  # TODO: this is where I left off
        return None


def solve_for(input_data: str) -> int:
    almanac = parse_almanac(input_data)

    min_location: int = float("inf")  # type: ignore[assignment]
    for seed_range_start, range_length in itertools.batched(almanac.target_seeds, 2):
        for seed in range(seed_range_start, seed_range_start + range_length):
            location = almanac.find_dest(
                src_category="seed",
                src=seed,
                dest_category="location",
            )
            min_location = min(location, min_location)

    return min_location


def parse_almanac(s: str) -> Almanac:
    seed_section, *maps_s = s.split("\n\n")
    seeds = parse_seeds(seed_section)

    parsed_maps = [parse_map(map) for map in maps_s]
    maps = {map.src_category: map for map in parsed_maps}

    return Almanac(seeds, maps)


def parse_seeds(s: str) -> list[int]:
    _, *seeds = s.split()
    return [int(seed) for seed in seeds]


def parse_map(s: str) -> AlmanacMap:
    category_line, *entry_lines = s.splitlines()
    src_category, dest_category = category_line.split()[0].split("-to-")
    entries = [parse_entry(line) for line in entry_lines]
    return AlmanacMap(src_category, dest_category, entries)


def parse_entry(s: str) -> AlmanacMapEntry:
    dest_start, src_start, range_len = (int(i) for i in s.split())
    return AlmanacMapEntry(dest_start, src_start, range_len)


def merge_ranges(ranges: list[range]) -> list[range]:
    merged_ranges: list[range] = []
    for range_ in sorted_ranges(ranges):
        if not merged_ranges or range_.start > merged_ranges[-1].stop:
            merged_ranges.append(range_)
            continue
        start = merged_ranges.pop()
        merged_ranges.append(range(start.start, range_.stop))
    return merged_ranges


def range_intersection(r1: range, r2: range) -> range | None:
    r1, r2 = sorted_ranges([r1, r2])
    if r1.stop <= r2.start:
        return None

    return range(r2.start, r1.stop)


def sorted_ranges(ranges: list[range]) -> list[range]:
    return sorted(ranges, key=lambda r: r.start)


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
