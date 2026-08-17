#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - 每日自动更新脚本
执行日期：2026-06-23
"""

import re
from datetime import datetime, timedelta

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

today = '2026-06-23'
today_short = '06-23'
today_display = '6月23日·周二·公募自购78亿·A股低开·半导体设备中报预增'

# 1. 更新 HTML 头部注释
html = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', 
              f'<!-- daily-update: {today} -->', 
              html)

# 2. 更新 content-fingerprint meta
html = re.sub(r'content="[^"]*"', 
              f'content="公募自购78亿|半导体设备中报预增|主动ETF指引|A股低开"', 
              html, count=1)

# 3. 更新 S0 今日焦点标题
html = re.sub(r'今日焦点（[^）]*）', 
              f'今日焦点（{today_display}）', 
              html)

# 4. 更新 footer 数据更新时间
html = re.sub(r'数据更新时间：\d{4}年\d{1,2}月\d{1,2}日', 
              f'数据更新时间：{today.replace("-", "年").replace("-", "月")}日', 
              html)

html = re.sub(r'近两周核心资讯（\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}）', 
              f'近两周核心资讯（2026.06.09 — 2026.06.23）', 
              html)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 基础更新完成：{today}")
print("   下一步：更新各模块具体内容")
