.. _oses:

Operating systems
=================

.. todo:: write an intro for all OS?

.. _win:
.. _Windows:

Windows
-------

Since Windows 2000, Windows offers a nice Unicode API and supports
:ref:`non-BMP characters <bmp>`. It uses :ref:`Unicode strings <str>`
implemented as :c:type:`wchar_t*` strings (LPWSTR). :c:type:`wchar_t` is 16 bits long
on Windows and so it uses :ref:`UTF-16 <utf16>`: :ref:`non-BMP <bmp>`
characters are stored as two :c:type:`wchar_t` (a :ref:`surrogate pair
<surrogates>`), and the length of a string is the number of UTF-16 units and
not the number of characters.

Windows 95, 98 an Me had also Unicode strings, but were limited to :ref:`BMP
characters <bmp>`: they used :ref:`UCS-2 <ucs>` instead of UTF-16.

.. todo:: And Windows CE?


.. index: Code page
.. _codepage:

Code pages
''''''''''

A Windows application has two encodings, called code pages (abbreviated "cp"):
ANSI and OEM code pages. The ANSI code page, :c:macro:`CP_ACP`, is used for the
ANSI version of the :ref:`Windows API <win_api>` to decode :ref:`byte strings <bytes>` to
:ref:`character strings <str>` and has a number between 874 and 1258. The OEM
code page or "IBM PC" code page, :c:macro:`CP_OEMCP`, comes from MS-DOS, is
used for the :ref:`Windows console <win_console>`, contains glyphs to create
text interfaces (draw boxes) and has a number between 437 and 874. Example of a
French setup: ANSI is :ref:`cp1252` and OEM is cp850.

There are code page constants:

 * :c:macro:`CP_ACP`: Windows ANSI code page
 * :c:macro:`CP_MACCP`: Macintosh code page
 * :c:macro:`CP_OEMCP`: ANSI code page of the current process
 * :c:macro:`CP_SYMBOL` (42): Symbol code page
 * :c:macro:`CP_THREAD_ACP`: ANSI code page of the current thread
 * :c:macro:`CP_UTF7` (65000): :ref:`UTF-7 <utf7>`
 * :c:macro:`CP_UTF8` (65001): :ref:`UTF-8 <utf8>`

Functions.

.. c:function:: UINT GetACP()

   Get the ANSI code page number.

.. c:function:: UINT GetOEMCP()

   Get the OEM code page number.

.. c:function:: BOOL SetThreadLocale(LCID locale)

   Set the locale. It can be used to change the ANSI code page of current
   thread (:c:macro:`CP_THREAD_ACP`).

.. seealso::

   Wikipedia article:
   `Windows code page <http://en.wikipedia.org/wiki/Windows_code_page>`_.


Encode and decode functions
'''''''''''''''''''''''''''

Encode and decode functions of ``<windows.h>``.

