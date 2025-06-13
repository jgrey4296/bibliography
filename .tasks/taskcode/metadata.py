#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""
# ruff: noqa: F401
# Imports
from __future__ import annotations

import datetime
import logging as logmod
import pathlib as pl

import bibtexparser as BTP
from bibtexparser import middlewares as ms
import doot
import doot.errors
from doot.util.dkey import DKey, DKeyed
from doot.workflow import TaskSpec
import bibble as BM

##-- logging
logging = logmod.getLogger(__name__)
printer = logmod.getLogger("doot._printer")
fail_l  = printer.getChild("fail")
##-- end logging

@DKeyed.types("tasks")
def report_chosen_files(spec, state, tasks):
    printer.info("Chosen Files:")
    for x in tasks:
        path = x.extra.fpath
        printer.warning("%-20s : %s", pl.Path(path.parent.name) / path.name, datetime.datetime.fromtimestamp(path.stat().st_mtime))

class ApplyMetadataToLibrary(BM.metadata.MetadataApplicator):
    """ A Standalone Wrapper around the library-metadata MetadataApplicator
      """

    def __init__(self):
        super().__init__()

    @DKeyed.types("from", check=BTP.Library)
    @DKeyed.paths("backup")
    def __call__(self, spec ,state, _lib, _backup):
        self._backup = _backup
        for i, entry in enumerate(_lib.entries):
            printer.info("(%-4s/%-4s) Processing: %s", i, total, entry.key)
            self.transform_entry(entry, None)

        return { "failures" : self._failures }

class GenBibEntryTask:
    """
    Generate a task for each entry of a library
    """

    @DKeyed.types("from", check=BTP.Library)
    @DKeyed.formats("template")
    @DKeyed.taskname
    @DKeyed.redirects("update_")
    def __call__(self, spec , state, _lib, template, _basename, _update):
        subtasks : list[TaskSpec] = []
        for i, entry in enumerate(_lib.entries):
            # Build task spec
            spec = TaskSpec.build({
                "name": _basename.root(top=True).subtask(i, "bib", "entry"),
                "sources":[template],
                "entry":entry
                                  })
            subtasks.append(spec)

        return { _update : subtasks }
