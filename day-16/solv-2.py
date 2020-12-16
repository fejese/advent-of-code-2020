#!/usr/bin/env python3

import re
from typing import Dict, List, Tuple, Optional, Set

INPUT_FILE_NAME: str = "test-input-2"
FIELD_TO_FIND: str = "class"
INPUT_FILE_NAME: str = "input"
FIELD_TO_FIND: str = "departure"

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


def is_valid_ticket(ticket: Ticket, rules: Rules) -> bool:
    for num in ticket:
        if not any(is_in_ranges(num, rule[1]) for rule in rules):
            return False
    return True


rules: Rules
nearby_tickets: Tickets
valid_tickets: Tickets
my_ticket: Ticket

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]
    rules = [get_rule(line) for line in lines[: lines.index("")]]
    nearby_tickets = [
        [int(x) for x in line.split(",")]
        for line in lines[lines.index("nearby tickets:") + 1 :]
        if line
    ]
    my_ticket = [int(x) for x in lines[lines.index("your ticket:") + 1].split(",")]

valid_tickets = [ticket for ticket in nearby_tickets if is_valid_ticket(ticket, rules)]

# for r in rules:
#     print(r[0])
#     for t in valid_tickets:
#         if not is_in_ranges(t[3], r[1]):
#             print(f"Not valid: {t[3]} from {t}")
#             break

# raise


potential_fields: List[Set[str]] = []
potential_poss: Dict[str, Set[int]] = {rule[0]: set() for rule in rules}
fields: List[Optional[str]] = [None] * len(rules)

for pos in range(len(my_ticket)):
    potential_fields.append(set())
    for rule in rules:
        if all(is_in_ranges(ticket[pos], rule[1]) for ticket in valid_tickets):
            potential_fields[pos].add(rule[0])
            potential_poss[rule[0]].add(pos)


while not all(field for field in fields):
    print(f"Fields left to find: {len([f for f in fields if not f])}")
    print(f"Potential field names: {potential_fields}")
    print(f"Potential field positions: {potential_poss}")
    print(f"Final fields: {fields}")
    for pos, _fields in enumerate(potential_fields):
        if len(_fields) == 1:
            field = _fields.pop()
            fields[pos] = field
            print(
                f"Found position for field {field}: {pos} (only field possible at this pos)"
            )
            potential_fields[pos] = set()
            potential_poss[field] = set()
            for p in range(len(potential_fields)):
                potential_fields[p] -= set([field])
            for f in potential_poss.keys():
                potential_poss[f] -= set([pos])
    for field, poss in potential_poss.items():
        if len(poss) == 1:
            pos = poss.pop()
            fields[pos] = field
            print(
                f"Found position for field {field}: {pos} (field is only possible at this pos)"
            )
            potential_fields[pos] = set()
            potential_poss[field] = set()
            for p in range(len(potential_fields)):
                potential_fields[p] -= set([field])
            for f in potential_poss.keys():
                potential_poss[f] -= set([pos])

print(f"Fields: {fields}")

departure_data = {
    fields[i]: num for i, num in enumerate(my_ticket) if FIELD_TO_FIND in fields[i]
}
print(departure_data)

result = 1
for val in departure_data.values():
    result *= val

print(f"Result: {result}")
