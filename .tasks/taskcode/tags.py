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
import more_itertools as mitz
##-- end lib imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

import doot
import doot.errors
from doot.structs import DootKey, Keyed
from jgdv.files.tags import TagFile, SubstitutionFile
from bib_middleware.metadata import TagsReader

UPDATE_KEY = DootKey.build("update_")
FROM_KEY   = DootKey.build("from")
TO_KEY     = DootKey.build("to")

@Keyed.paths("from")
@Keyed.redirects("update_")
def read_tags(spec, state, _from, _update):
    tags = TagFile.read(_from)
    return { _update : tags }

@Keyed.paths("from")
@Keyed.redirects("update_")
def read_subs(spec, state, _target, _update):
    target_subs = SubstitutionFile.read(_target)
    return { _update : target_subs }

@Keyed.types("total", hint={"type_":TagFile})
@Keyed.types("known", hint={"type_":SubstitutionFile})
@Keyed.redirects("update_")
def calc_new_tags(spec, state, _total, _known, _update):
    new_tags = TagFile({x:1 for x in _total if not (_known.has_sub(x) or x in _known)})
    return { _update : new_tags }

@Keyed.types("known", hint={"type_":SubstitutionFile})
@Keyed.redirects("update_")
def calc_canon_tags(spec, state, _known, _update):
    canonical = _known.canonical()
    return { _update : canonical }

@Keyed.types("from", hint={"type_":TagFile})
@Keyed.redirects("update_")
def write_tag_set(spec, state, _from, _update):
    tag_str = str(_from)
    return { _update : tag_str}

# @Keyed.redirects("update_")
# def write_name_set(spec, state, _update):
#     result     = BM.NameWriter.names_to_str()
#     return { _update : result }

@Keyed.types("from", hint={"type_":list|set})
@Keyed.redirects("update_")
def merge_tagfiles(spec, state, _tagfiles, _update):
    merged = TagFile()
    for tf in _tagfiles:
        assert(isinstance(tf, TagFile))
        merged += tf

    return { _update : merged }

@Keyed.types("from", hint={"type_":list|set})
@Keyed.redirects("update_")
def merge_subfiles(spec, state, _from, _update):
    merged = SubstitutionFile()
    for tf in _from:
        merged += tf

    return { _update : merged }

@Keyed.redirects("update_")
def tags_from_middleware_to_state(spec, state, _update):
    """ Get the TagFile of tags read from the current lib, and insert it into state """

    return { _update : TagsReader._all_tags }
