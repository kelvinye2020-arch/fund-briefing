#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查S7时间线所有条目的日期"""
import re

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

s7_start = content.find('Section 7')
s7_end = content.find('Section 8')
s7 = content[s7_start:s7_end]

dates = re.findall(r'<div class="timeline-date">([^<]+)</div>', s7)
print(f'S7时间线条目数: {len(dates)}')
print()
for i, d in enumerate(dates):
    print(f'  {i+1}. {d}')
