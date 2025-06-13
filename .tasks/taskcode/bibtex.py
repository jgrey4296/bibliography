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

from random import choice, choices

import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
import bibble as BM

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@DKeyed.types("entry")
def log_entry_name(spec, state, entry):
    match entry.fields_dict.get("title", None):
        case None:
            value = entry.key
        case x:
            value = x.value

    doot.report.act("> %s", value)

@DKeyed.types("entry")
@DKeyed.redirects("update_")
def get_entry_file(spec, state, entry, _update):
    match entry.fields_dict.get("file", None):
        case None:
            return
        case x:
            return { _update : x.value }

@DKeyed.types("bib_db")
@DKeyed.formats("key")
@DKeyed.redirects("update_")
def get_kv_from_library(spec, state, _db, key, _update):
    """ Get the TagFile of tags read from the current lib, and insert it into state """
    value = _db.get_meta_value(key)
    return { _update : value }
