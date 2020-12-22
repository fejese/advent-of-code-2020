#!/usr/bin/env python3

from typing import List, Tuple, Set

Deck = List[int]
Decks = List[Deck]

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    decks: Decks = [
        [int(line.strip()) for line in deck_data.split("\n")[1:] if line.strip()]
        for deck_data in input_file.read().split("\n\n")
    ]

print(decks)

winner: int
while all(d for d in decks):
    next_cards: Deck = [d[0] for d in decks]
    decks = [d[1:] for d in decks]
    winner = next_cards.index(max(next_cards))
    decks[winner] += sorted(next_cards, reverse=True)

winner_deck: Deck = decks[winner]

print("End of game!")
print(decks)
print("Winner:", winner)
print("Winner deck:", winner_deck)

score = sum((i + 1) * c for i, c in enumerate(reversed(winner_deck)))
print("winner score:", score)
