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

import doot
import doot.errors
from doot.structs import DootKey

@DootKey.kwrap.types("bib_db")
@DootKey.kwrap.redirects("update_")
def get_db_files(spec, state, _db, _update):
    """ get all files mentioned in the bibtex database """
    filelist = []
    for entry in _db.entries:
        fields = entry.fields_dict
        filelist += {v.value for k,v in fields.items() if "file" in x}

    return { _update : filelist }


@DootKey.kwrap.types("bib")
@DootKey.kwrap.types("fs")
def diff_filelists(spec, state, _bib, _fs):
    """ diff the bibtex filelist against the filesystem filelist """
    bib_set        : set[str] = set(_bib)
    fs_set         : set[str] = set(_fs)
    only_mentioned : set[str] = set()
    only_exists    : set[str] = set()


    { "only_mentioned"  :  only_mentioned, "only_exists" : only_exists }
