"""
This module translates .py files to .ipynb and vice versa
"""
from typing import Optional
import os
import sys
import json

from p2j.utils import _check_files

# Path to directory
HERE = os.path.abspath(os.path.dirname(__file__))

TRIPLE_QUOTES = ['"""', "'''"]
FOUR_SPACES = "{:<4}".format("")
EIGHT_SPACES = "{:<8}".format("")
TWELVE_SPACES = "{:<12}".format("")


# Read JSON files for .ipynb template
with open(HERE + "/templates/cell_code.json", encoding="utf-8") as file:
    CODE = json.load(file)
with open(HERE + "/templates/cell_markdown.json", encoding="utf-8") as file:
    MARKDOWN = json.load(file)
with open(HERE + "/templates/metadata.json", encoding="utf-8") as file:
    MISC = json.load(file)


def append_to_json(was_code, arr, cells):
    # Check if the last element of the block is a newline
    if arr[-1] in ("\n", "<br>\n"):
        arr = arr[:-1]

    # Check if the last block was code or markdown and appends to final array
    if was_code:
        CODE["source"] = arr
        cells.append(dict(CODE))
    else:
        MARKDOWN["source"] = arr
        cells.append(dict(MARKDOWN))
    return cells


def python2jupyter(source_filename: str, target_filename: str, overwrite: bool = False):
    """Convert Python scripts to Jupyter notebooks.

    Args:
        source_filename (str): Path to Python script.
        target_filename (str): Path to name of Jupyter notebook. Optional.
        overwrite (bool): Whether to overwrite an existing Jupyter notebook.
    """

    target_filename = _check_files(
        source_filename, target_filename, overwrite, conversion="p2j"
    )

    # Check if source file exists and read
    try:
        with open(source_filename, "r", encoding="utf-8") as infile:
            data = [line.rstrip() for line in infile]
    except FileNotFoundError:
        print("Source file not found. Specify a valid source file.")
        sys.exit(1)

    # Initialise variables
    final = {}  # the dictionary/json of the final notebook
    cells = []  # an array of all markdown and code cells
    arr = []  # an array to store individual lines for a cell
    is_code = True  # We assume the first cell is code

    # Read source code line by line
    for i, line in enumerate(data):
        # Use delimiters to separate cells
        if line.startswith("##"):
            marker = line[3:] if line[2].isspace() else line[2:]

            if marker.startswith("m"):
                if i != 0:
                    cells = append_to_json(is_code, arr, cells)
                    arr = []
                is_code = False
                continue

            elif marker.startswith("c"):
                if i != 0:
                    cells = append_to_json(is_code, arr, cells)
                    arr = []
                is_code = True
                continue

            else:
                raise ValueError(
                    f""" Cell markers start with either [## m] for markdown cells or [## c] for code cells.
                        Found cell marker {line}. """
                )

        if is_code:
            arr.append(f"{line}\n")
            continue
        else:
            if line.startswith("#"):
                if len(line) > 2:
                    buffer = line[2:] if line[1].isspace() else line[1:]
                else:
                    buffer = ""
            else:
                if line in TRIPLE_QUOTES:
                    continue
                buffer = line.replace(TRIPLE_QUOTES[0], "").replace(
                    TRIPLE_QUOTES[1], ""
                )
                if len(buffer) > 1:
                    buffer = buffer[1:] if buffer[0].isspace() else buffer
            arr.append(f"{buffer + '<br>'}\n")
            continue

    # Take care of the last cell
    cells = append_to_json(is_code, arr, cells)
    # Finalise the contents of notebook
    final["cells"] = cells
    final.update(MISC)

    # Write JSON to target file
    with open(target_filename, "w", encoding="utf-8") as outfile:
        json.dump(final, outfile, indent=1, ensure_ascii=False)
        print("Notebook {} written.".format(target_filename))
