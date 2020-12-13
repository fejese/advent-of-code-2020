#!/usr/bin/env python3

from typing import List

# INPUT = "test-input"
INPUT: str = "input"

with open(INPUT, "r") as f:
    ts: int = int(f.readline().strip())
    buses: List[int] = [
        int(bus) for bus in f.readline().strip().split(",") if bus != "x"
    ]

print(ts, buses)


def fun(ts: int, buses: List[int]) -> int:
    next: int = ts
    while True:
        for bus in buses:
            if next % bus == 0:
                print(next, bus)
                return bus * (next - ts)
        next += 1


print(f"solution: {fun(ts, buses)}")
