#!/usr/bin/env python3

from enum import Enum
from typing import Dict, List, Tuple, Optional
from pprint import pprint


# INPUT = "test-input"
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

adjacency_cache: Dict[Tuple[int, int, int, int], Optional[Tuple[int, int]]] = {}

def get_adjacent(grid: List[List[Seat]], x: int, y: int) -> List[Seat]:
    width = len(grid)
    height = len(grid[0])
    adjacent: List[Seat] = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            adjacency_cache_key = (x, y, dx, dy)
            if adjacency_cache_key not in adjacency_cache:
                tdx, tdy = dx, dy
                while True:
                    if tdx == 0 and tdy == 0:
                        adjacency_cache[adjacency_cache_key] = None
                        break
                    elif x + tdx < 0 or x + tdx >= width:
                        adjacency_cache[adjacency_cache_key] = None
                        break
                    elif y + tdy < 0 or y + tdy >= height:
                        adjacency_cache[adjacency_cache_key] = None
                        break
                    elif grid[x + tdx][y + tdy] != Seat.FLOOR:
                        adjacency_cache[adjacency_cache_key] = (x + tdx, y + tdy)
                        break
                    tdx += dx
                    tdy += dy

            adjacenct_coord = adjacency_cache[adjacency_cache_key]
            if adjacenct_coord:
                adjacent.append(grid[adjacenct_coord[0]][adjacenct_coord[1]])

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
                new_grid[x][y] = Seat.EMPTY if taken_adjacent >= 5 else Seat.TAKEN

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
    if new_grid == grid:
        print(f"Grid is same after step #{steps} as before")
        break
    grid = new_grid

print(get_taken_count(grid))
