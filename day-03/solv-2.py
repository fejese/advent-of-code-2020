#!/usr/bin/env python3

from typing import List

input = "input"

with open(input, "r") as f:
    map: List[str] = [line.strip() for line in f]
    height = len(map)
    width = len(map[0])

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
tree_product = 1
for slope in slopes:
    pos = (0, 0)
    tree_count = 0
    while pos[1] < height:
        if map[pos[1]][pos[0] % width] == "#":
            tree_count += 1
        pos = (pos[0] + slope[0], pos[1] + slope[1])
    print(slope, tree_count)
    tree_product *= tree_count
print(tree_product)
