# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = "index.html"
with open(PATH, "r", encoding="utf-8") as f:
    text = f.read()

# ---- phase 1: anchor precheck ----
checks = [
    "<!-- daily-update: 2026-07-13 -->",
    '<meta name="viewport" content="首批二季报出炉|244只提前结募|新发转向防御|四大公募举牌创新药|公募人才流动双创新高">',
    '<meta name="content-fingerprint" content="首批二季报出炉|244只提前结募|新发转向防御|四大公募举牌创新药|公募人才流动双创新高">',
    '    <div class="date-badge">📅 数据区间：2026.06.29 — 2026.07.13（每日更新）</div>',
    '      <span class="section-title">今日焦点（7月13日·周一·首批二季报出炉·年内244只提前结募·新发转向防御·四大公募举牌创新药）</span>',
    '    <div class="stat-number">39.48万亿</div>',
    '    <div class="stat-number">3966.02</div>',
    '    <div class="stat-number">236人</div>',
    '    <div class="stat-number">244只</div>',
    '      <div class="card p1">\n        <div class="card-top">\n          <div class="card-title">🟠 首批公募二季报出炉',  # S0 Card1 open
    '2026年7月13日（周一）',  # S6 marker substring
    '<!-- ============ Section 7:',
    '      <!-- 06-30 时间线条目 -->',
    '      <!-- 07-13 时间线条目 (NEW) -->',
    '      <!-- S8 Card NEW: 7月新发转向防御型',
]
for c in checks:
    n = text.count(c)
    assert n == 1, f"ANCHOR not found exactly once ({n}): {c[:50]!r}"
print("[phase1] all anchors present exactly once OK")

# ---- phase 2: apply ----
text = text.replace("<!-- daily-update: 2026-07-13 -->", "<!-- daily-update: 2026-07-15 -->", 1)
fp_old = '首批二季报出炉|244只提前结募|新发转向防御|四大公募举牌创新药|公募人才流动双创新高'
fp_new = '清盘271只创新高|翻倍基瘦身225至74|费率改革三周年|主动ETF申请递交|半导体设备领涨'
text = text.replace('<meta name="viewport" content="' + fp_old + '">',
                     '<meta name="viewport" content="' + fp_new + '">', 1)
text = text.replace('<meta name="content-fingerprint" content="' + fp_old + '">',
                     '<meta name="content-fingerprint" content="' + fp_new + '">', 1)
text = text.replace(
    '    <div class="date-badge">📅 数据区间：2026.06.29 — 2026.07.13（每日更新）</div>',
    '    <div class="date-badge">📅 数据区间：2026.07.01 — 2026.07.15（每日更新）</div>', 1)
text = text.replace(
    '      <span class="section-title">今日焦点（7月13日·周一·首批二季报出炉·年内244只提前结募·新发转向防御·四大公募举牌创新药）</span>',
    '      <span class="section-title">今日焦点（7月15日·周三·清盘271只创新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交）</span>', 1)

# Stats Bar (4-space indent for inner)
text = text.replace(
    '    <div class="stat-number">39.48万亿</div>\n'
    '    <div class="stat-label">公募总规模（截至2026年5月底·首批二季报亮相·含科量成业绩密码）</div>\n'
    '    <div class="stat-change up">▲ 同泰等首批二季报聚焦AI算力链·10年业绩首披露</div>',
    '    <div class="stat-number">271只</div>\n'
    '    <div class="stat-label">上半年公募基金清盘（创近7年新高·发起式占比过半·同质化加速出清）</div>\n'
    '    <div class="stat-change up">▲ 行业从"快车道"驶向"稳车道"·迷你发起式成高发地</div>', 1)
text = text.replace(
    '    <div class="stat-number">3966.02</div>\n'
    '    <div class="stat-label">上证综指 · 07-13开盘（跌0.75%·科创50-1.29%·半导体领跌）</div>\n'
    '    <div class="stat-change down">▼ 深成指-0.92%·创业板-0.86%·油气煤炭医药逆势</div>',
    '    <div class="stat-number">3972.51</div>\n'
    '    <div class="stat-label">上证综指 · 07-15盘中（翻红+0.14%·创业板+0.74%高开·半导体活跃）</div>\n'
    '    <div class="stat-change down">▼ 深成指+0.31%·油气黄金走弱</div>', 1)
