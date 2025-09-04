#!/usr/bin/env python3
"""

   commit-msg
       This hook is invoked by git-commit(1) and git-merge(1), and can be
       bypassed with the --no-verify option. It takes a single parameter, the
       name of the file that holds the proposed commit log message. Exiting
       with a non-zero status causes the command to abort.

       The hook is allowed to edit the message file in place, and can be used
       to normalize the message into some project standard format. It can also
       be used to refuse the commit after inspecting the message file.

       The default commit-msg hook, when enabled, detects duplicate
       Signed-off-by trailers, and aborts the commit if one is found.

"""
# ruff: noqa: F401
# Imports
from __future__ import annotations
import sys
import logging as logmod
import pathlib as pl
import re

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

HEAD_TAG_RE = re.compile(r"^\[\w+\]")

def validate(spec, state, text):
    head = text.split("\n")[0]
    if not HEAD_TAG_RE.match(head):
        printer.warning("Commit Messages need to have a [tag] at the start")
        return False

def print_changed(spec, state, changed):
    printer.info("Changed Files:")
    for x in changed:
        printer.info("-- %s", x)

def main():
    match sys.argv:
        case [_, str() as commit_file]:
            pass
        case x:
            raise TypeError(type(x))

    # read the commit file
    # validate it

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
