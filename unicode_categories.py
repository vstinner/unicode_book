import unicodedata
import random
from collections import defaultdict

allchars = defaultdict(set)
for x in range(0x10ffff):
 c = chr(x)
 cat = unicodedata.bidirectional(c)
 allchars[cat].add(c)

allchars = list(allchars.items())
allchars.sort()

nexample = 5

for cat, chars in allchars:
    if nexample < len(chars):
        example = random.sample(chars, nexample)
    else:
        example = chars
    example = list(example)
    example.sort()
    text = '%s: ' % repr(cat)
    if True:
        text += ', '.join(
            "U+%04x" % (ord(c),)
            for c in example)
    else:
        text += ', '.join(
            "U+%04x (%s)" % (ord(c), c)
            for c in example)
    if len(example) != len(chars):
        text += ', ...'
    text += ' (%s)' % len(chars)
    print(text)

