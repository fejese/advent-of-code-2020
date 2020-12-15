#!/usr/bin/env python3

import re
from typing import Dict, List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


isntructions: Dict[int, int]
memory: Dict[int, int] = {}
pat = re.compile("mem\[(\d+)\] = (\d+)")
mask = -1
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        if line.startswith("mask"):
            mask = line.strip().split(" ")[2]
            or_mask = 0
            and_mask = 1
            print("mask: {mask}")
            for ch in mask:
                or_mask <<= 1
                and_mask <<= 1
                if ch == "1":
                    or_mask += 1
                if ch == "X" or ch == "1":
                    and_mask += 1
            print(mask, or_mask, and_mask)
        else:
            matches = pat.match(line)
            if not matches:
                print(line)
                continue
            address = int(matches.group(1))
            value = int(matches.group(2))
            print(address, value)
            value &= and_mask
            value |= or_mask
            print(value)
            memory[address] = value

print(memory)
print(sum(memory.values()))
