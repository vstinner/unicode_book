Operating systems
=================

.. _win:
.. _Windows:

Windows
-------

Since Windows 2000, Windows offers a nice Unicode API and supports
:ref:`non-BMP characters <bmp>`. It uses :ref:`Unicode strings <str>`
implemented as :c:type:`wchar_t*` strings. :c:type:`wchar_t` is 16 bits long on
Windows and so it uses :ref:`UTF-16 <utf16>`: :ref:`non-BMP <bmp>` characters
are stored as two :c:type:`wchar_t` (a :ref:`surrogate pair <surrogates>`), and
the length of a string is the number of UTF-16 words and not the number of
characters.

Windows 95 and 98 had also Unicode strings, but were limited to :ref:`BMP
characters <bmp>`: they used :ref:`UCS-2 <ucs>` instead of UTF-16.


.. index: Code page
.. _codepage:

Code pages
''''''''''

An application has two encodings, called code pages (abbreviated "cp"): the
ANSI code page (:c:macro:`CP_ACP`) used for the ANSI version of the Windows API to decode a byte
string to a character string, and the OEM code page (:c:macro:`CP_OEMCP`), e.g. used for the console.
Example of a French setup: :ref:`cp1252` for ANSI and cp850 for OEM.

OEM code pages, or "IBM PC" code pages, have a number between 437 and 874 and
come from MS-DOS. They contain graphical glyphs to create text interfaces (draw
boxes). ANSI code pages have numbers between 874 and 1258. There are some
special code pages like 65001 (Microsoft version of :ref:`UTF-8`).

Get code pages.

.. c:function:: UINT GetACP()

   Get the ANSI code page number.

.. c:function:: UINT GetOEMCP()

   Get the OEM code page number.

Conversion.

.. c:function:: BOOL OemToCharW(LPCSTR src, LPWSTR dst)

   Decode a byte string from the OEM code page.

.. c:function:: BOOL CharToOemW(LPCWSTR src, LPSTR dst)

   Encode a character string to the OEM code page.

.. c:function:: BOOL AnsiToCharW(LPCSTR src, LPWSTR dst)

   Decode a byte string from the ANSI code page.

.. c:function:: BOOL CharToAnsiW(LPCWSTR src, LPSTR dst)

   Encode a character string to the ANSI code page.

Read also the `Wikipedia article <http://en.wikipedia.org/wiki/Windows_code_page>`_.


ANSI and Unicode versions of each function
''''''''''''''''''''''''''''''''''''''''''

Windows has two versions of each function of its API : the ANSI version using
byte strings (``A`` suffix) and the :ref:`ANSI code page <codepage>`, and the
wide character version (``W`` suffix). There are also functions without suffix
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
   supports the :ref:`ANSI <codepage>` and :ref:`OEM <codepage>` code pages,
   UTF-7 and :ref:`UTF-8`. By default, it :ref:`ignores <ignore>`
   :ref:`undecodable bytes <undecodable>`. Use :c:macro:`MB_ERR_INVALID_CHARS`
   flag to :ref:`raise an error <strict>` on an undecodable byte sequence.

.. c:function:: WideCharToMultiByte()

   Encode a :ref:`character string <str>` to a :ref:`byte string <bytes>`. As
   :c:func:`MultiByteToWideChar`, it supports :ref:`ANSI <codepage>` and the
   :ref:`OEM <codepage>` code pages, UTF-7 and :ref:`UTF-8`. By default, if
   :ref:`a character cannot be encoded <unencodable>`, it is :ref:`replaced by
   a character with a similar glyph <translit>`. For example, with
   :ref:`cp1252`, Ł (U+0141) is replaced by L (U+004C). Use
   :c:macro:`WC_NO_BEST_FIT_CHARS` flag to :ref:`raise an error <strict>` on
   :ref:`unencodable character <unencodable>`.

.. note::

   :c:func:`MultiByteToWideChar` and :c:func:`WideCharToMultiByte` are similar
   to :c:func:`mbstowcs` and :c:func:`wcstombs`.


Filenames
'''''''''

Windows stores filenames as Unicode in the filesystem. Filesystem wide
character POSIX-like API:

.. c:function:: int _wfstat(const wchar_t* filename, struct _stat *statbuf)

   Unicode version of :c:func:`stat()`.

.. c:function:: FILE *_wfopen(const wchar_t* filename, const wchar_t *mode)

   Unicode version of :c:func:`fopen`.

