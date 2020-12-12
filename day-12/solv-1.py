#!/usr/bin/env python3

from typing import Dict, Tuple

# INPUT = "test-input"
INPUT = "input"

left_rot: Dict[str, str] = {
    "E": "N",
    "N": "W",
    "W": "S",
    "S": "E",
}
right_rot: Dict[str, str] = {
    "E": "S",
    "S": "W",
    "W": "N",
    "N": "E",
}
forw: Dict[str, Tuple[int, int]] = {
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
}

pos: Tuple[int, int] = (0, 0)
direction: str = "E"
with open(INPUT, "r") as f:
    for line in f:
        cmd: str = line[0]
        val: int = int(line[1:].strip())
        if cmd == "L":
            for i in range(int(val / 90)):
                direction = left_rot[direction]
        elif cmd == "R":
            for i in range(int(val / 90)):
                direction = right_rot[direction]
        elif cmd == "F":
            pos = (pos[0] + forw[direction][0] * val, pos[1] + forw[direction][1] * val)
        elif cmd == "E":
            pos = (pos[0] + val, pos[1])
        elif cmd == "N":
            pos = (pos[0], pos[1] + val)
        elif cmd == "W":
            pos = (pos[0] - val, pos[1])
        elif cmd == "S":
            pos = (pos[0], pos[1] - val)

print(pos, direction)
print(abs(pos[0]) + abs(pos[1]))
