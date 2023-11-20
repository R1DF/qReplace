# Imports
import toml
import os
from typing import Any

# Constants
CONFIGURATIONS_PATH = os.path.join(os.getcwd(), "config.toml")


# Configuration reader class
class ConfigReader:
    def __init__(self):
        self.configurations = toml.load(CONFIGURATIONS_PATH)

    def get(self, key: str) -> Any:
        return self.configurations[key]
