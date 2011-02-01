Unicode nightmare
=================

:ref:`Unicode` is the nightmare of many developers (and users) for different, and
sometimes good, reasons.

In the 1980's, only few people read documents in languages other than English
and their mother tongue. A computer supported only a small number of
languages, the user configured his region to support languages of close
countries. Memories and disks were expensive, all applications were written to
use byte strings: one byte per character was a good compromise.

Today with the Internet and the globalization, we all read and exchange
documents from everywhere around the world (even if we don't understand
everything). The problem is that documents rarely indicate their language
(encoding), and displaying a document with the wrong encoding leads to a well
known problem: :ref:`mojibake <mojibake>`.

It is difficult to get, or worse, guess the encoding of a document. Except for
modern encodings such as those in the UTF family (coming from the Unicode standard), there
is no reliable algorithm for that. We have to rely on statistics to guess the most
probable encoding. This is done by most Internet browsers, but few libraries
include such algorithm.

Unicode support by operating systems, programming languages and libraries
varies a lot. In general, the support is weak or non-existent. Each operating
system manages Unicode differently. For example, :ref:`Windows` stores filenames as Unicode,
whereas UNIX and BSD operating systems use bytes.

Mixing documents stored as bytes is possible, even if they use different
encodings, but leads to :ref:`mojibake <mojibake>`. Because libraries and programs do also ignore
encode and decode warnings or errors, write a single character with a diacritic
(any non :ref:`ASCII` character) is sometimes enough to get an error.

Full Unicode support is complex because the Unicode charset is bigger than any
other charset. For example, :ref:`ISO-8859-1` contains 256 codes including 191
characters, whereas Unicode (version 6.0) contains approximatively 245,000
assigned codes (see :ref:`Statistics`). The Unicode standard is larger than just a
charset: it explains also how to display characters (eg. left-to-right for
English and right-to-left for persian), how to normalize a character string
(eg. precomposed characters versus the decomposed form), etc.

This book explains how to sympathize with Unicode, and how you should modify
your program to avoid most, or all, issues related to encodings and Unicode.

