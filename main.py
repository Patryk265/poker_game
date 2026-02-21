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
    """Draw a number of random cards from the deck without repetition.

    Args:
        deck (list[tuple[str, str]]): The deck to draw cards from.
        n (int, optional): Number of cards to draw. Defaults to 5.

    Returns:
        list[tuple[str, str]]: A list of drawn card tuples.
    """
    random.shuffle(deck)

    users_cards = {}
    for i in range(amount_of_users):
        player_cards = deck[:n]
        del deck[:n]
        users_cards[f"player{i}"] = player_cards

    return users_cards



def extract_colors_and_values(cards: list[tuple[str, str]]) ->\
        tuple[list[str], list[str]]:
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
    return [k for k, v in card_values.items() if card_values[k] == n][0]


def evaluate_hand(user_cards):
    """Evaluate the hand for each user's cards.
    Args:
    """
    colors, values = extract_colors_and_values(user_cards)

    card_values = Counter(values)
    value = list(card_values.values())
    keys = list(card_values.keys())

    print("\n--- ANALYSIS ---")
    # Checks whether the hand is a Royal Flush (10, J, Q, K, A all in the same suit)
    if is_royal_flush(colors, values):
        return 10

    # Checks whether the hand is a Straight Flush (five consecutive values in the same suit)
    elif is_straight(values) and check_flush(colors):
        return (9, high_card(keys))

    # Checks whether the hand contains Four of a Kind (four cards of the same value)
    elif find_four_of_a_kind(values):
        card_value = count_card_amount(4, card_values)
        max_card = high_card(keys[1:])
        return (8, card_value, max_card)

    # Checks whether the hand is a Full House (three of a kind plus a pair)
    elif has_full_house(values):
        three = count_card_amount(3, card_values)
        pair = count_card_amount(2, card_values)
        return (7, three, pair)

    # Checks whether the hand is a Flush (all cards of the same suit, not in sequence)
    elif check_flush(colors):
        return (6, high_card(keys))

    # Checks whether the hand is a Straight (five consecutive values, suits ignored)
    elif is_straight(values):
        return (5, high_card(keys))

    # Checks whether the hand contains Three of a Kind (three cards of the same value)
    elif find_three_of_a_kind(values):
        card_value = count_card_amount(3, card_values)
        max_card = high_card(keys[1:])
        return (4, card_value, max_card)

    # Checks whether the hand contains Two Pairs (two different pairs plus one kicker)
    elif len(value) == 3:
        return (3, keys[0], keys[1], keys[2])

    # Checks whether the hand contains One Pair (one pair plus three kickers)
    elif len(value) == 4:
        card_value = count_card_amount(2, card_values)
        max_card = high_card(keys[1:])
        return (2, card_value, max_card)

    # Checks for High Card when no other poker hand is present
    elif high_card(values):
        return (1, high_card(values))


def change_cards(cards: list[tuple[str, str]],
                 deck: list[tuple[str, str]],
                 indices: list[int] | None = None) -> None:
    if not indices:
        return

    for idx in indices:
        if idx < 0 or idx >= len(cards):
            raise IndexError(f"Invalid card index: {idx}")

        new_card = deck.pop(0)
        cards[idx] = new_card

def evaluate_result(game_result):
    player0_result = game_result[0]['result']
    player1_result = game_result[1]['result']

    if player0_result[0] > player1_result[0]:
        print("player with index 0 won")
    elif player0_result[0] < player1_result[0]:
        print("player with index 1 won")

    elif player0_result[0] == player1_result[0]:
        match player0_result[0]:
            case 1 | 5 | 6 | 9:
                tb.high_card_tie_break(player0_result[1], player1_result[1])
            case 2:
                tb.pair_tie_break(player0_result, player1_result)
            case 3:
                tb.two_paris_tie_break(player0_result, player1_result)
            case 4 | 7 | 8:
                tb.gorouped_cards_tie_break(player0_result, player1_result)

def main() -> None:
    """Main function to generate a deck, deal cards, and analyze the hand."""
    deck = generate_deck()
    users_cards = deal_cards(deck)

    print(users_cards)
    game_result = []

    for player, cards in users_cards.items():
        print(f"{player} before change: {cards}")
        indices_to_change = input("pass in card indexes form 0-4 to replace card or press enter to ommit: "
        ).strip()
        indices = list(map(int, indices_to_change.split())) if indices_to_change else None
        change_cards(cards, deck, indices)
        print(f"{player} after change: {cards}")

        result = evaluate_hand(cards)
        player_dict = {'player_name':player, 'hand':cards, 'result': result}
        game_result.append(player_dict)
        print(f"{player} has {cards} with {result}")

    print(game_result)

    evaluate_result(game_result)


if __name__ == "__main__":
    main()
