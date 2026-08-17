#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金看板兜底更新脚本 - 2026-06-29
更新内容：S0今日焦点 / S6市场行情 / S7时间线 / header日期 / stats bar / daily-update标记
"""

import re
from datetime import datetime, timedelta

TODAY = "2026-06-29"
TODAY_DISPLAY = "6月29日"
TODAY_WEEKDAY = "周一"

# ============================================================
# 新内容定义
# ============================================================

# --- S0 今日焦点（3条卡片）---
S0_NEW = '''    <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（6月29日·周一·公募基金基准改革全面铺开·翻倍基集中限购）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">

      <!-- S0 Card 1: 第二批公募基准调整全面铺开 -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 公募基金第二批业绩比较基准调整落地·千余只产品·从试点探路转入全面铺开</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-29</span>
          </div>
        </div>
        <div class="card-body">
          <b>全面铺开：</b>6月26日晚间，继首批12家机构后，第二批近百家基金公司发布存量产品业绩比较基准调整公告，涉及<b>千余只</b>产品，覆盖主动权益、主动债券、FOF、QDII等全部主流品类。<br>
          <b>改革意义：</b>基准改革从"试点落地"迈向"全面深化"，通过统一校准业绩评价标尺，解决基准失真、风格漂移等行业痛点。调整坚持"优先调整基准而非调仓"原则，不会对市场造成冲击。<br>
          <b>对基金行业影响：</b>产品名实相符→投资者选择更有依据→腾安需在营销中突出基准说明，并检查现有产品展示是否与实际基准一致。
        </div>
        <div class="card-footer">
          <a href="https://www.cnfin.com/yw-lb/detail/20260626/4432437_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经</span></a>
          <a href="https://www.chnfund.com/article/AR53146ee3-d00b-0bf0-91ec-3a22159d2918" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <span class="impact-tag high">基准改革：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 检查腾安平台产品展示页的业绩比较基准是否与实际一致→产品部；<br>
            ② 准备基准改革客户沟通话术→营销部；<br>
            ③ 关注基准调整后基金经理投资风格变化→投资顾问。
          </div>
        </div>
      </div>

      <!-- S0 Card 2: 翻倍基纷纷限购 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 年内收益前十公募基金均已限购·易方达郑希三只产品同步压降·部分仅限10元</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-29</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购动态：</b>6月25日，易方达基金公告"百亿基金经理"郑希旗下三只产品同步下调申购限额：易方达信息行业精选从50万降至<b>1万元</b>，易方达信息产业同步降至1万元，易方达全球成长精选(QDII)从20元压降至<b>10元</b>。<br>
          <b>行业全景：</b>截至6月25日，全市场年内收益率排名前十的公募产品涨幅均超150%，<b>已全部启动限购</b>。财通基金旗下4只翻倍基单日限购低至100元，富国创新科技A限购10万元。<br>
          <b>对基金行业影响：</b>翻倍基集中限购→明星产品稀缺性加剧→腾安应提前储备替代产品，并准备客户解释话术。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260626A08VB800" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻</span></a>
          <a href="https://www.stcn.com/article/detail/3984277.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">限购潮：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 基金中考冲刺历史新高 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 基金中考倒计时2天·最高收益175%有望刷新历史·首尾相差200个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-29</span>
          </div>
        </div>
        <div class="card-body">
          <b>业绩格局：</b>截至6月28日，全市场主动权益产品年内净值翻倍的基金数量已突破<b>百只</b>，最高收益达<b>175%</b>（财通多策略福鑫定开等），有望刷新基金中考历史纪录。但极致分化下，首尾业绩差距已达<b>200个百分点</b>。<br>
          <b>赛道特征：</b>翻倍基无一例外将AI算力作为核心重仓对象，财通基金金梓才所管多只产品位列业绩前十。消费、港股等方向产品业绩垫底。<br>
          <b>对基金行业影响：</b>中考业绩将影响下半年资金流向→腾安应提前布局绩优基金经理营销素材→7月初发力。
        </div>
        <div class="card-footer">
          <a href="https://yuemengdi@stcn.com/article/detail/3984183.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">中考业绩：极高</span>
        </div>
      </div>

    </div>
  </div>'''

# --- S6 市场行情（基于6月26日收盘数据）---
S6_NEW = '''      <!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

    <div class="card p3">
      <div class="card-top">
        <div class="card-title">2026年6月29日（周一）·A股开市·最新参考：6月26日（周五）收盘数据</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股最近收盘（6/26 周五）：</b><br>
            ▪ 沪指 <b>-2.26%</b>（4027.26点）—— 创3月24日以来最大单日跌幅<br>
            ▪ 深成指 <b>-3.44%</b>（15782.22点）<br>
            ▪ 创业板指 <b>-4.07%</b>（4194.21点）—— 成长赛道集中回调<br>
            ▪ 科创综指 <b>-2.02%</b>（2343.66点）<br>
            ▪ 成交额：沪市16212亿+深市19312亿=35524亿元<br><br>
            <b>📊 港股最近收盘（6/26 周五）：</b><br>
            ▪ 恒生指数 <b>-1.76%</b>（22671.86点）<br>
            ▪ 恒生科技 <b>-3.41%</b>（4255.59点）<br>
            ▪ 国企指数 <b>-1.94%</b>（7460.84点）<br>
            ▪ 日经225 <b>-4.15%</b>（69360.88点）
          </div>
          <div>
            <b>📊 美股最近收盘（6/26 周四夜盘）：</b><br>
            ▪ 道指 <b>-0.09%</b>（51876.11点）<br>
            ▪ 纳指 <b>-0.24%</b>（25297.62点）<br>
            ▪ 标普500 <b>-0.05%</b>（7354.02点）<br>
            ▪ 欧股同步走弱：德国DAX -1.29%<br><br>
            <b>📊 今日关注（6/29 周一）：</b><br>
            ▪ A股黑色星期五后再度开市→关注科技板块能否企稳<br>
            ▪ 公募基金基准改革全面铺开→行业关注产品调整影响<br>
            ▪ 翻倍基集中限购→资金流向替代产品
          </div>
        </div>
      </div>
        <div class="card-footer">
          <span class="source-tag">NeoData·2026-06-29 10:00</span>
          <span class="source-tag">数据来源：06-26 收盘</span>
        </div>
    </div>
  </div>'''

# --- S7 时间线（保留有效条目+新增今日事件，T-14到T）---
# 保留：06-26, 06-25, 06-24, 06-22, 06-20, 06-18, 06-17, 06-16, 06-15
# 删除：超期条目（如果有06-14及更早）
# 新增：06-29 今日事件

S7_NEW = '''      <!-- ============ Section 7: 关键时间线 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--primary-light);color:var(--primary);">📅</div>
      <span class="section-title">关键时间线（近两周）</span>
      <span class="section-badge" style="background:var(--primary-light);color:var(--primary);">事件脉络</span>
    </div>

    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-29（公募基准改革全面铺开·翻倍基集中限购·基金中考倒计时2天）</div>
          <div class="timeline-title">公募基金第二批基准调整全面铺开 / 年内前十基金均已限购 / 中考最高收益175%冲历史纪录</div>
          <div class="timeline-desc">6月26日第二批千余只公募基金基准调整公告落地，改革从"试点"转入"全面铺开"。同期，年内收益前十基金全部限购，易方达郑希三只产品同步压降。基金中考仅剩2天，最高收益175%有望刷新历史纪录，但首尾相差200个百分点，极致分化凸显。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-26（A股黑色星期五·半年度收官大跌·沪指-2.26%创业板-4.07%）</div>
          <div class="timeline-title">A股半年度收官集体重挫 / 上证-2.26%·深成指-3.44%·创业板-4.07% / 亚太股市同步走弱</div>
          <div class="timeline-desc">6月26日A股半年度收官，三大指数集体重挫，创业板指暴跌4.07%领跌主要指数。全市场超4600只个股下跌，成交额3.55万亿元。下跌受四重压力叠加：机构半年业绩结算+风格漂移严查→集中调仓；海外科技股大跌+韩国熔断→风险偏好传导；AI产业链价格传导不畅→盈利前景担忧。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-25（第二批公募基准调整公告落地·6月新基发行破千亿）</div>
          <div class="timeline-title">公募基金第二批业绩比较基准调整全面铺开·千余只产品·6月新基发行破千亿</div>
          <div class="timeline-desc">6月26日晚，第二批近百家基金公司发布存量产品业绩比较基准调整公告（实际公告日发布于6月25-26日），涉及千余只产品。同期，6月新基金发行规模突破1012亿元，FOF年内发行规模达1177亿元，超越2021年峰值。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-24（浮费基金一周年·QDII限购再加码·富国基金换帅）</div>
          <div class="timeline-title">首批浮费基金运作满一年·业绩断层316% vs -12.84% / QDII限购加码·易方达降至10元 / 富国换帅</div>
          <div class="timeline-desc">首批26只浮费基金运作满一年，华商致远回报A成"三倍基"，鹏华共赢未来A亏损-12.84%，首尾相差329个百分点。QDII限购力度再加码，易方达全球成长精选降至10元。富国基金公告董事长裴长江退休，王苏龙接棒。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-22（FOF破峰值·中小基金公司差异化发展）</div>
          <div class="timeline-title">FOF年内新发规模1137亿·超越2021年峰值 / 证监会支持中小基金公司差异化发展</div>
          <div class="timeline-desc">Wind数据显示，截至6月20日，2026年以来新成立FOF基金达88只，合计发行规模高达1137.69亿元，超越2021年创下的历史峰值。证监会宣布推出支持中小基金公司规范健康发展一揽子措施。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-20（央行5000亿MLF·A股缩量5200亿）</div>
          <div class="timeline-title">央行6/20开展5000亿MLF操作·净投放2000亿 / A股成交额缩至5200亿</div>
          <div class="timeline-desc">央行开展5000亿元1年期MLF操作，净投放2000亿元，应对季末流动性压力。A股成交额缩至5200亿，市场观望情绪浓厚。美股同日因中东局势缓和大幅反弹，纳指+793点。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-18（2026陆家嘴论坛·吴清致辞）</div>
          <div class="timeline-title">2026陆家嘴论坛开幕·证监会主席吴清致辞·支持中小基金公司差异化发展</div>
          <div class="timeline-desc">2026陆家嘴论坛在上海开幕，证监会主席吴清发表致辞，宣布推出支持中小基金公司规范健康发展一揽子措施，坚持分类监管、突出特色。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-17（主动ETF指引落地·债券ETF规模突破）</div>
          <div class="timeline-title">沪深交易所发布主动ETF业务指引 / 债券ETF规模首超8500亿元（同比+180%）</div>
          <div class="timeline-desc">沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。同日，债券ETF总规模首次突破8500亿元，同比增长超180%。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-15（多项公募新规落地·A股普涨科技收敛）</div>
          <div class="timeline-title">主题投资风格管理指引+适当性细则修订+公私兼任禁令三文同落 / A股沪指4096(+1.61%)普涨</div>
          <div class="timeline-desc">多项公募基金新规同日公布：主题投资风格管理指引（12/1施行）将风格漂移软约束转为硬约束；适当性细则修订加强65周岁以上高风险基金销售管理；公私兼任禁令防范利益冲突。</div>
        </div>
      </div>

    </div>
  </div>'''

# --- Stats Bar 新内容（基于6月26日数据）---
STATS_NEW = '''  <div class="stats-bar">
    <div class="stat-item primary">
      <div class="stat-value">38.93万亿</div>
      <div class="stat-label">公募总规模（2026Q1·最新）</div>
    </div>
    <div class="stat-item success">
      <div class="stat-value">4027.26</div>
      <div class="stat-label">沪指最近收盘（06-26·-2.26%）</div>
    </div>
    <div class="stat-item warning">
      <div class="stat-value">175%</div>
      <div class="stat-label">基金中考最高收益（倒计时2天）</div>
    </div>
    <div class="stat-item danger">
      <div class="stat-value">2天</div>
      <div class="stat-label">公募基金中考收官倒计时</div>
    </div>
  </div>'''

# --- Header 日期区间 ---
HEADER_DATE_NEW = f'<div class="date-badge">📅 数据区间：2026.06.15 — 2026.06.29（今日自动更新）</div>'

# --- Meta 标签更新 ---
META_NEW = '<meta name="viewport" content="公募基准改革|翻倍基限购|基金中考175%|A股-2.26%">'
CONTENT_FP_NEW = '<meta name="content-fingerprint" content="基准改革全面铺开|翻倍基限购|中考175%|A股-2.26%">'


def do_update():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    print(f"原始文件长度: {original_len} 字符")

    # 1. 替换 S0 今日焦点（从 Section 0 标记到 Section 1 标记之前）
    s0_start = content.find('<!-- ============ Section 0: 今日焦点 ============ -->')
    s1_start = content.find('<!-- ============ Section 1: 重磅信息 ============ -->')
    if s0_start == -1:
        print("ERROR: 找不到 Section 0 标记")
        return False
    if s1_start == -1:
        print("ERROR: 找不到 Section 1 标记")
        return False

    content = content[:s0_start] + S0_NEW + '\n' + content[s1_start:]
    print(f"✅ S0 今日焦点 已更新")

    # 2. 替换 S6 市场行情
    s6_start = content.find('<!-- ============ Section 6: 市场行情速览 ============ -->')
    s7_start = content.find('<!-- ============ Section 7: 关键时间线 ============ -->')
    if s6_start == -1:
        print("ERROR: 找不到 Section 6 标记")
        return False
    if s7_start == -1:
        print("ERROR: 找不到 Section 7 标记")
        return False

    content = content[:s6_start] + S6_NEW + '\n' + content[s7_start:]
    print(f"✅ S6 市场行情 已更新")

    # 3. 替换 S7 时间线
    # 重新找 s7_start（因为内容已经变化）
    s7_start = content.find('<!-- ============ Section 7: 关键时间线 ============ -->')
    s8_start = content.find('<!-- ============ Section 8: 待办跟踪 ============ -->')
    if s7_start == -1:
        print("ERROR: 找不到 Section 7 标记（第二次）")
        return False
    if s8_start == -1:
        print("ERROR: 找不到 Section 8 标记")
        return False

    content = content[:s7_start] + S7_NEW + '\n' + content[s8_start:]
    print(f"✅ S7 时间线 已更新")

    # 4. 替换 Stats Bar
    stats_start = content.find('<div class="stats-bar">')
    if stats_start != -1:
        stats_end = content.find('</div>', stats_start + 100)  # 找到 stats-bar 的结束
        # 找第二个 </div> 因为 stats-bar 有多个子 div
        temp = content[stats_start:]
        second_div = temp.find('</div>', temp.find('</div>') + 1)
        if second_div != -1:
            stats_end = stats_start + second_div + 6  # +6 for '</div>'
            content = content[:stats_start] + STATS_NEW + content[stats_end:]
            print(f"✅ Stats Bar 已更新")
        else:
            print("WARNING: 找不到 Stats Bar 结束标记")
    else:
        print("WARNING: 找不到 Stats Bar 开始标记")

    # 5. 替换 Header 日期区间
    header_old = re.search(r'<div class="date-badge">📅 数据区间：[^<]+</div>', content)
    if header_old:
        content = content.replace(header_old.group(0), HEADER_DATE_NEW)
        print(f"✅ Header 日期区间 已更新")
    else:
        print("WARNING: 找不到 Header 日期区间")

    # 6. 替换 Meta 标签
    if 'content-fingerprint' in content:
        content = re.sub(r'<meta name="viewport" content="[^"]*">', META_NEW, content)
        content = re.sub(r'<meta name="content-fingerprint" content="[^"]*">', CONTENT_FP_NEW, content)
        print(f"✅ Meta 标签 已更新")

    # 7. 替换 daily-update 标记
    content = re.sub(r'<!-- daily-update: [^ ]+ -->', f'<!-- daily-update: {TODAY} -->', content)
    print(f"✅ daily-update 标记 已更新为 {TODAY}")

    # 写回文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ 所有更新完成！新文件长度: {len(content)} 字符")
    return True


if __name__ == '__main__':
    import os
    # 确保在正确目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"工作目录: {os.getcwd()}")
    success = do_update()
    if success:
        print("\n🎉 兜底更新成功！")
    else:
        print("\n❌ 兜底更新失败！")
        exit(1)
