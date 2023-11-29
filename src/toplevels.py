# Imports
from tkinter import Tk, Toplevel, Frame, Entry, Label, Button, Listbox, Scrollbar, PhotoImage, messagebox
from config_writer import overwrite_configurations
from configuration_listbox import ConfigurationListbox
import os
import webbrowser


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


# Open Recent toplevel
# About toplevel
class OpenRecentToplevel(BaseToplevel):
    def __init__(self, master):
        super().__init__(master, "open_recent")
        # Initialisation
        self.title("Open recent")
        self.geometry("520x170")
        self.resizable(False, False)

        # Widget creation
        self.introduction_label = Label(self, text="Double click a recent file to open from the list:")
        self.introduction_label.pack()

        self.recent_files_frame = Frame(self)
        self.recent_files_frame.pack()

        self.recent_files_listbox = Listbox(self.recent_files_frame, width=60, height=8)
        self.recent_files_listbox.pack(side="left")

        self.recent_files_scrollbar = Scrollbar(self.recent_files_frame)
        self.recent_files_scrollbar.pack(side="right", fill="both")

        self.recent_files_listbox.config(yscrollcommand=self.recent_files_scrollbar.set)
        self.recent_files_scrollbar.config(command=self.recent_files_listbox.yview)

        # Setting up listbox
        for file in self.master.recent_files:
            self.recent_files_listbox.insert(0, file)
        self.recent_files_listbox.bind("<Double-1>", self.handle_double_click)

    def handle_double_click(self, event=None):
        file_path = self.recent_files_listbox.get(self.recent_files_listbox.curselection()[0])
        self.master.handle_open(file_path)
        self.handle_close()


# Preferences toplevel
class PreferencesToplevel(BaseToplevel):
    def __init__(self, master, configurations: dict):
        super().__init__(master, "preferences")
        # Initialisation
        self.title("Preferences")
        self.geometry("450x220")
        self.resizable(False, False)
        self.starter_data = configurations.copy()
        self.current_data = configurations.copy()
        self.active_setting = None

        # Widget creation
        self.introduction_label = Label(self, text="Preferences")
        self.introduction_label.pack()

        self.main_frame = Frame(self)
        self.main_frame.pack()

        self.configurations_outer_frame = Frame(self.main_frame)
        self.configurations_outer_frame.pack(side="left")

        self.configuration_listbox = ConfigurationListbox(self.configurations_outer_frame,
                                                          controlling_window=self, callback=self.switch_setting)

        self.user_input_frame = Frame(self.main_frame, width=50)
        self.user_input_frame.pack(side="right")

        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()

        self.cancel_button = Button(self.buttons_frame, text="Cancel", command=lambda: self.handle_close(False), width=15)
        self.cancel_button.grid(row=0, column=0, padx=20)

        self.save_button = Button(self.buttons_frame, text="Save", command=self.handle_save, width=15)
        self.save_button.grid(row=0, column=1, padx=20)

        # Adding settings
        self.configuration_listbox.add_setting("resolution", "Resolution")
        self.configuration_listbox.add_setting("defaults", "Defaults")
        self.switch_setting("resolution")

    def switch_setting(self, name: str):
        # Killing all children (don't take out of context)
        for widget in self.user_input_frame.winfo_children():
            widget.destroy()

        # Creating new children depending on active setting
        match name:
            case "resolution":
                self.active_setting = "resolution"

                self.resolution_label = Label(self.user_input_frame, text="Resolution:")
                self.resolution_label.grid(row=0, column=0)

                self.resolution_entry = Entry(self.user_input_frame)
                self.resolution_entry.grid(row=0, column=1)
                self.resolution_entry.insert("end", self.format_resolution(self.current_data["resolution"]))

            case "defaults":
                self.active_setting = "defaults"

                self.default_prefix_label = Label(self.user_input_frame, text="Default prefix:")
                self.default_prefix_label.grid(row=0, column=0)

                self.default_prefix_entry = Entry(self.user_input_frame)
                self.default_prefix_entry.grid(row=0, column=1)
                self.default_prefix_entry.insert("end", self.current_data["default_prefix"])

                self.default_suffix_label = Label(self.user_input_frame, text="Default suffix:")
                self.default_suffix_label.grid(row=1, column=0)

                self.default_suffix_entry = Entry(self.user_input_frame)
                self.default_suffix_entry.grid(row=1, column=1)
                self.default_suffix_entry.insert("end", self.current_data["default_suffix"])

            case _:
                pass

    def handle_save(self):
        # Saving specific input depending on active setting
        match self.active_setting:
            case "resolution":
                resolution_data = self.resolution_entry.get().strip().split("x")
                if len(resolution_data) != 2:
                    messagebox.showerror("Error", "Please enter a valid resolution.")
                    return

                try:
                    width, height = [int(x) for x in resolution_data]

                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid resolution.")
                    return

                self.current_data["resolution"] = [width, height]

            case "defaults":
                default_prefix = self.default_prefix_entry.get().strip()
                default_suffix = self.default_suffix_entry.get().strip()

                if not default_prefix:
                    messagebox.showerror("Error", "You must provide a default prefix.")
                    return

                self.current_data["default_prefix"] = default_prefix
                self.current_data["default_suffix"] = default_suffix

    def handle_close(self, overwrite=True):
        # Checking whether there should be a check to overwrite data
        if overwrite:
            # Checking for changes and overwriting if there are any
            if self.current_data != self.starter_data:
                overwrite_configurations(self.current_data)
                self.master.trigger_restart()

    def format_resolution(self, resolution: list[int]):
        return f"{resolution[0]}x{resolution[1]}"



# About toplevel
class AboutToplevel(BaseToplevel):
    def __init__(self, master):
        super().__init__(master, "about")
        # Initialisation
        self.title("About qReplace")
        self.geometry("410x130")
        self.resizable(False, False)
        url_to_open = "https://github.com/R1DF/qReplace"

        # Getting icon photo
        self.icon_photoimage = PhotoImage(file=os.path.join(os.getcwd(), "assets", "icon_32x32.png"))

        # Widget creation
        self.icon_label = Label(self, image=self.icon_photoimage)
        self.icon_label.pack()

        self.description_label = Label(
            self,
            text=f"qReplace v{self.master.version}\n"
                 "A simple program that makes making AutoHotkey files that map\n"
                 "character combinations easier for you.\n"
                 "Created by R1DF."
        )
        self.description_label.pack()

        self.open_repository_button = Button(self,
                                             text="Open GitHub repository",
                                             command=lambda: webbrowser.open_new_tab(url_to_open))
        self.open_repository_button.pack()
