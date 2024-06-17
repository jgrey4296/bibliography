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
##-- end logging

import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.structs import DootKey, Keyed
import bib_middleware as BM



@Keyed.paths("lib-root")
@Keyed.redirects("update_")
def build_backup_parse_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without handling latex encoding """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(True),
        ms.RemoveEnclosingMiddleware(True),
        BM.files.PathReader(lib_root=_libroot),
    ]
    return { _update : read_mids }


@Keyed.types("from", hint={"type_":BTP.Library})
@Keyed.redirects("update_")
def get_files(spec, state, _lib, _update):
    files = []
    for entry in _lib.entries:
        files += [x.value for x in entry.fields if "file" in x.key]

    return { _update : files }
