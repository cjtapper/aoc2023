# https://adventofcode.com/2023/day/1

from __future__ import annotations

import pytest

import support


def solve_for(input_data: str) -> int:
    calibration_values = (
        parse_calibration_value(line) for line in input_data.splitlines()
    )

    return sum(calibration_values)


def parse_calibration_value(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    return int(digits[0] + digits[-1])


EXAMPLE_1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
EXPECTED_1 = 142


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
    ],
)
def test_example1(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
