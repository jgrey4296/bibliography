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

import jinja2
import math
import json
import sys
import tqdm
import bibble as BM
import bibble._interface as API
from bibble.io import Reader
from bibble.fields._interface import AccumulationBlock
from bibtexparser.model import Entry

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
MAIN_DIR           : Final[pl.Path]  = pl.Path("main")
GLOB_STR           : Final[pl.Path]  = "*.bib"
REPORT_DATA        : Final[pl.Path]  = pl.Path(".temp/report.json")
REPORT_FILE        : Final[pl.Path]  = pl.Path("report.html")
FAIL_TARGET        : Final[pl.Path]  = pl.Path(".temp/failed.bib")
TEMPLATE_DIR       : Final[pl.Path]  = pl.Path("templates_")
REPORT_TEMPLATE_K  : Final[str]      = "report.html.jinja"
STATS_BASE         : Final[dict]     = {
    "authors"      : collections.defaultdict(lambda: 0),
    "editors"      : collections.defaultdict(lambda: 0),
    "entry_count"  : 0,
    "entry_types"  : collections.defaultdict(lambda: 0),
    "tags"         : set(),
    "year_max"     : 0,
    "year_min"     : math.inf,
    "file_count"   : 0,
    "url_count"    : 0,
}

##--|

class SetEncoder(json.JSONEncoder):
    """ JSON encoder able to handle sets """

    def default(self, obj:Any) -> Any:
        match obj:
            case set():
                return list(obj)
            case _:
                return super().default(obj)

##--| Body

def build_reader() -> Reader:
    stack = BM.PairStack()
    extra = BM.metadata.DataInsertMW()
    stack.add(read=[extra,
                    BM.failure.DuplicateKeyHandler(),
                    BM.bidi.BraceWrapper(),
                    BM.bidi.BidiNames(parts=False, authors=True),
                    BM.bidi.BidiTags(),
                    ])

    stack.add(read=[
        BM.fields.FieldAccumulator(name="all-tags",     fields=["tags"]),
        BM.fields.FieldAccumulator(name="all-pubs",     fields=["publisher"]),
        BM.fields.FieldAccumulator(name="all-series",   fields=["series"]),
        BM.fields.FieldAccumulator(name="all-journals", fields=["journal"]),
        BM.fields.FieldAccumulator(name="all-people",   fields=["author", "editor"]),
        # BM.fields.FieldDifference(known=_tagsubs, accumulated="all-tags")
    ])

    stack.add(read=[BM.failure.FailureHandler(file=FAIL_TARGET)])
    reader = Reader(stack)
    return reader

def init_jinja() -> jinja2.Environment:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        autoescape=jinja2.select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
        )

def collect(source:pl.Path) -> list[pl.Path]:
    if source.is_file():
        return [source]
    results = source.glob(GLOB_STR)
    return list(results)

def update_stats(stats:dict, lib:API.Library_p) -> None:
    x     : Any
    year  : int
    meta = BM.model.MetaBlock.find_in(lib)
    for entry in tqdm.tqdm(lib.entries):
        fields = entry.fields_dict
        year = int(fields['year'].value)

        stats['entry_count'] += 1
        stats['entry_types'][entry.entry_type] += 1
        stats['tags'].update(fields['tags'].value)
        match fields.get('author', None):
            case None:
                pass
            case x:
                for author in x.value:
                    stats['authors'][author] += 1
        match fields.get('editor', None):
            case None:
                pass
            case x:
                for editor in x.value:
                    stats['editors'][editor] += 1

        if year < stats['year_min']:
            stats['year_min'] = year
        if stats['year_max'] < year:
            stats['year_max'] = year

        if 'file' in fields:
            stats['file_count'] += 1
        if 'url' in fields:
            stats['url_count'] += 1
    else:
        pass

def write_report(stats:dict) -> None:
    # write raw data
    REPORT_DATA.write_text(json.dumps(stats, indent=4, cls=SetEncoder))
    # Write the report
    env          = init_jinja()
    template     = env.get_template(REPORT_TEMPLATE_K)
    report_text  = template.render()
    REPORT_FILE.write_text(report_text)

def main():
    match sys.argv:
        case [_, str() as target]:
            targets = collect(pl.Path(target))
        case [_, *xs]:
            targets = [pl.Path(x) for x in xs]
            assert(bool(targets))
        case [_]:
            targets = collect(MAIN_DIR)
        case x:
            raise TypeError(type(x))

    reader  = build_reader()
    stats   = deepcopy(STATS_BASE)
    for bib in targets:
        lib = reader.read(bib)
        print("Updating Stats from: %s", bib)
        update_stats(stats, lib)
    else:
        write_report(stats)
        print("Finished")

##-- ifmain
if __name__ == "__main__":
    main()
##-- end ifmain
