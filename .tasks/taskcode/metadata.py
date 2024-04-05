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

import sh
import bibtexparser as BTP
import doot
import doot.errors
from doot.structs import DootKey

exiftool = sh.exiftool
pdftk    = sh.pdftk
calibre  = sh.ebook_meta


class ApplyMetadata:
    """ Apply metadata to files mentioned in bibtex entries  """

    def __init__(self):
        pass

    @DootKey.kwrap.types("from", hint={"type":BTP.Library})
    def __call__(self, spec ,state, _lib):
        for entry in _lib.entrys:
            match self._get_file(entry):
                case None:
                    pass
                case x if x.suffix == ".pdf":
                    pass
                case x if x.suffix == ".epub":
                    pass
                case x:
                    printer.warning("Found a file that wasn't an epub or pdf: %s", x)

    def _get_file(self, entry) -> None|pl.Path:
        path = entry.field_dict.get("file", None)
        if path is None:
            return None

        match path:
            case pl.Path():
                return path
            case _:
                raise doot.errors.DootActionError("Bad File Path Type", path)


    def _update_pdf_by_exiftool(self, path, entry):
        pass

    def _update_pdf_by_pdftk(self, path, entry):
        pass

    def _update_pdf_by_calibre(self, path, entry):
        pass

    def _update_epub_by_calibre(self, path, entry):
        pass
