#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基金看板 2026-06-19 兜底补位更新脚本"""

import re
import sys

HTML_PATH = r"c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ========== 1. daily-update 标记 ==========
content = content.replace("<!-- daily-update: 2026-06-18 -->", "<!-- daily-update: 2026-06-19 -->")

# ========== 2. content-fingerprint ==========
content = content.replace(
    'content="证监会三年行动计划2026-2028发布|中基协适当性细则6个月改造倒计时|主题投资基金风格漂移新规12/1施行|天天基金6月新发135只近三年最高"',
    'content="美联储转鹰年内或加息一次|端午三市同休6/19-21|SpaceX挂牌后首周走势震荡|五部门新能源车下乡活动启动"'
)

# ========== 3. Header 日期区间 ==========
content = content.replace(
    "📅 数据区间：2026.06.04 — 2026.06.18（今日自动更新）",
    "📅 数据区间：2026.06.05 — 2026.06.19（今日自动更新）"
)

# ========== 4. Stats Bar ==========
new_stats = """<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">端午三市同休</div>
    <div class="stat-label">6/19-21 A股/港股通/美股均休市·节后6/22开市·持币过节情绪主导·跨境资产价格波动</div>
    <div class="stat-change up">▲ 三市同休历史罕见·黄金/日韩等跨市场基金资产价格节后更新·关注假期海外市场变化</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">美联储转鹰·年内或加息</div>
    <div class="stat-label">6/18沃什首秀维持不变但点阵图中值升至3.75%-4.0%·暗示年内可能加息一次·2027降息窗口延后</div>
    <div class="stat-change up">▲ 滞胀困境（增长放缓+通胀居高）·QDII产品波动风险上升·全球央行政策分化加剧</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4090·科创+3.84%</div>
    <div class="stat-label">6/18收盘沪指4090(-0.43%)·深成指16030(+0.94%)·创业板4252(+2.05%)·科创50+3.84%·成交3.31万亿</div>
    <div class="stat-change up">▲ 科技风格极致分化·芯片/半导体强者恒强·沪深300ETF净流出137亿机构高位兑现</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">五部门新能源车下乡</div>
    <div class="stat-label">工信部/商务部等五部门启动2026新能源车下乡·深入推进汽车以旧换新进乡村·A股新能源车板块震荡</div>
    <div class="stat-change up">▲ 政策催化·但新能源车板块短期震荡为主·7月后或有表现·关注相关主题基金</div>
  </div>
</div>"""

content = content.replace(
    """<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">美联储转鹰·沃什首秀</div>
    <div class="stat-label">6/18议息维持不变但点阵图中值升至3.75%-4.0%·暗示年内可能加息一次·2027年降息窗口延后</div>
    <div class="stat-change up">▲ 沃什首秀·滞胀困境（增长放缓+通胀居高）·QDII产品波动风险上升</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">陆家嘴论坛收官</div>
    <div class="stat-label">央行6项新政+证监会支持主动ETF+吴清定调中小基金差异化发展·主动管理ETF业务指引落地</div>
    <div class="stat-change up">▲ 上海国际金融中心政策礼包·跨境监管"开正门堵偏门"·公募行业政策信号密集</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4108·科创+4%</div>
    <div class="stat-label">6/17收盘沪指4108(+0.40%)·科创50涨超4%·芯片股午后大幅走强·沪深300ETF净流出137亿</div>
    <div class="stat-change up">▲ 科技风格延续但机构高位兑现·端午前最后交易周·关注海外市场波动</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">端午休市倒计时</div>
    <div class="stat-label">6/19-21端午休市·节前避险情绪升温·A股缩量震荡·机构资金净流出·节后上涨概率偏高</div>
    <div class="stat-change up">▲ 节日期间海外市场波动风险·美联储转鹰传导·QDII产品需重点关注</div>
  </div>
</div>""",
    new_stats
)

