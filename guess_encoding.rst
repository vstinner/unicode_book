.. _guess:

How to guess the encoding of a document?
========================================

Only :ref:`ASCII`, :ref:`UTF-8` and encodings using a :ref:`BOM <bom>` (:ref:`UTF-7 <utf7>`
with BOM, UTF-8 with BOM, :ref:`UTF-16 <utf16>`, and :ref:`UTF-32 <utf32>`)
have reliable algorithms to get the encoding of a document. For all other
encodings, you have to trust heuristics based on statistics.


Is ASCII?
---------

Check if a document is encoded to :ref:`ASCII` is simple: test if the bit 7 of
all bytes is unset (``0b0xxxxxxx``).

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
---------------------

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
:ref:`decoded <decode>` from UTF-16-LE.

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

.. _is utf8:

Is UTF-8?
---------

:ref:`UTF-8` encoding adds markers to each bytes and so it's possible to write
a reliable algorithm to check if a :ref:`byte string <bytes>` is encoded to
UTF-8.

.. highlight:: c

Example of a strict :ref:`C <c>` function to check if a string is encoded with
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
                /* str[0] >= 0xC2, so ch >= 0x0080.
                   str[0] <= 0xDF, (str[1] & 0x3f) <= 0x3f, so ch <= 0x07ff */
            } else if (code_length == 3) {
                /* 3 bytes sequence: U+0800..U+FFFF */
                ch = ((str[0] & 0x0f) << 12) + ((str[1] & 0x3f) << 6) +
                      (str[2] & 0x3f);
                /* (0xff & 0x0f) << 12 | (0xff & 0x3f) << 6 | (0xff & 0x3f) = 0xffff,
                   so ch <= 0xffff */
                if (ch < 0x0800)
                    return 0;

                /* surrogates (U+D800-U+DFFF) are invalid in UTF-8:
                   test if (0xD800 <= ch && ch <= 0xDFFF) */
                if ((ch >> 11) == 0x1b)
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
---------

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

