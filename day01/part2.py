# https://adventofcode.com/2023/day/1#part2

from __future__ import annotations

import re

import pytest

import support

WORDS_TO_DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

DIGIT_PATTERN = "|".join([*WORDS_TO_DIGITS.keys(), r"[0-9]"])


def solve_for(input_data: str) -> int:
    calibration_values = (
        parse_calibration_value(line) for line in input_data.splitlines()
    )

    return sum(calibration_values)


def parse_calibration_value(line: str) -> int:
    digits = find_digits(line)
    return int(translate_digit(digits[0]) + translate_digit(digits[-1]))


def find_digits(line: str) -> list[str]:
    # Use lookahead (?=...) to get overlapping matches
    overlapping_digits_pattern = re.compile(rf"(?=({DIGIT_PATTERN}))")
    return overlapping_digits_pattern.findall(line)


def translate_digit(digit: str) -> str:
    return WORDS_TO_DIGITS.get(digit, digit)


EXAMPLE_1 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
EXPECTED_1 = 281

EXAMPLE_2 = "91twonelt"
EXPECTED_2 = 91


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
        (EXAMPLE_2, EXPECTED_2),
    ],
)
def test_example(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
