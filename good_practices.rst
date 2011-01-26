Good practices
==============

Rules
-----

To limit or avoid issues with Unicode, try to follow these rules:

 * decode all bytes data as early as possible: keyboard strokes, files, data
   received from the network, ...
 * encode back Unicode to bytes as late as possible: write text to a file,
   log a message, send data to the network, ...
 * always store and manipulate text as character strings
 * if you have to encode text and you can choose the encoding: prefer the :ref:`UTF-8` encoding.
   It is able to encode all Unicode 6.0 characters (including :ref:`non-BMP
   characters <bmp>`), has no endian issue, and is well support by most
   programs.

Unicode support levels
----------------------

There are different levels of Unicode support:

 * 0 - no Unicode support: only work correctly if all inputs and outputs are
   encoded to the same encoding, usually the :ref:`locale encoding <locale
   encoding>`, use byte strings.
 * 1 - basic Unicode support: decode inputs and encode outputs using the
   correct encodings, usually only support :ref:`BMP <bmp>`
   characters. Use Unicode strings, or byte strings with the locale
   encoding or, better, an encoding of the UTF family (eg.  :ref:`UTF-8`).
 * 2 - full Unicode support: have access to the Unicode database,
   normalize text, render correctly bidirectional texts and characters with
   diacritics (not required for a server or command line programs).

These levels should help you to estimate the status of the Unicode support of
your project. Level 0 is enough if all of your users speak the same language or
live in close countries. Level 1 usually means an excellent support of Western
Europe languages. Level 2 is required to support Asian languages.

By default, the :ref:`C <c>`, :ref:`C++ <cpp>` and :ref:`PHP5 <php>` languages
are at level 0.  For the C and C++ languages, you can reach level 1 or 2 using
a third-party library like :ref:`glib <glib>`, :ref:`Qt <qt>` or :ref:`ICU
<icu>`. With PHP5, you can reach level 1 using "``mb_``" functions.

By default, the :ref:`Python 2 <python2>` language is at level 0. You can reach
level 1 if you store text into the ``unicode`` type and take care of input and
output encodings. For :ref:`Python 3 <python3>`, the situation is different: it
gives you directly the level 1 by using the wide character API on Windows and by
taking care of input and output encodings for you (eg. decode command line
arguments and environment variables). The ``unicodedata`` module is a first
step for a partial support of the level 2.

Most UNIX and Windows programs are at level 0. Firefox web browser and
OpenOffice.org office suite are at the level 2. Slowly, more and more programs
are coming to the level 1.

Don't expect to reach directly the level 2: it requires a lot of work. Your
project may be fully Unicode compliant for a specific task (eg. filenames), but
only have a basic Unicode support for the other parts of the project.


Test the Unicode support of a program
-------------------------------------

Tests to evaluate the Unicode support of a program:

 * Write non-ASCII characters (eg. é, U+00E9) in all input fields: if the
   program fails with an error, it has no Unicode support.
 * Write characters not encodable to the :ref:`locale encoding <locale
   encoding>` (eg. Ł, U+0141) in all input fields: if the program fails with an
   error, it has probably a basic Unicode program.
 * To test if a program is fully Unicode compliant, write text mixing different
   languages in different directions and characters with diacritics, especially
   in Persian characters. Try also :ref:`decomposed characters
   <normalization>`, for example: {e, U+0301} (decomposed form of é, U+00E9).

See also the Wikipedia article to `test the Unicode support of your web
browser`_.

.. _test the Unicode support of your web browser:
   http://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Unicode/Test


Get the encoding of your inputs
-------------------------------

Locale encoding (OSes different than Windows):

 * Get a copy of the current locale with ``setlocale(LC_CTYPE, NULL)``
 * Set the current locale encoding: ``setlocale(LC_CTYPE, "")``
 * Use ``nl_langinfo(CODESET)`` if available
 * or ``setlocale(LC_CTYPE, "")``

Console:

 * Windows: :c:func:`GetConsoleCP` for stdin and :c:func:`GetConsoleOutputCP` for
   stdout and stderr
 * Other OSes: use the locale encoding

Files:

 * XML: the encoding can be specified in the ``<?xml ...?>`` header, use UTF-8
   if the encoding is not specified.  For example, ``<?xml version="1.0"
   encoding="iso-8859-1"?>``.
 * HTML: the encoding can be specified in a "Content type" HTTP header, eg.
   ``<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">``.
   If it is not, you have to guess the encoding.

Filenames (filesystem):

 * Windows stores filenames as Unicode. It provides a bytes compatibily layer
   using the :ref:`ANSI code page` for applications using bytes strings.
 * Mac OS X encodes filenames to :ref:`UTF-8` and normalize see to a variant of the
   Normal Form D (see :ref:`Mac OS X`).
 * Other OSes: use the locale encoding

See also :ref:`Guess encoding` section.

