#!/usr/bin/env python3

import re
from typing import List

SPLIT_PAT = re.compile(r"([ ()])")

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]


def rindex(l: List[str], e: str) -> int:
    for i in range(len(l) - 1, -1, -1):
        if l[i] == e:
            return i
    raise ValueError(f"'{e}' is not in list")


def split(line: str) -> List[str]:
    return [s for s in SPLIT_PAT.split(line) if s not in ["", " "]]


def solve(parts: List[str]) -> int:
    while "(" in parts:
        rp_pos = parts.index(")")
        lp_pos = rindex(parts[:rp_pos], "(")
        sub_parts = parts[lp_pos + 1 : rp_pos]
        sub_sol = solve(sub_parts)
        parts = parts[:lp_pos] + [str(sub_sol)] + parts[rp_pos + 1 :]
    while "+" in parts:
        p_pos = parts.index("+")
        lop = int(parts[p_pos - 1])
        rop = int(parts[p_pos + 1])
        parts = parts[: p_pos - 1] + [str(lop + rop)] + parts[p_pos + 2 :]

    sol = int(parts[0])
    parts = parts[1:]
    while parts:
        op = parts[0]
        val = int(parts[1])
        if op != "*":
            print(f"OOPS: {sol} {op} {val}")
        sol *= val
        parts = parts[2:]
    return sol


solutions: List[int] = [solve(split(line)) for line in lines]
print("Solutions:", solutions)
print("Solution:", sum(solutions))
