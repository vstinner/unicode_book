Unicode issues
==============

.. index:: Mojibake
.. _mojibake:

Mojibake
--------

When a :ref:`byte strings <bytes>` is :ref:`decoded <decode>` from the wrong
encoding, or when two byte strings encoded to different encodings are
concatenated, a program will display **mojibake**.

The classical example is a latin string (with diacritics) encoded to UTF-8 but
decoded from ISO-8859-1. It displays Ã© {U+00C3, U+00A9} for the é (U+00E9)
letter, because é is encoded to ``0xC3 0xA9`` in UTF-8.

Other examples:

========== ========== ============ ===================
Text       Encoded to Decoded from Result
========== ========== ============ ===================
Noël          UTF-8    ISO-8859-1  NoÃ«l
Русский       KOI-8    ISO-8859-1  òÕÓÓËÉÊ
========== ========== ============ ===================

.. note::

   "Mojibake" is japanese word meaning literally "unintelligible sequence of
   characters". This issue is called "Кракозя́бры" (krakozyabry) in Russian.

.. seealso:: :ref:`How to guess the encoding of a document? <guess>`


Security vulnerabilities
------------------------

Special characters
''''''''''''''''''

Fullwidth (U+FF01—U+FF60) and halfwidth (U+FF61—U+FFEE) characters has been
used in 2007 to bypass security checks. Examples with the :ref:`Unicode
normalization <normalization>`:

 * U+FF0E is normalized to . (U+002E) in NFKC
 * U+FF0F is normalized to / (U+002F) in NFKC

Some important characters have also "alternatives" in Unicode:

 * Windows directory separator, \\ (U+005C): U+20E5, U+FF3C
 * UNIX directory separator, / (U+002F): U+2215, U+FF0F
 * Parent directory, .. (U+002E, U+002E): U+FF0E

For more information, read `GS07-01 Full-Width and Half-Width Unicode Encoding
IDS/IPS/WAF Bypass Vulnerability
<http://www.gamasec.net/english/gs07-01.html>`_ (GamaTEAM, april 2007).

.. todo:: usage of surrogates (U+D800-U+DFFF) in security?


.. _strict utf8 decoder:

Non-strict UTF-8 decoder: overlong byte sequences and surrogates
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

An :ref:`UTF-8 <utf8>` :ref:`decoder <decode>` have to reject overlong byte sequences, or an attacker can use
them to bypass security checks (e.g. check rejecting string containing nul bytes,
``0x00``). For example, ``0xC0 0x80`` byte sequence must raise an error and
not be decoded as U+0000, and "." (U+002E) can be encoded to ``0xC0 0xAE`` (two
bytes instead of one) to bypass directory traversal checks.

:ref:`Surrogates characters <surrogates>` are also invalid in UTF-8: characters in U+D800—U+DFFF
have to be rejected. See the table 3-7 in the `Conformance chapiter of the
Unicode standard <http://www.unicode.org/versions/Unicode5.2.0/ch03.pdf>`_
(december 2009); and the section 3 (UTF-8 definition) of `UTF-8, a
transformation format of ISO 10646
<http://www.rfc-editor.org/rfc/rfc3629.txt>`_ (RFC 3629, november 2003).

The libxml2 library had such vulnerability until january 2008: `CVE-2007-6284
<http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6284>`_.

Some PHP functions use a strict UTF-8 decoder (e.g. ``mb_convert_encoding()``),
some other don't. For example, ``utf8_decode()`` and ``mb_strlen()`` accept
``0xC0 0x80`` in PHP 5.3.2.

.. note::

   The :ref:`Java <java>` and Tcl languages uses a variant of :ref:`UTF-8`
   which encodes the nul character (U+0000) as the overlong byte sequence
   ``0xC0 0x80``, instead of ``0x00``, for practical reasons.


Check byte strings before decoding them to character strings
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Some applications check user inputs as :ref:`byte strings <bytes>`, but then
process them as :ref:`character strings <str>`. This vulnerability can be used
to bypass security checks.

The WordPress blog tool had such issue with :ref:`PHP5 <php>` and MySQL:
`WordPress Charset SQL Injection Vulnerability
<http://www.abelcheung.org/advisory/20071210-wordpress-charset.txt>`_ (Abel
Cheung, december 2007). WordPress used the PHP function ``addslashes()`` on the
input byte strings. This function adds ``0x5C`` prefix to ``0x00``, ``0x22``,
``0x27`` and ``0x5C`` bytes. If a input string is encoded to :ref:`ISO-8859-1`,
this operation escapes a quote: ``'`` (U+0027) becomes ``\'`` ({U+005C,
U+0027}).

The problem is that ``addslashes()`` process byte strings, whereas the result
is used by MySQL which process character strings.  Example with :ref:`Big5
<big5>` encoding: ``0xB5 0x27`` :ref:`cannot be decoded <undecodable>` from Big5, but escaped it
becomes ``0xB5 0x5C 0x27`` which is decoded to {U+8A31, U+0027}. The ``0x5C``
byte is no more a backslash: it is part of the multibyte character U+8A31
encoded to ``0xB5 0x5C``. The solution is to use ``mysql_real_escape_string()``
function, instead of ``addslashes()``, which process inputs as character
strings using the MySQL connection encoding.

.. seealso::

   `CVE-2006-2314 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-2314>`_ (PostgreSQL, may 2006),
   `CVE-2006-2753 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-2753>`_ (MySQL, may 2006) and
   `CVE-2008-2384 <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-2384>`_ (libapache2-mod-auth-mysql, january 2009).

