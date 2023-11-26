# Imports
from tkinter import Tk, Toplevel, Frame, Entry, Label, Button, messagebox

# Base toplevel
class BaseToplevel(Toplevel):
    def __init__(self, master: Tk, name: str):
        # Initialisation
        super().__init__(master)
        self.master = master
        self.name = name

        # Configuration
        self.master.child_toplevels[self.name] = True
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master.child_toplevels[self.name] = False
        self.destroy()


# Add toplevel
class AddToplevel(BaseToplevel):
    def __init__(self, master):
        super().__init__(master, "add")
        # Initialisation
        self.title("Add entry")
        self.geometry("225x100")
        self.resizable(False, False)

        # Widget creation
        self.introduction_label = Label(self, text="Add new entry:")
        self.introduction_label.pack()

        self.information_frame = Frame(self)
        self.information_frame.pack()

        self.phrase_label = Label(self.information_frame, text="Phrase:")
        self.phrase_label.grid(row=0, column=0)

        self.phrase_entry = Entry(self.information_frame)
        self.phrase_entry.grid(row=0, column=1)

        self.replacement_label = Label(self.information_frame, text="Replacement:")
        self.replacement_label.grid(row=1, column=0)

        self.replacement_entry = Entry(self.information_frame)
        self.replacement_entry.grid(row=1, column=1)

        self.add_button = Button(self, text="Add", command=self.handle_add)
        self.add_button.pack()

    def handle_add(self):
        # Getting phrase and replacement
        phrase = self.phrase_entry.get().strip()
        replacement = self.replacement_entry.get().strip()

        # Validation
        if not phrase:
            messagebox.showerror("Error", "Please enter a phrase.")
            return

        if not replacement:
            messagebox.showerror("Error", "Please enter a replacement.")
            return

        # Adding and closing
        self.master.replacer_listbox.add_item(phrase, replacement)
        self.handle_close()


# Edit toplevel
class EditToplevel(BaseToplevel):
    def __init__(self, master, index: int, original_phrase: str, original_replacement: str):
        super().__init__(master, "edit")
        # Initialisation
        self.entry_index = index
        self.original_phrase = original_phrase
        self.original_replacement = original_replacement
        self.title("Edit entry")
        self.geometry("225x100")
        self.resizable(False, False)

        # Widget creation
        self.introduction_label = Label(self, text="Edit entry:")
        self.introduction_label.pack()

        self.information_frame = Frame(self)
        self.information_frame.pack()

        self.phrase_label = Label(self.information_frame, text="Phrase:")
        self.phrase_label.grid(row=0, column=0)

        self.phrase_entry = Entry(self.information_frame)
        self.phrase_entry.grid(row=0, column=1)
        self.phrase_entry.insert("end", original_phrase)

        self.replacement_label = Label(self.information_frame, text="Replacement:")
        self.replacement_label.grid(row=1, column=0)

        self.replacement_entry = Entry(self.information_frame)
        self.replacement_entry.grid(row=1, column=1)
        self.replacement_entry.insert("end", original_replacement)

        self.edit_button = Button(self, text="Edit", command=self.handle_edit)
        self.edit_button.pack()

    def handle_edit(self):
        # Getting new phrase and replacement
        phrase = self.phrase_entry.get().strip()
        replacement = self.replacement_entry.get().strip()

        # Validation
        if not phrase:
            messagebox.showerror("Error", "Please enter a phrase.")
            return

        if not replacement:
            messagebox.showerror("Error", "Please enter a replacement.")
            return

        # Editing and closing
        self.master.replacer_listbox.edit_item(self.entry_index, phrase, replacement)
        self.handle_close()
