#!/usr/bin/env python3

from typing import Set

input = "input"

cache: Set[int] = set()

with open(input, "r") as f:
    for line in f:
        i = int(line)
        pair = 2020 - i
        if pair in cache:
            print(i, pair, i * pair)
            break
        cache.add(i)
