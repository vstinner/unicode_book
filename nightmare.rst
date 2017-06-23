Unicode nightmare
=================

:ref:`Unicode <unicode>` is the nightmare of many developers (and users) for
different, and sometimes good reasons.

In the 1980s, only few people read documents in languages other their mother
tongue and English. A computer supported only a small number of
languages, the user configured his region to support languages of close
countries. Memories and disks were expensive, all applications were written to
use :ref:`byte strings <bytes>` using 8 bits encodings: one byte per character
was a good compromise.

Today with the Internet and the globalization, we all read and exchange
documents from everywhere around the world (even if we don't understand
everything). The problem is that documents rarely indicate their language
(encoding), and displaying a document with the wrong encoding leads to a well
known problem: :ref:`mojibake <mojibake>`.

It is difficult to get, or worse, :ref:`guess the encoding <guess>` of a document. Except for
encodings of the UTF family (coming from the Unicode standard), there
is no reliable algorithm for that. We have to rely on statistics to guess the most
probable encoding, which is done by most Internet browsers.

:ref:`Unicode support <support>` by :ref:`operating systems <oses>`,
:ref:`programming languages <prog>` and :ref:`libraries <libs>` varies a lot.
In general, the support is basic or non-existent. Each operating system manages
Unicode differently. For example, :ref:`Windows` stores :ref:`filenames <filename>` as Unicode,
whereas UNIX and BSD operating systems use bytes.

Mixing documents stored as bytes is possible, even if they use different
encodings, but leads to :ref:`mojibake <mojibake>`. Because libraries and programs do also ignore
encode and decode :ref:`warnings or errors <errors>`, writing a single character with a diacritic
(any non-:ref:`ASCII` character) is sometimes enough to get an error.

Full Unicode support is complex because the Unicode charset is bigger than any
other charset. For example, :ref:`ISO-8859-1` contains 256 code points including 191
characters, whereas Unicode version 6.0 contains :ref:`248,966
assigned code points <unicode stats>`. The Unicode standard is larger than just a
charset: it also explains how to display characters (e.g. left-to-right for
English and right-to-left for persian), how to :ref:`normalize <normalization>` a :ref:`character string <str>`
(e.g. precomposed characters versus the decomposed form), etc.

This book explains how to sympathize with Unicode, and how you should modify
your program to avoid most, or all, issues related to encodings and Unicode.

