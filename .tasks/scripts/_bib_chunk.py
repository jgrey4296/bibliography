#!/usr/bin/env python3
"""
Utility script to chunk particularly large bibtex files

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

import tqdm
import bibble as BM
import bibble._interface as API
from bibble.io import JinjaWriter, Reader

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
CHUNK_SIZE   : Final[int]      = 100

FAIL_TARGET  : Final[pl.Path]  = pl.Path()
##--| Body

def build_reader_and_writer() -> tuple[Reader, JinjaWriter]:
    stack = BM.PairStack()
    stack.add(read=[BM.metadata.DataInsertWM(),
                    BM.failure.DuplicateKeyHandler(),
                    ],
              write=[BM.failure.FailureHandler()]
              )

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)],
              write=[extra_data])
    reader = Reader(stack)
    writer = JinjaWriter(stack)
    return reader, writer


def collect(source:pl.Path) -> list[pl.Path]:
    results = source.glob(GLOB_STR)

    return results

def chunk_library(lib:BM.Library) -> list[BM.Library]:
    results = []


    return results

def main():
    reader, writer = build_reader_and_writer()
    targets = collect()
    # TODO use tqdm here:
    for bib in targets:
        lib = reader.read(bib)
        for i,chunk in enumerate(chunk_library(lib)):
            chunk_stem = f"{bib.stem}-{i}"
            chunk_path = lib.with_stem(chunk_stem)
            writer.write(chunk, file=chunk_path)
    else:
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
