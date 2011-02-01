Unicode issues
==============

.. index:: Mojibake

Mojibake
--------

When a :ref:`byte strings <byte string>` is decoded from the wrong encoding
(see :ref:`Guess encoding`), or when two byte strings encoded to different
encodings are concatenated, a program will display **mojibake**.

The classical example is a latin string (with diacritics) encoded to UTF-8 but
decoded from ISO-8859-1. It displays Ã© (U+00C3, U+00A9) for the é (U+00E9)
letter, because é is encoded to ``0xC3 0xA9`` in UTF-8.

.. todo:: add a screenshot of mojibake


Security
--------

Special characters
''''''''''''''''''

Fullwidth (U+FF01—U+FF60) and halfwidth (U+FF61—U+FFEE) characters has been
used to workaround security checks. Some important characters have also
alternatives in Unicode:

 * Windows directory separator, \\ (U+005C):  ⃥ (U+20E5), ＼ (U+FF3C)
 * UNIX directory separator, / (U+002F): ∕ (U+2215), ／ (U+FF0F)
 * Parent directory, .. (U+002E, U+002E): ．(U+FF0E)


.. _strict utf8 decoder:

Non-strict UTF-8 decoder
''''''''''''''''''''''''

An UTF-8 decoder have to reject invalid byte sequences for security reasons:
``0xC0 0x80`` byte sequence must raise an error (and not be decoded as U+0000).
If the decoder accepts invalid byte sequence, an attacker can use it to workaround
security checks (eg. reject string containing nul bytes, ``0x00``). Surrogates
characters are also invalid in UTF-8: characters in U+D800—U+DFFF have to be
rejected.

