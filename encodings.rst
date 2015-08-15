Charsets and encodings
======================

.. todo:: write an introduction

Encodings
---------

There are many encodings around the world. Before Unicode, each manufacturer
invented its own encoding to fit its client market and its usage. Most
encodings are incompatible on at least one code, except some exceptions.
A document stored in :ref:`ASCII` can be read using :ref:`ISO-8859-1` or
UTF-8, because ISO-8859-1 and UTF-8 are supersets of ASCII. Each encoding can
have multiple aliases, examples:

 * ASCII: US-ASCII, ISO 646, ANSI_X3.4-1968, …
 * ISO-8859-1: Latin-1, iso88591, …
 * UTF-8: utf8, UTF_8, …

:ref:`Unicode <unicode charset>` is a charset and it requires a encoding. Only
encodings of the UTF family are able to encode and decode all Unicode code
points. Other encodings only support a subset of Unicode codespace. For
example, ISO-8859-1 are the first 256 Unicode code points (U+0000—U+00FF).

This book presents the following encodings: :ref:`ASCII`, :ref:`cp1252`,
:ref:`GBK <gbk>`, :ref:`ISO-8859-1`, :ref:`ISO-8859-15`, :ref:`JIS <jis>`,
:ref:`UCS-2 <ucs2>`, :ref:`UCS-4 <ucs4>`, :ref:`UTF-8`, :ref:`UTF-16 <utf16>`
and :ref:`UTF-32 <utf32>`.

.. see also: Definitions of a :ref:`charset <charset>` and of a :ref:`encoding
   <encoding>`.


Popularity
----------

The three most common encodings are, in chronological order of their creation:
:ref:`ASCII` (1968), :ref:`ISO-8859-1` (1987) and :ref:`UTF-8` (1996).

Google posted an interesting graph of the usage of different encodings on the
web: `Unicode nearing 50% of the web
<http://googleblog.blogspot.com/2010/01/unicode-nearing-50-of-web.html>`_
(Mark Davis, january 2010). Because Google crawls a huge part of the web,
these numbers should be reliable. In 2001, the most used encodings were:

 * 1st (56%): :ref:`ASCII`
 * 2nd (23%): Western Europe encodings (:ref:`ISO-8859-1`, :ref:`ISO-8859-15`
   and :ref:`cp1252`)
 * 3rd (8%): Chinese encodings (:ref:`GB2312 <gbk>`, ...)
 * and then come Korean (EUC-KR), Cyrillic (cp1251, KOI8-R, ...), East Europe
   (cp1250, ISO-8859-2), Arabic (cp1256, ISO-8859-6), etc.
 * (UTF-8 was not used on the web in 2001)

.. todo:: 4th: 13%?

In december 2007, for the first time: :ref:`UTF-8` becomes the most used encoding
(near 25%). In january 2010, UTF-8 was close to 50%, and ASCII and Western
Europe encodings near 20%. The usage of the other encodings don't change.

.. todo:: add an explicit list of top3 in 2010


Encodings performances
----------------------

Complexity of getting the n :sup:`th` character in a string, and of
getting the length in character of a string:

 * :math:`O(1)` for 7 and 8 bit encodings (:ref:`ASCII <ascii>`, :ref:`ISO 8859
   family <ISO-8859>`, ...), UCS-2 and UCS-4
 * :math:`O(n)` for variable length encodings (e.g. the UTF family)

.. todo:: Perf of the codec


Examples
--------

+------------+-------------------------+-------------------------+-------------------------+-------------------------+
| Encoding   |       A (U+0041)        |       é (U+00E9)        |       € (U+20AC)        |        U+10FFFF         |
+============+=========================+=========================+=========================+=========================+
| ASCII      | ``0x41``                | —                       | —                       | —                       |
+------------+-------------------------+-------------------------+-------------------------+-------------------------+
| ISO-8859-1 | ``0x41``                | ``0xE9``                | —                       | —                       |
+------------+-------------------------+-------------------------+-------------------------+-------------------------+
| UTF-8      | ``0x41``                | ``0xC3 0xA9``           | ``0xE2 0x82 0xAC``      | ``0xF4 0x8F 0xBF 0xBF`` |
+------------+-------------------------+-------------------------+-------------------------+-------------------------+
| UTF-16-LE  | ``0x41 0x00``           | ``0xE9 0x00``           | ``0xAC 0x20``           | ``0xFF 0xDB 0xFF 0xDF`` |
+------------+-------------------------+-------------------------+-------------------------+-------------------------+
| UTF-32-BE  | ``0x00 0x00 0x00 0x41`` | ``0x00 0x00 0x00 0xE9`` | ``0x00 0x00 0x20 0xAC`` | ``0x00 0x10 0xFF 0xFF`` |
+------------+-------------------------+-------------------------+-------------------------+-------------------------+

