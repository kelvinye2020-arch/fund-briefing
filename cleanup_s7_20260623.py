#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - S7时间线 清理过期条目脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 06-09 的 timeline-item （需要删除）
# 找到包含 "06-09" 的 timeline-item 并删除
# 06-09 的条目是最后一个，在 S7 的底部

# 使用正则表达式找到并删除 06-09 的 timeline-item
# 06-09 条目的特征：包含 "06-09" 和 "A股暴力反弹收复4000点"

pattern = r'\s*<div class="timeline-item">\s*<div class="timeline-dot red"></div>\s*<div>\s*<div class="timeline-date">2026-06-09（A股暴力反弹收复4000点·美股分化·港股止跌）</div>.*?</div>\s*</div>\s*</div>'

match = re.search(pattern, html, re.DOTALL)
if match:
    # 删除找到的内容
    html = html[:match.start()] + html[match.end():]
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ S7 时间线已清理：删除 06-09 条目")
    print("   当前时间线条目：12条（06-10 至 06-23）")
else:
    print("⚠️ 未找到 06-09 时间线条目，可能已删除或格式不匹配")
    print("   建议手动检查 S7 时间线条目数量")
    
# 验证当前时间线条目数量
count = html.count('<div class="timeline-item">')
print(f"   当前时间线条目数量：{count}")
