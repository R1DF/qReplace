# Imports
from replacer import Replacer
import re


# Infers prefix and suffix from a header line.
def infer_from_header(line: str) -> list[str]:
    return line.split(" ")[-1][1:-1].split("|")


# Saving list of Replace objects to .ahk file
def save_list_as_ahk(filename: str, prefix: str, suffix: str, version: str, replacers: list[Replacer]):
    # Getting all replacer representations in AutoHotKey code
    lines = []
    for replacer in replacers:
        lines.append(replacer.get_ahk_code(prefix, suffix))

    # Saving each line to a .ahk file
    with open(f"{filename}.ahk", "w") as file:
        file.write(
            f"; (DO NOT INSERT ANY LINES ABOVE THIS ONE)\n"
            f"; DO NOT REMOVE OR EDIT THIS LINE: QREPLACE V{version} [{prefix}|{suffix}]\n\n"
        )
        for line in lines:
            file.write(f"{line}\n")


# Opening .ahk file as a list of Replace objects
def open_ahk_as_dict(path: str) -> dict:
    replacers = []
    with open(path, "r") as file:
        # Getting non-empty lines and inferring prefix and suffix from header
        lines = [x for x in file.read().splitlines() if x]
        prefix, suffix = infer_from_header(lines[1])

        # Searching for AutoHotKey text replacement lines
        for line in lines[2:]:  # Header lines undeeded
            if re.match(r"^:[*?c]+:([^:]+)::([^:]+)$", line) is not None:

                # Getting phrase and replacement, with account to prefix and suffix
                line_parts = line.split(":")
                phrase = line_parts[2][len(prefix):]
                if suffix:  # If there's a suffix, an extra slice is necessary
                    phrase = phrase[:-1 * len(suffix)]

                replacement = line_parts[-1]
                replacers.append([phrase, replacement])

    return {"prefix": prefix, "suffix": suffix, "replacers": replacers}
