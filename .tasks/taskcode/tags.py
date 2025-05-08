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

import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
from doot.workflow import TaskName
from jgdv.files.tags import TagFile, SubstitutionFile
from bibble.metadata import TagsReader
from dootle.actions.postbox import _DootPostBox

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

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


