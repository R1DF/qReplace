# Imports
import os
import toml

# Constants
CONFIGURATIONS_PATH = os.path.join(os.getcwd(), "config.toml")


# Write new configurations function
def overwrite_configurations(data: dict):
    with open(CONFIGURATIONS_PATH, "w") as file:
        toml.dump(data, file)
