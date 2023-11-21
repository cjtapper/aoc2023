from __future__ import annotations

import argparse
import os.path
from typing import Callable, TypeAlias

Solver: TypeAlias = Callable[[str], object]


def cli(module_filename: str, solver: Solver) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        nargs="?",
        default=os.path.join(os.path.dirname(module_filename), "input.txt"),
    )
    args = parser.parse_args()

    input_data = slurp(args.input_file)

    print(solver(input_data))

    raise SystemExit(0)


def slurp(filename: str) -> str:
    """Read a whole file into memory"""

    with open(filename) as f:
        return f.read()
