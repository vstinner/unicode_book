About this book
===============

.. todolist::


License
-------

This book is distributed under the `CC BY-NC-SA 3.0 license <http://creativecommons.org/licenses/by-nc-sa/3.0/>`_.

Thanks to
---------

Reviewers:

 * Alexander Belopolsky
 * Antoine Pitrou
 * Feth Arezki
 * Nelle Varoquaux


Notations used in this book
---------------------------

 * ``0bBBBBBBBB``: 8 bit unsigned number written in binary, first digit is the most
   significant. For example, ``0b10000000`` is 128.
 * 0xHHHH: number written in hexadecimal, e.g. 0xFFFF is 65535.
 * ``0xHH 0xHH ...``: byte sequence with bytes written in hexadecimal, e.g.
   ``0xC3 0xA9`` (2 bytes) is the character é (U+00E9) encoded to UTF-8.
 * U+HHHH: Unicode code point with code written in hexadecimal. For example, U+20AC is
   the code point 8364 (euro sign). Big code point are written with more than 4
   hexadecimal digits, e.g. U+10FFFF is the biggest (unallocated) code point of
   Unicode 6.0: 1114111.
 * A—B: range including start and end. Examples:

   * ``0x00``\ —\ ``0x7F`` is a range of 128 bytes (0 through 127)
   * U+0000—U+00FF is a range of 256 characters (0 through 255)

.. todo:: document {U+HHHH, U+HHHH} syntax and check for its usage

