Historical charsets and encodings
=================================

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
-----

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


.. _ISO-8859:

ISO 8859 family
---------------

====  ===========  ============================================  ==============
Year  Norm         Description                                   Variant
1987  ISO 8859-1   Western European: German, French, Italian, …  cp1252
1987  ISO 8859-2   Central European: Croatian, Polish, Czech, …  cp1250
1988  ISO 8859-3   South European: Turkish and Esperanto         -
1988  ISO 8859-4   North European        -
1988  ISO 8859-5   Latin/Cyrillic: Macadonian, Russian, …        KOI family
1987  ISO 8859-6   Latin/Arabic: Arabic language characters      cp1256
1987  ISO 8859-7   Latin/Greek: modern greek language            cp1253
1988  ISO 8859-8   Latin/Hebrew: modern Hebrew alphabet          cp1255
1989  ISO 8859-9   Turkish: Largely the same as ISO 8859-1       cp1254
1992  ISO 8859-10  Nordic: a rearrangement of Latin-4            -
2001  ISO 8859-11  Latin/Thai: Thai language                     TIS 620, cp874
1998  ISO 8859-13  Baltic Rim: Baltic languages                  cp1257
1998  ISO 8859-14  Celtic: Gaelic, Breton                        -
1999  ISO 8859-15  Revision of 8859-1: euro sign                 cp1252
2001  ISO 8859-16  South-Eastern European                        -
====  ===========  ============================================  ==============

.. note::
   ISO 8859-12 doesn't exist.

.. todo:: Arabic (cp1256, ISO-8859-6)


.. index:: ISO-8859-1
.. _ISO-8859-1:

ISO 8859-1
''''''''''

ISO/CEI 8859-1, also known as "Latin-1" or "ISO-8859-1", is a superset of
:ref:`ASCII`: it adds 128 code points, mostly latin letters with diacritics and
32 control codes. It is used in the USA and in Western Europe.

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

ISO 8859-15
'''''''''''

ISO/CEI 8859-15, also known as Latin-9 or ISO-8859-15, is a variant of
:ref:`ISO-8859-1`. 248 code points are identicals, 8 are different:

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

CJK: asian encodings
--------------------

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

Other encodings: Big5 (大五碼, Big Five Encoding, 1984), cp950.


.. index:: JIS
.. _jis:

Japanese encodings
''''''''''''''''''

JIS is a family of Japanese encodings:

 * JIS X 0201 (1969): all code points are encoded to 1 byte
 * 16 bits:

   * JIS X 0208 (first version in 1978: "JIS C 6226", last revision in 1997):
     code points are encoded to 1 or 2 bytes
   * JIS X 0212 (1990), extends JIS X 0208 charset: it is only a charset. Use
     EUC-JP or ISO 2022 to encode it.
   * JIS X 0213 (first version in 2000, last revision in 2004: EUC JIS X 2004),
     EUC JIS X 0213: it is only a charset, use EUC-JP, ISO 2022 or ShiftJIS 2004
     to encode it.

 * JIS X 0211 (1994), based on ISO/IEC 6429

Microsoft encodings:

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


ISO 2022
''''''''

ISO/IEC 2022 is an encoding family:

 * ISO-2022-JP: JIS X 0201-1976, JIS X 0208-1978, JIS X 0208-1983
 * ISO-2022-JP-1: JIS X 0212-1990
 * ISO-2022-JP-2: GB 2312-1980, KS X 1001-1992, :ref:`ISO/IEC 8859-1 <ISO-8859-1>`, ISO/IEC 8859-7
 * ISO-2022-JP-3: JIS X 0201-1976, JIS X 0213-2000, JIS X 0213-2000
 * ISO-2022-JP-2004: JIS X 0213-2004
 * ISO-2022-KR: KS X 1001-1992
 * ISO-2022-CN: GB 2312-1980, CNS 11643-1992 (planes 1 and 2)
 * ISO-2022-CN-EXT: ISO-IR-165, CNS 11643-1992 (planes 3 though 7)


Extended Unix Code (EUC)
''''''''''''''''''''''''

 * EUC-CN: GB2312
 * EUC-JP: JIS X 0208, JIS X 0212, JIS X 0201
 * EUC-KR: KS X 1001, KS X 1003
 * EUC-TW: CNS 11643 (16 planes)


Cyrillic
--------

KOI family, "Код Обмена Информацией":

 * KOI-7: oldest KOI encoding (ASCII + some characters)
 * KOI8-R: Russian
 * KOI8-U: Ukrainian

Variants: ECMA-Cyrillic, KOI8-Unified, cp1251, MacUkrainian, Bulgarian MIK, ...

