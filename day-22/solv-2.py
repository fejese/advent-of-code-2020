#!/usr/bin/env python3

from typing import List, Tuple, Set

Deck = List[int]
Decks = List[Deck]

# INPUT_FILE_NAME: str = "test-input"
# INPUT_FILE_NAME: str = "test-input-2"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    decks: Decks = [
        [int(line.strip()) for line in deck_data.split("\n")[1:] if line.strip()]
        for deck_data in input_file.read().split("\n\n")
    ]


class GameIdCounter:
    next: int = 1

    @classmethod
    def use(cls) -> int:
        current = cls.next
        cls.next += 1
        return current


def get_decks_hash(decks: Decks) -> str:
    return "__".join(["_".join([str(c) for c in deck]) for deck in decks])


def get_winner(decks: Decks) -> Tuple[int, Decks]:
    game_id: int = GameIdCounter.use()
    previous_decks: Set[str] = set()
    print(f"=== Game {game_id} ===")
    print()
    round: int = 1
    while all(d for d in decks):
        print(f"-- Round {round} (Game {game_id}) --")
        print("Player 1's deck:", decks[0])
        print("Player 2's deck:", decks[1])
        decks_hash: str = get_decks_hash(decks)
        if decks_hash in previous_decks:
            print(f"The winner of game {game_id} is player 1 due to repetition.")
            print()
            return (0, decks)
        previous_decks.add(decks_hash)
        next_cards: Tuple[int, int] = tuple(d[0] for d in decks)
        print("Player 1 plays:", next_cards[0])
        print("Player 2 plays:", next_cards[1])
        decks = [d[1:] for d in decks]
        winner: int
        if all(len(deck) >= next_cards[i] for i, deck in enumerate(decks)):
            print("Playing a sub-game to determine the winner...")
            print()
            winner, _ = get_winner(
                [deck[: next_cards[i]] for i, deck in enumerate(decks)]
            )
            print(f"...anyway, back to game {game_id}.")
            next_cards = tuple([next_cards[winner], next_cards[1 - winner]])
        else:
            winner = next_cards.index(max(next_cards))
            print(f"Player {winner + 1} wins round {round} of game {game_id}!")
            print()
            next_cards = tuple(sorted(next_cards, reverse=True))
        decks[winner] += list(next_cards)
        round += 1
    print(f"The winner of game {game_id} is player {winner+1}!")
    print()
    return winner, decks


winner, decks = get_winner(decks)
winner_deck: Deck = decks[winner]

score: int = sum((i + 1) * c for i, c in enumerate(reversed(winner_deck)))
print("winner score:", score)
