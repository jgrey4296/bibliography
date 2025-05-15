#!/usr/bin/env python3
"""

"""

from __future__ import annotations

##-- stdlib
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

##-- end stdlib

import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
from doot.workflow import TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bibble.metadata import TagsReader
from dootle.actions.postbox import _DootPostBox

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@DKeyed.paths("from", fallback=None)
@DKeyed.types("from_all", fallback=[], named="_target_list")
@DKeyed.formats("sub_norm_replace", fallback="_")
@DKeyed.formats("sub_sep", fallback=" : ")
@DKeyed.redirects("update_")
def read_subs(spec, state, _target, _target_list, _norm_replace, _sep, _update):
    match _target:
        case pl.Path() if _target.exists():
            target_subs = SubstitutionFile.read(_target, norm_replace=_norm_replace, sep=_sep)
        case _:
            target_subs = SubstitutionFile(norm_replace=_norm_replace, sep=_sep)

    for key in _target_list:
        key     = DKey(key, mark=DKey.Mark.PATH)
        match key():
            case pl.Path() as x if x.exists():
                subfile = SubstitutionFile.read(x, norm_replace=_norm_replace, sep=_sep)
            case x:
                doot.report.fail("Unsuitable key expansion for reading sub file: %s", x)

        target_subs.update(subfile)
    else:
        return { _update : target_subs }

@DKeyed.args
def aggregate_subs(spec, state, args):
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
