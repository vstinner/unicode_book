#include <stdio.h>
#include <assert.h>
#include <stdint.h>

void
encode_utf16_pair(uint32_t code_point,
                  uint16_t *words)
{
    unsigned int ordinal;
    assert(code_point >= 0x10000);
    ordinal = (code_point - 0x10000);
    words[0] = 0xD800 | (ordinal >> 10);
    words[1] = 0xDC00 | (ordinal & 0x3FF);
}

uint32_t
decode_utf16_pair(uint16_t *words)
{
    uint32_t code;
    assert(0xD800 <= words[0] && words[0] <= 0xDBFF);
    assert(0xDC00 <= words[1] && words[1] <= 0xDFFF);
    code = 0x10000;
    code += (words[0] & 0x03FF) << 10;
    code += (words[1] & 0x03FF);
    return code;
}

int main()
{
    uint16_t words[2];
    uint32_t c;

    c = 0x10abcdU;
    encode_utf16_pair(c, words);
    printf("0x%04x 0x%04x\n", words[0], words[1]);

    c = decode_utf16_pair(words);
    printf("c = U+%06x\n", c);

    return 0;
}
