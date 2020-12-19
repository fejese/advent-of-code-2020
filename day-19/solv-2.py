#!/usr/bin/env python3

import re
from typing import Dict, List, Union

# INPUT_FILE_NAME: str = "test-input-2"
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


# 0: 8 11
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

unresolved[0] = [["(", 42, "){{{}}}", "(", 31, "){{{}}}"]]

# print(resolved)
# print(unresolved)

while 0 not in resolved:
    resolved_any: bool = False
    # print("Looking ...")
    for ui in unresolved:
        # print(f"Inspecting unresolved: {ui} -> {unresolved[ui]}")
        found_some: bool = False
        for si in range(len(unresolved[ui])):
            for pi in range(len(unresolved[ui][si])):
                if unresolved[ui][si][pi] in resolved:
                    unresolved[ui][si][pi] = resolved[unresolved[ui][si][pi]]
                    found_some = True
                    resolved_any = True
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
    if not resolved_any:
        print("Can't resolve any more")
        break

# print(messages)
print("pattern:", resolved[0])

matched: List[str] = []
unmatched: List[str] = [m for m in messages]

for i in range(2, 50):
    for j in range(1, i):
        patt = re.compile("^" + resolved[0].format(i, j) + "$")
        new_matched: List[str] = [m for m in unmatched if patt.match(m)]
        matched += new_matched
        unmatched = [m for m in unmatched if m not in new_matched]
        if new_matched:
            print(f"Found {len(new_matched)} for i={i},j={j}")
# print(matched)

print(len(matched))
