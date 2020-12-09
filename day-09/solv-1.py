#!/usr/bin/env python3

from typing import Dict, List, Tuple

input = "input"
PREAMBLE_LENGTH = 25


class Processor:
    def __init__(self) -> None:
        self.pos: int = 0
        self.number_list: List[int] = []

    def is_valid_next(self, x: int) -> bool:
        if self.pos < PREAMBLE_LENGTH:
            return True

        for i in range(len(self.number_list)):
            for j in range(len(self.number_list)):
                if i == j:
                    continue
                if self.number_list[i] + self.number_list[j] == x:
                    return True
        return False

    def add(self, x: int) -> None:
        if self.pos < PREAMBLE_LENGTH:
            self.number_list.append(x)
        else:
            self.number_list[self.pos % PREAMBLE_LENGTH] = x
        self.pos += 1


proc = Processor()

with open(input, "r") as f:
    for line in f:
        num = int(line.strip())
        if not proc.is_valid_next(num):
            print(f"#{proc.pos} ({num})")
            break
        proc.add(num)
