# Imports
from tkinter import Tk, Toplevel, Frame, Entry, Label, Button

# Base toplevel
class BaseToplevel(Toplevel):
    def __init__(self, master: Tk, name: str):
        super().__init__(master)
        self.master = master
        self.name = name
        self.master.child_toplevels[self.name] = True
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master.child_toplevels[self.name] = False
        self.destroy()


# Add toplevel
class AddToplevel(BaseToplevel):
    def __init__(self, master):
        super().__init__(master, "add")
        self.title("Add entry")


# Edit toplevel
class EditToplevel(BaseToplevel):
    def __init__(self, master):
        super().__init__(master, "edit")
        self.title("Edit entry")
