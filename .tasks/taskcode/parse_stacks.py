#!/usr/bin/env python3
"""

"""

from __future__ import annotations

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

import bibtexparser as BTP
from bibtexparser import middlewares as ms
import doot
import doot.errors
from doot.structs import DKey, TaskSpec, DKeyed
import bib_middleware as BM

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_general_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries. no latex decoding
    handles file paths,
    splits tags,
    separates coauthors
    """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.RemoveEnclosingMiddleware(),
        BM.files.PathReader(lib_root=_libroot),
        BM.metadata.IsbnValidator(),
        BM.metadata.TagsReader(),
        ms.SeparateCoAuthors(),
        BM.people.NameReader(),
        BM.fields.SubTitleReader(),
    ]
    return { _update : read_mids }

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_meta_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without decoding latex
    pre-processes file paths,
    validates isbn's,
    splits tag strings into a set
    """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.RemoveEnclosingMiddleware(True),
        ms.SeparateCoAuthors(),
        BM.files.PathReader(lib_root=_libroot),
        BM.metadata.IsbnValidator(True),
        BM.metadata.TagsReader(),
        BM.fields.TitleReader(),

        BM.fields.FieldAccumulator("all-tags",     ["tags"]),
        BM.fields.FieldAccumulator("all-pubs",     ["publisher"]),
        BM.fields.FieldAccumulator("all-series",   ["series"]),
        BM.fields.FieldAccumulator("all-journals", ["journal"]),
        BM.fields.FieldAccumulator("all-people",   ["author", "editor"]),
    ]
    return { _update : read_mids }

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_backup_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without handling latex encoding """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.RemoveEnclosingMiddleware(True),
        BM.files.PathReader(lib_root=_libroot),
    ]
    return { _update : read_mids }

@DKeyed.redirects("update_")
def build_minimal_stack(spec, state, _update):
    """ a minimal reader for moving entries around """
    read_mids = [
        BM.DuplicateHandler(),
        ms.RemoveEnclosingMiddleware(True),
    ]
    return { _update : read_mids}

@DKeyed.paths("lib-root", "online_saves")
@DKeyed.redirects("update_")
def build_online_download_stack(spec, state, _libroot, _dltarget, _update):
    """ downloads urls as pdfs if entry is 'online' and it doesn't have a file associated already """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.RemoveEnclosingMiddleware(),
        BM.files.PathReader(lib_root=_libroot),
        BM.files.OnlineDownloader(target=_dltarget),
    ]
    return { _update : read_mids}
