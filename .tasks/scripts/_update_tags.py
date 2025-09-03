#!/usr/bin/env python3
"""

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
TAGS_BASE   : Final[pl.Path]  = "tags/substitutions"
TAGS_TOTAL  : Final[pl.Path]  = ".temp/tags/total.sub"
TAGS_CANON  : Final[pl.Path]  = ".temp/tags/canon.tags"
TAGS_KNOWN  : Final[pl.Path]  = ".temp/tags/known.tags"
TAGS_FRESH  : Final[pl.Path]  = ".temp/tags/fresh.tags"

##--| Body

def load_tags() -> SubstitutionFile:
    pass

def build_reader_and_writer() -> tuple[Reader, JinjaWriter]:
    stack = BM.PairStack()
    extra = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[
                  BM.failure.FailureHandler(),
              ])
    stack.add(BM.bidi.BraceWrapper()
              BM.bidi.BidiPaths(lib_root=LIB_ROOT))

    stack.add(
        BM.bidi.BidiNames(parts=True, authors=True),
        BM.bidi.BidiIsbn(),
        BM.bidi.BidiTags(),
        None,
        read=[
            BM.metadata.KeyLocker(),
            BM.fields.TitleSplitter()
        ])
    stack.add(write=[
        BM.fields.FieldAccumulator(name="all-tags",     fields=["tags"]),
        BM.fields.FieldAccumulator(name="all-pubs",     fields=["publisher"]),
        BM.fields.FieldAccumulator(name="all-series",   fields=["series"]),
        BM.fields.FieldAccumulator(name="all-journals", fields=["journal"]),
        BM.fields.FieldAccumulator(name="all-people",   fields=["author", "editor"]),
        # BM.fields.FieldDifference(known=_tagsubs, accumulated="all-tags")
        ])

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)],
              write=[extra])
    reader = Reader(stack)
    writer = JinjaWriter(stack)
    return reader, writer

def collect(source:pl.Path) -> list[pl.Path]:
    results = source.glob(GLOB_STR)

    return results

def main():
    match sys.argv:
        case [_, str() as target]:
            print(f"Source: {target}")
            targets = collect(pl.Path(target))
        case x:
            raise TypeError(type(x))

    reader, writer = build_reader_and_writer()
    # TODO use tqdm here:
    for bib in targets:
        print(f"Target : {bib}")
        # lib = reader.read(bib)
        # writer.write(lib, file=bib)
    else:
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
