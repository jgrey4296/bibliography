#!/usr/bin/env -S uv run --script
"""
Read bibtex files, save tags into .temp
"""
# ruff: noqa: N812
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
import task_utils as _util

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

from os import environ
# Vars:
BIBLIO_ROOT  : Final[pl.Path]  = pl.Path(environ['POLYGLOT_ROOT'])
BIBLIO_TEMP  : Final[pl.Path]  = pl.Path(environ['POLYGLOT_TEMP'])
BIBLIO_TAGS  : Final[pl.Path]  = pl.Path(environ['BIBLIO_TAGS_LOC'])
LIB_ROOT     : Final[pl.Path]  = pl.Path(environ['BIBLIO_LIB'])

MAIN_BIB     : Final[pl.Path]  = BIBLIO_ROOT / "main"
TAGS_BASE    : Final[pl.Path]  = BIBLIO_ROOT / "tags/substitutions"
FAIL_TARGET  : Final[pl.Path]  = BIBLIO_TEMP / "failed.bib"
OUT_BASE     : Final[pl.Path]  = BIBLIO_TEMP / "tags"

TAGS_KNOWN   : Final[pl.Path]  = pl.Path("known.tags")

GLOB_STR     : Final[str]      = "*.bib"
##--| argparse
import argparse
parser = argparse.ArgumentParser(
    prog="biblio tags",
    description="Update tag files",
)
parser.add_argument("--output",                   default=OUT_BASE)
##--| Body

def build_reader_and_writer() -> tuple[Reader, API.Writer_p]:
    print("Building Bibtex Reader/Writer...")
    stack = BM.PairStack()
    extra = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[BM.failure.FailureHandler()],
              )
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiPaths(lib_root=LIB_ROOT),
              BM.bidi.BidiTags(),
              read=[
                  BM.fields.FieldAccumulator(name="all-tags", fields=["tags"]),
              ])
    reader = Reader(stack)
    writer = Writer(stack)
    return reader, writer


def main() -> None:
    args         = parser.parse_args()
    output_base  = pl.Path(args.output)
    output_base.mkdir(exist_ok=True)

    # Load Tags from bib files
    targets = _util.collect(MAIN_BIB)
    reader, writer  = build_reader_and_writer()
    raw             = TagFile()
    print("Reading Bibtex files...")
    for bib in targets:
        lib = reader.read(bib)
        match lib.blocks:
            case [*_, AccumulationBlock() as tags]:
                raw.update(tags.collection)
            case _:
                pass
    else:
        (output_base / TAGS_KNOWN).write_text(str(raw))
        print(f"Tag files writen in: {output_base}")


##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