.. c:function:: MultiByteToWideChar()

   :ref:`Decode <decode>` a :ref:`byte string <bytes>` from a code page to a
   :ref:`character string <str>`. Use :c:macro:`MB_ERR_INVALID_CHARS` flag to
   :ref:`return an error <strict>` on an :ref:`undecodable byte sequence
   <undecodable>`.

   The default behaviour (flags=0) depends on the Windows version:

    - Windows Vista and later: :ref:`replace <replace>` :ref:`undecodable bytes
      <undecodable>`
    - Windows 2000, XP and 2003: :ref:`ignore <ignore>` :ref:`undecodable bytes
      <undecodable>`

   In strict mode (:c:macro:`MB_ERR_INVALID_CHARS`), the :ref:`UTF-8 <utf8>`
   decoder (:c:macro:`CP_UTF8`) returns an error on :ref:`surrogate characters
   <surrogates>` in Windows Vista and later. On Windows XP, the :ref:`UTF-8
   decoder is not strict <strict utf8 decoder>`: surrogates can be decoded in
   any mode.

   The :ref:`UTF-7 <utf7>` decoder (:c:macro:`CP_UTF7`) only supports flags=0.

   Examples on any version Windows version:

   +------------------------+------------------+----------------------+
   | Flags                  | default (0)      | MB_ERR_INVALID_CHARS |
   +========================+==================+======================+
   | ``0xFF``, cp932        | {U+F8F3}         | *error*              |
   +------------------------+------------------+----------------------+
   | ``0xE9 0x80``, cp1252  | {U+00E9, U+20AC} | {U+00E9, U+20AC}     |
   +------------------------+------------------+----------------------+
   | ``0xFF``, CP_UTF7      | {U+FF}           | *invalid flags*      |
   +------------------------+------------------+----------------------+
   | ``0xC3 0xA9``, CP_UTF8 | {U+00E9}         | {U+00E9}             |
   +------------------------+------------------+----------------------+

   Examples on Windows Vista and later:

   +-----------------------------+--------------------------+----------------------+
   | Flags                       | default (0)              | MB_ERR_INVALID_CHARS |
   +=============================+==========================+======================+
   | ``0x81 0x00``, cp932        | {U+30FB, U+0000}         | *error*              |
   +-----------------------------+--------------------------+----------------------+
   | ``0xFF``, CP_UTF8           | {U+FFFD}                 | *error*              |
   +-----------------------------+--------------------------+----------------------+
   | ``0xED 0xB2 0x80``, CP_UTF8 | {U+FFFD, U+FFFD, U+FFFD} | *error*              |
   +-----------------------------+--------------------------+----------------------+

   Examples on Windows 2000, XP, 2003:

   +-----------------------------+-------------+----------------------+
   | Flags                       | default (0) | MB_ERR_INVALID_CHARS |
   +=============================+=============+======================+
   | ``0x81 0x00``, cp932        | {U+0000}    | *error*              |
   +-----------------------------+-------------+----------------------+
   | ``0xFF``, CP_UTF8           | *error*     | *error*              |
   +-----------------------------+-------------+----------------------+
   | ``0xED 0xB2 0x80``, CP_UTF8 | {U+DC80}    | {U+DC80}             |
   +-----------------------------+-------------+----------------------+

