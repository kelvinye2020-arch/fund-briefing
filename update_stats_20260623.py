#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - Stats Bar 更新脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 新的 Stats Bar 内容
new_stats_bar = """<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">公募自购78亿↑</div>
    <div class="stat-label">年内净申购78亿·同比+9%·权益类占28%·被动指数+港股科技成核心方向</div>
    <div class="stat-change up">▲ 自购常态化·行业从规模导向向投资者利益导向转型</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">半导体设备中报预增</div>
    <div class="stat-label">长川科技上半年预增110%-134%·ETF价格3.829再创历史新高·全球存储扩产拉动设备需求</div>
    <div class="stat-change up">▲ 中报季业绩确定性优势·晶圆厂扩产订单陆续交付</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">A股低开·创业板-0.36%</div>
    <div class="stat-label">6/23四大指数集体低开·沪指-0.23%·深成指-0.29%·创业板-0.36%·科创综指-0.8%</div>
    <div class="stat-change neutral">■ 人形机器人/PCB/AI应用下挫·培育钻石/工业金属活跃</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">主动ETF指引落地</div>
    <div class="stat-label">沪深交易所6/17发布业务指引·管理人准入：5年经验+100亿规模·投资组合不少于30只</div>
    <div class="stat-change neutral">■ 主动ETF望成ETF市场新增长引擎·产品创新加速</div>
  </div>
</div>"""

# 使用正则表达式找到并替换 stats-bar
stats_pattern = r'<div class="stats-bar">.*?</div>\s*</div>\s*<!-- Main Content -->'

match = re.search(stats_pattern, html, re.DOTALL)
if match:
    # 替换找到的内容
    html = html[:match.start()] + new_stats_bar + html[match.end():]
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Stats Bar 已更新（4个核心数据卡片）")
    print("   - 公募自购78亿↑")
    print("   - 半导体设备中报预增")
    print("   - A股低开·创业板-0.36%")
    print("   - 主动ETF指引落地")
else:
    print("❌ 未找到 stats-bar 标记，更新失败")
