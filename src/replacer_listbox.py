# Imports
from tkinter import Tk, Frame, Listbox, Scrollbar
from replacer import Replacer

# ReplacerListbox class
class ReplacerListbox:
    def __init__(self, master: Tk | Frame, **args):
        self.master = master
        self.replacer_listbox_frame = Frame(master)
        self.replacer_listbox_frame.pack()

        self.replacer_listbox = Listbox(self.replacer_listbox_frame, **args)
        self.replacer_listbox.pack(side="left")

        self.scrollbar = Scrollbar(self.replacer_listbox_frame)
        self.scrollbar.pack(side="right", fill="both")

        self.replacer_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.replacer_listbox.yview)

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
