from poker.hand_logic import high_card


def high_card_tie_break(player0_high_card, player1_high_card):
    """Resolve a tie by comparing the highest cards of two players.

    Args:
        player0_high_card (str): Highest card value for player 0.
        player1_high_card (str): Highest card value for player 1.

    Returns:
        None: Prints the result of the comparison.
    """
    high_card_value = high_card([player0_high_card, player1_high_card])

    if player0_high_card == player1_high_card:
        print("draw")
    elif high_card_value == player1_high_card:
        print("player1 won")
    else:
        print("player0 won")


def pair_tie_break(player0_result, player1_result):
    """Resolve a tie between two hands containing one pair.

    First compares the value of the pairs. If the pairs are equal,
    the highest kicker card is compared.

    Args:
        player0_result (tuple): Result tuple returned from hand evaluation
        for player 0.
        player1_result (tuple): Result tuple returned from hand evaluation
        for player 1.

    Returns:
        None
    """
    if player0_result[1] == player1_result[1]:
        high_card_tie_break(player0_result[2], player1_result[2])
    else:
        high_card_tie_break(player0_result[1], player1_result[1])


def two_pairs_tie_break(player0_result, player1_result):
    """Resolve a tie between two hands containing two pairs.

    Comparison order:
        1. Higher pair
        2. Lower pair
        3. Kicker card

    Args:
        player0_result (tuple): Result tuple returned from hand evaluation
        for player 0.
        player1_result (tuple): Result tuple returned from hand evaluation
        for player 1.

    Returns:
        None
    """
    # 1. compare higher pair
    if player0_result[1] != player1_result[1]:
        high_card_tie_break(player0_result[1], player1_result[1])
        return

    # 2. compare lower pair
    if player0_result[2] != player1_result[2]:
        high_card_tie_break(player0_result[2], player1_result[2])
        return

    # 3. compare kicker
    high_card_tie_break(player0_result[3], player1_result[3])


def grouped_cards_tie_break(player0_result, player1_result):
    """Resolve a tie for grouped-card hands.

    Used for:
        - Three of a Kind
        - Full House
        - Four of a Kind

    First compares the value of the grouped cards (three/four),
    and if equal compares the remaining card.

    Args:
        player0_result (tuple): Result tuple returned from hand evaluation
        for player 0.
        player1_result (tuple): Result tuple returned from hand evaluation
        for player 1.

    Returns:
        None
    """
    if player0_result[1] == player1_result[1]:
        high_card_tie_break(player0_result[2], player1_result[2])
    else:
        high_card_tie_break(player0_result[1], player1_result[1])

