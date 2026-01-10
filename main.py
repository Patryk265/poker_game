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

    card_values = count_card_values(values)
    value = list(card_values.values())
    keys = list(card_values.keys())



    # two pairs
    if len(value) == 3:

        return (3, keys[0], keys[1], keys[2])
    # one pair

    elif len(value) == 4:
        card_value = [k for k,v in card_values.items() if card_values[k] == 2][0]
        max_card = high_card(keys[1:])
        return (2, card_value, max_card)

    elif high_card(values):
        return (1,  high_card(values))


def change_cards(cards: list[tuple[str, str]],
                 deck: list[tuple[str, str]],
                 indices: list[int] | None = None) -> None:
    """
    Replace selected cards (by index) with new ones from the deck.
    Modifies cards in-place.
    """
    if not indices:
        return

    for idx in indices:
        if idx < 0 or idx >= len(cards):
            raise IndexError(f"Invalid card index: {idx}")

        # get new card
        new_card = deck.pop(0)

        # replace card
        cards[idx] = new_card

def high_card_tie_break(player0, player1):
    high_card_value = high_card([player0['result'][1], player1['result'][1]])

    if player0['result'][1] == player1['result'][1]:
        print("draw")
    elif high_card_value == player1['result'][1]:
        print("player1 won")
    else:
        print("player0 won")


# def one_pair_tie_break
#
# def tie_break(player0, player1):
#     match case
#




def main() -> None:
    """Main function to generate a deck, deal cards, and analyze the hand."""
    deck = generate_deck()
    users_cards = deal_cards(deck)

    # print(f"{users_cards}")
    print(users_cards)
    game_result = []


    for player, cards in users_cards.items():
        #print(f"{player} before change: {cards}")

        # exchange card on index 1 and 3
        # indices_to_change = [1, 3]

        # indices_to_change = input("pass in card indexes form 0-4 to replace card or press enter to ommit: "
        # ).strip()

        # indices = list(map(int, indices_to_change.split())) if indices_to_change else None

        # change_cards(cards, deck, indices)

        # print(f"{player} after change: {cards}")

        # print(cards)
        cards = [('Spades', '3'), ('Hearts', '5'), ('Clubs', '2'), ('Hearts', '9'), ('Spades', '7')]
        result = evaluate_hand(cards)
        print(result)
        player_dict = {'player_name':player, 'hand':cards, 'result': result}
        game_result.append(player_dict)


        print(f"{player} has {cards} with {result}")
    print(game_result)
    # for idx, player_result in enumerate(game_result):
    if game_result[0]['result'][0] > game_result[1]['result'][0]:
        print("player with index 0 won")
    elif game_result[0]['result'][0] < game_result[1]['result'][0]:
        print("player with index 1 won")
    elif game_result[0]['result'][0] == game_result[1]['result'][0]:
        match game_result[0]['result'][0]:
            case 1:
                high_card_tie_break(game_result[0], game_result[1])




    # else:
    #     print

if __name__ == "__main__":
    main()
