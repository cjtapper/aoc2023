from __future__ import annotations

import support


def solve_for(input_data: str) -> int:
    values = (parse_line(line) for line in input_data.splitlines())
    for v in values:
        pass

    # TODO: implement solution here!
    return 0


def parse_line(line: str) -> str:
    return line


INPUT1 = """\

"""
EXPECTED1 = 0

assert solve_for(INPUT1) == EXPECTED1


if __name__ == "__main__":
    support.cli(__file__, solve_for)
