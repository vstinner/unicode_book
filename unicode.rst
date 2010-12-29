.. section-numbering::

.. todo:: :c:type:`char*` points to char, not char*
.. todo:: add statistics about encodings popularity

About this book
===============

License
-------

This book is distributed under the `CC BY-NC-SA 3.0 license`_.

Thanks to
---------

Reviewers:

 * Alexander Belopolsky
 * Antoine Pitrou
 * Feth Arezki


Notations used in this book
---------------------------

 * ``0bBBBBBBBB``: 8 bit unsigned number written in binary, first digit is the most
   significant. For example, ``0b10000000`` is 128.
 * 0xHHHH: number written in hexadecimal, eg. 0xFFFF is 65535.
 * ``0xHH 0xHH ...``: byte sequence with bytes written in hexadecimal, eg.
   ``0xC3 0xA9`` (2 bytes) is the character é (U+00E9) encoded to UTF-8.
 * U+HHHH: Unicode code point with code written in hexadecimal. For example, U+20AC is
   the code point 8364 (euro sign). Big code point are written with more than 4
   hexadecimal digits, eg. U+10FFFF is the biggest (unallocated) code point of
   Unicode 6.0: 1114111.
 * A—B: range including start and end. Examples:

   * ``0x00``\ —\ ``0x7F`` is a range of 128 bytes (0 through 127)
   * U+0000—U+00FF is a range of 256 characters (0 through 255)


Unicode nightmare
=================

`Unicode`_ is the nightmare of many developers (and users) for different, and
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
known problem: mojibake (display of strange characters or squares).

.. todo:: add a screenshot of mojibake

It is difficult to get, or worse, guess the encoding of a document. Except for
modern encodings such as those in the UTF family (coming from the Unicode standard), there
is no reliable algorithm for that. We have to rely on statistics to guess the most
probable encoding. This is done by most Internet browsers, but few libraries
include such algorithm.

Unicode support by operating systems, programming languages and libraries
varies a lot. In general, the support is weak or non-existent. Each operating
system manages Unicode differently. For example, `Microsoft Windows`_ stores filenames as Unicode,
whereas UNIX and BSD operating systems use bytes.

Mixing documents stored as bytes is possible, even if they use different
encodings, but leads to mojibake. Because libraries and programs do also ignore
encode and decode warnings or errors, write a single character with a diacritic
(any non `ASCII`_ character) is sometimes enough to get an error.

Full Unicode support is complex because the Unicode charset is bigger than any
other charset. For example, `ISO-8859-1`_ contains 256 codes including 191
characters, whereas Unicode (version 6.0) contains approximatively 245,000
assigned codes (see `Statistics`_). The Unicode standard is larger than just a
charset: it explains also how to display characters (eg. left-to-right for
English and right-to-left for persian), how to normalize a character string
(eg. precomposed characters versus the decomposed form), etc.

This book explains how to sympathize with Unicode, and how you should modify
your program to avoid most, or all, issues related to encodings and Unicode.


Charsets and encodings
======================

What are charsets and encodings?
--------------------------------

A charset, character set, is a mapping between code points and characters. An
encoding describes how to encode characters (code points) to bytes and howto
decode bytes to characters (code points). 7 and 8 bits charsets don't need any
encoding: a code point is stored in a single byte (unsigned 8 bits number).
Because of these charsets, many people confuse charsets and encodings.
Bigger charsets need multibyte encodings like `UTF-8`_ or `GBK`_. A multibyte
encoding can encode all code points into byte sequences of the same size (eg. `UCS-2`_), or byte
sequence with a variable length (eg. `UTF-16`_). UTF-8 uses a variable length: code points lower
than 128 use a single byte, whereas higher code points take between 2 and 4 bytes.

There are many encodings around the world. Before Unicode, each manufacturer
invented its own encoding to fit its client market and its usage. Most
encodings are incompatible on at least one code, except some exceptions (eg. a
document stored in `ASCII`_ can be read using `ISO-8859-1`_ or UTF-8, because ASCII
is a subset of ISO-8859-1 and UTF-8) The most common encodings are, in
chronological order of their creation: ASCII (1968), ISO-8859-1 (1987) and
UTF-8 (1996). Each encoding can have multiple aliases, for example:

 * ASCII: US-ASCII, ISO 646, ANSI_X3.4-1968, …
 * ISO-8859-1: Latin-1, iso88591, …
 * UTF-8: utf8, UTF_8, …

`Unicode`_ is a charset and it requires a encoding. Only encodings of the UTF
family are able to encode and decode all Unicode code points. Other encodings
only support a subset of Unicode codespace. For example, ISO-8859-1 are the
first 256 Unicode code points (U+0000—U+00FF).

This book only present most popular encodings:

 * `ASCII`_
 * `cp1252`_
 * `GBK`_
 * `ISO-8859-1`_
 * `ISO-8859-15`_
 * `JIS`_
 * `UTF-8`_
 * `UTF-16`_
 * `UTF-32`_


Historical charsets and encodings
---------------------------------

Between 1950 and 2000, each manufacturer and each operating system created its
own 8 bits encoding. The problem was that 8 bits (256 code points) are not
enough to store any character, and so the encoding tries to fit the user's
language. Most 8 bits encodings are able to encode multiple languages, usually
geograpically close (eg. ISO-8859-1 is intented for Western Europe).

It was difficult to exchange documents of different languages, because if a
document was encoded to an encoding different than the user encoding, it leaded
to mojibake.


.. index:: ASCII

ASCII
'''''

ASCII encoding is supported by all applications. A document encoded in ASCII
can be read decoded by any other encoding. This is explained by the fact that
all 7 and 8 bits encodings are based on ASCII (to be compatible with ASCII,
except `JIS X 0201`_ encoding: ``0x5C`` is decoded to the yen sign (U+00A5, ¥)
instead of a backslash (U+005C, \\). ASCII is
the smallest encoding, it only contains 128 codes including 95 printable
characters (letters, digits, punctuation signs and some other various
characters) and 33 control codes. Control codes are used to control the
terminal, eg. 10, the "line feed", written ``"\n"`` is most programming
languages, marks the end of a line. There are some special control code, eg. 7,
known as "bell" and written ``"\b"``, sent to ring a bell. ASCII code points
are the first 128 code points of Unicode (U+0000—U+007F).

+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
|    |  -0 |  -1 |  -2 |  -3 |  -4 |  -5 |  -6 |  -7 |  -8 |  -9 |  -a |  -b |  -c |  -d |  -e |  -f |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 0- | NUL |  �  |  �  |  �  |  �  |  �  |  �  | BEL |  �  | TAB |  LF |  �  |  �  |  CR |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1- |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  | ESC |  �  |  �  |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 2- |     |  !  |  "  |  #  |  $  |  %  |  &  |  '  |  (  |  )  |  \* |  \+ |  ,  |  \- |  .  |  /  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 3- |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  :  |  ;  |  <  |  =  |  >  |  ?  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 4- |  @  |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |  J  |  K  |  L  |  M  |  N  |  O  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 5- |  P  |  Q  |  R  |  S  |  T  |  U  |  V  |  W  |  X  |  Y  |  Z  |  [  | \\  |  ]  |  ^  |  _  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 6- | \`  |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |  i  |  j  |  k  |  l  |  m  |  n  |  o  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 7- |  p  |  q  |  r  |  s  |  t  |  u  |  v  |  w  |  x  |  y  |  z  |  {  |  |  |  }  |  ~  | DEL |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

U+0000—U+001F and U+007F are control codes:

 * "NUL": nul character (U+0000, ``"\0"``)
 * "BEL": sent to ring a bell (U+0007, ``"\b"``)
 * "TAB": horizontal tabulation (U+0009, ``"\t"``)
 * "LF": line feed (U+000A, ``"\n"``)
 * "ESC": escape (U+001B)
 * "DEL": delete (U+007F)
 * other control codes are displayed as � in this table


.. index:: ISO-8859-1

ISO-8859-1
''''''''''

ISO-8859-1 is a superset of `ASCII`_ and adds 128 codes, mostly latin letters with diacritics, and
is used in the USA and Europe. ISO-8859-1 are the 256 first code points of
Unicode (U+0000—U+00FF).

