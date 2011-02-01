from sys import stdout

ASCII = False

NAMES = {
    0: 'NUL',
    7: 'BEL',
    9: 'TAB',
    10: 'LF',
    13: 'CR',
    27: 'ESC',
    127: 'DEL',
}

HEADER_WIDTH = 4
WIDTH = 5
LINE = ("+" + "-" * HEADER_WIDTH + ("+" + "-" * WIDTH) * 16 + "+\n")

stdout.write(LINE)
stdout.write("|" + " " * HEADER_WIDTH)
for ligne in xrange(16):
    stdout.write("|  -%x " % ligne)
stdout.write("|\n")
stdout.write(LINE)

if ASCII:
    LIGNES = xrange(8)
else:
    LIGNES = xrange(16)

for ligne in LIGNES:
    text = "%x-" % ligne
    stdout.write("| %s " % text)
    for colonne in xrange(16):
        ch = unichr(ligne*16 + colonne)
        if ord(ch) in NAMES:
            ch = NAMES[ord(ch)]
        elif ord(ch) < 32 or ord(ch) in (127, 0xAd) or (0x80 <= ord(ch) <= 0x9F):
            ch = '---'
        elif ch in '*+-`|':
            ch = '\\' + ch
        stdout.write("| %s " % ch.center(3).encode('utf-8'))
    stdout.write("|\n")
    stdout.write(LINE)

