import pytest
from poker.tie_break import (
    high_card_tie_break,
    pair_tie_break,
    two_pairs_tie_break,
    grouped_cards_tie_break,
)

# =====================================================
# HIGH CARD
# =====================================================

@pytest.mark.parametrize(
    "player0, player1, expected",
    [
        ("10", "10", "draw"),
        ("A", "10", "player0 won"),
        ("9", "K", "player1 won"),
        ("2", "A", "player1 won"),
        ("Q", "J", "player0 won"),
    ],
)
def test_high_card_tie_break(player0, player1, expected, capsys):
    high_card_tie_break(player0, player1)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


# =====================================================
# PAIR
# Format: (rank, pair_value, kicker)
# =====================================================

@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # identical pair → kicker
        ((2, "10", "A"), (2, "10", "9"), "player0 won"),
        ((2, "10", "9"), (2, "10", "A"), "player1 won"),

        # draw
        ((2, "10", "K"), (2, "10", "K"), "draw"),

        # different pairs
        ((2, "J", "2"), (2, "9", "A"), "player0 won"),
        ((2, "9", "A"), (2, "J", "2"), "player1 won"),

        # low pairs
        ((2, "2", "A"), (2, "3", "K"), "player1 won"),
    ],
)
def test_pair_tie_break(player0_result, player1_result, expected, capsys):
    pair_tie_break(player0_result, player1_result)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


# =====================================================
# TWO PAIRS
# Format: (rank, high_pair, low_pair, kicker)
# =====================================================

@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # różna najwyższa para
        ((3, "K", "10", "2"), (3, "Q", "J", "A"), "player0 won"),
        ((3, "Q", "10", "2"), (3, "K", "J", "A"), "player1 won"),

        # taka sama najwyższa para, różna niższa
        ((3, "K", "Q", "2"), (3, "K", "J", "A"), "player0 won"),
        ((3, "K", "J", "A"), (3, "K", "Q", "2"), "player1 won"),

        # takie same pary → kicker
        ((3, "K", "10", "A"), (3, "K", "10", "9"), "player0 won"),
        ((3, "K", "10", "9"), (3, "K", "10", "A"), "player1 won"),

        # pełny remis
        ((3, "K", "10", "A"), (3, "K", "10", "A"), "draw"),
    ],
)
def test_two_pairs_tie_break(player0_result, player1_result, expected, capsys):
    two_pairs_tie_break(player0_result, player1_result)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

# =====================================================
# THREE OF A KIND / FULL HOUSE
# Format: (rank, pair, kicker)
# =====================================================


@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # identical three of a kind kicker decides
        ((4, "K", "4"), (4, "K", "3"), "player0 won"),
        ((4, "10", "4"), (4, "10", "5"), "player1 won"),

        # not identical three of a kind
        ((4, "A", "4"), (4, "K", "3"), "player0 won"),
        ((4, "4", "4"), (4, "7", "3"), "player1 won"),

        # draw
        ((4, "5", "8"), (4, "5", "8"), "draw"),

        # FULL HOUSE
        # different three of a kind
        ((7, "K", "10"), (7, "Q", "A"), "player0 won"),
        ((7, "9", "A"), (7, "J", "2"), "player1 won"),

        # same three, different pair
        ((7, "K", "Q"), (7, "K", "J"), "player0 won"),
        ((7, "10", "2"), (7, "10", "A"), "player1 won"),

        # draw
        ((7, "K", "10"), (7, "K", "10"), "draw"),
    ],
)
def test_three_tie_break(player0_result, player1_result, expected, capsys):
    grouped_cards_tie_break(player0_result, player1_result)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected




# =====================================================
# STRAIGHT / FLUSH / STRAIGHT FLUSH
# Format: (rank, high_card)
# =====================================================

@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # straight
        ((5, "K"), (5, "Q"), "player0 won"),
        ((5, "9"), (5, "A"), "player1 won"),
        ((5, "10"), (5, "10"), "draw"),

        # flush
        ((6, "A"), (6, "K"), "player0 won"),
        ((6, "9"), (6, "Q"), "player1 won"),
        ((6, "J"), (6, "J"), "draw"),

        # straight flush
        ((9, "K"), (9, "Q"), "player0 won"),
        ((9, "10"), (9, "A"), "player1 won"),
        ((9, "J"), (9, "J"), "draw"),
    ],
)
def test_high_card_based_tie_break(player0_result, player1_result, expected, capsys):
    high_card_tie_break(player0_result[1], player1_result[1])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


# =====================================================
# FULL HOUSE
# Format: (rank, three, pair)
# =====================================================

@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # different three of a kind
        ((7, "K", "10"), (7, "Q", "A"), "player0 won"),
        ((7, "9", "A"), (7, "J", "2"), "player1 won"),

        # same three, different pair
        ((7, "K", "Q"), (7, "K", "J"), "player0 won"),
        ((7, "10", "2"), (7, "10", "A"), "player1 won"),

        # draw
        ((7, "K", "10"), (7, "K", "10"), "draw"),
    ],
)
def test_full_house_tie_break(player0_result, player1_result, expected, capsys):
    # full house używa logiki grouped_cards_tie_break
    grouped_cards_tie_break(
        (4, player0_result[1], player0_result[2]),
        (4, player1_result[1], player1_result[2]),
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == expected


# =====================================================
# FOUR OF A KIND
# Format: (rank, four, kicker)
# =====================================================

@pytest.mark.parametrize(
    "player0_result, player1_result, expected",
    [
        # different four
        ((8, "K", "2"), (8, "Q", "A"), "player0 won"),
        ((8, "9", "A"), (8, "J", "2"), "player1 won"),

        # same four → kicker
        ((8, "K", "Q"), (8, "K", "J"), "player0 won"),
        ((8, "10", "2"), (8, "10", "A"), "player1 won"),

        # draw
        ((8, "K", "10"), (8, "K", "10"), "draw"),
    ],
)
def test_four_of_kind_tie_break(player0_result, player1_result, expected, capsys):
    grouped_cards_tie_break(
        (4, player0_result[1], player0_result[2]),
        (4, player1_result[1], player1_result[2]),
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == expected
