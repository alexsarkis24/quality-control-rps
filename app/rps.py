import random

VALID_OPTIONS = ["rock", "paper", "scissors"]


def generate_random_choice():
    return random.choice(VALID_OPTIONS)


def determine_winner(u, c):
    if u == c:
        return "TIE GAME"
    elif u == "rock" and c == "scissors":
        return "USER WINS"
    elif u == "paper" and c == "rock":
        return "USER WINS"
    elif u == "scissors" and c == "paper":
        return "USER WINS"
    else:
        return "COMPUTER WINS"


if __name__ == "__main__":
    user_choice = input("Please choose one of 'rock', 'paper', or 'scissors': ")
    if user_choice not in VALID_OPTIONS:
        print("OOPS INVALID INPUT, PLEASE TRY AGAIN")
        quit()
    computer_choice = generate_random_choice()
    print("USER:", user_choice)
    print("COMP:", computer_choice)
    print(determine_winner(user_choice, computer_choice))
