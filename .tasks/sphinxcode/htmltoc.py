#!/usr/bin/env python3
"""

See EOF for license/metadata/notes as applicable
"""

from __future__ import annotations

##-- stdlib
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
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generator,
                    Generic, Iterable, Iterator, Mapping, Match,
                    MutableMapping, Protocol, Sequence, Tuple, TypeAlias,
                    TypeGuard, TypeVar, cast, final, overload,
                    runtime_checkable)
from uuid import UUID, uuid1

##-- end stdlib

##-- 3rd party
from sphinx.directives.other import TocTree
from sphinx.util.docutils import SphinxDirective
from sphinx.environment.collectors import EnvironmentCollector
from sphinx.util.fileutil import copy_asset
from docutils.parsers import Parser
from docutils.parsers.rst import directives
from docutils import nodes
from sphinx import addnodes
##-- end 3rd party

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

def setup(app):
    app.add_node(HtmlTocNode)
    app.add_directive("htmltoctree", HtmlTocTree)
    app.add_env_collector(HtmlTocCollector)

class HtmlTocTree(SphinxDirective):
    """ Toctree for Globbing existing html files """

    has_content               = True
    required_arguments        = 0
    optional_arguments        = 0
    final_argument_whitespace = False
    option_spec               = {
        'maxdepth': int,
        'name': directives.unchanged,
        'class': directives.class_option,
        'caption': directives.unchanged_required,
        'glob': directives.flag,
        'hidden': directives.flag,
        'includehidden': directives.flag,
        'numbered': int,
        'titlesonly': directives.flag,
        'reversed': directives.flag,
    }

    def run(self) -> list[Node]:
        subnode = HtmlTocNode()
        subnode['parent'] = self.env.docname

        # (title, ref) pairs, where ref may be a document, or an external link,
        # and title may be None if the document's title is to be used
        subnode['entries'] = []
        subnode['includefiles'] = []
        subnode['includehtml'] = []
        subnode['maxdepth'] = self.options.get('maxdepth', -1)
        subnode['caption'] = self.options.get('caption')
        subnode['glob'] = 'glob' in self.options
        subnode['hidden'] = 'hidden' in self.options
        subnode['includehidden'] = 'includehidden' in self.options
        subnode['numbered'] = self.options.get('numbered', 0)
        subnode['titlesonly'] = 'titlesonly' in self.options
        self.set_source_info(subnode)
        self.parse_content(subnode)

        wrappernode = nodes.compound(

            classes=['toctree-wrapper', *self.options.get('class', ())],
        )
        wrappernode.append(subnode)
        self.add_name(wrappernode)
        return [wrappernode]

    def parse_content(self, toctree) -> None:
        """
        Populate ``toctree['entries']`` and ``toctree['includefiles']`` from
        content.
        """
        assert('glob' in toctree)
        toctree['includehtml'] = []
        results = []
        cwd     = pl.Path.cwd()
        for entry in self.content:
            match entry:
                case str() if "*" in entry:
                    results += sorted(cwd.glob(entry))
                case str() if (path:= cwd / entry).exists():
                    results.append(path)
                case str():
                    print("Unknown Path: {}".format(entry))

            # copy_asset them to build dir whole
            # add links to toc for them

        print("Globbed Results: ({}) {}".format(len(results), results))
        for result in results:
            relative = result.relative_to(cwd)
            toctree['entries'].append((result.stem, str(relative)))
            toctree['includehtml'].append(str(result))

        print("htmlToctree Entries: {}".format(toctree['entries']))
        print("htmlToctree Includes: {}".format(toctree['includehtml']))

class HtmlTocNode(nodes.General, nodes.Element):
    pass

