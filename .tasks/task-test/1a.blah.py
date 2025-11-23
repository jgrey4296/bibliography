#!/usr/bin/env -S uv run --script

import sys
import task_utils

import argparse
parser = argparse.ArgumentParser(
    prog="biblio bookmarks",
    description="Extract firefox bookmarks and add to repo",
)

# args = parser.parse_args()

print(
"""----------
Python Script hook
----------"""
)

print(f"""
Args: {sys.argv}
Base Exec: {sys.executable}
""")

