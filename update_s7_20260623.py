#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - S7时间线 更新脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# S7 新时间线条目 (06-23 今日事件)
new_timeline_items = """
        <div class="timeline-item">
          <div class="timeline-dot red"></div>
          <div>
            <div class="timeline-date">2026-06-23（周二·A股低开·沪指-0.23%·创业板-0.36%·港股高开）</div>
            <div class="timeline-title">A股四大指数集体低开 / 港股三大指数小幅高开·科技股部分反弹·芯片股强势</div>
            <div class="timeline-desc">6月23日，A股四大指数集体低开，沪指跌0.23%（4153.59点），深成指跌0.29%，创业板指跌0.36%，科创50跌1.01%。港股三大指数小幅高开，恒指涨0.13%，科技股部分反弹（美团·百度涨近1%），芯片股继续强势（兆易创新高开2.5%）。美股昨夜纳指跌1.32%（SpaceX跌16%·谷歌跌5%）。</div>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot red"></div>
          <div>
            <div class="timeline-date">2026-06-23（公募自购常态化·年内净申购78亿·权益类占比28%）</div>
            <div class="timeline-title">公募年内自购超78亿元 / 权益基金占比28%·被动指数+港股科技成核心方向 / 自购走向常态化</div>
            <div class="timeline-desc">公募排排网数据显示，截至6月22日，年内公募基金净申购金额达78亿元，同比增长约9%，参与自购的基金公司超60家。权益基金净申购达22亿元（占比28%），其中被动指数型基金占权益基金总额41%。自购常态化+结构转向权益→行业从规模导向向投资者利益导向转型。</div>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot blue"></div>
          <div>
            <div class="timeline-date">2026-06-23（半导体设备中报预增·长川科技预增110%-134%）</div>
            <div class="timeline-title">半导体设备首份中报预计翻倍 / 长川科技上半年预增110%-134% / 半导体设备ETF价格3.829再创历史新高</div>
            <div class="timeline-desc">6月22日晚间，半导体ETF招商前十大权重股长川科技发布半年度业绩预告，预计上半年归母净利润9-10亿元，同比+110.76%-134.18%。半导体设备ETF招商6月22日收涨2.30%，收盘价3.829再创历史新高。2026年全球存储芯片正经历"史诗级"扩产，上游设备材料公司业绩释放具备扎实基础。</div>
          </div>
        </div>
"""

# 找到 S7 的开始位置（在 section-header 之后，第一个 timeline-item 之前）
s7_header_end = html.find('<!-- ============ Section 7: 关键时间线 ============ -->')
if s7_header_end > 0:
    # 找到 section 的 card div 开始位置
    s7_card_start = html.find('<div class="card" style="border-left-color: var(--info);">', s7_header_end)
    
    if s7_card_start > 0:
        # 找到第一个 timeline-item 的位置
        first_timeline = html.find('<div class="timeline-item">', s7_card_start)
        
        if first_timeline > 0:
            # 在第一个 timeline-item 之前插入新的时间线条目
            html_new = html[:first_timeline] + new_timeline_items + html[first_timeline:]
            
            # 写入文件
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html_new)
            
            print("✅ S7 时间线已更新（添加3条06-23事件）")
            print("   - A股低开·港股高开（06-23）")
            print("   - 公募自购78亿（06-23）")
            print("   - 半导体设备中报预增（06-23）")
            print("   ⚠️ 当前时间线条目约13条，建议清理06-09条目（T-14边界）")
        else:
            print("❌ 未找到第一个 timeline-item，更新失败")
    else:
        print("❌ 未找到 S7 的 card div，更新失败")
else:
    print("❌ 未找到 S7 标记，更新失败")
