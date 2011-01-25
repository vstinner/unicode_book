Operating systems
=================

.. _Windows:

Windows
-------

.. index: Code page
.. _codepage:

Code pages
''''''''''

An application has two encodings, called code pages (abbreviated "cp"): the
ANSI code page (:c:macro:`CP_ACP`) used for the ANSI version of the Windows API to decode a byte
string to a character string, and the OEM code page (:c:macro:`CP_OEMCP`), eg. used for the console.
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
byte strings (function name ending with "A") and the :ref:`ANSI code page <Code pages>`, and the wide character version
(name ending with "W"). There are also functions without suffix using
:c:type:`TCHAR*` strings: if the :ref:`C <c>` define :c:macro:`_UNICODE` is defined, :c:type:`TCHAR` is
:c:type:`wchar_t` and it use the Unicode functions; otherwise :c:type:`TCHAR` is char
and it uses the ANSI functions. Example:

 * :c:func:`CreateFileA()`: bytes version, use byte strings encoded to the ANSI code page
 * :c:func:`CreateFileW()`: Unicode version, use wide character strings
 * :c:func:`CreateFile()`: :c:type:`TCHAR` version depending on the :c:macro:`_UNICODE` define


Encode and decode functions
'''''''''''''''''''''''''''

Encode and decode functions of ``<windows.h>``.

.. c:function:: MultiByteToWideChar()

   Decode a byte string to a character string (similar to
   :c:func:`mbstowcs`). It supports the :ref:`ANSI code page <Code pages>` and :ref:`OEM code page <Code pages>`, UTF-7 and :ref:`UTF-8`. By default,
   it ignores undecodable bytes. Use :c:macro:`MB_ERR_INVALID_CHARS` flag to raise an
   error on an invalid byte sequence.

.. c:function:: WideCharToMultiByte()

   Encode a character string to a byte string (similar to
   :c:func:`wcstombs`). As :c:func:`MultiByteToWideChar`, it supports :ref:`ANSI code page <Code pages>` and the :ref:`OEM code page <Code pages>`,
   UTF-7 and :ref:`UTF-8`. By default, if a character cannot be encoded, it is
   replaced by a character with a similar glyph. For example, with :ref:`cp1252`, Ł (U+0141) is replaced
   by L (U+004C). Use :c:macro:`WC_NO_BEST_FIT_CHARS` flag to raise an error on
   unencodable character.


Filenames
'''''''''

Windows stores filenames as Unicode in the filesystem. Filesystem wide
character POSIX-like API:

.. c:function:: int _wfstat(const wchar_t* filename, struct _stat *statbuf)

   Unicode version of :c:func:`stat()`.

.. c:function:: FILE *_wfopen(const wchar_t* filename, const wchar_t *mode)

   Unicode version of :c:func:`fopen`.

POSIX functions, like :c:func:`fopen()`, use the :ref:`ANSI code page <Code pages>` to encode/decode
strings.


Windows console
'''''''''''''''

Console functions.

.. c:function:: GetConsoleCP()

   Get the ccode page of the standard input (stdin) of the console.

.. c:function:: GetConsoleOutputCP()

   Get the code page of the standard output (stdout and stderr) of the console.

In a console (``cmd.exe``), ``chcp`` command can be used to display or to
change the :ref:`OEM code page <Code pages>` (and console code page). Change the console code page is not a
good idea because the ANSI API of the console still expect characters encoded
to the previous console code page.

If the console is unable to render a character, it tries to use a character
with a similar glyph: eg. Ł (U+0141) is replaced by L (U+0041). If no
replacment character can be found, "?" (U+003F) is displayed instead.

To improve the support of Unicode in a console:

 * Set the code page to cp65001 using the ``chcp`` command
 * Set the console font to "Lucida Console"
 * Use the Unicode version of the API

