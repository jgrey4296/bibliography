#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""
# ruff: noqa: TC003, TC002, ARG001
# import
from __future__ import annotations

import logging as logmod
import pathlib as pl
import datetime
import re
import doot
import doot.errors
from doot.workflow import ActionSpec
from doot.util.dkey import DKey, DKeyed

# logging
logging = logmod.getLogger(__name__)

@DKeyed.paths("to")
@DKeyed.redirects("update_")
def gen_stub(spec:ActionSpec, state:dict, _fpath:pl.Path, _update:DKey) -> dict:
    fstem  = _fpath.stem
    year   = datetime.datetime.now().year # noqa: DTZ005

    stub   = []
    stub.append("@misc{,")
    stub.append(f"  title = {{{fstem}}},")
    stub.append(f"  year = {{{year}}},")
    stub.append(f"  file = {{{_fpath}}},")
    stub.append("}")
    return { _update : "\n".join(stub) }

@DKeyed.types("from", check=list|None)
@DKeyed.redirects("update_")
def join_stubs(spec:ActionSpec, state:dict, _from:pl.Path, _update:DKey) -> dict:
    match _from:
        case None:
            stubs = []
        case _ as x if hasattr(x, "__iter__"):
            stubs = x
    return { _update : "\n\n".join(stubs) }

def select_refiled(target:pl.Path) -> bool:
    logging.debug("Testing: %s", target)
    return target.stem.startswith("_refiled_") and not target.is_dir()

def not_copied(target:pl.Path) -> bool:
    logging.debug("Testing: %s", target)
    return target.is_file() and not target.name.startswith("_copied_")
