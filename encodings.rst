Charsets and encodings
======================

.. todo:: write an introduction

.. _charset:

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
:ref:`UCS-2 <ucs>`, :ref:`UCS-4 <ucs>`, :ref:`UTF-8`, :ref:`UTF-16 <utf16>`
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
(Mark Davis, january 2010). Because Google craws an huge part of the web,
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


Historical charsets and encodings
---------------------------------

Between 1950 and 2000, each manufacturer and each operating system created its
own 8 bits encoding. The problem was that 8 bits (256 code points) are not
enough to store any character, and so the encoding tries to fit the user's
language. Most 8 bits encodings are able to encode multiple languages, usually
geograpically close (e.g. ISO-8859-1 is intented for Western Europe).

.. TODO:: NELLE : "the problem was" & "The problem is" est plus une expression
  francaise traduite: ce n'est pas faux grammaticallement en anglais, mais ne
  sonne pas juste:

  8 bits (256 code points) are not enought so store all (Unicode?) characters

It was difficult to exchange documents of different languages, because if a
document was encoded to an encoding different than the user encoding, it
leaded to :ref:`mojibake <mojibake>`.


.. TODO:: NELLE : un exemple serait le bienvenu

.. index:: ASCII
.. _ASCII:

ASCII
'''''

ASCII encoding is supported by all applications. A document encoded in ASCII
can be read decoded by any other encoding. This is explained by the fact that
all 7 and 8 bits encodings are superset of ASCII, to be compatible with ASCII.
Except :ref:`JIS X 0201 <jis>` encoding: ``0x5C`` is decoded to the yen sign
(U+00A5, ¥) instead of a backslash (U+005C, \\).

ASCII is the smallest encoding, it only contains 128 codes including 95
printable characters (letters, digits, punctuation signs and some other various
characters) and 33 control codes. Control codes are used to control the
terminal. For example, the "line feed" (code point 10, usually written
``"\n"``) marks the end of a line. There are some special control code. For
example, the "bell" (code point 7, written ``"\b"``) sent to ring a bell.

+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
|    |  -0 |  -1 |  -2 |  -3 |  -4 |  -5 |  -6 |  -7 |  -8 |  -9 |  -a |  -b |  -c |  -d |  -e |  -f |
+====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
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
| 7- |  p  |  q  |  r  |  s  |  t  |  u  |  v  |  w  |  x  |  y  |  z  |  {  | \|  |  }  |  ~  | DEL |
+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

0x00—0x1F and 0x7F are control codes:

 * NUL (0x00): nul character (U+0000, ``"\0"``)
 * BEL (0x07): sent to ring a bell (U+0007, ``"\b"``)
 * TAB (0x09): horizontal tabulation (U+0009, ``"\t"``)
 * LF (0x0A): line feed (U+000A, ``"\n"``)
 * CR (0x0D): carriage return (U+000D, ``"\r"``)
 * ESC (0x1B): escape (U+001B)
 * DEL (0x7F): delete (U+007F)
 * other control codes are displayed as � in this table

0x20 is a space.

.. note::

   The first 128 code points of the Unicode charset (U+0000—U+007F) are the
   ASCII charset: Unicode is a superset of ASCII.


.. index:: ISO-8859-1
.. _ISO-8859-1:

ISO-8859-1
''''''''''

ISO-8859-1, also known as "Latin-1", is a superset of :ref:`ASCII`: it adds 128
code points, mostly latin letters with diacritics and 32 control codes. It is
used in the USA and in Western Europe.

+----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
|    |  -0 |  -1 |  -2 |  -3 |  -4 |  -5 |  -6 |  -7 |  -8 |  -9 |  -a |  -b |  -c |  -d |  -e |  -f |
+====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
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

.. note::

   The 256 first code points of the Unicode charset (U+0000—U+00FF) are the
   ISO-8859-1 charset: Unicode is a superset of ISO-8859-1.


.. index:: cp1252
.. _cp1252:

cp1252
''''''

Windows :ref:`code page <codepage>` 1252, best known as cp1252, is a variant
of :ref:`ISO-8859-1`. It is the default encoding of all English and western
europe Windows setups. It is used as a fallback by web browsers if the webpage
doesn't provide any encoding information (not in HTML, nor in HTTP).

