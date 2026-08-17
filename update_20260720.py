# -*- coding: utf-8 -*-
"""每日更新 2026-07-20（周一）。锚点slice+精确replace+per-step div快照。"""
import io, sys

FP = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with io.open(FP, encoding="utf-8") as f:
    s = f.read()
orig = s

def gbal(t):
    return t.count("<div") - t.count("</div>")

base = gbal(s)
print("BASE global div balance:", base)

def rep(old, new, label):
    global s
    n = s.count(old)
    assert n == 1, "ANCHOR [%s] count=%d (expect 1)" % (label, n)
    s = s.replace(old, new)
    print("OK  [%s]  div-delta=%+d" % (label, gbal(s) - base))

# ---------- 1. marker ----------
rep("<!-- daily-update: 2026-07-19 -->",
    "<!-- daily-update: 2026-07-20 -->", "marker")

# ---------- 2. date-badge ----------
rep('<div class="date-badge">📅 数据区间：2026.07.05 — 2026.07.19（每日更新）</div>',
    '<div class="date-badge">📅 数据区间：2026.07.06 — 2026.07.20（每日更新）</div>', "date-badge")

# ---------- 3. Stats Bar ----------
STATS_OLD = '''<div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">3764.15</div>
      <div class="stat-label">上证综指 · 07-17收盘-3.05%失守3800·创业板-7.15%·科创综指-8.13%（周五大跌·近5000股飘绿）</div>
      <div class="stat-change down">▼ A股罕见暴跌·二季报重仓科技集中释放回撤·需提示客户风险</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">超600%</div>
      <div class="stat-label">公募二季报首披"十年业绩"·20只基金披露过去10年数据·部分净值增长超600%</div>
      <div class="stat-change up">▲ 信披新规落地·引导长期投资理念·淡化短期排名</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">53.46%</div>
      <div class="stat-label">发起式基金清盘占比超50%·年内159只清盘85只发起式·翻倍基亦被错杀</div>
      <div class="stat-change down">▼ 三年大考清盘高发·"重首发轻持营"待解</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">18家</div>
      <div class="stat-label">公募集中上报首批主动股票ETF（境内ETF迈入"主动时代"·沪深各9只）</div>
      <div class="stat-change up">▲ 主动ETF从制度设计走向落地·腾安前瞻储备货架</div>
    </div>
  </div>'''

STATS_NEW = '''<div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">3802.00</div>
      <div class="stat-label">上证综指 · 07-20盘中+1.01%（开盘冲高沪+0.73%/创+2.2%后回落·半导体/CPO/HBM领涨）</div>
      <div class="stat-change up">▲ 周五暴跌后放量反弹·历史规律恐慌日后一周反弹胜率近七成</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">914亿</div>
      <div class="stat-label">上周前四交易日宽基ETF合计净流入·"跌出来"的抄底资金借道入场</div>
      <div class="stat-change up">▲ 华泰柏瑞沪深300ETF单周净流入121亿·规模935亿重回第一</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">10只</div>
      <div class="stat-label">长跑翻倍基·过去7-10年净值翻倍产品仅10只·占已披露二季报不足3%</div>
      <div class="stat-change up">▲ 二季报首披十年业绩·长跑绩优基金二季度逆势减仓科技</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">18家</div>
      <div class="stat-label">首批主动ETF落地倒计时·有望10个交易日内快速落地·"透明厨房"时代来临</div>
      <div class="stat-change up">▲ 主动ETF从上报走向落地·腾安前瞻储备货架与投教话术</div>
    </div>
  </div>'''
rep(STATS_OLD, STATS_NEW, "stats-bar")

# ---------- 4. S0 section-header title ----------
rep('<span class="section-title">今日焦点（7月19日·周日·主动ETF正式上报·二季报密集披露重仓AI算力·二季报首披十年业绩·发起式清盘占比过半）</span>',
    '<span class="section-title">今日焦点（7月20日·周一·A股放量反弹半导体领涨·AI行情现分歧基金经理调仓差异·主动ETF落地倒计时·长跑翻倍基逆势减仓）</span>',
    "s0-title")

# ---------- 5. S0 card-grid (full replace) ----------
# 从 S0 的 card-grid 开始到 Section1 注释前的 section 闭合
S0_START = '''    <div class="card-grid">

          <!-- S0 Card 1: 公募二季报首披"十年业绩"·部分基金10年净值增长超600% (T+0 07-18 P1) -->'''
i0 = s.index(S0_START)
S1_MARK = "<!-- ============ Section 1: 重磅信息 ============ -->"
i1 = s.index(S1_MARK)
# S0 card-grid 结束 + section 闭合，位于 Section1 注释前
old_s0_block = s[i0:i1]
# 结构应为 card-grid ... </div>(card-grid) \n  </div>(section) \n
assert old_s0_block.rstrip().endswith("</div>"), "S0 block tail unexpected"

