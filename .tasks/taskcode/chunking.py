#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""
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
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generator,
                    Generic, Iterable, Iterator, Mapping, Match,
                    MutableMapping, Protocol, Sequence, Tuple, TypeAlias,
                    TypeGuard, TypeVar, cast, final, overload,
                    runtime_checkable)
from uuid import UUID, uuid1

import bib_middleware as BM
import bibtexparser as BTP
import doot
import doot.errors
import more_itertools as mitz
from bibtexparser import middlewares as ms
from doot.structs import DKeyed

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

@DKeyed.types("bib_size", check=int, fallback=250)
@DKeyed.types("from", check=BTP.Library)
@DKeyed.redirects("update_")
def split_library(spec, state, bib_size, _base_lib, _update):
    """ Get a library of bibtex entries and split into chunks """
    max_count         = bib_size
    libs              = []
    curr              = BTP.Library()
    curr.source_files = _base_lib.source_files.copy()
    curr.split_count  = 0
    for entry in base.entries:
        if len(curr._blocks) > max_count:
            libs.append(curr)
            curr = BTP.Library()
            curr.source_files = base.source_files.copy()
            curr.split_count = libs[-1].split_count + 1

        curr.add(entry)
    else:
        libs.append(curr)
    printer.info("Split Into %s Sub Libraries", len(libs))
    return { _update : libs }

@DKeyed.types("from", check=BTP.Library)
@DKeyed.redirects("update_")
def generate_stem(spec, state, _base_lib, _update):
    source = list(_base_lib.source_files)[0]
    count  = _base_lib.split_count
    fstem  = f"{source.stem}_{count}"
    return { _update : fstem }
