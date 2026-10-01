# -*- coding: utf-8 -*-
import re, io, sys, subprocess, os
from datetime import date, timedelta
os.chdir(os.path.dirname(os.path.abspath(__file__)))
out = io.StringIO()
src = open('index.html', encoding='utf-8').read()
out.write(f'len={len(src)}  div_open={src.count("<div")} div_close={src.count("</div>")}\n')
out.write(f'U+FFFD={src.count(chr(0xFFFD))}  stray</div>>={src.count("</div>>")}\n')
for pat in ['<!-- daily-update:','数据区间','content-fingerprint','name="viewport"']:
    m = re.search(pat + r'[^>]{0,120}', src)
    out.write(f'{pat} -> {m.group(0)[:140] if m else "NOT FOUND"}\n')
# sections
for m in re.finditer(r'<!--\s*(Section[^>]*?)-->', src):
    out.write(f'SEC {m.start()}: {m.group(1).strip()}\n')
# date tags per section boundaries
secs = [(m.start(), m.group(1).strip()) for m in re.finditer(r'<!--\s*(Section[^>]*?)-->', src)]
for i,(pos,name) in enumerate(secs):
    end = secs[i+1][0] if i+1 < len(secs) else len(src)
    seg = src[pos:end]
    tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', seg)
    cards = re.findall(r'<div class="card-title[^>]*>(.*?)</div>', seg, re.S)
    cards = [re.sub(r'<[^>]+>','',c).strip()[:44] for c in cards]
    out.write(f'\n== {name} == date_tags={tags}\n')
    for c in cards:
        out.write('   - '+c+'\n')
open('_inspect_1001.txt','w',encoding='utf-8').write(out.getvalue())
print(out.getvalue())
