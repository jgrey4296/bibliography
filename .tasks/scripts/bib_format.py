#!/usr/bin/env python3
"""
Utility script to format bibtex files

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
import bibble as BM
import bibble._interface as API
from bibble.io import Reader
from bibble.io import Writer
from jgdv.files.tags import SubstitutionFile

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
sort_firsts  : Final[list[str]]  = ["title", "subtitle", "author", "editor", "year", "tags", "booktitle", "journal", "volume", "number", "edition", "edition_year", "publisher"]
sort_lasts   : Final[list[str]]  = ["isbn", "doi", "url", "file", "crossref"]
sub_fields   : Final[list[str]]  = ["publisher", "journal", "series", "institution"]
GLOB_STR     : Final[str]        = "*.bib"
LIB_ROOT     : Final[pl.Path]    = pl.Path("/media/john/data/library/pdfs")
TAGS_SOURCE  : Final[pl.Path]    = pl.Path(".temp/tags/canon.tags")
FAIL_TARGET  : Final[pl.Path]    = pl.Path(".temp/failed.bib")
##--| Body

def load_tags() -> SubstitutionFile:
    subs = SubstitutionFile.read(TAGS_SOURCE)
    assert(bool(subs))
    return subs

def build_reader_and_writer() -> tuple[Reader, API.Writer_p]:
    tag_subs  = load_tags()
    stack     = BM.PairStack()
    extra     = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[
                  BM.failure.FailureHandler(),
                  BM.metadata.ApplyMetadata(),
              ])
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiPaths(lib_root=LIB_ROOT))

    stack.add(
        BM.bidi.BidiNames(parts=True, authors=True),
        BM.bidi.BidiIsbn(),
        BM.bidi.BidiTags(),
        None,
        read=[
            BM.metadata.KeyLocker(),
            BM.fields.TitleSplitter()
        ],
        write=[
            BM.fields.FieldSorter(first=sort_firsts, last=sort_lasts),
            BM.metadata.EntrySorter(),
            BM.fields.FieldSubstitutor(fields=["tags"], subs=tag_subs),
            # BM.fields.FieldSubstitutor(fields=sub_fields, subs=_othersubs, force_single_value=True),
        ])
    stack.add(write=[
        BM.metadata.FileCheck(),
        # BM.fields.Waybacker(),
        # BM.files.HashFiles(),
    ])
    stack.add(write=[
        # BM.files.VirusScan(),
        # BM.fields.UrlCheck(),
        # BM.metadata.DoiValidator(),
        # BM.metadata.CrossrefValidator(),
    ])

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)],
              write=[extra])
    reader = Reader(stack)
    writer = Writer(stack)
    return reader, writer

def collect(source:pl.Path) -> list[pl.Path]:
    results = source.glob(GLOB_STR)
    return sorted(list(results))

def main():
    match sys.argv:
        case [_, str() as target]:
            print(f"Source: {target}")
            targets = collect(pl.Path(target))
        case x:
            raise TypeError(type(x))

    reader, writer = build_reader_and_writer()
    # TODO use tqdm here:
    for bib in targets[:2]:
        print(f"Target : {bib}")
        lib = reader.read(bib)
        writer.write(lib, file=bib)
    else:
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
