#!/usr/bin/env python3

from typing import Dict, List, Set, Tuple

input = "input"


class Instr:
    def __init__(self, cmd: str, val: str) -> None:
        self.cmd = cmd
        self.val = int(val)


class Prog(list):
    DEBUG_REPLACEMENTS: Dict[str, str] = {
        "jmp": "nop",
        "nop": "jmp",
    }

    def run(self, debug_pos: int) -> Tuple[bool, int]:
        pos: int = 0
        acc: int = 0
        visited: Set[int] = set()
        while True:
            if pos in visited:
                print(f"Instruction #{pos} to be repeated, breaking")
                return (False, acc)
            if pos >= len(self):
                print(f"Instruction #{pos} is out of bounds, assuming success")
                return (True, acc)
            visited.add(pos)
            instr = self[pos]
            if pos == debug_pos:
                orig_instr = instr
                instr = Instr(
                    Prog.DEBUG_REPLACEMENTS.get(orig_instr.cmd, orig_instr.cmd),
                    orig_instr.val,
                )
                print(
                    f"Running instruction #{pos}: DEBUG [{orig_instr.cmd} -> {instr.cmd}] {instr.val}"
                )
            else:
                print(f"Running instruction #{pos}: {instr.cmd} {instr.val}")
            if instr.cmd == "acc":
                acc += instr.val
                pos += 1
            elif instr.cmd == "jmp":
                pos += instr.val
            elif instr.cmd == "nop":
                pos += 1


prog: Prog = Prog()

with open(input, "r") as f:
    for line in f:
        cmd, val = line.strip().split(" ")
        val = int(val)
        prog.append(Instr(cmd, val))

for i in range(len(prog)):
    res = prog.run(i)
    if res[0]:
        print(f"Acc: {res[1]}")
        break
