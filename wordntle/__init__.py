from __future__ import annotations

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


def write_fake_words(words: Set[str]):
    with open(cwd / "fake_words.txt", "w") as _out:
        _out.write("\n".join(words))


def main():
    words = get_words()
    invalid_words = get_all_words()
    model = build_model(words)

    fake_words = set()
    for i in range(5000):
        print("----", i)
        word = generate_word(model, 5, invalid_words=invalid_words)
        if word in invalid_words:
            raise Exception("Duplicate word generated!")

        # Collect list of fake words
        fake_words.add(word)

        # Don't generate this word again
        invalid_words.add(word)

    write_fake_words(fake_words)


if __name__ == "__main__":
    main()
