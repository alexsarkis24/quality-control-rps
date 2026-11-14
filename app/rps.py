"""Rock, paper, scissors game logic and command-line interface."""

import random

VALID_OPTIONS = ["rock", "paper", "scissors"]

# Maps each option to the option it defeats.
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

TIE = "TIE GAME"
USER_WINS = "USER WINS"
COMPUTER_WINS = "COMPUTER WINS"


def generate_random_choice():
    """Returns a random valid option for the computer."""
    return random.choice(VALID_OPTIONS)


def is_valid_choice(choice):
    """Returns True if the choice is one of the valid options."""
    return choice in VALID_OPTIONS


def determine_winner(u, c):
    """Determines the winner.

    Params:
        u (str): the user's choice
        c (str): the computer's choice

    Returns one of TIE, USER_WINS, COMPUTER_WINS.
    Raises ValueError for an invalid choice.
    """
    if not (is_valid_choice(u) and is_valid_choice(c)):
        raise ValueError(f"Invalid choice. Must be one of {VALID_OPTIONS}")
    if u == c:
        return TIE
    return USER_WINS if BEATS[u] == c else COMPUTER_WINS


def play(user_choice, computer_choice=None):
    """Plays one round and returns the computer's choice and the result."""
    computer_choice = computer_choice or generate_random_choice()
    return computer_choice, determine_winner(user_choice, computer_choice)


if __name__ == "__main__":
    user_choice = input("Please choose one of 'rock', 'paper', or 'scissors': ").strip().lower()
    print("USER:", user_choice)

    if not is_valid_choice(user_choice):
        print("OOPS INVALID INPUT, PLEASE TRY AGAIN")
        quit()

    computer_choice, result = play(user_choice)
    print("COMP:", computer_choice)
    print(result)
