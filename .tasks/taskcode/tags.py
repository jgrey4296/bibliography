#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""
# ruff: noqa:
# Imports
from __future__ import annotations

import logging as logmod
import pathlib as pl

from jgdv.structs.dkey import DKeyed
import doot
import doot.errors
from doot.workflow import ActionSpec
from doot.util.dkey import DKey
from doot.workflow import TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bibble.metadata import TagsReader
from dootle.actions.postbox import _DootPostBox

logging = logmod.getLogger(__name__)

@DKeyed.paths("from")
@DKeyed.redirects("update_")
def read_tags(spec:ActionSpec, state:dict, _from:pl.Path, _update:DKey) -> dict:
    tags = TagFile.read(_from)
    return { _update : tags }

@DKeyed.types("from", check=TagFile)
@DKeyed.redirects("update_")
def write_tag_set(spec:ActionSpec, state:dict, _from:pl.Path, _update:DKey) -> dict:
    tag_str = str(_from)
    return { _update : tag_str}

@DKeyed.types("from", check=list|set)
@DKeyed.redirects("update_")
def merge_tagfiles(spec:ActionSpec, state:dict, _tagfiles:pl.Path, _update:DKey) -> dict:
    merged = TagFile()
    for tf in _tagfiles:
        assert(isinstance(tf, TagFile))
        merged += tf

    return { _update : merged }
