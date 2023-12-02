"""This file contains specific constant variables used in other files to avoid circular imports."""

# Covers special characters which have specific text representations
REPRESENTATION_TO_SPECIAL = [
    ["{{}", "{"],
    ["{}}", "}"],
    ["{+}", "+"],
    ["{!}", "!"],
    ["{#}", "#"],
    ["{^}", "^"]
]

SPECIAL_TO_REPRESENTATION = {
    "{": "{{}",
    "}": "{}}",
    "+": "{+}",
    "!": "{!}",
    "#": "{#}",
    "^": "{^}"
}
