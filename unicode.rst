.. index:: Unicode

Unicode
=======

What is Unicode?
----------------

Basic Multilingual Plane (BMP), or "Plane 0": range U+0000—U+FFFF. non-BMP
range: U+10000—U+10FFFF.

UTF codec family: :ref:`UTF-8`, :ref:`UTF-16-LE` and :ref:`UTF-16-BE`, :ref:`UTF-32-LE` and
:ref:`UTF-32-BE`. There are some extra UTF encodings like UTF-7 and UTF-EBCDIC.

.. todo:: Explains how to display characters (left-to-right, right-to-left)

Categories
----------

Unicode has 7 character categories. Categories with examples and character
count of Unicode 6.0:

 * Letter (L)

   * lowercase (Ll): U+0264 (ɤ), U+0441 (с), U+1D07 (ᴇ),
     U+1D5FF (𝗿), U+1D68A (𝚊), … (1,759)
   * modifier (Lm): U+1D2D (ᴭ), U+1D44 (ᵄ), U+1D9B (ᶛ),
     U+1DB0 (ᶰ), … (210)
   * titlecase (Lt): U+01C5 (ǅ), U+1F8C (ᾌ), U+1F8F (ᾏ),
     U+1F9C (ᾜ), U+1FAB (ᾫ), … (31)
   * uppercase (Lu): U+0051 (Q), U+1F1A (Ἒ), U+1D469 (𝑩),
     U+1D4AB (𝒫), U+1D57B (𝕻), … (1,436)
   * other (Lo): U+8E96 (躖), U+B585 (떅), U+B92E (뤮), … (97,084)

 * Mark (M)

   * spacing combining (Mc): U+09C0 (ী), U+0B4C (ୌ), U+0DDE (ෞ),
     … (287)
   * enclosing (Me): U+20DD (⃝), U+20E0 (⃠), U+20E4 (⃤), … (12)
   * non-spacing (Mn): U+0357, U+0B3C, U+1A5E, U+1D180, U+E017D,
     … (1,199)

 * Number (N)

   * decimal digit (Nd): U+0666 (٦), U+0AEA (૪), … (420)
   * letter (Nl): U+216E (Ⅾ), U+2171 (ⅱ), … (224)
   * other (No): U+2490 (⒐), U+325E (㉞), U+32B9 (㊹), … (456)

 * Punctuation (P)

   * connector (Pc): U+2040 (⁀), U+2054 (⁔), U+FE34 (︴), U+FE4D (﹍),
     U+FF3F (＿), … (10)
   * dash (Pd): U+2010 (‐), U+2011 (‑), U+FE63 (﹣), … (21)
   * initial quote (Pi): U+2018 (‘), U+201B (‛), … (12)
   * final quote (Pf): U+00BB (»), U+2019 (’), U+203A (›), … (10)
   * open (Ps): U+27E8 (⟨), U+2993 (⦓), U+2995 (⦕), U+301D (〝),
     U+FE41 (﹁), … (72)
   * close (Pe): U+276F (❯), U+300B (》), U+FE36 (︶), U+FE5C (﹜),
     U+FF5D (｝), … (71)
   * other (Po): U+0F06 (༆), U+2047 (⁇), U+FF3C (＼), … (402)

 * Symbol (S)

   * currency (Sc): U+0AF1 (૱), U+20A6 (₦), U+20B3 (₳), U+20B4 (₴),
     … (47)
   * modifier (Sk): U+00AF (¯), U+02D4 (˔), U+02E9 (˩), U+02F7 (˷),
     U+A70D (꜍), … (115)
   * math (Sm): U+2211 (∑), U+27D1 (⟑), U+293F (⤿), U+2AF0 (⫰),
     U+2AF4 (⫴), … (948)
   * other (So): U+0FC4 (࿄), U+2542 (╂), … (4398)

 * Separator (Z: 20)

   * line (Zl): U+2028
   * paragraph (Zp): U+2029
   * space (Zs): U+00A0, U+2003, U+2004, U+2007, U+2009, … (18)

 * Other (C)

   * control (Cc): U+0007, U+000A, U+0090, U+009E, … (65)
   * format (Cf): U+200B, U+2062, U+E0043, U+E004A, U+E0063, … (140)
   * not assigned (Cn): U+4D67A, U+51797, U+A63FB, U+D0F5B, U+D9791,
     … (865,146)
   * private use (Co): U+E000—U+F8FF (6400), U+F0000—U+FFFFD (65534),
     U+100000—U+10FFFD (65534); total = 137,468
   * surrogate (Cs): U+D800—U+DFFF (2048)

Statistics
----------

77.6% of all codes are not assigned. Statistics excluding not assigned (Cn),
private use (Co) and surrogate (Cs) categories:

 * Letter: 100,520 (91.8%)
 * Symbol: 5,508 (5.0%)
 * Mark: 1,498 (1.4%)
 * Number: 1,100 (1.0%)
 * Punctuation: 598 (0.5%)
 * Other: 205 (0.2%)
 * Separator: 20 (0.0%)

.. _Normalization:

Normalization
-------------

Unicode standard explains how to decompose a character, eg. the precomposed
character ç (U+00C7, Latin capital letter C with cedilla) can be written as the
sequence ¸̧ (U+0327, Combining cedilla) c (U+0043, Latin capital letter C), two
characters. This decomposition can be useful to search a substring in a text,
eg. remove diacritic is pratical for the user. The decomposed form is called
Normal Form D (NFD) and the precomposed form is called Normal Form C (NFC).

+------+--------+----------------+
| Form | String | Unicode        |
+======+========+================+
| NFC  | ç      | U+00C7         |
+------+--------+----------------+
| NFD  | ,c     | U+0327, U+0043 |
+------+--------+----------------+

.. todo:: rst doesn't accept diacritics (U+0327) in a table cell: | NFD | ¸̧c | U+0327, U+0043 |

Unicode database contains also a compatibility layer: if a character cannot be
rendered (no font contain the requested character) or encoded to a specific
encoding, Unicode proposes a replacment character sequence which looks like the
character, but may have a different meaning. For example, ĳ (U+0133, Latin small
ligature ij) is replaced by i (U+0069, Latin small letter I) j (U+006A, Latin
small letter J), two characters. ĳ character cannot be encoded to :ref:`ISO-8859-1`,
whereas ij characters can. Two extra normal forms use this compatibility layer:
NFKD (decomposed) and NFKC (precomposed).

.. note::

   The precomposed forms (NFC and NFKC) begin by a canonical decomposition
   before recomposing pre-combined characters again.

