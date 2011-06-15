from ctypes import *

CP_UTF7 = 65000
CP_UTF8 = 65001
CODE_PAGES = {
    CP_UTF7: 'CP_UTF7',
    CP_UTF8: 'CP_UTF8',
}

MB_ERR_INVALID_CHARS = 8
MB_FLAGS = {
  'MB_ERR_INVALID_CHARS': MB_ERR_INVALID_CHARS,
}

WC_ERR_INVALID_CHARS = 0x0080
WC_NO_BEST_FIT_CHARS = 0x0400

WC_FLAGS = {
    'WC_ERR_INVALID_CHARS': WC_ERR_INVALID_CHARS,
    'WC_NO_BEST_FIT_CHARS': WC_NO_BEST_FIT_CHARS,
}

_decode = windll.kernel32.MultiByteToWideChar
_decode.argtypes = (c_uint, c_uint, c_char_p, c_int, c_wchar_p, c_int)
_decode.restype = c_int

_encode = windll.kernel32.WideCharToMultiByte
_encode.argtypes = (c_uint, c_uint, c_wchar_p, c_int, c_char_p, c_int, c_void_p, c_void_p)
_encode.restype = c_int

def format_flags(flags, names):
    text = []
    for name, value in names.iteritems():
        if flags & value:
            text.append(name)
            flags &= ~value
    if flags:
        text.append(str(flags))
    if text:
        return '|'.join(text)
    else:
        return '0'

def format_cp(cp):
    try:
        return CODE_PAGES[cp]
    except KeyError:
        return "'cp%s'" % cp

def decode(cp, raw, flags=0):
    buflen = len(raw)
    buf = create_unicode_buffer(buflen)
    ret = _decode(cp, flags, raw, len(raw), buf, buflen)
    if ret == 0:
        return '*error*'
    return buf[:ret]

def test_decode(cp, raw, flags=0):
    flags_text = format_flags(flags, MB_FLAGS)
    text = decode(cp, raw, flags)
    print("%r.decode(%s, flags=%s) = %r"
          % (raw, format_cp(cp), format_flags(flags, MB_FLAGS), text))

def encode(cp, text, flags=0):
    buflen = len(text) * 10
    buf = create_string_buffer(buflen)
    ret = _encode(cp, flags, text, len(text), buf, buflen, None, None)
    if ret == 0:
        return '*error*'
    return buf[:ret]

def test_encode(cp, text, flags=0):
    raw = encode(cp, text, flags)
    print("%r.encode(%s, flags=%s) = %r"
          % (text, format_cp(cp), format_flags(flags, WC_FLAGS), raw))

for flags in (0, MB_ERR_INVALID_CHARS):
    test_decode(1252, b'\xE9\x80', flags)
    test_decode(CP_UTF8, b'\xC3\xA9', flags)
    test_decode(932, b'\x81\x00', flags)
    test_decode(932, b'\xFF', flags)
    test_decode(CP_UTF8, b'\xff', flags)
    test_decode(CP_UTF8, b'\xED\xB2\x80', flags)
print
for flags in (0, WC_NO_BEST_FIT_CHARS, WC_ERR_INVALID_CHARS):
    test_encode(932, u'\xFF', flags)
    test_encode(1252, u'\u0141', flags)
    test_encode(1252, u'\u20AC', flags)
    test_encode(CP_UTF8, u'\uDC80', flags)

