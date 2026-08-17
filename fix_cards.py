#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用正则表达式更新 index.html 的 S0 卡片内容"""
import re

fp = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"文件长度: {len(c)}")

# 1. S0 卡片1: 替换标题（用正则，不依赖精确匹配）
# 把 "端午三市同休！A股/港股通/美股" 替换为新标题
old = r'陆家嘴论坛6/18落幕！三大监管定调：不走注水救市老路·转向制度改革替代短期刺激'
if old in c:
    print("  卡片1标题已更新，跳过")
else:
    # 用正则替换卡片1的 card-title
    pattern = r'(<div class="card-title">)[^<]*端午三市同休[^<]*(</div>)'
    repl = r'\1🔴 陆家嘴论坛6/18落幕！三大监管定调：不走注水救市老路·转向制度改革替代短期刺激\2'
    new_c = re.sub(pattern, repl, c)
    if new_c != c:
        c = new_c
        print("[1/6] 卡片1标题已更新（正则）")
    else:
        print("[1/6] 未匹配卡片1标题")

# 2. S0 卡片2: 美联储鹰派 → 主动ETF获批
pattern2 = r'(<div class="card-title">)[^<]*美联储鹰派信号持续发酵[^<]*(</div>)'
repl2 = r'\1🔴 主动ETF获批！吴清6/17陆家嘴宣布·沪深交易所同步发布业务指引·公募基金重大创新\2'
new_c = re.sub(pattern2, repl2, c)
if new_c != c:
    c = new_c
    print("[2/6] 卡片2标题已更新（正则）")
else:
    print("[2/6] 未匹配卡片2标题（可能已更新）")

# 3. S0 卡片3: 五部门新能源车 → 端午三市同休持续
pattern3 = r'(<div class="card-title">)[^<]*五部门启动2026新能源车下乡[^<]*(</div>)'
repl3 = r'\1🟠 端午三市同休持续·节后6/22开市·美联储鹰派信号假期发酵·QDII产品节后或承压\2'
new_c = re.sub(pattern3, repl3, c)
if new_c != c:
    c = new_c
    print("[3/6] 卡片3标题已更新（正则）")
else:
    print("[3/6] 未匹配卡片3标题（可能已更新）")

# 4. 更新 S0 卡片1 的 date-tag (06-19 → 06-18~20)
pattern_dt1 = r'(<div class="card-title">[^<]*陆家嘴论坛[^<]*</div>\s*<div class="card-meta">[^<]*<span class="priority-tag[^<]*</span>\s*<span class="date-tag">)06-19(</span>)'
repl_dt1 = r'\106-18~20\2'
new_c = re.sub(pattern_dt1, repl_dt1, c)
if new_c != c:
    c = new_c
    print("[4a/6] 卡片1 date-tag 已更新")
else:
    print("[4a/6] 卡片1 date-tag 未变（可能已更新）")

# 5. 清理 S1 中 06-05 的条目（中证金牛）
pattern_s1 = r'\s*<div class="card p1">\s*<div class="card-top">\s*<div class="card-title">[^<]*中证金牛[^<]*</div>\s*<div class="card-meta">.*?</div>\s*</div>\s*<div class="card-body">.*?</div>\s*<div class="card-footer">.*?</div>'
new_c = re.sub(pattern_s1, '', c, flags=re.DOTALL)
if new_c != c:
    c = new_c
    print("[5/6] 已删除 S1 中 06-05 中证金牛条目")
else:
    print("[5/6] 未找到 S1 中证金牛条目（可能已删除）")

# 6. 清理 S2 中 06-05 的条目（国办私募基金）
pattern_s2 = r'\s*<div class="card p0">\s*<div class="card-top">\s*<div class="card-title">[^<]*国办发文[^<]*</div>\s*<div class="card-meta">.*?</div>\s*</div>\s*<div class="card-body">.*?</div>\s*<div class="card-footer">.*?</div>'
new_c = re.sub(pattern_s2, '', c, flags=re.DOTALL)
if new_c != c:
    c = new_c
    print("[6/6] 已删除 S2 中 06-05 国办私募基金条目")
else:
    print("[6/6] 未找到 S2 国办私募基金条目（可能已删除）")

# 写回文件
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n[完成] 文件已保存，新长度: {len(c)}")
