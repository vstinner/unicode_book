Good practices
==============

Rules
-----

.. TODO:: NELLE : I'd probably replace rules per tips

To limit or avoid issues with Unicode, try to follow these rules:

 * :ref:`decode <decode>` all bytes data as early as possible: keyboard
   strokes, files, data received from the network, ...
 * :ref:`encode <encode>` back Unicode to bytes as late as possible: write text
   to a file, log a message, send data to the network, ...
 * always store and manipulate text as :ref:`character strings <str>`
 * if you have to encode text and you can choose the encoding: prefer the :ref:`UTF-8` encoding.
   It is able to encode all Unicode 6.0 characters (including :ref:`non-BMP
   characters <bmp>`), does not depend on endianness, is well supported by most
   programs, and its size is a good compromise.

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
your project. Basic support is enough if all of your users speak the same language or
live in close countries. Basic Unicode support usually means excellent support of Western
Europe languages. Full Unicode support is required to support Asian languages.

By default, the :ref:`C <c>`, :ref:`C++ <cpp>` and :ref:`PHP5 <php>` languages
have basic Unicode support.  For the C and C++ languages, you can have basic or full Unicode support using
a third-party library like :ref:`glib <glib>`, :ref:`Qt <qt>` or :ref:`ICU
<icu>`. With PHP5, you can have basic Unicode support using "``mb_``" functions.

By default, the :ref:`Python 2 <python2>` language doesn't support Unicode. You can have
basic Unicode support if you store text into the ``unicode`` type and take care of input and
output encodings. For :ref:`Python 3 <python3>`, the situation is different: it
has direct basic Unicode support by using the wide character API on Windows and by
taking care of input and output encodings for you (e.g. decode command line
arguments and environment variables). The ``unicodedata`` module is a first
step for a full Unicode support.

Most UNIX and Windows programs don't support Unicode. Firefox web browser and
OpenOffice.org office suite have full Unicode support. Slowly, more and more programs
have basic Unicode support.

.. NELLE : juste en anecdote: OOo supporte complétement l'unicode, mais les
  branches OOo4Kids et OOoLight ont désactivées ce support par défaut parce
  que ça compliquait la compilation à mort :p

  Je pense qu'elle va être remise un jour ou un autre dans ces branches.

Don't expect to have full Unicode support directly: it requires a lot of work. Your
project may be fully Unicode compliant for a specific task (e.g. :ref:`filenames <filename>`), but
only have basic Unicode support for the other parts of the project.


Test the Unicode support of a program
-------------------------------------

Tests to evaluate the Unicode support of a program:

 * Write non-ASCII characters (e.g. é, U+00E9) in all input fields: if the
   program fails with an error, it has no Unicode support.
 * Write characters not encodable to the :ref:`locale encoding <locale
   encoding>` (e.g. Ł, U+0141) in all input fields: if the program fails with an
   error, it probably has basic Unicode support.
 * To test if a program is fully Unicode compliant, write text mixing different
   languages in different directions and characters with diacritics, especially
   in Persian characters. Try also :ref:`decomposed characters
   <normalization>`, for example: {e, U+0301} (decomposed form of é, U+00E9).

.. seealso::

   Wikipedia article to `test the Unicode support of your web browser
   <http://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Unicode/Test>`_. `UTF-8 encoded
   sample plain-text file <http://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-demo.txt>`_
   (Markus Kuhn, 2002).


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

 * :ref:`Windows` stores filenames as Unicode. It provides a bytes compatibility layer
   using the :ref:`ANSI code page <codepage>` for applications using :ref:`byte strings <bytes>`.
 * :ref:`Mac OS X <osx>` encodes filenames to :ref:`UTF-8` and :ref:`normalize
   <normalization>` see to a variant of the Normal Form D.
 * Other OSes: use the :ref:`locale encoding <locale encoding>`

.. seealso:: :ref:`guess`


Switch from byte strings to character strings
---------------------------------------------

Use character strings, instead of byte strings, to avoid :ref:`mojibake issues
<mojibake>`.

.. todo:: explain why byte strings are still used (backward compatibility)
.. todo:: explain how to switch from byte to unicode strings: Python 2=>3, Windows A=>W, PHP 5=>6

