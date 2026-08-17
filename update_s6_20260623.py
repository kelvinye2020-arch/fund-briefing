#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - S6市场行情速览 更新脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# S6 市场行情 - 新内容 (2026-06-23 周二)
s6_new_content = """    <div class="card p3">
      <div class="card-top">
        <div class="card-title">2026年6月23日（周二）·A股低开·港股高开·美股昨夜纳指跌1.32%</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股今日（6/23）低开：</b><br>
            ▪ 沪指跌<b>0.23%</b>（4153.59点）<br>
            ▪ 深成指跌<b>0.29%</b>（16324.24点）<br>
            ▪ 创业板指跌<b>0.36%</b>（4343.88点）<br>
            ▪ 科创50跌<b>1.01%</b>（1929.27点）<br>
            ▪ 盘面：培育钻石·液冷服务器活跃；MLCC·互联网保险走低<br><br>
            <b>📊 港股今日（6/23）高开：</b><br>
            ▪ 恒生指数涨<b>0.13%</b><br>
            ▪ 国企指数涨<b>0.01%</b><br>
            ▪ 恒生科技指数涨<b>0.04%</b><br>
            ▪ 科技股部分反弹：美团·百度涨近1%，阿里涨0.49%；芯片股强势：兆易创新高开2.5%
          </div>
          <div>
            <b>📊 美股昨夜（6/22）收盘分化：</b><br>
            ▪ 道指<b>+0.29%</b>（41712.71点）——能源·航运传统蓝筹上涨<br>
            ▪ 纳指<b>-1.32%</b>（26166.60点）——SpaceX跌16%·谷歌跌5%·亚马逊跌4.8%<br>
            ▪ 标普500<b>-0.37%</b>（7472.79点）<br>
            ▪ 芯片股分化：美光+6%·英特尔+5% vs ARM-7%·博通-4%<br><br>
            <b>📊 对基金行业影响（今日A股）：</b><br>
            ▪ A股低开→客户可能咨询市场观点，提前准备话术<br>
            ▪ 科技股分化→关注科创50能否止跌企稳<br>
            ▪ 港股高开→港股主题基金可能表现活跃
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·2026-06-23 09:58</span>
        <span class="source-tag">美股：2026-06-22 收盘</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>"""

# 找到 S6 开始和 S7 开始的位置
s6_start = html.find('<!-- ============ Section 6: 市场行情速览 ============ -->')
s7_start = html.find('<!-- ============ Section 7: 关键时间线 ============ -->')

if s6_start > 0 and s7_start > 0:
    # 提取 S6 之前的 HTML
    html_before_s6 = html[:s6_start]
    
    # 构建新的 S6 部分
    new_s6 = f'''  <!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

{s6_new_content}
  </div>
'''
    
    # 提取 S7 及之后的 HTML
    html_after_s6 = html[s7_start:]
    
    # 合并
    new_html = html_before_s6 + new_s6 + html_after_s6
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("✅ S6 市场行情速览已更新")
    print("   - A股低开（6/23 09:58）")
    print("   - 港股高开（6/23 09:24）")
    print("   - 美股昨夜收盘分化（6/22）")
else:
    print("❌ 未找到 S6 或 S7 标记，更新失败")
