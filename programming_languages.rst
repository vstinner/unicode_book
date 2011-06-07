.. _prog:

Programming languages
=====================

.. _c:

C language
----------

The C language is a low level language, close to the hardware. It has a builtin
:ref:`character string <str>` type (:c:type:`wchar_t*`), but only few libraries
support this type. It is usually used as the first "layer" between the kernel
(system calls, e.g.  open a file) and applications, higher level libraries and
other programming languages. This first layer uses the same type than the
kernel: except :ref:`Windows`, all kernels use :ref:`byte strings <bytes>`.

There are higher level libraries, like :ref:`glib <glib>` or :ref:`Qt <qt>`,
offering a Unicode API, even if the underlying kernel use byte strings. Such
libraries use a codec to :ref:`encode <encode>` data to the kernel and to
:ref:`decode <decode>` data from the kernel. The codec is usually the current
:ref:`locale encoding <locale encoding>`.

Because there is no Unicode standard library, most third-party libraries chose
the simple solution: use :ref:`byte strings <str>`. For example, the OpenSSL library, an
open source cryptography toolkit, expects :ref:`filenames <filename>` as byte strings. On
Windows, you have to encode Unicode filenames to the current :ref:`ANSI code
page <codepage>`, which is a small subset of the Unicode charset.

.. todo:: "Because there is no Unicode standard library": add historical/compatibilty reasons

Byte API (char)
'''''''''''''''

.. c:type:: char

    For historical reasons, :c:type:`char` is the C type for a character ("char" as
    "character"). In pratical, it's only true for 7 and 8 bits encodings like :ref:`ASCII`
    or :ref:`ISO-8859-1`. With multibyte encodings, a :c:type:`char` is only one byte. For example, the
    character "é" (U+00E9) is encoded as two bytes (``0xC3 0xA9``) in :ref:`UTF-8`.

    :c:type:`char` is a 8 bits integer, it is signed or not depending on the
    operating system and the compiler. On Linux, the GNU compiler (gcc) uses a
    signed type for Intel CPU. It defines :c:macro:`__CHAR_UNSIGNED__` if
    :c:type:`char` type is unsigned. Check if the :c:macro:`CHAR_MAX` constant
    from ``<limits.h>`` is equal to 255 to check if :c:type:`char` is unsigned.

    A literal byte is written between apostrophes, e.g. ``'a'``. Some control
    characters can be written with an backslash plus a letter (e.g. ``'\n'`` = 10).
    It's also possible to write the value in octal (e.g. ``'\033'`` = 27) or
    hexadecimal (e.g. ``'\x20'`` = 32). An apostrophe can be written ``'\''`` or
    ``'\x27'``. A backslash is written ``'\\'``.

    ``<ctype.h>`` contains functions to manipulate bytes, like
    :c:func:`toupper` or :c:func:`isprint`.

.. todo:: toupper() and isprint() are locale dependent


Byte string API (char*)
'''''''''''''''''''''''

.. todo:: :c:type:`char*` points to char, not char*

.. c:type:: char*

   :c:type:`char*` is a a :ref:`byte string <bytes>`. This type is used
   in many places in the C standard library. For example, :c:func:`fopen` uses
   :c:type:`char*` for the filename.

   ``<string.h>`` is the byte string library. Most functions starts with "str"
   (string) prefix: :c:func:`strlen`, :c:func:`strcat`, etc. ``<stdio.h>`` contains useful string
   functions like :c:func:`snprintf` to format a message.

   The length of a string is stored directly in the string as a nul byte at the end. This
   is a problem with encodings using nul bytes (e.g. :ref:`UTF-16 <utf16>` and :ref:`UTF-32 <utf32>`): :c:func:`strlen()`
   cannot be used to get the length of the string, whereas most C functions
   suppose that :c:func:`strlen` gives the length of the string. To support such
   encodings, the length should be stored differently (e.g. in another variable or
   function argument) and :c:func:`str*` functions should be replaced by :c:type:`mem*`
   functions (e.g. replace ``strcmp(a, b) == 0`` by ``memcmp(a, b) == 0``).

   A literal byte strings is written between quotes, e.g. ``"Hello World!"``. As byte
   literal, it's possible to add control characters and characters in octal or
   hexadecimal, e.g. ``"Hello World!\n"``.

