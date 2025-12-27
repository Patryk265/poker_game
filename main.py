"""poker game."""
import random
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



    # karty dla graczy
    users_cards = {}
    for i in range(amount_of_users):
        player_cards = deck[:5]
        del deck[:5]
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


def is_royal_flush(colors: list[str], values: list[str]) -> bool:
    """Check if the hand is a Royal Flush.

    Args:
        colors (list[str]): list of suits of the hand.
        values (list[str]): list of values of the hand.

    Returns:
        bool: True if the hand is a Royal Flush, False otherwise.
    """
    royal_flush = {"10", "J", "Q", "K", "A"}
    return len(set(colors)) == 1 and set(values) == royal_flush



def is_straight(values: list[str]) -> bool:
    """Check if the hand is a straight (five consecutive values).

    Args:
        values (list[str]): list of card values.

    Returns:
        bool: True if the hand forms a straight, False otherwise.
    """
    mapping = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    numeric_values = [int(mapping.get(v, v)) for v in values]
    numeric_values.sort()

    if len(set(numeric_values)) != 5:
        return False

    return all(numeric_values[i] + 1 == numeric_values[i + 1] for i in range(4))


def check_flush(colors: list[str]) -> bool:
    """Check if all cards are of the same suit.

    Args:
        colors (list[str]): list of suits of the hand.

    Returns:
        bool: True if all cards have the same suit, False otherwise.
    """
    return len(set(colors)) == 1


def count_card_values(values: list[str]) -> Counter:
    """Count occurrences of each card value in the hand.

    Args:
        values (list[str]): list of card values.

    Returns:
        Counter: A Counter object mapping card values to their counts.
    """
    return Counter(values)


def find_pairs(values: list[str]) -> list[str]:
    """Find all card values that appear exactly twice (pairs).

    Args:
        counts (Counter): Counter of card values.

    Returns:
        list[str]: list of card values forming pairs.
    """
    counts_values = count_card_values(values)
    return [card for card, count in counts_values.items() if count == 2]


def find_three_of_a_kind(values: list[str]) -> str | None:
    """Find the card value that appears three times (three of a kind).

    Args:
        counts (Counter): Counter of card values.

    Returns:
        str | None: The card value that forms three of a kind, or None if not found.
    """
    counts_values = count_card_values(values)
    return any(card for card, count in counts_values.items() if count == 3)


def find_four_of_a_kind(values: list[str]) -> str | None:
    """Find the card value that appears four times (four of a kind).

    Args:
        counts (Counter): Counter of card values.

    Returns:
        str | None: The card value that forms four of a kind, or None if not found.
    """
    counts_values = count_card_values(values)
    return any(card for card, count in counts_values.items() if count == 4)


def has_full_house(values: list[str]) -> bool:
    """Check if the hand is a full house (three of a kind + one pair).

    Args:
        counts (Counter): Counter of card values.

    Returns:
        bool: True if the hand is a full house, False otherwise.
    """
    counts_values = count_card_values(values)
    has_three = any(count == 3 for count in counts_values.values())
    has_pair = any(count == 2 for count in counts_values.values())
    return has_three and has_pair

def high_card(values: list[str]) -> str:
    order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    highest = max(values, key=lambda c:order.index(c))
    return highest


def analyze_combinations(values: list[str]) -> list[str]:
    """Analyze card combinations like pairs, three of a kind, four of a kind, etc.

    Args:
        values (list[str]): list of card values.

    Returns:
        list[str]: Descriptions of combinations found in the hand.
    """
    counts = count_card_values(values)
    results = []

    four_card = find_four_of_a_kind(counts)
    if four_card:
        results.append(f"Quad of a kind '{four_card}'")

    three_card = find_three_of_a_kind(counts)
    if three_card:
        results.append(f"Three of a kind '{three_card}'")

    pairs = find_pairs(counts)
    for pair in pairs:
        results.append(f"One pair of '{pair}'")

    if has_full_house(counts):
        results.append(
            f"Full House: three of '{three_card}' and pair of '{', '.join(pairs)}'")
    elif len(pairs) == 2:
        results.append(f"Two pairs: '{pairs[0]}' and '{pairs[1]}'")

    return results


def evaluate_hand(user_cards):
    """Evaluate the hand for each user's cards.
    Args:
    """
    colors, values = extract_colors_and_values(user_cards)


    print("\n--- ANALYSIS ---")
    if is_royal_flush(colors, values):
        print("Royal Flush!")
        return 10
    elif is_straight(values) and check_flush(colors):
        print("Straight Flush!")
        return 9

    elif find_four_of_a_kind(values):
        return 8

    elif has_full_house(values):
        return 7

    elif check_flush(colors):
        print("Flush!")
        return 6

    elif is_straight(values):
        print("Straight!")
        return 5

    elif find_three_of_a_kind(values):
        return 4

    pairs = find_pairs(values)
    # two pairs
    if len(pairs) == 2:
        return 3
    # one pair

    elif len(pairs) == 1:
        return 2

    elif high_card(values):
        return 1





def main() -> None:
    """Main function to generate a deck, deal cards, and analyze the hand."""
    deck = generate_deck()
    users_cards = deal_cards(deck)

    # print(f"{users_cards}")

    game_result = []
    for player, cards in users_cards.items():
        # print(cards)
        # cards = [('Spades', '3'), ('Hearts', '5'), ('Clubs', '4'), ('Hearts', '2'), ('Spades', '7')]
        result = evaluate_hand(cards)
        player_dict = {'player_name':player, 'hand':cards, 'result': result}
        game_result.append(player_dict)

        # print(f"{player} has {cards} with {result}")
    print(game_result)


if __name__ == "__main__":
    main()





