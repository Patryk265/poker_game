def count_card_amount(n: int, card_values: dict) -> int:
    """Return the card value that appears exactly n times in the hand.

    Args:
        n (int): Number of occurrences to search for (e.g., 2 for pair, 3 for three of a kind).
        card_values (dict): Dictionary mapping card values to their counts.

    Returns:
        int: The card value that appears exactly n times.
    """
    return [k for k, v in card_values.items() if card_values[k] == n][0]


def evaluate_hand(user_cards):
    """Evaluate the strength of a poker hand.

    Determines the poker hand ranking for the provided cards and returns
    a tuple describing the result. The first element represents the rank
    of the hand (higher is better). Additional elements are used for
    tie-breaking when comparing hands of the same rank.

    Args:
        user_cards (list[tuple[str, str]]): A list of cards represented as
        (suit, value) tuples.

    Returns:
        tuple | int: A ranking representation of the hand. The first value
        indicates the hand category:
            10 - Royal Flush
             9 - Straight Flush
             8 - Four of a Kind
             7 - Full House
             6 - Flush
             5 - Straight
             4 - Three of a Kind
             3 - Two Pairs
             2 - One Pair
             1 - High Card
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
    """Replace selected cards in a player's hand with new ones from the deck.

    Args:
        cards (list[tuple[str, str]]): The player's current hand.
        deck (list[tuple[str, str]]): Remaining deck to draw new cards from.
        indices (list[int] | None): List of card positions to replace. If None,
        no cards will be changed.

    Raises:
        IndexError: If a provided index is outside the valid card range.
    """
    if not indices:
        return

    for idx in indices:
        if idx < 0 or idx >= len(cards):
            raise IndexError(f"Invalid card index: {idx}")

        new_card = deck.pop(0)
        cards[idx] = new_card


def evaluate_result(game_result):
    """Determine the winning player(s) based on evaluated hands.

    Finds the highest hand rank among all players and selects the players
    who achieved that rank. Tie-breaking logic can be applied afterwards
    if multiple players share the same rank.

    Args:
        game_result (list[dict]): List containing player results. Each element
        should include:
            - 'player_name': name or identifier of the player
            - 'hand': list of cards
            - 'result': evaluated hand ranking

    Returns:
        None
    """
    best_rank = max(player['result'][0] for player in game_result)
    finalists = [p for p in game_result if p['result'][0] == best_rank]

    print(best_rank)
    print(finalists)


def main() -> None:
    """Run the poker game simulation.

    The function:
        1. Generates a deck of cards.
        2. Deals cards to players.
        3. Allows players to optionally exchange cards.
        4. Evaluates each hand.
        5. Determines the winner.

    Returns:
        None
    """
    deck = generate_deck()
    users_cards = deal_cards(deck,  amount_of_users=3)

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
