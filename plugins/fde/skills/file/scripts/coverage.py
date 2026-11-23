#!/usr/bin/env python3
"""Coverage gate: every substantive source line must appear in the staged specimen."""
import re, sys, os, subprocess, glob

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def staged_text(paths):
    blob = []
    for p in paths:
        t = open(p, encoding='utf-8').read()
        t = t.split('---\n', 2)[-1]          # drop front matter
        for chunk in re.findall(r'```text\n(.*?)```', t, re.S):
            blob.append(chunk)
    return set(norm(l) for l in '\n'.join(blob).split('\n') if norm(l))

def check(src_lines, staged, minlen=45, skip=()):
    missing = []
    for pg, ln in src_lines:
        n = norm(ln)
        if len(n) < minlen:
            continue
        if any(s in n for s in skip):
            continue
        if n not in staged:
            missing.append((pg, n))
    total = sum(1 for pg, ln in src_lines
                if len(norm(ln)) >= minlen and not any(s in norm(ln) for s in skip))
    return total, missing
