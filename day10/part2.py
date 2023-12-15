# https://adventofcode.com/2023/day/10#part2

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generator, Literal, NamedTuple

import pytest

import support

Pipe = Literal["|", "-", "L", "J", "7", "F"]

CONNECTS_EAST = ("L", "F", "-")
CONNECTS_WEST = ("J", "7", "-")
CONNECTS_NORTH = ("J", "L", "|")
CONNECTS_SOUTH = ("7", "F", "|")


class Position(NamedTuple):
    x: int
    y: int


@dataclass
class Grid:
    grid: list[tuple[str]]

    def at(self, position: Position) -> str:
        return self.grid[position.x][position.y]

    def iter_positions(self) -> Generator[Position, None, None]:
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                yield Position(x, y)

    @classmethod
    def from_str(cls, input_data: str) -> Grid:
        return cls(
            # transposed so we can address by x, y
            grid=list(zip(*input_data.splitlines()))
        )


def solve_for(input_data: str) -> int:
    grid = Grid.from_str(input_data)
    start_position = find_entry_position(grid)
    assert start_position is not None

    visited: dict[Position, int] = {}
    unvisited = deque[tuple[Position, int]]()
    unvisited.append((start_position, 0))

    # Breadth first search
    while unvisited:
        current_position, distance = unvisited.popleft()

        # Already visited, first seen distance would have been farthest
        # from beginning
        if current_position in visited:
            return visited[current_position]

        visited[current_position] = distance
        connections = find_connections(grid, current_position)
        for connection in connections:
            if connection not in visited:
                unvisited.append((connection, distance + 1))

    assert (
        False
    ), "We should never reach this point within the constraints of the puzzle"


def parse_line(line: str) -> str:
    return line


def find_entry_position(grid: Grid) -> Position | None:
    for position in grid.iter_positions():
        if grid.at(position) == "S":
            return position
    return None


def determine_pipe(grid: Grid, pipe: Position) -> Pipe:
    connects_north = grid.at(Position(pipe.x, pipe.y - 1)) in CONNECTS_SOUTH
    connects_south = grid.at(Position(pipe.x, pipe.y + 1)) in CONNECTS_NORTH
    connects_east = grid.at(Position(pipe.x + 1, pipe.y)) in CONNECTS_WEST
    connects_west = grid.at(Position(pipe.x - 1, pipe.y)) in CONNECTS_EAST

    if connects_north and connects_south:
        return "|"
    elif connects_north and connects_east:
        return "L"
    elif connects_north and connects_west:
        return "J"
    elif connects_south and connects_west:
        return "7"
    elif connects_south and connects_east:
        return "F"
    elif connects_east and connects_west:
        return "-"
    else:
        raise ValueError("Invalid pipe")


def find_connections(grid: Grid, pipe: Position) -> list[Position]:
    pipe_shape = grid.at(pipe)
    if pipe_shape == "S":
        pipe_shape = determine_pipe(grid, pipe)
    candidate_connections = []

    if pipe_shape == "-":
        candidate_connections.extend(
            [Position(pipe.x - 1, pipe.y), Position(pipe.x + 1, pipe.y)]
        )
    elif pipe_shape == "|":
        candidate_connections.extend(
            [Position(pipe.x, pipe.y - 1), Position(pipe.x, pipe.y + 1)]
        )
    elif pipe_shape == "J":
        candidate_connections.extend(
            [Position(pipe.x, pipe.y - 1), Position(pipe.x - 1, pipe.y)]
        )
    elif pipe_shape == "L":
        candidate_connections.extend(
            [Position(pipe.x, pipe.y - 1), Position(pipe.x + 1, pipe.y)]
        )
    elif pipe_shape == "F":
        candidate_connections.extend(
            [Position(pipe.x + 1, pipe.y), Position(pipe.x, pipe.y + 1)]
        )
    elif pipe_shape == "7":
        candidate_connections.extend(
            [Position(pipe.x - 1, pipe.y), Position(pipe.x, pipe.y + 1)]
        )
    else:
        raise ValueError("Invalid pipe")

    return candidate_connections


EXAMPLE_1 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
EXPECTED_1 = 4

EXAMPLE_2 = """\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""
EXPECTED_2 = 4

EXAMPLE_3 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
EXPECTED_3 = 8


@pytest.mark.parametrize(
    "input_data,expected",
    [
        (EXAMPLE_1, EXPECTED_1),
        (EXAMPLE_2, EXPECTED_2),
        (EXAMPLE_3, EXPECTED_3),
    ],
)
@pytest.mark.skip("Haven't solved this yet")
def test_example(input_data, expected):
    assert solve_for(input_data) == expected


if __name__ == "__main__":
    support.cli(__file__, solve_for)
