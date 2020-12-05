#!/usr/bin/env python3

from typing import List

input = "input"


def get_id(line: str) -> int:
    row: int = 0
    for i in range(7):
        row <<= 1
        if line[i].lower() == "b":
            row += 1
    col: int = 0
    for i in range(7, 10):
        col <<= 1
        if line[i].lower() == "r":
            col += 1

    id: int = row * 8 + col
    print(line, row, col, id)
    return id


with open(input, "r") as f:
    ids: List[int] = [get_id(line.strip()) for line in f]

ids = sorted(ids)
for i, id in enumerate(ids):
    if ids[i + 1] != id + 1:
        print(id + 1)
        break
