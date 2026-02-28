from poker.hand_logic import high_card

def high_card_tie_break(player0_high_card, player1_high_card):
    high_card_value = high_card([player0_high_card, player1_high_card])

    if player0_high_card== player1_high_card:
        print("draw")
    elif high_card_value == player1_high_card:
        print("player1 won")
    else:
        print("player0 won")


def pair_tie_break(player0_result, player1_result):
    if player0_result[1] == player1_result[1]:
        high_card_tie_break(player0_result[2], player1_result[2])
    else:
        high_card_tie_break(player0_result[1], player1_result[1])


def two_pairs_tie_break(player0_result, player1_result):
    # 1. porównanie wyższej pary
    if player0_result[1] != player1_result[1]:
        high_card_tie_break(player0_result[1], player1_result[1])
        return

    # 2. porównanie niższej pary
    if player0_result[2] != player1_result[2]:
        high_card_tie_break(player0_result[2], player1_result[2])
        return

    # 3. porównanie kickera
    high_card_tie_break(player0_result[3], player1_result[3])



def grouped_cards_tie_break(player0_result, player1_result):
    if player0_result[1] == player1_result[1]:
        high_card_tie_break(player0_result[2], player1_result[2])
    else:
        high_card_tie_break(player0_result[1], player1_result[1])



