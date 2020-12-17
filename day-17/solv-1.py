#!/usr/bin/env python3

from pprint import pprint
from typing import Dict, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

Cell = Tuple[int, int, int]

actives: Set[Cell] = set()
with open(INPUT_FILE_NAME, "r") as input_file:
    z = 0
    y = 0
    for line in input_file:
        actives.update([(x, y, z) for x, val in enumerate(line.strip()) if val == "#"])
        y += 1


def get_neighbours(cell: Cell) -> Set[Cell]:
    neighbours: Set[Cell] = set(
        [
            (cell[0] + dx, cell[1] + dy, cell[2] + dz)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            for dz in [-1, 0, 1]
            if (dx != 0 or dy != 0 or dz != 0)
        ]
    )
    return neighbours


def step(active_cells: Set[Cell]) -> Set[Cell]:
    active_neighbour_count: Dict[Cell, int] = {}
    for active in active_cells:
        for neighbour in get_neighbours(active):
            if neighbour not in active_neighbour_count:
                active_neighbour_count[neighbour] = 0
            active_neighbour_count[neighbour] += 1

    new_actives: Set[Cell] = set()
    for cell, cnt in active_neighbour_count.items():
        if cell in active_cells and cnt in (2, 3):
            new_actives.add(cell)
        elif cell not in active_cells and cnt == 3:
            new_actives.add(cell)
    return new_actives


print("cycle=0")
# pprint(actives)
print(f"Count: {len(actives)}")
for cycle in range(1, 7):
    actives = step(actives)
    print(f"cycle={cycle}")
    # pprint(actives)
    print(f"Count: {len(actives)}")
