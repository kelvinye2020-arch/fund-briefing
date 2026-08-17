#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
with open('index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()
items = re.findall(r'<div class="timeline-item">', content)
print(f'S7 timeline items: {len(items)}')
dates = re.findall(r'<div class="timeline-date">(.*?)</div>', content)
for d in dates:
    if '06-09' in d:
        print(f'  Found 06-09: {d.strip()}')
print('Done')
