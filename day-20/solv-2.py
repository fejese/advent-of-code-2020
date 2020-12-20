#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from math import sqrt
from typing import Dict, List, Set, Tuple, Optional


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

MONSTER_LEN: int = 20
MONSTER_PATS: List[re.Pattern] = [
    re.compile(r"^(..................)#(.)"),
    re.compile(r"^#(....)##(....)##(....)###"),
    re.compile(r"^(.)#(..)#(..)#(..)#(..)#(..)#(...)"),
]
MONSTER_REPL: List[str] = [
    r"\1O\2",
    r"O\1OO\2OO\3OOO",
    r"\1O\2O\3O\4O\5O\6O\7",
]


Coord = Tuple[int, int]


def reverse(l: str) -> str:
    x = [e for e in l]
    x.reverse()
    return "".join(x)


class Direction(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

    def opposite(self) -> "Direction":
        return {
            Direction.TOP: Direction.BOTTOM,
            Direction.RIGHT: Direction.LEFT,
            Direction.BOTTOM: Direction.TOP,
            Direction.LEFT: Direction.RIGHT,
        }.get(self)

    def left(self) -> "Direction":
        return {
            Direction.TOP: Direction.LEFT,
            Direction.RIGHT: Direction.TOP,
            Direction.BOTTOM: Direction.RIGHT,
            Direction.LEFT: Direction.BOTTOM,
        }.get(self)

    def right(self) -> "Direction":
        return {
            Direction.TOP: Direction.RIGHT,
            Direction.RIGHT: Direction.BOTTOM,
            Direction.BOTTOM: Direction.LEFT,
            Direction.LEFT: Direction.TOP,
        }.get(self)

    def flipped_h(self) -> "Direction":
        return {
            Direction.TOP: Direction.TOP,
            Direction.RIGHT: Direction.LEFT,
            Direction.BOTTOM: Direction.BOTTOM,
            Direction.LEFT: Direction.RIGHT,
        }.get(self)

    def flipped_v(self) -> "Direction":
        return {
            Direction.TOP: Direction.BOTTOM,
            Direction.RIGHT: Direction.RIGHT,
            Direction.BOTTOM: Direction.TOP,
            Direction.LEFT: Direction.LEFT,
        }.get(self)


class Img(list, List[str]):
    def __init__(self, *args, **kwargs) -> None:
        list.__init__(self, *args, **kwargs)

    def trimmed(self) -> "Img":
        return Img(line[1:-1] for line in self[1:-1])

    def flipped_h(self) -> "Img":
        return Img(reverse(line) for line in self)

    def flipped_v(self) -> "Img":
        return Img(self[i] for i in range(len(self) - 1, -1, -1))

    def rotated_right(self) -> "Img":
        rotated = [
            "".join([self[len(self) - 1 - x][y] for x in range(len(self))])
            for y in range(len(self))
        ]
        return Img(rotated)

    def print(self) -> None:
        for row in self:
            print(row)

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self])


@dataclass
class Tile:
    id: int
    top: List[str]
    right: List[str]
    bottom: List[str]
    left: List[str]
    img: Img
    potential_neighbours: Dict[Direction, Set[Tuple[int, Direction]]] = field(
        default_factory=lambda: Tile.default_potential_neighbours_factory()
    )
    neighbours: Dict[Direction, Tuple[int, Direction]] = field(default_factory=dict)

    @classmethod
    def default_potential_neighbours_factory(
        cls,
    ) -> Dict[Direction, Set[Tuple[int, Direction]]]:
        return {d: set() for d in Direction}

    def get_sides(self) -> Dict[Direction, List[str]]:
        return {
            Direction.TOP: self.top,
            Direction.RIGHT: self.right,
            Direction.BOTTOM: self.bottom,
            Direction.LEFT: self.left,
        }

    def set_sides(self, sides: Dict[Direction, List[str]]) -> None:
        self.top = sides.get(Direction.TOP)
        self.right = sides.get(Direction.RIGHT)
        self.bottom = sides.get(Direction.BOTTOM)
        self.left = sides.get(Direction.LEFT)

    def add_potential_neighbour(self, d: Direction, n: "Tile", nd: Direction) -> None:
        self.potential_neighbours[d].add((n.id, nd))

    def rotate_right(self, tiles: Dict[int, "Tile"]):
        # print(f"rotating right: {self.id}")
        self.set_sides({d.right(): side for d, side in self.get_sides().items()})
        self.img = self.img.rotated_right()

        self.neighbours = {d.right(): self.neighbours.get(d) for d in Direction}

    def flip_h(self, tiles: Dict[int, "Tile"]):
        # print(f"flipping h: {self.id}")
        self.set_sides(
            {d.flipped_h(): reverse(side) for d, side in self.get_sides().items()}
        )
        self.img = self.img.flipped_h()
        self.neighbours = {d: self.neighbours.get(d.flipped_h()) for d in Direction}

    def flip_v(self, tiles: Dict[int, "Tile"]):
        # print(f"flipping v: {self.id}")
        self.set_sides(
            {d.flipped_v(): reverse(side) for d, side in self.get_sides().items()}
        )
        self.img = self.img.flipped_v()
        self.neighbours = {d: self.neighbours.get(d.flipped_v()) for d in Direction}


