#!/usr/bin/env python3

from typing import Dict, Set

input = "input"


with open(input, "r") as f:
    nums = [int(line) for line in f]

try:
    for ai in range(len(nums) - 2):
        a = nums[ai]
        for bi in range(ai + 1, len(nums) - 1):
            b = nums[bi]
            c = 2020 - a - b
            if c in nums[bi + 1 :]:
                print(a, b, c, a * b * c)
                raise Exception()
    print("not found")
except:
    pass