+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
|    |  -0 |  -1 |  -2 |  -3 |  -4 |  -5 |  -6 |  -7 |  -8 |  -9 |  -a |  -b |  -c |  -d |  -e |  -f |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 0- | NUL |  �  |  �  |  �  |  �  |  �  |  �  | BEL |  �  | TAB |  LF |  �  |  �  |  CR |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1- |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  | ESC |  �  |  �  |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 2- |     |  !  |  "  |  #  |  $  |  %  |  &  |  '  |  (  |  )  |  \* |  \+ |  ,  |  \- |  .  |  /  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 3- |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  :  |  ;  |  <  |  =  |  >  |  ?  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 4- |  @  |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |  J  |  K  |  L  |  M  |  N  |  O  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 5- |  P  |  Q  |  R  |  S  |  T  |  U  |  V  |  W  |  X  |  Y  |  Z  |  [  |  \\ |  ]  |  ^  |  _  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 6- |  \` |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |  i  |  j  |  k  |  l  |  m  |  n  |  o  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 7- |  p  |  q  |  r  |  s  |  t  |  u  |  v  |  w  |  x  |  y  |  z  |  {  |  |  |  }  |  ~  | DEL |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 8- |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 9- |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |  �  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| a- | NBSP|  ¡  |  ¢  |  £  |  ¤  |  ¥  |  ¦  |  §  |  ¨  |  ©  |  ª  |  «  |  ¬  | SHY |  ®  |  ¯  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| b- |  °  |  ±  |  ²  |  ³  |  ´  |  µ  |  ¶  |  ·  |  ¸  |  ¹  |  º  |  »  |  ¼  |  ½  |  ¾  |  ¿  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| c- |  À  |  Á  |  Â  |  Ã  |  Ä  |  Å  |  Æ  |  Ç  |  È  |  É  |  Ê  |  Ë  |  Ì  |  Í  |  Î  |  Ï  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| d- |  Ð  |  Ñ  |  Ò  |  Ó  |  Ô  |  Õ  |  Ö  |  ×  |  Ø  |  Ù  |  Ú  |  Û  |  Ü  |  Ý  |  Þ  |  ß  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| e- |  à  |  á  |  â  |  ã  |  ä  |  å  |  æ  |  ç  |  è  |  é  |  ê  |  ë  |  ì  |  í  |  î  |  ï  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| f- |  ð  |  ñ  |  ò  |  ó  |  ô  |  õ  |  ö  |  ÷  |  ø  |  ù  |  ú  |  û  |  ü  |  ý  |  þ  |  ÿ  |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

U+0000—U+001F, U+007F and U+0080—U+009F are control codes (displayed as � in
this table). See the ASCII table for U+0000—U+001F and U+007F control codes.

"NBSP" (U+00A0) is a non breaking space and "SHY" (U+00AD) is a soft hyphen.


.. index:: cp1252

cp1252
''''''

Windows code page 1252, best known as cp1252, is a variant of `ISO-8859-1`_. It is
the default encoding of all English and western europe Windows setups.
It is used as a fallback by web browsers
if the webpage doesn't provide any encoding information (not in HTML, nor in
HTTP).

cp1252 shares 224 code points with ISO-8859-1, the range ``0x80``\ —\ ``0x9F`` (32
characters, including 5 not assigned codes) are different. In ISO-8859-1, this
range are 32 control codes (not printable).

+------------+------------+----------------+------------+------------+----------------+
| Code point | ISO-8859-1 |   cp1252       | Code point | ISO-8859-1 |   cp1252       |
+============+============+================+============+============+================+
|  ``0x80``  |   U+0080   | € (U+20AC)     |  ``0x90``  |   U+0090   | *not assigned* |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x81``  |   U+0081   | *not assigned* |  ``0x91``  |   U+0091   | ‘ (U+2018)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x82``  |   U+0082   | ‚ (U+201A)     |  ``0x92``  |   U+0092   | ’ (U+2019)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x83``  |   U+0083   | ƒ (U+0192)     |  ``0x93``  |   U+0093   | “ (U+201C)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x84``  |   U+0084   | „ (U+201E)     |  ``0x94``  |   U+0094   | ” (U+201D)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x85``  |   U+0085   | … (U+2026)     |  ``0x95``  |   U+0095   | \• (U+2022)    |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x86``  |   U+0086   | † (U+2020)     |  ``0x96``  |   U+0096   | – (U+2013)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x87``  |   U+0087   | ‡ (U+2021)     |  ``0x97``  |   U+0097   | — (U+2014)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x88``  |   U+0088   | ˆ (U+02C6)     |  ``0x98``  |   U+0098   | ˜ (U+02DC)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x89``  |   U+0089   | ‰ (U+2030)     |  ``0x99``  |   U+0099   | ™ (U+2122)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8A``  |   U+008A   | Š (U+0160)     |  ``0x9A``  |   U+009A   | š (U+0161)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8B``  |   U+008B   | ‹ (U+2039)     |  ``0x9B``  |   U+009B   | › (U+203A)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8C``  |   U+008C   | Œ (U+0152)     |  ``0x9C``  |   U+009C   | œ (U+0153)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8D``  |   U+008D   | *not assigned* |  ``0x9D``  |   U+009D   | *not assigned* |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8E``  |   U+008E   | Ž (U+017D)     |  ``0x9E``  |   U+009E   | ž (U+017U)     |
+------------+------------+----------------+------------+------------+----------------+
|  ``0x8F``  |   U+008F   | *not assigned* |  ``0x9F``  |   U+009F   | Ÿ (U+0178)     |
+------------+------------+----------------+------------+------------+----------------+


.. index:: ISO-8859-15

ISO-8859-15
'''''''''''

ISO-8859-15, also known as Latin-9, is a variant of `ISO-8859-1`_. 248 code points
are identicals, 8 are different:

+------------+------------+-------------+------------+------------+-------------+
| Code point | ISO-8859-1 | ISO-8859-15 | Code point | ISO-8859-1 | ISO-8859-15 |
+============+============+=============+============+============+=============+
| ``0xA4``   | ¤ (U+00A4) | € (U+20AC)  | ``0xB8``   | ¸ (U+00B8) | ž (U+017E)  |
+------------+------------+-------------+------------+------------+-------------+
| ``0xA6``   | ¦ (U+00A6) | Š (U+0160)  | ``0xBC``   | ¼ (U+00BC) | Œ (U+0152)  |
+------------+------------+-------------+------------+------------+-------------+
| ``0xA8``   | ¨ (U+00A8) | š (U+0161)  | ``0xBD``   | ½ (U+00BD) | œ (U+0152)  |
+------------+------------+-------------+------------+------------+-------------+
| ``0xB4``   | ´ (U+00B4) | Ž (U+017D)  | ``0xBE``   | ¾ (U+00BE) | Ÿ (U+0178)  |
+------------+------------+-------------+------------+------------+-------------+


.. _GBK:

GBK encoding family (Chinese)
'''''''''''''''''''''''''''''

GBK is a family of Chinese charsets / multibyte encodings:

 * GB 2312 (1980): includes 6,763 Chinese characters
 * GBK (1993) (cp936)
 * GB 18030 (2005, last revision in 2006)
 * HZ (1989) (HG-GZ-2312)

To encode Chinese, there is also the Big5 encoding family and cp950.


.. _JIS:
.. _JIS X 0201:

JIS encoding family (Japanese)
''''''''''''''''''''''''''''''

JIS is a family of Japanese charsets/encodings:

 * JIS X 0201 (1969)
 * JIS X 0208 (first version in 1978: "JIS C 6226", last revision in 1997)
 * JIS X 0211 (1994), based on ISO/IEC 6429
 * JIS X 0212 (1990), extends JIS X 0208
 * JIS X 0213 (first version in 2000, last revision in 2004: EUC JIS X 2004), EUC JIS X 0213
 * Shift JIS
 * EUC JP
 * Windows code page 932 (cp932)

   * U+F8F1 (``0xFD``)
   * U+F8F2 (``0xFE``)
   * U+F8F3 (``0xFF``)

The JIS family causes troubles on MS-DOS and Microsoft Windows because the yen
sign (U+00A5, ¥) is encoded to ``0x5C`` which is a backslash (U+005C, \\) in
ASCII. For example, "C:\\Windows\\win.ini" is displayed "C:¥Windows¥win.ini". The
backslash is encoded to ``0x81 0x5F``.

To encode Japanese, there is also the ISO/IEC 2022 encoding family.


Unicode encodings
-----------------

.. index:: UTF-8

