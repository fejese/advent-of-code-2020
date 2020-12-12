#!/usr/bin/env python3

from typing import Tuple

# INPUT = "test-input"
INPUT = "input"

pos: Tuple[int, int] = (0, 0)
wp: Tuple[int, int] = (10, 1)
with open(INPUT, "r") as f:
    for line in f:
        cmd: str = line[0]
        val: int = int(line[1:].strip())
        if cmd == "L":
            for i in range(int(val / 90)):
                wp = (-wp[1], wp[0])
        elif cmd == "R":
            for i in range(int(val / 90)):
                wp = (wp[1], -wp[0])
        elif cmd == "F":
            pos = (pos[0] + val * wp[0], pos[1] + val * wp[1])
        elif cmd == "E":
            wp = (wp[0] + val, wp[1])
        elif cmd == "N":
            wp = (wp[0], wp[1] + val)
        elif cmd == "W":
            wp = (wp[0] - val, wp[1])
        elif cmd == "S":
            wp = (wp[0], wp[1] - val)

print(pos, wp)
print(abs(pos[0]) + abs(pos[1]))
