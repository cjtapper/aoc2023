# https://adventofcode.com/2023/day/8#part2

from __future__ import annotations

import itertools
import math
import re
from typing import NamedTuple

import pytest

import support

NODE_PATTERN = re.compile(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)")


class NetworkNode(NamedTuple):
    label: str
    left: str
    right: str


def solve_for(input_data: str) -> int:
    instructions, network_s = input_data.split("\n\n")

    parsed_nodes = (parse_node(line) for line in network_s.splitlines())

    network = {node.label: node for node in parsed_nodes}
    current_nodes = [node for node in network.values() if node.label.endswith("A")]
    steps_required = [-1] * len(current_nodes)
    for step, instruction in enumerate(itertools.cycle(instructions), 1):
        for index, node in enumerate(current_nodes):
            if instruction == "L":
                next_node = network[node.left]
            elif instruction == "R":
                next_node = network[node.right]
            else:
                raise ValueError(f"Invalid instruction: {instruction}")

            if next_node.label.endswith("Z") and steps_required[index] < 0:
                steps_required[index] = step

            current_nodes[index] = next_node
        if all(s > 0 for s in steps_required):
            break

    return math.lcm(*steps_required)


def parse_node(s: str) -> NetworkNode:
    match = NODE_PATTERN.match(s)
    if not match:
        raise ValueError(f"Could not parse node from '{s}'")
    label, left, right = match.groups()
    return NetworkNode(label, left, right)


EXAMPLE_1 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
EXPECTED_1 = 6


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