UTF-8
'''''

UTF-8 is a multibyte encoding able to encode the whole Unicode character
encoding. An encoded character takes between 1 and 4 bytes. UTF-8 encoding
supports longer byte sequences, up to 6 bytes, but the biggest code point of
Unicode 6.0 (U+10FFFF) only takes 4 bytes.

It is possible to be sure that a byte string
is encoded by UTF-8, because UTF-8 adds markers to each byte. For the first
byte of a multibyte character, bit 7 and bit 6 are set (``0b11xxxxxx``); the next
bytes have bit 7 set and bit 6 unset (``0b10xxxxxx``). Another cool feature of UTF-8
is that it has no endianness (it can be read in big or little endian order, it does
not matter). The problem with UTF-8, if you compare it to ASCII or ISO-8859-1,
is that it is a multibyte encoding: you cannot access a character by its
character index directly, you have to compute the byte index. If getting a character by
its index is a common operation in your program, use a real character type
like :c:type:`wchar_t`. Another advantage of UTF-8 is that most `C`_ bytes
functions are compatible with UTF-8 encoded strings (eg. :c:func:`strcat` or :c:func:`printf`), whereas they fail with UTF-16
and UTF-32 encoded strings because these encodings encode small codes with nul bytes.

An UTF-8 decoder have to reject invalid byte sequences for security reasons:
``0xC0 0x80`` byte sequence must raise an error (and not be decoded as U+0000).
If the decoder accepts invalid byte sequence, an attacker can use it to skip
security checks (eg. reject string containing nul bytes, ``0x00``). Surrogates
characters are also invalid in UTF-8: characters in U+D800—U+DFFF have to be
rejected.


.. _UCS-2:
.. _UCS-4:
.. _UTF-16:
.. _UTF-16-LE:
.. _UTF-16-BE:
.. _UTF-32:
.. _UTF-32-LE:
.. _UTF-32-BE:
.. index:: UCS-2, UCS-4, UTF-16, UTF-16-LE, UTF-16-BE, UTF-32, UTF-32-LE, UTF-32-BE

UCS-2, UCS-4, UTF-16 and UTF-32
'''''''''''''''''''''''''''''''

UCS-2 and UCS-4 encodings encode each code point to exaclty one word of, respectivelly,
16 and 32 bits. UCS-4 is able to encode all Unicode 6.0 code points, whereas
UCS-2 is limited to BMP characters (U+0000—U+FFFF). These encodings are
practical because the length in words is the number of characters.

UTF-16 and UTF-32 encodings use, respectivelly, 16 and 32 bits words. UTF-16
encodes code points bigger than U+FFFF using two words (see `UTF-16 surrogate
pairs`_). UCS-2 can be decoded by UTF-16. UTF-32 is also supposed to use two
words for big code points, but in practical, it only requires one word to store
all code points of Unicode 6.0. That's why UTF-32 and UCS-4 are the same
encoding.

Windows 95 used UCS-2, whereas Windows 2000 uses UTF-16.

.. note::

   UCS stands for *Universal Character Set*, and UTF stands for *UCS
   Transformation format*.


.. _BOM:
.. index:: BOM

Byte order marks (BOM)
''''''''''''''''''''''

`UTF-16`_ and `UTF-32`_ use words bigger than 8 bits, and so hit endian issue. A
single word can be stored in the big endian (most significant bits first) or
little endian (less significant bits first). BOM are short byte sequences to
indicate the encoding and the endian. It's the U+FEFF code point encoded to
the UTF encodings.

Unicode defines 6 different BOM:

 * ``0x2B 0x2F 0x76 0x38 0x2D`` (5 bytes): UTF-7 (endianless)
 * ``0xEF 0xBB 0xBF`` (3): `UTF-8`_ (endianless)
 * ``0xFF 0xFE`` (2): `UTF-16-LE`_ (LE: little endian)
 * ``0xFE 0xFF`` (2): `UTF-16-BE`_ (BE: big endian)
 * ``0xFF 0xFE 0x00 0x00`` (4): `UTF-32-LE`_
 * ``0x00 0x00 0xFE 0xFF`` (4): `UTF-32-BE`_

UTF-16-LE and UTF-32-LE BOMs start with the same 2 bytes sequence.

"UTF-16" and "UTF-32" encoding names are imprecise: depending of the context, format or
protocol, it means UTF-16 and UTF-32 with BOM markers, or UTF-16 and UTF-32 in
the host endian without BOM. On Windows, "UTF-16" usually means UTF-16-LE.

Some Windows applications, like notepad.exe, use UTF-8 BOM, whereas many
applications are unable to detect the BOM, and so the BOM causes troubles.
UTF-8 BOM should not be used for better interoperability.


.. index:: Surrogate pair

UTF-16 surrogate pairs
''''''''''''''''''''''

In `UTF-16`_, characters in ranges U+0000—U+D7FF and U+E000—U+FFFD are stored as
a single 16 bits word. Non-BMP characters (range U+10000—U+10FFFF) are stored
as "surrogate pairs", two 16 bits words: the first word is in the range
U+D800—U+DBFF, and the second word is in the range U+DC00—U+DFFF.

Example in `C`_ to encode/decode a non-BMP character to/from UTF-16 (using
surrogate pairs): ::

    void
    encode_utf16_pair(uint32_t character,
                      uint16_t *words)
    {
        unsigned int code;
        assert(character >= 0x10000);
        code = (character - 0x10000);
        words[0] = 0xD800 | (code >> 10);
        words[1] = 0xDC00 | (code & 0x3FF);
    }

    uint32_t
    decode_utf16_pair(uint16_t *words)
    {
        uint32_t code;
        assert(0xD800 <= words[0] && words[0] <= 0xDBFF);
        assert(0xDC00 <= words[1] && words[1] <= 0xDFFF);
        code = 0x10000;
        code += (words[0] & 0x03FF) << 10;
        code += (words[1] & 0x03FF);
        return code;
    }

A lone surrogate character is invalid in UTF-16, surrogate characters are
always written as pairs.


Other charsets and encodings
----------------------------

There are much more charsets and encodings, but it is not useful to know them.
The knowledge of a good conversion library, like iconv, is enough.


How to guess the encoding of a document?
----------------------------------------

Ony `ASCII`_, `UTF-8`_ and encodings using a `BOM`_ (UTF-7, UTF-8, `UTF-16`_,
and `UTF-32`_) have reliable algorithms to get the encoding of a
document. For all other encodings, you have to trust heuristics based on
statistics.


Is ASCII?
'''''''''

Check if a document is encoded to `ASCII`_ is simple: check that the bit 7 of each
byte is unset (``0b0xxxxxxx``).

Example in `C`_: ::

    int isASCII(const char *data, size_t size)
    {
        const unsigned char *str = (unsigned char*)data;
        const unsigned char *end = str + size;
        for (; str != end; str++) {
            if (*str & 0x80)
                return 0;
        }
        return 1;
    }

In `Python`_, the ASCII decoder can be used: ::

    def isASCII(data):
        try:
            data.decode('ASCII')
        except UnicodeDecodeError:
            return False
        else:
            return True


Check for BOM markers
'''''''''''''''''''''

If the string begins with a `BOM`_, the encoding
can be extracted from the BOM. But there is a problem with `UTF-16-BE`_ and
`UTF-32-LE`_: their BOMs start with the same 2 bytes sequence.

Example of a function written in `C`_ to check if a BOM is present: ::

    #include <string.h>   /* memcmp() */

    const char UTF_16_BE_BOM[] = "\xFE\xFF";
    const char UTF_16_LE_BOM[] = "\xFF\xFE";
    const char UTF_8_BOM[] = "\xEF\xBB\xBF";
    const char UTF_32_BE_BOM[] = "\x00\x00\xFE\xFF";
    const char UTF_32_LE_BOM[] = "\xFF\xFE\x00\x00";

    char* check_bom(const char *data, size_t size)
    {
        if (size >= 3) {
            if (memcmp(data, UTF_8_BOM, 3) == 0)
                return "UTF-8";
        }
        if (size >= 4) {
            if (memcmp(data, UTF_32_LE_BOM, 4) == 0)
                return "UTF-32-LE";
            if (memcmp(data, UTF_32_BE_BOM, 4) == 0)
                return "UTF-32-BE";
        }
        if (size >= 2) {
            if (memcmp(data, UTF_16_LE_BOM, 2) == 0)
                return "UTF-16-LE";
            if (memcmp(data, UTF_16_BE_BOM, 2) == 0)
                return "UTF-16-BE";
        }
        return NULL;
    }

For the UTF-16-LE/UTF-32-LE BOM conflict: this function returns ``"UTF-32-LE"``
if the string begins with ``"\xFF\xFE\x00\x00"``, even if this string can be
decoded from UTF-16-LE. Modify the function by adding other checks if you would
like a better heuristic to decide between these two encodings.

Example in `Python`_ getting the BOMs from the codecs library: ::

    from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

    BOMS = (
        (BOM_UTF8, "UTF-8"),
        (BOM_UTF32_BE, "UTF-32-BE"),
        (BOM_UTF32_LE, "UTF-32-LE"),
        (BOM_UTF16_BE, "UTF-16-BE"),
        (BOM_UTF16_LE, "UTF-16-LE"),
    )

    def check_bom(data):
        return [encoding for bom, encoding in BOMS if data.startswith(bom)]

This function is different from the C function: it returns a list. It returns
``['UTF-32-LE', 'UTF-16-LE']`` if the string begins with
``b"\xFF\xFE\x00\x00"``.

Is UTF-8?
'''''''''

`UTF-8`_ encoding adds markers to each bytes and so it's possible to write a
reliable algorithm to check if a function is encoded to UTF-8.


