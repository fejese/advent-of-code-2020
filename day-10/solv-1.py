#!/usr/bin/env python3

input = "input"

with open(input, "r") as f:
    jolts = [int(line.strip()) for line in f]

jolts = sorted(jolts)
jolts.append(max(jolts) + 3)

last_jolt = 0
jolt_diffs = {}
for jolt in jolts:
    diff = jolt - last_jolt
    diffs = jolt_diffs.get(diff, 0)
    jolt_diffs[diff] = diffs + 1
    last_jolt = jolt

print(jolt_diffs)
print(jolt_diffs[3] * jolt_diffs[1])
