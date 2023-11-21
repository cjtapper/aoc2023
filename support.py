from __future__ import annotations


def slurp(filename: str) -> str:
    """Read a whole file into memory"""

    with open(filename) as f:
        return f.read()
