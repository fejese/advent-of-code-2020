#!/usr/bin/env python3

import re
from typing import Dict, List, Tuple

INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"


isntructions: Dict[int, int]
memory: Dict[int, int] = {}
pat = re.compile("mem\[(\d+)\] = (\d+)")
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        if line.startswith("mask"):
            mask = line.strip().split(" ")[2]
            print(f"mask: {mask}")
        else:
            matches = pat.match(line)
            if not matches:
                print(line)
                continue
            address = int(matches.group(1))
            value = int(matches.group(2))
            print(f"address: {address:4} {address:8b}")
            print(f"value:   {value:4} {value:8b}")

            addresses = [0]
            for mi in range(0, len(mask)):
                ch = mask[len(mask) - mi - 1]
                if ch == "X":
                    new_addresses = [(1 << mi) | a for a in addresses]
                    addresses += new_addresses
                if ch == "0":
                    for ai in range(len(addresses)):
                        addresses[ai] |= address & (1 << mi)
                if ch == "1":
                    for ai in range(len(addresses)):
                        addresses[ai] |= 1 << mi
            for address in sorted(addresses):
                print(f"address[x]: {address:4} {address:8b}")
                memory[address] = value

# print(memory)
print(sum(memory.values()))