.. c:function:: WideCharToMultiByte()

   :ref:`Encode <encode>` a :ref:`character string <str>` to a :ref:`byte
   string <bytes>`. Use :c:macro:`WC_ERR_INVALID_CHARS` flag to have a strict
   encoder: :ref:`return an error <strict>` on :ref:`unencodable character
   <unencodable>`. By default, if :ref:`a character cannot be encoded
   <unencodable>`, it is :ref:`replaced by a character with a similar glyph
   <translit>` or by "?" (U+003F). For example, with :ref:`cp1252`, Ł (U+0141)
   is replaced by L (U+004C).

   Use :c:macro:`WC_NO_BEST_FIT_CHARS` flag to not replace unencodable
   characters by characters with similar glyph. For example, Ł (U+0141) is
   decoded as "?" (U+003F) from :ref:`cp1252` using the
   :c:macro:`WC_NO_BEST_FIT_CHARS` flag.

   On Windows Vista or later with :c:macro:`WC_ERR_INVALID_CHARS` flag, the
   :ref:`UTF-8 <utf8>` encoder (:c:macro:`CP_UTF8`) returns an error on
   :ref:`surrogate characters <surrogates>`. The default behaviour (flags=0)
   depends on the Windows version: surrogates are replaced by U+FFFD on Windows
   Vista and later, and are encoded to UTF-8 on older Windows versions.  The
   :c:macro:`WC_NO_BEST_FIT_CHARS` flag is not supported by the UTF-8 encoder.

   The :ref:`UTF-7 <utf7>` encoder (:c:macro:`CP_UTF7`) only supports flags=0.
   It is not strict: it encodes :ref:`surrogate characters <surrogates>`.

   Examples (on any version Windows version):

   +--------------------+--------------------------------------+----------------------+----------------------+
   | Flags              | default (0)                          | WC_ERR_INVALID_CHARS | WC_NO_BEST_FIT_CHARS |
   +====================+======================================+======================+======================+
   | ÿ (U+00FF), cp932  | ``0x79`` (y)                         | *error*              | ``0x3F`` (?)         |
   +--------------------+--------------------------------------+----------------------+----------------------+
   | Ł (U+0141), cp1252 | ``0x4C`` (L)                         | *error*              | ``0x3F`` (?)         |
   +--------------------+--------------------------------------+----------------------+----------------------+
   | € (U+20AC), cp1252 | ``0x80``                             | *error*              | ``0x80``             |
   +--------------------+--------------------------------------+----------------------+----------------------+
   | U+DC80, CP_UTF7    | ``0x2b 0x33 0x49 0x41 0x2d`` (+3IA-) | *invalid flags*      | *invalid flags*      |
   +--------------------+--------------------------------------+----------------------+----------------------+

   Examples on Windows Vista an later:

   +--------------------+--------------------+----------------------+----------------------+
   | Flags              | default (0)        | WC_ERR_INVALID_CHARS | WC_NO_BEST_FIT_CHARS |
   +====================+====================+======================+======================+
   | U+DC80, CP_UTF8    | ``0xEF 0xBF 0xBD`` | *error*              | *invalid flags*      |
   +--------------------+--------------------+----------------------+----------------------+

   Examples on Windows 2000, XP, 2003:

   +--------------------+--------------------+----------------------+----------------------+
   | Flags              | default (0)        | WC_ERR_INVALID_CHARS | WC_NO_BEST_FIT_CHARS |
   +====================+====================+======================+======================+
   | U+DC80, CP_UTF8    | ``0xED 0xB2 0x80`` | *invalid flags*      | *invalid flags*      |
   +--------------------+--------------------+----------------------+----------------------+

.. note::

   :c:func:`MultiByteToWideChar` and :c:func:`WideCharToMultiByte` functions
   are similar to :c:func:`mbstowcs` and :c:func:`wcstombs` functions.

.. note::

   There are also the :c:func:`OemToCharW`, :c:func:`CharToOemW`,
   :c:func:`AnsiToCharW` and :c:func:`CharToAnsiW` codec functions to
   encode/decode to/from OEM or ANSI code pages, but these functions doesn't
   give control on unencodable characters/undecodable bytes, and can't be used
   to get the size of the output buffer.

.. todo:: Document NormalizeString()

.. todo:: Document the replacement character?


.. _win_api:

Windows API: ANSI and wide versions
'''''''''''''''''''''''''''''''''''

Windows has two versions of each function of its API: the ANSI version using
:ref:`byte strings <bytes>` (``A`` suffix) and the :ref:`ANSI code page
<codepage>`, and the wide version (``W`` suffix) using :ref:`character strings
<str>`. There are also functions without suffix using :c:type:`TCHAR*` strings:
if the :ref:`C <c>` define :c:macro:`_UNICODE` is defined, :c:type:`TCHAR` is
replaced by :c:type:`wchar_t` and the Unicode functions are used; otherwise
:c:type:`TCHAR` is replaced by :c:type:`char` and the ANSI functions are used.
Example:

 * :c:func:`CreateFileA()`: bytes version, use :ref:`byte strings <bytes>`
   encoded to the ANSI code page
 * :c:func:`CreateFileW()`: Unicode version, use :ref:`wide character strings
   <str>`
 * :c:func:`CreateFile()`: :c:type:`TCHAR` version depending on the
   :c:macro:`_UNICODE` define

Always prefer the Unicode version to avoid encoding/decoding errors, and use
directly the ``W`` suffix to avoid compiling issues.

.. note::

   There is a third version of the API: the MBCS API (multibyte character
   string). Use the TCHAR functions and define :c:macro:`_MBCS` to use the MBCS
   functions.  For example, :c:func:`_tcsrev` is replaced by :c:func:`_mbsrev`
   if :c:macro:`_MBCS` is defined, by :c:func:`_wcsrev` if :c:macro:`_UNICODE`
   is defined, or by :c:func:`_strrev` otherwise.



Windows string types
''''''''''''''''''''

 * LPSTR (LPCSTR): :ref:`byte string <bytes>`, :c:type:`char*` (:c:type:`const char*`)
 * LPWSTR (LPCWSTR): :ref:`wide character string <str>`, :c:type:`wchar_t*`
   (:c:type:`const wchar_t*`)
 * LPTSTR (LPCTSTR): byte or wide character string depending of ``_UNICODE``
   define, :c:type:`TCHAR*` (:c:type:`const TCHAR*`)


Filenames
'''''''''

