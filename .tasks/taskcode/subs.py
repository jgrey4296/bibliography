#!/usr/bin/env python3
"""

"""
# ruff: noqa: TC002, ARG001
from __future__ import annotations

import logging as logmod
import pathlib as pl
import doot
import doot.errors
from jgdv.structs.dkey import DKeyed
from doot.workflow import ActionSpec
from doot.util.dkey import DKey
from doot.workflow import TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bibble.metadata import TagsReader
from dootle.actions.postbox import _DootPostBox

# logging
logging = logmod.getLogger(__name__)

@DKeyed.paths("from", fallback=None)
@DKeyed.types("from_all", fallback=[], named="_target_list")
@DKeyed.formats("sub_norm_replace", fallback="_")
@DKeyed.formats("sub_sep", fallback=" : ")
@DKeyed.redirects("update_")
def read_subs(spec:ActionSpec, state:dict, _target:pl.Path, _target_list:list, _norm_replace:str, _sep:str, _update:DKey) -> dict:
    key          : DKey
    target_subs  : SubstitutionFile
    subfile      : SubstitutionFile

    match _target:
        case pl.Path() if _target.exists():
            target_subs = SubstitutionFile.read(_target, norm_replace=_norm_replace, sep=_sep)
        case _:
            target_subs = SubstitutionFile(norm_replace=_norm_replace, sep=_sep)

    for val in _target_list:
        key     = DKey(val, mark=DKey.Mark.PATH)
        match key():
            case pl.Path() as x if x.exists():
                subfile = SubstitutionFile.read(x, norm_replace=_norm_replace, sep=_sep)
            case x:
                doot.report.fail("Unsuitable key expansion for reading sub file: %s", x)

        target_subs.update(subfile)
    else:
        return { _update : target_subs }

@DKeyed.args
def aggregate_subs(spec:ActionSpec, state:dict, args:list) -> dict:
    """ merge keys from args together,
      handling tagfiles, and lists of tag files
    """
    merged = SubstitutionFile()
    for x in args:
        key = DKey(x, mark=DKey.Mark.FREE, implicit=True)
        match key.expand(spec, state):
            case None:
                pass
            case TagFile() as tf:
                merged += tf
            case list() as lst:
                for tf in lst:
                    merged += tf
            case x:
                doot.report.fail("Unknown value attempted to be aggregated: %s", type(x))

    else:
        canon_tags = merged.canonical()
        known_tags = merged.known()
        return { "known_tags": known_tags, "canon_tags": canon_tags, "total_subs": merged }