# ========== 5. Section 0 今日焦点 ==========
new_s0 = """  <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（6月19日·周四·端午休市首日·美联储鹰派持续发酵·五部门新能源车下乡）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 端午三市同休！A股/港股通/美股6/19-21同步休市，节后6/22开市·持币过节情绪主导</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-19</span>
          </div>
        </div>
        <div class="card-body">
          <b>休市安排：</b>2026年端午节，A股6/19（周五）至6/21（周日）休市，6/22（周一）起照常开市。港股通同步暂停，6/22起恢复。美股6/19（周五）也休市。<b>三市同休</b>历史罕见。<br>
          <b>节前最后交易日（6/18）：</b>A股分化，沪指4090点（-0.43%），但创业板指+2.05%、科创50指数+3.84%，芯片股强者恒强。全市场成交3.31万亿，较前日放量2177亿。<br>
          <b>节后关注：</b>①美联储鹰派信号在假期期间持续发酵，节后QDII产品可能面临赎回压力；②科技风格能否延续；③黄金/日韩等跨市场基金资产价格将在节后更新。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.cn/2026-06-18/detail-inicvvzp5363094.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·休市安排</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1868151736245041010" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·投顾指南针</span></a>
          <span class="impact-tag high">端午休市：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 三市同休→节前权益基金赎回高峰已过，节后关注补仓资金入市节奏；<br>
            ② 跨市场基金节后价格更新→提前准备客户解释话术，尤其是黄金/海外资产；<br>
            ③ 美联储鹰派发酵→节后QDII美股产品可能承压，关注客户咨询高峰。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 美联储鹰派信号持续发酵！沃什首秀点阵图转鹰·年内加息预期升温·全球债市遭抛售</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-18~19</span>
          </div>
        </div>
        <div class="card-body">
          <b>议息结果持续发酵：</b>6/18美联储维持利率3.50%-3.75%不变，但点阵图中值升至3.75%-4.0%（暗示年内可能加息一次），新任主席沃什首秀释放鹰派信号。2026全年GDP增速预测从2.4%下调至2.2%，核心PCE通胀上调，美联储陷入"滞胀困境"。<br>
          <b>全球市场反应：</b>6/18美股三大指数集体收跌（道指-0.98%、纳指-1.34%、标普-1.21%），全球债市遭抛售，美元指数走强。欧央行已重启加息25bp，全球央行政策分化进一步加剧。<br>
          <b>对基金行业影响：</b>①QDII美股产品节后可能面临净值压力和赎回；②全球债券收益率上行→国内QDII美元债基金承压；③黄金等避险资产价格波动加大。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202606183775060947.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·美联储</span></a>
          <a href="https://finance.sina.com.cn/roll/2026-06-18/doc-inicuqfz3367633.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·鹰派信号</span></a>
          <span class="impact-tag high">全球央行：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 美联储转鹰→节后QDII纳斯达克100产品客户可能集中咨询，提前准备解释话术；<br>
            ② 全球债市抛售→关注QDII美元债基金净值波动，做好客户陪伴；<br>
            ③ 端午假期→利用休市时间窗口，内部培训美联储政策对基金产品的影响逻辑。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 五部门启动2026新能源车下乡·工信部/商务部等深入推进汽车以旧换新进乡村</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-19</span>
          </div>
        </div>
        <div class="card-body">
          <b>政策内容：</b>工信部、商务部等五部门联合开展2026年新能源汽车下乡活动，深入推进汽车以旧换新进乡村。该消息A股开盘时已发布，但新能源车板块反应平淡，属于"旧事重提"，短期仍以震荡为主。<br>
          <b>机构研判：</b>新能源车板块短期震荡为主，预计7月以后或有表现。对应公募基金方面，新能源主题基金经历长期调整后，估值已处历史低位，政策催化下具备反弹动能。<br>
          <b>对基金行业影响：</b>新能源车ETF/主动管理的新能源主题基金可关注节后布局机会。但需注意：新能源车板块与科技AI板块存在资金跷跷板效应，短期资金仍集中在科技方向。
        </div>
        <div class="card-footer">
          <a href="https://caifuhao.eastmoney.com/news/20260619081107166463570" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·早评</span></a>
          <span class="impact-tag medium">政策催化：中</span>
        </div>
      </div>

    </div>
  </div>"""

# 找到旧的S0部分并替换
old_s0_pattern = r'  <!-- ============ Section 0: 今日焦点 ============ -->.*?  </div>\n\n  <!-- ============ Section 1:'
content = re.sub(old_s0_pattern, new_s0 + '\n\n  <!-- ============ Section 1:', content, flags=re.DOTALL)