Windows stores filenames as Unicode in the filesystem. Filesystem wide
character POSIX-like API:

.. c:function:: int _wfstat(const wchar_t* filename, struct _stat *statbuf)

   Unicode version of :c:func:`stat()`.

.. c:function:: FILE *_wfopen(const wchar_t* filename, const wchar_t *mode)

   Unicode version of :c:func:`fopen`.

.. c:function:: int _wopen(const wchar_t *filename, int oflag[, int pmode])

   Unicode version of :c:func:`open`.

POSIX functions, like :c:func:`fopen()`, use the :ref:`ANSI code page
<codepage>` to encode/decode strings.


.. _win_console:

Windows console
'''''''''''''''

Console functions.

.. c:function:: GetConsoleCP()

   Get the ccode page of the standard input (stdin) of the console.

.. c:function:: GetConsoleOutputCP()

   Get the code page of the standard output (stdout and stderr) of the console.

.. c:function:: WriteConsoleW()

   Write a :ref:`character string <str>` into the console.

.. todo:: document ReadConsoleW()?

To improve the :ref:`Unicode support <support>` of the console, set the
console font to a TrueType font (e.g. "Lucida Console") and use the wide
character API

If the console is unable to render a character, it tries to use a
:ref:`character with a similar glyph <translit>`. For example, with OEM
:ref:`code page <codepage>` 850, Ł (U+0141) is replaced by L (U+0041). If no
replacment character can be found, "?" (U+003F) is displayed instead.

In a console (``cmd.exe``), ``chcp`` command can be used to display or to
change the :ref:`OEM code page <codepage>` (and console code page). Change the
console code page is not a good idea because the ANSI API of the console still
expect characters encoded to the previous console code page.

.. seealso::

   `Conventional wisdom is retarded, aka What the @#%&* is _O_U16TEXT?
   <http://blogs.msdn.com/b/michkap/archive/2008/03/18/8306597.aspx>`_ (Michael
   S.  Kaplan, 2008) and the Python bug report #1602: `windows console doesn't
   print or input Unicode <http://bugs.python.org/issue1602>`_.

.. note::

   Set the console :ref:`code page <codepage>` to cp65001 (:ref:`UTF-8`)
   doesn't improve Unicode support, it is the opposite: non-ASCII are not
   rendered correctly and type non-ASCII characters (e.g. using the keyboard)
   doesn't work correctly, especially using raster fonts.


File mode
'''''''''

:c:func:`_setmode` and :c:func:`_wsopen` are special functions to set the
encoding of a file:

 * :c:macro:`_O_U8TEXT`: :ref:`UTF-8` without :ref:`BOM <bom>`
 * :c:macro:`_O_U16TEXT`: :ref:`UTF-16 <utf16>` without BOM
 * :c:macro:`_O_WTEXT`: UTF-16 with BOM

