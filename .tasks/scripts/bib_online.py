#!/usr/bin/env python3
"""
Utility script to download urls mentioned in bibtex files

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
ONLINE_SOURCE    : Final[pl.Path]  = pl.Path("in_progress/online.bib")
DOWNLOAD_TARGET  : Final[pl.Path]  = pl.Path("/media/john/data/todo/pdfs/online")
LIB_ROOT         : Final[pl.Path]  = pl.Path("/media/john/data/library/pdfs")
SAVE_TARGET      : Final[pl.Path]  = pl.Path(".temp/online_saved.bib")
FAIL_TARGET      : Final[pl.Path]  = pl.Path(".temp/failed.bib")

##--| Body

def build_reader_and_writer() -> tuple[Reader, API.Writer_p]:
    stack = BM.PairStack()
    extra = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[BM.failure.FailureHandler()])
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiPaths(lib_root=LIB_ROOT),
              )

    extra.update({BM.files.PathWriter.SuppressKey:[DOWNLOAD_TARGET]})
    stack.add(read=[BM.files.OnlineDownloader(target=DOWNLOAD_TARGET)])

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)], write=[extra])
    reader = Reader(stack)
    writer = Writer(stack)
    return reader, writer

def main():
    match sys.argv:
        case [*_, "--help"]:
            print("bib_online.py target:str")
            sys.exit()
        case [_]:
            target = ONLINE_SOURCE
        case [_, str() as target]:
            target = pl.Path(target)
        case x:
            raise TypeError(type(x))
    print("Starting online downloader")
    reader, writer = build_reader_and_writer()
    lib = reader.read(target)
    writer.write(lib, file=SAVE_TARGET)
    print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
