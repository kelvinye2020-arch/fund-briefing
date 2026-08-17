#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 - S0今日焦点更新脚本
执行日期：2026-06-23
"""

import re

# 读取当前 HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# S0 今日焦点 - 新内容 (T+0 2026-06-23)
s0_new_cards = """
      <!-- S0 Card 1: 公募自购超78亿 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募年内自购超78亿元·权益类占比28%·被动指数+港股科技成核心方向</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模创新高：</b>公募排排网数据显示，截至6月22日，年内公募基金净申购金额达<b>78亿元</b>，同比增长约9%，参与自购的基金公司超60家。<br>
          <b>结构变化：</b>权益基金净申购达<b>22亿元</b>（占比28%），其中被动指数型基金占权益基金总额41%。债券型基金自购占比从2025年同期的近半，下降至20.8%。<br>
          <b>主题方向：</b>港股主题基金净申购2.4亿元（占11%），科技主题基金净申购1.4亿元（占6.5%）。<br>
          <b>对基金行业影响：</b>自购常态化+结构转向权益→行业从规模导向向投资者利益导向转型→腾安可关注自购比例高、锁定期长的产品推荐机会。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/tech/roll/2026-06-23/doc-inieixwx9811983.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济参考报</span></a>
          <span class="impact-tag medium">自购升温：高</span>
        </div>
      </div>

      <!-- S0 Card 2: A股低开 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 A股6/23低开·沪指跌0.23%·创业板跌0.36%·人形机器人/PCB/AI应用下挫</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>开盘数据：</b>6月23日，A股四大指数集体低开，沪指跌<b>0.23%</b>，深成指跌<b>0.29%</b>，创业板指跌<b>0.36%</b>，科创综指跌<b>0.8%</b>。<br>
          <b>盘面表现：</b>人形机器人、PCB、华为鸿蒙、网络安全、炒股软件、AI应用、光伏、芯片概念股下挫。培育钻石、工业金属、液冷服务器概念股活跃。<br>
          <b>个股亮点：</b>卫星化学一字涨停，公司预计上半年净利润同比增长119%-155%。<br>
          <b>对基金行业影响：</b>低开不改中期趋势→光大证券认为市场新一轮上行趋势逐步确立→腾安客户咨询可能增加，需准备市场观点话术。
        </div>
        <div class="card-footer">
          <a href="https://cj.sina.cn/articles/view/1733360754/6750fc7202001fusg" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经</span></a>
          <span class="impact-tag low">A股低开：低</span>
        </div>
      </div>

      <!-- S0 Card 3: 半导体设备中报预增 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 半导体设备首份中报预计翻倍！长川科技上半年预增110%-134%·存储扩产锁定业绩</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>首份中报预告：</b>6月22日晚间，半导体ETF招商(561980)前十大权重股<b>长川科技</b>发布半年度业绩预告，预计上半年归母净利润<b>9-10亿元</b>，同比<b>+110.76%-134.18%</b>；预计二季度净利润5.47-6.47亿元，环比<b>+55%-83%</b>。<br>
          <b>ETF表现：</b>半导体设备ETF招商6月22日收涨2.30%，收盘价3.829再创历史新高，成为A股"最贵"半导体设备ETF。本周将进行1:5份额拆分。<br>
          <b>行业背景：</b>2026年全球存储芯片正经历"史诗级"扩产，海外巨头五年产能翻倍直接拉动设备采购需求。<br>
          <b>对基金行业影响：</b>半导体设备中报季业绩确定性优势→相关主题基金可能受关注→腾安可提前准备相关产品推荐逻辑。
        </div>
        <div class="card-footer">
          <a href="https://caifuhao.eastmoney.com/news/20260623091137242776260" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <span class="impact-tag medium">半导体：中高</span>
        </div>
      </div>

      <!-- S0 Card 4: 主动ETF业务指引解读 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 主动ETF业务指引落地·管理人准入门槛：5年经验+100亿规模·投资组合不少于30只</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-23解读</span>
          </div>
        </div>
        <div class="card-body">
          <b>指引落地：</b>6月17日，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。主动ETF融合主动投研能力与ETF标准化运作优势。<br>
          <b>准入门槛：</b>管理人需具备<b>5年以上</b>主动权益公募基金管理运作经验，近3年平均主动权益公募基金管理规模不少于<b>100亿元</b>。<br>
          <b>投资要求：</b>基金投资组合持有证券数量不少于<b>30只</b>，前十大持仓合计占比不超过60%；合理控制换手率，保持投资风格稳定。<br>
          <b>对基金行业影响：</b>主动ETF有望成为ETF市场新增长引擎→产品创新加速→腾安可关注主动ETF产品布局机会。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/730782" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag low">产品创新：低</span>
        </div>
      </div>
"""

# 使用正则表达式替换 S0 的 card-grid 内容
# 找到 S0 的 card-grid 开始和结束位置
s0_pattern = r'(<!-- ============ Section 0: 今日焦点 ============ -->.*?<div class="card-grid">).*?(</div>\s*</div>\s*<!-- ============ Section 1)'

# 由于正则表达式复杂，我使用更简单的方法：直接替换整个 S0 部分
# 找到 S0 开始和 S1 开始的位置
s0_start = html.find('<!-- ============ Section 0: 今日焦点 ============ -->')
s1_start = html.find('<!-- ============ Section 1: 重磅信息 ============ -->')

if s0_start > 0 and s1_start > 0:
    # 提取 S0 之前的 HTML
    html_before_s0 = html[:s0_start]
    
    # 构建新的 S0 部分
    new_s0 = f'''  <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（6月23日·周二·公募自购78亿·A股低开·半导体设备中报预增）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
{s0_new_cards}
    </div>
  </div>

'''
    
    # 提取 S1 及之后的 HTML
    html_after_s0 = html[s1_start:]
    
    # 合并
    new_html = html_before_s0 + new_s0 + html_after_s0
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("✅ S0 今日焦点已更新（4张卡片）")
    print("   - 公募自购超78亿 (06-23)")
    print("   - A股低开 (06-23)")
    print("   - 半导体设备中报预增 (06-23)")
    print("   - 主动ETF业务指引解读 (06-23)")
else:
    print("❌ 未找到 S0 或 S1 标记，更新失败")
