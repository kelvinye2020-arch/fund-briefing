#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最小化更新脚本 - 避免多行字符串和emoji"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

fp = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"文件长度: {len(c)}")

# 1. daily-update 标记
old1 = '<!-- daily-update: 2026-06-19 -->'
new1 = '<!-- daily-update: 2026-06-20 -->'
if old1 in c:
    c = c.replace(old1, new1)
    print("[1/8] OK daily-update")
else:
    print("[1/8] SKIP daily-update 已更新或不存在")

# 2. content-fingerprint
old2 = 'content="美联储转鹰年内或加息一次|端午三市同休6/19-21|SpaceX挂牌后首周走势震荡|五部门新能源车下乡活动启动"'
new2 = 'content="陆家嘴论坛闭幕三大监管定调|主动ETF获批沪深同步推出|端午休市A股6/22开市|美联储沃什首秀转鹰"'
if old2 in c:
    c = c.replace(old2, new2)
    print("[2/8] OK content-fingerprint")
else:
    print("[2/8] SKIP content-fingerprint")

# 3. Header 数据区间
old3 = '数据区间：2026.06.05 — 2026.06.19（今日自动更新）'
new3 = '数据区间：2026.06.06 — 2026.06.20（今日自动更新）'
if old3 in c:
    c = c.replace(old3, new3)
    print("[3/8] OK Header 数据区间")
else:
    print("[3/8] SKIP Header 数据区间")

# 4. Stats Bar - 替换
old4 = ('<!-- Stats Bar -->\n<div class="stats-bar">\n  <div class="stat-card">\n'
       '    <div class="stat-number">端午三市同休</div>')
new4 = ('<!-- Stats Bar -->\n<div class="stats-bar">\n  <div class="stat-card">\n'
       '    <div class="stat-number">陆家嘴论坛闭幕·三大监管定调</div>')
if old4[0:50] in c:
    # 用更精确的方式
    c = c.replace('>端午三市同休<', '>陆家嘴论坛闭幕·三大监管定调<')
    c = c.replace('>美联储转鹰·年内或加息<', '>主动ETF获批·沪深同步推出<')
    c = c.replace('>沪指4090·科创+3.84%<', '>端午休市中·6/22开市<')
    c = c.replace('>五部门新能源车下乡<', '>美联储沃什首秀·年内或加息<')
    print("[4/8] OK Stats Bar (逐卡片替换)")
else:
    print("[4/8] SKIP Stats Bar")

# 5. S0 今日焦点 - 替换标题
old5 = '今日焦点（6月19日·周四·端午休市首日·美联储鹰派持续发酵·五部门新能源车下乡）'
new5 = '今日焦点（6月20日·周六·端午休市·陆家嘴论坛闭幕解读·主动ETF获批）'
if old5 in c:
    c = c.replace(old5, new5)
    print("[5/8] OK S0 标题")
else:
    print("[5/8] SKIP S0 标题")

# 6. S0 卡片1 标题
old6 = '>端午三市同休！A股/港股通/美股6/19-21同步休市，节后6/22开市·持币过节情绪主导<'
new6 = '>RED 陆家嘴论坛6/18落幕！三大监管定调：不走注水救市老路·转向制度改革替代短期刺激<'
if old6 in c:
    c = c.replace(old6, new6)
    print("[6a/8] OK S0 卡片1 标题")
else:
    print("[6a/8] SKIP S0 卡片1 标题")

# 7. Footer
old7 = '数据更新时间：2026年6月19日 10:30 · 近两周核心资讯（06-05 — 06-19）'
new7 = '数据更新时间：2026年6月20日 10:30 · 近两周核心资讯（06-06 — 06-20）'
if old7 in c:
    c = c.replace(old7, new7)
    print("[7/8] OK Footer")
else:
    print("[7/8] SKIP Footer")

# 写回文件
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n[完成] 文件已保存，新长度: {len(c)}")
