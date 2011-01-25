Programming languages
=====================

.. _c:

C language
----------

The C language is a low level language, close to the CPU. It has a builtin
Unicode string type (:c:type:`wchar_t*`), but only few libraries support
Unicode. It is usually used as the first "layer" between the kernel and
applications, higher level libraries and other programming languages. This
first layer uses the same type than the kernel: except :ref:`Windows`, all
kernels use byte strings. The C standard library is a first layer for system
calls (eg.  open a file).

There are higher level libraries, like :ref:`glib <glib>` or :ref:`Qt <qt>`,
offering a Unicode API, even if the underlying kernel use byte strings. Such
libraries use a codec to encode data for the kernel and to decode data from the
kernel. The codec is usually the current :ref:`locale encoding <locale
encoding>`.

Because there is no Unicode standard library, most third-party libraries chose
the simple solution: use byte strings. For example, the OpenSSL library, an
open source cryptography toolkit, expects filenames as byte strings. On
Windows, you have to encode Unicode filenames to the current :ref:`ANSI code
page <codepage>`, which is a small subset of the Unicode charset.

Byte API (char)
'''''''''''''''

.. c:type:: char

    For historical reasons, :c:type:`char` is the C type for a character ("char" as
    "character"). In pratical, it's only true for 7 and 8 bits encodings like :ref:`ASCII`
    or :ref:`ISO-8859-1`. With multibyte encodings, a :c:type:`char` is only one byte. For example, the
    character "é" (U+00E9) is encoded as two bytes (``0xC3 0xA9``) in :ref:`UTF-8`.

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
   is a problem with encodings using nul bytes (eg. :ref:`UTF-16 <utf16>` and :ref:`UTF-32 <utf32>`): :c:func:`strlen()`
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
   like WCHAR_MAX. If :c:type:`wchar_t` is 16 bits long, :ref:`non-BMP <bmp>` characters are encoded
   to :ref:`UTF-16 <utf16>` using surrogate pairs (see :ref:`Surrogate pair`).

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
if U+0141 (Ł) cannot be encoded to the locale encoding: ::

    wprintf(L"Latin capital letter L with stroke: [%s]\n", L"\u0141");

So to avoid truncated strings, try to use only :c:func:`wprintf` with character
string arguments.

.. note::

   There is also ``"%S"`` format which is a deprecated alias to the ``"%ls"``
   format, don't use it.


.. _cpp:

C++
---

 * ``std::wstring``: character string using the :c:type:`wchar_t` type, unicode
   version of ``std::string``
 * ``std::wcin``, ``std::wcout`` and ``std::wcerr``: standard input, output
   and error output; unicode version of ``std::cin``, ``std::cout`` and
   ``std::cerr``
 * ``std::wostringstream``: character stream buffer; unicode version of
   ``std::ostringstream``.

To initialize the locales (see :ref:`Locales`), equivalent to ``setlocale(LC_ALL,
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

   Use ``typedef basic_ostringstream<wchar_t> wostringstream;`` if
   wostringstream is not available.


.. _Python:

Python
------

Python supports Unicode since its version 2.0 released in october 2000. Byte
and Unicode strings store their length, so it's possible to embed nul
byte/character.

Python can be compiled in two modes: narrow (:ref:`UTF-16 <utf16>`) and wide (:ref:`UCS-4 <ucs>`).
``sys.maxunicode`` constant is 0xFFFF in narrow mode, and 0x10FFFF in wide mode.
Python is compiled in narrow mode on Windows, because :c:type:`wchar_t` is also 16 bits
on Windows and so it is possible to use Python Unicode strings as :c:type:`wchar_t*`
strings without any (expensive) conversion.

See also the :ref:`Python Unicode HOWTO <http://docs.python.org/howto/unicode.html>`.


.. _python2:

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
decoded from the default encoding (:ref:`ASCII`). This coercion was a bad design idea
because it was the source of a lot of confusion. At the same time, it was not
possible to switch completly to Unicode in 2000: computers were slower and
there were fewer Python core developers. It took 8 years to switch completly to
Unicode: Python 3 was relased in december 2008.

Narrow mode of Python 2 has a partial support of :ref:`non-BMP <bmp>` characters. unichr()
function raise an error for code bigger than U+FFFF, whereas literal strings
support non-BMP characters (eg. ``'\U00010000'``). Non-BMP characters are
encoded as surrogate pairs (see :ref:`UTF-16 surrogate pairs`). The disavantage is
that ``len(u'\U00010000')`` is 2, and ``u'\U00010000'[0]`` is ``u'\uDC80'``
(lone surrogate character).

In Python 2, it is possible to change the default encoding, but it is a bad idea
because it impacts all libraries which may suppose that the default encoding is
ASCII.


.. _python3:

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

Python 3 has a full support of :ref:`non-BMP <bmp>` characters, in narrow and wide modes.
But as Python 2, chr(0x10FFFF) creates a string of 2 characters (a UTF-16
surrogate pair, see :ref:`UTF-16 surrogate pairs`) in a narrow mode. ``chr()`` and
``ord()`` supports non-BMP characters in both modes.

Python 3 uses U+DC80—U+DCFF character range to store undecodable bytes with the
``surrogateescape`` error handler, described in the `PEP 383`_ (*Non-decodable
Bytes in System Character Interfaces*). It is used for filenames and
environment variables on UNIX and BSD systems. Example:
``b'abc\xff'.decode('ASCII', 'surrogateescape')`` gives ``'abc\uDCFF'``.


Differences between Python 2 and Python 3
'''''''''''''''''''''''''''''''''''''''''

