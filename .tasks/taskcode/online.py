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

from waybackpy import WaybackMachineSaveAPI
import bibble as BM
import bibtexparser as BTP
from bibtexparser import middlewares as ms

from jgdv.structs.dkey import DKeyed
import doot
import doot.errors
from doot.structs import TaskName
from doot.enums import ActionResponse_e
from jgdv.files.tags import TagFile
from jgdv.files.bookmarks import BookmarkCollection
import bibble as BM

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
##-- end logging

def shutdown_firefox(spec, state):
    BM.files.OnlineDownloader.close_firefox()
