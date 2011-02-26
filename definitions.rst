Definitions
===========

.. _character:

Character
---------

.. todo:: define a character


Glyph
-----

.. todo:: define a glyph


.. _code point:

Code point
----------

A **code point** is an unsigned integer. The smallest code point is zero. Code
points are usually written as hexadecimal, e.g. "0x20AC" (8,364 in decimal).


.. _charset:

Character set (charset)
-----------------------

A **character set**, abbreviated **charset**, is a mapping between :ref:`code
points <code point>` and :ref:`characters <character>`. The mapping has a fixed
size.  For example, most 7 bits encodings have 128 entries, and most 8 bits
encodings have 256 entries. The biggest charset is Unicode 6.0 with 1,114,112
entries.

In some charsets, code points are not all contiguous. For example, the
:ref:`cp1252 <cp1252>` charset maps code points from 0 though 255, but it has
only 251 entries: 0x81, 0x8D, 0x8F, 0x90 and 0x9D code points are not assigned.

Examples of the :ref:`ASCII <ascii>` charset: the "5" character (U+0035) is
assigned to the code point 0x35 (53 in decimal), and "A" (U+0041) to the code
point 0x41 (65).

The biggest code point depends on the size of the charset. For example, the
biggest code point of the ASCII charset is 127 (:math:`2^7-1`)


.. _str:

Character string
----------------

A **character string**, or "Unicode string", is a string where each unit is a
:ref:`character <character>`. Depending on the implementation, each character
can be any Unicode character, or only characters in the range U+0000—U+FFFF,
range called the :ref:`Basic Multilingual Plane (BMP) <bmp>`. There are 3
different implementations of character strings:

 * array of 32 bits unsigned integers (the :ref:`UCS-4 <ucs>` encoding): full
   Unicode range
 * array of 16 bits unsigned integers (:ref:`UCS-2 <ucs>`): BMP only
 * array of 16 bits unsigned integers with :ref:`surrogate pairs
   <surrogates>` (:ref:`UTF-16 <utf16>`): full Unicode range

UCS-4 use twice as much memory than UCS-2, but it supports all Unicode
character. UTF-16 is a compromise between UCS-2 and UCS-4: characters in the
BMP range use one UTF-16 unit (16 bits), characters outside this range use two
UTF-16 units (a :ref:`surrogate pair <surrogates>`, 32 bits). This advantage is
also the main disadvantage of this kind of character string.

The length of a character string implemented using UTF-16 is the number of
UTF-16 units, and not the number of characters, which is confusing. For
example, the U+10FFFF character is encoded as two UTF-16 units: {U+DBFF,
U+DFFF}. If the character string only contains characters of the BMP range, the
length is the number of characters. Getting the n\ :sup:`th` character or the
length in characters using UTF-16 has a complexity of :math:`O(n)`, whereas
it has a complexity of :math:`O(1)` for UCS-2 and UCS-4 strings.

The :ref:`Java` language, the :ref:`Qt <qt>` library and :ref:`Windows 2000
<win>` implement character strings with UTF-16. The :ref:`C <c>` and :ref:`Python
<python>` languages use UTF-16 or UCS-4 depending on: the size of the
:c:type:`wchar_t` type (16 or 32 bits) for C, and the compilation mode (narrow
or wide) for Python. Windows 95 uses UCS-2 strings.

.. seealso::

   :ref:`UCS-2 <ucs>`, :ref:`UCS-4 <ucs>` and :ref:`UTF-16 <utf16>` encodings,
   and :ref:`surrogate pairs <surrogates>`.


.. _bytes:

Byte string
-----------

A **byte string** is a :ref:`character string <str>` encoded to an
:ref:`encoding <encoding>`. It is implemented as an array of 8 bits unsigned
integers. It can be called by its encoding. For example, a byte string encoded
to :ref:`ASCII <ascii>` is called an "ASCII encoded string", or simply an
"ASCII string".

