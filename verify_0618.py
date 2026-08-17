#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 index.html 更新结果"""

import re

with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. S7 时间线条目
entries = re.findall(r'timeline-date">(2026-06-\d+)', content)
print("S7 时间线条目：", entries)
print("  06-04 是否存在：", "2026-06-04" in entries)
print("  06-05 是否存在：", "2026-06-05" in entries)
print("  06-18 是否存在：", "2026-06-18" in entries)
print()

# 2. S0 第3张卡片
idx3 = content.find('科创50暴涨超4%')
if idx3 > 0:
    # 取该卡片区域（从标题到下一个 card 或 section 结束）
    snippet = content[idx3:idx3+2000]
    has_action = 'action-box' in snippet
    print("S0 第3张卡片：")
    print("  标题正确：", '科创50暴涨超4%' in content)
    print("  是否有 action-box：", has_action)
    # 检查 card-footer
    has_footer = '东方财富·资金流向' in snippet or '每经·ETF净流出' in snippet
    print("  是否有正确 footer：", has_footer)
else:
    print("S0 第3张卡片标题未找到")
print()

# 3. S6 市场行情
print("S6 市场行情：")
print("  标题正确：", '今日行情（6/18上午10:30）' in content)
print("  昨日收盘：", '昨日收盘（6/17）' in content)
print("  美联储议息结果：", '美联储议息结果' in content)
print()

# 4. Header + Footer + daily-update
print("Header 日期区间：", '06.04 — 2026.06.18' in content)
print("Footer 数据更新时间：", '2026年6月18日 10:30' in content)
print("daily-update 标记：", 'daily-update: 2026-06-18' in content)
print()

# 5. Stats Bar
print("Stats Bar：")
print("  第1张（美联储）：", '美联储转鹰' in content)
print("  第2张（陆家嘴）：", '陆家嘴论坛收官' in content)
print("  第3张（科创）：", '沪指4108' in content)
print("  第4张（端午）：", '端午休市倒计时' in content)