.. todo:: Create a section for NUL byte/character


Character API (wchar_t)
'''''''''''''''''''''''

.. c:type:: wchar_t

   With ISO C99 comes :c:type:`wchar_t`: the :ref:`character <character>` type.
   It can be used to store Unicode characters. As :c:type:`char`, it has a
   library: ``<wctype.h>`` contains functions like :c:func:`towupper` or
   :c:func:`iswprint` to manipulate characters.

   :c:type:`wchar_t` is a 16 or 32 bits integer, signed or not. Linux uses 32
   bits signed integer. Mac OS X uses 32 bits integer. Windows uses 16 bits
   integer (:ref:`BMP <bmp>` only). Check if the :c:macro:`WCHAR_MAX` constant
   from ``<wchar.h>`` is equal to 0xFFFF to check if :c:type:`wchar_t` is a 16
   bits unsigned integer.

   A literal character is written between apostrophes with the ``L`` prefix, e.g.
   ``L'a'``. As byte literal, it's possible to write control character with an
   backslash and a character with its value in octal or hexadecimal. For codes
   bigger than 255, ``'\uHHHH'`` syntax can be used. For codes bigger than 65535,
   ``'\UHHHHHHHH'`` syntax can be used with 32 bits :c:type:`wchar_t`.

.. todo:: towupper() and iswprint() are locale dependent
.. todo:: is wchar_t signed on Windows and Mac OS X?
.. todo:: can wchar_t be signed?


Character string API (wchar_t*)
'''''''''''''''''''''''''''''''

.. c:type:: wchar_t*

   With ISO C99 comes :c:type:`wchar_t*`: the :ref:`character string <str>`
   type. The standard library ``<wchar.h>`` contains character string functions
   like :c:func:`wcslen` or :c:func:`wprintf`, and constants like
   :c:macro:`WCHAR_MAX`. If :c:type:`wchar_t` is 16 bits long, :ref:`non-BMP
   <bmp>` characters are encoded to :ref:`UTF-16 <utf16>` as :ref:`surrogate
   pairs <surrogates>`.

   A literal character strings is written between quotes with the ``L``
   prefix, e.g. ``L"Hello World!\n"``. As character literals, it supports also control
   character, codes written in octal, hexadecimal, ``L"\uHHHH"`` and ``L"\UHHHHHHHH"``.

POSIX.1-2001 has no function ignoring case to compare character strings.
POSIX.1-2008, a recent standard, adds :c:func:`wcscasecmp`: the GNU libc has it
has an extension (if :c:macro:`_GNU_SOURCE` is defined). Windows has the
:c:func:`_wcsnicmp` function.

:ref:`Windows` uses (:ref:`UTF-16 <utf16>`) wchar_t* strings for its Unicode
API.


printf functions family
'''''''''''''''''''''''

.. c:function:: int printf(const char* format, ...)

.. c:function:: int wprintf(const wchar_t* format, ...)


Formats of string arguments for the printf functions:

 * ``"%s"``: literal byte string (:c:type:`char*`)
 * ``"%ls"``: literal character string (:c:type:`wchar_t*`)

``printf("%ls")`` is :ref:`strict <strict>`: it stops immediatly if a
:ref:`character string <str>` argument :ref:`cannot be encoded <unencodable>`
to the :ref:`locale encoding <locale encoding>`. For example, the following
code prints the truncated string "Latin capital letter L with stroke: [" if
Ł (U+0141) cannot be encoded to the locale encoding. ::

    printf("Latin capital letter L with stroke: [%ls]\n", L"\u0141");

