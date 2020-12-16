#!/usr/bin/env python3

import re
from typing import Dict, List, Tuple, cast

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

RULE_PATTERN = re.compile(r"^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$")


Range = Tuple[int, int]
Ranges = Tuple[Range, Range]
Rule = Tuple[str, Ranges]
Rules = List[Rule]
Ticket = List[int]
Tickets = List[Ticket]


def get_rule(line: str) -> Rule:
    parts = RULE_PATTERN.match(line)
    return (
        parts[1],
        (
            (int(parts[2]), int(parts[3])),
            (int(parts[4]), int(parts[5])),
        ),
    )


def is_in_range(x: int, r: Range) -> bool:
    return x in range(r[0], r[1] + 1)


def is_in_ranges(x: int, ranges: Ranges) -> bool:
    return is_in_range(x, ranges[0]) or is_in_range(x, ranges[1])


def ticket_error_rate(ticket: Ticket, rules: Rules) -> int:
    error_rate: int = 0
    for num in ticket:
        error_rate += (
            num if not any(is_in_ranges(num, rule[1]) for rule in rules) else 0
        )
    # print(f"Ticket: {ticket}, error_rate: {error_rate}")
    return error_rate


rules: Rules
nearby_tickets: Tickets
scanning_error_rate: int = 0

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]
    rules = [get_rule(line) for line in lines[: lines.index("")]]
    nearby_tickets = [
        [int(x) for x in line.split(",")]
        for line in lines[lines.index("nearby tickets:") + 1 :]
        if line
    ]

# print(f"Rules: {rules}")
# print(f"Nearby tickets: {nearby_tickets}")

scanning_error_rate = sum(
    [ticket_error_rate(ticket, rules) for ticket in nearby_tickets]
)

print(f"Scanning error rate: {scanning_error_rate}")
