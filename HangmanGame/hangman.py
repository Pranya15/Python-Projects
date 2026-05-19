import random


WORDS = ["apple", "grape", "stone", "chair", "plant"]
MAX_INCORRECT = 6


def choose_word():
    return random.choice(WORDS)


def display_progress(secret_word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in secret_word)


def get_guess(guessed_letters):
    while True:
        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one letter.")
        elif guess in guessed_letters:
            print("You already guessed that letter.")
        else:
            return guess


def play_game():
    secret_word = choose_word()
    guessed_letters = []
    incorrect_guesses = 0

    print("Welcome to Hangman!")
    print(f"You have {MAX_INCORRECT} incorrect guesses.\n")

    while incorrect_guesses < MAX_INCORRECT:
        print("Word:", display_progress(secret_word, guessed_letters))
        print("Guessed letters:", ", ".join(guessed_letters) if guessed_letters else "None")
        print(f"Incorrect guesses left: {MAX_INCORRECT - incorrect_guesses}")

        guess = get_guess(guessed_letters)
        guessed_letters.append(guess)

        if guess in secret_word:
            print("Correct!\n")
        else:
            incorrect_guesses += 1
            print("Wrong!\n")

        if all(letter in guessed_letters for letter in secret_word):
            print("Word:", display_progress(secret_word, guessed_letters))
            print("You win!")
            return

    print(f"You lose. The word was '{secret_word}'.")


if __name__ == "__main__":
    play_game()
