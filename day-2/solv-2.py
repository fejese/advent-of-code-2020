#!/usr/bin/env python3

input = "input"

matches = 0
with open(input, "r") as f:
    for line in f:
        rest, pwd = line.split(":", 1)
        pwd = pwd.strip()
        rng, char = rest.split(" ", 1)
        char_matches = [pwd[int(x) - 1] == char for x in rng.split("-")]
        match = any(char_matches) and not all(char_matches)
        if match:
            matches += 1
print(matches)
