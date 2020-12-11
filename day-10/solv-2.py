#!/usr/bin/env python3

from typing import Dict, List, Set, Tuple

input = "input"

with open(input, "r") as f:
    jolts: List[int] = [int(line.strip()) for line in f]

jolts.append(0)
jolts.append(max(jolts) + 3)
jolts = sorted(jolts)

last_cache: Dict[int, int] = {max(jolts): 1}

for ji in range(len(jolts) - 2, -1, -1):
    jolt = jolts[ji]
    last_cache[jolt] = 0
    for i in range(3, 0, -1):
        if jolt + i in last_cache:
            last_cache[jolt] += last_cache[jolt + i]

print(last_cache[0])
