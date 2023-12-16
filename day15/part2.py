# https://adventofcode.com/2023/day/15#part2
from __future__ import annotations

import re
from functools import reduce
from typing import NamedTuple

import pytest

import support


class LensBoxes:
    boxes: list[dict[str, int]]

    def __init__(self):
        self.boxes = [{} for _ in range(256)]

    def insert(self, label: str, focal_length: int) -> None:
        box_number = calculate_hash(label)
        box = self.boxes[box_number]
        box[label] = focal_length

    def remove(self, label: str) -> None:
        box_number = calculate_hash(label)
        box = self.boxes[box_number]
        box.pop(label, None)

    def calculate_total_focusing_power(self) -> int:
        return sum(
            (box_number + 1) * self._box_focusing_power(box)
            for box_number, box in enumerate(self.boxes)
        )

    def _box_focusing_power(self, box: dict[str, int]) -> int:
        return sum(
            slot_number * focal_length
            for slot_number, focal_length in enumerate(box.values(), 1)
        )


class InsertOperation(NamedTuple):
    label: str
    focal_length: int


class RemoveOperation(NamedTuple):
    label: str


Operation = InsertOperation | RemoveOperation


def solve_for(input_data: str) -> int:
    steps = (parse_step(line) for line in input_data.split(","))
    lens_boxes = LensBoxes()
    for step in steps:
        match step:
            case InsertOperation(label, focal_length):
                lens_boxes.insert(label, focal_length)
            case RemoveOperation(label):
                lens_boxes.remove(label)

    return lens_boxes.calculate_total_focusing_power()


def parse_step(line: str) -> Operation:
    insert_pattern = re.compile(r"([a-zA-Z]+)=([0-9]+)")
    remove_pattern = re.compile(r"([a-zA-Z]+)\-")
    if match := insert_pattern.match(line):
        label, focal_length = match.groups()
        return InsertOperation(label, int(focal_length))
    elif match := remove_pattern.match(line):
        [label] = match.groups()
        return RemoveOperation(label)
    else:
        raise ValueError


def calculate_hash(label: str) -> int:
    return reduce(hash_char, label, 0)


def hash_char(acc: int, char: str) -> int:
    assert len(char) == 1
    acc += ord(char)
    acc *= 17
    acc %= 256
    return acc


EXAMPLE_1 = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
EXPECTED_1 = 145


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
