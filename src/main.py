# Imports
from config_reader import ConfigReader
from qreplace import QReplace

# Constants
VERSION = "0.0.0"
SAFE = True  # Set to false to disable error handler


# Run function
def run():
    configurations = ConfigReader()
    QReplace(VERSION, configurations)


# Running program
if __name__ == "__main__":
    # Safe run
    if SAFE:
        try:
            run()
        except Exception as exception:
            pass
    else:
        run()
