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
from doot.structs import DootKey
from dootle.tags.structs import TagFile, SubstitutionFile

UPDATE_KEY = DootKey.make("update_")
FROM_KEY   = DootKey.make("from")
TO_KEY     = DootKey.make("to")


class ReadSubs:
    _total = SubstitutionFile()

    def __call__(self, spec, state):
        target  = FROM_KEY.to_path(spec, state)

        target_subs = SubstitutionFile.read(target)
        ReadSubs._total.update(target_subs)


def write_known(spec, state):
    target  = TO_KEY.to_path(spec, state)
    total   = set()
    for tag in ReadSubs._total:
        total.update(ReadSubs._total.sub(tag))

    target.write_text("\n".join(sorted(total)))

def write_new(spec, state):
    total   = FROM_KEY.to_type(spec, state, type_=TagFile)
    known   = ReadSubs._total

    new_tags = {x for x in total if not (known.has_sub(x) or x in known)}

    target  = TO_KEY.to_path(spec, state)
    target.write_text("\n".join(sorted(new_tags)))



"""


"""

def read_tags(spec, state):
    update = UPDATE_KEY.redirect(spec)
    target = FROM_KEY.to_path(spec, state)

    tags = TagFile.read(target)

    return { update : tags }
