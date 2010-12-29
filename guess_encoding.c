#include <stdio.h>    /* printf() */
#include <stdint.h>   /* uint32_t */
#include <string.h>   /* memcmp() */

static void
dump_byte_string(FILE *f,
                 const char *prefix,
                 const char *string,
                 size_t len,
                 const char *suffix)
{
    const char *end;
    unsigned c;
    fputs(prefix, f);
    end = string + len;
    for (; string != end; string++) {
        c = (unsigned char)*string;
        if (32 <= c && c <= 127)
            fputc((char)c, f);
        else
            fprintf(f, "\\x%02X", c);
    }
    fputs(suffix, f);
    fflush(f);
}

int
isASCII(const char *data, size_t size)
{
    const unsigned char *str = (unsigned char*)data;
    const unsigned char *end = str + size;
    for (; str != end; str++) {
        if (*str & 0x80)
            return 0;
    }
    return 1;
}

int
isUTF8(const char *data, size_t size)
{
    const unsigned char *str = (unsigned char*)data;
    unsigned int code_length, i;
    uint32_t ch;
    const unsigned char *end = str + size;
    while (str != end) {
        if (*str <= 0x7F) {
            /* 1 byte character (ASCII): U+0000..U+007F */
            str += 1;
            continue;
        }

        if (0xC2 <= *str && *str <= 0xDF)
            code_length = 2;
        else if (0xE0 <= *str && *str <= 0xEF)
            code_length = 3;
        else if (0xF0 <= *str && *str <= 0xF4)
            code_length = 4;
        else {
            /* invalid first byte of a multibyte character */
            return 0;
        }

        if (str + (code_length -1) >= end) {
            /* truncated string or invalid byte sequence */
            return 0;
        }

        /* Check continuation bytes: bit 7 should be set, bit 6 should unset */
        for (i=1; i < code_length; i++) {
            if ((str[i] & 0xc0) != 0x80)
                return 0;
        }

        if (code_length == 2) {
            ch = ((str[0] & 0x1f) << 6) + (str[1] & 0x3f);
            /* 2 bytes sequence: U+0080..U+07FF */
            if ((ch < 0x0080) || (0x07FF < ch))
                return 0;
        } else if (code_length == 3) {
            ch = ((str[0] & 0x0f) << 12) + ((str[1] & 0x3f) << 6) +
                  (str[2] & 0x3f);
            /* 3 bytes sequence: U+0800..U+FFFF */
            if ((ch < 0x0800) || (0xFFFF < ch))
                return 0;
            /* 3 bytes sequence: U+0800..U+FFFF... excluding U+D800..U+DFFF:
             * surrogates are invalid in UTF-8 */
            if ((0xD800 <= ch) && (ch <= 0xDFFF))
                return 0;
        } else if (code_length == 4) {
            ch = ((str[0] & 0x7) << 18) + ((str[1] & 0x3f) << 12) +
                 ((str[2] & 0x3f) << 6) + (str[3] & 0x3f);
            /* 4 bytes sequence: U+10000..U+10FFFF */
            if ((ch < 0x10000) || (0x10FFFF < ch))
                return 0;
        }
        str += code_length;
    }
    return 1;
}

const char UTF_8_BOM[] = "\xEF\xBB\xBF"; /* 3 bytes */
const char UTF_16_BE_BOM[] = "\xFE\xFF"; /* 2 bytes */
const char UTF_16_LE_BOM[] = "\xFF\xFE"; /* 2 bytes */
const char UTF_32_BE_BOM[] = "\x00\x00\xFE\xFF"; /* 4 bytes */
const char UTF_32_LE_BOM[] = "\xFF\xFE\x00\x00"; /* 4 bytes */

void guess_encoding(const char *data, size_t size)
{
#define FOUND(name) \
    do { \
        if (found) fputs(", ", stdout); \
        fputs(name, stdout); \
        found = 1; \
    } while (0)

    int found = 0;

    dump_byte_string(stdout, "guess_encoding(\"", data, size, "\"): ");

    if (size >= 3) {
        if (memcmp(data, UTF_8_BOM, 3) == 0)
            FOUND("UTF-8 (BOM)");
    }
    if (size >= 4) {
        if (memcmp(data, UTF_32_LE_BOM, 4) == 0)
            FOUND("UTF-32-LE (BOM)");
        if (memcmp(data, UTF_32_BE_BOM, 4) == 0)
            FOUND("UTF-32-BE (BOM)");
    }
    if (size >= 2) {
        if (memcmp(data, UTF_16_LE_BOM, 2) == 0)
            FOUND("UTF-16-LE (BOM)");
        if (memcmp(data, UTF_16_BE_BOM, 2) == 0)
            FOUND("UTF-16-BE (BOM)");
    }

    if (isASCII(data, size)) { FOUND("ASCII"); }

    if (isUTF8(data, size)) { FOUND("UTF-8"); }

    if (!found)
        printf("<unknown>");
    fputs("\n", stdout);

}

#define GUESS_ENCODING(data) guess_encoding(data, sizeof(data) - 1)

int main()
{
    char ascii[] = "ascii";
    char utf8_ecute[] = "\xC3\xA9"; /* U+00E9 */
    char utf8_euro[] = "\xE2\x82\xAC"; /* U+20AC */
    char utf8_10ffff[] = "\xF4\x8F\xBF\xBF"; /* U+10FFFF */
    char invalid_utf8[] = "\xC0\x80";
    char utf8_surrogate[] = "\xED\xB2\x80";
    /* U+00E9, U+20AC */
    char utf8_bom[] = "\xEF\xBB\xBF\xC3\xA9\xE2\x82\xAC";
    char utf16le_bom[] = "\xFF\xFE\xE9\x00\xAC\x20";
    char utf16be_bom[] = "\xFE\xFF\x00\xE9\x20\xAC";
    char utf32le_bom[] = "\xFF\xFE\x00\x00\xE9\x00\x00\x00\xAC\x20\x00\x00";
    char utf32be_bom[] = "\x00\x00\xFE\xFF\x00\x00\x00\xE9\x00\x00\x20\xAC";

    GUESS_ENCODING(ascii);

    GUESS_ENCODING(utf8_ecute);
    GUESS_ENCODING(utf8_euro);
    GUESS_ENCODING(utf8_10ffff);
    GUESS_ENCODING(invalid_utf8);
    GUESS_ENCODING(utf8_surrogate);

    GUESS_ENCODING(utf8_bom);
    GUESS_ENCODING(utf16le_bom);
    GUESS_ENCODING(utf16be_bom);
    GUESS_ENCODING(utf32le_bom);
    GUESS_ENCODING(utf32be_bom);

    return 0;
}
