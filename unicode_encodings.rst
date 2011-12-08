Unicode encodings
=================

.. index:: UTF-8
.. _utf8:
.. _UTF-8:

UTF-8
-----

UTF-8 is a multibyte encoding able to encode the whole Unicode charset. An
encoded character takes between 1 and 4 bytes. UTF-8 encoding supports longer
byte sequences, up to 6 bytes, but the biggest code point of Unicode 6.0
(U+10FFFF) only takes 4 bytes.

.. TODO:: NELLE - I don't understand. Why would UTF-8 support longer 5 bytes
  sequences if it is useless ?

It is possible to be sure that a :ref:`byte string <bytes>` is encoded to
UTF-8, because UTF-8 adds markers to each byte. For the first byte of a
multibyte character, bit 7 and bit 6 are set (``0b11xxxxxx``); the next bytes
have bit 7 set and bit 6 unset (``0b10xxxxxx``).

Another cool feature of UTF-8 is that it has no
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
   :ref:`Non-strict UTF-8 decoder <strict utf8 decoder>` and :ref:`Is UTF-8?
   <is utf8>`.


.. index:: UCS-2, UCS-4, UTF-16, UTF-32
.. _ucs:
.. _utf16:
.. _utf32:

UCS-2, UCS-4, UTF-16 and UTF-32
-------------------------------

**UCS-2** and **UCS-4** encodings :ref:`encode <encode>` each code point to exactly one unit
of, respectivelly, 16 and 32 bits. UCS-4 is able to encode all Unicode 6.0
code points, whereas UCS-2 is limited to :ref:`BMP <bmp>` characters. These
encodings are practical because the length in units is the number of
characters.

**UTF-16** and **UTF-32** encodings use, respectivelly, 16 and 32 bits units.
UTF-16 encodes code points bigger than U+FFFF using two units: a
:ref:`surrogate pair <surrogates>`. UCS-2 can be :ref:`decoded <decode>` from UTF-16. UTF-32
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


.. index:: UTF-7
.. _utf7:

UTF-7
-----

The UTF-7 encoding is similar to the :ref:`UTF-8 encoding <utf8>`, except that
it uses 7 bits units instead of 8 bits units. It is used for example in emails
with server which are not "8 bits clean".


.. index:: BOM
.. _bom:

Byte order marks (BOM)
----------------------

:ref:`UTF-16 <utf16>` and :ref:`UTF-32 <utf32>` use units bigger than 8 bits,
and so hit endian issue. A single unit can be stored in the big endian (most
significant bits first) or little endian (less significant bits first). BOM
are short byte sequences to indicate the encoding and the endian. It's the
U+FEFF code point encoded to the UTF encodings.

Unicode defines 6 different BOM:

 * ``0x2B 0x2F 0x76 0x38 0x2D`` (5 bytes): :ref:`UTF-7 <utf7>` (endianless)
 * ``0xEF 0xBB 0xBF`` (3): :ref:`UTF-8 <utf8>` (endianless)
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
----------------------

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

:ref:`C <c>` functions to :ref:`encode <encode>` and :ref:`decode <decode>` a
non-BMP character to/from UTF-16 (using surrogate pairs): ::

    #include <stdint.h>

    void
    encode_utf16_pair(uint32_t character, uint16_t *units)
    {
        unsigned int code;
        assert(0x10000 <= character && character <= 0x10FFF);
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
   (U+D800—U+DFFF), see :ref:`Non-strict UTF-8 decoder <strict utf8 decoder>`.

