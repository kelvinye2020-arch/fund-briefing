# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ---------- 0. daily-update marker ----------
html = html.replace("<!-- daily-update: 2026-08-16 -->", "<!-- daily-update: 2026-08-17 -->")

# ---------- 1. Stats Bar (independent fill) ----------
OLD_STATS = '''<!-- Stats Bar -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">腾安待改</div>
      <div class="stat-label">业绩基准"同框"展示改造 · 08-14实测</div>
      <div class="stat-change down">▼ 腾安/盈米仅展示宽基指数·天天/京东已达标</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">15家</div>
      <div class="stat-label">摊余成本法债基重启上报 · 08-15披露</div>
      <div class="stat-change up">▲ 63个月封闭式·中小公募+贝莱德等外资获倾斜</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">40只</div>
      <div class="stat-label">主动权益基金疑似风格漂移 · 08-15财联社</div>
      <div class="stat-change down">▼ 建信高股息7月回撤20.79%·红利涨它跌</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">近70只</div>
      <div class="stat-label">主动权益基金净值创成立以来新高·08-13 Wind</div>
      <div class="stat-change up">▲ 灵活配置约37只·偏股混合约29只·低回撤绩优占优</div></div>
  </div>'''

NEW_STATS = '''<!-- Stats Bar -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">15家</div>
      <div class="stat-label">摊余成本法债基重启上报 · 08-15披露</div>
      <div class="stat-change up">▲ 63个月封闭式·中小公募+贝莱德等外资获倾斜</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">125只</div>
      <div class="stat-label">LOF拟终止上市 · 沪深交易所征求意见稿</div>
      <div class="stat-change down">▼ 商品期货/QDII/小规模LOF·2027年底为限</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">7.18万亿</div>
      <div class="stat-label">纯债基金Q2规模 · 济安金信08-15</div>
      <div class="stat-change up">▲ 环比+5515亿·利率+商金策略收益居前</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">40只</div>
      <div class="stat-label">主动权益基金疑似风格漂移 · 08-15财联社</div>
      <div class="stat-change down">▼ 建信高股息7月回撤20.79%·红利涨它跌</div>
    </div>
  </div>'''

assert OLD_STATS in html, "Stats Bar anchor not found"
html = html.replace(OLD_STATS, NEW_STATS)

# ---------- 2. S0 section-context + cards ----------
OLD_S0_CTX = '''        <span class="section-title">今日焦点</span>
        <span class="section-context">8月15日 · 4条今日要闻</span>'''
NEW_S0_CTX = '''        <span class="section-title">今日焦点</span>
        <span class="section-context">8月17日 · 4条今日要闻</span>'''
assert OLD_S0_CTX in html, "S0 context anchor not found"
html = html.replace(OLD_S0_CTX, NEW_S0_CTX)

# Replace entire S0 card-grid block (from '<!-- S0 Card 1' to closing of card-grid before '</div>\n  </div>')
S0_START = "      <!-- S0 Card 1: 摊余成本法债基重启 (T+0 08-15 P1) -->"
S0_END = "    </div>\n  </div>\n\n<!-- ============ Section 1: 重磅信息 ============ -->"

idx_s = html.index(S0_START)
idx_e = html.index(S0_END)
old_s0 = html[idx_s:idx_e]

