# Imports
from tkinter import Tk
from config_reader import ConfigReader

# QReplace class
class QReplace(Tk):
    def __init__(self, version: str, configurations: ConfigReader):
        super().__init__()
        self.configurations = configurations
        self.title(f"qReplace v{version}")
        self.geometry(f"{self.configurations.get('resolution')[0]}x{self.configurations.get('resolution')[1]}")
        self.mainloop()
