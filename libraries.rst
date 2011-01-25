Libraries
=========

.. _qt:


Qt library
----------

Qt is a big :ref:`C++` library covering different topics, but it is typically used
to create graphical interfaces. It is distributed under the `GNU LGPL license`_
(version 2.1), but it is also available under a commercial license.

Character and string
''''''''''''''''''''

``QString`` is a character string: each character is stored as a ``QChar``.
Interesting ``QString`` methods:

 * ``toAscii()``, ``fromAscii()``: encode to/decode from :ref:`ASCII`
 * ``toLatin1()``, ``fromLatin1()``: encode to/decode from :ref:`ISO-8859-1`
 * ``utf16()``, ``fromUtf16()``: encode to/decode to :ref:`UTF-16 <utf16>`
 * ``normalized()``: normalize to NFC, NFD, NFKC or NFKD (see :ref:`Normalization`)

Qt decodes string literals using the QLatin1String class. It is a thin wrapper
to const char* strings. QLatin1String stores a character as a single byte. It
is possible because it only supports characters in range U+0000—U+00FF.
QLatin1String are smaller than ``QString`` because they cannot be used to
manipulate text, eg. it is not possible to concatenate two QLatin1String
strings.

``QChar`` is a 16 bits Unicode character. Interesting ``QChar`` methods:

 * ``isSpace()``: True if the character category is separator
 * ``toUpper()``: convert to upper case

Codec
'''''

``QTextCodec.codecForLocale()`` gets the locale codec. The locale codec is:

 * Windows: :ref:`ANSI code page <Code pages>`
 * The locale encoding otherwise: try ``nl_langinfo(CODESET)``, or ``LC_ALL``,
   ``LC_CTYPE``, ``LANG`` environment variables. If no one gives any useful information,
   fallback to :ref:`ISO-8859-1`.


Filesystem
''''''''''

``QFile.encodeName()``:

 * Windows: encode to :ref:`UTF-16 <utf16>`
 * Mac OS X: normalize the name to the D form and then encode to :ref:`UTF-8`
 * Other (UNIX/BSD): encode to the local encoding (``QTextCodec.codecForLocale()``)

``QFile.decodeName()`` is the reverse operation.

Qt has two implementations of its ``QFSFileEngine``:

 * Windows: use Windows native API
 * Unix: use POSIX API. Examples: ``fopen()``, ``getcwd()`` or ``get_current_dir_name()``,
   ``mkdir()``, etc.

Classes: ``QFile``, ``QFileInfo``, ``QAbstractFileEngineHandler``, ``QFSFileEngine``.

.. _glib:

glib library
------------

:ref:`Gtk+` is a :ref:`C <c>` toolkit to create graphic interfaces, based on the glib library.
Both projects are distributed under the `GNU LGPL license`_ (version 2.1). The
glib library uses the :ref:`UTF-8` encoding as internal encoding to store character
strings using :c:type:`gchar*` :ref:`C <c>` type. There is also :c:type:`gunichar` C type to store a
single code point able to store any Unicode 6.0 character (U+0000—U+10FFFF).

Functions:

 * :c:func:`g_get_charset`: chraset of the current locale

   * Windows: :ref:`ANSI code page <Code pages>` (CPxxxx)
   * OS/2: read the code page from :c:func:`DosQueryCp`
   * other: try ``nl_langinfo(CODESET)``, or ``LC_ALL``, ``LC_CTYPE`` or ``LANG`` environment
     variables

 * :c:func:`g_get_filename_charsets`: list of charsets
 * :c:func:`g_filename_display_name`
 * ``G_FILENAME_ENCODING`` environment variable
 * :c:func:`g_utf8_get_char`: get the first character of an UTF-8 string as
   :c:type:`gunichar`
 * :c:func:`g_convert`: decode from an encoding and encode to another encoding. Use
   :c:func:`g_convert_with_fallback` to choose how to replace unencodable characters.
 * :c:func:`g_filename_from_utf8` / :c:func:`g_filename_to_utf8`: encode to/decode from a
   filename.
 * :c:func:`g_locale_from_utf8` / :c:func:`g_locale_to_utf8`: encode to/decode from the locale
   encoding.
 * :c:func:`g_convert`: Converts a string from one character set to another (use iconv library)

.. _Gtk+: http://www.gtk.org/


.. _icu:

ICU library
-----------

`International Components for Unicode` (ICU) is a mature, widely used set of
:ref:`C <c>`/:ref:`C++ <cpp>` and :ref:`Java <java>` libraries providing
Unicode and Globalization support for software applications. ICU is a open
source library distributed under the `MIT license`_.

.. todo:: complete this section

.. _International Components for Unicode: http://site.icu-project.org/
.. _GNU LGPL license: http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License

