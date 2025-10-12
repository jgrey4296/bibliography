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

import sys
import tqdm
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", SyntaxWarning)
    import bibble as BM
    import bibble._interface as API
    from bibble.io import Reader
    from bibble.io import Writer
    from bibble.fields._interface import AccumulationBlock

from jgdv.files.tags import SubstitutionFile, TagFile
from jgdv.files.bookmarks import BookmarkCollection
import _util

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
MAIN_BIB     : Final[pl.Path]  = pl.Path("main")
TAGS_BASE    : Final[pl.Path]  = pl.Path("tags/substitutions")
TAGS_TOTAL   : Final[pl.Path]  = pl.Path(".temp/tags/total.sub")
TAGS_CANON   : Final[pl.Path]  = pl.Path(".temp/tags/canon.tags")
TAGS_KNOWN   : Final[pl.Path]  = pl.Path(".temp/tags/known.tags")
TAGS_FRESH   : Final[pl.Path]  = pl.Path(".temp/tags/fresh.tags")
LIB_ROOT     : Final[pl.Path]  = pl.Path("/media/john/data/library/pdfs")
FAIL_TARGET  : Final[pl.Path]  = pl.Path(".temp/failed.bib")
BOOKMARKS    : Final[pl.Path]  = pl.Path("bookmarks/total.bookmarks")

##--| Body

def get_tags_from_bookmarks() -> TagFile:
    bookmarks = BookmarkCollection.read(BOOKMARKS)
    bkmk_tags = TagFile()
    for bkmk in bookmarks:
        bkmk_tags.update(bkmk.tags)
    else:
        return bkmk_tags

def build_reader_and_writer() -> tuple[Reader, API.Writer_p]:
    stack = BM.PairStack()
    extra = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ]
              )
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiPaths(lib_root=LIB_ROOT),
              BM.bidi.BidiTags(),
              read=[
                  BM.fields.FieldAccumulator(name="all-tags", fields=["tags"]),
                  BM.failure.FailureHandler(file=FAIL_TARGET)
              ])
    reader = Reader(stack)
    writer = Writer(stack)
    return reader, writer

def collate_tags(subs:SubstitutionFile, raw:TagFile, bkmks:TagFile) -> tuple[TagFile, TagFile]:
    """  """
    canon = subs.canonical()
    total = TagFile()
    fresh = TagFile()

    total.update(canon)
    total.update(subs.to_set())
    total.update(raw.to_set())
    total.update(bkmks)

    raw_set = total.to_set()
    raw_set -= subs.to_set()
    raw_set -= canon.to_set()
    fresh.update(raw_set)

    return (canon, fresh, total)

def main():
    match sys.argv:
        case [*_, "--help"]:
            print("update_tags.py target:str*")
            sys.exit()
        case [_, str() as target] if bool(target):
            print(f"Source: {target}")
            targets = _util.collect(pl.Path(target))
        case [_, *_]:
            targets = _util.collect(MAIN_BIB)
        case x:
            raise TypeError(type(x))

    # Load known:
    subs   = _util.load_tags(TAGS_BASE)
    bkmks  = get_tags_from_bookmarks()

    # Load Tags from bib files
    reader, writer  = build_reader_and_writer()
    raw             = TagFile()
    for bib in targets:
        lib = reader.read(bib)
        match lib.blocks:
            case [*_, AccumulationBlock() as tags]:
                raw.update(tags.collection)
            case _:
                pass
    else:
        canon, fresh, total = collate_tags(subs, raw, bkmks)
        TAGS_TOTAL.write_text(str(total))
        TAGS_CANON.write_text(str(canon))
        TAGS_KNOWN.write_text(str(raw))
        TAGS_FRESH.write_text(str(fresh))
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