POSIX functions, like :c:func:`fopen()`, use the :ref:`ANSI code page <codepage>` to encode/decode
strings.


Windows console
'''''''''''''''

Console functions.

.. c:function:: GetConsoleCP()

   Get the ccode page of the standard input (stdin) of the console.

.. c:function:: GetConsoleOutputCP()

   Get the code page of the standard output (stdout and stderr) of the console.

.. c:function:: WriteConsoleW()

   Write a :ref:`character string <str>` into the console.

To improve the :ref:`Unicode support <support>` of the console, set the console
font to a TrueType font (e.g. "Lucida Console") and use the wide character API

If the console is unable to render a character, it tries to use a
:ref:`character with a similar glyph <translit>`. For example, with OEM
:ref:`code page <codepage>` 850, Ł (U+0141) is replaced by L (U+0041). If no
replacment character can be found, "?" (U+003F) is displayed instead.

In a console (``cmd.exe``), ``chcp`` command can be used to display or to
change the :ref:`OEM code page <codepage>` (and console code page). Change the console code page is not a
good idea because the ANSI API of the console still expect characters encoded
to the previous console code page.

:c:func:`_setmode` and :c:func:`_wsopen` are special functions to set the encoding of a
file (especially of stdin, stdout and stderr):

 * :c:macro:`_O_U8TEXT`: :ref:`UTF-8` without :ref:`BOM <bom>`
 * :c:macro:`_O_U16TEXT`: :ref:`UTF-16 <utf16>` without BOM
 * :c:macro:`_O_WTEXT`: UTF-16 with BOM

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


MS-DOS
''''''

Windows inherits from MS-DOS. MS-DOS has also code pages. Commands:

 * ``MODE CON CODEPAGE``: display the current code page
 * ``MODE CON CODEPAGE SELECT=xxx``: set the current code page
 * ``MODE CON CODEPAGE PREPARE=((850)``
 * ``MODE CON CODEPAGE PREPARE=((863,850) C:\WINDOWS\COMMAND\EGA.CPI)``

``CON`` stands for the console device, but another device name can be
specified: ``PRN`` (printer), ``LPT1``, ``LPT2`` or ``LPT3``.

.. _osx:

Mac OS X
--------

Mac OS X uses :ref:`UTF-8` for the filenames. If a filename is an invalid UTF-8
byte string, Mac OS raises an error. The filenames are :ref:`decomposed
<normalization>`) using an (incompatible) variant of the Normal Form D,
`Technical Q&A QA1173
<http://developer.apple.com/mac/library/qa/qa2001/qa1173.html>`_: "For example,
HFS Plus uses a variant of Normal Form D in which U+2000 through U+2FFF, U+F900
through U+FAFF, and U+2F800 through U+2FAFF are not decomposed."

.. todo:: Document %3A pattern for undecodable filename


.. _locales:

Locales
-------

To support different languages and encodings, UNIX and BSD operating systems
have "locales". Locales are process-wide: if a thread or a library change
the locale, the whole process is impacted.


.. _locale categories:

Locale categories
'''''''''''''''''

Locale categories:

 * :c:macro:`LC_COLLATE`: compare and sort strings
 * :c:macro:`LC_CTYPE`: encode and decode characters, "C" locale usually means 7 bits
   :ref:`ASCII` (not always, see below)
 * :c:macro:`LC_MESSAGES`: language of messages (gettext), "C" locale means English
 * :c:macro:`LC_MONETARY`: monetary formatting
 * :c:macro:`LC_NUMERIC`: number formatting (e.g. thousands separator)
 * :c:macro:`LC_TIME`: time and date formatting

:c:macro:`LC_ALL` is a special category: if you set a locale using this category, it sets
the locale for all categories.

Each category has its own environment variable with the same name. For example,
``LC_MESSAGES=C`` displays error messages in English. To get the value of a locale
category, ``LC_ALL``, ``LC_xxx`` (e.g. ``LC_CTYPE``) or ``LANG`` environment variables are
checked: use the first non empty variable. If all variables are unset,
fallback to the C locale.

The "C" locale is a special locale. It is also known as "POSIX". It is used if
``LC_ALL``, ``LC_xxx`` and ``LANG`` environment variables are not set. As English is used
as the default language, use C locale means that programs speak English.

