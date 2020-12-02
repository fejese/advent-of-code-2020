#!/usr/bin/env python3

input = "input"

matches = 0
with open(input, "r") as f:
    for line in f:
        rest, pwd = line.split(":", 1)
        pwd = pwd.strip()
        rng, char = rest.split(" ", 1)
        range_min, range_max = (int(x) for x in rng.split("-"))
        count = pwd.count(char)
        if count <= range_max and count >= range_min:
            matches += 1
print(matches)