``wprintf("%s")`` is also :ref:`strict <strict>`: it stops immediatly if
:ref:`a byte string <bytes>` argument :ref:`cannot be decoded <undecodable>`
from the :ref:`locale encoding <locale encoding>`. For example, the following
code prints the truncated string "Latin capital letter L with stroke: [" if
``0xC5 0x81`` (U+0141 encoded to :ref:`UTF-8`) cannot be decoded from the
:ref:`locale encoding <locale encoding>`. ::

    wprintf(L"Latin capital letter L with stroke): [%s]\n", "\xC5\x81");

``wprintf("%ls")`` :ref:`replaces <replace>` :ref:`unencodable <unencodable>`
:ref:`character string <str>` arguments by ? (U+003F). For example, the
following example print "Latin capital letter L with stroke: [?]" if Ł (U+0141)
cannot be encoded to the :ref:`locale encoding <locale encoding>`: ::

    wprintf(L"Latin capital letter L with stroke: [%s]\n", L"\u0141");

So to avoid truncated strings, try to use only :c:func:`wprintf` with character
string arguments.

.. todo:: how are non-ASCII characters handled in the format string?

.. note::

   There is also ``"%S"`` format which is a deprecated alias to the ``"%ls"``
   format, don't use it.

.. todo:: locale encoding should be initialized.


.. _cpp:

C++
---

 * ``std::wstring``: :ref:`character string <str>` using the
   :c:type:`wchar_t` type, Unicode version of ``std::string`` (:ref:`byte
   string <bytes>`)
 * ``std::wcin``, ``std::wcout`` and ``std::wcerr``: standard input, output
   and error output; Unicode version of ``std::cin``, ``std::cout`` and
   ``std::cerr``
 * ``std::wostringstream``: character stream buffer; Unicode version of
   ``std::ostringstream``.

To initialize the :ref:`locales <locales>`, equivalent to ``setlocale(LC_ALL,
"")``, use: ::

    #include <locale>
    std::locale::global(std::locale(""));

If you use also C and C++ functions (e.g. :c:func:`printf` and ``std::cout``)
to access the standard streams, you may have issues with :ref:`non-ASCII
<ascii>` characters.  To avoid these issues, you can disable the automatic
synchronization between C (``std*``) and C++ (``std::c*``) streams using: ::

    #include <iostream>
    std::ios_base::sync_with_stdio(false);

.. note::

   Use ``typedef basic_ostringstream<wchar_t> wostringstream;`` if
   wostringstream is not available.


.. _Python:

Python
------

Python supports Unicode since its version 2.0 released in october 2000.
:ref:`Byte <bytes>` and :ref:`Unicode <str>` strings store their length, so
it's possible to embed nul byte/character.

Python can be compiled in two modes: narrow (:ref:`UTF-16 <utf16>`) and wide (:ref:`UCS-4 <ucs>`).
``sys.maxunicode`` constant is 0xFFFF in narrow build, and 0x10FFFF in wide build.
Python is compiled in narrow mode on Windows, because :c:type:`wchar_t` is also 16 bits
on Windows and so it is possible to use Python Unicode strings as :c:type:`wchar_t*`
strings without any (expensive) conversion.

.. seealso::

   `Python Unicode HOWTO <http://docs.python.org/howto/unicode.html>`_.


.. _python2:

Python 2
''''''''

``str`` is the :ref:`byte string <bytes>` type and ``unicode`` is the
:ref:`character string <str>` type. Literal byte strings are written ``b'abc'`` (syntax
compatible with Python 3) or ``'abc'`` (legacy syntax), ``\xHH`` can be used to
write a byte by its hexadecimal value (e.g. ``b'\x80'`` for 128). Literal
Unicode strings are written with the prefix ``u``: ``u'abc'``. Code points can
be written as hexadecimal: ``\xHH`` (U+0000—U+00FF), ``\uHHHH``
(U+0000—U+FFFF) or ``\UHHHHHHHH`` (U+0000—U+10FFFF), e.g. ``'euro
sign:\u20AC'``.

