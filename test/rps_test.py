import pytest

from app.rps import (
    COMPUTER_WINS, TIE, USER_WINS, VALID_OPTIONS,
    determine_winner, generate_random_choice, is_valid_choice, play,
)


@pytest.mark.parametrize("u,c,expected", [
    ("rock", "rock", TIE), ("rock", "paper", COMPUTER_WINS), ("rock", "scissors", USER_WINS),
    ("paper", "rock", USER_WINS), ("paper", "paper", TIE), ("paper", "scissors", COMPUTER_WINS),
    ("scissors", "rock", COMPUTER_WINS), ("scissors", "paper", USER_WINS), ("scissors", "scissors", TIE),
])
def test_determine_winner(u, c, expected):
    assert determine_winner(u, c) == expected


def test_determine_winner_invalid():
    with pytest.raises(ValueError):
        determine_winner("lizard", "rock")


def test_generate_random_choice():
    for _ in range(50):
        assert generate_random_choice() in VALID_OPTIONS


def test_is_valid_choice():
    assert is_valid_choice("rock")
    assert not is_valid_choice("ROCK")
    assert not is_valid_choice("")


def test_play_with_fixed_computer_choice():
    assert play("rock", "scissors") == ("scissors", USER_WINS)


def test_play_random_computer_choice(monkeypatch):
    monkeypatch.setattr("app.rps.generate_random_choice", lambda: "paper")
    assert play("rock") == ("paper", COMPUTER_WINS)


def test_determine_winner_rejects_wrong_case():
    with pytest.raises(ValueError):
        determine_winner("Rock", "paper")
