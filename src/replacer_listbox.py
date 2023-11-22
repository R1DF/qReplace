# Imports
from tkinter import Tk, Frame, Listbox, Scrollbar
from replacer import Replacer

# ReplacerListbox class
class ReplacerListbox(Listbox):
    def __init__(self, master: Tk | Frame, **args):
        self.master = master
        super().__init__(master, **args)
        self._contents = []

    # Methods
    def add_item(self, phrase: str, replacement: str):
        pass

    def edit_item(self, index: int, new_phrase: str, new_replacement: str):
        pass

    def remove_item(self, index: int):
        pass

    # Properties
    @property
    def contents(self) -> list[Replacer]:
        return self._contents
