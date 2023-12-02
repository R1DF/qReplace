# Imports
from constants import SPECIAL_TO_REPRESENTATION


# Replacer class
class Replacer:
    def __init__(self, phrase: str, replacement: str):
        self.phrase = phrase
        self.replacement = replacement

    def get_ahk_code(self, prefix: str = "", suffix: str = "") -> str:
        replacement = ""

        # Ensuring special character presence and replacing
        for letter in self.replacement:
            replacement += SPECIAL_TO_REPRESENTATION.get(letter, letter)

        return f":?c*:{prefix}{self.phrase}{suffix}::{replacement}"


    def __repr__(self) -> str:
        return f"Replacer (\"{self.phrase}\" ---> \"{self.replacement}\")"