.. note::

   The gettext library reads ``LANGUAGE``, ``LC_ALL`` and ``LANG`` environment
   variables (and some others) to get the user language. The ``LANGUAGE``
   variable is specific to gettext and is not related to locales.


.. _locale encoding:

Locale encoding
'''''''''''''''

For Unicode, the most important locale category is ``LC_CTYPE``: it is used to set
the "locale encoding".

To get the locale encoding:

 * Get a copy of the current locale with ``setlocale(LC_CTYPE, NULL)``
 * Set the current locale encoding: ``setlocale(LC_CTYPE, "")``
 * Use ``nl_langinfo(CODESET)`` if available
 * or ``setlocale(LC_CTYPE, "")``

.. todo:: write a full example in C

For the C locale, ``nl_langinfo(CODESET)`` returns :ref:`ASCII`, or an alias to
this encoding (e.g. "US-ASCII" or "646"). But on FreeBSD, Solaris and :ref:`Mac
OS X <osx>`, codec functions (e.g. :c:func:`mbstowcs`) use :ref:`ISO-8859-1`
even if ``nl_langinfo(CODESET)`` announces ASCII encoding. AIX uses
:ref:`ISO-8859-1` for the C locale (and ``nl_langinfo(CODESET)`` returns
``"ISO8859-1"``).


Locale functions
''''''''''''''''

``<locale.h>`` functions.

.. c:function:: char* setlocale(category, NULL)

   Get the current locale of the specified category.

.. c:function:: char* setlocale(category, name)

   Set the locale of the specified category.

``<langinfo.h>`` functions.

.. c:function::  char* nl_langinfo(CODESET)

   Get the name of the locale encoding.

``<stdlib.h>`` functions.

.. c:function:: size_t mbstowcs(wchar_t *dest, const char *src, size_t n)

   Decode a :ref:`byte string <bytes>` from the :ref:`locale encoding <locale
   encoding>` to a :ref:`character string <str>`. Return an :ref:`error
   <strict>` on :ref:`undecodable byte sequence <undecodable>`. If available,
   always prefer the reentrant version: :c:func:`mbsrtowcs`.

.. c:function:: size_t wcstombs(char *dest, const wchar_t *src, size_t n)

   Encode a :ref:`character string <str>` to a :ref:`byte string <bytes>` in
   the :ref:`locale encoding <locale encoding>`. Return an :ref:`error
   <strict>` if :ref:`a character cannot by encoded <unencodable>`.  If
   available, always prefer the reentrant version: :c:func:`wcsrtombs`.

mbstowcs() and wcstombs() are :ref:`strict <strict>` and don't support
:ref:`error handlers <errors>`.

.. note::

   "mbs" stands for "multibyte string" (byte string) and "wcs" stands for "wide
   character string".

On Windows, the "locale encoding" are the :ref:`ANSI and OEM code pages
<codepage>`.


Filesystems (filenames)
-----------------------

CD-ROM and DVD
''''''''''''''

CD-ROM uses ISO 9660 filesystem which doesn't support Unicode filenames. This
filesystem is very restrictive: only A-Z, 0-9, _ and "." are allowed. Microsoft
has developped has extension to the ISO 9660 filesystem: Joliet. This extension
stores filenames as Unicode, up to 64 characters (BMP only, stored as
:ref:`UCS-2 <ucs>`). It was first supported by Windows 95, Today, all
operationg systems are able to read it.

UDF (Universal Disk Format) is the filesystem of DVD: it stores filenames as
Unicode.


Microsoft
'''''''''

On MS-DOS, filenames are :ref:`byte strings <bytes>`, were displayed
differently depending on the :ref:`code page <codepage>` and were limited to
8+3 caracters (8 characters for the name, 3 for the filename extension).
Microsoft extended its FAT filesystem in Windows 95 to add "long filenames":
filenames up to 255 :ref:`UCS-2 <ucs>` characters. Starting at Windows 2000,
non-BMP can be used: filenames are now 255 :ref:`UTF-16 <utf16>` characters.

The NTFS filesystem stores also filenames at Unicode.

Apple
'''''

HFS uses bytes filenames.

HFS+ uses UTF-16 for filenames: the maximum length is 255 UTF-16 characters.


Others
''''''

JFS and ZFS also use Unicode.

The ext family (ext2, ext3, ext4) use bytes.

.. todo:: Network fileystems like NFS (NFS4 supports Unicode?)