Example of a strict `C`_ function to check if a string is encoded to UTF-8. It
rejects overlong sequences (eg.  ``0xC0 0x80``) and surrogate characters (eg.
``0xED 0xB2 0x80``, U+DC80). ::

    #include <stdint.h>

    int isUTF8(const char *data, size_t size)
    {
        const unsigned char *str = (unsigned char*)data;
        const unsigned char *end = str + size;
        unsigned char byte;
        unsigned int code_length, i;
        uint32_t ch;
        while (str != end) {
            byte = *str;
            if (byte <= 0x7F) {
                /* 1 byte character (ASCII): U+0000..U+007F */
                str += 1;
                continue;
            }

            if (0xC2 <= byte && byte <= 0xDF)
                /* 0b110xxxxx: 2 bytes sequence */
                code_length = 2;
            else if (0xE0 <= byte && byte <= 0xEF)
                /* 0b1110xxxx: 3 bytes sequence */
                code_length = 3;
            else if (0xF0 <= byte && byte <= 0xF4)
                /* 0b11110xxx: 4 bytes sequence */
                code_length = 4;
            else {
                /* invalid first byte of a multibyte character */
                return 0;
            }

            if (str + (code_length - 1) >= end) {
                /* truncated string or invalid byte sequence */
                return 0;
            }

            /* Check continuation bytes: bit 7 should be set, bit 6 should be
             */ unset (b10xxxxxx). */
            for (i=1; i < code_length; i++) {
                if ((str[i] & 0xc0) != 0x80)
                    return 0;
            }

            if (code_length == 2) {
                /* 2 bytes sequence: U+0080..U+07FF */
                ch = ((str[0] & 0x1f) << 6) + (str[1] & 0x3f);
                if ((ch < 0x0080) || (0x07FF < ch))
                    return 0;
            } else if (code_length == 3) {
                /* 3 bytes sequence: U+0800..U+FFFF */
                ch = ((str[0] & 0x0f) << 12) + ((str[1] & 0x3f) << 6) +
                      (str[2] & 0x3f);
                if ((ch < 0x0800) || (0xFFFF < ch))
                    return 0;
                /* 3 bytes sequence: U+0800-U+FFFF... excluding U+D800-U+DFFF:
                 * surrogates are invalid in UTF-8 */
                if ((0xD800 <= ch) && (ch <= 0xDFFF))
                    return 0;
            } else if (code_length == 4) {
                /* 4 bytes sequence: U+10000..U+10FFFF */
                ch = ((str[0] & 0x07) << 18) + ((str[1] & 0x3f) << 12) +
                     ((str[2] & 0x3f) << 6) + (str[3] & 0x3f);
                if ((ch < 0x10000) || (0x10FFFF < ch))
                    return 0;
            }
            str += code_length;
        }
        return 1;
    }

In `Python`_, the UTF-8 decoder can be used: ::

    def isUTF8(data):
        try:
            data.decode('UTF-8')
        except UnicodeDecodeError:
            return False
        else:
            return True

In `Python 2`_, this function is more tolerant than the C function, because the
UTF-8 decoder of Python 2 accepts surrogate characters. For example,
``isUTF8(b'\xED\xB2\x80')`` returns ``True``. With `Python 3`_, the Python function is
equivalent to the C function. If you would like to reject surrogate characters
in Python 2, use the following strict function: ::

    def isUTF8Strict(data):
        try:
            decoded = data.decode('UTF-8')
        except UnicodeDecodeError:
            return False
        else:
            for ch in decoded:
                if 0xD800 <= ord(ch) <= 0xDFFF:
                    return False
            return True


Libraries
'''''''''

 * chardet_: `Python`_ version of the "chardet" algorithm implemented in Mozilla
 * UTRAC_: command line program (written in `C`_) to recognize the encoding of
   an input file and its end-of-line type
 * charguess_: Ruby library to guess the charset of a document

.. todo:: update/complete this list

.. _chardet: http://chardet.feedparser.org/
.. _charguess:  http://raa.ruby-lang.org/project/charguess/
.. _UTRAC: http://utrac.sourceforge.net/


.. index:: Unicode

Unicode
=======

What is Unicode?
----------------

Basic Multilingual Plane (BMP), or "Plane 0": range U+0000—U+FFFF. non-BMP
range: U+10000—U+10FFFF.

UTF codec family: `UTF-8`_, `UTF-16-LE`_ and `UTF-16-BE`_, `UTF-32-LE`_ and
`UTF-32-BE`_. There are some extra UTF encodings like UTF-7 and UTF-EBCDIC.

.. todo:: Explains how to display characters (left-to-right, right-to-left)

Categories
----------

Unicode has 7 character categories. Categories with examples and character
count of Unicode 6.0:

 * Letter (L)

   * lowercase (Ll): U+0264 (ɤ), U+0441 (с), U+1D07 (ᴇ),
     U+1D5FF (𝗿), U+1D68A (𝚊), … (1,759)
   * modifier (Lm): U+1D2D (ᴭ), U+1D44 (ᵄ), U+1D9B (ᶛ),
     U+1DB0 (ᶰ), … (210)
   * titlecase (Lt): U+01C5 (ǅ), U+1F8C (ᾌ), U+1F8F (ᾏ),
     U+1F9C (ᾜ), U+1FAB (ᾫ), … (31)
   * uppercase (Lu): U+0051 (Q), U+1F1A (Ἒ), U+1D469 (𝑩),
     U+1D4AB (𝒫), U+1D57B (𝕻), … (1,436)
   * other (Lo): U+8E96 (躖), U+B585 (떅), U+B92E (뤮), … (97,084)

 * Mark (M)

   * spacing combining (Mc): U+09C0 (ী), U+0B4C (ୌ), U+0DDE (ෞ),
     … (287)
   * enclosing (Me): U+20DD (⃝), U+20E0 (⃠), U+20E4 (⃤), … (12)
   * non-spacing (Mn): U+0357, U+0B3C, U+1A5E, U+1D180, U+E017D,
     … (1,199)

 * Number (N)

   * decimal digit (Nd): U+0666 (٦), U+0AEA (૪), … (420)
   * letter (Nl): U+216E (Ⅾ), U+2171 (ⅱ), … (224)
   * other (No): U+2490 (⒐), U+325E (㉞), U+32B9 (㊹), … (456)

 * Punctuation (P)

   * connector (Pc): U+2040 (⁀), U+2054 (⁔), U+FE34 (︴), U+FE4D (﹍),
     U+FF3F (＿), … (10)
   * dash (Pd): U+2010 (‐), U+2011 (‑), U+FE63 (﹣), … (21)
   * initial quote (Pi): U+2018 (‘), U+201B (‛), … (12)
   * final quote (Pf): U+00BB (»), U+2019 (’), U+203A (›), … (10)
   * open (Ps): U+27E8 (⟨), U+2993 (⦓), U+2995 (⦕), U+301D (〝),
     U+FE41 (﹁), … (72)
   * close (Pe): U+276F (❯), U+300B (》), U+FE36 (︶), U+FE5C (﹜),
     U+FF5D (｝), … (71)
   * other (Po): U+0F06 (༆), U+2047 (⁇), U+FF3C (＼), … (402)

 * Symbol (S)

   * currency (Sc): U+0AF1 (૱), U+20A6 (₦), U+20B3 (₳), U+20B4 (₴),
     … (47)
   * modifier (Sk): U+00AF (¯), U+02D4 (˔), U+02E9 (˩), U+02F7 (˷),
     U+A70D (꜍), … (115)
   * math (Sm): U+2211 (∑), U+27D1 (⟑), U+293F (⤿), U+2AF0 (⫰),
     U+2AF4 (⫴), … (948)
   * other (So): U+0FC4 (࿄), U+2542 (╂), … (4398)

 * Separator (Z: 20)

   * line (Zl): U+2028
   * paragraph (Zp): U+2029
   * space (Zs): U+00A0, U+2003, U+2004, U+2007, U+2009, … (18)

 * Other (C)

   * control (Cc): U+0007, U+000A, U+0090, U+009E, … (65)
   * format (Cf): U+200B, U+2062, U+E0043, U+E004A, U+E0063, … (140)
   * not assigned (Cn): U+4D67A, U+51797, U+A63FB, U+D0F5B, U+D9791,
     … (865,146)
   * private use (Co): U+E000—U+F8FF (6400), U+F0000—U+FFFFD (65534),
     U+100000—U+10FFFD (65534); total = 137,468
   * surrogate (Cs): U+D800—U+DFFF (2048)

Statistics
----------

77.6% of all codes are not assigned. Statistics excluding not assigned (Cn),
private use (Co) and surrogate (Cs) categories:

 * Letter: 100,520 (91.8%)
 * Symbol: 5,508 (5.0%)
 * Mark: 1,498 (1.4%)
 * Number: 1,100 (1.0%)
 * Punctuation: 598 (0.5%)
 * Other: 205 (0.2%)
 * Separator: 20 (0.0%)

Normalization
-------------

Unicode standard explains how to decompose a character, eg. the precomposed
character ç (U+00C7, Latin capital letter C with cedilla) can be written as the
sequence ¸̧ (U+0327, Combining cedilla) c (U+0043, Latin capital letter C), two
characters. This decomposition can be useful to search a substring in a text,
eg. remove diacritic is pratical for the user. The decomposed form is called
Normal Form D (NFD) and the precomposed form is called Normal Form C (NFC).

+------+--------+----------------+
| Form | String | Unicode        |
+======+========+================+
| NFC  | ç      | U+00C7         |
+------+--------+----------------+
| NFD  | ,c     | U+0327, U+0043 |
+------+--------+----------------+

.. todo:: rst doesn't accept diacritics (U+0327) in a table cell: | NFD | ¸̧c | U+0327, U+0043 |

Unicode database contains also a compatibility layer: if a character cannot be
rendered (no font contain the requested character) or encoded to a specific
encoding, Unicode proposes a replacment character sequence which looks like the
character, but may have a different meaning. For example, ĳ (U+0133, Latin small
ligature ij) is replaced by i (U+0069, Latin small letter I) j (U+006A, Latin
small letter J), two characters. ĳ character cannot be encoded to `ISO-8859-1`_,
whereas ij characters can. Two extra normal forms use this compatibility layer:
NFKD (decomposed) and NFKC (precomposed).

.. note::

   The precomposed forms (NFC and NFKC) begin by a canonical decomposition
   before recomposing pre-combined characters again.


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
   using the `ANSI code page`_ for applications using bytes strings.
 * Mac OS X encodes filenames to `UTF-8`_ and normalize see to a variant of the
   Normal Form D (see `Mac OS X`_).
 * Other OSes: use the locale encoding

See also `How to guess the encoding of a document?`_ section.


Operating systems
=================

Microsoft Windows
-----------------

.. index: Code page
.. _ANSI code page:
.. _OEM code page:

Code pages
''''''''''