S0_NEW = '''    <div class="card-grid">

          <!-- S0 Card 1: A股周一放量反弹·恐慌后技术性反弹 (T+0 07-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 A股周一放量反弹·沪指+1.01%·创业板+1.29%·半导体/CPO/HBM领涨·恐慌日后技术性反弹</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-20</span>
          </div>
        </div>
        <div class="card-body">
          <b>放量反弹：</b>周五罕见暴跌后，7月20日三大指数集体高开——沪指开盘+0.73%、创业板+2.2%；盘中冲高回落，截至上午沪指<b>+1.01%</b>报3802点、创业板<b>+1.29%</b>报3472.90点，半导体、MLCC、CPO、存储芯片、光通信领涨，中药、白色家电走弱。<br>
          <b>机构定调：</b>华泰证券指出历史规律显示恐慌日后一周内技术性反弹是高概率事件、胜率接近七成；反弹中资金往往切回超跌的成长与顺周期，而非停留在防御资产。东方财富证券建议积极布局反攻、看好国产AI链"真科技"龙头。<br>
          <b>对基金行业影响：</b>暴跌后情绪修复→腾安应引导客户理性看待波动、避免恐慌离场，把握结构性反弹中的科技+顺周期配置机会。
        </div>
        <div class="card-footer">
          <a href="https://finance.ifeng.com/c/8uuMaKuUfd2" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">凤凰财经·证券时报</span></a>
          <span class="impact-tag medium">市场反弹：中</span>
        </div>
      </div>
    <!-- S0 Card 2: AI行情现分歧·基金经理调仓差异 (T+0 07-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 AI行情现分歧·二季报密集披露·基金经理调仓动作出现明显差异</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-20</span>
          </div>
        </div>
        <div class="card-body">
          <b>多空分歧：</b>随公募二季报密集披露，AI板块是否已现泡沫成为基金经理讨论最集中的话题。一方认为部分AI资产估值已透支未来、局部泡沫特征愈发明显；另一方认为本轮AI行情有真实产业需求和订单支撑、产业景气仍有望延续。<br>
          <b>调仓分化：</b>分歧之下调仓动作明显差异——有人兑现收益、降低仓位，也有人继续加码算力、芯片核心赛道；围绕AI产业链的投资博弈进一步升温。张晓泉提示TMT成交额占比一度攀升至45%、接近历史级拥挤阈值。<br>
          <b>对基金行业影响：</b>AI主线进入分歧期→腾安推荐需平衡景气与拥挤，弱化单一赛道押注，强化均衡配置与风险揭示话术。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L2901VA0053469RG.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·人民财讯</span></a>
          <span class="impact-tag medium">AI分歧：中</span>
        </div>
      </div>
    <!-- S0 Card 3: 主动ETF落地倒计时·10日内有望快速落地 (T+0 07-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 主动ETF落地倒计时·首批18只有望10个交易日内快速落地·公募开启"透明厨房"窗口</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-20</span>
          </div>
        </div>
        <div class="card-body">
          <b>火速推进：</b>从监管6月17日首次表态"支持推出主动ETF"，到18只产品注册申请材料齐挂证监会官网，不到一个月；据业内反馈，首批主动ETF有望在<b>10个交易日内</b>迎来快速落地、有序推进。<br>
          <b>稳健起步：</b>18家管理人涵盖易方达、华夏、华泰柏瑞等头部ETF大厂及招商、南方、摩根等内外资机构；产品策略刻意避开激进赛道，以"低换手、高分散"起步，聚焦大盘均衡价值/成长、红利低波等类型（工银瑞信红利、招商价值智选等）。<br>
          <b>对基金行业影响：</b>主动投资"透明厨房"时代来临→头部机构拉开差异化竞争序幕，腾安应前瞻储备主动ETF货架与投教内容。
        </div>
        <div class="card-footer">
          <a href="https://guba.eastmoney.com/news,cjpl,1745913749.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经</span></a>
          <span class="impact-tag medium">主动ETF：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 长跑型绩优基金调仓策略出炉·10只翻倍基逆势减仓 (T+0 07-20 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募二季报新增披露十年业绩·长跑型绩优基金调仓出炉·翻倍基逆势减仓科技</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-20</span>
          </div>
        </div>
        <div class="card-body">
          <b>凤毛麟角：</b>截至7月19日已披露二季报产品超400只，此次新增7年、10年中长期业绩披露成一大看点；过去7-10年由同一基金经理管理、净值涨幅超100%的"长跑型"产品仅<b>10只</b>、占比不足3%。红土创新转型精选（LOF）过去七年涨680.39%居首，睿远成长价值（超220亿规模最大）涨183.41%。<br>
          <b>逆势减仓：</b>与"追高科技股"不同，这批长跑基金大多在二季度科技股火热之际逆势减仓、锁定收益；傅鹏博/朱璘顺势减少PCB/芯片/光通信持仓，盖俊龙提示高预期下未来面临低于预期风险。<br>
          <b>对基金行业影响：</b>信披新规引导长期视角→腾安推荐应强化长期业绩与持有体验，弱化"冠军效应"营销。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_4266a5d771e38252" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">长期业绩：中</span>
        </div>
      </div>
    </div>
  </div>
'''
s = s[:i0] + S0_NEW + s[i1:]
print("OK  [s0-block]  div-delta=%+d" % (gbal(s) - base))

