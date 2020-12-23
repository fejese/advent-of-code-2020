#!/usr/bin/env python3

from typing import List

# INPUT_FILE_NAME: str = "test-input"
# STEP_COUNT: int = 10
INPUT_FILE_NAME: str = "input"
STEP_COUNT: int = 100


cups: List[int]
with open(INPUT_FILE_NAME, "r") as input_file:
    cups = [int(c) for c in input_file.read().strip()]
curr: int = cups[0]
cup_count: int = len(cups)


def print_cups(cups: List[int], curr: int) -> None:
    print(f"cups: {' '.join([f'({c})' if c == curr else str(c) for c in cups])}")


for step in range(1, STEP_COUNT + 1):
    print(f"--- move {step} ---")
    print_cups(cups, curr)

    # pick up
    curr_idx: int = cups.index(curr)
    picked_up: List[int] = cups[curr_idx + 1 : curr_idx + 4]
    cups = cups[: curr_idx + 1] + cups[curr_idx + 4 :]
    wrap_around: int = 3 - len(picked_up)
    picked_up += cups[:wrap_around]
    print("pick up:", ", ".join([str(x) for x in picked_up]))
    cups = cups[wrap_around:]
    # print("cups:", cups)

    # select dest
    sorted_cups = sorted(cups, reverse=True)
    dest_cup: int = sorted_cups[(sorted_cups.index(curr) + 1) % (cup_count - 3)]
    print("destination:", dest_cup)

    # place
    dest_idx: int = cups.index(dest_cup)
    cups = cups[: dest_idx + 1] + picked_up + cups[dest_idx + 1 :]

    # new curr
    curr = cups[(cups.index(curr) + 1) % cup_count]

print(f"--- final ---")
print_cups(cups, curr)

sol_start_idx = (cups.index(1) + 1) % cup_count
sol = "".join([str(x) for x in cups[sol_start_idx:] + cups[: sol_start_idx - 1]])

print("solution:", sol)
