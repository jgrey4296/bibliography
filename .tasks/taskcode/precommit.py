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
from doot.structs import DootKey

HEAD_TAG_RE = re.compile(r"^\[\w+\]")

@DootKey.kwrap.types("files")
def cli_retriever(spec, state, files):
    root = doot.locs["."]
    printer.info("Testing: %s", files)
    for x in files:
        fpath = doot.locs[x]
        if fpath.suffix != ".bib":
            continue
        printer.info("success: %s", fpath)
        lpath = fpath.relative_to(root)
        yield dict(name=fpath.stem,
                   fpath=fpath,
                   fstem=fpath.stem,
                   fname=fpath.name,
                   lpath=lpath,
                   pstem=fpath.parent.stem)

@DootKey.kwrap.expands("text")
def validate(spec, state, text):
    head = text.split("\n")[0]
    if not HEAD_TAG_RE.match(head):
        printer.warning("Commit Messages need to have a [tag] at the start")
        return False
