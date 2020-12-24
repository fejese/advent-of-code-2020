#!/usr/bin/env python3

from enum import Enum, auto
from typing import List, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

Coord = Tuple[int, int]


class D(Enum):
    # e, se, sw, w, nw, and ne
    E = auto()
    SE = auto()
    SW = auto()
    W = auto()
    NW = auto()
    NE = auto()

    def __str__(self) -> str:
        return self.name

    @property
    def coord(self) -> Coord:
        return {
            D.E: (1, 0),
            D.SE: (1, -1),
            D.SW: (0, -1),
            D.W: (-1, 0),
            D.NW: (-1, 1),
            D.NE: (0, 1),
        }.get(self)

    @classmethod
    def parse(cls, line: str) -> List["D"]:
        ds: List[D] = []
        line = line.upper()
        while line:
            d: D
            if line.startswith("E"):
                d = D.E
            elif line.startswith("SE"):
                d = D.SE
            elif line.startswith("SW"):
                d = D.SW
            elif line.startswith("W"):
                d = D.W
            elif line.startswith("NW"):
                d = D.NW
            elif line.startswith("NE"):
                d = D.NE
            else:
                raise ValueError(f"Line doesn't start with a valid direction: {line}")
            ds.append(d)
            line = line[len(str(d)) :]
        return ds

    @classmethod
    def target(cls, line: str) -> Coord:
        ds = cls.parse(line)
        pos: Coord = (0, 0)
        for d in ds:
            pos = (pos[0] + d.coord[0], pos[1] + d.coord[1])
        return pos


turned: Set[Coord] = set()
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        target = D.target(line.strip())
        if target in turned:
            turned.remove(target)
        else:
            turned.add(target)


def get_neighbours(tile: Coord) -> Set[Coord]:
    return set((tile[0] + d.coord[0], tile[1] + d.coord[1]) for d in D)


def day(turned: Set[Coord]) -> Set[Coord]:
    new_turned: Set[Coord] = set()
    white_processed: Set[Coord] = set()
    for black_tile in turned:
        neighbours = get_neighbours(black_tile)
        black_neighbours = set(n for n in neighbours if n in turned)
        if len(black_neighbours) in (1, 2):
            new_turned.add(black_tile)

        white_neighbours = neighbours - black_neighbours - white_processed
        white_processed.update(white_neighbours)

        for white_tile in white_neighbours:
            w_neighbours = get_neighbours(white_tile)
            w_black_neighbours = set(n for n in w_neighbours if n in turned)
            if len(w_black_neighbours) == 2:
                new_turned.add(white_tile)
    return new_turned


for i in range(0, 101):
    if i <= 10 or i % 10 == 0:
        print(f"Day {i}: {len(turned)}")
    turned = day(turned)
