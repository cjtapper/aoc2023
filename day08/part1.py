# https://adventofcode.com/2023/day/8

from __future__ import annotations

import itertools
import re
from typing import NamedTuple

import pytest

import support

NODE_PATTERN = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")

START_LABEL = "AAA"
DEST_LABEL = "ZZZ"


class NetworkNode(NamedTuple):
    label: str
    left: str
    right: str


def solve_for(input_data: str) -> int:
    instructions, network_s = input_data.split("\n\n")

    parsed_nodes = (parse_node(line) for line in network_s.splitlines())

    network = {node.label: node for node in parsed_nodes}
    current_node = network[START_LABEL]
    for step, instruction in enumerate(itertools.cycle(instructions), 1):
        if instruction == "L":
            current_node = network[current_node.left]
        elif instruction == "R":
            current_node = network[current_node.right]
        else:
            raise ValueError(f"Invalid instruction: {instruction}")
        if current_node.label == DEST_LABEL:
            break

    return step


def parse_node(s: str) -> NetworkNode:
    match = NODE_PATTERN.match(s)
    if not match:
        raise ValueError(f"Could not parse node from '{s}'")
    label, left, right = match.groups()
    return NetworkNode(label, left, right)


EXAMPLE_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED_1 = 2

EXAMPLE_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED_2 = 6


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
