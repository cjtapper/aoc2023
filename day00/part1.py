from __future__ import annotations

import argparse
import os.path

import support


def solve_for(input_data: str) -> int:
    numbers = (parse_line(line) for line in input_data.splitlines())
    for n in numbers:
        pass

    # TODO: implement solution here!
    return 0


def parse_line(line: str) -> int:
    return int(line)


INPUT1 = """\

"""
EXPECTED1 = 0

assert solve_for(INPUT1) == EXPECTED1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        nargs="?",
        default=os.path.join(os.path.dirname(__file__), "input.txt"),
    )
    args = parser.parse_args()

    input_data = support.slurp(args.input_file)

    print(solve_for(input_data))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
