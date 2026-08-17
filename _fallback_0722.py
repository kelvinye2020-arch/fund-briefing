# -*- coding: utf-8 -*-
import re, sys

PATH = r"c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"
s = open(PATH, encoding="utf-8").read()

# ---------- Phase 1: all asserts ----------
def must(cond, msg):
    if not cond:
        print("ANCHOR FAIL: " + msg)
        sys.exit(1)

# required 6 anchors (each exactly once)
must(s.count("<!-- daily-update: 2026-07-21 -->") == 1, "daily-update marker")
must(s.count("<!-- ============ Section 1: 重磅信息 ============ -->") == 1, "Section1 boundary")
must(s.count("<!-- ============ Section 7: 关键时间线 ============ -->") == 1, "Section7 boundary")
must(s.count("                    <!-- S0 Card 1:") == 1, "S0 Card 1")
must(s.count("      <!-- 07-21 时间线条目 (NEW) -->") == 1, "07-21 timeline entry")
must(s.count('      <div class="stat-label">上证综指 · 07-21深V反转+1.39%·双创领涨·科创50+9.01%·半导体深V反弹</div>') == 1, "Stats 上证综指 card")

# extra anchors
must(s.count('<meta name="viewport" content="首批18只主动ETF获证监会接收|A股07-21深V反转双创领涨|宽基ETF单日净流入590亿次新高|证监会座谈会规范量化与AI|绩优基金松绑限购+自购">') == 1, "meta viewport fp")
must(s.count('<meta name="content-fingerprint" content="首批18只主动ETF获证监会接收|A股07-21深V反转双创领涨|宽基ETF单日净流入590亿次新高|证监会座谈会规范量化与AI|绩优基金松绑限购+自购">') == 1, "meta fingerprint")
must(s.count('    <div class="date-badge">📅 数据区间：2026.07.07 — 2026.07.21（每日更新）</div>') == 1, "header date-badge")
must(s.count('      <span class="section-title">今日焦点（7月21日·周二·首批18只主动ETF获证监会接收·证监会座谈会规范量化与AI·宽基ETF单日净流入590亿·绩优基金松绑限购）</span>') == 1, "S0 title")
must(s.count('      <!-- 07-07 时间线条目 (NEW) -->') == 1, "07-07 timeline entry")

# regex-anchored big blocks
pat_s0 = re.compile(r'                    <!-- S0 Card 1: A股07-21深V反转·双创领涨 \(T\+0 07-21 P1\) -->.*?\n    </div>\n  </div>\n<!-- ============ Section 1: 重磅信息 ============ -->', re.DOTALL)
pat_s6 = re.compile(r'          <div class="card p3">\n        <div class="card-top">\n          <div class="card-title">2026年7月21日（周二·盘中）·A股深V反转·沪指\+1\.39%·创业板\+6\.46%·科创50\+9\.01%领涨</div>.*?\n      </div>\n  </div>\n<!-- ============ Section 7: 关键时间线 ============ -->', re.DOTALL)
must(pat_s0.search(s) is not None, "S0 block regex match")
must(pat_s6.search(s) is not None, "S6 block regex match")

# div balance snapshot
div_open0 = s.count("<div")
div_close0 = s.count("</div>")
must(div_open0 == div_close0, "div balance before (open=%d close=%d)" % (div_open0, div_close0))

print("ALL ASSERTS PASSED (div %d/%d)" % (div_open0, div_close0))

# ---------- Phase 2: replacements ----------
OLD_FP = "首批18只主动ETF获证监会接收|A股07-21深V反转双创领涨|宽基ETF单日净流入590亿次新高|证监会座谈会规范量化与AI|绩优基金松绑限购+自购"
NEW_FP = "二季度公募规模近40万亿|公募十大重仓股洗牌中际旭创登顶|超3000亿股票ETF逆市抄底|创新药主题基金规模破1500亿|A股07-21深V反弹双创领涨"

s = s.replace("<!-- daily-update: 2026-07-21 -->", "<!-- daily-update: 2026-07-22 -->")
s = s.replace('<meta name="viewport" content="%s">' % OLD_FP, '<meta name="viewport" content="%s">' % NEW_FP)
s = s.replace('<meta name="content-fingerprint" content="%s">' % OLD_FP, '<meta name="content-fingerprint" content="%s">' % NEW_FP)
s = s.replace('    <div class="date-badge">📅 数据区间：2026.07.07 — 2026.07.21（每日更新）</div>',
              '    <div class="date-badge">📅 数据区间：2026.07.08 — 2026.07.22（每日更新）</div>')
s = s.replace('      <span class="section-title">今日焦点（7月21日·周二·首批18只主动ETF获证监会接收·证监会座谈会规范量化与AI·宽基ETF单日净流入590亿·绩优基金松绑限购）</span>',
              '      <span class="section-title">今日焦点（7月22日·周三·二季度公募规模近40万亿·重仓股洗牌中际旭创登顶·超3000亿股票ETF逆市抄底·创新药主题基金破1500亿）</span>')