text = text.replace(
    '    <div class="stat-number">236人</div>\n'
    '    <div class="stat-label">年内基金经理离任（新聘376人·双双创同期新高）</div>\n'
    '    <div class="stat-change neutral">■ 去明星化提速·平台化投研建设加速</div>',
    '    <div class="stat-number">74只</div>\n'
    '    <div class="stat-label">年内"翻倍基"仅剩（7/12·较6月末225只骤降三分之二）</div>\n'
    '    <div class="stat-change down">▼ 科技高位回调·重仓基金7月平均跌超10%</div>', 1)
text = text.replace(
    '    <div class="stat-number">244只</div>\n'
    '    <div class="stat-label">年内基金提前结募（远超延长募集101只·发行热度攀升）</div>\n'
    '    <div class="stat-change neutral">■ 7月新发转向偏债/红利/均衡防御赛道</div>',
    '    <div class="stat-number">41只</div>\n'
    '    <div class="stat-label">本周新基发行（权益类占58.54%·偏债/红利防御并行补位）</div>\n'
    '    <div class="stat-change neutral">■ 机构主动调整供给结构应对再平衡</div>', 1)

# S0 block: replace [ <!-- S0 Card 1: , <!-- ============ Section 1: )
s0_start = text.index('<!-- S0 Card 1:')
s0_end = text.index('<!-- ============ Section 1:')
s0_new = '''    <!-- S0 Card 1: 上半年公募基金清盘271只创近7年新高·发起式成高发地 (T+0 07-15) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 上半年公募基金清盘271只创近7年新高·发起式基金成"高发地"·行业驶向"稳车道"</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-15</span>
          </div>
        </div>
        <div class="card-body">
          <b>清盘创纪录：</b>经济日报报道，2026年上半年公募基金清盘<b>271只</b>（不同份额分开计算），创2019年以来同期新高。其中148只主份额中<b>77只发起式基金</b>因三年期满规模未达2亿元触发自动清盘，占比高达52%——2023年发起式发行高峰的产品于今年集中到期。<br>
          <b>同质化出清：</b>东财基金年内12只、泓德基金8只产品陆续清盘，低效同质化产品批量出清成常态，公募基金数量虽突破1.4万只，行业却从"快车道"驶向"稳车道"。<br>
          <b>对基金行业影响：</b>产品供给侧出清→腾安选品需更重生命力与持续运营能力，规避"迷你"发起式陷阱。
        </div>
        <div class="card-footer">
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202607/t20260715_3086487.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济日报</span></a>
          <span class="impact-tag high">清盘潮：高</span>
        </div>
      </div>
    <!-- S0 Card 2: "翻倍基"两周大瘦身·从225只骤降至74只 (T+0 07-15) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 "翻倍基"两周大瘦身·年内从225只骤降至74只·科技高位回调重创重仓基金</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-15</span>
          </div>
        </div>
        <div class="card-body">
          <b>批量退群：</b>腾讯新闻报道，截至6月30日年内净值翻倍权益基金还有225只，到7月12日仅剩<b>74只</b>，短短两周少了151只、缩水近三分之二；涨幅超150%基金从15只锐减至1只，超120%从88只降至25只。<br>
          <b>回调重创：</b>主因是上半年最强主线科技成长高位回调，上半年热门产品7月以来几乎全负收益、平均跌幅超10%，方正富邦核心优势、财通多策略福鑫、华商均衡成长等多只跌逾10%。<br>
          <b>对基金行业影响：</b>极致结构性行情进入深度调整→腾安需强化客户预期管理与哑铃配置，提示高位波动。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260715A034QC00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻</span></a>
          <span class="impact-tag high">翻倍基缩水：高</span>
        </div>
      </div>
    <!-- S0 Card 3: 公募费率改革三周年·全链条让利·浮动费率落地 (T-1 07-14) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募费率改革三周年·管理费/交易费/销售费全链条下调·浮动费率产品落地</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-14</span>
          </div>
        </div>
        <div class="card-body">
          <b>三阶段推进：</b>2023年7月证监会启动费率改革，分阶段降低管理费、托管费、交易佣金及销售环节费率，当前债券/货币/行业主题ETF等纷纷加入降费阵营；2025年底《销售费用管理规定》自2026年1月1日实施。<br>
          <b>机制创新：</b>与业绩挂钩的浮动管理费收取机制落地，推动公募基金回归"为投资者创造价值"本源，从"规模导向"转向"持有人回报导向"。<br>
          <b>对基金行业影响：</b>费率下行+浮动费率→代销平台以"重长期、重体验"服务构建差异，弱化单纯价格战。
        </div>
        <div class="card-footer">
          <a href="https://m.21jingji.com/article/20260714/herald/7cd74001b8ab6b87ddf07a486a986dde.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">21世纪经济报道</span></a>
          <span class="impact-tag medium">费率改革：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 已有基金公司递交主动ETF发行申请材料·主动管理ETF落地在即 (T-1 07-14) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 已有基金公司递交主动ETF发行申请材料·主动管理ETF落地在即·丰富ETF工具箱</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-14</span>
          </div>
        </div>
        <div class="card-body">
          <b>落地提速：</b>7月14日获悉，已有基金公司递交主动ETF发行申请材料。主动ETF指管理人自主选择投资策略、不跟踪特定指数的上市ETF；此前证监会宣布支持沪深交易所推出主动ETF，上交所、深交所已发布业务指引并施行。<br>
          <b>产品扩容：</b>主动ETF将补齐国内ETF"主动管理"空白，为投资者提供兼具透明度与主动Alpha的工具，头部公募有望率先卡位。<br>
          <b>对基金行业影响：</b>ETF工具箱再丰富→腾安可提前储备主动ETF货架与投教，把握新品种发行红利。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/4017750.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·人民财讯</span></a>
          <span class="impact-tag medium">主动ETF：中</span>
        </div>
      </div>
    </div>
  </div>
'''
text = text[:s0_start] + s0_new + text[s0_end:]