In Python 2, ``str + unicode`` gives ``unicode``: the byte string is
:ref:`decoded <decode>` from the default encoding (:ref:`ASCII`). This coercion was a bad design idea
because it was the source of a lot of confusion. At the same time, it was not
possible to switch completly to Unicode in 2000: computers were slower and
there were fewer Python core developers. It took 8 years to switch completly to
Unicode: Python 3 was relased in december 2008.

Narrow build of Python 2 has a partial support of :ref:`non-BMP <bmp>`
characters. The unichr() function raises an error for code bigger than U+FFFF,
whereas literal strings support non-BMP characters (e.g. ``'\U0010FFFF'``).
Non-BMP characters are encoded as :ref:`surrogate pairs <surrogates>`. The
disavantage is that ``len(u'\U00010000')`` is 2, and ``u'\U0010FFFF'[0]`` is
``u'\uDBFF'`` (lone surrogate character).

.. note::

   **DO NOT CHANGE THE DEFAULT ENCODING!** Calling sys.setdefaultencoding() is
   a very bad idea because it impacts all libraries which suppose that the
   default encoding is ASCII.


.. _python3:

Python 3
''''''''

``bytes`` is the :ref:`byte string <bytes>` type and ``str`` is the
:ref:`character string <str>` type. Literal byte strings are written with the ``b`` prefix:
``b'abc'``. ``\xHH`` can be used to write a
byte by its hexadecimal value, e.g. ``b'\x80'`` for 128. Literal Unicode strings are
written ``'abc'``. Code points can be used directly in hexadecimal: ``\xHH``
(U+0000—U+00FF), ``\uHHHH`` (U+0000—U+FFFF) or ``\UHHHHHHHH``
(U+0000—U+10FFFF), e.g. ``'euro sign:\u20AC'``. Each item of a byte string is
an integer in range 0—255: ``b'abc'[0]`` gives 97, whereas ``'abc'[0]`` gives
``'a'``.

Python 3 has a full support of :ref:`non-BMP <bmp>` characters, in narrow and
wide builds. But as Python 2, chr(0x10FFFF) creates a string of 2 characters (a
:ref:`UTF-16 surrogate pair <surrogates>`) in a narrow build. ``chr()`` and
``ord()`` supports non-BMP characters in both modes.

Python 3 uses U+DC80—U+DCFF character range to store :ref:`undecodable bytes <undecodable>` with the
``surrogateescape`` error handler, described in the `PEP 383`_ (*Non-decodable
Bytes in System Character Interfaces*). It is used for filenames and
environment variables on UNIX and BSD systems. Example:
``b'abc\xff'.decode('ASCII', 'surrogateescape')`` gives ``'abc\uDCFF'``.


