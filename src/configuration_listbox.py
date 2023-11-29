# Imports
from tkinter import Tk, Toplevel, Frame, Listbox, Scrollbar


# ConfigurationListbox class
class ConfigurationListbox:
    def __init__(self, master: Tk | Frame, controlling_window: Tk | Toplevel, callback, **args):
        # Initialisation
        self.master = master
        self.controlling_window = controlling_window
        self.callback = callback
        self._contents = []

        # Widget creation
        self.configuration_listbox_frame = Frame(master)
        self.configuration_listbox_frame.pack()

        self.configuration_listbox = Listbox(self.configuration_listbox_frame, **args)
        self.configuration_listbox.pack(side="left")

        self.scrollbar = Scrollbar(self.configuration_listbox_frame)
        self.scrollbar.pack(side="right", fill="both")

        self.configuration_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.configuration_listbox.yview)

        # Binding
        self.controlling_window.bind("<<ListboxSelect>>", self.handle_listbox_select, add="+")

    def add_setting(self, name: str, display_name: str):
        self.configuration_listbox.insert("end", display_name)
        self._contents.append(name)

    def handle_listbox_select(self, event=None):
        if curselection := self.configuration_listbox.curselection():
            setting_index = curselection[0]
            self.callback(self.contents[setting_index])


    # Properties
    @property
    def contents(self) -> list[str]:
        return self._contents
