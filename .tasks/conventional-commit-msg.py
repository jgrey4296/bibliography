# basic.local.py -*- mode: python -*-
"""
Ensure the first line of a commit msg matches:
https://www.conventionalcommits.org/en/v1.0.0/
"""

import sys
import re
import pathlib as pl

commit_head = re.compile(r"^(fixup! )?\[\w+\]:")

match sys.argv:
    case [_, str() as fname]:
        contents = pl.Path(fname).read_text().split("\n")
        if commit_head.match(contents[0]):
            sys.exit(0)
        else:
            print(f"Commit msg head invalid: ^{contents[0]}$")
            print("Use conventional commits: https://www.conventionalcommits.org/en/v1.0.0/#summary")
            sys.exit(1)
    case _:
        sys.exit(1)
