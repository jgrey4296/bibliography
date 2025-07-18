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

import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
import bibble as BM

@DKeyed.types("from", check=BTP.Library)
@DKeyed.redirects("update_")
def get_files(spec, state, _lib, _update):
    files = []
    for entry in _lib.entries:
        files += [x.value for x in entry.fields if "file" in x.key]

    return { _update : files }