:c:func:`_setmode` and :c:func:`_wsopen` are special functions to set the encoding of a
file (especially of stdin, stdout and stderr):

 * :c:macro:`_O_U8TEXT`: :ref:`UTF-8` without :ref:`BOM <bom>`
 * :c:macro:`_O_U16TEXT`: :ref:`UTF-16 <utf16>` without BOM
 * :c:macro:`_O_WTEXT`: UTF-16 with BOM

See also `Conventional wisdom is retarded, aka What the @#%&* is _O_U16TEXT?`_
(Michael S. Kaplan, 2008).

.. _Conventional wisdom is retarded, aka What the @#%&* is _O_U16TEXT?:
   http://blogs.msdn.com/b/michkap/archive/2008/03/18/8306597.aspx


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

Mac OS X uses :ref:`UTF-8` for the filenames. If a filename is an invalid UTF-8 byte
string, Mac OS raises an error. The filenames are decomposed using an
(incompatible) variant of the Normal Form D: `Technical Q&A QA1173`_ (see
:ref:`Normalization`).

"For example, HFS Plus uses a variant of Normal Form D in which U+2000 through
U+2FFF, U+F900 through U+FAFF, and U+2F800 through U+2FAFF are not decomposed."

.. _Technical Q&A QA1173:
   http://developer.apple.com/mac/library/qa/qa2001/qa1173.html

.. todo:: Document %3A pattern for undecodable filename


.. _Locales:

Locales (UNIX and BSD)
----------------------

To support different languages and encodings, UNIX and BSD operating systems
have "locales". Locales are process-wide: if a thread or a library change
the locale, the whole process is impacted.


Locale categories
'''''''''''''''''

Locale categories:

 * :c:macro:`LC_COLLATE`: compare and sort strings
 * :c:macro:`LC_CTYPE`: encode and decode characters, "C" locale usually means 7 bits
   :ref:`ASCII` (not always, see below)
 * :c:macro:`LC_MESSAGES`: language of messages (gettext), "C" locale means English
 * :c:macro:`LC_MONETARY`: monetary formatting
 * :c:macro:`LC_NUMERIC`: number formatting (eg. thousands separator)
 * :c:macro:`LC_TIME`: time and date formatting

:c:macro:`LC_ALL` is a special category: if you set a locale using this category, it sets
the locale for all categories.

Each category has its own environment variable with the same name. For example,
``LC_MESSAGES=C`` displays error messages in English. To get the value of a locale
category, ``LC_ALL``, ``LC_xxx`` (eg. ``LC_CTYPE``) or ``LANG`` environment variables are
checked: use the first non empty variable. If all variables are unset,
fallback to the C locale.

The "C" locale is a special locale. It is also known as "POSIX". It is used if
``LC_ALL``, ``LC_xxx`` and ``LANG`` environment variables are not set. As English is used
as the default language, use C locale means that programs speak English.

.. _locale encoding:

Locale encoding
'''''''''''''''

For Unicode, the most important locale category is ``LC_CTYPE``: it is used to set
the "locale encoding".

For the C locale, ``nl_langinfo(CODESET)`` returns :ref:`ASCII`, or an alias to
this encoding (eg. "US-ASCII" or "646"). But on FreeBSD, Solaris and :ref:`Mac
OS X <osx>`, codec functions (eg. :c:func:`mbstowcs`) use :ref:`ISO-8859-1`
even if ``nl_langinfo(CODESET)`` announces ASCII encoding.

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

   Decode a byte string from the locale encoding to a character string.  Raise
   an error on undecodable byte sequence. If available, always prefer the
   reentrant version: :c:func:`mbsrtowcs`.

.. c:function:: size_t wcstombs(char *dest, const wchar_t *src, size_t n)

   Encode a character string to a byte string in the locale encoding. Raise an
   error if a character cannot by encoded. If available, always prefer the
   reentrant version: :c:func:`wcsrtombs`.

.. note::

   "mbs" means "multibyte string" (byte string) and "wcs" means "wide character
   string".

On Windows, the "locale encoding" are the :ref:`ANSI and OEM code pages
<codepage>`.

