#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
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