# S0 four cards (replace whole block up to Section1 comment)
new_s0 = '''                    <!-- S0 Card 1: 二季度公募规模近40万亿 (T+0 07-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 二季度公募规模大增·距40万亿元仅一步之遥·主动管理类增幅最大</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模新高：</b>财联社7月22日报道，2026年二季度公募基金管理规模显著增长，距离40万亿元仅一步之遥；主动管理类产品凭借亮眼业绩成为二季度增幅最大品类，绩优产品"吸金"显著。<br>
          <b>结构转型：</b>业内人士指出，公募基金行业在规模快速扩张的同时，正从"量的增长"向"质的提升"转型，主动权益与绩优策略受资金青睐。<br>
          <b>对基金行业影响：</b>规模逼近40万亿印证居民资金持续入市，腾安可借势强化"长期持有、优中选优"配置主线，引导客户关注主动管理能力。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?doc-id=70000021_6416a5ff4d050752" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·上证报</span></a>
          <span class="impact-tag medium">行业规模：中</span>
        </div>
      </div>
    <!-- S0 Card 2: 公募十大重仓股洗牌·中际旭创登顶 (T+0 07-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露完毕·十大重仓股大洗牌·中际旭创跃居第一重仓股</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>持仓总览：</b>天相投顾数据显示，截至2026年二季度末公募基金股票持仓总市值88354亿元，较一季度增加7745亿元、涨幅9.60%；二季报已于7月21日基本披露完毕。<br>
          <b>重仓洗牌：</b>中际旭创二季度末持股总市值大增1306亿元至2619亿元、跃居第一重仓股，宁德时代退居第四（此前连续6个报告期居首）；新十大重仓依次为中际旭创、新易盛、东山精密、寒武纪、宁德时代、北方华创、兆易创新、源杰科技、中微公司、三环集团。<br>
          <b>对基金行业影响：</b>AI算力链（光模块/半导体）成为公募共识底仓，腾安可借重仓变迁优化科技成长货架与投教话术。
        </div>
        <div class="card-footer">
          <a href="https://www.sohu.com/a/1053178049_120109837" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">搜狐·立方早知道</span></a>
          <span class="impact-tag medium">持仓风向：中</span>
        </div>
      </div>
    <!-- S0 Card 3: 超3000亿股票ETF逆市抄底 (T+0 07-22 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 超3000亿股票ETF逆市抄底·连续11日净流入·单周2036亿破纪录</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>资金风向：</b>Choice数据显示，截至7月20日全市场股票ETF已连续11个交易日获资金流入，区间累计净流入达3567亿元；其中7月17日单日净流入758.67亿元，为历史单日净流入规模第三高。<br>
          <b>单周破纪录：</b>仅上周股票型ETF合计净流入便突破2036亿元，刷新历史单周最高纪录，宽基ETF毫无悬念占据主导地位。<br>
          <b>对基金行业影响：</b>增量资金借道ETF强势抄底特征明显，叠加A股07-21深V反弹（科创50+10.73%），客户风险偏好快速回升，腾安需做好承接与理性引导。
        </div>
        <div class="card-footer">
          <a href="https://xueqiu.com/1474197611/401517473" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">雪球·Choice财经早班车</span></a>
          <span class="impact-tag high">ETF资金：高</span>
        </div>
        <div class="action-box">
          <b>⚡ 腾安行动建议：</b>股票ETF连续11日净流入超3500亿、单周破2000亿纪录，显示散户与机构借道ETF强势抄底；叠加A股深V反弹，客户风险偏好快速回升。<b>①</b> 借势引导客户关注宽基/科技ETF定投，但提示"深V后勿盲目追高、分批布局"；<b>②</b> 对前期被套科技成长客户做好安抚与再平衡沟通；<b>③</b> 提前储备ETF投教话术与货架，承接增量资金。
        </div>
      </div>
    <!-- S0 Card 4: 创新药主题基金规模破1500亿 (T+0 07-22 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 创新药主题基金总规模突破1500亿元·月内净值全部走高</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模跃升：</b>Wind数据显示，截至7月20日64只创新药主题基金月内净值全部走高，总规模已突破1500亿元，较月初增长逾180亿元。<br>
          <b>结构分化：</b>港股通创新药ETF整体涨幅居前，科创板创新药ETF表现相对滞后；分析认为创新药板块受流动性改善及政策预期提振，但不同指数编制方案及底层资产差异或致产品业绩分化。<br>
          <b>对基金行业影响：</b>创新药主线景气延续，腾安可丰富医药主题货架并强化风险提示，引导客户关注长期产业逻辑。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?doc-id=70000021_0506a6009c534552" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">主题规模：中</span>
        </div>
      </div>
    </div>
  </div>
<!-- ============ Section 1: 重磅信息 ============ -->'''
s = pat_s0.sub(new_s0, s, count=1)

