#!/usr/bin/env python3
"""

"""
# ruff: noqa: F401

# Imports:
from __future__ import annotations

# ##-- stdlib imports
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import collections
import contextlib
import hashlib
from copy import deepcopy
from uuid import UUID, uuid1
from weakref import ref
import atexit # for @atexit.register
import faulthandler
# ##-- end stdlib imports

import bibble as BM
import bibtexparser as BTP
import doot
import doot.errors
from bibtexparser import middlewares as ms
from doot.structs import DKey, DKeyed, TaskSpec
from bibble import PairStack
from jgdv.files.tags import SubstitutionFile

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType
# Protocols:
from typing import Protocol, runtime_checkable
# Typing Decorators:
from typing import no_type_check, final, override, overload

if TYPE_CHECKING:
    from jgdv import Maybe
    from typing import Final
    from typing import ClassVar, Any, LiteralString
    from typing import Never, Self, Literal
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

    type M_SubF = Maybe[SubstitutionFile]
##--|

# isort: on
# ##-- end types

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

# Vars:
sort_firsts = ["title", "author", "editor", "year", "tags", "booktitle", "journal", "volume", "number", "edition", "edition_year", "publisher"]
sort_lasts  = ["isbn", "doi", "url", "file", "crossref"]
sub_fields  = ["publisher", "journal", "series", "institution"]
meta_keys   = {
    "all"    : "run all middlewares",
    "check"  : "check metadata/urls",
    "latex"  : "latex read/write",
    "rst"    : "rst write",
    "count"  : "field counting",
    "online" : "online downloading",
    "format" : "general formatting",
    "validate" : "in depth validation / metadata application",
    "report"  : "generate a report on the loaded bibtex",
}

# Body:

@DKeyed.kwargs
@DKeyed.paths("lib-root")
@DKeyed.paths("online_saves")
@DKeyed.types("people_subs", "tag_subs", "other_subs", check=SubstitutionFile|None)
@DKeyed.redirects("update_")
def build_new_stack(spec, state, kwargs:dict, _libroot:pl.Path, _online:pl.Path, _namesubs:M_SubF=None, _tagsubs:M_SubF=None, _othersubs:M_SubF=None, _update=None) -> PairStack:
    """ Build a new PairStack of middlewares, with optional and required elements
    Because of how pairstack works, to see the parse stack, read from top to bottom.
    To see the write transforms, read from bottom to top.
    """
    _meta = set(x for x,y in kwargs.items() if y is True)
    if bool((extra:=_meta - set(meta_keys.keys()))):
        msg = "Unrecognised meta keys provided"
        raise ValueError(msg, extra)

    ALL      = "all"             in _meta
    CHECK    = ALL or "check"    in _meta
    VALIDATE = ALL or "validate" in _meta
    LATEX    = ALL or "latex"    in _meta
    RST      = ALL or "rst"      in _meta
    COUNT    = ALL or "count"    in _meta
    ONLINE   = ALL or "online"   in _meta
    FORMAT   = ALL or "format"   in _meta
    REPORT   = ALL or "reprot"   in _meta

    # Extra data is added at the start of both stack directions
    extra_data = BM.metadata.DataInsertMW()

    stack    = PairStack()

    stack.add(read=[extra_data])
    # Very first/last middlewares:
    stack.add(read=[BM.failure.DuplicateKeyHandler()],
              write=[
                  BM.failure.FailureHandler(),
                  BM.metadata.ApplyMetadata() if VALIDATE else None,
              ])
    # Add standard bidirectional transforms
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiLatex() if LATEX else None,
              BM.bidi.BidiPaths(lib_root=_libroot),
              None,
              )

    if FORMAT:   # Cleaning up entries
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
                BM.fields.FieldSubstitutor(fields=["tags"], subs=_tagsubs) if _tagsubs is not None else None,
                BM.fields.FieldSubstitutor(fields=sub_fields, subs=_othersubs, force_single_value=True) if _othersubs is not None else None,
            ])

    if FORMAT and COUNT: # counting tags etc
        # Accumulate various fields
        stack.add(write=[
            BM.fields.FieldAccumulator(name="all-tags",     fields=["tags"]),
            BM.fields.FieldAccumulator(name="all-pubs",     fields=["publisher"]),
            BM.fields.FieldAccumulator(name="all-series",   fields=["series"]),
            BM.fields.FieldAccumulator(name="all-journals", fields=["journal"]),
            BM.fields.FieldAccumulator(name="all-people",   fields=["author", "editor"]),

            # BM.fields.FieldDifference(known=_tagsubs, accumulated="all-tags")
        ])

    if CHECK:    # entry mutation checks
        stack.add(write=[
            BM.metadata.FileCheck(),
            # BM.fields.Waybacker(),
            # BM.files.HashFiles(),
        ])

    if VALIDATE: # entry static checks
        stack.add(write=[
            # BM.files.VirusScan(),
            # BM.fields.UrlCheck(),
            # BM.metadata.DoiValidator(),
            # BM.metadata.CrossrefValidator(),
        ])


    if ONLINE:   # online saving
        # Ignore path relative errors:
        extra_data.update({BM.files.PathWriter.SuppressKey:[_online]})
        stack.add(read=[
            BM.files.OnlineDownloader(target=_online),
        ])

    if REPORT:   # stats
        stack.add(write=[
            # BM.reporters.SummaryGenerator(),
        ])

    stack.add(read=[BM.failure.FailureHandler(file=doot.locs['bibfails'])])
    stack.add(write=[extra_data])
    return { _update : stack }
