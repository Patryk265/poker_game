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
        high_card_value = high_card([player0_result[1],  player1_result[1]])
        if high_card_value == player0_result[1]:
            print("player0 won")
        else:
            print("player1 won")

def two_pairs_tie_break(player0_result, player1_result):
    # 1. porównanie wyższej pary
    if player0_result[1] != player1_result[1]:
        high = high_card([player0_result[1], player1_result[1]])
        print("player0 won" if high == player0_result[1] else "player1 won")
        return

    # 2. porównanie niższej pary
    if player0_result[2] != player1_result[2]:
        high = high_card([player0_result[2], player1_result[2]])
        print("player0 won" if high == player0_result[2] else "player1 won")
        return

    # 3. porównanie kickera
    high_card_tie_break(player0_result[3], player1_result[3])



def three_of_kind_tie_break(player0_result, player1_result):
    if player0_result[1] == player1_result[1]:
        high_card_tie_break(player0_result[2], player1_result[2])
    else:
        high_card_value = high_card([player0_result[1], player1_result[1]])
        if high_card_value == player0_result[1]:
            print("player0 won")
        else:
            print("player1 won")








