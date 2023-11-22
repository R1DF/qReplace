# Replacer class
class Replacer:
    def __init__(self, phrase: str, replacement: str):
        self.phrase = phrase
        self.replacement = replacement

    def get_ahk_code(self, prefix: str) -> str:
        return f":?c*:{prefix}{self.phrase}::{self.replacement}"


    def __repr__(self) -> str:
        return f"Replacer (\"{self.phrase}\" ---> \"{self.replacement}\")"
