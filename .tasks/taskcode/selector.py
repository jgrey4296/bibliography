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

printer = logmod.getLogger("doot._printer")

import doot
import doot.errors
from doot.structs import DootKey

def sort_oldest(spec:list, state, sub_specs) -> list:
    # Sorts oldest -> newest
    by_mod_time = sorted(sub_specs, key=lambda x: x.extra.fpath.stat().st_mtime)
    return by_mod_time[0:spec.kwargs.count]

@DootKey.kwrap.types("from", hint={"type":BTP.Library})
@DootKey.kwrap.redirects("update_")
def select_one_entry(spec, state, _bib_db, _update):
    entries    = bib_db.entries
    entry      = choice(entries)
    # TODO have white/black list

    if bool(entry):
        return { _update : entry }
