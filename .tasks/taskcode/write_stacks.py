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
from taskcode.rst import Bib2RstEntryTransformer

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

@DKeyed.paths("lib-root")
@DKeyed.types("tag_subs", "other_subs", "people_subs", fallback=None)
@DKeyed.redirects("update_")
def build_format_stack(spec, state, _libroot, _tagsubs, _othersubs, _namesubs, _update):
    """ Doesn't encode into latex,'
    Expects split author names.
    joins authors, formats isbns, checks files, joins tags,
    encloses with braces
    """
    sort_firsts = ["title", "author", "editor", "year", "tags", "booktitle", "journal", "volume", "number", "edition", "edition_year", "publisher"]
    sort_lasts  = ["isbn", "doi", "url", "file", "crossref"]
    sub_fields  = ["publisher", "journal", "series", "institution"]

    write_mids  = [
        BM.people.NameWriter(),
        BM.people.NameSubstitutor(_namesubs),
        ms.MergeCoAuthors(allow_inplace_modification=False),
        BM.metadata.IsbnWriter(),
        BM.fields.FieldSubstitutor("tags",           subs=_tagsubs),
        BM.fields.FieldSubstitutor(sub_fields,       subs=_othersubs, force_single_value=True),
        BM.metadata.TagsWriter(),
        BM.metadata.FileCheck(),
        BM.files.PathWriter(lib_root=_libroot),
        BM.fields.FieldSorter(sort_firsts, sort_lasts),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids }


@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_export_latex_stack(spec,state, _libroot, _update):
    """ encodes into latex for compilation """
    write_mids = [
        BM.people.NameWriter(),
        ms.MergeCoAuthors(),
        BM.latex.LatexWriter(), # maybe .skip_fields(...)
        BM.metadata.IsbnWriter(),
        BM.metadata.TagsWriter(to_keywords=True),
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids }

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_export_rst_stack(spec,state, _libroot, _update):
    """ encodes into rst for compilation by sphinx """
    write_mids = [
        BM.people.NameWriter(),
        ms.MergeCoAuthors(),
        BM.metadata.IsbnWriter(),
        BM.metadata.TagsWriter(),
        Bib2RstEntryTransformer()
    ]
    return { _update : write_mids }


@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_online_download_stack(spec, state, _libroot, _update):
    """ just writes paths appropriately, does no other processing """
    write_mids = [
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids}