Differences between Python 2 and Python 3
'''''''''''''''''''''''''''''''''''''''''

``str + unicode`` gives ``unicode`` in Python 2 (the byte string is decoded
from the default encoding, :ref:`ASCII`) and it raises a ``TypeError`` in Python 3. In
Python 3, comparing ``bytes`` and ``str`` gives ``False``, emits a ``BytesWarning`` warning or
raises a ``BytesWarning`` exception depending of the bytes warning flag (``-b``
or ``-bb`` option passed to the Python program). In Python 2, the byte string
is :ref:`decoded <decode>` from the default encoding (ASCII) to Unicode before being compared.

:ref:`UTF-8` decoder of Python 2 accept :ref:`surrogate characters
<surrogates>`, even if there are invalid, to keep backward compatibility with
Python 2.0. In Python 3, the :ref:`UTF-8 decoder is strict <strict utf8 decoder>`:
it rejects surrogate characters.


.. _PEP 383:
   http://www.python.org/dev/peps/pep-0383/


Codecs
''''''

The ``codecs`` and ``encodings`` module provide text encodings. They supports a lot of
encodings. Some examples: ASCII, ISO-8859-1, UTF-8, UTF-16-LE,
ShiftJIS, Big5, cp037, cp950, EUC_JP, etc.

``UTF-8``, ``UTF-16-LE``, ``UTF-16-BE``, ``UTF-32-LE`` and ``UTF-32-BE`` don't
use :ref:`BOM <bom>`, whereas ``UTF-8-SIG``, ``UTF-16`` and ``UTF-32`` use BOM.
``mbcs`` is only available on Windows: it is the :ref:`ANSI code page
<codepage>`.

Python provides also many :ref:`error handlers <errors>` used to specify how to handle
:ref:`undecodable byte sequences <undecodable>` and :ref:`unencodable characters
<unencodable>`:

 * ``strict`` (default): raise a ``UnicodeDecodeError`` or a ``UnicodeEncodeError``
 * ``replace``: replace undecodable bytes by � (U+FFFD) and unencodable
   characters by ``?`` (U+003F)
 * ``ignore``: ignore undecodable bytes and unencodable characters
 * ``backslashreplace`` (only to decode): replace undecodable bytes by ``\xHH``

Python 3 has two more error handlers:

 * ``surrogateescape``: replace undecodable bytes (non-ASCII: ``0x80``\ —\
   ``0xFF``) by :ref:`surrogate characters <surrogates>` (in U+DC80—U+DCFF) on
   decoding, replace characters in range U+DC80—U+DCFF by bytes in
   ``0x80``\ —\ ``0xFF`` on encoding.  Read the `PEP 383`_ (*Non-decodable
   Bytes in System Character Interfaces*) for the details.
 * ``surrogatepass``, specific to ``UTF-8`` codec: allow encoding/decoding
   surrogate characters in :ref:`UTF-8`. It is required because UTF-8 decoder of
   Python 3 rejects surrogate characters by default.

Decoding examples in Python 3:

 * ``b'abc\xff'.decode('ASCII')`` uses the ``strict`` error handler and raises
   an ``UnicodeDecodeError``
 * ``b'abc\xff'.decode('ASCII', 'ignore')`` gives ``'abc'``
 * ``b'abc\xff'.decode('ASCII', 'replace')`` gives ``'abc\uFFFD'``
 * ``b'abc\xff'.decode('ASCII', 'surrogateescape')`` gives
   ``'abc\uDCFF'``

Encoding examples in Python 3:

 * ``'\u20ac'.encode('UTF-8')`` gives ``b'\xe2\x82\xac'``
 * ``'abc\xff'.encode('ASCII')`` uses the ``strict`` error handler and raises
   an ``UnicodeEncodeError``
 * ``'abc\xff'.encode('ASCII', 'backslashreplace')`` gives ``b'abc\\xff'``


String methods
''''''''''''''

:ref:`Byte string <bytes>` (``str`` in Python 2, ``bytes`` in Python 3) methods:

 * ``.decode(encoding, errors='strict')``: :ref:`decode <decode>` from the specified encoding
   and (optional) :ref:`error handler <errors>`.

:ref:`Character string <str>` (``unicode`` in Python 2, ``str`` in Python 3) methods:

 * ``.encode(encoding, errors='strict')``: :ref:`encode <encode>` to the
   specified encoding with an (optional) :ref:`error handler <errors>`
 * ``.isprintable()``: ``False`` if the :ref:`character category <unicode
   categories>` is other (Cc, Cf, Cn, Co, Cs) or separator (Zl, Zp, Zs),
   ``True`` otherwise. There is an exception: even if U+0020 is a separator,
   ``' '.isprintable()`` gives ``True``.
 * ``.toupper()``: convert to uppercase


Filesystem
''''''''''

Python decodes bytes filenames and encodes Unicode filenames using the
filesystem encoding, ``sys.getfilesystemencoding()``:

 * ``mbcs`` (:ref:`ANSI code page <codepage>`) on :ref:`Windows`
 * ``UTF-8`` on :ref:`Mac OS X <osx>`
 * :ref:`locale encoding <locale encoding>` otherwise

