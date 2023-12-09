# https://adventofcode.com/2023/day/9
from __future__ import annotations

import itertools

import pytest

import support


def solve_for(input_data: str) -> int:
    sequences = (parse_history(line) for line in input_data.splitlines())

    return sum(predict_next(seq) for seq in sequences)


def parse_history(line: str) -> list[int]:
    return [int(c) for c in line.split()]


def predict_next(seq: list[int]) -> int:
    prediction = seq[-1]
    while not all(el == seq[0] for el in seq):
        seq = get_diffs(seq)
        prediction += seq[-1]
    return prediction


def get_diffs(seq: list[int]) -> list[int]:
    result: list[int] = []
    for a, b in itertools.pairwise(seq):
        result.append(b - a)
    return result


EXAMPLE_1 = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
EXPECTED_1 = 114


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
