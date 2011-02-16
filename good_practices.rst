Good practices
==============

.. _bytes:

Definition of a byte string
---------------------------

A "byte string" is a string encoded to an encoding. It is usually implemented
as an array of 8 bits unsigned integers (e.g. :c:type:`char*` in :ref:`C <c>`). The
character range supported by a byte string depends on its encoding. For
example, an :ref:`ASCII <ascii>` (byte) string can only store characters in
U+0000—U+007F (128 code points).

Concatenate two byte strings leads to :ref:`mojibake <mojibake>` if the strings
use different encodings. Unicode strings don't have this issue.

A :ref:`UTF-8 <utf8>` encoded byte string is a particular case, because this
encoding is able to encode all Unicode characters. An UTF-8 encoded string can
be seen as an Unicode string, but it is called "byte string" in this book to
avoid the confusion with "native" Unicode string. The main difference between
an UTF-8 byte string and a Unicode string is the complexity of getting the nth
character: O(n) for the byte string and O(1) for the Unicode string. There is
one exception: if the Unicode string is implemented using UTF-16: it has also a
complexity of O(n).

:ref:`PHP5 <php>` only supports byte strings.


.. _str:

Definition of a character string
--------------------------------

A "character string", or "Unicode string", is a string where each character can
be, depending on the implementation, any Unicode character or :ref:`BMP-only
<bmp>` characters. There are 3 different implementations:

 * array of 32 bits unsigned integers, :ref:`UCS-4 <ucs>`: full Unicode
   range
 * array of 16 bits unsigned integers, :ref:`UCS-2 <ucs>`: BMP only
 * array of 16 bits unsigned integers with :ref:`surrogate pairs
   <surrogates>`, :ref:`UTF-16 <utf16>`: full Unicode range

UCS-4 strings use two times more memory than UCS-2 strings, but there are able
to store non-BMP character. UTF-16 is a compromise between UCS-2 and UCS-4, but
it has disadvantages.

UTF-16 strings are not exactly character strings, because their length is the
number of UTF-16 words, and not the number of characters. For :ref:`BMP <bmp>`
characters, the length is the same, but not for non-BMP characters.  For
example, U+10FFFF is one character, but it is encoded as 2 UTF-16 words: U+DBFF
and U+DFFF (a :ref:`surrogate pair <surrogates>`). Getting the nth character in
such string has a complexity of O(n), whereas it has a complexity of O(1) for
UCS-2 and UCS-4 strings.

:ref:`Java` language, the :ref:`Qt <qt>` library and :ref:`Windows 2000 <win>` implement
Unicode strings with UTF-16. The :ref:`C <c>` and :ref:`Python <python>`
languages use UTF-16 or UCS-4 depending on: the size of the :c:type:`wchar_t`
type (16 or 32 bits) for C, and the compilation mode (narrow or wide) for
Python. Windows 95 used UCS-2 strings.


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


.. _support:

Unicode support levels
----------------------

There are different levels of Unicode support:

 * **0 - no** Unicode support: only work correctly if all inputs and outputs are
   encoded to the same encoding, usually the :ref:`locale encoding <locale
   encoding>`, use :ref:`byte strings <bytes>`.
 * **1 - basic** Unicode support: decode inputs and encode outputs using the
   correct encodings, usually only support :ref:`BMP <bmp>`
   characters. Use :ref:`Unicode strings <str>`, or :ref:`byte strings <bytes>`
   with the locale encoding or, better, an encoding of the UTF family (e.g.
   :ref:`UTF-8`).
 * **2 - full** Unicode support: have access to the Unicode database,
   :ref:`normalize text <normalization>`, render correctly bidirectional texts
   and characters with diacritics.

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
taking care of input and output encodings for you (e.g. decode command line
arguments and environment variables). The ``unicodedata`` module is a first
step for a partial support of the level 2.

Most UNIX and Windows programs are at level 0. Firefox web browser and
OpenOffice.org office suite are at the level 2. Slowly, more and more programs
are coming to the level 1.

Don't expect to reach directly the level 2: it requires a lot of work. Your
project may be fully Unicode compliant for a specific task (e.g. filenames), but
only have a basic Unicode support for the other parts of the project.


Test the Unicode support of a program
-------------------------------------

Tests to evaluate the Unicode support of a program:

 * Write non-ASCII characters (e.g. é, U+00E9) in all input fields: if the
   program fails with an error, it has no Unicode support.
 * Write characters not encodable to the :ref:`locale encoding <locale
   encoding>` (e.g. Ł, U+0141) in all input fields: if the program fails with an
   error, it has probably a basic Unicode program.
 * To test if a program is fully Unicode compliant, write text mixing different
   languages in different directions and characters with diacritics, especially
   in Persian characters. Try also :ref:`decomposed characters
   <normalization>`, for example: {e, U+0301} (decomposed form of é, U+00E9).

.. seealso::

   Wikipedia article to `test the Unicode support of your web browser
   <http://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Unicode/Test>`_.


Get the encoding of your inputs
-------------------------------

Console:

 * Windows: :c:func:`GetConsoleCP` for stdin and :c:func:`GetConsoleOutputCP` for
   stdout and stderr
 * Other OSes: use the :ref:`locale encoding <locale encoding>`

File formats:

 * XML: the encoding can be specified in the ``<?xml ...?>`` header, use
   :ref:`UTF-8` if the encoding is not specified.  For example, ``<?xml
   version="1.0" encoding="iso-8859-1"?>``.
 * HTML: the encoding can be specified in a "Content type" HTTP header, e.g.
   ``<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">``.
   If it is not, you have to guess the encoding.

Filesystem (filenames):

 * :ref:`Windows` stores filenames as Unicode. It provides a bytes compatibily layer
   using the :ref:`ANSI code page` for applications using bytes strings.
 * :ref:`Mac OS X <osx>` encodes filenames to :ref:`UTF-8` and normalize see to a
   variant of the Normal Form D.
 * Other OSes: use the :ref:`locale encoding <locale encoding>`

.. seealso:: :ref:`guess`.

