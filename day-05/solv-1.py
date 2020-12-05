#!/usr/bin/env python3

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


max_id: int = -1

with open(input, "r") as f:
    for line in f:
        id: int = get_id(line.strip())
        max_id = max(id, max_id)

print(max_id)
