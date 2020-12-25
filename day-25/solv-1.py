#!/usr/bin/env python3

INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

INITIAL_SUBJECT_NUM: int = 7
DIVIDER: int = 20201227

def transform(subject_number: int, loop_size: int, start_value: int = 1) -> int:
    value = start_value
    for _ in range(loop_size):
        value *= subject_number
        value = value % DIVIDER
    return value

def get_loop_size(pub_key: int) -> int:
    loop_size = 0
    pub_key_i = 1
    while pub_key_i != pub_key:
        pub_key_i = transform(INITIAL_SUBJECT_NUM, 1, pub_key_i)
        loop_size += 1
    return loop_size

pub_key_a: int
pub_key_b: int
with open(INPUT_FILE_NAME, "r") as input_file:
    pub_key_a, pub_key_b = [int(line.strip()) for line in input_file]

print("Pub key A:", pub_key_a)
print("Pub key B:", pub_key_b)

loop_size_a: int = get_loop_size(pub_key_a)
loop_size_b: int = get_loop_size(pub_key_b)
print("Loop size A:", loop_size_a)
print("Loop size B:", loop_size_b)

encryption_key_a: int = transform(pub_key_b, loop_size_a)
encryption_key_b: int = transform(pub_key_a, loop_size_b)
print("Encrypion key A:", encryption_key_a)
print("Encrypion key B:", encryption_key_b)