An application has two encodings, called `code pages`_ (abbreviated "cp"): the
ANSI code page (:c:macro:`CP_ACP`) used for the ANSI version of the Windows API to decode a byte
string to a character string, and the OEM code page (:c:macro:`CP_OEMCP`), eg. used for the console.
Example of a French setup: `cp1252`_ for ANSI and cp850 for OEM.

OEM code pages, or "IBM PC" code pages, have a number between 437 and 874 and
come from MS-DOS. They contain graphical glyphs to create text interfaces (draw
boxes). ANSI code pages have numbers between 874 and 1258. There are some
special code pages like 65001 (Microsoft version of `UTF-8`_).

Get code pages.

.. c:function:: UINT GetACP()

   Get the ANSI code page number.

.. c:function:: UINT GetOEMCP()

   Get the OEM code page number.

Conversion.

.. c:function:: BOOL OemToCharW(LPCSTR src, LPWSTR dst)

   Decode a byte string from the OEM code page.

.. c:function:: BOOL CharToOemW(LPCWSTR src, LPSTR dst)

   Encode a character string to the OEM code page.

.. c:function:: BOOL AnsiToCharW(LPCSTR src, LPWSTR dst)

   Decode a byte string from the ANSI code page.

.. c:function:: BOOL CharToAnsiW(LPCWSTR src, LPSTR dst)

   Encode a character string to the ANSI code page.

.. _code pages:
   http://en.wikipedia.org/wiki/Windows_code_page


ANSI and Unicode versions of each function
''''''''''''''''''''''''''''''''''''''''''

Windows has two versions of each function of its API : the ANSI version using
byte strings (function name ending with "A") and the `ANSI code page`_, and the wide character version
(name ending with "W"). There are also functions without suffix using
:c:type:`TCHAR*` strings: if the `C`_ define :c:macro:`_UNICODE` is defined, :c:type:`TCHAR` is
:c:type:`wchar_t` and it use the Unicode functions; otherwise :c:type:`TCHAR` is char
and it uses the ANSI functions. Example:

 * :c:func:`CreateFileA()`: bytes version, use byte strings encoded to the ANSI code page
 * :c:func:`CreateFileW()`: Unicode version, use wide character strings
 * :c:func:`CreateFile()`: :c:type:`TCHAR` version depending on the :c:macro:`_UNICODE` define


Encode and decode functions
'''''''''''''''''''''''''''

Encode and decode functions of ``<windows.h>``.

.. c:function:: MultiByteToWideChar()

   Decode a byte string to a character string (similar to
   :c:func:`mbstowcs`). It supports the `ANSI code page`_ and `OEM code page`_, UTF-7 and `UTF-8`_. By default,
   it ignores undecodable bytes. Use :c:macro:`MB_ERR_INVALID_CHARS` flag to raise an
   error on an invalid byte sequence.

.. c:function:: WideCharToMultiByte()

   Encode a character string to a byte string (similar to
   :c:func:`wcstombs`). As :c:func:`MultiByteToWideChar`, it supports `ANSI code page`_ and the `OEM code page`_,
   UTF-7 and `UTF-8`_. By default, if a character cannot be encoded, it is
   replaced by a character with a similar glyph. For example, with `cp1252`_, Ł (U+0141) is replaced
   by L (U+004C). Use :c:macro:`WC_NO_BEST_FIT_CHARS` flag to raise an error on
   unencodable character.


Filenames
'''''''''

Windows stores filenames as Unicode in the filesystem. Filesystem wide
character POSIX-like API:

.. c:function:: int _wfstat(const wchar_t* filename, struct _stat *statbuf)

   Unicode version of :c:func:`stat()`.

.. c:function:: FILE *_wfopen(const wchar_t* filename, const wchar_t *mode)

   Unicode version of :c:func:`fopen`.

POSIX functions, like :c:func:`fopen()`, use the `ANSI code page`_ to encode/decode
strings.


Windows console
'''''''''''''''

Console functions.

.. c:function:: GetConsoleCP()

   Get the ccode page of the standard input (stdin) of the console.

.. c:function:: GetConsoleOutputCP()

   Get the code page of the standard output (stdout and stderr) of the console.

In a console (``cmd.exe``), ``chcp`` command can be used to display or to
change the `OEM code page`_ (and console code page). Change the console code page is not a
good idea because the ANSI API of the console still expect characters encoded
to the previous console code page.

If the console is unable to render a character, it tries to use a character
with a similar glyph: eg. Ł (U+0141) is replaced by L (U+0041). If no
replacment character can be found, "?" (U+003F) is displayed instead.

To improve the support of Unicode in a console:

 * Set the code page to cp65001 using the ``chcp`` command
 * Set the console font to "Lucida Console"
 * Use the Unicode version of the API

:c:func:`_setmode` and :c:func:`_wsopen` are special functions to set the encoding of a
file (especially of stdin, stdout and stderr):

 * :c:macro:`_O_U8TEXT`: `UTF-8`_ without `BOM`_
 * :c:macro:`_O_U16TEXT`: `UTF-16`_ without BOM
 * :c:macro:`_O_WTEXT`: UTF-16 with BOM

See also `Conventional wisdom is retarded, aka What the @#%&* is _O_U16TEXT?`_
(Michael S. Kaplan, 2008).

.. _Conventional wisdom is retarded, aka What the @#%&* is _O_U16TEXT?:
   http://blogs.msdn.com/b/michkap/archive/2008/03/18/8306597.aspx


MS-DOS
''''''

Windows inherits from MS-DOS. MS-DOS has also code pages. Commands:

 * ``MODE CON CODEPAGE``: display the current code page
 * ``MODE CON CODEPAGE SELECT=xxx``: set the current code page
 * ``MODE CON CODEPAGE PREPARE=((850)``
 * ``MODE CON CODEPAGE PREPARE=((863,850) C:\WINDOWS\COMMAND\EGA.CPI)``

``CON`` stands for the console device, but another device name can be
specified: ``PRN`` (printer), ``LPT1``, ``LPT2`` or ``LPT3``.


Mac OS X
--------

Mac OS X uses `UTF-8`_ for the filenames. If a filename is an invalid UTF-8 byte
string, Mac OS raises an error. The filenames are decomposed using an
(incompatible) variant of the Normal Form D: `Technical Q&A QA1173`_ (see
`Normalization`_).

"For example, HFS Plus uses a variant of Normal Form D in which U+2000 through
U+2FFF, U+F900 through U+FAFF, and U+2F800 through U+2FAFF are not decomposed."

.. _Technical Q&A QA1173:
   http://developer.apple.com/mac/library/qa/qa2001/qa1173.html


.. _Locales:

Locales (UNIX and BSD)
----------------------

To support different languages and encodings, UNIX and BSD operating systems
have "locales". Locales are process-wide: if a thread or a library change
the locale, the whole process is impacted.


Locale categories
'''''''''''''''''

Locale categories:

 * :c:macro:`LC_COLLATE`: compare and sort strings
 * :c:macro:`LC_CTYPE`: encode and decode characters, "C" locale usually means 7 bits
   `ASCII`_ (not always, see below)
 * :c:macro:`LC_MESSAGES`: language of messages (gettext), "C" locale means English
 * :c:macro:`LC_MONETARY`: monetary formatting
 * :c:macro:`LC_NUMERIC`: number formatting (eg. thousands separator)
 * :c:macro:`LC_TIME`: time and date formatting

:c:macro:`LC_ALL` is a special category: if you set a locale using this category, it sets
the locale for all categories.

