from collections import Counter


CARD_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUE_MAP = {v: i for i, v in enumerate(CARD_ORDER, start=2)}


def to_numbers(values: list[str]) -> list[int]:
    """Convert card values to numeric representations and sort them.

    Args:
        values (list[str]): List of card values (e.g. ["A", "K", "10"]).

    Returns:
        list[int]: Sorted list of numeric card values.
    """
    return sorted(VALUE_MAP[v] for v in values)


def is_royal_flush(colors: list[str], values: list[str]) -> bool:
    """Check if the hand is a Royal Flush.

    A Royal Flush consists of 10, J, Q, K, A all in the same suit.

    Args:
        colors (list[str]): List of suits of the hand.
        values (list[str]): List of card values of the hand.

    Returns:
        bool: True if the hand is a Royal Flush, False otherwise.
    """
    royal_flush = {"10", "J", "Q", "K", "A"}
    return len(set(colors)) == 1 and set(values) == royal_flush


def is_straight(values: list[str]) -> bool:
    """Check if the hand is a straight (five consecutive values).

    Args:
        values (list[str]): List of card values.

    Returns:
        bool: True if the hand forms a straight, False otherwise.
    """
    sorted_values = to_numbers(values)
    return all(sorted_values[i] + 1 == sorted_values[i + 1] for i in range(4))


def check_flush(colors: list[str]) -> bool:
    """Check if all cards are of the same suit.

    Args:
        colors (list[str]): List of suits of the hand.

    Returns:
        bool: True if all cards have the same suit, False otherwise.
    """
    return len(set(colors)) == 1


def _find_number_of_kind(values: list[str], quantity: int) -> bool:
    """Check if the hand contains a specific number of identical card values.

    Args:
        values (list[str]): List of card values.
        quantity (int): Number of identical cards to look for.

    Returns:
        bool: True if such a group exists, False otherwise.
    """
    counts = Counter(values)
    return any(count == quantity for count in counts.values())


def find_three_of_a_kind(values: list[str]) -> bool:
    """Check if the hand contains three cards of the same value.

    Args:
        values (list[str]): List of card values.

    Returns:
        bool: True if three of a kind is present, False otherwise.
    """
    return _find_number_of_kind(values, 3)


def find_four_of_a_kind(values: list[str]) -> bool:
    """Check if the hand contains four cards of the same value.

    Args:
        values (list[str]): List of card values.

    Returns:
        bool: True if four of a kind is present, False otherwise.
    """
    return _find_number_of_kind(values, 4)


def has_full_house(values: list[str]) -> bool:
    """Check if the hand is a full house.

    A full house consists of three cards of one value and two cards of another value.

    Args:
        values (list[str]): List of card values.

    Returns:
        bool: True if the hand is a full house, False otherwise.
    """
    has_three = _find_number_of_kind(values, 3)
    has_pair = _find_number_of_kind(values, 2)
    return has_three and has_pair


def high_card(values: list[str]) -> str:
    """Return the highest card value from the hand.

    Args:
        values (list[str]): List of card values.

    Returns:
        str: The highest card value according to VALUE_MAP.
    """
    return max(values, key=lambda v: VALUE_MAP[v])