# Input

tiles: Dict[int, Tile] = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    tile_infos = input_file.read().split("\n\n")
    for tile_info in tile_infos:
        lines = [line.strip() for line in tile_info.strip().split("\n")]
        tile = Tile(
            id=int(lines[0].split(":")[0].split(" ")[1]),
            top="".join(list(lines[1].strip())),
            bottom=reverse(list(lines[10].strip())),
            right="".join([row[-1] for row in lines[1:]]),
            left=reverse([row[0] for row in lines[1:]]),
            img=Img(lines[1:]),
        )
        tiles[tile.id] = tile

GRID_SIZE = int(sqrt(len(tiles)))
CELL_SIZE = len(list(tiles.values())[0].img) - 2

# Find all potential neighbours

visited: Set[Tuple[int, int]] = set()
for ti, tile_i in tiles.items():
    for tj, tile_j in tiles.items():
        if ti == tj:
            continue
        visited_key = (min(ti, tj), max(ti, tj))
        if visited_key in visited:
            continue
        visited.add(visited_key)

        for direction_i, side_i in tile_i.get_sides().items():
            for direction_j, side_j in tile_j.get_sides().items():
                if side_i == reverse(side_j) or side_i == side_j:
                    tile_i.add_potential_neighbour(direction_i, tile_j, direction_j)
                    tile_j.add_potential_neighbour(direction_j, tile_i, direction_i)


# Find corner elements

corner_ids: Set[int] = set()
for tile in tiles.values():
    if sum([1 if s else 0 for s in tile.potential_neighbours.values()]) == 2:
        corner_ids.add(tile.id)

# Find neighbours for all tiles

while not all(
    sum(len(side) for side in tile.potential_neighbours.values()) == 0
    for tile in tiles.values()
):
    for tile in tiles.values():
        for direction in Direction:
            if len(tile.potential_neighbours[direction]) == 1:
                n_id, nd = tile.potential_neighbours[direction].pop()
                tile.neighbours[direction] = (n_id, nd)
                tiles[n_id].neighbours[nd] = (tile.id, direction)

                for pnid, pnd in tile.potential_neighbours[direction]:
                    tiles[pnid].potential_neighbours[pnd] -= set([(tile.id, direction)])
                for pnid, pnd in tiles[n_id].potential_neighbours[nd]:
                    tiles[pnid].potential_neighbours[pnd] -= set([(n_id, nd)])

# Place tiles

coord_to_tile: Dict[Coord, int] = {}


