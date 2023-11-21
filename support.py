from __future__ import annotations


def slurp(filename: str) -> str:
    with open(filename) as f:
        return f.read()
