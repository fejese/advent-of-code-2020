#!/usr/bin/env python3

import re
from typing import Dict, List, Set, Tuple

input = "input"
PARENT = "shiny gold"
INF = -1

nested_pat = re.compile(
    r"^(\S+ \S+) bags contain" + 10 * r"(?: (\d+) (\S+ \S+) bags?[.,])?"
)

# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# dotted black bags contain no other bags.

children_map: Dict[str, List[Tuple[str, int]]] = {}


def get_children_count(
    children_map: Dict[str, List[Tuple[str, int]]],
    parent: str,
    colors: Set[str] = set(),
) -> int:
    direct_children = children_map.get(parent, [])
    children_colors = set([p[0] for p in direct_children])
    if colors.intersection(children_colors.union(set(parent))):
        return INF
    children_count = sum([p[1] for p in direct_children])
    colors.update(direct_children)
    for direct_child in direct_children:
        child_tree_count = get_children_count(children_map, direct_child[0], colors)
        if child_tree_count == INF:
            return INF
        children_count += direct_child[1] * child_tree_count
    return children_count


with open(input, "r") as f:
    for line in f:
        if "no other bags" in line:
            pass
        else:
            matches = nested_pat.match(line)
            print(line, matches.groups())
            parent = matches.groups()[0]
            if parent not in children_map:
                children_map[parent]: List[Tuple[str, int]] = []
            child_matches = matches.groups()[1:]
            for i in range(int(len(child_matches) / 2)):
                cnt_idx = 2 * i
                col_idx = 2 * i + 1
                if not child_matches[cnt_idx]:
                    continue
                children_map[parent].append(
                    (child_matches[col_idx], int(child_matches[cnt_idx]))
                )

import pprint

pprint.pprint(children_map)

children_count = get_children_count(children_map, PARENT)
print(children_count)
