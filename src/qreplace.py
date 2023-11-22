# Imports
from tkinter import Tk, Frame, Entry, Label, Button, Menu, PhotoImage
from config_reader import ConfigReader
from replacer_listbox import ReplacerListbox
import os


# QReplace class
class QReplace(Tk):
    def __init__(self, version: str, configurations: ConfigReader):
        # Window creation
        super().__init__()
        self.configurations = configurations
        self.title(f"qReplace v{version}")
        self.resizable(False, False)
        self.geometry(f"{self.configurations.get('resolution')[0]}x{self.configurations.get('resolution')[1]}")

        # Setting icon
        self.icon_photoimage = PhotoImage(file=os.path.join(os.getcwd(), "assets", "icon_32x32.png"))
        self.iconphoto(True, self.icon_photoimage)

        # Laying out menu
        self.main_menu_bar = Menu(self, tearoff=0)
        self.file_menu = Menu(self.main_menu_bar, tearoff=0)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Reset")
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Open recent")
        self.main_menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.qreplace_menu = Menu(self.main_menu_bar, tearoff=0)
        self.qreplace_menu.add_command(label="Preferences")
        self.qreplace_menu.add_command(label="About")
        self.qreplace_menu.add_separator()
        self.qreplace_menu.add_command(label="Check for updates")
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

        self.prefix_entry = Entry(self.entries_frame)
        self.prefix_entry.grid(row=0, column=1)
        self.prefix_entry.insert("end", self.configurations.get("default_prefix"))

        self.suffix_label = Label(self.entries_frame, text="Suffix:")
        self.suffix_label.grid(row=1, column=0)

        self.suffix_entry = Entry(self.entries_frame)
        self.suffix_entry.grid(row=1, column=1)
        self.suffix_entry.insert("end", self.configurations.get("default_suffix"))

        self.buttons_frame = Frame(self.right_frame)
        self.buttons_frame.pack()

        self.add_button = Button(self.buttons_frame, text="Add", width=15)
        self.add_button.pack(pady=4)

        self.edit_button = Button(self.buttons_frame, text="Edit", width=15)
        self.edit_button.pack(pady=4)

        self.remove_button = Button(self.buttons_frame, text="Remove", width=15)
        self.remove_button.pack(pady=4)

        self.save_button = Button(self.buttons_frame, text="Save", width=15)
        self.save_button.pack(pady=4)



        # Mainloop
        self.mainloop()
