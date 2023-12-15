# https://adventofcode.com/2023/day/15

from __future__ import annotations

from functools import reduce

import pytest

import support


def solve_for(input_data: str) -> int:
    steps = input_data.strip().split(",")

    return sum(reduce(calculate_hash, step, 0) for step in steps)


def calculate_hash(acc: int, char: str) -> int:
    assert len(char) == 1
    acc += ord(char)
    acc *= 17
    acc %= 256
    return acc


EXAMPLE_1 = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
EXPECTED_1 = 1320


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
