#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set, Tuple, Optional


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


class Direction(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


@dataclass
class Tile:
    id: int
    top: List[str]
    right: List[str]
    bottom: List[str]
    left: List[str]
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

    def add_potential_neighbour(self, d: Direction, n: "Tile", nd: Direction) -> None:
        self.potential_neighbours[d].add((n.id, nd))


def reverse(l: List[str]) -> List[str]:
    x = [e for e in l]
    x.reverse()
    return x


tiles: Dict[int, Tile] = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    tile_infos = input_file.read().split("\n\n")
    for tile_info in tile_infos:
        lines = tile_info.strip().split("\n")
        tile = Tile(
            id=int(lines[0].split(":")[0].split(" ")[1]),
            top=list(lines[1].strip()),
            bottom=reverse(list(lines[10].strip())),
            right=[row[9] for row in lines[1:]],
            left=reverse([row[0] for row in lines[1:]]),
        )
        tiles[tile.id] = tile


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

corner_ids: Set[int] = set()
for tile in tiles.values():
    # print(f"#{tile.id} -> {tile.potential_neighbours}")
    if sum([1 if s else 0 for s in tile.potential_neighbours.values()]) == 2:
        corner_ids.add(tile.id)

print(corner_ids)

prod = 1
for cid in corner_ids:
    prod *= cid

print("Product: ", prod)

# while len(corner_ids) != 4:
#     print("new round")
#     for tile in tiles.values():
#         print(f"#{tile.id} -> {tile.potential_neighbours}")
#         print(f"      -> {({d: (n[0], n[1]) for d, n in tile.neighbours.items()})}")

#     for tile in tiles.values():
#         for direction in Direction:
#             if len(tile.potential_neighbours[direction]) == 1:
#                 n_id, nd = tile.potential_neighbours[direction].pop()
#                 tile.neighbours[direction] = (n_id, nd)
#                 tiles[n_id].neighbours[nd] = (tile.id, direction)

#                 for pnid, pnd in tile.potential_neighbours[direction]:
#                     tiles[pnid].potential_neighbours[pnd] -= set([(tile.id, direction)])
#                 for pnid, pnd in tiles[n_id].potential_neighbours[nd]:
#                     tiles[pnid].potential_neighbours[pnd] -= set([(n_id, nd)])

#         if sum([len(s) for s in tile.potential_neighbours.values()]) == 0 and len(tile.neighbours) == 2:
#             corner_ids.add(tile.id)

# print(corner_ids)
