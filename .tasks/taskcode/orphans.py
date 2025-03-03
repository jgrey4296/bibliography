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

import doot
import doot.errors
from doot.structs import DKey, DKeyed, TaskName
from doot.actions.postbox import _DootPostBox

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

@DKeyed.types("bib_db")
@DKeyed.redirects("update_")
def get_db_files(spec, state, _db, _update):
    """ get all files mentioned in the bibtex database """
    filelist = set()
    for entry in _db.entries:
        fields = entry.fields_dict
        filelist.update({v.value for k,v in fields.items() if "file" in k})

    return { _update : filelist }

@DKeyed.types("bib")
@DKeyed.types("fs")
def diff_filelists(spec, state, _bib, _fs):
    """ a simple diff of the bibtex filelist against the filesystem filelist """
    bib_set        : set[str] = set(x.strip() for x in _bib)
    fs_set         : set[str] = set(x.strip() for x in _fs)
    only_mentioned : set[str] = bib_set.difference(fs_set)
    only_exists    : set[str] = fs_set.difference(bib_set)
    printer.info("Difference:")
    printer.info("Mentioned : %s -|- %s Exists", len(only_mentioned), len(only_exists))
    return { "only_mentioned"  :  "\n".join(only_mentioned), "only_exists" : "\n".join(only_exists) }

@DKeyed.types("from")
@DKeyed.redirects("update")
def format_filelist(spec, state, _files, _update):
    result = "\n".join(sorted(str(x) for x in _files))
    return { _update : result }

@DKeyed.types("entry")
@DKeyed.formats("box")
def get_orphans(spec, state, entry, box):
    """
      Check then entry's files all exist.
      add to the target postbox if it doesn't
    """
    match entry.fields_dict.get("orphaned", None):
        case None:
            pass
        case x:
            printer.info("Orphan Reference found: %s", x.key)
            box = TaskName(box)
            _DootPostBox.put(box, x.key)