# S6 market card
marker = text.index('2026年7月13日（周一）')
s6_start = text.rfind('<div class="card p3">', 0, marker)
s6_end = text.index('<!-- ============ Section 7:')
s6_new = '''    <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月15日（周三）·A股开盘涨跌不一·创业板指高开0.74%·半导体设备/存储/光纤活跃·油气黄金走弱</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-15开盘（涨跌不一·盘中沪指翻红）：</b><br>
              ▪ 沪指 <b>-0.09%→+0.14%</b>（3963.73→3972.51）·深成指 <b>+0.31%</b>（14970.77）<br>
              ▪ 创业板指 <b>+0.74%→+0.34%</b>（3879.77→3864.08）·科创50 平盘附近<br>
              ▪ 板块：先进封装/半导体设备/培育钻石/存储芯片/光纤/稀土/光刻机/PCB活跃；油气/商业航天/中药/白酒/黄金/银行走弱；创新药反复活跃（哈药4连板）
            </div>
            <div>
              <b>📊 上一交易日（07-14）复盘·强势反弹：</b><br>
              ▪ 沪指 <b>+1.36%</b>（3967.13）·深成指 <b>+2.77%</b>（14924.87）·创业板 <b>+3.43%</b>（3851.14）<br>
              ▪ 两市成交2.7万亿（缩量1138亿）；算力硬件/PCB/CPO走强，游戏下挫<br>
              ▪ 外围：美股07-14延续科技主线；港股创新药/AI应用活跃，关注中东地缘风险
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-15（周三开市·07-15开盘/07-14收盘）</span>
            <span class="source-tag">数据来源：澎湃/新浪/中新经纬/证券之星/网易财经</span>
          </div>
      </div>
  </div>
'''
text = text[:s6_start] + s6_new + text[s6_end:]