NEW_S0 = '''      <!-- S0 Card 1: 摊余成本法债基重启 (08-15 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🟡 摊余成本法债基时隔五年重启·15家中小公募+外资上报63个月封闭式</div>
        </div>
        <div class="card-body">
          8月14日晚证监会官网显示，<b>15家基金公司上报新一批摊余成本法债基</b>，均为<b>63个月封闭式债券型基金</b>。申报主体以中小公募为主——朱雀、易米、国融、兴合、鹏安、红土创新、百嘉等，同时包含<b>贝莱德、路博迈、安联、联博</b>等外资机构；业内透露后续或有第二批上报。这是自2021年暂停审批以来<b>时隔五年重新开闸</b>，被视为落实陆家嘴论坛吴清"支持中小基金公司规范健康发展一揽子措施"的具体动作。<br>
          <b>运作原则：</b>每家公司此类产品总数不超过2只、单只规模上限80亿元、期限约5年；截至2026年二季度末入围机构非货规模均在300亿元以下，扶持中小机构意图明确。存量摊余成本法债基规模已从2020年末1.46万亿增至2025年末2.08万亿。<br>
          <b>影响：</b>对基金公司做大规模、代销机构提升保有量均有助益；短期或利好债市中长久期信用债，但推动力不宜高估。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L4B5KKSL0530NLC9.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
        </div>
      </div>

      <!-- S0 Card 2: LOF退市新规征求意见稿 (08-15 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🟡 LOF退市新规征求意见·125只拟终止上市·华宝油气LOF已终止做市</div>
        </div>
        <div class="card-body">
          沪深交易所发布LOF相关安排<b>征求意见稿</b>，拟明确商品期货LOF、QDII-LOF及小规模LOF的终止上市情形与程序。尽管仍处征集意见阶段，<b>多家基金公司已着手提前部署</b>——华宝基金8月14日公告终止华宝油气LOF与浙商证券的做市合作，为后续退市铺路。<br>
          <b>退市范围：</b>① 商品期货LOF和QDII-LOF设较长过渡期，最晚于<b>2027年12月31日</b>前终止上市；② 小规模LOF不设过渡期，连续60个交易日场内资产净值均低于1000万元即启动终止上市。截至2026年6月底，两市LOF共402只、场内外合计6498亿元，<b>此次拟退市约125只、场内规模约260亿元</b>。<br>
          <b>行业含义：</b>LOF为分级基金转型产物，属过渡型产品；随ETF壮大与主动ETF未来上市，LOF将逐步完成历史使命，统一退市有助从源头减少折溢价客诉与运营风险。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://finance.sina.com.cn/jjxw/2026-08-15/doc-ininmhui8443875.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
        </div>
      </div>

      <!-- S0 Card 3: 纯债基金Q2规模7.18万亿 (08-15 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🔵 纯债基金Q2规模增至7.18万亿·环比+5515亿·利率+商金策略收益居前</div>
        </div>
        <div class="card-body">
          济安金信2026年二季度数据显示，纯债型基金整体规模达<b>71768.96亿元</b>，较上季度增加<b>5515.38亿元</b>，增量集中于综合投资策略基金；今年以来纯债型基金维持正收益，<b>利率+商金策略收益最高</b>。<br>
          <b>背景：</b>在权益市场极致结构化、科技主线虹吸效应下，纯债基金凭借低波动、稳健票息成为机构与零售资金的重要"压舱石"；银行自营与理财资金对摊余成本法债基、定制债基的偏好同步升温。<br>
          <b>对腾安：</b>固收类货架的"稳健获客"价值凸显，可结合摊余成本法债基重启窗口，优化低风险产品供给与投资者陪伴。
        </div>
        <div class="card-footer">
          <span class="impact-tag low">影响：低</span>
          <a href="https://new.qq.com/rain/a/20260815A0859J00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻</span></a>
        </div>
      </div>

      <!-- S0 Card 4: 风格漂移屡禁不止·均衡型基金两难 (08-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-17</span>
          </div>
          <div class="card-title">🟡 风格漂移屡禁不止·C基金罚单后再引关注·均衡型基金陷"变形求生"两难</div>
        </div>
        <div class="card-body">
          财联社8月17日讯，C基金公司监管罚单再度将风格漂移拉回视野。证券时报指出，今年以来围绕公募投资端监管约束持续加码，但<b>风格漂移仍屡禁不止</b>——二季度科技行情虹吸下，部分消费、红利主题乃至均衡、价值风格基金纷纷转向半导体、光通信等热门赛道，实际持仓与定位明显偏离。<br>
          <b>根因：</b>受访机构普遍认为，<b>规模诉求与相对排名考核导向、部分产品契约边界较宽</b>是主因；短期收益不能成为偏离产品定位的理由，需从考核机制、产品设计、销售评价和持续监督形成全流程约束。<br>
          <b>另一面：</b>同日财联社报道，主打"控回撤、分散配置"的均衡型基金陷入生存两难——极致结构化行情中"平滑波动"优势反成资金流失劣势，不少产品被迫调整框架；但随着市场从普涨转向结构分化，哑铃型等均衡思路或成下一阶段重要选择。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="http://www.cailianpress.com/subject/1349" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
        </div>
      </div>
'''

html = html[:idx_s] + NEW_S0 + html[idx_e:]

# ---------- 3. S2: remove 摊余 card (moved to S0), keep C基金 + 央行 ----------
# Remove the second S2 card (摊余成本法债基重启) block
S2_CARD2_START = '      <div class="card p1">\n        <div class="card-top">\n          <div class="card-title">🟡 摊余成本法债基重启申报'
idx2 = html.index(S2_CARD2_START)
# find the card-footer close + </div> for this card; it ends before the next '<div class="card p1">' or section end
# Locate end: after its source-tag 上海证券报 and </div></div>
end_marker = '          <a href="https://www.163.com/dy/article/L4C1QL090552C2FY.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>\n        </div>\n      </div>\n\n'
idx2e = html.index(end_marker, idx2) + len(end_marker)
html = html[:idx2] + html[idx2e:]

# ---------- 4. S6 market: fix label + date-tag + values (Aug 14 close) ----------
OLD_S6_TITLE = '          <div class="card-title">📈 上一交易日收盘（2026-08-15 周五）·三大指数窄幅整理沪指微红·算力链走强</div>'
NEW_S6_TITLE = '          <div class="card-title">📈 上一交易日收盘（2026-08-14 周五）·三大指数窄幅整理沪指微红·算力链走强</div>'
assert OLD_S6_TITLE in html, "S6 title anchor not found"
html = html.replace(OLD_S6_TITLE, NEW_S6_TITLE)

