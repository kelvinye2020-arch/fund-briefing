# -*- coding: utf-8 -*-
import re, io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = open(P, encoding='utf-8').read()
print('len', len(s))
print('U+FFFD', s.count('\ufffd'))
print('S8?', 'Section 8' in s, s.count('Section 8'))

# markers
for m in re.finditer(r'<!--\s*(daily-update|Section \d[^>]*?)\s*[:：]?[^>]*?-->', s):
    print('MARK:', m.group(0)[:90], '@', m.start())

print('--- section markers raw ---')
for m in re.finditer(r'<!--\s*=*\s*Section \d.*?-->', s, re.S):
    print(m.start(), m.group(0)[:100].replace('\n', ' '))

print('--- date tags ---')
tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s)
print(len(tags), tags)
print('--- td dates in S3 ---')
i3 = s.find('Section 3')
i4 = s.find('Section 4')
seg = s[i3:i4]
print(seg[:200].replace('\n',' '))
print(re.findall(r'<td>(\d{2}-\d{2})</td>', seg))
print('--- header badge ---')
m = re.search(r'数据区间：[^<（]*', s)
print(m.group(0) if m else None)
print('--- meta ---')
for k in ['content-fingerprint', 'description']:
    mm = re.search(r'<meta name="%s" content="([^"]*)">' % k, s)
    print(k, ':', mm.group(1) if mm else None)
print('--- counts ---')
for c in ['card p0', 'card p1', 'card p2', 'card p3', 'action-box', 'timeline-item', 'stat-card']:
    print(c, s.count('class="%s' % c))
print('div open', s.count('<div'), 'close', s.count('</div>'))
