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
from bibble.io import PairStack
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

meta_keys = {"all", "apply", "latex", "rst", "subs", "check", "fsort", "esort", "count",}

# Body:
@DKeyed.kwargs
@DKeyed.paths("libroot")
@DKeyed.redirects("update_")
def build_new_stack(spec, state, kwargs:dict, _libroot:pl.Path,
                    _namesubs:Maybe[SubstitutionFile],
                    _tagsubs:Maybe[SubstitutionFile],
                    _othersubs:Maybe[SubstitutionFile],
                    _update) -> PairStack:
    """ Build a new PairStack of middlewares, with optional and required elements
    Because of how pairstack works, to see the parse stack, read from top to bottom.
    To see the write transforms, read from bottom to top.
    """
    _meta = set(_meta.keys())
    ALL   = "all" in _meta
    APPLY = ALL or "apply" in _meta
    LATEX = ALL or "latex" in _meta
    FSORT = ALL or "fsort" in _meta
    ESORT = ALL or "esort" in _meta
    COUNT = ALL or "count" in _meta
    SUBS  = ALL or "subs" in _meta
    CHECK = ALL or "check" in _meta

    stack = PairStack()
    # Very first/last middlewares:
    stack.add(read=[BM.failure.DuplicateKeyHandler(),
                    ],
              write=[BM.failure.FailureHandler(),
                     BM.metadata.ApplyMetadata() if APPLY else None,
                     ])
    # Add bidirectional transforms
    stack.add(BM.bidi.BraceWrapper(),
              BM.bidi.BidiLatex() if LATEX else None,
              BM.bidi.BidiPaths(lib_root=_libroot),
              BM.bidi.BidiNames(),
              BM.bidi.BidiIsbn(),
              BM.bidi.BidiTags(),
              None,
              read=[
                  BM.metadata.KeyLocker(),
                  BM.fields.TitleSplitter()
              ],
              write=[
                  BM.fields.FieldSorter(first=sort_firsts, last=sort_lasts) if FSORT else None,
                  BM.metadata.EntrySorter() if ESORT else None,
              ])

    if COUNT:
        # Accumulate various fields
        stack.add(write=[
            BM.fields.FieldAccumulator("all-tags",     ["tags"]),
            BM.fields.FieldAccumulator("all-pubs",     ["publisher"]),
            BM.fields.FieldAccumulator("all-series",   ["series"]),
            BM.fields.FieldAccumulator("all-journals", ["journal"]),
            BM.fields.FieldAccumulator("all-people",   ["author", "editor"]),
        ])

    if SUBS:
        stack.add(write=[
            # NameSubs need to merge with BidiNames
            # BM.people.NameSubstitutor(_namesubs) if _namesubs is not None else None,
            BM.fields.FieldSubstitutor("tags", subs=_tagsubs) if _tagsubs is not None else None,
            BM.fields.FieldSubstitutor(sub_fields, subs=_othersubs, force_single_value=True) if _othersubs is not None else None,
        ])

    if CHECK:
        stack.add(write=[BM.metadata.FileCheck()])

    return { _update : stack }
