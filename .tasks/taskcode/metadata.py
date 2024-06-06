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
fail_l  = printer.getChild("fail")
##-- end logging

import json
import jsonlines
import sh
import bibtexparser as BTP
from bibtexparser import middlewares as ms
import doot
import doot.errors
from doot.structs import DootKey
import bib_middleware as BM

exiftool = sh.exiftool
calibre  = sh.ebook_meta
qpdf     = sh.qpdf

@DootKey.kwrap.paths("lib-root")
@DootKey.kwrap.redirects("update_")
def build_metadata_parse_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without handling latex encoding """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(True),
        ms.RemoveEnclosingMiddleware(True),
        BM.files.PathReader(lib_root=_libroot),
        BM.metadata.IsbnValidator(True),
        BM.metadata.TagsReader(),
        BM.fields.TitleReader()
    ]
    return { _update : read_mids }


@DootKey.dec.types("tasks")
def report_chosen_files(spec, state, tasks):
    printer.info("Chosen Files:")
    for x in tasks:
        path = x.extra.fpath
        printer.warning("%-20s : %s", pl.Path(path.parent.name) / path.name, datetime.datetime.fromtimestamp(path.stat().st_mtime))


class ApplyMetadata(BM.metadata.MetadataApplicator):
    """ A Standalone Wrapper around the library-metadata MetadataApplicator
      """

    def __init__(self):
        super().__init__()

    @DootKey.kwrap.types("from", hint={"type_":BTP.Library})
    @DootKey.kwrap.paths("backup")
    def __call__(self, spec ,state, _lib, _backup):
        self._backup = _backup
        for i, entry in enumerate(_lib.entries):
            printer.info("(%-4s/%-4s) Processing: %s", i, total, entry.key)
            self.trasnform_entry(entry)

        return { "failures" : self._failures }

class GenMetadataTasks:
    """
      TODO Alternative implementation
      Iterate through each entry in a lib,
      and generate a taskspec, returning them
    """

    pass
