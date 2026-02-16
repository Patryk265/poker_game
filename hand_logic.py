from collections import Counter


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


# def find_pairs(values: list[str]) -> list[str]:
#     """Find all card values that appear exactly twice (pairs).

#     Args:
#         counts (Counter): Counter of card values.

#     Returns:
#         list[str]: list of card values forming pairs.
#     """
#     counts_values = count_card_values(values)
#     return [card for card, count in counts_values.items() if count == 2]


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
