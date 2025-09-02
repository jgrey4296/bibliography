#!/usr/bin/env python3
"""
   pre-commit
       This hook is invoked by git-commit(1), and can be bypassed with the
       --no-verify option. It takes no parameters, and is invoked before
       obtaining the proposed commit log message and making a commit. Exiting
       with a non-zero status from this script causes the git commit command
       to abort before creating a commit.

       The default pre-commit hook, when enabled, catches introduction of
       lines with trailing whitespaces and aborts the commit when such a line
       is found.

       All the git commit hooks are invoked with the environment variable
       GIT_EDITOR=: if the command will not bring up an editor to modify the
       commit message.

       The default pre-commit hook, when enabled—and with the
       hooks.allownonascii config option unset or set to false—prevents the
       use of non-ASCII filenames.
"""
# ruff: noqa: F401
# Imports
from __future__ import annotations

import logging as logmod
import pathlib as pl
import re

import doot
import doot.errors
import doot.util.dkey
from jgdv.structs.dkey import DKeyed

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

HEAD_TAG_RE = re.compile(r"^\[\w+\]")

@DKeyed.formats("text")
def validate(spec, state, text):
    head = text.split("\n")[0]
    if not HEAD_TAG_RE.match(head):
        printer.warning("Commit Messages need to have a [tag] at the start")
        return False

@DKeyed.types("changed")
def print_changed(spec, state, changed):
    printer.info("Changed Files:")
    for x in changed:
        printer.info("-- %s", x)

def main():
    pass

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
