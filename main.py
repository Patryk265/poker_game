"""poker game."""
import random
from poker.hand_logic import is_royal_flush, is_straight, check_flush, count_card_values, find_three_of_a_kind, find_four_of_a_kind, has_full_house, high_card
import poker.tie_break as tb



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



def evaluate_hand(user_cards):
    """Evaluate the hand for each user's cards.
    Args:
    """
    colors, values = extract_colors_and_values(user_cards)

    card_values = count_card_values(values)
    value = list(card_values.values())
    keys = list(card_values.keys())

    print("\n--- ANALYSIS ---")
    if is_royal_flush(colors, values):
        print("Royal Flush!")
        return 10
    elif is_straight(values) and check_flush(colors):
        print("Straight Flush!")
        max_card = high_card(keys)
        return (9, max_card)

    elif find_four_of_a_kind(values):
        card_value = [k for k, v in card_values.items() if card_values[k] == 4][0]
        max_card = high_card(keys[1:])
        return (8, card_value, max_card)

    elif has_full_house(values):
        three = [k for k, v in card_values.items() if card_values[k] == 3][0]
        pair = [k for k, v in card_values.items() if card_values[k] == 2][0]
        return (7, three, pair)

    elif check_flush(colors):
        print("Flush!")
        max_card = high_card(keys)
        return (6, max_card)

    elif is_straight(values):
        print("Straight!")
        max_card = high_card(keys)
        return (5, max_card)


    elif find_three_of_a_kind(values):
        card_value = [k for k, v in card_values.items() if card_values[k] == 3][0]
        max_card = high_card(keys[1:])
        return (4, card_value, max_card)



    # two pairs
    elif len(value) == 3:

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


# def one_pair_tie_break
#
# def tie_break(player0, player1):
#     match case
#



def main() -> None:
    """Main function to generate a deck, deal cards, and analyze the hand."""
    deck = generate_deck()
    users_cards = deal_cards(deck)
    # users_cards = {'player0': [('Clubs', '8'), ('Hearts', '8'), ('Clubs', '8'), ('Spades', '8'), ('Hearts', 'A')],
    #                'player1': [('Diamonds', '9'), ('Clubs', '9'), ('Spades', '9'), ('Spades', '9'), ('Hearts', 'A')]}

    print(f"{users_cards}")
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
        # cards = [('Spades', '5'), ('Spades', '5'), ('Spades', '5'), ('Spades', '4'), ('Spades', '4')]
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
                tb.high_card_tie_break(game_result[0]['result'][1], game_result[1]['result'][1])

            case 2:
                tb.pair_tie_break(game_result[0]['result'], game_result[1]['result'])

            case 3:
                tb.two_paris_tie_break(game_result[0]['result'], game_result[1]['result'])

            case 4:
                tb.three_of_kind_tie_break(game_result[0]['result'], game_result[1]['result'])
            case 5:
                # reused function
                tb.high_card_tie_break(game_result[0]['result'], game_result[1]['result'])
            case 6:
                tb.high_card_tie_break(game_result[0]['result'], game_result[1]['result'])
            case 7:
                tb.three_of_kind_tie_break(game_result[0]['result'], game_result[1]['result'])
            case 8:
                tb.three_of_kind_tie_break(game_result[0]['result'], game_result[1]['result'])
            case 9:
                tb.high_card_tie_break(game_result[0]['result'], game_result[1]['result'])



# TODO
# napisać testy do tie_break

#wysłać gotowy kod na git huba z gotowymi testami i dodać dominika jako rewiuera

    # else:
    #     print

if __name__ == "__main__":
    main()
