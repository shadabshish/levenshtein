import Levenshtein as lev
import string
from collections import deque


def distance_to_secret(guess, secret):
    """
    Computes the Levenshtein distance between the guess and the secret word.

    Parameters:
    - guess (str): The current guess.
    - secret (str): The secret word to compare against.

    Returns:
    - int: The Levenshtein distance.
    """
    return lev.distance(guess, secret)


def generate_one_edit_neighbors(s):
    """
    Generates all strings that are one edit away from the input string.

    Parameters:
    - s (str): The current string.

    Returns:
    - set: A set of neighboring strings.
    """
    neighbors = set()
    letters = string.ascii_lowercase

    # Insertions
    for i in range(len(s) + 1):
        for c in letters:
            new_s = s[:i] + c + s[i:]
            neighbors.add(new_s)

    # Replacements
    for i in range(len(s)):
        for c in letters:
            if c != s[i]:
                new_s = s[:i] + c + s[i + 1:]
                neighbors.add(new_s)

    # Deletions
    if len(s) > 0:
        for i in range(len(s)):
            new_s = s[:i] + s[i + 1:]
            neighbors.add(new_s)

    return neighbors


def find_word_beam_search(secret, beam_size=3, max_steps=200):
    """
    Finds the secret word using Beam Search based on Levenshtein distance feedback.

    Parameters:
    - secret (str): The secret word to find.
    - beam_size (int): The number of top candidates to keep at each step.
    - max_steps (int): The maximum number of iterations to perform.

    Returns:
    - str: The found secret word or the best guess after max_steps.
    """
    possible_chars = string.ascii_lowercase
    beam = ['']  # Initialize beam with empty string
    visited = set([''])  # Keep track of visited guesses
    step = 0

    while step < max_steps and beam:
        step += 1
        new_candidates = []

        print(f"\nStep {step}, Beam: {beam}")

        for candidate in beam:
            neighbors = generate_one_edit_neighbors(candidate)

            for neighbor in neighbors:
                if neighbor in visited:
                    continue  # Skip already visited guesses

                distance = distance_to_secret(neighbor, secret)
                print(f"  Trying '{neighbor}': distance = {distance}")

                if distance == 0:
                    print(f"\nSecret word found: '{neighbor}' in {step} steps.")
                    return neighbor

                new_candidates.append((neighbor, distance))
                visited.add(neighbor)

        # Sort candidates by distance and select top beam_size
        new_candidates.sort(key=lambda x: x[1])
        beam = [candidate for candidate, _ in new_candidates[:beam_size]]

        print(f"New Beam after step {step}: {beam}")

    print("\nFailed to find the secret word within the step limit.")
    return beam[0] if beam else None
"""if __name__ == '__main__':
    secret_word = 'leonardo'  # Define your secret word here
    found_word = find_word_beam_search(secret_word, beam_size=3, max_steps=200)
    if found_word:
        print(f"\nFound secret word: '{found_word}'")
    else:
        print("\nFailed to find the secret word.")"""

if __name__ == '__main__':
    secret_word = input("Please enter the secret word (only lowercase letters, max 20 characters): ").strip().lower()
    if not secret_word.isalpha() or len(secret_word) > 20:
        print("Invalid input! The secret word must be alphabetic and have a maximum of 20 characters.")
    else:
        found_word = find_word_beam_search(secret_word, beam_size=3, max_steps=200)
        if found_word:
            print(f"\nFound secret word: '{found_word}'")
        else:
            print("\nFailed to find the secret word.")