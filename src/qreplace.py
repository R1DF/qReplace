# Imports
from tkinter import Tk, Frame, Label, Button
from config_reader import ConfigReader
from replacer_listbox import ReplacerListbox

# QReplace class
class QReplace(Tk):
    def __init__(self, version: str, configurations: ConfigReader):
        # Window creation
        super().__init__()
        self.configurations = configurations
        self.title(f"qReplace v{version}")
        self.geometry(f"{self.configurations.get('resolution')[0]}x{self.configurations.get('resolution')[1]}")

        # Laying out widgets
        self.introduction_label = Label(self, text="qReplace")
        self.introduction_label.pack()

        self.main_frames_frame = Frame(self)
        self.main_frames_frame.pack()

        self.left_frame = Frame(self.main_frames_frame)
        self.left_frame.grid(row=0, column=0, padx=15)

        self.right_frame = Frame(self.main_frames_frame)
        self.right_frame.grid(row=0, column=1, padx=15)

        self.replacer_listbox = ReplacerListbox(self.left_frame, width=35)
        self.replacer_listbox.pack()

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