# ---------- 6. S6 market card (full replace) ----------
S6_START = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月19日（周日·休市）·展示07-17收盘·A股罕见暴跌·沪指-3.05%失守3800·创业板-7.15%·科创综指-8.13%</div>'''
j0 = s.index(S6_START)
S7_MARK = "<!-- ============ Section 7: 关键时间线 ============ -->"
# S6 card 结束到 </div>(section) 再到 S7 注释
j_end_section = s.index("  </div>\n" + S7_MARK)
old_s6 = s[j0:j_end_section]
assert old_s6.count("<div") - old_s6.count("</div>") == 0, "S6 old block not balanced"

S6_NEW = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月20日（周一·盘中）·A股放量反弹·沪指+1.01%·创业板+1.29%·半导体/CPO领涨</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股07-20盘中（暴跌后放量反弹）：</b><br>
              ▪ 沪指 <b>+1.01%</b>（3802，开盘+0.73%冲高回落）·深成指开 <b>+1.18%</b><br>
              ▪ 创业板指 <b>+1.29%</b>（3472.90，开盘+2.2%）·成交放量<br>
              ▪ 板块：半导体、MLCC、CPO、存储芯片、光通信领涨；中药、白色家电跌
            </div>
            <div>
              <b>📉 港股07-17收盘（最近交易日）：</b><br>
              ▪ 恒指 <b>-1.78%</b>（24562.24）·恒生科技 <b>-4.37%</b>（4623.17）·国企指数-2.18%<br>
              <b>📉 美股07-17收盘（芯片续挫）：</b>道指-0.77%（52146.42）·标普-1.01%（7457.69）·纳指<b>-1.40%</b>（25520.24）；存储概念重挫SK海力士-13.48%
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：华泰证券称恐慌日后一周技术性反弹胜率近七成；上周前四交易日宽基ETF净流入超914亿（华泰柏瑞沪深300ETF重回规模第一）；二季报密集披露、AI行情现分歧、首批主动ETF有望10日内快速落地。
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-20（周一盘中）</span>
            <span class="source-tag">数据来源：证券时报/凤凰财经/东方财富/国际金融要情</span>
          </div>
      </div>
'''
s = s[:j0] + S6_NEW + s[j_end_section:]
print("OK  [s6-block]  div-delta=%+d" % (gbal(s) - base))

# ---------- 7. S7: 删除 07-05 过期条目 ----------
S7_0705 = '''      <!-- 07-05 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-05</div>
        <div class="timeline-title">美股股票基金周流出172亿美元·大空头做空美光预警半导体30%回调</div>
      </div>

'''
rep(S7_0705, "", "s7-del-0705")

# ---------- 8. S7: 新增 07-20 置顶 ----------
S7_ANCHOR = '''    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
    <!-- 07-18 时间线条目 (NEW) -->'''
S7_NEW = '''    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
    <!-- 07-20 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-20</div>
        <div class="timeline-title">A股周一放量反弹·沪指+1.01%·半导体领涨（恐慌后技术性反弹）</div>
      </div>

    <!-- 07-18 时间线条目 (NEW) -->'''
rep(S7_ANCHOR, S7_NEW, "s7-add-0720")

# ---------- 最终校验 ----------
final = gbal(s)
print("FINAL global div balance:", final, "(base was", base, ")")
assert final == base, "GLOBAL DIV BALANCE CHANGED! delta=%d" % (final - base)
assert s.count('class="timeline-item"') > 0
assert "timeline-desc" not in s, "S7 timeline-desc detected!"
assert "Section 8" not in s and "待办跟踪" not in s, "S8 残留!"
assert s.count('<!-- daily-update: 2026-07-20 -->') == 1

with io.open(FP, "w", encoding="utf-8") as f:
    f.write(s)
print("WRITTEN OK. timeline items:", s.count('class="timeline-item"'))
