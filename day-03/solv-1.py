#!/usr/bin/env python3

from typing import List

input = "input"

with open(input, "r") as f:
    map: List[str] = [line.strip() for line in f]
    height = len(map)
    width = len(map[0])

pos = (0, 0)
tree_count = 0
while pos[1] < height:
    if map[pos[1]][pos[0] % width] == "#":
        tree_count += 1
    pos = (pos[0] + 3, pos[1] + 1)

print(tree_count)
