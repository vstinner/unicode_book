.. index:: BMP, Unicode
.. _bmp:
.. _unicode charset:

Unicode
=======

Unicode is a character set. It is a superset of all the other character sets.
In the version 6.0, Unicode has 1,114,112 code points (the last code point is
U+10FFFF). Unicode 1.0 was limited to 65,536 code points (the last code point
was U+FFFF), the range U+0000—U+FFFF called **BMP** (*Basic Multilingual
Plane*). I call the range U+10000—U+10FFFF as **non-BMP** characters.

.. todo:: examples of applications only supporting BMP characters?


.. _unicode categories:

Categories
----------

Unicode 6.0 has 7 character categories, and each category has subcategories:

 * Letter (L): lowercase (Ll), modifier (Lm), titlecase (Lt), uppercase (Lu),
   other (Lo)
 * Mark (M): spacing combining (Mc), enclosing (Me), non-spacing (Mn)
 * Number (N): decimal digit (Nd), letter (Nl), other (No)
 * Punctuation (P): connector (Pc), dash (Pd), initial quote (Pi), final quote
   (Pf), open (Ps), close (Pe), other (Po)
 * Symbol (S): currency (Sc), modifier (Sk), math (Sm), other (So)
 * Separator (Z): line (Zl),  paragraph (Zp), space (Zs)
 * Other (C): control (Cc), format (Cf), not assigned (Cn), private use (Co),
   :ref:`surrogate <surrogates>` (Cs)

.. TODO:: NELLE - exemples ? Il y a beaucoup de catégories/sous catégories que
  je ne comprends pas

There are 3 ranges reserved for private use (Co subcategory): U+E000—U+F8FF (6,400 code
points), U+F0000—U+FFFFD (65,534) and U+100000—U+10FFFD (65,534). Surrogates (Cs subcategory)
use the range U+D800—U+DFFF (2,048 code points).


.. _unicode stats:

Statistics
----------

On a total of 1,114,112 possible code points, only 248,966 code points are
assigned: 77.6% are not assigned. Statistics excluding not assigned (Cn),
private use (Co) and :ref:`surrogate <surrogates>` (Cs) subcategories:

 * Letter: 100,520 (91.8%)
 * Symbol: 5,508 (5.0%)
 * Mark: 1,498 (1.4%)
 * Number: 1,100 (1.0%)
 * Punctuation: 598 (0.5%)
 * Other: 205 (0.2%)
 * Separator: 20 (0.0%)

.. TODO:: NELLE - Je pense que ça vaut le coup de faire un graphique pour les
  stats. C'est un peu chiant à faire, mais ça change la vie du lecteur !

On a total of 106,028 letters and symbols, 101,482 are in "other"
subcategories (Lo and So): only 4.3% have well defined subcategories:

 * Letter, lowercase (Ll): 1,759
 * Letter, uppercase (Lu): 1,436
 * Symbol, math (Sm): 948
 * Letter, modifier (Lm): 210
 * Symbol, modifier (Sk): 115
 * Letter, titlecase (Lt): 31
 * Symbol, currency (Sc): 47


.. index:: NFC, NFD, NFKC, NFKD
.. _Normalization:

Normalization
-------------

Unicode standard explains how to decompose a character. For example, the precomposed
character ç (U+00C7, Latin capital letter C with cedilla) can be written as
the sequence of two characters: {¸ (U+0327, Combining cedilla), c (U+0043, Latin capital letter C)}.
This decomposition can be useful to search a substring in a
text, e.g. remove diacritic is pratical for the user. The decomposed form is
called Normal Form D (**NFD**) and the precomposed form is called Normal Form
C (**NFC**).

+------+--------+------------------+
| Form | String | Unicode          |
+======+========+==================+
| NFC  | ç      | U+00C7           |
+------+--------+------------------+
| NFD  | ¸c     | {U+0327, U+0043} |
+------+--------+------------------+

Unicode database contains also a compatibility layer: if a character cannot be
rendered (no font contain the requested character) or encoded to a specific
encoding, Unicode proposes a :ref:`replacment character sequence which looks
like the character <translit>`, but may have a different meaning.

.. TODO:: NELLE - typo "replacment"

For example, ĳ (U+0133, Latin small ligature ij) is replaced by the two
characters {i (U+0069, Latin small letter I), j (U+006A, Latin small letter
J)}. ĳ character :ref:`cannot be encoded <unencodable>` to :ref:`ISO-8859-1`,
whereas ij characters can.

Two extra normal forms use this compatibility layer: **NFKD**
(decomposed) and **NFKC** (precomposed).

.. note::

   The precomposed forms (NFC and NFKC) begin by a canonical decomposition
   before recomposing pre-combined characters again.

.. todo:: CJK and Han issues
.. todo:: is printable?
.. todo:: lower/upper case
.. todo:: character properties: name, category, number, RTL

