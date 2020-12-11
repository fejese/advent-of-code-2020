#!/usr/bin/env python3

from enum import Enum
from typing import List
from pprint import pprint


# INPUT = "test-input"
# INPUT = "test-input-2"
INPUT = "input"

class Seat(Enum):
    FLOOR=0
    EMPTY=1
    TAKEN=2

grid: List[List[Seat]] = []
height = 0
width = 0
with open(INPUT, "r") as f:
    lines = [line.strip() for line in f]
    height = len(lines)
    width = len(lines[0])
    for x in range(width):
        col: List[Seat] = []
        for y in range(height):
            if lines[y][x] == ".":
                col.append(Seat.FLOOR)
            elif lines[y][x] == "L":
                col.append(Seat.EMPTY)
            else:
                col.append(Seat.TAKEN)
        grid.append(col)

def get_adjacent(grid: List[List[Seat]], x: int, y: int) -> List[Seat]:
    width = len(grid)
    height = len(grid[0])
    adjacent: List[Seat] = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if x + dx < 0 or x + dx >= width:
                continue
            if y + dy < 0 or y + dy >= height:
                continue
            adjacent.append(grid[x + dx][y + dy])

    return adjacent

def step(grid: List[List[Seat]]) -> List[List[Seat]]:
    width = len(grid)
    height = len(grid[0])
    new_grid: List[List[Seat]] = []
    for x in range(width):
        new_grid.append([Seat.FLOOR] * height)

    for x in range(width):
        for y in range(height):
            if grid[x][y] == Seat.FLOOR:
                continue
            adjacent = get_adjacent(grid, x, y)
            taken_adjacent = len([seat for seat in adjacent if seat == Seat.TAKEN])
            if grid[x][y] == Seat.EMPTY:
                new_grid[x][y] = Seat.TAKEN if taken_adjacent == 0 else Seat.EMPTY
            else:
                new_grid[x][y] = Seat.EMPTY if taken_adjacent >= 4 else Seat.TAKEN
            # print(x, y, grid[x][y], new_grid[x][y], adjacent, taken_adjacent)

    return new_grid

def get_taken_count(grid: List[List[Seat]]) -> int:
    taken_count = 0
    width = len(grid)
    height = len(grid[0])

    for x in range(width):
        for y in range(height):
            if grid[x][y] == Seat.TAKEN:
                taken_count += 1

    return taken_count


steps = 0
while True:
    new_grid = step(grid)
    steps += 1
    # if steps == 2:
    #     pprint(new_grid)
    #     break
    if new_grid == grid:
        print(f"Grid is same after step #{steps} as before")
        break
    grid = new_grid

print(get_taken_count(grid))
