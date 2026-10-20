# -*- coding: utf-8 -*-
import re
P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
OUT = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/_dump_1020.txt'
s = open(P, encoding='utf-8').read()
marks = [(m.start(), m.group(0)) for m in re.finditer(r'<!-- =+ Section \d.*?-->', s, re.S)]
marks.append((len(s), 'EOF'))
buf = []
for i in range(len(marks) - 1):
    a, b = marks[i], marks[i+1]
    seg = s[a[0]:b[0]]
    buf.append('=' * 20 + ' ' + a[1].strip() + '\n')
    if a[1].find('Section 3') > 0 or a[1].find('Section 6') > 0 or a[1].find('Section 7') > 0:
        buf.append(seg[:7000])
    else:
        buf.append(seg)
open(OUT, 'w', encoding='utf-8').write('\n'.join(buf))
print('ok')