``str + unicode`` gives ``unicode`` in Python 2 (the byte string is decoded
from the default encoding, :ref:`ASCII`) and it raises a ``TypeError`` in Python 3. In
Python 3, comparing ``bytes`` and ``str`` emits a ``BytesWarning`` warning or
raise a ``BytesWarning`` exception depending of the bytes warning flag (``-b``
or ``-bb`` option passed to the Python program). In Python 2, the byte string
is decoded to Unicode using the default encoding (ASCII) before being compared.

:ref:`UTF-8` decoder of Python 2 accept surrogate characters, even if there are
invalid, to keep backward compatibility with Python 2.0. In Python 3, the
decoder rejects surrogate characters.


.. _PEP 383:
   http://www.python.org/dev/peps/pep-0383/


Codecs
''''''

Python has a ``codecs`` module providing text encodings. It supports a lot of
encodings, some examples: ``ASCII``, ``ISO-8859-1``, ``UTF-8``, ``UTF-16-LE``,
``ShiftJIS``, ``Big5``, ``cp037``, ``cp950``, ``EUC_JP``, etc. ``UTF-8``,
``UTF-16-LE``, ``UTF-16-BE``, ``UTF-32-LE`` and ``UTF-32-BE`` don't use :ref:`BOM <bom>`,
whereas ``UTF-8-SIG``, ``UTF-16`` and ``UTF-32`` use BOM. ``mbcs`` is the :ref:`ANSI
code page <Code pages>` and so is only available on Windows.

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
   surrogate characters in :ref:`UTF-8`. It is required because UTF-8 decoder of
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

 * ``BOM_UTF8``, ``BOM_UTF16_BE``, ``BOM_UTF32_LE``, ...: UTF :ref:`BOM <bom>` constants
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

``locale`` module (see :ref:`Locales`):

 * ``getlocale(category)``: get the value of a locale category as the tuple
   (language code, encoding)
 * ``getpreferredencoding()``: get the locale encoding
 * ``LC_ALL``, ``LC_CTYPE``, ...: :ref:`locale categories`
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


.. _php:

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
the beginning of 2010. Read `The Death of PHP 6/The Future of PHP 6 <http://blog.dmcinsights.com/2010/05/25/the-death-of-php-6the-future-of-php-6/>`_ (May 25,
2010 by Larry Ullman) and `Future of PHP6 <http://schlueters.de/blog/archives/128-Future-of-PHP-6.html>`_ (March 2010 by Johannes Schlüter)
for more information.


Perl
----

 * Perl 5.6 (2000): initial Unicode support, store strings as characters
 * Perl 5.8 (2002): regex supports Unicode
 * use "``use utf-8;``" pragma to specify that your Perl script is encoded in
   :ref:`UTF-8`

Read perluniintro, perlunicode and perlunifaq manuals.


.. _java:

Java
----

``char`` is a character able to store Unicode :ref:`BMP <bmp>` only characters
(U+0000—U+FFFF), whereas ``Character`` is a character able to store any Unicode
character (U+0000—U+10FFFF). ``Character`` methods:

 * ``.getType(ch)``: get the Unicode category (see :ref:`Categories`) of a
   character
 * ``.isWhitespace(ch)``: test if a character is a whitespace
   according to Java
 * ``.toUpperCase(ch)``: convert to uppercase

``String`` is a character strings implemented using a ``char`` array, :ref:`UTF-16 <utf16>`
characters. ``String`` methods:

 * ``String(bytes, encoding)``: decode a byte string from the specified
   encoding, throw a ``CharsetDecoder`` exception if a byte sequence cannot be
   decoded.
 * ``.getBytes(encoding)``: encode to the specified encoding, throw a
   ``CharsetEncoder`` exception if a character cannot be encoded.
 * ``.length()``: length in UTF-16 characters.

As :ref:`Python` compiled in narrow mode, :ref:`non-BMP <bmp>` characters are stored as :ref:`UTF-16
surrogate pairs <Surrogate pair>` and the length of a string is the number of UTF-16
characters, not the length in Unicode characters.

Java uses a variant of :ref:`UTF-8` which encodes the nul character (U+0000) as the
overlong byte sequence ``0xC0 0x80``, instead of ``0x00``. This is be able to
use :ref:`C <c>` functions like :c:func:`strlen`. The Tcl language uses the same encoding.


Go and D
--------

The Go and D languages use UTF-8 as internal encoding to store Unicode strings.
