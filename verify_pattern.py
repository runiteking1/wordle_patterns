"""
Monolithic file which does several things:
1. For each pattern, see if it's possible using every possible final solution.

For the Wordle output, 0 is gray, 1 is yellow and 2 is green.

There are a total of 3 ** 5 == 243 per row, meaning that there are
243 + 243 ** 2 + ... + 243 ** 5 = 850789802043 total combinations for Wordle art.
I'm just interested in the Christmas version...
"""

from typing import Union
import itertools
from collections import Counter
from tqdm import tqdm
import math

colors = {0: "⬜", 1: "🟨", 2: "🟩"}


def calculate_pattern(guess: str, sol: str) -> tuple:
    """
    Source: https://github.com/GillesVandewiele/Wordle-Bot/blob/main/wordle.py

    >>> calculate_pattern('weary', 'crane')
    (0, 1, 2, 1, 0)
    >>> calculate_pattern('meets', 'weary')
    (0, 2, 0, 0, 0)
    >>> calculate_pattern('rower', 'goner')
    (0, 2, 0, 2, 2)
    """
    wrong = [i for i, v in enumerate(guess) if v != sol[i]]
    counts = Counter(sol[i] for i in wrong)
    pattern = [2] * 5
    for i in wrong:
        v = guess[i]
        if counts[v] > 0:
            pattern[i] = 1
            counts[v] -= 1
        else:
            pattern[i] = 0
    return tuple(pattern)


def verify_pattern_possible(patterns: list, sol: str, word_list: list) -> bool:
    """
    Given a pattern and solution, determine if it's achievable or not.
    """
    assert len(patterns) <= 6, "Wordle may only have 6 guesses"

    # Build all possible patterns
    all_possible_patterns = set()
    for word in word_list:
        all_possible_patterns.add(calculate_pattern(word, sol))

    # See subset
    return set(patterns).issubset(all_possible_patterns)


def count_valid_words(guesses: Union[list, tuple], patterns: list, words: list):
    """
    Given the list of guesses and patterns, count the number of remaining "valid" guesses from the "words" list

    Note that one should pass in the list of possible solutions instead of the full word list, as aalii will never
    be a solution
    """
    valid_words = words
    for guess, pattern in zip(guesses, patterns):
        # For each guess/pattern output from guess, filter out the words
        valid_words = [w for w in valid_words if calculate_pattern(guess, w) == pattern]
    return len(valid_words), valid_words


def strictly_decreasing(L):
    # From stackoverflow
    return all(x > y for x, y in zip(L, L[1:]))


def gen_possible_guesses(patterns: Union[list, tuple], sol: str, word_list: list, sol_list: list):
    """
    Given the patterns and the solution, generate a possible set of guesses where each guess actually
    makes sense in that it lowers the total number of possible words.
    """
    assert verify_pattern_possible(patterns, sol, word_list), "Pattern not possible with word."

    for row in patterns:
        print("".join(colors[i] for i in row))

    # Since patterns are possible, we need to construct the wordlist for each pattern
    possible_guesses_per_pattern = [[] for _ in range(len(patterns))]

    for word in word_list:
        pattern = calculate_pattern(word, sol)
        if pattern in patterns:
            # Just do a dumb for loop; note that in theory pattern can repeat so cannot use .index()
            for i, given_pattern in enumerate(patterns):
                if given_pattern == pattern:
                    possible_guesses_per_pattern[i].append(word)

    # Now brute force more; start from the first word
    total_combinations = math.prod(len(guesses) for guesses in possible_guesses_per_pattern)
    print(f"Total items to process: {total_combinations:,}")

    for combination in tqdm(itertools.product(*possible_guesses_per_pattern)):
        # Since it's a max of only 6, might as well just find the number of valid guesses for each
        num_words = [count_valid_words(combination[0:i + 1], patterns[0:i + 1], sol_list)[0] for i in
                     range(len(combination))]
        if strictly_decreasing(num_words):
            print(*combination)
            break


if __name__ == '__main__':
    # Load all words and solutions
    with open('words.txt') as f:
        all_words = [line.strip() for line in f.readlines()]
    with open('solutions.txt') as f:
        all_sols = [line.strip() for line in f.readlines()]

    gen_possible_guesses([(0, 0, 1, 0, 0), (0, 0, 2, 0, 0), (0, 2, 2, 2, 0), (2, 2, 2, 2, 2)],
                         'prism', all_words, all_sols)

    # This pattern would be easier if "Christmas" themed words are used
    # gen_possible_guesses([(0, 0, 1, 0, 0), (0, 0, 2, 0, 0), (0, 2, 2, 2, 0), (2, 2, 2, 2, 2)],
    #                          'angel', all_words, all_sols)
    #
    # gen_possible_guesses([(0, 0, 1, 0, 0), (0, 0, 2, 0, 0), (0, 2, 2, 2, 0), (2, 2, 2, 2, 2)],
    #                          'carol', all_words, all_sols)