:c:func:`fopen` can use these modes using ``ccs=`` in the file mode:

 * ``ccs=UNICODE``: :c:macro:`_O_WTEXT`
 * ``ccs=UTF-8``: :c:macro:`_O_UTF8`
 * ``ccs=UTF-16LE``: :c:macro:`_O_UTF16`

.. todo:: Consequences on TTY and pipes?


.. _osx:

Mac OS X
--------

Mac OS X uses :ref:`UTF-8` for the filenames. If a filename is an invalid UTF-8
byte string, Mac OS X :ref:`returns an error <strict>`. The filenames are
:ref:`decomposed <normalization>` to an incompatible variant of the Normal Form
D (NFD). Extract of the `Technical Q&A QA1173
<http://developer.apple.com/mac/library/qa/qa2001/qa1173.html>`_: "For example,
HFS Plus uses a variant of Normal Form D in which U+2000 through U+2FFF, U+F900
through U+FAFF, and U+2F800 through U+2FAFF are not decomposed."


.. _locales:

Locales
-------

To support different languages and encodings, UNIX and BSD operating systems
have "locales". Locales are process-wide: if a thread or a library change the
locale, the whole process is impacted.


.. _locale categories:

Locale categories
'''''''''''''''''

Locale categories:

 * :c:macro:`LC_COLLATE`: compare and sort strings
 * :c:macro:`LC_CTYPE`: decode :ref:`byte strings <bytes>` and encode
   :ref:`character strings <str>`
 * :c:macro:`LC_MESSAGES`: language of messages
 * :c:macro:`LC_MONETARY`: monetary formatting
 * :c:macro:`LC_NUMERIC`: number formatting (e.g. thousands separator)
 * :c:macro:`LC_TIME`: time and date formatting

:c:macro:`LC_ALL` is a special category: if you set a locale using this
category, it sets the locale for all categories.

Each category has its own environment variable with the same name. For
example, ``LC_MESSAGES=C`` displays error messages in English. To get the
value of a locale category, ``LC_ALL``, ``LC_xxx`` (e.g. ``LC_CTYPE``) or
``LANG`` environment variables are checked: use the first non empty variable.
If all variables are unset, fallback to the C locale.

.. note::

   The gettext library reads ``LANGUAGE``, ``LC_ALL`` and ``LANG`` environment
   variables (and some others) to get the user language. The ``LANGUAGE``
   variable is specific to gettext and is not related to locales.

The C locale
''''''''''''

When a program starts, it does not get directly the user locale: it uses the
default locale which is called the "C" locale or the "POSIX" locale. It is also
used if no locale environment variable is set. For :c:macro:`LC_CTYPE`, the C
locale usually means :ref:`ASCII`, but not always (see the locale
encoding section). For :c:macro:`LC_MESSAGES`, the C locale means to speak the
original language of the program, which is usually English.


.. _locale encoding:

Locale encoding
'''''''''''''''

For Unicode, the most important locale category is ``LC_CTYPE``: it is used to
set the "locale encoding".

To get the locale encoding:

 * Copy the current locale: ``setlocale(LC_CTYPE, NULL)``
 * Set the current locale encoding to the user preference: ``setlocale(LC_CTYPE, "")``
 * Use ``nl_langinfo(CODESET)`` if available
 * or ``setlocale(LC_CTYPE, NULL)``

.. todo:: write a full example in C

For the C locale, ``nl_langinfo(CODESET)`` returns :ref:`ASCII`, or an alias
to this encoding (e.g. "US-ASCII" or "646"). But on FreeBSD, Solaris and
:ref:`Mac OS X <osx>`, codec functions (e.g. :c:func:`mbstowcs`) use
:ref:`ISO-8859-1` even if ``nl_langinfo(CODESET)`` announces ASCII encoding.
AIX uses :ref:`ISO-8859-1` for the C locale (and ``nl_langinfo(CODESET)``
returns ``"ISO8859-1"``).


