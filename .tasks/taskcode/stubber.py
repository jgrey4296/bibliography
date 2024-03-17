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

FPATH    = DootKey.build("fpath")
UPDATE   = DootKey.build("update_")
FROM_KEY = DootKey.build("from")
TO_KEY   = DootKey.build("to")

def gen_stub(spec, state):
    update = UPDATE.redirect(spec)
    fpath  = TO_KEY.to_path(spec, state)
    fstem  = fpath.stem
    year   = datetime.datetime.now().year

    stub   = []
    stub.append("@misc{,")
    stub.append(f"  title = {{{fstem}}},")
    stub.append(f"  year = {{{year}}},")
    stub.append(f"  file = {{{fpath}}},")
    stub.append("}")
    return { update : "\n".join(stub) }

def join_stubs(spec, state):
    match FROM_KEY.to_type(spec, state, type_=list|None):
        case None:
            stubs = []
        case _ as x:
            stubs = x
    update = UPDATE.redirect(spec)
    return { update : "\n\n".join(stubs) }

def select_refiled(target:pl.Path):
    return target.stem.startswith("_refiled_") and not target.is_dir()

def not_copied(target:pl.Path):
    printer.info("Testing: %s", target)
    return target.is_file() and not target.name.startswith("_copied_")
