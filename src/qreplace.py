# Imports
from tkinter import Tk, Frame, Entry, Label, Button, Menu, PhotoImage, messagebox, filedialog
from config_reader import ConfigReader
from replacer_listbox import ReplacerListbox
from toplevels import AddToplevel, EditToplevel
from file_manager import save_list_as_ahk, open_ahk_as_dict
import os


# QReplace class
class QReplace(Tk):
    def __init__(self, version: str, configurations: ConfigReader):
        # Window creation
        super().__init__()
        self.child_toplevels = {
            "add": False,
            "edit": False,
            "open_recent": False,
            "preferences": False,
            "about": False
        }
        self.version = version
        self.configurations = configurations
        self.title(f"qReplace v{version}")
        self.resizable(False, False)
        self.geometry(f"{self.configurations.get('resolution')[0]}x{self.configurations.get('resolution')[1]}")
        self.recent_files = []

        # Setting icon
        self.icon_photoimage = PhotoImage(file=os.path.join(os.getcwd(), "assets", "icon_32x32.png"))
        self.iconphoto(True, self.icon_photoimage)

        # Laying out menu
        self.main_menu_bar = Menu(self, tearoff=0)
        self.file_menu = Menu(self.main_menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.handle_new)
        self.file_menu.add_command(label="Open", command=self.handle_open)
        self.file_menu.add_command(label="Open recent", command=self.handle_open_recent)
        self.main_menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.qreplace_menu = Menu(self.main_menu_bar, tearoff=0)
        self.qreplace_menu.add_command(label="Preferences", command=self.handle_preferences)
        self.qreplace_menu.add_command(label="About", command=self.handle_about)
        self.qreplace_menu.add_separator()
        self.qreplace_menu.add_command(label="Check for updates", command=self.handle_check_for_updates)
        self.main_menu_bar.add_cascade(label="qReplace", menu=self.qreplace_menu)

        self.config(menu=self.main_menu_bar)

        # Laying out widgets
        self.introduction_label = Label(self, text="qReplace")
        self.introduction_label.pack()

        self.main_frames_frame = Frame(self)
        self.main_frames_frame.pack()

        self.left_frame = Frame(self.main_frames_frame)
        self.left_frame.grid(row=0, column=0, padx=15)

        self.right_frame = Frame(self.main_frames_frame)
        self.right_frame.grid(row=0, column=1, padx=15)

        self.replacer_listbox = ReplacerListbox(self.left_frame, width=35, height=12)

        self.entries_frame = Frame(self.right_frame)
        self.entries_frame.pack()

        self.prefix_label = Label(self.entries_frame, text="Prefix:")
        self.prefix_label.grid(row=0, column=0)

        self.prefix_entry = Entry(self.entries_frame, width=18)
        self.prefix_entry.grid(row=0, column=1)
        self.prefix_entry.insert("end", self.configurations.get("default_prefix"))

        self.suffix_label = Label(self.entries_frame, text="Suffix:")
        self.suffix_label.grid(row=1, column=0)

        self.suffix_entry = Entry(self.entries_frame, width=18)
        self.suffix_entry.grid(row=1, column=1)
        self.suffix_entry.insert("end", self.configurations.get("default_suffix"))

        self.buttons_frame = Frame(self.right_frame)
        self.buttons_frame.pack()

        self.add_button = Button(self.buttons_frame, text="Add", width=15, command=self.handle_add)
        self.add_button.pack(pady=4)

        self.edit_button = Button(self.buttons_frame, text="Edit", width=15, command=self.handle_edit)
        self.edit_button.pack(pady=4)

        self.remove_button = Button(self.buttons_frame, text="Remove", width=15, command=self.handle_remove)
        self.remove_button.pack(pady=4)

        self.save_button = Button(self.buttons_frame, text="Save", width=15, command=self.handle_save)
        self.save_button.pack(pady=4)

        # Mainloop
        self.mainloop()

    # Handler methods
    def handle_add(self):
        if not self.child_toplevels["add"]:
            AddToplevel(self)

    def handle_edit(self):
        if not self.child_toplevels["edit"]:
            # Getting index of the entry in the listbox to edit
            entry_index = self.replacer_listbox.replacer_listbox.curselection()

            if not entry_index:  # If the user didn't select an entry
                messagebox.showerror("Error", "Please select an entry to edit.")
                return

            # Creating edit entry
            original_phrase = self.replacer_listbox.contents[entry_index[0]].phrase
            original_replacement = self.replacer_listbox.contents[entry_index[0]].replacement
            EditToplevel(self, entry_index[0], original_phrase, original_replacement)

    def handle_remove(self):
        # Getting index of the entry in the listbox to remove
        entry_index = self.replacer_listbox.replacer_listbox.curselection()

        if not entry_index:  # If the user didn't select an entry
            messagebox.showerror("Error", "Please select an entry to remove.")
            return

        # Removing item
        self.replacer_listbox.remove_item(entry_index[0])

    def handle_save(self):
        if self.replacer_listbox.is_empty:
            messagebox.showerror("Error", "Please add an entry to the list before saving.")
            return

        # Getting data
        prefix = self.prefix_entry.get().strip()
        suffix = self.suffix_entry.get().strip()
        if not prefix:
            messagebox.showerror("Error", "A prefix is required.")
            return

        else:
            path = filedialog.asksaveasfilename(filetypes=[
                    ("AutoHotKey file", "*.ahk")
                ]
            )

            if path:
                # Saving data to .ahk file
                save_list_as_ahk(path, prefix, suffix, self.version, self.replacer_listbox.contents)

    def handle_new(self):
        self.prefix_entry.delete(0, "end")
        self.suffix_entry.delete(0, "end")
        self.replacer_listbox.erase()

    def handle_open(self):
        path = filedialog.askopenfilename(filetypes=[
                    ("AutoHotKey file", "*.ahk")
                ]
            )
        if path:
            # Getting data from function
            file_data = open_ahk_as_dict(path)
            prefix = file_data["prefix"]
            suffix = file_data["suffix"]
            replacers_list = file_data["replacers"]

            # Adding to recent (or putting to top)
            if path not in self.recent_files:
                self.recent_files.append(path)
            else:
                self.recent_files.remove(path)
                self.recent_files.append(path)

            # Setting up prefixes
            self.prefix_entry.delete(0, "end")
            self.suffix_entry.delete(0, "end")
            self.prefix_entry.insert("end", prefix)
            self.suffix_entry.insert("end", suffix)

            # Copying replacers
            self.replacer_listbox.erase()
            for phrase, suffix in replacers_list:
                self.replacer_listbox.add_item(phrase, suffix)

    def handle_open_recent(self):
        pass

    def handle_preferences(self):
        pass

    def handle_about(self):
        pass

    def handle_check_for_updates(self):
        pass
