import random
from collections import Counter


def generate_deck():
    """Creates a full deck of cards (suit + value)."""
    colors = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [(color, value) for color in colors for value in values]


def deal_cards(deck, n=5):
    """Draws n random cards from the deck without repetition."""
    return random.sample(deck, n)


def extract_colors_and_values(cards):
    """Returns two separate lists: one for suits and one for values."""
    colors = [color for color, _ in cards]
    values = [value for _, value in cards]
    return colors, values


def is_royal_flush(colors: list, values: list):
    """Checks if the hand is a Royal Flush."""
    royal_flush = {"10", "J", "Q", "K", "A"}
    return len(set(colors)) == 1 and set(values) == royal_flush


def is_straight(values):
    """Checks if the cards form a straight (five consecutive values)."""
    mapping = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    numeric_values = [int(mapping.get(v, v)) for v in values]
    numeric_values.sort()

    # Straight requires 5 unique and consecutive values
    if len(set(numeric_values)) != 5:
        return False

    return all(numeric_values[i] + 1 == numeric_values[i + 1] for i in range(4))


def check_flush(colors):
    """Checks if all cards are of the same suit."""
    return len(set(colors)) == 1


def count_card_values(values):
    """Returns a Counter object for card values."""
    return Counter(values)


def find_pairs(counts):
    """Returns a list of cards that form pairs (exactly 2 of the same value)."""
    return [card for card, count in counts.items() if count == 2]


def find_three_of_a_kind(counts):
    """Returns the value of the card that appears 3 times (Three of a Kind)."""
    return next((card for card, count in counts.items() if count == 3), None)


def find_four_of_a_kind(counts):
    """Returns the value of the card that appears 4 times (Four of a Kind)."""
    return next((card for card, count in counts.items() if count == 4), None)


def has_full_house(counts):
    """Checks if the hand is a Full House (Three of a Kind + One Pair)."""
    has_three = any(count == 3 for count in counts.values())
    has_pair = any(count == 2 for count in counts.values())
    return has_three and has_pair


def analyze_combinations(values):
    """Analyzes card combinations like pairs, three of a kind, four of a kind, etc."""
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

    # Check for Full House
    if has_full_house(counts):
        results.append(f"Full House: three of '{three_card}' and pair of '{', '.join(pairs)}'")
    # Check for Two Pairs
    elif len(pairs) == 2:
        results.append(f"Two pairs: '{pairs[0]}' and '{pairs[1]}'")

    return results


def main():
    deck = generate_deck()
    table = deal_cards(deck)

    print("Cards on table:")
    for color, value in table:
        print(f"  {value} of {color}")

    colors, values = extract_colors_and_values(table)

    print("\n--- ANALYSIS ---")
    if is_royal_flush(colors, values):
        print("Royal Flush!")
    elif is_straight(values) and check_flush(colors):
        print("Straight Flush!")
    elif check_flush(colors):
        print("Flush!")
    elif is_straight(values):
        print("Straight!")

    # Check for pair/triple/full house/kareta combinations
    for result in analyze_combinations(values):
        print(result)


if __name__ == "__main__":
    main()
