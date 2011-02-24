#!/usr/bin/env python
#coding:utf8
import io
import os
import shutil
import subprocess
import sys

rebuild = True

path = os.path.join("build", "latex")

if rebuild:
    if os.path.exists(path):
        shutil.rmtree(path)

    # TODO: encodings:: column or row spanning cells are not yet implemented.
    tableBefore = os.linesep.join((
        u"+--------------------------------------------------------+------------------------------------------+",
        u"| Character                                              | Replaced by                              |",
    ))
    tableAfter = os.linesep.join((
        u"+--------------------------------------------+-----------+---------+--------------------------------+",
        u"| Character                                  |           |         | Replaced by                    |",
    ))

    with io.open("encodings.rst", encoding="utf-8") as fp:
        encodings = fp.read()

    try:
        with io.open("encodings.rst", "w", encoding="utf-8") as fp:
            fp.write(encodings.replace(tableBefore, tableAfter))

        shutil.copyfile("encodings.rst", "encodings.rst.new")

        ret = subprocess.call(("make", "latex"))
    finally:
        with io.open("encodings.rst", "w", encoding="utf-8") as fp:
            fp.write(encodings)
    if ret != 0:
        sys.exit(ret)

os.chdir(path)
with io.open("programming_with_unicode.tex", encoding="utf-8") as fp:
    content = fp.read()

DUlineblock = os.linesep.join((
    ur"\begin{DUlineblock}{0em}",
    ur"\item[] ",
    ur"\end{DUlineblock}",
))

REPLACE = (
    (u"\\usepackage[T1]{fontenc}", u"\\usepackage[T1,T2A]{fontenc}"),
    (u"\\usepackage{babel}", u"\\usepackage[english,russian]{babel}"),
    # TODO: ! Package inputenc Error: Unicode char \u8:� not set up for use with LaTeX.
    # TODO: ! Package textcomp Error: Symbol \textcurrency not provided by
    #       (textcomp)                font family ptm in TS1 encoding.
    #       (textcomp)                Default family used instead.
    # Try: \usepackage[force,almostfull]{textcomp}
    (u"�", u"<?>"),
    (u"¤", u"<X>"),
    (u" \u0327", u","),
    (DUlineblock, u"|"),
    (u"я\u0301", u"я"),
    # TODO: ! LaTeX Error: Command \DH unavailable in encoding T2A.
    # TODO: ! LaTeX Error: Command \TH unavailable in encoding T2A.
    # TODO: ! LaTeX Error: Command \dh unavailable in encoding T2A.
    # TODO: ! LaTeX Error: Command \th unavailable in encoding T2A.
    (u"Ð", u"D"),
    (u"ð", u"d"),
    (u"Þ", u"P"),
    (u"þ", u"p"),
)
for before, after in REPLACE:
    content = content.replace(before, after)

with io.open("programming_with_unicode.tex", "w", encoding="utf-8") as fp:
    fp.write(content)

ret = subprocess.call(("make", "all-pdf", "clean"))
if ret != 0:
    sys.exit(ret)

