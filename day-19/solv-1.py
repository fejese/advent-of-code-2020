#!/usr/bin/env python3

import re
from typing import Dict, List, Union

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

unresolved: Dict[int, List[Union[str, int]]] = {}
resolved: Dict[int, str] = {}
messages: List[str] = []
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        if ":" in line:
            id, rest = line.split(":")
            if '"' in rest:
                resolved[int(id)] = rest.strip().strip('"')
            else:
                sub_parts = [
                    [int(x) for x in sub.strip().split(" ")]
                    for sub in rest.strip().split("|")
                ]
                unresolved[int(id)] = sub_parts
            continue
        if not line.strip():
            continue
        messages.append(line.strip())

# print(resolved)
# print(unresolved)

while 0 not in resolved:
    for ui in unresolved:
        # print(f"Inspecting unresolved: {ui} -> {unresolved[ui]}")
        found_some: bool = False
        for si in range(len(unresolved[ui])):
            for pi in range(len(unresolved[ui][si])):
                if unresolved[ui][si][pi] in resolved:
                    unresolved[ui][si][pi] = resolved[unresolved[ui][si][pi]]
                    found_some = True
        if found_some:
            found_all: bool = all(
                all(isinstance(part, str) for part in sub) for sub in unresolved[ui]
            )
            if found_all:
                resolved[ui] = (
                    "(" + ("|".join(["".join(sub) for sub in unresolved[ui]])) + ")"
                )
                unresolved.pop(ui)
                break

# print(messages)
print("pattern:", resolved[0])
patt = re.compile("^" + resolved[0] + "$")
matched = [m for m in messages if patt.match(m)]
# print(matched)
print(len(matched))
