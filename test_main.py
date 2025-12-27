import pytest
import main


@pytest.mark.parametrize("colors,values,expected", [
    (["Hearts"] * 5, ["10", "J", "Q", "K", "A"], True),
    (["Hearts", "Hearts", "Clubs", "Hearts", "Hearts"], ["10", "J", "Q", "K", "A"], False),
    (["Spades"] * 5, ["9", "10", "J", "Q", "K"], False),
    (["Diamonds"] * 5, ["K", "A", "Q", "10", "J"], True),
])

def test_is_royal_flush(colors, values, expected) -> None:
    assert main.is_royal_flush(colors, values) == expected



@pytest.mark.parametrize("values, expected", [
    (["10", "J", "Q", "K", "A"], True),
    (["9", "10", "J", "Q", "K"], True),
    (["7", "8", "3", "Q", "K"], False),
    (["2", "3", "Q", "K", "10"], False),
    (["1"], False)

])
def test_is_straight(values, expected) -> None:
    assert main.is_straight(values) == expected


@pytest.mark.parametrize("colors, expected", [
    (["Hearts"] * 5, True),
    (["Spades"] * 5, True),
    (["Diamonds", "Hearts", "Spades", "Diamonds", "Diamonds"], False),
    (["Diamonds", "Hearts", "Hearts", "Diamonds", "Hearts"], False),

])
def test_check_flush(colors, expected) -> None:
    assert main.check_flush(colors) == expected


@pytest.mark.parametrize("values, expected", [
    (["10", "10", "Q", "A", "K"], ["10"]),
    (["Q", "Q", "3", "5", "6"], ["Q"]),
    (["7", "8", "3", "Q", "K"], []),
    (["2", "3", "Q", "K", "10"], []),

])

def test_find_pairs(values, expected) -> None:
    assert sorted(main.find_pairs(values)) == sorted(expected)


@pytest.mark.parametrize("values,expected", [
    (["A", "A", "A", "Q", "K"], True),
    (["9", "9", "9", "3", "3"], True),
    (["A", "K", "Q", "J", "10"], False),
])
def test_find_three_of_a_kind(values, expected) -> None:
    assert bool(main.find_three_of_a_kind(values)) == expected


@pytest.mark.parametrize("values,expected", [
    (["A", "A", "A", "A", "K"], True),
    (["9", "9", "9", "3", "3"], False),
])
def test_find_four_of_a_kind(values, expected) -> None:
    assert bool(main.find_four_of_a_kind(values)) == expected


@pytest.mark.parametrize("values,expected", [
    (["A", "A", "A", "K", "K"], True),
    (["A", "A", "A", "A", "K"], False),
    (["A", "A", "K", "K", "Q"], False),
])
def test_has_full_house(values, expected) -> None:
    assert bool(main.has_full_house(values)) == expected

@pytest.mark.parametrize("values, expected", [
    (["2", "5", "J", "9", "A"], "A"),
    (["2", "3", "4", "5", "6"], "6"),
])
def test_high_card(values, expected):
    assert main.high_card(values) == expected
