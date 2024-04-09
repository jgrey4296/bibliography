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

import json
import jsonlines
import libxmp
import pikepdf
import sh
import bibtexparser as BTP
from bibtexparser import middlewares as ms
import doot
import doot.errors
from doot.structs import DootKey
import bib_middleware as BM

exiftool = sh.exiftool
calibre  = sh.ebook_meta
qpdf     = sh.qpdf

@DootKey.kwrap.paths("lib-root")
@DootKey.kwrap.redirects("update_")
def build_metadata_parse_stack(spec, state, _libroot, _update):
    """ read and clean the file's entries, without handling latex encoding """
    read_mids = [
        BM.DuplicateHandler(),
        ms.ResolveStringReferencesMiddleware(True),
        ms.RemoveEnclosingMiddleware(True),
        BM.PathReader(lib_root=_libroot),
        BM.IsbnValidator(True),
        BM.TagsReader(),
        BM.TitleReader()
    ]
    return { _update : read_mids }

class ApplyMetadata:
    """ Apply metadata to files mentioned in bibtex entries
      uses xmp-prism tags and some custom ones for pdfs,
      and epub standard.
      """

    def __init__(self):
        pass

    @DootKey.kwrap.types("from", hint={"type_":BTP.Library})
    @DootKey.kwrap.paths("meta_backup")
    def __call__(self, spec ,state, _lib, _backup):
        for entry in _lib.entries:
            printer.info("Processing: %s", entry.key)
            match self._get_file(entry):
                case None:
                    pass
                case x if x.suffix == ".pdf" and not self._pdf_is_modifiable(x):
                    printer.warning("PDF is locked: %s", x)
                case x if self._metadata_matches_entry(x, entry):
                    printer.info("No Metadata Update Necessary: %s", x)
                case x if x.suffix == ".pdf":
                    self._backup_original_metadata(_backup, x)
                    self._update_pdf_by_exiftool(x, entry)
                    self._pdf_validate(x)
                    self._pdf_finalize(x)
                case x if x.suffix == ".epub":
                    self._backup_original_metadata(_backup, x)
                    self._update_epub_by_calibre(x, entry)
                case x:
                    printer.warning("Found a file that wasn't an epub or pdf: %s", x)

    def _get_file(self, entry) -> None|pl.Path:
        path = entry.fields_dict.get("file", None)
        if path is None:
            return None

        match path:
            case pl.Path():
                return path
            case BTP.model.Field() if isinstance(path.value, pl.Path) :
                return path.value
            case _:
                raise doot.errors.DootActionError("Bad File Path Type", path)

    def _update_pdf_by_exiftool(self, path, entry):
        # exiftool -{tag}="{content}" {file}
        # Build args:
        args   = []
        fields = entry.fields_dict

        # XMP-bib:
        args += [f'-bibtex={entry.raw}']
        args += ['-tags={}'.format(",".join(fields['tags'].value))]
        args += ['-Year={}'.format(fields['year'].value)]
        if 'isbn' in fields:
            args += ['-ISBN={}'.format(fields['isbn'].value)]

        # General
        title = fields['title'].value
        if 'subtitle' in fields:
            title += ": {}".format(fields['subtitle'].value)
        args += ['-title={}'.format(title)]
        args += ['-author={}'.format(fields['author'].value)]
        args += ['-Keywords={}'.format(",".join(fields['tags'].value))]

        if 'edition' in fields:
            args += ['-xmp-prism:edition={}'.format(fields['edition'].value)]
        if 'publisher' in fields:
            args += ["-publisher={}".format(fields['publisher'].value)]
        if 'url' in fields:
            args += ["-xmp-prism:link={}".format(fields['url'].value)]
        if 'doi' in fields:
            args += ['-xmp-prism:DOI={}'.format(fields['doi'].value)]
        if 'institution' in fields:
            args += ['-xmp-prism:organization=[}'.format(fields['institution'].value)]
        if 'issn' in fields:
            args += ['-xmp-prism:issn={}'.format(fields['issn'].value)]

        logging.debug("Pdf update args: %s : %s", path, args)
        # Call
        exiftool(*args, str(path))

    def _update_epub_by_calibre(self, path, entry):
        fields = entry.fields_dict
        args = []

        title = fields['title'].value
        if 'subtitle' in fields:
            title += ": {}".format(fields['subtitle'].value)
        args += ['--title={}'.format(title)]
        args += ['--authors={}'.format(fields['author'].value)]
        if 'publisher' in fields:
            args += ["--publisher={}".format(fields['publisher'].value)]
        if 'series' in fields:
            args += ["--series={}".format(fields['series'].value)]
        if 'number' in fields:
            args += ['--index={}'.format(fields['number'].value)]
        if 'volume' in fields:
            args += ['--index={}'.format(fields['volume'].value)]

        if 'isbn' in fields:
            args += ['--isbn={}'.format(fields['isbn'].value)]
        if 'doi' in fields:
            args += ['--identifier=doi:{}'.format(fields['doi'].value)]

        args += ['--tags={}'.format(",".join(fields['tags'].value))]
        args += ['--date={}'.format(fields['year'].value)]
        args += ['--comments={}'.format(entry.raw)]

        logging.debug("Ebook update args: %s : %s", path, args)
        calibre(str(path), *args)

    def _pdf_is_modifiable(self, path) -> bool:
        """ Test the pdf for encryption or password locking """
        try:
            cmd1 = qpdf("--is-encrypted", str(path), _ok_code=(2))
            cmd2 = qpdf("--requires-password", str(path), _ok_code=(2))
        except sh.ErrorReturnCode as err:
            return False

        return True

    def _pdf_validate(self, path) -> bool:
        # code 0 for fine,
        # writes to stderr for issues
        qpdf("--check", str(path))
        return True

    def _pdf_finalize(self, path):
        """ run qpdf --linearize,
          and delete the pdf_original if it exists """
        assert(path.suffix == ".pdf")
        logging.debug("Finalizing Pdf: {}", path)
        original = str(path)
        copied   = path.with_stem(path.stem + "_cp")
        backup   = path.with_suffix(".pdf_original")
        if copied.exists():
            raise doot.errors.DootActionError("the temp copy for linearization shouldn't already exist", original)

        path.rename(copied)

        qpdf(str(copied), "--linearize", original)

        if backup.exists():
            backup.unlink()
        copied.unlink()

    def _backup_original_metadata(self, archive, path):
        result = json.loads(exiftool("-J", str(path)))[0]
        with jsonlines.open(archive, mode='a') as f:
            f.write(result)

    def _metadata_matches_entry(self, path, entry) -> bool:
        result = json.loads(exiftool("-J", str(path)))[0]
        if 'Bibtex' not in result and 'Description' not in result:
            return False

        if result.get('Bibtex', None) == entry.raw:
            return True

        if result.get('Description', None) == entry.raw:
            return True

        return False
