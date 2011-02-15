Libraries
=========

.. _qt:


Qt library
----------

Qt is a big :ref:`C++` library covering different topics, but it is typically used
to create graphical interfaces. It is distributed under the `GNU LGPL license`_
(version 2.1), and is also available under a commercial license.

Character and string classes
''''''''''''''''''''''''''''

``QChar`` is a Unicode character, only able to store :ref:`BMP characters
<bmp>`. It is implemented using a 16 bits unsigned number. Interesting
``QChar`` methods:

 * ``isSpace()``: True if the :ref:`character category <unicode categories>` is
   separator (Zl, Zp or Zs)
 * ``toUpper()``: convert to upper case

``QString`` is a :ref:`UTF-16 <utf16>` :ref:`character string <str>`: it is a
string of ``QChar``. A :ref:`Non-BMP character <bmp>` are stored as a
:ref:`surrogate pairs <surrogates>`, as two ``QChar``. Interesting ``QString``
methods:

 * ``toAscii()``, ``fromAscii()``: encode to/decode from :ref:`ASCII`
 * ``toLatin1()``, ``fromLatin1()``: encode to/decode from :ref:`ISO-8859-1`
 * ``utf16()``, ``fromUtf16()``: encode to/decode to :ref:`UTF-16 <utf16>`
 * ``normalized()``: :ref:`normalize <normalization>` to NFC, NFD, NFKC or NFKD

Qt decodes literal strings using the QLatin1String class. It is a thin wrapper
to :c:type:`char*` :ref:`byte strings <bytes>`. QLatin1String stores a
character as a single byte.  It is possible because it only supports characters
in range U+0000—U+00FF. QLatin1String API is smaller than ``QString`` API,
because QLatin1String cannot be used to manipulate text. For example, it is not
possible to concatenate two QLatin1String strings.

Codec
'''''

``QTextCodec.codecForLocale()`` gets the locale codec. The locale codec is:

 * Windows: :ref:`ANSI code page <codepage>`
 * The :ref:`locale encoding <locale encoding>` otherwise: try
   ``nl_langinfo(CODESET)``, or ``LC_ALL``, ``LC_CTYPE``, ``LANG`` environment
   variables. If no one gives any useful information, fallback to
   :ref:`ISO-8859-1`.


Filesystem
''''''''''

``QFile.encodeName()``:

 * :ref:`Windows`: encode to :ref:`UTF-16 <utf16>`
 * :ref:`Mac OS X <os>`: :ref:`normalize <normalization>` to the D form and
   then encode to :ref:`UTF-8`
 * Other (UNIX/BSD): encode to the :ref:`local encoding <locale encoding>`
   (``QTextCodec.codecForLocale()``)

``QFile.decodeName()`` is the reverse operation.

Qt has two implementations of its ``QFSFileEngine``:

 * Windows: use Windows native API
 * Unix: use POSIX API. Examples: ``fopen()``, ``getcwd()`` or ``get_current_dir_name()``,
   ``mkdir()``, etc.

Classes: ``QFile``, ``QFileInfo``, ``QAbstractFileEngineHandler``, ``QFSFileEngine``.


.. _glib:

Gtk+ and glib libraries
-----------------------

`Gtk+ <http://www.gtk.org/>`_ is a :ref:`C <c>` toolkit to create graphic
interfaces. It is based on the glib library.  Both projects are distributed
under the `GNU LGPL license`_ (version 2.1).

Character strings
'''''''''''''''''

The :c:type:`gunichar` type is a character. It is able to store any Unicode 6.0
character (U+0000—U+10FFFF).

The glib library implements :ref:`character strings <str>` as :c:type:`gchar*`
:ref:`byte strings <bytes>` encoded to :ref:`UTF-8`.


Codec functions
'''''''''''''''

 * :c:func:`g_convert`: decode from an encoding and encode to another encoding
   with the :ref:`iconv library <iconv>`. Use :c:func:`g_convert_with_fallback`
   to choose how to :ref:`handle <errors>` :ref:`undecodable bytes
   <undecodable>` and :ref:`unencodable characters <unencodable>`.
 * :c:func:`g_locale_from_utf8` / :c:func:`g_locale_to_utf8`: encode to/decode
   from the :ref:`locale encoding <locale encoding>`.
 * :c:func:`g_get_charset`: get the charset of the current locale

   * Windows: current :ref:`ANSI code page <codepage>`
   * OS/2: current code page (call :c:func:`DosQueryCp`)
   * other: try ``nl_langinfo(CODESET)``, or ``LC_ALL``, ``LC_CTYPE`` or
     ``LANG`` environment variables

 * :c:func:`g_utf8_get_char`: get the first character of an UTF-8 string as
   :c:type:`gunichar`


Filename functions
''''''''''''''''''

 * :c:func:`g_filename_from_utf8` / :c:func:`g_filename_to_utf8`: encode/decode
   a filename
 * :c:func:`g_filename_display_name`: human readable version of a filename. Try
   to decode the filename from each encoding of
   :c:func:`g_get_filename_charsets` encoding list. If all decoding failed,
   decode the filename from :ref:`UTF-8` and :ref:`replace <replace>`
   :ref:`undecodable bytes <undecodable>` by � (U+FFFD).
 * :c:func:`g_get_filename_charsets`: get the list of charsets used to decode
   and encode filenames. :c:func:`g_filename_display_name` tries each encoding
   of this list, other functions just use the first encoding. Use :ref:`UTF-8`
   on :ref:`Windows`. On other operating systems, use:

   * ``G_FILENAME_ENCODING`` environment variable (if set): comma-separated
     list of character set names, the special token ``"@locale"`` is taken to mean
     the :ref:`locale encoding <locale encoding>`
   * or UTF-8 if ``G_BROKEN_FILENAMES`` environment variable is set
   * or call :c:func:`g_get_charset` (:ref:`locale encoding <locale encoding>`)


.. _iconv:

iconv library
-------------

`libiconv <http://www.gnu.org/software/libiconv/>`_ is a library to encode and
decode text in different encodings. It is distributed under the `GNU LGPL
license`_. It supports a lot of encodings including rare and old encodings.

By default, libiconv is :ref:`strict <strict>`: an :ref:`unencodable character
<unencodable>` raise an error. You can :ref:`ignore <ignore>` these characters
by add ``//IGNORE`` suffix to the encoding. There is also the ``//TRANSLIT``
suffix to  :ref:`replace unencodable characters <translit>` by similarly looking
characters.

:ref:`PHP <php>` has a builtin binding of iconv.


.. _icu:

ICU libraries
-------------

`International Components for Unicode <http://site.icu-project.org/>`_ (ICU) is
a mature, widely used set of :ref:`C <c>`/:ref:`C++ <cpp>` and :ref:`Java
<java>` libraries providing Unicode and Globalization support for software
applications. ICU is an open source library distributed under the `MIT
license`_.

.. _GNU LGPL license: http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License

