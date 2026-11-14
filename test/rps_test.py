from app.rps import determine_winner


def test_winners():
    assert determine_winner("rock", "rock") == "TIE GAME"
    assert determine_winner("rock", "paper") == "COMPUTER WINS"
    assert determine_winner("rock", "scissors") == "USER WINS"
    assert determine_winner("paper", "rock") == "USER WINS"
    assert determine_winner("paper", "paper") == "TIE GAME"
    assert determine_winner("paper", "scissors") == "COMPUTER WINS"
    assert determine_winner("scissors", "scissors") == "TIE GAME"
    assert determine_winner("scissors", "paper") == "USER WINS"
    assert determine_winner("scissors", "rock") == "COMPUTER WINS"