# S7: remove expired 06-30, add 07-15 before 07-13
# NOTE: anchor the close on '\n      </div>\n' (newline+6spaces+close+newline) so we match the
# timeline-item's OWN close line, NOT the 8-space wrapper close which contains '      </div>' as substring.
t30_start = text.index('      <!-- 06-30 时间线条目 -->')
t30_close = text.index('\n      </div>\n', t30_start)
t30_end = t30_close + len('\n      </div>\n')
assert text[t30_close+1:t30_end] == '      </div>\n', f"06-30 close guard failed: {text[t30_close:t30_end]!r}"
text = text[:t30_start] + text[t30_end:]
t15_block = '''    <!-- 07-15 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-07-15（上半年清盘271只创7年新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交·A股涨跌不一半导体活跃）</div>
          <div class="timeline-title">上半年公募基金清盘271只创近7年新高 / "翻倍基"两周从225只骤降至74只 / 公募费率改革三周年全链条让利 / 主动ETF发行申请材料已递交</div>
          <div class="timeline-desc">7月15日，行业"新陈代谢"加速：2026年上半年公募基金清盘271只（不同份额）创2019年以来同期新高，其中发起式基金因三年期满规模未达2亿触发自动清盘占比过半，行业从"快车道"驶向"稳车道"。同日，年内"翻倍基"大幅缩水——截至7月12日仅剩74只（6月末225只），高收益梯队快速收缩，重仓科技基金7月以来平均跌超10%。公募费率改革迎来三周年节点，管理费/交易费/销售费全链条下调、浮动费率产品落地，推动行业回归"为投资者创造价值"本源；主动ETF落地再进一步，已有基金公司递交发行申请材料。A股三大指数开盘涨跌不一，沪指-0.09%、创业板指+0.74%，半导体设备/存储/光纤/培育钻石活跃，油气黄金走弱。</div>
        </div>
      </div>

'''
t13_idx = text.index('      <!-- 07-13 时间线条目 (NEW) -->')
text = text[:t13_idx] + t15_block + text[t13_idx:]

# S8: add 清盘潮 action card before existing first S8 card
s8_new = '''    <!-- S8 Card NEW: 上半年清盘271只创7年新高·发起式成高发地 (07-15) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 上半年公募基金清盘271只创近7年新高·发起式成"高发地"·腾安需优化选品标准规避迷你基陷阱</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-15</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>2026年上半年公募基金清盘271只（不同份额）创2019年以来同期新高；148只主份额中77只发起式基金因三年期满规模未达2亿元触发自动清盘，同质化产品加速出清，行业从"快车道"驶向"稳车道"。<br>
          <b>腾安行动建议：</b>① 优化选品标准，强化产品生命力与持续运营能力评估，规避"迷你"发起式陷阱；② 建立清盘预警监测，对规模临界产品提前提示客户；③ 借行业出清契机，向客户传递"少而精"的优质产品理念。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 优化选品标准→产品部<br>
            ② 建立清盘预警监测→投顾部<br>
            ③ 传递"少而精"产品理念→营销部
          </div>
        </div>
      </div>

'''
s8_idx = text.index('      <!-- S8 Card NEW: 7月新发转向防御型')
text = text[:s8_idx] + s8_new + text[s8_idx:]

# ---- checks ----
opens = text.count('<div'); closes = text.count('</div>')
assert opens == closes, f"DIV IMBALANCE: {opens} vs {closes}"
assert '06-30 时间线条目' not in text, "06-30 timeline NOT removed!"
assert '首批二季报出炉·同泰4只' not in text, "old S0 card1 still present!"
assert '2026年7月13日（周一）' not in text, "old S6 card still present!"
print(f"[check] div balance OK: {opens} == {closes}")
print("[check] 06-30 gone / old S0 gone / old S6 gone OK")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(text)
print("[done] index.html updated -> 2026-07-15")
