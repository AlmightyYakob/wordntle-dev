from __future__ import annotations
import random

__version__ = "0.1.0"

from pathlib import Path
from typing import Set

import markovify

cwd = Path(__file__).parent


def get_words():
    with open(cwd / "words.txt") as _in:
        return set(_in.read().splitlines())


def get_all_words():
    with open(cwd / "all_words.txt") as _in:
        return set(_in.read().splitlines())


def analyze_words():
    """Determine all groups of vowels and consonants."""


def build_model(words: Set[str], state_size=2):
    model = None
    for word in words:
        new_model = markovify.Text(" ".join(word), state_size=state_size)
        if model is not None:
            new_model = markovify.combine([new_model, model])

        model = new_model

    return model


def generate_word(model: markovify.Text, length: int, invalid_words: Set[str]):
    """Generate a new word (doesn't exist in invalid_words)."""
    while True:
        word: str | None = model.make_sentence(min_words=length, max_words=length)
        if word is None:
            continue

        word = word.replace(" ", "")
        if word not in invalid_words:
            return word


def main():
    words = get_words()
    invalid_words = get_all_words()
    model = build_model(words)

    fake_words = set()
    for i in range(15000):
        print("----", i)
        word = generate_word(model, 5, invalid_words=invalid_words)
        if word in invalid_words:
            raise Exception("Duplicate word generated!")

        # Collect list of fake words
        fake_words.add(word)

        # Don't generate this word again
        invalid_words.add(word)

    # Write total list of fake words
    with open(cwd / "all_fake_words.txt", "w") as _out:
        _out.write("\n".join(fake_words))

    # Select subset of all fake words as answers and write out
    answers = set(random.sample(fake_words, 3000))
    with open(cwd / "answers.txt", "w") as _out:
        _out.write("\n".join(answers))

    # Select remainder of that set and write out
    allowed_guesses = fake_words - answers
    with open(cwd / "allowed_guesses.txt", "w") as _out:
        _out.write("\n".join(allowed_guesses))


if __name__ == "__main__":
    main()