Locale functions
''''''''''''''''

``<locale.h>`` functions.

.. c:function:: char* setlocale(category, NULL)

   Get the value of the specified locale category.

.. c:function:: char* setlocale(category, name)

   Set the value of the specified locale category.

.. todo:: setlocale("") means user preference

``<langinfo.h>`` functions.

.. c:function::  char* nl_langinfo(CODESET)

   Get the name of the locale encoding.

``<stdlib.h>`` functions.

.. c:function:: size_t mbstowcs(wchar_t *dest, const char *src, size_t n)

   :ref:`Decode <decode>` a :ref:`byte string <bytes>` from the :ref:`locale encoding <locale
   encoding>` to a :ref:`character string <str>`. The decoder is :ref:`strict
   <strict>`: it returns an error on :ref:`undecodable byte sequence
   <undecodable>`. If available, prefer the reentrant version:
   :c:func:`mbsrtowcs`.

.. c:function:: size_t wcstombs(char *dest, const wchar_t *src, size_t n)

   :ref:`Encode <encode>` a :ref:`character string <str>` to a :ref:`byte string <bytes>` in
   the :ref:`locale encoding <locale encoding>`. The encoder is :ref:`strict
   <strict>` : it returns an error if :ref:`a character cannot by encoded
   <unencodable>`.  If available, prefer the reentrant version:
   :c:func:`wcsrtombs`.

mbstowcs() and wcstombs() are :ref:`strict <strict>` and don't support
:ref:`error handlers <errors>`.

.. note::

   "mbs" stands for "multibyte string" (byte string) and "wcs" stands for "wide
   character string".

On Windows, the "locale encoding" are the :ref:`ANSI and OEM code pages
<codepage>`. A Windows program uses the user preferred code pages at startup,
whereas a program starts with the C locale on UNIX.


.. _filename:

Filesystems (filenames)
-----------------------

CD-ROM and DVD
''''''''''''''

CD-ROM uses the ISO 9660 filesystem which stores filenames as :ref:`byte
strings <bytes>`.  This filesystem is very restrictive: only A-Z, 0-9, _ and
"." are allowed.  Microsoft has developped the Joliet extension: store
filenames as :ref:`UCS-2 <ucs>`, up to 64 characters (:ref:`BMP <bmp>` only).
It was first supported by Windows 95.  Today, all operationg systems are able
to read it.

UDF (Universal Disk Format) is the filesystem of DVD: it stores filenames as
character strings.

.. todo:: UDF encoding?


Microsoft: FAT and NTFS filesystems
'''''''''''''''''''''''''''''''''''

MS-DOS uses the FAT filesystems (FAT 12, FAT 16, FAT 32): filenames are stored
as :ref:`byte strings <bytes>`. Filenames are limited to 8+3 characters (8 for
the name, 3 for the extension) and displayed differently depending on the
:ref:`code page <codepage>` (:ref:`mojibake issue <mojibake>`).

Microsoft extended its FAT filesystem in Windows 95: the Virtual FAT (VFAT)
supports "long filenames", filenames are stored as :ref:`UCS-2 <ucs>`, up to
255 characters (BMP only). Starting at Windows 2000, :ref:`non-BMP characters
<bmp>` can be used: :ref:`UTF-16 <utf16>` replaces UCS-2 and the limit is now
255 UTF-16 units.

The NTFS filesystem stores filenames as character strings.

.. todo:: NTFS encoding

Apple: HFS and HFS+ filesystems
'''''''''''''''''''''''''''''''

HFS stores filenames as byte strings.

HFS+ stores filenames as :ref:`UTF-16 <utf16>`: the maximum length is 255
UTF-16 units.


Others
''''''

JFS and ZFS also use Unicode.

The ext family (ext2, ext3, ext4) store filenames as byte strings.

.. todo:: Linux: mount options (FAT, NFSv3)
.. todo:: USB keys, camera, memory cards
.. todo:: Network fileystems like NFS (NFS4 supports Unicode?)