class Map(list, List[str]):
    def __init__(self, grid_size: int, cell_size: int) -> None:
        self.cell_size = cell_size
        self.grid_size = grid_size
        size = grid_size * cell_size
        list.__init__(self, ["_" * size for _ in range(size)])

    def add(self, tile: Tile, c: Coord) -> None:
        # print(f"Adding {tile.id} as c: {c}")
        x0 = c[0] * self.cell_size
        y0 = c[1] * self.cell_size
        img = tile.img.trimmed()
        for dy in range(self.cell_size):
            self[y0 + dy] = (
                self[y0 + dy][:x0] + img[dy] + self[y0 + dy][x0 + self.cell_size :]
            )

    def flip_h(self) -> "Img":
        flipped = [reverse(line) for line in self]
        self.clear()
        self.extend(flipped)

    def flip_v(self) -> None:
        flipped = [self[i] for i in range(len(self) - 1, -1, -1)]
        self.clear()
        self.extend(flipped)

    def rotate_right(self) -> None:
        rotated = [
            "".join([self[len(self) - 1 - x][y] for x in range(len(self))])
            for y in range(len(self))
        ]
        self.clear()
        self.extend(rotated)

    def print(self) -> None:
        for row in self:
            print(row)

    def find_monsters(self) -> int:
        monsters = 0
        for y in range(GRID_SIZE * CELL_SIZE - len(MONSTER_PATS) + 1):
            for x in range(GRID_SIZE * CELL_SIZE - MONSTER_LEN + 1):
                if all(
                    MONSTER_PATS[pi].match(self[y + pi][x:])
                    for pi in range(len(MONSTER_PATS))
                ):
                    for pi in range(len(MONSTER_PATS)):
                        self[y + pi] = self[y + pi][:x] + MONSTER_PATS[pi].sub(
                            MONSTER_REPL[pi], self[y + pi][x:]
                        )
                    monsters += 1
                    print(f"Found monster at ({x}, {y})")

        return monsters

    def find_all_monsters(self) -> None:
        print("Searching default rotations")
        for _ in range(4):
            m = self.find_monsters()
            print(f"Found {m} monsters")
            self.rotate_right()
        self.flip_h()
        print("Flipped horizontally")
        for _ in range(4):
            m = self.find_monsters()
            print(f"Found {m} monsters")
            self.rotate_right()
        self.flip_h()
        self.flip_v()
        print("Flipped vertically")
        for _ in range(4):
            m = self.find_monsters()
            print(f"Found {m} monsters")
            self.rotate_right()
        self.flip_v()

    def count_waves(self):
        return sum(line.count("#") for line in self)


map: Map = Map(GRID_SIZE, CELL_SIZE)
remaining_ids = set(tiles.keys())

try:
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            coord = (x, y)
            if coord == (0, 0):
                topleft = tiles[list(corner_ids)[3]]
                while not topleft.neighbours.get(
                    Direction.RIGHT
                ) or not topleft.neighbours.get(Direction.BOTTOM):
                    topleft.rotate_right(tiles)
                coord_to_tile[coord] = topleft.id
                map.add(topleft, coord)
                remaining_ids.remove(topleft.id)
                continue
            if x == 0:
                prev_coord = (0, y - 1)
                prev_side_dir = Direction.BOTTOM
                exp_side_dir = Direction.TOP
                flip_method = Tile.flip_h
            else:
                prev_coord = (x - 1, y)
                prev_side_dir = Direction.RIGHT
                exp_side_dir = Direction.LEFT
                flip_method = Tile.flip_v

            prev_tile_id = coord_to_tile[prev_coord]
            prev_tile = tiles[prev_tile_id]
            prev_side = prev_tile.get_sides()[prev_side_dir]

            tile = None
            tile_id = None
            side_dir = None
            for potential_tid in remaining_ids:
                if tile:
                    break
                potential_tile = tiles[potential_tid]
                potential_sides = potential_tile.get_sides()
                for potential_side_dir, potential_side in potential_sides.items():
                    if prev_side in (potential_side, "".join(reverse(potential_side))):
                        side_dir = potential_side_dir
                        tile_id = potential_tid
                        tile = potential_tile
                        break

            if not tile:
                print(remaining_ids)
                for rid in remaining_ids:
                    print(rid)
                    tiles[rid].img.print()
                raise

            while prev_side not in (
                tile.get_sides()[exp_side_dir],
                "".join(reverse(tile.get_sides()[exp_side_dir])),
            ):
                tile.rotate_right(tiles)

            side = tile.get_sides()[exp_side_dir]

            if prev_side == side:
                flip_method(tile, tiles)

            coord_to_tile[coord] = tile_id
            map.add(tile, coord)
            remaining_ids.remove(tile_id)
except Exception as e:
    raise
finally:
    print(coord_to_tile)
    map.print()

map.find_all_monsters()
map.print()
print("Waves: ", map.count_waves())