cp1252 shares 224 code points with ISO-8859-1, the range 0x80—0x9F (32
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
.. _ISO-8859-15:

ISO-8859-15
'''''''''''

ISO-8859-15, also known as Latin-9, is a variant of :ref:`ISO-8859-1`. 248 code points
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


.. index:: GBK
.. _gbk:
.. _big5:

Chinese encodings
'''''''''''''''''

GBK is a family of Chinese charsets using multibyte encodings:

 * GB 2312 (1980): includes 6,763 Chinese characters
 * GBK (1993) (:ref:`code page <codepage>` 936)
 * GB 18030 (2005, last revision in 2006)
 * HZ (1989) (HG-GZ-2312)

To encode Chinese, there is also the Big5 encoding family and cp950.


.. index:: JIS
.. _jis:

Japanese encodings
''''''''''''''''''

JIS is a family of Japanese encodings:

 * JIS X 0201 (1969): all code points are encoded to 1 byte
 * JIS X 0208 (first version in 1978: "JIS C 6226", last revision in 1997):
   code points are encoded to 1 or 2 bytes
 * JIS X 0211 (1994), based on ISO/IEC 6429
 * JIS X 0212 (1990), extends JIS X 0208 charset: it is only a charset. Use
   EUC-JP or ISO 2022 to encode it.
 * JIS X 0213 (first version in 2000, last revision in 2004: EUC JIS X 2004),
   EUC JIS X 0213: it is only a charset, use EUC-JP, ISO 2022 or ShiftJIS 2004
   to encode it.
 * Shift JIS
 * Windows :ref:`code page <codepage>` 932 (cp932): extension of Shift JIS

In strict mode (flags=MB_ERR_INVALID_CHARS), cp932 cannot decode bytes in
``0x81``\ —\ ``0xA0`` and ``0xE0``\ —\ ``0xFF`` ranges. By default (flags=0),
``0x81``\ —\ ``0x9F`` and ``0xE0``\ —\ ``0xFC`` are decoded as U+30FB (Katakana
middle dot), ``0xA0`` as U+F8F0, ``0xFD`` as U+F8F1, ``0xFE`` as U+F8F2 and
``0xFF`` as U+F8F3 (U+E000—U+F8FF is for private usage).

.. todo:: which JIS encodings use multibyte?

The JIS family causes :ref:`mojibake <mojibake>` on MS-DOS and Microsoft
Windows because the yen sign (U+00A5, ¥) is encoded to ``0x5C`` which is a
backslash (U+005C, \\) in ASCII. For example, "C:\\Windows\\win.ini" is
displayed "C:¥Windows¥win.ini". The backslash is encoded to ``0x81 0x5F``.

To encode Japanese, there is also the ISO/IEC 2022 encoding family.

.. todo:: Korean (EUC-KR)
.. todo:: Cyrillic (cp1251, KOI8-R, ...)
.. todo:: Arabic (cp1256, ISO-8859-6)
.. todo:: ISO 8859 family
.. todo:: ISO 646
.. todo:: ISO 2022
.. todo:: Extended Unix Code (EUC), EUC JP
.. todo:: ISO 10646


Unicode encodings
-----------------

.. index:: UTF-8
.. _utf8:
.. _UTF-8:

UTF-8
'''''

UTF-8 is a multibyte encoding able to encode the whole Unicode charset. An
encoded character takes between 1 and 4 bytes. UTF-8 encoding supports longer
byte sequences, up to 6 bytes, but the biggest code point of Unicode 6.0
(U+10FFFF) only takes 4 bytes.

.. TODO:: NELLE - I don't understand. Why would UTF-8 support longer 5 bytes
  sequences if it is useless ?

It is possible to be sure that a :ref:`byte string <bytes>` is encoded to UTF-8, because
UTF-8 adds markers to each byte. For the first byte of a multibyte character,
bit 7 and bit 6 are set (``0b11xxxxxx``); the next bytes have bit 7 set and
bit 6 unset (``0b10xxxxxx``). Another cool feature of UTF-8 is that it has no
endianness (it can be read in big or little endian order, it does not matter).
Another advantage of UTF-8 is that most :ref:`C <c>` bytes
functions are compatible with UTF-8 encoded strings (e.g. :c:func:`strcat` or
:c:func:`printf`), whereas they fail with UTF-16 and UTF-32 encoded strings
because these encodings encode small codes with nul bytes.

.. todo:: write a section: handle NUL byte/character

The problem with UTF-8, if you compare it to :ref:`ASCII` or :ref:`ISO-8859-1`, is that it is
a multibyte encoding: you cannot access a character by its character index
directly, you have to iterate on each character because each character may have
a different length in bytes. If getting a character by its index is a common
operation in your program, use a :ref:`character string <str>` instead of a
:ref:`UTF-8 encoded string <bytes>`.

.. TODO:: NELLE la première phrase ne me semble pas "correcte" d'un point de
  vue grammatical :

  "It is possible to be sure that a byte string is encoded by UTF-8, because
  UTF-8 adds markers to each byte." => "Thanks to markers placed at each byte,
  it is possible to make sure a byte string is encoded in UTF-8"

.. TODO:: NELLE - "The problem with"

.. TODO:: NELLE - Il me semble que tu utilises endianness, sans avoir
  expliquer avant ce que c'était. Considères tu que le lecteur connaît ?

.. TODO:: NELLE - "If getting" a partir de là, je ne comprends plus bien

.. seealso::

   :ref:`strict utf8 decoder`.


.. index:: UCS-2, UCS-4, UTF-16, UTF-32
.. _ucs:
.. _utf16:
.. _utf32:

UCS-2, UCS-4, UTF-16 and UTF-32
'''''''''''''''''''''''''''''''

**UCS-2** and **UCS-4** encodings encode each code point to exactly one unit
of, respectivelly, 16 and 32 bits. UCS-4 is able to encode all Unicode 6.0
code points, whereas UCS-2 is limited to :ref:`BMP <bmp>` characters. These
encodings are practical because the length in units is the number of
characters.

**UTF-16** and **UTF-32** encodings use, respectivelly, 16 and 32 bits units.
UTF-16 encodes code points bigger than U+FFFF using two units: a
:ref:`surrogate pair <surrogates>`. UCS-2 can be decoded from UTF-16. UTF-32
is also supposed to use more than one unit for big code points, but in
practical, it only requires one unit to store all code points of Unicode 6.0.
That's why UTF-32 and UCS-4 are the same encoding.

+----------+-----------+-----------------+
| Encoding | Word size | Unicode support |
+==========+===========+=================+
| UCS-2    |  16 bits  | BMP only        |
+----------+-----------+-----------------+
| UTF-16   |  16 bits  | Full            |
+----------+-----------+-----------------+
| UCS-4    |  32 bits  | Full            |
+----------+-----------+-----------------+
| UTF-32   |  32 bits  | Full            |
+----------+-----------+-----------------+

:ref:`Windows 95 <win>` uses UCS-2, whereas Windows 2000 uses UTF-16.

.. note::

   UCS stands for *Universal Character Set*, and UTF stands for *UCS
   Transformation format*.


.. index:: BOM
.. _bom:

Byte order marks (BOM)
''''''''''''''''''''''

:ref:`UTF-16 <utf16>` and :ref:`UTF-32 <utf32>` use units bigger than 8 bits,
and so hit endian issue. A single unit can be stored in the big endian (most
significant bits first) or little endian (less significant bits first). BOM
are short byte sequences to indicate the encoding and the endian. It's the
U+FEFF code point encoded to the UTF encodings.

Unicode defines 6 different BOM:

 * ``0x2B 0x2F 0x76 0x38 0x2D`` (5 bytes): UTF-7 (endianless)
 * ``0xEF 0xBB 0xBF`` (3): :ref:`UTF-8` (endianless)
 * ``0xFF 0xFE`` (2): :ref:`UTF-16-LE <utf16>` (little endian)
 * ``0xFE 0xFF`` (2): :ref:`UTF-16-BE <utf16>` (big endian)
 * ``0xFF 0xFE 0x00 0x00`` (4): :ref:`UTF-32-LE <utf32>` (little endian)
 * ``0x00 0x00 0xFE 0xFF`` (4): :ref:`UTF-32-BE <utf32>` (big endian)

UTF-32-LE BOMs starts with UTF-16-LE BOM.

"UTF-16" and "UTF-32" encoding names are imprecise: depending of the context,
format or protocol, it means UTF-16 and UTF-32 with BOM markers, or UTF-16 and
UTF-32 in the host endian without BOM. On Windows, "UTF-16" usually means
UTF-16-LE.

Some Windows applications, like notepad.exe, use UTF-8 BOM, whereas many
applications are unable to detect the BOM, and so the BOM causes troubles.
UTF-8 BOM should not be used for better interoperability.

.. todo:: which troubles?


.. index:: Surrogate pair
.. _surrogates:

UTF-16 surrogate pairs
''''''''''''''''''''''

Surrogates are characters in the Unicode range U+D800—U+DFFF (2,048 code
points): it is also the :ref:`Unicode category <unicode categories>`
"surrogate" (Cs).

In :ref:`UTF-16 <utf16>`, characters in ranges U+0000—U+D7FF and U+E000—U+FFFD
are stored as a single 16 bits unit. :ref:`Non-BMP <bmp>` characters (range
U+10000—U+10FFFF) are stored as "surrogate pairs", two 16 bits units: the
first unit in the range U+D800—U+DBFF and the second unit in the range
U+DC00—U+DFFF. A lone surrogate character is invalid in UTF-16, surrogate
characters are always written as pairs.

.. todo:: can a UTF-16 encoder encode characters in U+D800-U+DFFF?

Examples of surrogate pairs:

+-----------+------------------+
| Character | Surrogate pair   |
+===========+==================+
|   U+10000 | {U+D800, U+DC00} |
+-----------+------------------+
|   U+10E6D | {U+D803, U+DE6D} |
+-----------+------------------+
|   U+1D11E | {U+D834, U+DD1E} |
+-----------+------------------+
|  U+10FFFF | {U+DBFF, U+DFFF} |
+-----------+------------------+

.. highlight:: c

:ref:`C <c>` functions to encode and decode a non-BMP character to/from UTF-16
(using surrogate pairs): ::

    #include <stdint.h>

    void
    encode_utf16_pair(uint32_t character, uint16_t *units)
    {
        unsigned int code;
        assert(character >= 0x10000);
        code = (character - 0x10000);
        units[0] = 0xD800 | (code >> 10);
        units[1] = 0xDC00 | (code & 0x3FF);
    }

    uint32_t
    decode_utf16_pair(uint16_t *units)
    {
        uint32_t code;
        assert(0xD800 <= units[0] && units[0] <= 0xDBFF);
        assert(0xDC00 <= units[1] && units[1] <= 0xDFFF);
        code = 0x10000;
        code += (units[0] & 0x03FF) << 10;
        code += (units[1] & 0x03FF);
        return code;
    }

.. note::

   An :ref:`UTF-8` encoder should not encode surrogate characters
   (U+D800—U+DFFF).


Encodings performances
----------------------

Complexity of getting the n :sup:`th` character in a string, and of
getting the length in character of a string:

 * :math:`O(1)` for 7 and 8 bit encodings (ASCII, ISO 8859 family, ...), UCS-2
   and UCS-4
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

.. todo:: Encode and decode sections?

.. _undecodable:

Undecodable byte sequences
''''''''''''''''''''''''''

When a :ref:`byte string <bytes>` is decoded from an encoding, the decoder may
fail to decode a specific byte sequence. For example, ``0x61 0x62 0x63 0xE9``
is not decodable from :ref:`ASCII` nor :ref:`UTF-8`, but it is decodable from
:ref:`ISO-8859-1`.

.. TODO:: NELLE "is decoded from an encoding" => "is decoded"

Some encodings are able to decode any byte sequences. All encodings of the
ISO-8859 family have this property, because all of the 256 code points of
these 8 bits encodings are assigned.


.. _unencodable:

Unencodable characters
''''''''''''''''''''''

When a :ref:`character string <str>` is encoded to a :ref:`charset <charset>`
smaller than the Unicode charset, a character may not be encodable. For example, €
(U+20AC) is not encodable to :ref:`ISO-8859-1`, but it is encodable to
:ref:`ISO-8859-15` and :ref:`UTF-8`.


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

:ref:`Python <python>` "replace" error handler uses ``\xHH``, ``\uHHHH`` or
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


.. _guess:

How to guess the encoding of a document?
----------------------------------------

Only :ref:`ASCII`, :ref:`UTF-8` and encodings using a :ref:`BOM <bom>` (UTF-7
with BOM, UTF-8 with BOM, :ref:`UTF-16 <utf16>`, and :ref:`UTF-32 <utf32>`)
have reliable algorithms to get the encoding of a document. For all other
encodings, you have to trust heuristics based on statistics.


Is ASCII?
'''''''''

Check if a document is encoded to :ref:`ASCII` is simple: test if the bit 7 of
each byte is unset (``0b0xxxxxxx``).

.. TODO:: NELLE - test if the bit 7 of all byte is unset

.. highlight:: c

Example in :ref:`C <c>`: ::

    int isASCII(const char *data, size_t size)
    {
        const unsigned char *str = (const unsigned char*)data;
        const unsigned char *end = str + size;
        for (; str != end; str++) {
            if (*str & 0x80)
                return 0;
        }
        return 1;
    }

.. highlight:: python

In :ref:`Python`, the ASCII decoder can be used: ::

    def isASCII(data):
        try:
            data.decode('ASCII')
        except UnicodeDecodeError:
            return False
        else:
            return True

.. note::

   Only use the Python function on short strings because it decodes the whole
   string into memory.  For long strings, it is better to use the algorithm of
   the C function because it doesn't allocate any memory.


Check for BOM markers
'''''''''''''''''''''

If the string begins with a :ref:`BOM <bom>`, the encoding can be extracted
from the BOM. But there is a problem with :ref:`UTF-16-BE <utf16>` and
:ref:`UTF-32-LE <utf32>`: UTF-32-LE BOM starts with the UTF-16-LE BOM.

.. highlight:: c

Example of a function written in :ref:`C <c>` to check if a BOM is present: ::

    #include <string.h>   /* memcmp() */

    const char *UTF_16_BE_BOM = "\xFE\xFF";
    const char *UTF_16_LE_BOM = "\xFF\xFE";
    const char *UTF_8_BOM = "\xEF\xBB\xBF";
    const char *UTF_32_BE_BOM = "\x00\x00\xFE\xFF";
    const char *UTF_32_LE_BOM = "\xFF\xFE\x00\x00";

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
decoded from UTF-16-LE.

.. highlight:: python

Example in :ref:`Python` getting the BOMs from the codecs library: ::

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

:ref:`UTF-8` encoding adds markers to each bytes and so it's possible to write a
reliable algorithm to check if a function is encoded to UTF-8.

.. highlight:: c

Example of a strict :ref:`C <c>` function to check if a string is encoded to
UTF-8. It rejects :ref:`overlong sequences <strict utf8 decoder>` (e.g.  ``0xC0
0x80``) and :ref:`surrogate characters <surrogates>` (e.g. ``0xED 0xB2 0x80``,
U+DC80). ::

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
                /* 1 byte sequence: U+0000..U+007F */
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
             * unset (b10xxxxxx). */
            for (i=1; i < code_length; i++) {
                if ((str[i] & 0xC0) != 0x80)
                    return 0;
            }

            if (code_length == 2) {
                /* 2 bytes sequence: U+0080..U+07FF */
                ch = ((str[0] & 0x1f) << 6) + (str[1] & 0x3f);
                /* ch cannot be greater than 0x07FF */
                if (ch < 0x0080)
                    return 0;
            } else if (code_length == 3) {
                /* 3 bytes sequence: U+0800..U+FFFF */
                ch = ((str[0] & 0x0f) << 12) + ((str[1] & 0x3f) << 6) +
                      (str[2] & 0x3f);
                /* ch cannot be greater than 0xFFFF */
                if (ch < 0x0800)
                    return 0;
                /* surrogates (U+D800-U+DFFF) are invalid in UTF-8 */
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

.. highlight:: python

In :ref:`Python`, the UTF-8 decoder can be used: ::

    def isUTF8(data):
        try:
            data.decode('UTF-8')
        except UnicodeDecodeError:
            return False
        else:
            return True

In :ref:`Python 2 <python2>`, this function is more tolerant than the C
function, because the UTF-8 decoder of Python 2 accepts surrogate characters
(U+D800—U+DFFF). For example, ``isUTF8(b'\xED\xB2\x80')`` returns ``True``.
With :ref:`Python 3 <python3>`, the Python function is equivalent to the C
function. If you would like to reject surrogate characters in Python 2, use
the following strict function: ::

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

:ref:`PHP <php>` has a builtin function to detect the encoding of a :ref:`byte
string <bytes>`: ``mb_detect_encoding()``.

 * chardet_: :ref:`Python` version of the "chardet" algorithm implemented in Mozilla
 * UTRAC_: command line program (written in :ref:`C <c>`) to recognize the encoding of
   an input file and its end-of-line type
 * charguess_: Ruby library to guess the charset of a document

.. todo:: update/complete this list

.. _chardet: http://chardet.feedparser.org/
.. _charguess:  http://raa.ruby-lang.org/project/charguess/
.. _UTRAC: http://utrac.sourceforge.net/

