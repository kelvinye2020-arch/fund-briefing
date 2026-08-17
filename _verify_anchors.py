# -*- coding: utf-8 -*-
import io
PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
html = io.open(PATH, "r", encoding="utf-8").read()

# the exact anchor strings used in update_20260711.py (old-part of each REPL)
checks = {
 "marker": "<!-- daily-update: 2026-07-10 -->",
 "badge": "📅 数据区间：2026.06.26 — 2026.07.10（每日更新）",
 "stats_block": """  <div class="stat-card">
    <div class="stat-number">39.48万亿</div>
    <div class="stat-label">公募总规模（截至2026年5月底·逼近40万亿）</div>""",
 "s0title": '      <span class="section-title">今日焦点（7月10日·周五·AI赛道ETF大举吸金·科创50ETF成净流入最多宽基·首批REITs全收益基金结募·科技主题基金破5600亿）</span>',
 "s0cards": """    <div class="card-grid">

      <!-- S0 Card 1: AI赛道ETF大举吸金·科创50ETF成净流入最多宽基 (T+0 07-10) -->""",
 "s1expired": """      <!-- S1 Card 1: 第二批公募基准调整全面铺开 (06-26) -->
      <div class="card p1">""",
 "s2expired": """      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会五方面推动资本市场法治协同建设·推动修改证券投资基金法</div>""",
 "s6": """      <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月10日（周五）·A股开盘涨跌不一·盘中翻红·CPO/半导体领涨·贵金属反弹</div>""",
 "s7remove": """      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-26（A股黑色星期五·半年度收官大跌·沪指-2.26%创业板-4.07%）</div>""",
 "s7add": """      <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
      <!-- 07-10 时间线条目 (NEW) -->""",
 "s8add": """    <div class="card-grid">

      <!-- S8 Card NEW: AI赛道ETF吸金·科技主题基金过热 (07-10) -->""",
 "s8_rm_a": """      <!-- S8 Card 0: 基金中考收官 (NEW) -->
      <div class="card p0">""",
 "s8_rm_b": """      <!-- S8 Card 1: A股06-30涨跌不一 -->""",
 "s8_rm_c": """      <!-- S8 Card 2: FOF单周发行环比+175% -->""",
 "s8_rm_d": """      <!-- S8 Card: A股半年度收官大跌 (06-27) -->""",
 "s8_rm_e": """      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 浮费基金业绩分化·三倍基诞生·费率机制正式生效</div>""",
 "s8_rm_f": """      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>""",
}
for k, s in checks.items():
    print("%-12s count=%d" % (k, html.count(s)))
