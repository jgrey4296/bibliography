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
        BM.metadata.TagsWriter(),
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids }
