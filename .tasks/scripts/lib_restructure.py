#!/usr/bin/env python3
"""
Utility script to restructure library pdfs to group by decade

"""
# ruff: noqa:
from __future__ import annotations

# Imports:
# ##-- stdlib imports
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import collections
import contextlib
import hashlib
from copy import deepcopy
from uuid import UUID, uuid1
from weakref import ref
import atexit # for @atexit.register
import faulthandler
# ##-- end stdlib imports

import shutil
import math
import sys
import tqdm
import bibble as BM
import bibble._interface as API
from bibble.io import Writer, Reader

# ##-- types
# isort: off
# General
import abc
import collections.abc
import typing
import types
from typing import cast, assert_type, assert_never
from typing import Generic, NewType, Never
from typing import no_type_check, final, override, overload
# Protocols and Interfaces:
from typing import Protocol, runtime_checkable
# isort: on
# ##-- end types

# ##-- type checking
# isort: off
if typing.TYPE_CHECKING:
    from typing import Final, ClassVar, Any, Self
    from typing import Literal, LiteralString
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

    from jgdv import Maybe
## isort: on
# ##-- end type checking

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

# Vars:
CHUNK_SIZE     : Final[int]              = 100
FAIL_TARGET    : Final[pl.Path]          = pl.Path()
MAIN_DIR       : Final[pl.Path]          = pl.Path("main")
GLOB_STR       : Final[str]              = "*.bib"
LIB_ROOT       : Final[pl.Path]          = pl.Path("/media/john/data/library/pdfs")
NEW_ROOT       : Final[pl.Path]          = pl.Path("/media/john/data/library/pdfs_structured")

CENTURY_RANGE  : Final[tuple[int, int]]  = (1200, 2100)
ZERO_ZERO_ONE  : Final[float]            = 0.01
ZERO_ONE       : Final[float]            = 0.1
HUNDRED        : Final[int]              = 100
TEN            : Final[int]              = 10
WINDOW_SIZE    : Final[int]              = 10
##--| Body

def window_collection(i:int, coll:list) -> list[pl.Path]:
    if i == -1:
        return coll

    start   = WINDOW_SIZE * i
    window  = coll[start:(start + WINDOW_SIZE)]
    return window

def build_reader_and_writer() -> tuple[Reader, API.Writer_p]:
    stack     = BM.PairStack()
    extra     = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[
                  BM.failure.FailureHandler(),
              ])
    stack.add(BM.bidi.BraceWrapper(),
              # BM.bidi.BidiPaths(lib_root=LIB_ROOT),
              )

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)],
              write=[extra])
    reader = Reader(stack)
    writer = Writer(stack)
    return reader, writer

def collect(source:pl.Path) -> list[pl.Path]:
    if source.is_file():
        return [source]
    results = source.glob(GLOB_STR)
    return list(sorted(results))

def generate_year_structures() -> None:
    print("Generating Century/Decade Directories")
    centuries  = list(range(*CENTURY_RANGE, 100))
    for cent in centuries:
        century = NEW_ROOT / str(cent)
        for dec in range(cent, cent+100, 10):
            if 2030 < dec:
                return
            decade = century / str(dec)
            decade.mkdir(parents=True, exist_ok=True)

def year_to_pair(year:int) -> pl.Path:
    century  = int(year * ZERO_ZERO_ONE) * HUNDRED
    decade   = int(year * ZERO_ONE) * TEN
    return pl.Path(f"{century}/{decade}")

def retarget_entries(lib, base:pl.Path, decade:pl.Path) -> None:
    print("Retargeting Entries for: %s", base)
    for entry in tqdm.tqdm(lib.entries):
        for key,val in entry.fields_dict.items():
            if "file" not in key:
                continue
            assert(isinstance(val.value, str))
            file       = pl.Path(val.value)
            if file.is_relative_to(decade):
                continue
            target     = decade / file
            val.value  = target


def retarget_files(i:int) -> None:
    print("Retargeting Directories")
    dirs = list(sorted(LIB_ROOT.glob("*")))
    for dir in tqdm.tqdm(window_collection(i, dirs)):
        if dir.is_file():
            continue
        rel_path  = dir.relative_to(LIB_ROOT)
        target    = NEW_ROOT / year_to_pair(int(dir.stem)) / dir.stem
        assert(not target.exists())
        dir.rename(target)

def main():
    window = -1
    match sys.argv:
        case [_, "--window", str() as wind]:
            window   = int(wind)
            targets  = collect(MAIN_DIR)
        case [_, str() as target]:
            print(f"Source: {target}")
            targets = collect(pl.Path(target))
        case [_]:
            targets = collect(MAIN_DIR)
        case x:
            raise TypeError(type(x))
    reader, writer  = build_reader_and_writer()
    generate_year_structures()
    for bib in window_collection(window, targets):
        lib         = reader.read(bib)
        new_prefix  = year_to_pair(int(bib.stem))
        retarget_entries(lib, bib, new_prefix)
        writer.write(lib, file=bib)
    else:
        retarget_files(window)
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
