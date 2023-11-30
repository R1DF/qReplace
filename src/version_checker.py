# Imports
import requests

# Constants
VERSION_URL = "https://r1df.github.io/version_check.json"


# Version checker function
def get_latest_version_data() -> dict:
    version_data = requests.get(VERSION_URL).json()["qr"]
    return {"version": version_data["v"], "note": version_data["note"]}