Python uses the ``strict`` :ref:`error handler <errors>` in Python 2, and
``surrogateescape`` (PEP 383) in Python 3. In Python 2, if ``os.listdir(u'.')``
cannot decode a filename, it keeps the bytes filename unchanged. Thanks to
``surrogateescape``, decode a filename does never fail in Python 3. But
encoding a filename can fail in Python 2 and 3 depending on the filesystem
encoding. For example, on Linux with the C locale, the Unicode filename
``"h\xe9.py"`` cannot be encoded because the filesystem encoding is ASCII.

In Python 2, use ``os.getcwdu()`` to get the current directory as Unicode.


Modules
'''''''

``codecs`` module:

 * ``BOM_UTF8``, ``BOM_UTF16_BE``, ``BOM_UTF32_LE``, ...: :ref:`Byte order
   marks (BOM) <bom>` constants
 * ``lookup(name)``: get a Python codec. ``lookup(name).name`` gets the Python
   normalized name of a codec, e.g. ``codecs.lookup('ANSI_X3.4-1968').name``
   gives ``'ascii'``.
 * ``open(filename, mode='rb', encoding=None, errors='strict', ...)``: legacy
   API to open a binary or text file. To open a file in Unicode mode, use
   ``io.open()`` instead

``io`` module:

 * ``open(name, mode='r', buffering=-1, encoding=None, errors=None, ...)``:
   open a binary or text file in read and/or write mode. For text file,
   ``encoding`` and ``errors`` can be used to specify the encoding and the
   :ref:`error handler <errors>`. By default, it opens text files with the :ref:`locale encoding
   <locale encoding>` in :ref:`strict <strict>` mode.
 * ``TextIOWrapper()``: wrapper to read and/or write text files, encode from/decode to
   the specified encoding (and :ref:`error handler <errors>`) and normalize
   newlines (``\r\n`` and ``\r`` are replaced by ``\n``). It requires a
   buffered file. Don't use it directly to open a text file: use ``open()``
   instead.

``locale`` module (:ref:`locales <locales>`):

 * ``LC_ALL``, ``LC_CTYPE``, ...: :ref:`locale categories <locale categories>`
 * ``getlocale(category)``: get the value of a :ref:`locale category <locale
   categories>` as the tuple (language code, encoding name)
 * ``getpreferredencoding()``: get the :ref:`locale encoding <locale encoding>`
 * ``setlocale(category, value)``: set the value of a locale category

``sys`` module:

 * ``getdefaultencoding()``: get the default encoding, e.g. used by
   ``'abc'.encode()``. In Python 3, the default encoding is fixed to
   ``'utf-8'``, in Python 2, it is ``'ascii'`` by default.
 * ``getfilesystemencoding()``: get the filesystem encoding used to decode
   and encode filenames
 * ``maxunicode``: biggest Unicode code point storable in a single Python
   Unicode character, 0xFFFF in narrow build or 0x10FFFF in wide build.

``unicodedata`` module:

 * ``category(char)``: get the :ref:`category <unicode categories>` of a
   character
 * ``name(char)``: get the name of a character
 * ``normalize(string)``: :ref:`normalize <normalization>` a string to the NFC,
   NFD, NFKC or NFKD form

.. todo:: cleanup Python 2/3 here (open)


.. _php:

PHP
---

In PHP 5, a literal string (e.g. ``"abc"``) is a :ref:`byte string <bytes>`.
PHP has no :ref:`character string <str>` type, only a "string" type which is a
:ref:`byte string <bytes>`.

PHP have "multibyte" functions to manipulate byte strings using their encoding.
These functions have an optional encoding argument. If the encoding is not
specified, PHP uses the default encoding (called "internal encoding"). Some
multibyte functions:

 * ``mb_internal_encoding()``: get or set the internal encoding
 * ``mb_substitute_character()``: change how to :ref:`handle <errors>` :ref:`unencodable
   characters <unencodable>`:

   * ``"none"``: :ref:`ignore <ignore>` unencodable characters
   * ``"long"``: :ref:`escape as hexadecimal <escape>` value, e.g. ``"U+E9"``
     or ``"JIS+7E7E"``
   * ``"entity"``: :ref:`escape as HTML entities <escape>`, e.g. ``"&#xE9;"``

 * ``mb_convert_encoding()``: :ref:`decode <decode>` from an encoding and
   :ref:`encode <encode>` to another encoding
 * ``mb_ereg()``: search a pattern using a regular expression
 * ``mb_strlen()``: get the length in characters
 * ``mb_detect_encoding()``: :ref:`detect the encoding <guess>` of a :ref:`byte
   string <bytes>`