class HtmlTocCollector(EnvironmentCollector):

    def clear_doc(self, app: Sphinx, env: BuildEnvironment, docname: str) -> None:
        env.tocs.pop(docname, None)
        env.toc_secnumbers.pop(docname, None)
        env.toc_fignumbers.pop(docname, None)
        env.toc_num_entries.pop(docname, None)
        env.toctree_includes.pop(docname, None)
        env.glob_toctrees.discard(docname)
        env.numbered_toctrees.discard(docname)

        for subfn, fnset in list(env.files_to_rebuild.items()):
            fnset.discard(docname)
            if not fnset:
                del env.files_to_rebuild[subfn]

    def merge_other(
        self,
        app: Sphinx,
        env: BuildEnvironment,
        docnames: set[str],
        other: BuildEnvironment,
    ) -> None:
        for docname in docnames:
            env.tocs[docname] = other.tocs[docname]
            env.toc_num_entries[docname] = other.toc_num_entries[docname]
            if docname in other.toctree_includes:
                env.toctree_includes[docname] = other.toctree_includes[docname]
            if docname in other.glob_toctrees:
                env.glob_toctrees.add(docname)
            if docname in other.numbered_toctrees:
                env.numbered_toctrees.add(docname)

        for subfn, fnset in other.files_to_rebuild.items():
            env.files_to_rebuild.setdefault(subfn, set()).update(fnset & set(docnames))

    def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
        """Build a TOC from the doctree and store it in the inventory."""
        docname = app.env.docname
        numentries = [0]  # nonlocal again...

        def build_toc(
            node: Element | Sequence[Element],
            depth: int = 1,
        ) -> nodes.bullet_list | None:
            # list of table of contents entries
            entries: list[Element] = []
            for sectionnode in node:
                # find all toctree nodes in this section and add them
                # to the toc (just copying the toctree node which is then
                # resolved in self.get_and_resolve_doctree)
                if isinstance(sectionnode, nodes.section):
                    title = sectionnode[0]
                    # copy the contents of the section title, but without references
                    # and unnecessary stuff
                    visitor = SphinxContentsFilter(doctree)
                    title.walkabout(visitor)
                    nodetext = visitor.get_entry_text()  # type: ignore[no-untyped-call]
                    anchorname = _make_anchor_name(sectionnode['ids'], numentries)
                    # make these nodes:
                    # list_item -> compact_paragraph -> reference
                    reference = nodes.reference(
                        '',
                        '',
                        internal=True,
                        refuri=docname,
                        anchorname=anchorname,
                        *nodetext,
                    )
                    para = addnodes.compact_paragraph('', '', reference)
                    item: Element = nodes.list_item('', para)
                    sub_item = build_toc(sectionnode, depth + 1)
                    if sub_item:
                        item += sub_item
                    entries.append(item)
                # Wrap items under an ``.. only::`` directive in a node for
                # post-processing
                elif isinstance(sectionnode, addnodes.only):
                    onlynode = addnodes.only(expr=sectionnode['expr'])
                    blist = build_toc(sectionnode, depth)
                    if blist:
                        onlynode += blist.children
                        entries.append(onlynode)
                # check within the section for other node types
                elif isinstance(sectionnode, nodes.Element):
                    # cache of parent node -> list item
                    memo_parents: dict[nodes.Element, nodes.list_item] = {}
                    toctreenode: nodes.Node
                    for toctreenode in sectionnode.findall():
                        if isinstance(toctreenode, nodes.section):
                            continue
                        if isinstance(toctreenode, addnodes.toctree):
                            item = toctreenode.copy()
                            entries.append(item)
                            # important: do the inventory stuff
                            note_toctree(app.env, docname, toctreenode)
                        # add object signatures within a section to the ToC
                        elif isinstance(toctreenode, addnodes.desc):
                            # The desc has one or more nested desc_signature,
                            # and then a desc_content, which again may have desc nodes.
                            # Thus, desc is the one we can bubble up to through parents.
                            entry: nodes.list_item | None = None
                            for sig_node in toctreenode:
                                if not isinstance(sig_node, addnodes.desc_signature):
                                    continue
                                # Skip if no name set
                                if not sig_node.get('_toc_name', ''):
                                    continue
                                # Skip if explicitly disabled
                                if sig_node.parent.get('no-contents-entry'):
                                    continue
                                # Skip entries with no ID (e.g. with :no-index: set)
                                ids = sig_node['ids']
                                if not ids:
                                    continue

                                anchorname = _make_anchor_name(ids, numentries)

                                reference = nodes.reference(
                                    '',
                                    '',
                                    nodes.literal('', sig_node['_toc_name']),
                                    internal=True,
                                    refuri=docname,
                                    anchorname=anchorname,
                                )
                                para = addnodes.compact_paragraph(
                                    '', '', reference, skip_section_number=True
                                )
                                entry = nodes.list_item('', para)

                                # Find parent node
                                parent = sig_node.parent
                                while (
                                    parent not in memo_parents and parent != sectionnode
                                ):
                                    parent = parent.parent
                                # Note, it may both be the limit and in memo_parents,
                                # prefer memo_parents, so we get the nesting.
                                if parent in memo_parents:
                                    root_entry = memo_parents[parent]
                                    if isinstance(root_entry[-1], nodes.bullet_list):
                                        root_entry[-1].append(entry)
                                    else:
                                        root_entry.append(nodes.bullet_list('', entry))
                                else:
                                    assert parent == sectionnode
                                    entries.append(entry)

                            # Save the latest desc_signature as the one we put sub entries in.
                            # If there are multiple signatures, then the latest is used.
                            if entry is not None:
                                # are there any desc nodes without desc_signature nodes?
                                memo_parents[toctreenode] = entry

            if entries:
                return nodes.bullet_list('', *entries)
            return None

        toc = build_toc(doctree)
        if toc:
            app.env.tocs[docname] = toc
        else:
            app.env.tocs[docname] = nodes.bullet_list('')
        app.env.toc_num_entries[docname] = numentries[0]

    def get_updated_docs(self, app: Sphinx, env: BuildEnvironment) -> list[str]:
        return self.assign_section_numbers(env) + self.assign_figure_numbers(env)

    def assign_section_numbers(self, env: BuildEnvironment) -> list[str]:
        """Assign a section number to each heading under a numbered toctree."""
        # a list of all docnames whose section numbers changed
        rewrite_needed = []

        assigned: set[str] = set()
        old_secnumbers = env.toc_secnumbers
        env.toc_secnumbers = {}

        def _walk_toc(
            node: Element,
            secnums: dict[str, tuple[int, ...]],
            depth: int,
            titlenode: nodes.title | None = None,
        ) -> None:
            # titlenode is the title of the document, it will get assigned a
            # secnumber too, so that it shows up in next/prev/parent rellinks
            for subnode in node.children:
                if isinstance(subnode, nodes.bullet_list):
                    numstack.append(0)
                    _walk_toc(subnode, secnums, depth - 1, titlenode)
                    numstack.pop()
                    titlenode = None
                elif isinstance(subnode, nodes.list_item):  # NoQA: SIM114
                    _walk_toc(subnode, secnums, depth, titlenode)
                    titlenode = None
                elif isinstance(subnode, addnodes.only):
                    # at this stage we don't know yet which sections are going
                    # to be included; just include all of them, even if it leads
                    # to gaps in the numbering
                    _walk_toc(subnode, secnums, depth, titlenode)
                    titlenode = None
                elif isinstance(subnode, addnodes.compact_paragraph):
                    if 'skip_section_number' in subnode:
                        continue
                    numstack[-1] += 1
                    reference = cast(nodes.reference, subnode[0])
                    if depth > 0:
                        number = numstack.copy()
                        secnums[reference['anchorname']] = tuple(numstack)
                    else:
                        number = None
                        secnums[reference['anchorname']] = ()
                    reference['secnumber'] = number
                    if titlenode:
                        titlenode['secnumber'] = number
                        titlenode = None
                elif isinstance(subnode, addnodes.toctree):
                    _walk_toctree(subnode, depth)

        def _walk_toctree(toctreenode: addnodes.toctree, depth: int) -> None:
            if depth == 0:
                return
            for _title, ref in toctreenode['entries']:
                if url_re.match(ref) or ref == 'self':
                    # don't mess with those
                    continue
                if ref in assigned:
                    logger.warning(
                        __(
                            '%s is already assigned section numbers '
                            '(nested numbered toctree?)'
                        ),
                        ref,
                        location=toctreenode,
                        type='toc',
                        subtype='secnum',
                    )
                elif ref in env.tocs:
                    secnums: dict[str, tuple[int, ...]] = {}
                    env.toc_secnumbers[ref] = secnums
                    assigned.add(ref)
                    _walk_toc(env.tocs[ref], secnums, depth, env.titles.get(ref))
                    if secnums != old_secnumbers.get(ref):
                        rewrite_needed.append(ref)

        for docname in env.numbered_toctrees:
            assigned.add(docname)
            doctree = env.get_doctree(docname)
            for toctreenode in doctree.findall(addnodes.toctree):
                depth = toctreenode.get('numbered', 0)
                if depth:
                    # every numbered toctree gets new numbering
                    numstack = [0]
                    _walk_toctree(toctreenode, depth)

        return rewrite_needed

    def assign_figure_numbers(self, env: BuildEnvironment) -> list[str]:
        """Assign a figure number to each figure under a numbered toctree."""
        generated_docnames = frozenset(env.domains.standard_domain._virtual_doc_names)

        rewrite_needed = []

        assigned: set[str] = set()
        old_fignumbers = env.toc_fignumbers
        env.toc_fignumbers = {}
        fignum_counter: dict[str, dict[tuple[int, ...], int]] = {}

        def get_figtype(node: Node) -> str | None:
            for domain in env.domains.sorted():
                figtype = domain.get_enumerable_node_type(node)
                if isinstance(domain, StandardDomain) and not domain.get_numfig_title(
                    node
                ):
                    # Skip if uncaptioned node
                    continue

                if figtype:
                    return figtype

            return None

        def get_section_number(docname: str, section: nodes.section) -> tuple[int, ...]:
            anchorname = '#' + section['ids'][0]
            secnumbers = env.toc_secnumbers.get(docname, {})
            if anchorname in secnumbers:
                secnum = secnumbers.get(anchorname)
            else:
                secnum = secnumbers.get('')

            return secnum or ()

        def get_next_fignumber(
            figtype: str, secnum: tuple[int, ...]
        ) -> tuple[int, ...]:
            counter = fignum_counter.setdefault(figtype, {})

            secnum = secnum[: env.config.numfig_secnum_depth]
            counter[secnum] = counter.get(secnum, 0) + 1
            return (*secnum, counter[secnum])

        def register_fignumber(
            docname: str, secnum: tuple[int, ...], figtype: str, fignode: Element
        ) -> None:
            env.toc_fignumbers.setdefault(docname, {})
            fignumbers = env.toc_fignumbers[docname].setdefault(figtype, {})
            figure_id = fignode['ids'][0]

            fignumbers[figure_id] = get_next_fignumber(figtype, secnum)

        def _walk_doctree(
            docname: str, doctree: Element, secnum: tuple[int, ...]
        ) -> None:
            nonlocal generated_docnames
            for subnode in doctree.children:
                if isinstance(subnode, nodes.section):
                    next_secnum = get_section_number(docname, subnode)
                    if next_secnum:
                        _walk_doctree(docname, subnode, next_secnum)
                    else:
                        _walk_doctree(docname, subnode, secnum)
                elif isinstance(subnode, addnodes.toctree):
                    for _title, subdocname in subnode['entries']:
                        if url_re.match(subdocname) or subdocname == 'self':
                            # don't mess with those
                            continue
                        if subdocname in generated_docnames:
                            # or these
                            continue

                        _walk_doc(subdocname, secnum)
                elif isinstance(subnode, nodes.Element):
                    figtype = get_figtype(subnode)
                    if figtype and subnode['ids']:
                        register_fignumber(docname, secnum, figtype, subnode)

                    _walk_doctree(docname, subnode, secnum)

        def _walk_doc(docname: str, secnum: tuple[int, ...]) -> None:
            if docname not in assigned:
                assigned.add(docname)
                doctree = env.get_doctree(docname)
                _walk_doctree(docname, doctree, secnum)

        if env.config.numfig:
            _walk_doc(env.config.root_doc, ())
            for docname, fignums in env.toc_fignumbers.items():
                if fignums != old_fignumbers.get(docname):
                    rewrite_needed.append(docname)

        return rewrite_needed


class HtmlParser(Parser):

    supported = ("html")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, inputstring, document) -> None:
        """Parse `inputstring` and populate `document`, a document tree."""
        self.setup_parse(inputstring, document)
        # provide fallbacks in case the document has only generic settings
        self.document.settings.setdefault('tab_width', 8)
        self.document.settings.setdefault('syntax_highlight', 'long')
        self.statemachine = states.RSTStateMachine(
              state_classes=self.state_classes,
              initial_state=self.initial_state,
              debug=document.reporter.debug_flag)
        inputlines = docutils.statemachine.string2lines(
              inputstring, tab_width=document.settings.tab_width,
              convert_whitespace=True)
        for i, line in enumerate(inputlines):
            if len(line) > self.document.settings.line_length_limit:
                error = self.document.reporter.error(
                            'Line %d exceeds the line-length-limit.'%(i+1))
                self.document.append(error)
                break
        else:
            self.statemachine.run(inputlines, document, inliner=self.inliner)
        # restore the "default" default role after parsing a document
        if '' in roles._roles:
            del roles._roles['']
        self.finish_parse()
