"""poker game."""
import random
from poker.hand_logic import is_royal_flush, is_straight, check_flush, find_three_of_a_kind, find_four_of_a_kind, has_full_house, high_card
import poker.tie_break as tb
from collections import Counter


def generate_deck() -> list[tuple[str, str]]:
    """Generate a full deck of playing cards.

    Returns:
        list[tuple[str, str]]: A list of tuples where each tuple represents a card
        with a suit and a value.
    """
    colors = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [(color, value) for color in colors for value in values]


def deal_cards(deck: list[tuple[str, str]], n: int = 5, amount_of_users: int = 2) -> list[tuple[str, str]]:
    """Draw cards for each player from the deck without repetition.

    Args:
        deck (list[tuple[str, str]]): The deck to draw cards from.
        n (int, optional): Number of cards per player. Defaults to 5.
        amount_of_users (int, optional): Number of players. Defaults to 2.

    Returns:
        dict: Dictionary where keys are player names and values are lists of cards.
    """
    random.shuffle(deck)

    users_cards = {}
    for i in range(amount_of_users):
        player_cards = deck[:n]
        del deck[:n]
        users_cards[f"player{i}"] = player_cards

    return users_cards


def extract_colors_and_values(cards: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    """Separate suits and values from a list of cards.

    Args:
        cards (list[tuple[str, str]]): list of cards as (suit, value) tuples.

    Returns:
        tuple[list[str], list[str]]: Two lists, first with suits and second with values.
    """
    colors = [color for color, _ in cards]
    values = [value for _, value in cards]
    return colors, values


def count_card_amount(n: int, card_values: dict) -> int:
    """Return the card value that appears exactly n times.

    Args:
        n (int): Number of occurrences to look for (e.g. 2 for pair).
        card_values (dict): Dictionary mapping card values to counts.

    Returns:
        int: Card value that appears n times.
    """
    return [k for k, v in card_values.items() if card_values[k] == n][0]


def evaluate_hand(user_cards):
    """Evaluate the poker hand for a given set of cards.

    Determines the rank of the hand according to poker rules.

    Args:
        user_cards (list[tuple[str, str]]): Player's cards.

    Returns:
        tuple | int: Hand ranking representation used later for comparison.
    """
    colors, values = extract_colors_and_values(user_cards)

    card_values = Counter(values)
    value = list(card_values.values())
    keys = list(card_values.keys())

    print("\n--- ANALYSIS ---")

    if is_royal_flush(colors, values):
        return 10

    elif is_straight(values) and check_flush(colors):
        return (9, high_card(keys))

    elif find_four_of_a_kind(values):
        card_value = count_card_amount(4, card_values)
        max_card = high_card(keys[1:])
        return (8, card_value, max_card)

    elif has_full_house(values):
        three = count_card_amount(3, card_values)
        pair = count_card_amount(2, card_values)
        return (7, three, pair)

    elif check_flush(colors):
        return (6, high_card(keys))

    elif is_straight(values):
        return (5, high_card(keys))

    elif find_three_of_a_kind(values):
        card_value = count_card_amount(3, card_values)
        max_card = high_card(keys[1:])
        return (4, card_value, max_card)

    elif len(value) == 3:
        return (3, keys[0], keys[1], keys[2])

    elif len(value) == 4:
        card_value = count_card_amount(2, card_values)
        max_card = high_card(keys[1:])
        return (2, card_value, max_card)

    elif high_card(values):
        return (1, high_card(values))


def change_cards(cards: list[tuple[str, str]],
                 deck: list[tuple[str, str]],
                 indices: list[int] | None = None) -> None:
    """Replace selected cards in a player's hand with cards from the deck.

    Args:
        cards (list[tuple[str, str]]): Player's current cards.
        deck (list[tuple[str, str]]): Remaining deck.
        indices (list[int] | None): Positions of cards to replace.

    Raises:
        IndexError: If provided card index is invalid.
    """
    if not indices:
        return

    for idx in indices:
        if idx < 0 or idx >= len(cards):
            raise IndexError(f"Invalid card index: {idx}")

        new_card = deck.pop(0)
        cards[idx] = new_card


def evaluate_result(game_result):
    """Determine which player has the best hand.

    Args:
        game_result (list[dict]): List containing player names,
        hands and evaluation results.

    Returns:
        None
    """
    best_rank = max(player['result'][0] for player in game_result)
    finalists = [p for p in game_result if p['result'][0] == best_rank]

    print(best_rank)
    print(finalists)


def main() -> None:
    """Run the poker game.

    Generates the deck, deals cards, allows card replacement,
    evaluates each player's hand and prints the result.
    """
    deck = generate_deck()
    users_cards = deal_cards(deck, amount_of_users=3)

    print(users_cards)
    game_result = []

    for player, cards in users_cards.items():
        print(f"{player} before change: {cards}")
        indices_to_change = input(
            "pass in card indexes form 0-4 to replace card or press enter to ommit: "
        ).strip()

        indices = list(map(int, indices_to_change.split())) if indices_to_change else None
        change_cards(cards, deck, indices)
        print(f"{player} after change: {cards}")

        result = evaluate_hand(cards)
        player_dict = {'player_name': player, 'hand': cards, 'result': result}
        game_result.append(player_dict)
        print(f"{player} has {cards} with {result}")

    print(game_result)

    evaluate_result(game_result)

#TODO
# OGARNĄĆ TESTY W RUFF
# DOKOŃCZYĆ LOGIKĘ EVALUATE_HAND DLA WIELU GRACZY MOŻE BYĆ Z CHATEM
if __name__ == "__main__":
    main()
