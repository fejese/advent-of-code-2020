#!/usr/bin/env python3

input = "input"

total_count = 0
yes = set()
with open(input, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            yes.update([c for c in line])
        if not line:
            group_count = len(yes)
            print(group_count)
            total_count += group_count
            group_count = 0
            yes = set()

group_count = len(yes)
print(group_count)
total_count += group_count

print(total_count)
