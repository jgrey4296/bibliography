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
import doot.utils.expansion as exp
from dootle.tags.structs import TagFile
from dootle.bookmarks.structs import BookmarkCollection

UPDATE   : Final[exp.DootKey] = exp.DootKey("update_")
FROM_KEY : Final[exp.DootKey] = exp.DootKey("from_")

def collect_tags(spec, state):
    update_key     = UPDATE.redirect(spec)
    bkmk_coll      = FROM_KEY.to_type(spec, state, type_=BookmarkCollection)
    tags           = TagFile()

    for bkmk in bkmk_coll:
        tags.update(bkmk.tags)

    return { update_key : str(tags) }
