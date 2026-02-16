import pytest
from poker import main


def test_generate_deck_has_52_unique_cards() -> None:
    deck = main.generate_deck()

    assert len(deck) == 52
    assert len(set(deck)) == 52

def test_deal_cards_deals_correct_number_of_cards() -> None:
    deck = main.generate_deck()
    users_cards = main.deal_cards(deck, amount_of_users=2)

    assert len(users_cards) == 2
    assert all(len(cards) == 5 for cards in users_cards.values())

def test_deal_cards_removes_cards_from_deck() -> None:
    deck = main.generate_deck()
    original_len = len(deck)

    main.deal_cards(deck, amount_of_users=2)

    assert len(deck) == original_len - 10

def extract_colors_and_values(
    cards: list[tuple[str, str]],
) -> tuple[list[str], list[str]]:
    colors = [color for color, _ in cards]
    values = [value for _, value in cards]
    return colors, values

def test_evaluate_hand_royal_flush() -> None:
    cards = [
        ("Hearts", "10"),
        ("Hearts", "J"),
        ("Hearts", "Q"),
        ("Hearts", "K"),
        ("Hearts", "A"),
    ]

    result = main.evaluate_hand(cards)

    assert result == 10


def test_evaluate_hand_straight_flush() -> None:
    cards = [
        ("Spades", "9"),
        ("Spades", "10"),
        ("Spades", "J"),
        ("Spades", "Q"),
        ("Spades", "K"),
    ]

    result = main.evaluate_hand(cards)

    assert result == (9, "K")


def test_evaluate_hand_one_pair() -> None:
    cards = [
        ("Hearts", "3"),
        ("Spades", "3"),
        ("Clubs", "9"),
        ("Diamonds", "J"),
        ("Hearts", "K"),
    ]

    result = main.evaluate_hand(cards)

    assert result[0] == 2


def test_change_cards_replaces_selected_cards() -> None:
    cards = [
        ("Hearts", "2"),
        ("Spades", "3"),
        ("Clubs", "4"),
        ("Diamonds", "5"),
        ("Hearts", "6"),
    ]

    deck = [
        ("Spades", "A"),
        ("Clubs", "K"),
    ]

    main.change_cards(cards, deck, indices=[1, 3])

    assert cards[1] == ("Spades", "A")
    assert cards[3] == ("Clubs", "K")
    assert len(deck) == 0

def test_change_cards_invalid_index_raises() -> None:
    cards = [("Hearts", "2")] * 5
    deck = [("Spades", "A")]

    with pytest.raises(IndexError):
        main.change_cards(cards, deck, indices=[10])
