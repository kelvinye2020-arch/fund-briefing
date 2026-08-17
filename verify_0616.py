#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 index.html 2026-06-16 更新质量"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("基金行业资讯看板 2026-06-16 更新验证")
print("=" * 60)

# 检查关键更新
checks = [
    ("数据区间", "2026.06.02 — 2026.06.16" in content),
    ("S0标题", "今日焦点（6月16日·周一" in content),
    ("S0卡片1日期06-15", '06-15' in content and '多项公募新规' in content),
    ("S0卡片2日期06-16", '06-16' in content and 'ETF停牌' in content),
    ("S0卡片3日期06-16", '06-16' in content and '新基发行' in content),
    ("S1超期已删", "创业板指首次收盘超越上证" not in content),
    ("S2超期已删", "06-01~04" not in content),
    ("S6更新", "今日行情（6/16上午）" in content),
    ("S7超期已删(06-02)", "06-02（腾讯暴涨" not in content),
    ("S7超期已删(06-01)", "06-01（宇树科技" not in content),
    ("S7新增06-16", "2026-06-16（多只QDII" in content),
    ("S7新增06-15", "2026-06-15（多项公募新规" in content),
    ("S8日期", "6月16日周一更新" in content),
    ("Footer日期", "2026年6月16日" in content),
]

print("\n[内容] 关键更新检查：")
for name, result in checks:
    status = "[OK]" if result else "[FAIL]"
    print(f"  {status} {name}")

# 检查跨模块重复
print("\n[去重] 跨模块重复检查：")
s0_block = content[content.find('Section 0'):content.find('Section 1')]
s1_block = content[content.find('Section 1'):content.find('Section 2')]
s2_block = content[content.find('Section 2'):content.find('Section 3')]

s0_titles = re.findall(r'<div class="card-title">([^<]+)</div>', s0_block)
s1_titles = re.findall(r'<div class="card-title">([^<]+)</div>', s1_block)
s2_titles = re.findall(r'<div class="card-title">([^<]+)</div>', s2_block)

def simplify(title):
    return re.sub(r'[^\w\u4e00-\u9fff].*? ', '', title)[:30]

s0_set = set(simplify(t) for t in s0_titles)
s1_set = set(simplify(t) for t in s1_titles)
s2_set = set(simplify(t) for t in s2_titles)

overlap = s0_set & s1_set or s0_set & s2_set or s1_set & s2_set
if overlap:
    print(f"  [FAIL] 发现跨模块重复：{overlap}")
else:
    print(f"  [OK] 无跨模块重复（S0:{len(s0_titles)}条 S1:{len(s1_titles)}条 S2:{len(s2_titles)}条）")

# 检查date-tag时效性
print("\n[时效] date-tag 检查：")
all_dates = re.findall(r'<span class="date-tag">([^<]+)</span>', content)
print(f"  共找到 {len(all_dates)} 个 date-tag")
invalid = []
for d in all_dates:
    m = re.search(r'(\d{2})-(\d{2})', d)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        if (month == 6 and day < 2) or month < 6:
            invalid.append(d)
if invalid:
    print(f"  [FAIL] 发现超期date-tag: {invalid}")
else:
    print(f"  [OK] 所有date-tag均在T-14内")

print("\n" + "=" * 60)
print("验证完成！")