Each category has its own environment variable with the same name. For example,
``LC_MESSAGES=C`` displays error messages in English. To get the value of a locale
category, ``LC_ALL``, ``LC_xxx`` (eg. ``LC_CTYPE``) or ``LANG`` environment variables are
checked: use the first non empty variable. If all variables are unset,
fallback to the C locale.

The "C" locale is a special locale. It is also known as "POSIX". It is used if
``LC_ALL``, ``LC_xxx`` and ``LANG`` environment variables are not set. As English is used
as the default language, use C locale means that programs speak English.

Locale codec
''''''''''''

For Unicode, the most important locale category is ``LC_CTYPE``: it is used to set
the "locale encoding".

For the C locale, ``nl_langinfo(CODESET)`` returns ASCII, or an alias to this
encoding (eg. "US-ASCII" or "646"). But on FreeBSD, Solaris and Mac OS X,
codec functions (eg. :c:func:`mbstowcs`) use `ISO-8859-1`_ even if ``nl_langinfo(CODESET)``
announces ASCII encoding.

``<locale.h>`` functions.

.. c:function:: char* setlocale(category, NULL)

   Get the current locale of the specified category.

.. c:function:: char* setlocale(category, name)

   Set the locale of the specified category.

``<langinfo.h>`` functions.

.. c:function::  char* nl_langinfo(CODESET)

   Get the name of the locale encoding.

``<stdlib.h>`` functions.

.. c:function:: size_t mbstowcs(wchar_t *dest, const char *src, size_t n)

   Decode a byte string from the locale encoding to a character string.  Raise
   an error on undecodable byte sequence. If available, always prefer the
   reentrant version: :c:func:`mbsrtowcs`.

.. c:function:: size_t wcstombs(char *dest, const wchar_t *src, size_t n)

   Encode a character string to a byte string in the locale encoding. Raise an
   error if a character cannot by encoded. If available, always prefer the
   reentrant version: :c:func:`wcsrtombs`.

.. note::

   "mbs" means "multibyte string" (byte string) and "wcs" means "wide character
   string".


Programming languages
=====================

.. _C:

C language
----------

Byte API (char)
'''''''''''''''

.. c:type:: char

    For historical reasons, :c:type:`char` is the C type for a character ("char" as
    "character"). In pratical, it's only true for 7 and 8 bits encodings like `ASCII`_
    or `ISO-8859-1`_. With multibyte encodings, a :c:type:`char` is only one byte. For example, the
    character "é" (U+00E9) is encoded as two bytes (``0xC3 0xA9``) in `UTF-8`_.

    :c:type:`char` is a 8 bits byte, it may be signed depending on the operating system and
    the compiler. On Linux, gcc uses a signed type for Intel CPU. The GNU compiler
    defines :c:macro:`__CHAR_UNSIGNED__` if :c:type:`char` type is unsigned. You can use :c:macro:`CHAR_MAX`
    constant from ``<limits.h>`` to check if :c:type:`char` is signed or not.

    A literal character is written between apostrophes, eg. ``'a'``. Some control
    characters can be written with an backslash plus a letter (eg. ``'\n'`` = 10).
    It's also possible to write the value in octal (eg. ``'\033'`` = 27) or
    hexadecimal (eg. ``'\x20'`` = 32). An apostrophe can be written ``'\''`` or
    ``'\x27'``. A backslash is written ``'\\'``.

    ``<ctype.h>`` contains functions to manipulate characters, like :c:func:`toupper` or
    :c:func:`isprint`.

Byte string API (char*)
'''''''''''''''''''''''

.. c:type:: char*

   :c:type:`char*` is a character string (a byte string for multibyte encodings). This type
   is used in many places in the C standard library. For example, :c:func:`fopen` uses :c:type:`char*`
   for the filename.

   ``<string.h>`` is the (byte) string library. Most functions starts with "str"
   (string) prefix: :c:func:`strlen`, :c:func:`strcat`, etc. ``<stdio.h>`` contains useful string
   functions like :c:func:`snprintf` to format a message.

   The length of a string is stored as a nul byte at the end of the string. This
   is a problem with encodings using nul bytes (eg. `UTF-16`_ and `UTF-32`_): :c:func:`strlen()`
   cannot be used to get the length of the string, whereas most C functions
   suppose that :c:func:`strlen` gives the length of the string. To support such
   encodings, the length should be stored differently (eg. in another variable or
   function argument) and :c:func:`str*` functions should be replaced by :c:type:`mem*`
   functions (eg. replace ``strcmp(a, b) == 0`` by ``memcmp(a, b) == 0``).

   A literal byte strings is written between quotes, eg. ``"Hello World!"``. As byte
   literal, it's possible to add control characters and characters in octal or
   hexadecimal, eg. ``"Hello World!\n"``.

Character API (wchar_t)
'''''''''''''''''''''''

.. c:type:: wchar_t

   With ISO C99 comes :c:type:`wchar_t`: the wide character type. It can be used to store
   Unicode characters. As :c:type:`char`, it has a character library: ``<wctype.h>`` which
   contains functions like :c:func:`towupper` or :c:func:`iswprint`.

   :c:type:`wchar_t` is a 16 or 32 bits integer, and it may be signed or not. Linux uses 32
   bits signed integer. Mac OS X uses 32 bits integer. Windows uses 16 bits
   integer.

   A literal character is written between apostrophes with the ``L`` prefix, eg.
   ``L'a'``. As byte literal, it's possible to write control character with an
   backslash and a character with its value in octal or hexadecimal. For codes
   bigger than 255, ``'\uHHHH'`` syntax can be used. For codes bigger than 65535,
   ``'\UHHHHHHHH'`` syntax can be used with 32 bits :c:type:`wchar_t`.


Character string API (wchar_t*)
'''''''''''''''''''''''''''''''

.. c:type:: wchar_t*

   :c:type:`wchar_t*` is a character string. The standard library ``<wchar.h>`` contains
   character string functions like :c:func:`wcslen` or :c:func:`wprintf`, and constants
   like WCHAR_MAX. If :c:type:`wchar_t` is 16 bits long, non-BMP characters are encoded
   to `UTF-16`_ using surrogate pairs (see `UTF-16 surrogate pairs`_).

   A literal character strings is written between quotes with the ``L``
   prefix, eg. ``L"Hello World!\n"``. As character literals, it supports also control
   character, codes written in octal, hexadecimal, ``L"\uHHHH"`` and ``L"\UHHHHHHHH"``.


printf functions family
'''''''''''''''''''''''

.. c:function:: int printf(const char* format, ...)

.. c:function:: int wprintf(const wchar_t* format, ...)


Formats of string arguments for the printf functions:

 * ``"%s"``: literal byte string (:c:type:`char*`)
 * ``"%ls"``: literal character string (:c:type:`wchar_t*`)

