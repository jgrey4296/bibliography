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
##-- end logging

import doot
import doot.errors
from doot.structs import DootKey
from doot.enums import ActionResponseEnum
from dootle.tags.structs import TagFile
from dootle.bookmarks.structs import BookmarkCollection

TODAY                       = datetime.datetime.now().date()

@DootKey.kwrap.types("from", hint={"type_":BookmarkCollection})
@DootKey.kwrap.redirects("update_")
def collect_tags(spec, state, _db, _update):
    """ merge tags of bookmarks together """
    tags           = TagFile()

    for bkmk in _db:
        tags.update(bkmk.tags)

    return { _update : str(tags) }

@DootKey.kwrap.paths("bookmarks")
def recency_test(spec, state, bookmarks):
    """ trigger task skip if the bookmarks file was modified today """
    mod_date = datetime.datetime.fromtimestamp(bookmarks.stat().st_mtime).date()
    if TODAY <= mod_date:
        return ActionResponseEnum.SKIP
