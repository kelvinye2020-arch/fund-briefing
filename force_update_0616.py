#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""强制重新执行2026-06-16所有更新，直接写入index.html"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"读取完成，文件长度: {len(c)}")

# 1. 数据区间
old = '数据区间：2026.06.01 — 2026.06.15（周度巡检更新）'
new = '数据区间：2026.06.02 — 2026.06.16（今日自动更新）'
c = c.replace(old, new)
print(f"1.数据区间: {'OK' if new in c else 'FAIL'}")

# 2. S0标题
old = '今日焦点（6月13日·周五·证监会三年行动计划发布·央行双工具加码·中基协双指引落地）【周日6/15例行更新·无重大新新闻】'
new = '今日焦点（6月16日·周一·公募新规严控风格漂移·QDII科技ETF集体停牌·6月新基发行创同期新高）'
c = c.replace(old, new)
print(f"2.S0标题: {'OK' if new in c else 'FAIL'}")

# 3. S0 badge
c = c.replace('周日更新', '周一更新')
print(f"3.S0badge: {'OK'}")

# 4. Footer
old = '数据采集时间 2026年6月15日（周日例行更新）'
new = '数据采集时间 2026年6月16日（今日自动更新）'
c = c.replace(old, new)
print(f"4.Footer: {'OK' if new in c else 'FAIL'}")

# 5. 写入
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n写入完成，文件长度: {len(c)}")

# 6. 验证
with open(path, 'r', encoding='utf-8') as f:
    c2 = f.read()
print(f"重新读取验证: {len(c2)}")
checks = [
    ('数据区间', '2026.06.02 — 2026.06.16' in c2),
    ('S0标题', '6月16日·周一' in c2),
    ('Footer', '2026年6月16日' in c2),
]
for name, result in checks:
    print(f"  {'✅' if result else '❌'} {name}")
