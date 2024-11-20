#!/usr/bin/env python3
"""



"""

from __future__ import annotations

import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import weakref
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generator,
                    Generic, Iterable, Iterator, Mapping, Match,
                    MutableMapping, Protocol, Sequence, Tuple, TypeAlias,
                    TypeGuard, TypeVar, cast, final, overload,
                    runtime_checkable)
from uuid import UUID, uuid1

import doot
import doot.errors
from doot.structs import DKey, DKeyed, TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bib_middleware.metadata import TagsReader
from doot.actions.postbox import _DootPostBox

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


@DKeyed.paths("from", fallback=None)
@DKeyed.types("from_all", fallback=[])
@DKeyed.formats("sub_norm_replace", fallback="_")
@DKeyed.formats("sub_sep", fallback=" : ")
@DKeyed.redirects("update_")
def read_subs(spec, state, _target, _target_list, _norm_replace, _sep, _update):
    match _target:
        case pl.Path() if _target.exists():
            target_subs = SubstitutionFile.read(_target, norm_replace=_norm_replace, sep=_sep)
        case _:
            target_subs = SubstitutionFile(norm_replace=_norm_replace, sep=_sep)

    for key in [DKey(x, mark=DKey.mark.PATH) for x in _target_list]:
        subfile = SubstitutionFile.read(key(), norm_replace=_norm_replace, sep=_sep)
        target_subs.update(subfile)

    return { _update : target_subs }

@DKeyed.args
def aggregate_subs(spec, state, args):
    """ merge keys from args together,
      handling tagfiles, and lists of tag files
    """
    keys = [DKey(x, mark=DKey.mark.FREE, implicit=True) for x in args]
    merged = SubstitutionFile()
    for key in keys:
        match key.expand(spec, state):
            case TagFile() as tf:
                merged += tf
            case list() as lst:
                for tf in lst:
                    merged += tf

    canon_tags = merged.canonical()
    known_tags = merged.known()
    return { "known": known_tags, "canon": canon_tags, "subs": merged }
