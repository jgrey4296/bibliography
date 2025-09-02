#!/usr/bin/env python3
"""
Utility script to report on the repo bibtex files

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
from bibble.io import Reader

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
REPORT_FILE : Final[pl.Path] = pl.Path("report.html")

##--| Body

def build_reader() -> Reader:
    stack = BM.PairStack()



    reader = Reader(stack)
    return reader

def collect() -> list[pl.Path]:
    results = []
    return results

def update_stats(stats:dict, lib:BM.Library) -> None:
    pass

def write_report(stats:dict) -> None:
    pass

def main():
    reader   = build_reader()
    targets  = collect()
    stats    = {}
    # TODO use tqdm here:
    for bib in targets:
        lib = reader.read(bib)
        update_stats(stats, lib)
    else:
        write_report(stats)
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
