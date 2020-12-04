#!/usr/bin/env python3

import re

input = "input"

expected_keys = {
    "byr": re.compile(r"^(19[2-9][0-9]|200[0-2])$"),
    "iyr": re.compile(r"^20(1[0-9]|20)$"),
    "eyr": re.compile(r"^20(2[0-9]|30)$"),
    "hgt": re.compile(r"^(1([5-8][0-9]|9[0-3])cm|(59|6[0-9]|7[0-6])in)$"),
    "hcl": re.compile(r"^#[0-9a-f]{6}$"),
    "ecl": re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$"),
    "pid": re.compile(r"^[0-9]{9}$"),
    # "cid",
}

valid_passports: int = 0

with open(input, "r") as f:
    keys_found = set()
    for line in f:
        line = line.strip()
        if line:
            pairs = line.split(" ")
            for k, v in [pair.split(":") for pair in pairs]:
                if k not in expected_keys:
                    continue
                pat = expected_keys[k]
                if not pat.search(v):
                    continue
                keys_found.add(k)
        if set(expected_keys.keys()).issubset(keys_found):
            valid_passports += 1
            keys_found = set()
        if not line:
            keys_found = set()

print(valid_passports)
