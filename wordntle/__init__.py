__version__ = "0.1.0"

from pathlib import Path

cwd = Path(__file__).parent


def get_words():
    with open(cwd / "words.txt") as _in:
        return _in.read().splitlines()


def analyze_words():
    """Determine all groups of vowels and consonants."""
