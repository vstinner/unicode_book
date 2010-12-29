#!/usr/bin/env python
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

BOMS = (
    (BOM_UTF8, "UTF-8 (BOM)"),
    (BOM_UTF32_BE, "UTF-32-BE (BOM)"),
    (BOM_UTF32_LE, "UTF-32-LE (BOM)"),
    (BOM_UTF16_BE, "UTF-16-BE (BOM)"),
    (BOM_UTF16_LE, "UTF-16-LE (BOM)"),
)

def isASCII(data):
    try:
        data.decode('ASCII')
    except UnicodeDecodeError:
        return False
    else:
        return True

def isUTF8(data):
    try:
        decoded = data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
        for ch in decoded:
            if 0xD800 <= ord(ch) <= 0xDFFF:
                return False
        return True

def guess_encoding(data):
    encodings = []

    for bom, encoding in BOMS:
        if data.startswith(bom):
            encodings.append(encoding)

    if isASCII(data):
        encodings.append("ASCII")

    if isUTF8(data):
        encodings.append("UTF-8")

    return encodings

if __name__ == "__main__":
    def GUESS_ENCODING(data):
        encodings = guess_encoding(data)
        if encodings:
            encodings = ", ".join(encodings)
        else:
            encodings = "<unknown>"
        print("guess_encoding(%r): %s" % (data, encodings))

    GUESS_ENCODING("ascii");

    GUESS_ENCODING("\xC3\xA9")         # UTF-8: U+00E9 (2 bytes)
    GUESS_ENCODING("\xE2\x82\xAC")     # UTF-8: U+20AC
    GUESS_ENCODING("\xF4\x8F\xBF\xBF") # UTF-8: U+10FFFF (4 bytes)
    GUESS_ENCODING("\xC0\x80")         # Invalid UTF-8: too long
    GUESS_ENCODING("\xED\xB2\x80")     # Invalid UTF-8: surrogate

    # U+00E9, U+20AC
    GUESS_ENCODING("\xEF\xBB\xBF\xC3\xA9\xE2\x82\xAC");
    GUESS_ENCODING("\xFF\xFE\xE9\x00\xAC\x20");
    GUESS_ENCODING("\xFE\xFF\x00\xE9\x20\xAC");
    GUESS_ENCODING("\xFF\xFE\x00\x00\xE9\x00\x00\x00\xAC\x20\x00\x00");
    GUESS_ENCODING("\x00\x00\xFE\xFF\x00\x00\x00\xE9\x00\x00\x20\xAC");

