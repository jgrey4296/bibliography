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
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable, Generator)
from uuid import UUID, uuid1

##-- end builtin imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
from doot.workflow._interface import ActionResponse_e
from jgdv.files.tags import TagFile
from jgdv.files.bookmarks import BookmarkCollection

def today() -> datetime.datetime:
    return datetime.datetime.now().date()

@DKeyed.types("from", check=BookmarkCollection)
@DKeyed.redirects("update_")
def collect_tags(spec, state, _db, _update):
    """ merge tags of bookmarks together """
    tags           = TagFile()

    for bkmk in _db:
        tags.update(bkmk.tags)

    return { _update : str(tags) }
