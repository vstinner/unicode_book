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

See also :ref:`How to guess the encoding of a document?` section.

