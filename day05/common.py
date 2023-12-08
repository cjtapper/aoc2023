from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

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
        elif interval.stop <= parent.interval.start:
            if not parent.left:
                parent.left = IntervalTreeNode[T](interval, value)
            else:
                self._insert(parent.left, interval, value)
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

    def search_by_range(self, key: range) -> T | None:
        """Return first range found that intersects with key"""
        if not self.root:
            return None
        else:
            return self._search_by_range(self.root, key)

    def _search_by_range(self, node: IntervalTreeNode[T], key: range) -> T | None:
        if key.stop <= node.interval.start:
            return self._search_by_range(node.left, key) if node.left else None
        if key.start >= node.interval.stop:
            return self._search_by_range(node.right, key) if node.right else None
        return node.value


@dataclass
class IntervalTreeNode(Generic[T]):
    interval: range
    value: T
    left: IntervalTreeNode[T] | None = None
    right: IntervalTreeNode[T] | None = None


@dataclass
class Almanac:
    maps: dict[str, AlmanacMap]

    def find_dest(self, src_category: str, src: int, dest_category: str) -> int:
        target = src
        while src_category != dest_category:
            map = self.maps[src_category]
            target = map.find_dest(target)
            src_category = map.dest_category
        return target

    def find_dest_by_range(
        self, src_category: str, src_range: range, dest_category: str
    ) -> list[range]:
        result = [src_range]
        target_ranges = []
        while src_category != dest_category:
            map = self.maps[src_category]
            target_ranges = result
            result = []

            while target_ranges:
                target = target_ranges.pop()
                dest = map.find_dest_ranges(target)
                result.extend(dest)
            src_category = map.dest_category
        return result


@dataclass
class AlmanacMap:
    src_category: str
    dest_category: str

    entries: IntervalTree[AlmanacMapEntry]

    def find_dest(self, source: int) -> int:
        map_entry = self.entries.search(source)
        if not map_entry:
            return source
        dest = map_entry.find_dest(source)
        return dest or source

    def find_dest_ranges(self, src_range: range) -> list[range]:
        results = []
        target_ranges = [src_range]
        while target_ranges:
            target = target_ranges.pop()
            map_entry = self.entries.search_by_range(target)
            if not map_entry:
                results.append(target)
            else:
                intersection = range_intersection(map_entry.src_range, target)
                if not intersection:
                    results.append(target)
                    continue

                intersection_start_offset = (
                    intersection.start - map_entry.src_range.start
                )
                dest_start = map_entry.dest_range.start + intersection_start_offset
                results.append(range(dest_start, dest_start + len(intersection)))
                diff = diff_ranges(target, map_entry.src_range)
                target_ranges.extend(diff)

        return results


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


def parse_almanac(s: str) -> Almanac:
    _, *maps_s = s.split("\n\n")

    parsed_maps = [parse_map(map) for map in maps_s]
    maps = {map.src_category: map for map in parsed_maps}

    return Almanac(maps)


def parse_map(s: str) -> AlmanacMap:
    category_line, *entry_lines = s.splitlines()
    src_category, dest_category = category_line.split()[0].split("-to-")
    entries: IntervalTree[AlmanacMapEntry] = IntervalTree()
    parsed_entries = (parse_entry(line) for line in entry_lines)
    for entry in parsed_entries:
        entries.insert(entry.src_range, entry)
    return AlmanacMap(src_category, dest_category, entries)


def parse_entry(s: str) -> AlmanacMapEntry:
    dest_start, src_start, range_len = (int(i) for i in s.split())
    return AlmanacMapEntry(src_start, dest_start, range_len)


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

    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


def diff_ranges(r1: range, r2: range) -> list[range]:
    """Returns portions of r1 that do not intersect r2"""
    result: list[range] = []
    if r1.start < r2.start:
        result.append(range(r1.start, min(r1.stop, r2.start)))
    if r1.stop > r2.stop:
        result.append(range(max(r1.start, r2.stop), r1.stop))
    return result


def sorted_ranges(ranges: list[range]) -> list[range]:
    return sorted(ranges, key=lambda r: r.start)
