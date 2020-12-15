#!/usr/bin/env python3

from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    numbers = [int(x) for x in input_file.readline().strip().split(",")]

last_mentions = {num: idx + 1 for idx, num in enumerate(numbers)}
print(f"last mentions: {last_mentions}")
previous_mentions = {}
round = len(numbers) + 1
last_number = numbers[round - 2]

while round <= 30000000:
    if last_number in previous_mentions:
        next_number = last_mentions[last_number] - previous_mentions[last_number]
    else:
        next_number = 0

    if next_number in last_mentions:
        previous_mentions[next_number] = last_mentions[next_number]
    last_mentions[next_number] = round
    round += 1
    last_number = next_number

print(f"30000000th number: {last_number}")
