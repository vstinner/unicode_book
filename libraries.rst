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

Gtk+ and glib libraries
-----------------------

`Gtk+ <http://www.gtk.org/>`_ is a :ref:`C <c>` toolkit to create graphic interfaces, based on the glib library.
Both projects are distributed under the `GNU LGPL license`_ (version 2.1). The
glib library uses the :ref:`UTF-8` encoding as internal encoding to store character
strings using :c:type:`gchar*` :ref:`C <c>` type. There is also :c:type:`gunichar` C type to store a
single code point able to store any Unicode 6.0 character (U+0000—U+10FFFF).

Codec functions:

 * :c:func:`g_convert`: decode from an encoding and encode to another encoding
   with the :ref:`iconv library <iconv>`. Use :c:func:`g_convert_with_fallback`
   to choose how to handle :ref:`undecodable bytes <undecodable>` and
   :ref:`unencodable characters <unencodable>`.
 * :c:func:`g_locale_from_utf8` / :c:func:`g_locale_to_utf8`: encode to/decode from the locale
   encoding.
 * :c:func:`g_get_charset`: get the charset of the :ref:`current locale <locale
   encoding>`

   * Windows: current :ref:`ANSI code page <codepage>`
   * OS/2: current code page (call :c:func:`DosQueryCp`)
   * other: try ``nl_langinfo(CODESET)``, or ``LC_ALL``, ``LC_CTYPE`` or ``LANG`` environment
     variables

 * :c:func:`g_utf8_get_char`: get the first character of an UTF-8 string as
   :c:type:`gunichar`

Filename functions:

 * :c:func:`g_filename_from_utf8` / :c:func:`g_filename_to_utf8`: encode/decode
   a filename
 * :c:func:`g_filename_display_name`: human readable version of a filename. Try
   to decode the filename from each encoding of
   :c:func:`g_get_filename_charsets` encoding list. If all decoding failed,
   decode the filename from UTF-8 and escape :ref:`undecodable bytes
   <undecodable>`.
 * :c:func:`g_get_filename_charsets`: get the list of charsets used to decode
   and encode filenames. :c:func:`g_filename_display_name` tries each encoding
   of this list, other functions just use the first encoding. Use UTF-8 on
   Windows. On other operating systems, use:

   * ``G_FILENAME_ENCODING`` environment variable (if set): comma-separated
     list of character set names, the special token ``"@locale"`` is taken to mean
     the :ref:`locale encoding <locale encoding>`
   * or UTF-8 if ``G_BROKEN_FILENAMES`` environment variable is set
   * or call :c:func:`g_get_charset` (:ref:`locale encoding <locale encoding>`)


.. _icu:

ICU library
-----------

`International Components for Unicode` (ICU) is a mature, widely used set of
:ref:`C <c>`/:ref:`C++ <cpp>` and :ref:`Java <java>` libraries providing
Unicode and Globalization support for software applications. ICU is a open
source library distributed under the `MIT license`_.

.. _International Components for Unicode: http://site.icu-project.org/
.. _GNU LGPL license: http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License
.. _MIT license: http://en.wikipedia.org/wiki/MIT_License


.. _iconv:

iconv library
-------------

`libiconv <http://www.gnu.org/software/libiconv/>`_ is a library to encode and
decode text in different encodings. It is distributed under the `GNU LGPL
license`_. It supports a lot of encodings including rare and old encodings.

By default, libiconv is :ref:`strict <strict>`: an :ref:`unencodable character
<unencodable>` raise an error. You can :ref:`ignore <ignore>` these characters
by add ``//IGNORE`` suffix to the encoding. There is also the ``//TRANSLIT``
suffix to  :ref:`replace unencodable characters <replace>` by similarly looking
characters.

