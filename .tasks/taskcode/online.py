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

printer = logmod.getLogger("doot._printer")

from waybackpy import WaybackMachineSaveAPI
import bib_middleware as BM
import bibtexparser as BTP
from bibtexparser import middlewares as ms

import doot
import doot.errors
from doot.structs import DKey, DKeyed
from doot.enums import ActionResponse_e
from jgdv.files.tags import TagFile
from jgdv.files.bookmarks import BookmarkCollection

FF_DRIVER          = "__$ff_driver"
READER_PREFIX      = "about:reader?url="
LOAD_TIMEOUT       = 2
WAYBACK_USER_AGENT = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

import bib_middleware as BM

def shutdown_firefox(spec, state):
    BM.files.OnlineDownloader.close_firefox()


@DKeyed.paths("lib-root", "online_saves")
@DKeyed.redirects("update_")
def build_online_downloader_parse_stack(spec, state, _libroot, _dltarget, _update):
    """ downloads urls as pdfs if entry is 'online' and it doesn't have a file associated already """
    read_mids = [
        BM.metadata.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(),
        ms.RemoveEnclosingMiddleware(),
        BM.files.PathReader(lib_root=_libroot),
        BM.files.OnlineDownloader(target=_dltarget),
    ]
    return { _update : read_mids}


@DKeyed.paths("lib-root")
@DKeyed.redirects("update_")
def build_online_downloader_write_stack(spec, state, _libroot, _update):
    """ Doesn't encode into latex """
    write_mids = [
        BM.files.PathWriter(lib_root=_libroot),
        ms.AddEnclosingMiddleware(allow_inplace_modification=False, default_enclosing="{", reuse_previous_enclosing=False, enclose_integers=True),
    ]
    return { _update : write_mids}
