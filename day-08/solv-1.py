#!/usr/bin/env python3

from typing import List, Set

input = "input"


class Instr:
    def __init__(self, cmd: str, val: str) -> None:
        self.cmd = cmd
        self.val = int(val)


class Prog(list):
    def run(self) -> int:
        pos: int = 0
        acc: int = 0
        visited: Set[int] = set()
        while True:
            if pos in visited:
                print(f"Instruction #{pos} to be repeated, breaking")
                break
            visited.add(pos)
            instr = self[pos]
            print(f"Running instruction #{pos}: {instr.cmd} {instr.val}")
            if instr.cmd == "acc":
                acc += instr.val
                pos += 1
            elif instr.cmd == "jmp":
                pos += instr.val
            elif instr.cmd == "nop":
                pos += 1

        return acc


prog: Prog = Prog()

with open(input, "r") as f:
    for line in f:
        cmd, val = line.strip().split(" ")
        val = int(val)
        prog.append(Instr(cmd, val))

print(f"Acc: {prog.run()}")
