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

FF_DRIVER          = "__$ff_driver"
READER_PREFIX      = "about:reader?url="
LOAD_TIMEOUT       = 2
WAYBACK_USER_AGENT = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

def shutdown_firefox(spec, state):
    BM.files.OnlineDownloader.close_firefox()

# @DKeyed.types("entry")
# @DKeyed.formats("box")
# def link_check(spec, state, entry, box):
#     match entry.fields_dict.get("url", None):
#         case None:
#             return
#         case x:
#             printer.info("Checking Url: %s", x.value)
#             ## check
#             check_result = True
#             if not check_result:
#                 box = TaskName(box)
#                 _DootPostBox.put(box, x.value)
