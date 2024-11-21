#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""

##-- builtin imports
from __future__ import annotations

# import abc
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
# from copy import deepcopy
# from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable, Generator)
from uuid import UUID, uuid1

##-- end builtin imports

##-- lib imports
import more_itertools as mitz
##-- end lib imports

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

import doot
import doot.errors
from doot.structs import DKey, DKeyed, TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bib_middleware.metadata import TagsReader
from doot.actions.postbox import _DootPostBox

@DKeyed.paths("from")
@DKeyed.redirects("update_")
def read_tags(spec, state, _from, _update):
    tags = TagFile.read(_from)
    return { _update : tags }

@DKeyed.types("from", check=TagFile)
@DKeyed.redirects("update_")
def write_tag_set(spec, state, _from, _update):
    tag_str = str(_from)
    return { _update : tag_str}

@DKeyed.types("from", check=list|set)
@DKeyed.redirects("update_")
def merge_tagfiles(spec, state, _tagfiles, _update):
    merged = TagFile()
    for tf in _tagfiles:
        assert(isinstance(tf, TagFile))
        merged += tf

    return { _update : merged }


class TagCalculator:
    """
      Given a raw set of tags, a collection of subfiles,
      and a tag file of total tags,
      calculate updates
    """

    @DKeyed.types("raw", check=set)
    @DKeyed.types("totals", check=TagFile)
    def __call__(self, spec, state, raw, totals):
        new_tags  = self._calc_new_tags(totals, raw)

        return { "new_tags" : new_tags }

    def _calc_new_tags(self, _total:TagFile, _raw:set[str]):
        _raw             = _raw or set()
        total_set : set = _total.to_set()
        new_tags        = TagFile(counts={x:1 for x in (_raw - total_set)})
        return new_tags
