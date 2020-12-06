#!/usr/bin/env python3

input = "input"

total_count = 0
yes = set()
new_group = True
with open(input, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            new_yes = set([c for c in line])
            yes = new_yes if new_group else yes.intersection(new_yes)
            new_group = False
        if not line:
            group_count = len(yes)
            print(group_count)
            total_count += group_count
            group_count = 0
            yes = set()
            new_group = True

group_count = len(yes)
print(group_count)
total_count += group_count

print(total_count)
