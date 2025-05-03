#!/usr/bin/env python3
"""

"""
# ruff: noqa:

# Imports:
from __future__ import annotations

# ##-- stdlib imports
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import collections
import contextlib
import hashlib
from copy import deepcopy
from uuid import UUID, uuid1
from weakref import ref
import atexit # for @atexit.register
import faulthandler
# ##-- end stdlib imports

import doot
from jgdv.structs.dkey import DKeyed

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType, Never
# Protocols:
from typing import Protocol, runtime_checkable
# Typing Decorators:
from typing import no_type_check, final, override, overload
# from dataclasses import InitVar, dataclass, field
# from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError

if TYPE_CHECKING:
    from jgdv import Maybe
    from typing import Final
    from typing import ClassVar, Any, LiteralString
    from typing import Self, Literal
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

##--|

# isort: on
# ##-- end types

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

# Vars:
DATE_FORMAT : Final[str] = "%Y-%m-%d"
# Body:

@DKeyed.types("rpath")
@DKeyed.types("lib")
@DKeyed.redirects("update_")
def fmt_lib_size(spec, state, _path, lib, _update):
    """ Get the size of the library,
    returns both the size, and a formatted str of it
    """
    today     = datetime.datetime.today().strftime(DATE_FORMAT)
    count     = len(lib.entries)
    f_str     = str(_path)
    formatted = f"{f_str} : {today} : {count}"
    doot.report.act(info="Lib Size", msg=formatted, level=10)
    return { _update : formatted, "lib.size" : count }

@DKeyed.types("rpath")
@DKeyed.paths("db")
@DKeyed.redirects("update_")
def get_lib_history(spec, state, _path:pl.Path, _db_file:pl.Path, _update):
    """
    Get any recorded lib sizes for a given file
    returns the history as a dict of {date : count}
    """
    matches = {}
    test_str = str(_path)
    for line in _db_file.read_text().splitlines():
        if test_str not in line:
            continue

        match line.split(":"):
            case _, date_str, count_str:
                date = datetime.datetime.strptime(date_str.strip(), DATE_FORMAT)
                count = int(count_str)
                matches[date] = count
            case _:
                return False

    else:
        doot.report.act(info="History", msg=f"{len(matches)} Records")
        return { _update : matches }

@DKeyed.types("rpath")
@DKeyed.types("lib")
@DKeyed.types("history", fallback=None)
@DKeyed.types("override", fallback=False)
def error_on_entry_decrease(spec, state, _path, lib, history, override):
    """
    Checks the given lib has not decreased in size

    If overriden, will notify on decrease without halting the workflow
    """
    if not bool(history):
        doot.report.act("N/A", f"No History for: {_path}")
        return

    current      = len(lib.entries)
    sorted_dates = sorted(history.keys())
    previous     = sorted_dates[-1]
    date_str = previous.strftime(DATE_FORMAT)
    match history[previous]:
        case int() as p if p == current:
            doot.report.act("N/A", f"{p} -> {current}")
        case int() as p if p < current:
            doot.report.act("++", f"{p} -> {current}")
        case int() as p if current < p and override:
            doot.report.fail(info="Mismatch", msg=f"Current {current} < {p} : ({date_str}) ")
        case int() as p if current < p:
            doot.report.fail(info="Mismatch", msg=f"Current {current} < {p} : ({date_str}) ")
            return False
        case _:
            return False


@DKeyed.types("rpath")
@DKeyed.types("lib")
@DKeyed.types("history", fallback=None)
def log_lib_history(spec, state, _path, lib, history):
    prev = ""
    for x in sorted(history.keys()):
        date_str = x.strftime(DATE_FORMAT)
        count    = history[x]
        doot.report.act(info=f"{_path} {date_str}", msg=f"{prev} -> {count}", level=10)
        prev = f"{count}"
    else:
        pass
