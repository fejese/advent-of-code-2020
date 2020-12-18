#!/usr/bin/env python3

import re
from typing import List

PAR_PAT = re.compile(r".*(\([^)]+\)).*")


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]


def solve(line: str) -> int:
    while "(" in line:
        match = PAR_PAT.match(line)
        sub_solve = solve(match.group(1).strip("(").strip(")"))
        line = line.replace(match.group(1), str(sub_solve))

    parts = line.split(" ")
    sol = int(parts[0])
    parts = parts[1:]
    while parts:
        op = parts[0]
        val = int(parts[1])
        if op == "+":
            sol += val
        elif op == "-":
            sol -= val
        elif op == "*":
            sol *= val
        else:
            print(f"WTF: {sol} {op} {val}")
        parts = parts[2:]
    return sol


solutions: List[int] = [solve(line) for line in lines]
print("Solutions:", solutions)
print("Solution:", sum(solutions))
