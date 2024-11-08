#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""

##-- builtin imports
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
# from copy import deepcopy
# from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeAlias, TypeGuard, TypeVar,
                    cast, final, overload, runtime_checkable, Generator)
from uuid import UUID, uuid1

##-- end builtin imports

##-- lib imports
import more_itertools as mitz
##-- end lib imports

from random import choice, choices

import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.structs import DKey, DKeyed
import bib_middleware as BM

##-- logging
logging = logmod.getLogger(__name__)
printer = doot.subprinter("action_exec")
##-- end logging

MYBIB    = "#my_bibtex"
MAX_TAGS = 7

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_working_parse_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without handling latex encoding """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(),
        ms.RemoveEnclosingMiddleware(),
        BM.files.PathReader(lib_root=_libroot),
        BM.metadata.IsbnValidator(),
        BM.metadata.TagsReader(),
        ms.SeparateCoAuthors(),
        BM.people.NameReader(),
        BM.fields.TitleReader()
    ]
    return { _update : read_mids }

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_working_write_stack(spec, state, _libroot, _update):
    """ Doesn't encode into latex """
    write_mids = [
        BM.people.NameWriter(),
        ms.MergeCoAuthors(allow_inplace_modification=False),
        BM.metadata.IsbnWriter(),
        BM.metadata.TagsWriter(),
        BM.metadata.FileCheck(),
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids }

@DKeyed.redirects("update_")
def build_minimal_parse_stack(spec, state, _update):
    """ a minimal reader for moving entries around """
    read_mids = [
        BM.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(True),
        ms.RemoveEnclosingMiddleware(True),
    ]
    return { _update : read_mids}

@DKeyed.types("entry")
def log_entry_name(spec, state, entry):
    match entry.fields_dict.get("title", None):
        case None:
            printer.info("> %s", entry.key)
        case x:
            printer.info("> %s", x.value)

@DKeyed.types("entry")
@DKeyed.redirects("update_")
def get_entry_file(spec, state, entry, _update):
    match entry.fields_dict.get("file", None):
        case None:
            return
        case x:
            return { _update : x.value }
