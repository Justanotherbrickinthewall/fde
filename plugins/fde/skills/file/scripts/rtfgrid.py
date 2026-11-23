#!/usr/bin/env python3
"""Minimal RTF reader that recovers table grids from textutil output."""
import re

SKIP_DEST = {'fonttbl', 'colortbl', 'stylesheet', 'info', 'pict', 'object', 'themedata',
             'colorschememapping', 'datastore', 'latentstyles', 'listtable', 'listoverridetable',
             'rsidtbl', 'generator', 'xmlnstbl', 'filetbl', 'header', 'footer', 'footnote',
             'expandedcolortbl', 'defchp', 'defpap'}
SPECIAL = {'line': '\n', 'tab': '\t', 'emdash': '\u2014', 'endash': '\u2013',
           'lquote': '\u2018', 'rquote': '\u2019', 'ldblquote': '\u201c', 'rdblquote': '\u201d',
           'bullet': '\u2022', 'nbsp': '\xa0'}

TOKEN = re.compile(r"\\([a-zA-Z]+)(-?\d+)? ?|\\'([0-9a-fA-F]{2})|\\(.)|([{}])|([^\\{}]+)", re.S)


def parse(rtf):
    """Yield ('row', {'itap': depth, 'cells': [(text, (hmerged, vmerge_start,
    vmerge_cont))]}) and ('par', text) in document order.

    A block on the form is marked by vertical merge, not by blank cells:
    `\\clvmgf` starts one and `\\clvmrg` continues it. Dropping those left
    every block span in the wiki to be inferred rather than read. `\\itap`
    is the table nesting depth; this document flattens its nested tables so
    it reads 1 throughout, but other document families will nest.
    """
    out = []
    depth = 0
    skip_to = None
    buf = []
    cells = []
    in_tbl = False
    celldefs = []
    vmgfdefs = []
    vmrgdefs = []
    pending_merge = False
    pending_vmgf = False
    pending_vmrg = False
    itap = 0
    for m in TOKEN.finditer(rtf):
        cw, arg, hexv, sym, brace, text = m.groups()
        if brace == '{':
            depth += 1
            continue
        if brace == '}':
            if skip_to is not None and depth <= skip_to:
                skip_to = None
            depth -= 1
            continue
        if skip_to is not None:
            continue
        if cw:
            if cw in SKIP_DEST:
                skip_to = depth
                continue
            if cw in SPECIAL:
                buf.append(SPECIAL[cw])
            elif cw == 'u':
                try:
                    buf.append(chr(int(arg) % 65536))
                except (TypeError, ValueError):
                    pass
            elif cw == 'clmrg':
                pending_merge = True
            elif cw == 'clvmgf':
                pending_vmgf = True
            elif cw == 'clvmrg':
                pending_vmrg = True
            elif cw == 'itap':
                try:
                    itap = int(arg)
                except (TypeError, ValueError):
                    pass
            elif cw == 'cellx':
                celldefs.append(pending_merge)
                vmgfdefs.append(pending_vmgf)
                vmrgdefs.append(pending_vmrg)
                pending_merge = pending_vmgf = pending_vmrg = False
            elif cw == 'intbl':
                in_tbl = True
            elif cw == 'cell':
                cells.append(''.join(buf).strip())
                buf = []
            elif cw == 'row':
                if cells:
                    n = len(cells)
                    hflags = (celldefs + [False] * n)[:n]
                    gflags = (vmgfdefs + [False] * n)[:n]
                    rflags = (vmrgdefs + [False] * n)[:n]
                    row_cells = list(zip(cells, zip(hflags, gflags, rflags)))
                    out.append(('row', {'itap': itap, 'cells': row_cells}))
                cells, celldefs, vmgfdefs, vmrgdefs, in_tbl = [], [], [], [], False
                itap = 0
            elif cw in ('par', 'sect'):
                # A cell can hold more than one paragraph — a consultant's
                # block on a form is often name, address and certificate
                # number as three. Mid-cell that is a line break to keep, not a
                # document paragraph to flush; the old code cleared `buf`
                # either way and silently dropped every line but the last.
                if in_tbl:
                    buf.append('\n')
                else:
                    out.append(('par', ''.join(buf).strip()))
                    buf = []
            elif cw == 'trowd':
                celldefs, vmgfdefs, vmrgdefs = [], [], []
                pending_merge = pending_vmgf = pending_vmrg = False
                itap = 0
        elif hexv:
            buf.append(bytes([int(hexv, 16)]).decode('cp1252', 'replace'))
        elif sym:
            if sym == '*':
                skip_to = depth
            elif sym == '\n':
                # RTF spec: a backslash followed by a literal CR/LF means
                # \par. Same fix as the \par branch above.
                if in_tbl:
                    buf.append('\n')
                else:
                    out.append(('par', ''.join(buf).strip()))
                    buf = []
            elif sym in ('\\', '{', '}'):
                buf.append(sym)
        elif text:
            buf.append(text.replace('\n', '').replace('\r', ''))
    t = ''.join(buf).strip()
    if t:
        out.append(('par', t))
    return out