The character range supported by a byte string depends on its encoding, because
an encoding is associated to a charset. For example, an ASCII string can only
store characters in the range U+0000—U+007F.

The encoding is not stored explicitly in a byte string. If the encoding is not
documented or attached to the byte string, :ref:`the encoding have to be
guessed <guess>`, which is a difficult task. If a byte string is decoded from
the wrong encoding, it will not be displayed correctly, leading to a well known
issue: :ref:`mojibake <mojibake>`.

The same problem occurs if two byte strings encoded to different encodings are
concatenated. **Never concatenate byte strings encoded to different
encodings!** Use character strings, instead of byte strings, to avoid mojibake
issues.

:ref:`PHP5 <php>` only supports byte strings. In the :ref:`C language <c>`,
"strings" are usually byte strings which are implemented as the :c:type:`char*`
type (or :c:type:`const char*`).

.. seealso::

   The :c:type:`char*` type of the C language and the :ref:`mojibake
   <mojibake>` issue.


UTF-8 encoded strings and UTF-16 character strings
--------------------------------------------------

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

.. [1] A UTF-8 encoder :ref:`should not encode <strict utf8 decoder>` :ref:`surrogate characters <surrogates>` (U+D800—U+DFFF).


.. _encoding:

Encoding
--------

An **encoding** describes how to encode :ref:`code points <code point>` to bytes
and how to decode bytes to code points.

An encoding is always associated to a :ref:`charset <charset>`. For example,
the UTF-8 encoding is associated to the Unicode charset. So we can say  that an
encoding encodes characters to bytes and decode bytes to characters, or more
generally, it encodes a :ref:`character string <str>` to a :ref:`byte string
<bytes>` and decodes a byte string to a character string.

The 7 and 8 bits charsets have most simple encoding: store a code point as a
single byte. These charsets are also called encodings, it is easy to confused
them. The best example is the :ref:`ISO-8859-1 encoding <ISO-8859-1>`: all of
the 256 possible bytes are considered as 8 bit code points (0 through 255) and
are associated to characters. For example, the character A (U+0041) has the
code point 65 (0x41 in hexadecimal) and is stored as the byte ``0x41``.

Charsets with more than 256 entries cannot encode all code points into a single
byte. The encoding encode all code points into byte sequences of the same
length or of variable length. For example, :ref:`UTF-8` is a variable length
encoding: code points lower than 128 use a single byte, whereas higher code
points take 2, 3 or 4 bytes. The :ref:`UCS-2 <ucs>` encoding encodes all
code points into sequences of two bytes (16 bits).

.. TODO:: NELLE : je ne m'y connais pas trop en encodage, mais il me semble
  que ce que tu affirmes dans le paragraphe précédent n'est pas tout à fait
  correct: un encodage associe un character/glyphe/symbole avec quelque chose
  d'autre, comme une série d'entier, d'octet ou n'importe quoi (en fait plus
  exactement, pour moi de l'encodage, c'est une maniere d'associer X à Y, avec
  la possibilité de décoder de Y vers X). Si tu prends l'article de wikipédia
  sur le sujet (http://en.wikipedia.org/wiki/Character_encoding), il mentionne
  le code morse. Le pire dans tout ça, c'est qu'il me semble qu'il existe
  différent type de code morse pour différent language. Entre, la chine.

  Bref, tout ça pour dire que je ne suis pas d'accord sur le fait que : "7 and
  8 bits don't need any encoding". Tu associes une série de booléen à un
  caractère, donc par définition, il y a encodage. Cependant, je suppose que
  c'est un encodage "standard"


Unicode: an Universal Character Set (UCS)
-----------------------------------------

.. todo:: define UCS

.. seealso::

   :ref:`UCS-2 <ucs>`, :ref:`UCS-4 <ucs>`, :ref:`UTF-8 <utf8>`, :ref:`UTF-16
   <utf16>`, and :ref:`UTF-32 <utf32>` encodings.


.. todo:: add maybe Encode and Decode sections?