— indicates that the character cannot be encoded.


Handle undecodable bytes and unencodable characters
---------------------------------------------------

.. _undecodable:

Undecodable byte sequences
''''''''''''''''''''''''''

When a :ref:`byte string <bytes>` is :ref:`decoded <decode>` from an encoding, the decoder may
fail to decode a specific byte sequence. For example, ``0x61 0x62 0x63 0xE9``
is not decodable from :ref:`ASCII` nor :ref:`UTF-8`, but it is decodable from
:ref:`ISO-8859-1`.

.. TODO:: NELLE "is decoded from an encoding" => "is decoded"

Some encodings are able to decode any byte sequences. All encodings of the
:ref:`ISO-8859 family <ISO-8859>` have this property, because all of the 256
code points of these 8 bits encodings are assigned.


.. _unencodable:

Unencodable characters
''''''''''''''''''''''

When a :ref:`character string <str>` is :ref:`encoded <encode>` to a
:ref:`character set <charset>` smaller than the :ref:`Unicode character set
(UCS) <UCS>`, a character may not be encodable. For example, € (U+20AC) is not
encodable to :ref:`ISO-8859-1`, but it is encodable to :ref:`ISO-8859-15` and
:ref:`UTF-8`.


.. _errors:
.. _strict:
.. _replace:
.. _ignore:

Error handlers
''''''''''''''

There are different choices to handle :ref:`undecodable byte sequences
<undecodable>` and :ref:`unencodable characters <unencodable>`:

 * strict: raise an error
 * ignore
 * replace by ? (U+003F) or � (U+FFFD)
 * replace by a similar glyph
 * escape: format its code point
 * etc.

Example of the "abcdé" string encoded to ASCII, é (U+00E9) is not encodable to
ASCII:

+----------------------------+------------------+
| Error handler              | Output           |
+============================+==================+
| strict                     | *raise an error* |
+----------------------------+------------------+
| ignore                     | ``"abcd"``       |
+----------------------------+------------------+
| replace by ?               | ``"abcd?"``      |
+----------------------------+------------------+
| replace by a similar glyph | ``"abcde"``      |
+----------------------------+------------------+
| escape as hexadecimal      | ``"abcd\xe9"``   |
+----------------------------+------------------+
| escape as XML entities     | ``"abcd&#233;"`` |
+----------------------------+------------------+

.. _translit:

Replace unencodable characters by a similar glyph
'''''''''''''''''''''''''''''''''''''''''''''''''

By default, :c:func:`WideCharToMultiByte` replaces unencodable characters by
similarly looking characters. The :ref:`normalization <normalization>` to NFKC
and NFKD does also such operation. Examples:

+--------------------------------------------------------+------------------------------------------+
| Character                                              | Replaced by                              |
+============================================+===========+=========+================================+
| U+0141, latin capital letter l with stroke | Ł         | L       | U+004C, latin capital letter l |
+--------------------------------------------+-----------+---------+--------------------------------+
| U+00B5, micro sign                         | µ         | μ       | U+03BC, greek small letter mu  |
+--------------------------------------------+-----------+---------+--------------------------------+
| U+221E, infinity                           | ∞         | 8       | U+0038, digit eight            |
+--------------------------------------------+-----------+---------+--------------------------------+
| U+0133, latin small ligature ij            | ĳ         | ij      | {U+0069, U+006A}               |
+--------------------------------------------+-----------+---------+--------------------------------+
| U+20AC, euro sign                          | €         | EUR     | {U+0045, U+0055, U+0052}       |
+--------------------------------------------+-----------+---------+--------------------------------+

∞ (U+221E) replaced by 8 (U+0038) is the worst example of the method: these two
characters are different meanings.

.. todo:: define "glyph"


.. _escape:

Escape the character
''''''''''''''''''''

:ref:`Python <python>` "backslashreplace" error handler uses ``\xHH``, ``\uHHHH`` or
``\UHHHHHHHH`` where HHH...H is the code point formatted in hexadecimal. PHP
"long" error handler uses ``U+HH``, ``U+HHHH`` or ``encoding+HHHH`` (e.g.
``JIS+7E7E``).

:ref:`PHP <php>` "entity" and Python "xmlcharrefreplace" error handlers escape
the code point as an HTML/XML entity. For example, when U+00E9 is encoded to
ASCII: it is replaced by ``&#xE9;`` in PHP and ``&#233;`` in Python.


Other charsets and encodings
----------------------------

There are much more charsets and encodings, but it is not useful to know them.
The knowledge of a good conversion library, like :ref:`iconv <iconv>`, is
enough.

.. todo:: VISCII, EDBIC

