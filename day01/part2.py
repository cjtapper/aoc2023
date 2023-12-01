from __future__ import annotations

import re

import pytest

import support

SPELLED_OUT_DIGITS = {
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

DIGIT_PATTERN = "|".join([*SPELLED_OUT_DIGITS.keys(), r"[0-9]"])


def solve_for(input_data: str) -> int:
    calibration_values = (
        parse_calibration_value(line) for line in input_data.splitlines()
    )

    return sum(calibration_values)


def parse_calibration_value(line: str) -> int:
    digits = find_digits(line)
    return int(unspell_digit(digits[0]) + unspell_digit(digits[-1]))


def find_digits(line: str) -> list[str]:
    # Python's re.findall() function only finds NON-OVERLAPPING matches.
    # This means that if we try to find digits in a string like "twone",
    # we would only find "two".
    # To get around this, we can use a lookahead assertion (denoted by
    # (?=...).
    # So essentially what we are doing here is matching zero length
    # strings that are immediately followed by our digit pattern. This
    # returns two match groups:
    #   0: the zero length string
    #   1: the string matching our lookahead pattern
    pattern = re.compile(rf"(?=({DIGIT_PATTERN}))")
    return [match.group(1) for match in pattern.finditer(line)]


def unspell_digit(digit: str) -> str:
    return SPELLED_OUT_DIGITS.get(digit, digit)


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