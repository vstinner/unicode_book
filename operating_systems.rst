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

Example of text boxes using characters of OEM code pages: ::

  ╔══════════════╗  ╭─────────────╮
  ║ double lines ║  │ single line │
  ╚══════════════╝  ╰─────────────╯

There are some special code pages like cp65001 (Microsoft version of
:ref:`UTF-8`).

Get code pages.

.. c:function:: UINT GetACP()

   Get the ANSI code page number.

.. c:function:: UINT GetOEMCP()

   Get the OEM code page number.

Conversion.

.. c:function:: BOOL OemToCharW(LPCSTR src, LPWSTR dst)

   Decode a :ref:`byte string <bytes>` from the OEM code page.

.. c:function:: BOOL CharToOemW(LPCWSTR src, LPSTR dst)

   Encode a :ref:`character string <str>` to the OEM code page.

.. c:function:: BOOL AnsiToCharW(LPCSTR src, LPWSTR dst)

   Decode a :ref:`byte string <bytes>` from the ANSI code page.

.. c:function:: BOOL CharToAnsiW(LPCWSTR src, LPSTR dst)

   Encode a :ref:`character string <str>` to the ANSI code page.

.. todo:: How are undecodable/unencodable handled?

.. seealso::

   Wikipedia article:
   `Windows code page <http://en.wikipedia.org/wiki/Windows_code_page>`_.


.. _win_api:

Windows API: ANSI and wide versions
'''''''''''''''''''''''''''''''''''

Windows has two versions of each function of its API : the ANSI version using
:ref:`byte strings <bytes>` (``A`` suffix) and the :ref:`ANSI code page <codepage>`, and the
wide version (``W`` suffix) using :ref:`character strings <str>`. There are also functions without suffix
using :c:type:`TCHAR*` strings: if the :ref:`C <c>` define :c:macro:`_UNICODE`
is defined, :c:type:`TCHAR` is :c:type:`wchar_t` and it use the Unicode
functions; otherwise :c:type:`TCHAR` is :c:type:`char` and it uses the ANSI
functions. Example:

 * :c:func:`CreateFileA()`: bytes version, use :ref:`byte strings <bytes>`
   encoded to the ANSI code page
 * :c:func:`CreateFileW()`: Unicode version, use :ref:`wide character strings
   <str>`
 * :c:func:`CreateFile()`: :c:type:`TCHAR` version depending on the
   :c:macro:`_UNICODE` define

Always prefer the Unicode version to avoid encoding/decoding errors, and use
directly the ``W`` suffix to avoid compiling issues.


Windows string types
''''''''''''''''''''

 * LPSTR (LPCSTR): :ref:`byte string <bytes>`, :c:type:`char*` (:c:type:`const char*`)
 * LPWSTR (LPCWSTR): :ref:`wide character string <str>`, :c:type:`wchar_t*`
   (:c:type:`const wchar_t*`)
 * LPTSTR (LPCTSTR): byte or wide character string depending of ``_UNICODE``
   define, :c:type:`TCHAR*` (:c:type:`const TCHAR*`)


Encode and decode functions
'''''''''''''''''''''''''''

Encode and decode functions of ``<windows.h>``.

.. c:function:: MultiByteToWideChar()

   Decode a :ref:`byte string <bytes>` to a :ref:`character string <str>`. It
   supports :ref:`ANSI and OEM code pages <codepage>`,
   UTF-7 and :ref:`UTF-8`. By default, it :ref:`ignores <ignore>`
   :ref:`undecodable bytes <undecodable>`. Use :c:macro:`MB_ERR_INVALID_CHARS`
   flag to :ref:`return an error <strict>` on an undecodable byte sequence.

.. c:function:: WideCharToMultiByte()

   Encode a :ref:`character string <str>` to a :ref:`byte string <bytes>`. As
   :c:func:`MultiByteToWideChar`, it supports :ref:`ANSI <codepage>` and the
   :ref:`OEM <codepage>` code pages, UTF-7 and :ref:`UTF-8`. By default, if
   :ref:`a character cannot be encoded <unencodable>`, it is :ref:`replaced by
   a character with a similar glyph <translit>`. For example, with
   :ref:`cp1252`, Ł (U+0141) is replaced by L (U+004C). Use
   :c:macro:`WC_NO_BEST_FIT_CHARS` flag to :ref:`return an error <strict>` on
   :ref:`unencodable character <unencodable>`.

.. note::

   :c:func:`MultiByteToWideChar` and :c:func:`WideCharToMultiByte` are similar
   to :c:func:`mbstowcs` and :c:func:`wcstombs`.

.. todo:: Document the replacement character?


Filenames
'''''''''

Windows stores filenames as Unicode in the filesystem. Filesystem wide
character POSIX-like API:

.. c:function:: int _wfstat(const wchar_t* filename, struct _stat *statbuf)

   Unicode version of :c:func:`stat()`.

.. c:function:: FILE *_wfopen(const wchar_t* filename, const wchar_t *mode)

   Unicode version of :c:func:`fopen`.

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

:c:func:`_setmode` and :c:func:`_wsopen` are special functions to set the
encoding of a file (especially of stdin, stdout and stderr):

 * :c:macro:`_O_U8TEXT`: :ref:`UTF-8` without :ref:`BOM <bom>`
 * :c:macro:`_O_U16TEXT`: :ref:`UTF-16 <utf16>` without BOM
 * :c:macro:`_O_WTEXT`: UTF-16 with BOM

.. todo:: Consequences on TTY and pipes?

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

   Decode a :ref:`byte string <bytes>` from the :ref:`locale encoding <locale
   encoding>` to a :ref:`character string <str>`. The decoder is :ref:`strict
   <strict>`: it returns an error on :ref:`undecodable byte sequence
   <undecodable>`. If available, prefer the reentrant version:
   :c:func:`mbsrtowcs`.

.. c:function:: size_t wcstombs(char *dest, const wchar_t *src, size_t n)

   Encode a :ref:`character string <str>` to a :ref:`byte string <bytes>` in
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

The NTFS filesystem stores filenames at character strings.

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

