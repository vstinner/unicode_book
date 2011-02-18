Good practices
==============

.. _bytes:

Definition of a byte string
---------------------------

A "byte string" is an array of 8 bits unsigned integers. The
character range supported by a byte string depends on its encoding. For
example, an :ref:`ASCII <ascii>` string can only store characters in
U+0000—U+007F (128 code points).

.. todo:: explain why byte strings are still used (backward compatibility)
.. todo:: Define "ASCII-encoded string", "ASCII string", "ASCII byte string"

:ref:`PHP5 <php>` only supports byte strings. In the :ref:`C language <c>`, a
byte string uses the :c:type:`char*` type (or :c:type:`const char*`).


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

.. todo:: NELLE - I think you should define BMP *before* using the term

UCS-4 strings use twice as much memory than UCS-2 strings, but are able
to store non-BMP character. UTF-16 is a compromise between UCS-2 and UCS-4, but
has its disadvantages.

UTF-16 strings are not strictly character strings, because their length is the
number of UTF-16 units, and not the number of characters. For :ref:`BMP <bmp>`
characters, the length is the same, but not for non-BMP characters.  For
example, U+10FFFF is one character, but it is encoded as two UTF-16 units: {U+DBFF,
U+DFFF} (a :ref:`surrogate pair <surrogates>`). Getting the nth character in
such string has a complexity of :math:`O(n)`, whereas it has a complexity of :math:`O(1)` for
UCS-2 and UCS-4 strings.

:ref:`Java` language, the :ref:`Qt <qt>` library and :ref:`Windows 2000 <win>` implement
Unicode strings with UTF-16. The :ref:`C <c>` and :ref:`Python <python>`
languages use UTF-16 or UCS-4 depending on: the size of the :c:type:`wchar_t`
type (16 or 32 bits) for C, and the compilation mode (narrow or wide) for
Python. Windows 95 uses UCS-2 strings.


Differences between byte and character strings
----------------------------------------------

.. TODO:: Nelle : what is a character strings ? In any case strings is plural
  and byte singular. ISn't that a bit strange ?

The most important difference between byte and character strings is that a byte
string has an encoding. The encoding is usually not stored in the string, the
developer have to take care of the encoding of all strings. Concatenate two
byte strings of different encodings leads to :ref:`mojibake <mojibake>`,
whereas Unicode strings don't have this issue.

.. TODO:: Nelle : the developer **has**

A :ref:`UTF-8 <utf8>` string is a particular case, because UTF-8 is able to
encode all Unicode characters [1]_ . But a UTF-8 string is not a Unicode string
because the string unit is byte and not character: you can get an individual
byte of a multibyte character.

.. TODO:: Nelle : un exemple de ce dernier cas serais, je pense, le bienvenue
  ici 

Another difference between UTF-8 strings and Unicode strings is the complexity
of getting the nth character: :math:`O(n)` for the byte string and :math:`O(1)`
for the Unicode string. There is one exception: if the Unicode string is
implemented using UTF-16: it has also a complexity of :math:`O(n)`.

.. todo:: explain how to switch from byte to unicode strings: Python 2=>3, Windows A=>W, PHP 5=>6

.. [1] A UTF-8 encoder :ref:`should not encode <strict utf8 decoder>` :ref:`surrogate characters <surrogates>` (U+D800—U+DFFF).


Rules
-----

.. TODO:: NELLE : I'd probably replace rules per tips

To limit or avoid issues with Unicode, try to follow these rules:

 * decode all bytes data as early as possible: keyboard strokes, files, data
   received from the network, ...
 * encode back Unicode to bytes as late as possible: write text to a file,
   log a message, send data to the network, ...
 * always store and manipulate text as :ref:`character strings <str>`
 * if you have to encode text and you can choose the encoding: prefer the :ref:`UTF-8` encoding.
   It is able to encode all Unicode 6.0 characters (including :ref:`non-BMP
   characters <bmp>`), has no endian issue, is well support by most
   programs, and is good compromise is size.

.. TODO:: problem grammatical dans la dernière phrase du dernier point

.. _support:

Unicode support levels
----------------------

There are different levels of Unicode support:

 * **don't** support Unicode: only work correctly if all inputs and outputs are
   encoded to the same encoding, usually the :ref:`locale encoding <locale
   encoding>`, use :ref:`byte strings <bytes>`.
 * **basic** Unicode support: decode inputs and encode outputs using the
   correct encodings, usually only support :ref:`BMP <bmp>`
   characters. Use :ref:`Unicode strings <str>`, or :ref:`byte strings <bytes>`
   with the locale encoding or, better, an encoding of the UTF family (e.g.
   :ref:`UTF-8`).
 * **full** Unicode support: have access to the Unicode database,
   :ref:`normalize text <normalization>`, render correctly bidirectional texts
   and characters with diacritics.

These levels should help you to estimate the status of the Unicode support of
your project. A basic support is enough if all of your users speak the same language or
live in close countries. A basic Unicode support usually means an excellent support of Western
Europe languages. Full Unicode support is required to support Asian languages.

By default, the :ref:`C <c>`, :ref:`C++ <cpp>` and :ref:`PHP5 <php>` languages
have a basic Unicode support.  For the C and C++ languages, you can have a basic of full Unicode support using
a third-party library like :ref:`glib <glib>`, :ref:`Qt <qt>` or :ref:`ICU
<icu>`. With PHP5, you can have a basic Unicode support using "``mb_``" functions.

By default, the :ref:`Python 2 <python2>` language doesn't support Unicode. You can have a
basic Unicode support if you store text into the ``unicode`` type and take care of input and
output encodings. For :ref:`Python 3 <python3>`, the situation is different: it
has directly a basic Unicode support by using the wide character API on Windows and by
taking care of input and output encodings for you (e.g. decode command line
arguments and environment variables). The ``unicodedata`` module is a first
step for a full Unicode support.

Most UNIX and Windows programs don't support Unicode. Firefox web browser and
OpenOffice.org office suite have a full Unicode support. Slowly, more and more programs
have a basic Unicode support.

.. NELLE : juste en anecdote: OOo supporte complétement l'unicode, mais les
  branches OOo4Kids et OOoLight ont désactivées ce support par défaut parce
  que ça compliquait la compilation à mort :p

  Je pense qu'elle va être remise un jour ou un autre dans ces branches.

Don't expect to have directly a full Unicode support: it requires a lot of work. Your
project may be fully Unicode compliant for a specific task (e.g. :ref:`filenames <filename>`), but
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

