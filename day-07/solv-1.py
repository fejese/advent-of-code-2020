#!/usr/bin/env python3

import re
from typing import Dict, Set

input = "input"
CHILD = "shiny gold"

nested_pat = re.compile(r"^(\S+ \S+) bags contain(?: \d+ (\S+ \S+) bags?[.,])?(?: \d+ (\S+ \S+) bags?[.,])?(?: \d+ (\S+ \S+) bags?[.,])?(?: \d+ (\S+ \S+) bags?[.,])?(?: \d+ (\S+ \S+) bags?[.,])?(?: \d+ (\S+ \S+) bags?[.,])?")

# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# dotted black bags contain no other bags.

parents: Dict[str, Set[str]] = {}

def get_possible_parents(parents: Dict[str, Set[str]], child: str, possible_parents: Set[str] = set()) -> possible_parents: Set[str]:
    new_possible_parents = parents.get(child, set()) - possible_parents
    for new_possible_parent in new_possible_parents:
        possible_parents.add(new_possible_parent)
        get_possible_parents(parents, new_possible_parent, possible_parents)
    return possible_parents

with open(input, "r") as f:
    for line in f:
        if "no other bags" in line:
            pass
        else:
            matches = nested_pat.match(line)
            print(line, matches.groups())
            for child in matches.groups()[1:]:
                if not child:
                    continue
                if child not in parents:
                    parents[child]: Set[str] = set()
                parents[child].add(matches.groups()[0])

import pprint
pprint.pprint(parents)

possible_parents = get_possible_parents(parents, CHILD)
pprint.pprint(possible_parents)
print(len(possible_parents))
