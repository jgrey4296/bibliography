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
# import more_itertools as mitz
# from boltons import
##-- end lib imports

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

import bibtexparser as BTP
from bibtexparser import middlewares as ms
from bibtexparser.model import Field, Entry
from bibtexparser.middlewares.middleware import BlockMiddleware

import doot
import doot.errors
from doot.structs import DKey, DKeyed
import bib_middleware as BM

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_export_write_stack(spec,state, _libroot, _update):
    """ encodes into latex for compilation """
    write_mids = [
        BM.people.NameWriter(),
        ms.MergeCoAuthors(),
        BM.latex.LatexWriter(),
        BM.metadata.IsbnWriter(),
        BM.metadata.TagsWriter(to_keywords=True),
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids }

@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_export_rst_write_stack(spec,state, _libroot, _update):
    """ encodes into rst for compilation """
    write_mids = [
        BM.people.NameWriter(),
        ms.MergeCoAuthors(),
        BM.metadata.IsbnWriter(),
        BM.metadata.TagsWriter(),
        Bib2RstEntryTransformer()
    ]
    return { _update : write_mids }

# name.encode('ascii', 'xmlcharrefreplace')

@DKeyed.formats("title")
@DKeyed.types("from")
@DKeyed.types("write_stack")
@DKeyed.redirects("update_")
def lib2rst(spec, state, title, _library, write_stack, _update):
    """ Convert a libray to an rst str """
    result = Bib2RstEntryTransformer.build_file_header(title)
    # Prep for export
    for middleware in write_stack:
        _library = middleware.transform(library=_library)

    # Retrieve and add to result
    for i, ent in enumerate(_library.entries):
        assert(hasattr(ent, "_rst"))
        result += Bib2RstEntryTransformer.get_rst_text(ent)
        result += ["", ""]

    # Footer
    result += []

    return { _update : "\n".join(result) }

class Bib2RstEntryTransformer(BlockMiddleware):
    """ Add an _rst field to every library entry
    """
    # These need to match the BibEntryDirective of the sphinx domain
    _entry      : ClassVar[str]       = ".. bibtex:entry:: {}"
    _entry_args : ClassVar[list[str]] = ["title","author", "editor", "year", "tags",
                                         "journal", "booktitle", "within",
                                         "platform", "publisher", "institution",
                                         "series", "url", "doi", "isbn", "edition",
                                         "crossref"
                                         ]
    _indent     : ClassVar[str]       = " "*3
    _curr       : list[str]           = []
    _fields     : dict[str, Field]    = {}
    _key        : str                 = ""

    def transform_entry(self, entry:Entry, library:Library) -> Block:
        self._curr = []
        self._curr.append(self._entry.format(entry.key))
        self._key = entry.key
        self._fields = entry.fields_dict
        match entry.entry_type:
            case "case" | "legal" | "judicial" | "law":
                pass
            case "standard" | "online" | "blog" | "dataset":
                pass
            case "tweet" | "thread":
                pass
            case _:
                self._title_add()
                self._must_add("tags")
                self._can_add("author", "editor", "year", "series")
                self._can_add("journal", "booktitle", "doi", "url", "isbn", "publisher")
                self._can_add("incollection", "institution")
                # TODO volume, number, pages, chapter


        if bool(self._curr):
            self._curr += ["", "", "..",
                           f"{self._indent} Fields:",
                           "{} {}".format(self._indent, ", ".join(self._fields.keys())), "",
                           f"{self._indent} Object Keys:",
                           "{} {}".format(self._indent,
                                          ", ".join([x for x in dir(entry) if "__" not in x]))
                           ]

            entry._rst   = self._curr
            self._curr   = None
            self._fields = None

        return entry

    def _title_add(self) -> None:
        if "title" not in self._fields:
            raise KeyError("no title", self._key)
        val = self._fields['title'].value
        if "subtitle" in self._fields:
            val = " ".join([val, ":",
                            self._fields['subtitle'].value])

        self._curr.append(f"{self._indent}:title: {val}")

    def _must_add(self, key) -> None:
        if key not in self._entry_args:
            return
        if key not in self._fields:
            raise KeyError('tags', self._key)

        val = self._fields[key].value
        self._curr.append(f"{self._indent}:{key}: {val}")

    def _can_add(self, *keys) -> None:
        for key in keys:
            if key not in self._entry_args:
                continue
            if key not in self._fields:
                continue

            val = self._fields[key].value
            self._curr.append(f"{self._indent}:{key}: {val}")

    @staticmethod
    def build_file_header(title:str):
        lines = [".. -*- mode: ReST -*-",
                 f".. _{title}:", "",
                 "="*len(title), title, "="*len(title), "",
                 ".. contents:: Entries:",
                 "   :class: bib_entries",
                 "   :local:", "",
                 "For the raw bibtex, see `the file`_.", "",
                 f".. _`the file`: https://github.com/jgrey4296/bibliography/blob/main/main/{title}.bib", "", "",
                 ]
        return lines

    @staticmethod
    def get_rst_text(entry:Entry) -> list[str]:
        if not hasattr(entry, "_rst"):
            return []

        return entry._rst