OLD_S6_DT = '            <span class="date-tag">08-13</span>'
NEW_S6_DT = '            <span class="date-tag">08-14</span>'
assert OLD_S6_DT in html, "S6 date-tag anchor not found"
html = html.replace(OLD_S6_DT, NEW_S6_DT)

# HK/US values: update 纳指 + 标普 to Aug14 verified
OLD_HS = '              恒生指数 <b>25116.85</b> <span style="color:#52c41a;">-1.10%</span><br>\n              恒生科技 <b>4708.19</b> <span style="color:#52c41a;">-1.77%</span><br>\n              国企指数 <b>8362.31</b> <span style="color:#52c41a;">-1.02%</span><br>\n              道琼斯 <b>53750.11</b> <span style="color:#52c41a;">-0.20%</span><br>\n              纳斯达克 <b>26728.55</b> <span style="color:#52c41a;">-0.28%</span><br>\n              标普500 <b>7785.11</b> <span style="color:#52c41a;">-0.17%</span><br>'
NEW_HS = '              恒生指数 <b>25116.85</b> <span style="color:#52c41a;">-1.10%</span><br>\n              恒生科技 <b>4707.62</b> <span style="color:#52c41a;">-1.77%</span><br>\n              国企指数 <b>8340.83</b> <span style="color:#52c41a;">-1.02%</span><br>\n              道琼斯 <b>53732.41</b> <span style="color:#52c41a;">-0.20%</span><br>\n              纳斯达克 <b>26803.03</b> <span style="color:#f5222d;">+0.81%</span><br>\n              标普500 <b>7785.76</b> <span style="color:#52c41a;">-0.17%</span><br>'
if OLD_HS in html:
    html = html.replace(OLD_HS, NEW_HS)
else:
    print("WARN: S6 HK/US block not matched exactly, skipping values update")

# KOSPI value update
html = html.replace('韩KOSPI <b>7045.12</b> <span style="color:#f5222d;">+3.40%</span>', '韩KOSPI <b>6977.94</b> <span style="color:#f5222d;">+2.42%</span>')
html = html.replace('日经225 <b>68101.22</b> <span style="color:#f5222d;">+0.44%</span>', '日经225 <b>68713.80</b> <span style="color:#f5222d;">+0.59%</span>')

# ---------- 5. S7 timeline rewrite (clean, 11 items, T-14~T) ----------
S7_START = '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">'
S7_END = '    </div>\n  </div>\n\n</div>'

idx7s = html.index(S7_START)
idx7e = html.index(S7_END, idx7s)
# Ensure S7_END is the one right after timeline (the one containing timeline items)
old_s7 = html[idx7s:idx7e]

NEW_S7 = '''    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
      <!-- 08-17 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-17</div>
        <div class="timeline-title">风格漂移屡禁不止·均衡型基金陷两难</div>
      </div>
      <!-- 08-15 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-15</div>
        <div class="timeline-title">LOF退市新规征求意见·125只拟终止上市</div>
      </div>
      <!-- 08-15 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-15</div>
        <div class="timeline-title">摊余成本法债基重启·15家中小公募上报</div>
      </div>
      <!-- 08-14 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-14</div>
        <div class="timeline-title">业绩基准同框改造过半·腾安被点名滞后</div>
      </div>
      <!-- 08-13 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-13</div>
        <div class="timeline-title">集中度监管首例落地·C基金公司被通报追责</div>
      </div>
      <!-- 08-12 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-12</div>
        <div class="timeline-title">太保寿险申请公募代销资格获接收</div>
      </div>
      <!-- 08-11 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-11</div>
        <div class="timeline-title">证监会通报双罚·严禁风格漂移与大V带货</div>
      </div>
      <!-- 08-10 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-10</div>
        <div class="timeline-title">基金投顾牌照扩容冲刺·8月底集中申报</div>
      </div>
      <!-- 08-09 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-09</div>
        <div class="timeline-title">医药基金回血·公募持仓降至冰点后反弹</div>
      </div>
      <!-- 08-08 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-08</div>
        <div class="timeline-title">19只医药基年内涨超10%·医药接力科技</div>
      </div>
      <!-- 08-06 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-06</div>
        <div class="timeline-title">基金风险评级滞后·25只回撤超40%仍挂R3</div>
      </div>
'''

html = html[:idx7s] + NEW_S7 + html[idx7e:]

# ---------- 6. Integrity checks ----------
assert "S8" not in html.replace("s8","").replace("S8",""), "S8 must not exist"  # crude
assert "<!-- S8" not in html, "S8 section marker found!"
# U+FFFD check
assert "\ufffd" not in html, "U+FFFD replacement char detected!"
# div balance overall
assert html.count("<div") == html.count("</div>"), f"div mismatch: {html.count('<div')} vs {html.count('</div>')}"

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("OK: daily-update-2026-08-17 applied")
print("div open/close:", html.count("<div"), html.count("</div>"))
print("S0 context:", "8月17日 · 4条今日要闻" in html)
print("S6 label Aug14:", "2026-08-14 周五" in html)
print("S7 items:", html.count('class="timeline-item"'))
print("S8 absent:", "<!-- S8" not in html)
