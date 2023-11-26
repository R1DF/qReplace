# Imports
from tkinter import Tk, Frame, Listbox, Scrollbar
from replacer import Replacer


# ReplacerListbox class
class ReplacerListbox:
    def __init__(self, master: Tk | Frame, **args):
        # Initialisation
        self.master = master
        self._contents = []

        # Widget creation
        self.replacer_listbox_frame = Frame(master)
        self.replacer_listbox_frame.pack()

        self.replacer_listbox = Listbox(self.replacer_listbox_frame, **args)
        self.replacer_listbox.pack(side="left")

        self.scrollbar = Scrollbar(self.replacer_listbox_frame)
        self.scrollbar.pack(side="right", fill="both")

        self.replacer_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.replacer_listbox.yview)

    # Methods
    def add_item(self, phrase: str, replacement: str):
        self._contents.append(Replacer(phrase, replacement))
        self.replacer_listbox.insert("end", f"{phrase}: {replacement}")

    def edit_item(self, index: int, new_phrase: str, new_replacement: str):
        self.remove_item(index)
        self._contents.insert(index, Replacer(new_phrase, new_replacement))
        self.replacer_listbox.insert(index, f"{new_phrase}: {new_replacement}")

    def remove_item(self, index: int):
        self._contents.pop(index)
        self.replacer_listbox.delete(index)

    def erase(self):
        self._contents = []
        self.replacer_listbox.delete(0, "end")

    # Properties
    @property
    def contents(self) -> list[Replacer]:
        return self._contents

    @property
    def is_empty(self) -> bool:
        return len(self._contents) == 0
