#!/usr/bin/env python3

input = "input"

expected_keys = set(
    [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        # "cid",
    ]
)

valid_passports: int = 0

with open(input, "r") as f:
    keys_found = set()
    for line in f:
        line = line.strip()
        if line:
            pairs = line.split(" ")
            keys_found.update(set(pair.split(":")[0] for pair in pairs))
        if expected_keys.issubset(keys_found):
            valid_passports += 1
            keys_found = set()
        if not line:
            keys_found = set()

print(valid_passports)
