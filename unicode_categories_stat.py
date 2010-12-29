import unicodedata
import sys
from collections import Counter
from pprint import pprint

t=Counter()
for x in range(0x10ffff):
 c = chr(x)
 cat = unicodedata.category(c)
 if cat[0] != 'L':
    continue
 key = cat
 t[key] += 1

N = sum(t.values())

for cat, count in t.items():
    print("%s: %s: %.1f%%" % (cat, count, count*100./N))
