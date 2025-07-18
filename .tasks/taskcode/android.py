#!/usr/bin/env python3
"""

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

from jgdv.enums import LoopControl_e

def select_dirs(target) -> bool | LoopControl_e:
    if target.stem == "pdfs":
        return LoopControl_e.noBut
    if target.is_dir():
        return LoopControl_e.yesAnd
    return False
