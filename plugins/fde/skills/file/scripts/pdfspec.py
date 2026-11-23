#!/usr/bin/env python3
"""Shared layer-1 machinery: page-anchored, header-stripped document model."""
import os, re, subprocess, hashlib, csv as _csv

# Engagement root. Defaults to the current working directory, which is
# the engagement folder when a driver script is run from there.
ROOT = os.environ.get("ENGAGEMENT_ROOT", os.getcwd())

CAP_RE  = re.compile(r'^\s*(?:Table|Figure)\s+(\d+\.\d+)\b')
HEAD_RE = re.compile(r'^\s{0,6}(\d+\.\d+(?:\.\d+)?)\s+[A-Z]')
CHAP_RE = re.compile(r'^\s*CHAPTER\s+\d+\s*[:.]', re.I)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pdftext(src, first=None, last=None):
    cmd = ["pdftotext", "-layout"]
    if first:
        cmd += ["-f", str(first), "-l", str(last or first)]
    cmd += [os.path.join(ROOT, src), "-"]
    return subprocess.run(cmd, capture_output=True, check=True).stdout.decode('utf-8', 'replace')


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def columnar(ln):
    return bool(ln.strip()) and len(re.split(r'\s{2,}', ln.strip())) >= 2


def build_doc(src, npages, header_test, footer_re):
    """Return (doc, hdr_variants, ftr_variants).
    doc is a flat list of (pdfpage, line, is_page_start) with furniture removed.
    hdr/ftr variants are keyed by their text with whitespace runs collapsed, and each holds one
    verbatim exemplar plus the pages it appears on. Only the stripped furniture is grouped this
    way; body text is never normalised."""
    parts = pdftext(src).split('\f')
    if len(parts) > npages and parts[-1].strip() == '':
        parts = parts[:-1]
    assert len(parts) == npages, (len(parts), npages)
    doc, hdrs, ftrs = [], {}, {}
    for pno, page in enumerate(parts, 1):
        lines = page.split('\n')
        j = 0
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and header_test(lines[j]):
            k = j
            while k < len(lines) and lines[k].strip():
                k += 1
            blk = '\n'.join(lines[j:k])
            hdrs.setdefault(re.sub(r'[ \t]+', ' ', blk).strip(), [blk, []])[1].append(pno)
            lines = lines[k:]
        k = len(lines)
        while k > 0 and not lines[k - 1].strip():
            k -= 1
        if k > 0 and footer_re.match(lines[k - 1]):
            raw_ftr = lines[k - 1].rstrip()
            m = footer_re.match(raw_ftr)
            ftr = (raw_ftr[:m.start(1)] + '<PAGE>' + raw_ftr[m.end(1):]) if m.group(1) else raw_ftr
            ftrs.setdefault(re.sub(r'[ \t]+', ' ', ftr).strip(), [ftr, []])[1].append(pno)
            lines = lines[:k - 1]
        a, b = 0, len(lines)
        while a < b and not lines[a].strip():
            a += 1
        while b > a and not lines[b - 1].strip():
            b -= 1
        first = True
        for ln in lines[a:b]:
            doc.append((pno, ln, first))
            first = False
        if a >= b:                      # page with no body at all
            doc.append((pno, '', True))
    return doc, hdrs, ftrs


def find_boundary(doc, pdfpage, pattern):
    rx = re.compile(pattern)
    for i, (pg, ln, _) in enumerate(doc):
        if pg == pdfpage and rx.match(ln):
            return i
    raise LookupError("boundary not found: pdf %s %r" % (pdfpage, pattern))


def compress(pgs):
    pgs = sorted(set(pgs))
    out, s, p = [], pgs[0], pgs[0]
    for x in pgs[1:]:
        if x == p + 1:
            p = x
            continue
        out.append(str(s) if s == p else "%d-%d" % (s, p))
        s = p = x
    out.append(str(s) if s == p else "%d-%d" % (s, p))
    return ", ".join(out)


def table_block(seq, start):
    """seq is a list of (pdfpage, line). Collect a table's ASCII block."""
    out = [seq[start]]
    seen_col = False
    lead_nonco = nonco = blanks = 0
    i = start + 1
    while i < len(seq) and len(out) < 400:
        pg, ln = seq[i]
        if CAP_RE.match(ln) or CHAP_RE.match(ln):
            break
        if seen_col and HEAD_RE.match(ln):
            break
        if not ln.strip():
            blanks += 1
            if seen_col and blanks >= 3:
                break
        elif columnar(ln):
            blanks = nonco = 0
            seen_col = True
        else:
            blanks = 0
            if seen_col:
                nonco += 1
                if nonco >= 12:
                    break
            else:
                lead_nonco += 1
                if lead_nonco >= 20:
                    break
        out.append((pg, ln))
        i += 1
    while len(out) > 1 and not columnar(out[-1][1]):
        out.pop()
    return out


def resolve_csv(block):
    rows = []
    for pg, ln in block[1:]:
        if not ln.strip():
            continue
        rows.append([f.strip() for f in re.split(r'\s{2,}', ln.strip())])
    if len(rows) < 2:
        return None
    n = len(rows[0])
    if n < 2 or any(len(r) != n for r in rows):
        return None
    return rows


def render_page(src, pdfpage, outdir, stem, dpi=150):
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(["pdftoppm", "-f", str(pdfpage), "-l", str(pdfpage), "-r", str(dpi),
                    "-png", "-singlefile", os.path.join(ROOT, src),
                    os.path.join(outdir, stem)], check=True)
    return stem + ".png"


def write_csv(path, rows):
    with open(path, "w", encoding="utf-8", newline='') as fh:
        w = _csv.writer(fh)
        for r in rows:
            w.writerow(r)