:c:func:`printf` stops immediatly if a character cannot be encoded to the locale
encoding. For example, the following code prints the truncated string "Latin
capital letter L with stroke: [" if U+0141 (Ł) cannot be encoded to the locale
encoding. ::

    printf("Latin capital letter L with stroke: [%ls]\n", L"\u0141");

:c:func:`wprintf` function stops immediatly if a byte string argument cannot be decoded
from the current locale encoding. For example, the following code prints the
truncated string "Latin capital letter L with stroke: [" if ``0xC5 0x81``
(U+0141 encoded to UTF-8) cannot be decoded from the locale encoding. ::

    wprintf(L"Latin capital letter L with stroke): [%s]\n", "\xC5\x81");

``wprintf("%ls")`` replaces unencodable characters by "?" (U+003F). For example,
the following example print "Latin capital letter L with stroke: [?]"
with a newline if U+0141 (Ł) cannot be encoded to the locale encoding: ::

    wprintf(L"Latin capital letter L with stroke: [%s]\n", L"\u0141");

So to avoid truncated strings because of non-ASCII characters, try to use only
:c:func:`wprintf` with character string arguments.

.. note::

   There is also ``"%S"`` format which is a deprecated alias to the ``"%ls"``
   format, don't use it.


C++
---

 * ``std::wstring``: character string using the :c:type:`wchar_t` type, unicode
   version of ``std::string``
 * ``std::wcin``, ``std::wcout`` and ``std::wcerr``: standard input, output
   and error output; unicode version of ``std::cin``, ``std::cout`` and
   ``std::cerr``
 * ``std::wostringstream``: character stream buffer; unicode version of
   ``std::ostringstream``.

To initialize the locales (see `Locales`_), equivalent to ``setlocale(LC_ALL,
"")``, use: ::

    #include <locale>
    std::locale::global(std::locale(""));

If you use also C functions (eg. :c:func:`printf`) to access the stdio streams, you
may have issues with non-ASCII characters. To avoid these issues, you can
disable the automatic synchronization between C (``std*``) and C++
(``std::c*``) streams using: ::

    #include <iostream>
    std::ios_base::sync_with_stdio(false);

.. note::

   Use ``typedef basic_ostringstream<wchar_t> wostringstream`` if
   wostringstream is not available.


Python
------

Python supports Unicode since its version 2.0 released in october 2000. Byte
and Unicode strings store their length, so it's possible to embed nul
byte/character.

Python can be compiled in two modes: narrow (`UTF-16`_) and wide (`UCS-4`_).
``sys.maxunicode`` constant is 0xFFFF in narrow mode, and 0x10FFFF in wide mode.
Python is compiled in narrow mode on Windows, because :c:type:`wchar_t` is also 16 bits
on Windows and so it is possible to use Python Unicode strings as :c:type:`wchar_t*`
strings without any (expensive) conversion.

See also the `Python Unicode HOWTO`_.


Python 2
''''''''

``str`` is the type of byte strings and ``unicode`` is the type of character
(Unicode) strings. Literal byte strings are written ``b'abc'`` (syntax
compatible with Python 3) or ``'abc'`` (legacy syntax), ``\xHH`` can be used to
write a byte by its hexadecimal value (eg. ``b'\x80'`` for 128). Literal
Unicode strings are written with the prefix ``u``: ``u'abc'``. Code points can
be used directly in hexadecimal: ``\xHH`` (U+0000—U+00FF), ``\uHHHH``
(U+0100—U+FFFF) or ``\UHHHHHHHH`` (U+10000—U+10FFFF), eg. ``'euro
sign:\u20AC'``.

In Python 2, ``str + unicode`` gives ``unicode``: the byte string is
decoded from the default encoding (`ASCII`_). This coercion was a bad design idea
because it was the source of a lot of confusion. At the same time, it was not
possible to switch completly to Unicode in 2000: computers were slower and
there were fewer Python core developers. It took 8 years to switch completly to
Unicode: Python 3 was relased in december 2008.

Narrow mode of Python 2 has a partial support of non-BMP characters. unichr()
function raise an error for code bigger than U+FFFF, whereas literal strings
support non-BMP characters (eg. ``'\U00010000'``). Non-BMP characters are
encoded as surrogate pairs (see `UTF-16 surrogate pairs`_). The disavantage is
that ``len(u'\U00010000')`` is 2, and ``u'\U00010000'[0]`` is ``u'\uDC80'``
(lone surrogate character).

In Python 2, it is possible to change the default encoding, but it is a bad idea
because it impacts all libraries which may suppose that the default encoding is
ASCII.


Python 3
''''''''

``bytes`` is the type of byte strings and ``str`` is the type of character
(Unicode) strings. Literal byte strings are written with the prefix ``b``:
``b'abc'`` (syntax compatible with Python 2), ``\xHH`` can be used to write a
byte by its hexadecimal value (eg. ``b'\x80'`` for 128). Literal Unicode strings are
written ``u'abc'``. Code points can be used directly in hexadecimal: ``\xHH``
(U+0000—U+00FF), ``\uHHHH`` (U+0100—U+FFFF) or ``\UHHHHHHHH``
(U+10000—U+10FFFF), eg. ``'euro sign:\u20AC'``. Each byte of a byte string is
an integer in range 0—255: ``b'abc'[0]`` gives 97; whereas ``'abc'[0]`` gives
``'a'``.

Python 3 has a full support of non-BMP characters, in narrow and wide modes.
But as Python 2, chr(0x10FFFF) creates a string of 2 characters (a UTF-16
surrogate pair, see `UTF-16 surrogate pairs`_) in a narrow mode. ``chr()`` and
``ord()`` supports non-BMP characters in both modes.

Python 3 uses U+DC80—U+DCFF character range to store undecodable bytes with the
``surrogateescape`` error handler, described in the `PEP 383`_ (*Non-decodable
Bytes in System Character Interfaces*). It is used for filenames and
environment variables on UNIX and BSD systems. Example:
``b'abc\xff'.decode('ASCII', 'surrogateescape')`` gives ``'abc\uDCFF'``.


Differences between Python 2 and Python 3
'''''''''''''''''''''''''''''''''''''''''

``str + unicode`` gives ``unicode`` in Python 2 (the byte string is decoded
from the default encoding, `ASCII`_) and it raises a ``TypeError`` in Python 3. In
Python 3, comparing ``bytes`` and ``str`` emits a ``BytesWarning`` warning or
raise a ``BytesWarning`` exception depending of the bytes warning flag (``-b``
or ``-bb`` option passed to the Python program). In Python 2, the byte string
is decoded to Unicode using the default encoding (ASCII) before being compared.

`UTF-8`_ decoder of Python 2 accept surrogate characters, even if there are
invalid, to keep backward compatibility with Python 2.0. In Python 3, the
decoder rejects surrogate characters.


.. _Python Unicode HOWTO:
   http://docs.python.org/howto/unicode.html
.. _PEP 383:
   http://www.python.org/dev/peps/pep-0383/


Codecs
''''''

Python has a ``codecs`` module providing text encodings. It supports a lot of
encodings, some examples: ``ASCII``, ``ISO-8859-1``, ``UTF-8``, ``UTF-16-LE``,
``ShiftJIS``, ``Big5``, ``cp037``, ``cp950``, ``EUC_JP``, etc. ``UTF-8``,
``UTF-16-LE``, ``UTF-16-BE``, ``UTF-32-LE`` and ``UTF-32-BE`` don't use `BOM`_,
whereas ``UTF-8-SIG``, ``UTF-16`` and ``UTF-32`` use BOM. ``mbcs`` is the `ANSI
code page`_ and so is only available on Windows.

Python provides also many error handlers used to specify how to handle
undecodable bytes / unencodable characters:

 * ``strict`` (default): raise ``UnicodeDecodeError`` / ``UnicodeEncodeError``
 * ``replace`` replace undecodable bytes by � (U+FFFD) and unencodable
   characters by ``?`` (U+003F)
 * ``ignore``: ignore undecodable bytes / unencodable characters
 * ``backslashreplace`` (only to decode): replace undecodable bytes by ``\xHH``
   (U+0000—U+00FF), ``\uHHHH`` (U+0100—U+FFFF)  or ``\UHHHHHHHH``
   (U+10000—U+10FFFF)

Python 3 has two more error handlers:

 * ``surrogateescape``: replace undecodable bytes (non-ASCII: ``0x80``\ —\
   ``0xFF``) by surrogate characters (in U+DC80—U+DCFF), and replace characters
   in range U+DC80—U+DCFF by bytes in ``0x80``\ —\ ``0xFF``.  Read the `PEP
   383`_ (*Non-decodable Bytes in System Character Interfaces*) for the
   details.
 * ``surrogatepass``, specific to ``UTF-8`` codec: allow encoding/decoding
   surrogate characters in `UTF-8`_. It is required because UTF-8 decoder of
   Python 3 rejects surrogate characters.

Examples with Python 3:

 * ``b'abc\xff'.decode('ASCII', 'ignore')`` gives ``'abc'``
 * ``b'abc\xff'.decode('ASCII', 'replace')`` gives ``'abc\uFFFD'``
 * ``b'abc\xff'.decode('ASCII', 'surrogateescape')`` gives
   ``'abc\uDCFF'``
 * ``'abc\xff'.encode('ASCII', 'backslashreplace')`` gives ``b'abc\\xff'``
 * ``'\u20ac'.encode('UTF-8')`` gives ``b'\xe2\x82\xac'``


String methods
''''''''''''''

Byte string (``str`` / ``bytes``) methods:

 * ``.decode(encoding, errors='strict')``: decode from the specified encoding
   and (optional) error handler.

Character string (``unicode`` / ``str``) methods:

 * ``.encode(encoding, errors='strict')``: encode to the specified encoding
   and (optional) error handler
 * ``.isprintable()``: ``False`` if the character category is other (Cc, Cf, Cn, Co, Cs)
   or separator (Zl, Zp, Zs), ``True`` otherwise. There is an exception: even if
   U+0020 is a separator, ``' '.isprintable()`` gives ``True``.
 * ``.toupper()``: convert to uppercase


Modules
'''''''

``codecs`` module:

 * ``BOM_UTF8``, ``BOM_UTF16_BE``, ``BOM_UTF32_LE``, ...: UTF `BOM`_ constants
 * ``lookup(name)``: get a Python codec. ``lookup(name).name`` gets the Python
   normalized name of a codec, eg. ``codecs.lookup('ANSI_X3.4-1968').name``
   gives ``'ascii'``.
 * ``open(filename, mode='rb', encoding=None, errors='strict', ...)``: legacy
   API to open a text file in Unicode mode, use ``io.open()`` instead

``io`` module:

 * ``open(name, mode='r', buffering=-1, encoding=None, errors=None, ...)``:
   open a binary or text file in read and/or write mode. For text file,
   ``encoding`` and ``errors`` can be used to specify the encoding. Otherwise,
   Python uses the locale encoding in strict mode.
 * ``TextIOWrapper()``: wrapper to read and/write text files, encode from/decode to
   the specified encoding (and error handler) and normalize newlines. It requires
   a buffered file. Don't use it directly to open a text file: use ``open()``
   instead.

``locale`` module (see `Locales`_):

 * ``getlocale(category)``: get the value of a locale category as the tuple
   (language code, encoding)
 * ``getpreferredencoding()``: get the locale encoding
 * ``LC_ALL``, ``LC_CTYPE``, ...: `locale categories`_
 * ``setlocale(category, value)``: set the value of a locale category

``sys`` module:

 * ``getdefaultencoding()``: get the default encoding, eg. used by
   ``'abc'.encode()``. In Python 3, the default encoding is fixed to
   ``'utf-8'``, in Python 2, it's ``'ascii'`` by default.
 * ``maxunicode``: biggest Unicode code point storable in a single Python
   Unicode character, 0xFFFF in narrow mode or 0x10FFFF in wide mode.

``unicodedata`` module:

 * ``category(char)``: get the category of a character
 * ``name(char)``: get the name of a character
 * ``normalize(string)``: normalize a string to the NFC, NFD, NFKC or NFKD form



PHP
---

In PHP 5, a literal string (eg. ``"abc"``) is a byte string. PHP has no Unicode type,
only a "string" type which is a byte string.  But PHP have "multibyte"
functions to manipulate character strings. These functions have an optional
encoding argument. If the encoding is not specified, PHP uses the default
encoding (called "internal encoding"). mb_internal_encoding() function can be
used to get or set the internal encoding. mb_substitute_character() can be used
to change how to encode unencodable characters:

 * ``"none"``: ignore unencodable characters
 * ``"long"``: escape as hexadecimal value, eg. ``"U+E9"`` or ``"JIS+7E7E"``
 * ``"entity"``: escape as HTML entity, eg. ``"&#xE9;"``

Some multibyte functions:

 * ``mb_convert_encoding()``: decode from an encoding and encode to another
   encoding
 * ``mb_ereg()``: search a pattern using a regular expression
 * ``mb_strlen()``: length of a character string

.. todo:: Howto get $_POST and $_GET encoding
.. todo:: Howto get uri encoding

PHP 6 was a project to improve Unicode support of Unicode. This project died at
the beginning of 2010. Read `The Death of PHP 6/The Future of PHP 6`_ (May 25,
2010 by Larry Ullman) and `Future of PHP6`_ (March 2010 by Johannes Schlüter)
for more information.

.. _The Death of PHP 6/The Future of PHP 6:
   http://blog.dmcinsights.com/2010/05/25/the-death-of-php-6the-future-of-php-6/
.. _Future of PHP6:
   http://schlueters.de/blog/archives/128-Future-of-PHP-6.html


Perl
----

 * Perl 5.6 (2000): initial Unicode support, store strings as characters
 * Perl 5.8 (2002): regex supports Unicode
 * use "``use utf-8;``" pragma to specify that your Perl script is encoded in
   `UTF-8`_

Read perluniintro, perlunicode and perlunifaq manuals.


Java
----

``char`` is a character able to store Unicode BMP only characters
(U+0000—U+FFFF), whereas ``Character`` is a character able to store any Unicode
character (U+0000—U+10FFFF). ``Character`` methods:

 * ``.getType(ch)``: get the Unicode category (see `Categories`_) of a
   character
 * ``.isWhitespace(ch)``: test if a character is a whitespace
   according to Java
 * ``.toUpperCase(ch)``: convert to uppercase

``String`` is a character strings implemented using a ``char`` array, `UTF-16`_
characters. ``String`` methods:

 * ``String(bytes, encoding)``: decode a byte string from the specified
   encoding, throw a ``CharsetDecoder`` exception if a byte sequence cannot be
   decoded.
 * ``.getBytes(encoding)``: encode to the specified encoding, throw a
   ``CharsetEncoder`` exception if a character cannot be encoded.
 * ``.length()``: length in UTF-16 characters.

As `Python`_ compiled in narrow mode, non-BMP characters are stored as `UTF-16
surrogate pairs`_ and the length of a string is the number of UTF-16
characters, not the length in Unicode characters.

Java uses a variant of `UTF-8`_ which encodes the nul character (U+0000) as the
overlong byte sequence ``0xC0 0x80``, instead of ``0x00``. This is be able to
use `C`_ functions like :c:func:`strlen`. The Tcl language uses the same encoding.


Libraries
=========

Qt library
----------

Qt is a big `C++`_ library covering different topics, but it is typically used
to create graphical interfaces. It is distributed under the `GNU LGPL license`_
(version 2.1), but it is also available under a commercial license.

Character and string
''''''''''''''''''''

``QString`` is a character string: each character is stored as a ``QChar``.
Interesting ``QString`` methods:

 * ``toAscii()``, ``fromAscii()``: encode to/decode from `ASCII`_
 * ``toLatin1()``, ``fromLatin1()``: encode to/decode from `ISO-8859-1`_
 * ``utf16()``, ``fromUtf16()``: encode to/decode to `UTF-16`_
 * ``normalized()``: normalize to NFC, NFD, NFKC or NFKD (see `Normalization`_)

Qt decodes string literals using the QLatin1String class. It is a thin wrapper
to const char* strings. QLatin1String stores a character as a single byte. It
is possible because it only supports characters in range U+0000—U+00FF.
QLatin1String are smaller than ``QString`` because they cannot be used to
manipulate text, eg. it is not possible to concatenate two QLatin1String
strings.

``QChar`` is a 16 bits Unicode character. Interesting ``QChar`` methods:

 * ``isSpace()``: True if the character category is separator
 * ``toUpper()``: convert to upper case

Codec
'''''

``QTextCodec.codecForLocale()`` gets the locale codec. The locale codec is:

 * Windows: `ANSI code page`_
 * The locale encoding otherwise: try ``nl_langinfo(CODESET)``, or ``LC_ALL``,
   ``LC_CTYPE``, ``LANG`` environment variables. If no one gives any useful information,
   fallback to `ISO-8859-1`_.


Filesystem
''''''''''

``QFile.encodeName()``:

 * Windows: encode to `UTF-16`_
 * Mac OS X: normalize the name to the D form and then encode to `UTF-8`_
 * Other (UNIX/BSD): encode to the local encoding (``QTextCodec.codecForLocale()``)

``QFile.decodeName()`` is the reverse operation.

Qt has two implementations of its ``QFSFileEngine``:

 * Windows: use Windows native API
 * Unix: use POSIX API. Examples: ``fopen()``, ``getcwd()`` or ``get_current_dir_name()``,
   ``mkdir()``, etc.

Classes: ``QFile``, ``QFileInfo``, ``QAbstractFileEngineHandler``, ``QFSFileEngine``.


Gtk+ and glib libraries
-----------------------

`Gtk+`_ is a `C`_ toolkit to create graphic interfaces, based on the glib library.
Both projects are distributed under the `GNU LGPL license`_ (version 2.1). The
glib library uses the `UTF-8`_ encoding as internal encoding to store character
strings using :c:type:`gchar*` `C`_ type. There is also :c:type:`gunichar` C type to store a
single code point able to store any Unicode 6.0 character (U+0000—U+10FFFF).

Functions:

 * :c:func:`g_get_charset`: chraset of the current locale

   * Windows: `ANSI code page`_ (CPxxxx)
   * OS/2: read the code page from :c:func:`DosQueryCp`
   * other: try ``nl_langinfo(CODESET)``, or ``LC_ALL``, ``LC_CTYPE`` or ``LANG`` environment
     variables

 * :c:func:`g_get_filename_charsets`: list of charsets
 * :c:func:`g_filename_display_name`
 * ``G_FILENAME_ENCODING`` environment variable
 * :c:func:`g_utf8_get_char`: get the first character of an UTF-8 string as
   :c:type:`gunichar`
 * :c:func:`g_convert`: decode from an encoding and encode to another encoding. Use
   :c:func:`g_convert_with_fallback` to choose how to replace unencodable characters.
 * :c:func:`g_filename_from_utf8` / :c:func:`g_filename_to_utf8`: encode to/decode from a
   filename.
 * :c:func:`g_locale_from_utf8` / :c:func:`g_locale_to_utf8`: encode to/decode from the locale
   encoding.
 * :c:func:`g_convert`: Converts a string from one character set to another (use iconv library)

.. _Gtk+: http://www.gtk.org/


ICU library
-----------

`International Components for Unicode` (ICU) is a mature, widely used set of
`C`_/`C++`_ and `Java`_ libraries providing Unicode and Globalization support for
software applications. ICU is a open source library distributed under the `MIT
license`_.

.. todo:: complete this section

.. _International Components for Unicode: http://site.icu-project.org/


See also
========

 * `UTF-8 and Unicode FAQ for Unix/Linux`_
   by Markus Kuhn, first version in june 1999, last edit in may 2009

.. _UTF-8 and Unicode FAQ for Unix/Linux:
   http://www.cl.cam.ac.uk/~mgk25/unicode.html

.. _CC BY-NC-SA 3.0 license:
   http://creativecommons.org/licenses/by-nc-sa/3.0/
.. _GNU LGPL license: http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License

