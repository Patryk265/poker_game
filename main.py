"""Poker game."""

import random
from collections import Counter

from poker.hand_logic import (
    is_royal_flush,
    is_straight,
    check_flush,
    find_three_of_a_kind,
    find_four_of_a_kind,
    has_full_house,
    high_card,
)


def generate_deck() -> list[tuple[str, str]]:
    """Generate a full deck of playing cards.

    Returns:
        list[tuple[str, str]]: A list of tuples where each tuple represents a card
        with a suit and a value.
    """
    colors = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    return [(color, value) for color in colors for value in values]


def deal_cards(
    deck: list[tuple[str, str]],
    n: int = 5,
    amount_of_users: int = 2,
) -> dict[str, list[tuple[str, str]]]:
    """Draw cards for each player from the deck without repetition.

    Args:
        deck: The deck to draw cards from.
        n: Number of cards per player.
        amount_of_users: Number of players.

    Returns:
        dict[str, list[tuple[str, str]]]: Mapping of player name to cards.
    """
    random.shuffle(deck)

    users_cards: dict[str, list[tuple[str, str]]] = {}

    for i in range(amount_of_users):
        player_cards = deck[:n]
        del deck[:n]
        users_cards[f"player{i}"] = player_cards

    return users_cards


def extract_colors_and_values(
    cards: list[tuple[str, str]],
) -> tuple[list[str], list[str]]:
    """Separate suits and values from cards.

    Args:
        cards: Cards represented as (suit, value).

    Returns:
        tuple[list[str], list[str]]: Suits and values.
    """
    colors = [color for color, _ in cards]
    values = [value for _, value in cards]

    return colors, values


def count_card_amount(n: int, card_values: dict[str, int]) -> str:
    """Return the card value that appears exactly n times.

    Args:
        n: Number of occurrences to search for.
        card_values: Mapping of card value to occurrences.

    Returns:
        str: Card value that appears n times.
    """
    return [k for k, v in card_values.items() if v == n][0]


def evaluate_hand(user_cards: list[tuple[str, str]]) -> tuple | int:
    """Evaluate the poker hand.

    Args:
        user_cards: Cards belonging to a player.

    Returns:
        tuple | int: Hand ranking used for comparison.
    """
    colors, values = extract_colors_and_values(user_cards)

    card_values = Counter(values)
    counts = list(card_values.values())
    keys = list(card_values.keys())

    print("\n--- ANALYSIS ---")

    if is_royal_flush(colors, values):
        return 10

    if is_straight(values) and check_flush(colors):
        return (9, high_card(values))

    if find_four_of_a_kind(values):
        card_value = count_card_amount(4, card_values)
        max_card = high_card(values)
        return (8, card_value, max_card)

    if has_full_house(values):
        three = count_card_amount(3, card_values)
        pair = count_card_amount(2, card_values)
        return (7, three, pair)

    if check_flush(colors):
        return (6, high_card(values))

    if is_straight(values):
        return (5, high_card(values))

    if find_three_of_a_kind(values):
        card_value = count_card_amount(3, card_values)
        max_card = high_card(values)
        return (4, card_value, max_card)

    if len(counts) == 3:
        return (3, keys[0], keys[1], keys[2])

    if len(counts) == 4:
        card_value = count_card_amount(2, card_values)
        max_card = high_card(values)
        return (2, card_value, max_card)

    return (1, high_card(values))


def change_cards(
    cards: list[tuple[str, str]],
    deck: list[tuple[str, str]],
    indices: list[int] | None = None,
) -> None:
    """Replace selected cards in player's hand.

    Args:
        cards: Player cards.
        deck: Remaining deck.
        indices: Positions of cards to replace.

    Raises:
        IndexError: If invalid card index is provided.
    """
    if not indices:
        return

    for idx in indices:
        if idx < 0 or idx >= len(cards):
            raise IndexError(f"Invalid card index: {idx}")

        new_card = deck.pop(0)
        cards[idx] = new_card


def evaluate_result(game_result: list[dict]) -> None:
    """Determine winner(s) of the game using lexicographic comparison."""
    best_hand = max(player["result"] for player in game_result)

    winners = [
        player for player in game_result
        if player["result"] == best_hand
    ]

    print("Winner(s):")

    for winner in winners:
        print(
            f"{winner['player_name']} "
            f"with {winner['hand']} -> {winner['result']}"
        )


def main() -> None:
    """Run the poker game."""
    amount_of_users = int(input("How many players will play? "))

    deck = generate_deck()
    users_cards = deal_cards(deck, amount_of_users=amount_of_users)

    print(users_cards)

    game_result: list[dict] = []

    for player, cards in users_cards.items():
        print(f"{player} before change: {cards}")

        indices_to_change = input(
            "Pass card indexes 0-4 to replace or press enter to skip: "
        ).strip()

        indices = (
            list(map(int, indices_to_change.split()))
            if indices_to_change
            else None
        )

        change_cards(cards, deck, indices)

        print(f"{player} after change: {cards}")

        result = evaluate_hand(cards)

        player_dict = {
            "player_name": player,
            "hand": cards,
            "result": result,
        }

        game_result.append(player_dict)

        print(f"{player} has {cards} with {result}")

    print(game_result)

    evaluate_result(game_result)


if __name__ == "__main__":
    main()
