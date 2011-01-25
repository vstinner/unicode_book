Good practices
==============

Rules
-----

To limit/avoid issues with Unicode, try to follow the following rules:

 * decode all bytes data (eg. keyboard strokes, files, data received from the network,
   ...) as early as possible
 * encode back Unicode to bytes as late as possible (eg. write text to a file,
   log a message, send data to the network, ...)
 * always store and manipulate text as character strings
 * if you have to encode text and you can choose the encoding, prefer UTF-8
   because it is able to encode all Unicode 6.0 characters and it is a good
   compromise in size.

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

Basic tests to estimate the level of a program:

 * Write a non-ASCII character (eg. é, U+00E9) in all input fields: if the
   program fails with an error, you are at level 0.
 * Write a character not-encodable to the locale (eg. Ł, U+0141): if the
   program fails with an error, you are probably at level 1.
 * Write text mixing languages in different directions and using characters
   with diacritics, especially in Persian. For example, XXX.

See also the Wikipedia article to `test the Unicode support of your web
browser`_.

.. _test the Unicode support of your web browser:
   http://fr.wikipedia.org/wiki/Wikipedia:Aide_Unicode


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