# S6 market card (07-21 close data)
new_s6 = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月21日（周二·收盘）·A股深V强势反弹·沪指+1.79%·创业板+7.05%·科创50+10.73%领涨</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股07-21收盘（深V反弹·双创领涨）：</b><br>
              ▪ 沪指 <b>+1.79%</b>（3864.37）·深成指 <b>+4.81%</b>（14264.29）<br>
              ▪ 创业板指 <b>+7.05%</b>（3685.97）·科创50 <b>+10.73%</b>（1903.16）<br>
              ▪ 早盘探底翻绿后10:10拉升，半导体/芯片/光通信领涨；两市成交2.97万亿
            </div>
            <div>
              <b>📉 港股07-21收盘（微跌）：</b><br>
              ▪ 恒指 <b>-0.04%</b>（25132.29）·恒生科技 <b>+1.32%</b>（4814.83）·国企指数-0.25%<br>
              <b>📉 美股07-21收盘（全线收涨）：</b>道指+0.74%（52224.64）·标普+0.89%（7509.20）·纳指+1.29%（25837.21）；费城半导体+5.21%芯片反弹
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：A股深V强势反弹、政策资金共振（国资增持+险资加大配置+证监会积极表态），机构称急跌阶段大概率已过；股票ETF连续11日净流入超3500亿、单周破2000亿纪录；公募二季报披露完毕，中际旭创跃居第一大重仓股。
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-22（周二收盘）</span>
            <span class="source-tag">数据来源：新浪财经/同花顺/港交所/东方财富</span>
          </div>
      </div>
  </div>
<!-- ============ Section 7: 关键时间线 ============ -->'''
s = pat_s6.sub(new_s6, s, count=1)

# S7 timeline: remove 07-07 (exceeds T-14), insert 07-22 at top
old_0707 = '      <!-- 07-07 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-07</div>\n        <div class="timeline-title">A股三大指数集体低开·半导体芯片领跌</div>\n      </div>\n'
must(old_0707 in s, "07-07 block exact match")
s = s.replace(old_0707, "")
s = s.replace('      <!-- 07-21 时间线条目 (NEW) -->',
              '      <!-- 07-22 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-22</div>\n        <div class="timeline-title">二季度公募规模近40万亿·重仓股洗牌中际旭创登顶</div>\n      </div>\n\n      <!-- 07-21 时间线条目 (NEW) -->')

# Stats Bar 上证综指 card
old_stats = '    <div class="stat-card">\n      <div class="stat-number">3849.22</div>\n      <div class="stat-label">上证综指 · 07-21深V反转+1.39%·双创领涨·科创50+9.01%·半导体深V反弹</div>\n      <div class="stat-change up">▲ A股深V反转·政策资金共振·机构"力挺"称牛市中调整</div>\n    </div>'
new_stats = '    <div class="stat-card">\n      <div class="stat-number">3864.37</div>\n      <div class="stat-label">上证综指 · 07-21收盘+1.79%·深V反转·创业板+7.05%·科创50+10.73%</div>\n      <div class="stat-change up">▲ A股深V强势反弹·政策资金共振·增量资金借道ETF抄底</div>\n    </div>'
must(old_stats in s, "Stats 上证综指 block exact match")
s = s.replace(old_stats, new_stats)

# ---------- Phase 2 verification ----------
must(s.count("<!-- daily-update: 2026-07-22 -->") == 1, "new marker present")
must(s.count("<!-- daily-update: 2026-07-21 -->") == 0, "old marker gone")
must(pat_s0.search(s) is None, "old S0 block gone")
must(pat_s6.search(s) is None, "old S6 block gone")
must(s.count('      <!-- 07-07 时间线条目 (NEW) -->') == 0, "07-07 removed")
must(s.count('      <!-- 07-22 时间线条目 (NEW) -->') == 1, "07-22 added")
# no S8 residual
must("Section 8" not in s, "no S8 section")
must("腾安行动清单" not in s, "no S8 residual")
# S0 date-tags all 07-22
s0_region = s.split("<!-- ============ Section 1:")[0]
must(s0_region.count('date-tag">07-22<') == 4, "S0 has 4 date-tags 07-22 (got %d)" % s0_region.count('date-tag">07-22<'))
must(s0_region.count('date-tag">07-2') == 4, "S0 no other date-tags")
# div balance unchanged
div_open1 = s.count("<div")
div_close1 = s.count("</div>")
must(div_open1 == div_close1, "div balance after (open=%d close=%d)" % (div_open1, div_close1))

open(PATH, "w", encoding="utf-8").write(s)
print("SUCCESS: fallback write complete (div %d/%d)" % (div_open1, div_close1))