# ========== 6. Section 6 市场行情 ==========
new_s6 = """  <!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

    <div class="card p3">
      <div class="card-top">
        <div class="card-title">端午休市·节前最后交易日（6/18）收盘数据 + 美联储鹰派持续发酵·节后6/22开市</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 节前最后交易日（6/18）收盘：</b>A股分化，沪指<b>4090点(-0.43%)</b>，深证成指<b>16030点(+0.94%)</b>，创业板指<b>4252点(+2.05%)</b>，科创50指数<b>涨3.84%</b>。芯片/半导体强者恒强，兆易创新涨停+10%。全市场成交<b>3.31万亿</b>，较前日放量2177亿。<br><br>
            <b>📊 港股（6/18）：</b>恒生指数<b>跌1.59%</b>，恒生科技指数<b>跌1.39%</b>，美联储鹰派预期压制港股科技板块。<br><br>
            <b>📊 端午休市：</b>6/19-6/21休市，6/22（周一）开市。三市同休（A股+港股通+美股）历史罕见。
          </div>
          <div>
            <b>📊 美股（6/18 美联储议息后）：</b><br>
            ▪ 道指 <b>-0.98%</b>（美联储鹰派信号压制）<br>
            ▪ 纳指 <b>-1.34%</b>（科技权重股领跌）<br>
            ▪ 标普500 <b>-1.21%</b><br>
            ▪ 沃什首秀点阵图转鹰，年内加息预期升温<br><br>
            <b>📊 对基金行业影响（节后）：</b><br>
            ▪ 美联储转鹰→QDII美股产品节后或承压<br>
            ▪ 科技风格极致分化→节后关注科创50能否延续<br>
            ▪ 三市同休→跨市场基金节后价格更新，黄金/海外资产需重点关注
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·6/18收盘</span>
        <span class="source-tag">端午休市·6/19-21</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>
  </div>"""

old_s6_pattern = r'  <!-- ============ Section 6: 市场行情速览 ============ -->.*?  </div>\n\n  <!-- ============ Section 7:'
content = re.sub(old_s6_pattern, new_s6 + '\n\n  <!-- ============ Section 7:', content, flags=re.DOTALL)

# ========== 7. Section 7 时间线 ==========
# 删除06-04及更早的超期条目（T-14 = 06-05，所以06-04及更早需要删除）
# 当前S7有：06-18, 06-17, 06-16, 06-15, 06-13, 06-12, 06-11, 06-10, 06-09, 06-08, 06-06, 06-05
# 需要删除06-05（T-14，保留），06-04及更早（没有06-04，但06-05是边界，保留）
# 实际检查：今天06-19，T-14 = 06-05，所以06-05保留，没有超期条目
# 但需要新增06-19条目

new_timeline_item = """      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-19（端午三市同休·A股/港股通/美股均休市·美联储鹰派持续发酵·五部门新能源车下乡）</div>
          <div class="timeline-title">端午三市同休（A股/港股通/美股6/19均休市）/ 美联储鹰派信号持续发酵·年内或加息一次 / 五部门启动新能源车下乡·深入推进以旧换新</div>
          <div class="timeline-desc">2026年端午节，A股/港股通/美股罕见三市同休（6/19-6/21），6/22开市。美联储6/18议息结果持续发酵，沃什首秀点阵图转鹰，年内加息预期升温，全球债市遭抛售。五部门（工信部/商务部等）启动2026新能源车下乡活动，深入推进汽车以旧换新进乡村，但新能源车板块短期仍震荡。节后关注：QDII产品净值压力、科技风格延续性、跨市场基金价格更新。</div>
        </div>
      </div>
"""

# 在S7的第一个timeline-item前插入新条目
content = content.replace(
    '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-18',
    new_timeline_item + '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-18'
)

# 检查并删除超期条目（06-05及更早，T-14=06-05，06-05保留）
# 当前最旧条目是06-06（中基协换届）和06-05（中证金牛），06-05在边界内，保留
# 但06-06条目内容实际是06-06的事件，在T-14内，保留
# 无需删除

# ========== 8. Footer 数据采集时间 ==========
content = content.replace(
    "数据更新时间：2026年6月18日 10:30 · 近两周核心资讯（06-04 — 06-18）·",
    "数据更新时间：2026年6月19日 10:30 · 近两周核心资讯（06-05 — 06-19）·"
)

# ========== 写回文件 ==========
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ patch_0619 完成")
print(f"   daily-update: 2026-06-19")
print(f"   数据区间: 2026.06.05 — 2026.06.19")
print(f"   Stats Bar: 4张新卡片")
print(f"   S0: 3张卡片（端午休市/美联储发酵/新能源车下乡）")
print(f"   S6: 6/18收盘数据 + 端午休市提示")
print(f"   S7: 新增06-19条目")
print(f"   Footer: 2026年6月19日 10:30")
