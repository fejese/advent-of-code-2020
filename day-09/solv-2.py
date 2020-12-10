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

        for i in range(self.pos - PREAMBLE_LENGTH, self.pos):
            for j in range(i, self.pos):
                if i == j:
                    continue
                if self.number_list[i] + self.number_list[j] == x:
                    return True
        return False

    def add(self, x: int) -> None:
        self.number_list.append(x)
        self.pos += 1

    def find_set(self, x: int) -> List[int]:
        sum: int = 0
        nums: List[int] = []
        start: int = 0
        end: int = 0
        while True:
            if sum < x:
                sum += self.number_list[end]
                nums.append(self.number_list[end])
                end += 1
            elif sum > x:
                sum -= self.number_list[start]
                nums.remove(self.number_list[start])
                start += 1
            else:
                return nums



proc = Processor()

with open(input, "r") as f:
    for line in f:
        num = int(line.strip())
        if not proc.is_valid_next(num):
            print(f"#{proc.pos} ({num})")
            nums = proc.find_set(num)
            print(min(nums), max(nums), min(nums) + max(nums))
            break
        proc.add(num)
