#!/usr/bin/env -S uv run --script

import sys
import task_utils

print(
"""----------
Python Script hook
----------"""
)

print(f"""
Args: {sys.argv}
Base Exec: {sys.executable}
""")

