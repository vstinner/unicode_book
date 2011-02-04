Unicode issues
==============

.. index:: Mojibake

Mojibake
--------

When a :ref:`byte strings <bytes>` is decoded from the wrong encoding, or when
two byte strings encoded to different encodings are concatenated, a program
will display **mojibake**.

The classical example is a latin string (with diacritics) encoded to UTF-8 but
decoded from ISO-8859-1. It displays Ã© (U+00C3, U+00A9) for the é (U+00E9)
letter, because é is encoded to ``0xC3 0xA9`` in UTF-8.

See also the :ref:`guess` section.

.. todo:: add a screenshot of mojibake


Security
--------

Special characters
''''''''''''''''''

Fullwidth (U+FF01—U+FF60) and halfwidth (U+FF61—U+FFEE) characters has been
used to bypass security checks. Some important characters have also
"alternatives" in Unicode:

 * Windows directory separator, \\ (U+005C): U+20E5, U+FF3C
 * UNIX directory separator, / (U+002F): U+2215, U+FF0F
 * Parent directory, .. (U+002E, U+002E): U+FF0E

Example with :ref:`Unicode normalization <normalization>`:

 * U+FF0E is normalized to . (U+002E) in NFKC
 * U+FF0F is normalized to / (U+002F) in NFKC

For more information, read `GS07-01 Full-Width and Half-Width Unicode Encoding
IDS/IPS/WAF Bypass Vulnerability
<http://www.gamasec.net/english/gs07-01.html>`_ (april 2007).


.. _strict utf8 decoder:

Non-strict UTF-8 decoder
''''''''''''''''''''''''

An UTF-8 decoder have to reject invalid byte sequences for security reasons:
``0xC0 0x80`` byte sequence must raise an error (and not be decoded as U+0000).
If the decoder accepts invalid byte sequence, an attacker can use it to bypass
security checks (e.g. reject string containing nul bytes, ``0x00``). Surrogates
characters are also invalid in UTF-8: characters in U+D800—U+DFFF have to be
rejected.

For example, . (U+002E) can be encoded to ``0xC0 0xAE``: two bytes instead of
one.

The libxml2 library had such vulnerability until january 2008: `CVE-2007-6284
<http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6284>`_.

Some PHP functions use a strict UTF-8 decoder (e.g. ``mb_convert_encoding()``),
some other don't. For example, ``utf8_decode()`` and ``mb_strlen()`` accept
``0xC0 0x80`` in PHP 5.3.2.

.. note::

   The :ref:`Java <java>` and Tcl languages uses a variant of :ref:`UTF-8`
   which encodes the nul character (U+0000) as the overlong byte sequence
   ``0xC0 0x80``, instead of ``0x00``.


Check byte strings but use Unicode strings
''''''''''''''''''''''''''''''''''''''''''

Some applications check user inputs as :ref:`byte strings <bytes>`, but
then process them as :ref:`Unicode strings <str>`.

The WordPress blog tool had such issue with :ref:`PHP5 <php>` and MySQL. If
PHP "magic quotes" feature is enabled, ``0x27`` is replaced by ``0x5C 0x27`` in
the input strings. If the input data is encoded to ISO-8859-1, this operation
escapes a quote: ``'`` (U+0027) becomes ``\'`` (U+005C, U+0027). The problem is
that inputs are byte strings. Example with :ref:`Big5 <big5>` encoding: ``0xB5
0x27`` in an invalid byte sequence, but escaped, it becomes ``0xB5 0x5C 0x27``
which is decoded as {U+8A31, U+0027}. ``0x5C`` is no more a back slash: it is
part of a multibyte character (U+8A31).

For more information, see
`CVE-2006-2314 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-2314>`_ (PostgreSQL, may 2006),
`CVE-2006-2753 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-2753>`_ (MySQL, may 2006) and
`CVE-2008-2384 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-2384>`_ (libapache2-mod-auth-mysql, january 2009).

