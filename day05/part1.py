# https://adventofcode.com/2023/day/5

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

import pytest

import support

T = TypeVar("T")


class IntervalTree(Generic[T]):
    root: IntervalTreeNode[T] | None = None

    def insert(self, interval: range, value: T) -> None:
        if self.root:
            self._insert(self.root, interval, value)
        else:
            self.root = IntervalTreeNode[T](interval, value)

    def _insert(self, parent: IntervalTreeNode[T], interval: range, value: T) -> None:
        if interval.start in parent.interval or interval.stop - 1 in parent.interval:
            raise NotImplementedError("Overlapping ranges are not supported")
        if interval.start >= parent.interval.stop:
            if not parent.right:
                parent.right = IntervalTreeNode[T](interval, value)
            else:
                self._insert(parent.right, interval, value)
        elif interval.stop < parent.interval.start:
            if not parent.left:
                parent.left = IntervalTreeNode[T](interval, value)
            else:
                self._insert(parent.left, interval, value)
        breakpoint()
        return None

    def search(self, key: int) -> T | None:
        if not self.root:
            return None
        else:
            return self._search(self.root, key)

    def _search(self, node: IntervalTreeNode[T], key: int) -> T | None:
        if key < node.interval.start:
            return self._search(node.left, key) if node.left else None
        if key >= node.interval.stop:
            return self._search(node.right, key) if node.right else None
        return node.value


@dataclass
class IntervalTreeNode(Generic[T]):
    interval: range
    value: T
    left: IntervalTreeNode[T] | None = None
    right: IntervalTreeNode[T] | None = None


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


@dataclass
class AlmanacMap:
    src_category: str
    dest_category: str

    entries: IntervalTree[AlmanacMapEntry]

    def find_dest(self, source: int):
        map_entry = self.entries.search(source)
        return map_entry.find_dest(source) if map_entry else source


@dataclass
class AlmanacMapEntry:
    dest_range: range
    src_range: range

    def __init__(self, src_start: int, dest_start: int, range_length: int) -> None:
        self.src_range = range(src_start, src_start + range_length)
        self.dest_range = range(dest_start, dest_start + range_length)

    def find_dest(self, source: int) -> int | None:
        if source in self.src_range:
            return self.dest_range.start + source - self.src_range.start

        return None


def solve_for(input_data: str) -> int:
    almanac = parse_almanac(input_data)

    locations = []
    for seed in almanac.target_seeds:
        locations.append(almanac.find_dest("seed", seed, "location"))

    return min(locations)


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
    entries: IntervalTree[AlmanacMapEntry] = IntervalTree()
    parsed_entries = (parse_entry(line) for line in entry_lines)
    for entry in parsed_entries:
        entries.insert(entry.src_range, entry)
    breakpoint()
    return AlmanacMap(src_category, dest_category, entries)


def parse_entry(s: str) -> AlmanacMapEntry:
    dest_start, src_start, range_len = (int(i) for i in s.split())
    return AlmanacMapEntry(src_start, dest_start, range_len)


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
