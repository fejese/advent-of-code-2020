#!/usr/bin/env python3

from typing import Dict, List, Optional

# INPUT_FILE_NAME: str = "test-input"
# STEP_COUNT: int = 100
# CUP_COUNT: int = 9
INPUT_FILE_NAME: str = "input"
STEP_COUNT: int = 10000000
CUP_COUNT: int = 1000000


class Cup:
    def __init__(self, label: int) -> None:
        self.label = label
        self.left: Optional["Cup"] = None
        self.right: Optional["Cup"] = None
        self.picked_up: bool = False

    def insert_right(self, to_insert: "Cup") -> None:
        to_insert.left = self
        to_insert.right = self.right
        self.right.left = to_insert
        self.right = to_insert

    def remove_right(self) -> "Cup":
        to_remove = self.right
        to_remove.right.left = self
        self.right = to_remove.right
        return to_remove

    def __str__(self) -> str:
        return str(self.label)


class Ring:
    def __init__(self, labels: List[int]) -> None:
        self.cups: Dict[int, Cup] = {label: Cup(label) for label in labels}
        self.curr: Cup = self.cups[labels[0]]

        for i, label in enumerate(labels):
            self.cups[label].left = self.cups[labels[(i - 1) % CUP_COUNT]]
            self.cups[label].right = self.cups[labels[(i + 1) % CUP_COUNT]]

        self.picked_up: List[Cup] = []

    def play_round(self) -> None:
        # pick up
        for _ in range(3):
            removed = self.curr.remove_right()
            removed.picked_up = True
            self.picked_up.append(removed)
        # print("pick up:",  ", ".join([str(x) for x in self.picked_up]))

        # select dest
        self.curr.picked_up = True
        dest_label = self.curr.label
        while self.cups[dest_label].picked_up:
            dest_label -= 1
            if dest_label not in self.cups:
                dest_label = max(self.cups)
        self.curr.picked_up = False
        dest_cup = self.cups[dest_label]
        # print("destination:", dest_cup)

        # place
        for removed in reversed(self.picked_up):
            dest_cup.insert_right(removed)
            removed.picked_up = False
        self.picked_up.clear()

        # new curr
        self.curr = self.curr.right

    def to_list(self, start: Optional[Cup] = None) -> None:
        start = start or self.curr
        l: List[Cup] = [start]
        i = start.right
        while i != start:
            l.append(i)
            i = i.right
        return l

    def print_cups(self) -> None:
        lst = self.to_list()
        if CUP_COUNT > 35:
            print(
                "cups:",
                " ".join([f"({c})" if c == self.curr else str(c) for c in lst[:15]]),
                "...",
                " ".join([f"({c})" if c == self.curr else str(c) for c in lst[-15:]]),
            )
        else:
            print(
                f"cups: {' '.join([f'({c})' if c == self.curr else str(c) for c in lst])}"
            )

    def play_game(self) -> None:
        for step in range(1, STEP_COUNT + 1):
            if step % 100000 == 0:
                print(f"--- move {step} ---")
            # self.print_cups()
            self.play_round()

        print(f"--- final ---")
        self.print_cups()

        # part 1
        # sol_lst = self.to_list(start=self.cups[1])[1:]
        # sol = "".join([str(x) for x in sol_lst])
        # print("solution 1:", sol)

        # part 2
        sol_pair = (self.cups[1].right.label, self.cups[1].right.right.label)
        print("solution 2:", sol_pair, "->", sol_pair[0] * sol_pair[1])


labels: List[int]
with open(INPUT_FILE_NAME, "r") as input_file:
    labels = [int(c) for c in input_file.read().strip()]
labels.extend([l for l in range(max(labels) + 1, CUP_COUNT + 1)])

ring = Ring(labels)
ring.play_game()
