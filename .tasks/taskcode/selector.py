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


import bibtexparser as BTP
import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
from doot.workflow._interface import ActionResponse_e as ActE

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

@DKeyed.types("count")
def sort_oldest(spec:ActionSpec, state:dict, sub_specs:list[pl.Path|TaskSpec], count:int|str) -> list:
    count = int(count)
    # Sorts oldest -> newest
    by_mod_time = sorted(sub_specs, key=lambda x: x.stat().st_mtime)
    return by_mod_time[:count]

@DKeyed.types("from", check=BTP.Library)
@DKeyed.redirects("update_")
def select_one_entry(spec, state, _bib_db, _update):
    entries    = bib_db.entries
    entry      = choice(entries)
    # TODO have white/black list

    if bool(entry):
        return { _update : entry }

@DKeyed.types("entry")
def skip_if_no_file_in_entry(spec, state, entry):
    if "file" not in entry.fields_dict:
        return ActE.SKIP
