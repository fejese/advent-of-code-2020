#!/usr/bin/env python3

from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    numbers = [int(x) for x in input_file.readline().strip().split(",")]

while len(numbers) < 2020:
    last_number = numbers[len(numbers) - 1]
    if numbers.count(last_number) == 1:
        next_number = 0
    else:
        list_copy = numbers.copy()
        list_copy.reverse()
        next_number = list_copy[1:].index(last_number) + 1
    numbers.append(next_number)

print(f"2020th number: {numbers[len(numbers) - 1]}")
