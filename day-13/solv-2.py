#!/usr/bin/env python3

from typing import List

# INPUT = "test-input"
INPUT: str = "input"

with open(INPUT, "r") as f:
    f.readline()
    buses: List[int] = [
        0 if bus == "x" else int(bus) for bus in f.readline().strip().split(",")
    ]

print(f"buses: {buses}")
print(f"count: {len(buses)}")


def fun(buses: List[int]) -> int:
    next: int = 0
    max_bus: int = max(buses)
    max_bus_idx: int = buses.index(max_bus)
    next -= max_bus_idx
    increment = max_bus
    in_increment = set([max_bus])
    while True:
        ok = True
        for i, bus in enumerate(buses):
            if bus == 0:
                continue
            if (next + i) % bus != 0:
                ok = False
                break
            if bus not in in_increment:
                multiple_included = False
                for inc in in_increment:
                    if inc % bus == 0:
                        multiple_included = True
                        break
                if not multiple_included:
                    increment *= bus
                in_increment.add(bus)
        if ok:
            return next
        next += increment


print(f"solution: {fun(buses)}")