Perl compatible regular expressions (PCRE) have an ``u`` flag ("PCRE8") to
process byte strings as UTF-8 encoded strings.

.. todo:: u flag: instead of which encoding?

PHP includes also a binding of the :ref:`iconv <iconv>` library.

 * ``iconv()``: :ref:`decode <decode>` a :ref:`byte string <bytes>` from an
   encoding and :ref:`encode <encode>` to another encoding, you can use
   ``//IGNORE`` or ``//TRANSLIT`` suffix to choose the :ref:`error handler
   <errors>`
 * ``iconv_mime_decode()``: decode a MIME header field

.. todo:: Document utf8_encode() and utf8_decode() functions?

PHP 6 was a project to improve Unicode support of Unicode. This project died at
the beginning of 2010. Read `The Death of PHP 6/The Future of PHP 6 <http://blog.dmcinsights.com/2010/05/25/the-death-of-php-6the-future-of-php-6/>`_ (May 25,
2010 by Larry Ullman) and `Future of PHP6 <http://schlueters.de/blog/archives/128-Future-of-PHP-6.html>`_ (March 2010 by Johannes Schlüter)
for more information.

.. todo:: PHP6 creation date?


Perl
----

 * Perl 5.6 (2000): initial Unicode support, support :ref:`character strings
   <str>`
 * Perl 5.8 (2002): regex supports Unicode
 * use "``use utf-8;``" pragma to specify that your Perl script is encoded to
   :ref:`UTF-8`

Read ``perluniintro``, ``perlunicode`` and ``perlunifaq`` manuals.


.. _java:

Java
----

``char`` is a character able to store Unicode :ref:`BMP <bmp>` only characters
(U+0000—U+FFFF), whereas ``Character`` is a character able to store any Unicode
character (U+0000—U+10FFFF). ``Character`` methods:

 * ``.getType(ch)``: get the :ref:`category <unicode categories>` of a
   character
 * ``.isWhitespace(ch)``: test if a character is a whitespace
   according to Java
 * ``.toUpperCase(ch)``: convert to uppercase

.. todo:: explain isWhitespace()

``String`` is a :ref:`character string <str>` implemented using a
``char`` array and :ref:`UTF-16 <utf16>`. ``String`` methods:

 * ``String(bytes, encoding)``: :ref:`decode <decode>` a :ref:`byte string
   <bytes>` from the specified encoding. The decoder is :ref:`strict <strict>`:
   throw a ``CharsetDecoder`` exception if a :ref:`byte sequence cannot be
   decoded <undecodable>`.
 * ``.getBytes(encoding)``: :ref:`encode <encode>` to the specified encoding,
   throw a ``CharsetEncoder`` exception if a character :ref:`cannot be encoded
   <undecodable>`.
 * ``.length()``: get the length in UTF-16 units.

As :ref:`Python` compiled in narrow mode, :ref:`non-BMP <bmp>` characters are
stored as :ref:`UTF-16 surrogate pairs <surrogates>` and the length of a string
is the number of UTF-16 units, not the number of Unicode characters.

Java, as the Tcl language, uses a variant of :ref:`UTF-8` which encodes the nul
character (U+0000) as the :ref:`overlong byte sequence <strict utf8 decoder>`
``0xC0 0x80``, instead of ``0x00``. So it is possible to use :ref:`C <c>`
functions like :c:func:`strlen` on :ref:`byte string <bytes>` with embeded nul
characters.


Go and D
--------

The Go and D languages use :ref:`UTF-8` as internal encoding to store
:ref:`Unicode strings <str>`.

