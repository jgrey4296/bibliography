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

from random import choice, choices

import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.structs import DKey, DKeyed
import bib_middleware as BM

##-- logging
logging = logmod.getLogger(__name__)
printer = doot.subprinter("action_exec")
##-- end logging

@DKeyed.types("entry")
def log_entry_name(spec, state, entry):
    match entry.fields_dict.get("title", None):
        case None:
            printer.info("> %s", entry.key)
        case x:
            printer.info("> %s", x.value)

@DKeyed.types("entry")
@DKeyed.redirects("update_")
def get_entry_file(spec, state, entry, _update):
    match entry.fields_dict.get("file", None):
        case None:
            return
        case x:
            return { _update : x.value }
