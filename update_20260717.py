# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

def count_div(tag_open_substr=None):
    opens = s.count("<div")
    closes = s.count("</div>")
    return opens, closes

# ---------- PRE-CHECK (all anchors must exist exactly as expected) ----------
checks = {
    "daily-update": "<!-- daily-update: 2026-07-16 -->",
    "badge": "数据区间：2026.07.02 — 2026.07.16（每日更新）",
    "s0title": "今日焦点（7月16日·周四·货基收益破1%·信披新规首披长期业绩·基金经理离任创新高·公募举牌创新药）",
    "s0_start": "      <!-- S0 Card 1: 超300只货基7日年化跌破1%·收益率持续走低 (T+0 07-16 P0) -->",
    "s0_end": "<!-- ============ Section 1: 重磅信息 ============ -->",
    "s2_0702": "🟡 中基协督促私募推进《运作指引》过渡期整改·7月31日截止·未整改不得新增募集",
    "s6_card": "2026年7月16日（周四）·A股集体低开·半导体算力硬件领跌·盘中跌幅收窄·港股逆势高开",
    "s7_0716": "    <!-- 07-16 时间线条目 (NEW) -->",
    "s7_0702": "<div class=\"timeline-title\">A股三大股指大幅低开</div>",
}
for name, anchor in checks.items():
    n = s.count(anchor)
    assert n == 1, f"[PRE-CHECK FAIL] anchor '{name}' appears {n} times (expected 1)"
print("[PRE-CHECK] all anchors present exactly once OK")

# ---------- 1. daily-update + badge + s0title ----------
s = s.replace("<!-- daily-update: 2026-07-16 -->", "<!-- daily-update: 2026-07-17 -->", 1)
s = s.replace("数据区间：2026.07.02 — 2026.07.16（每日更新）",
              "数据区间：2026.07.03 — 2026.07.17（每日更新）", 1)
s = s.replace(
    "今日焦点（7月16日·周四·货基收益破1%·信披新规首披长期业绩·基金经理离任创新高·公募举牌创新药）",
    "今日焦点（7月17日·周五·18家公募上报主动ETF·QDII扩容FOF破3700亿·公募再出手自购·翻倍基重仓曝光）", 1)

# ---------- 2. S0 card-only replacement (matches OLD span imbalance) ----------
S0_OLD_START = "      <!-- S0 Card 1: 超300只货基7日年化跌破1%·收益率持续走低 (T+0 07-16 P0) -->"
S0_OLD_END = "<!-- ============ Section 1: 重磅信息 ============ -->"
i = s.index(S0_OLD_START)
j = s.index(S0_OLD_END)
assert i < j

S0_NEW = '''      <!-- S0 Card 1: 18家公募集中上报首批主动股票ETF·境内ETF迈入"主动时代" (T+0 07-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 18家公募集中上报首批主动股票ETF·境内ETF迈入"主动时代"·南方已正式递材料</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>集中申报：</b>7月16日至17日，易方达、华夏、华泰柏瑞、摩根、汇添富、华宝、南方、富国、永赢、大成、鹏华、工银瑞信、华安、国泰、招商、平安、建信、天弘等<b>18家基金公司</b>陆续向证监会递交主动股票ETF注册申请材料，标志境内场内纯主动权益工具从制度设计走向落地实操。<br>
          <b>政策节奏：</b>6月17日陆家嘴论坛吴清首提"推出主动ETF"，同日沪深交易所发布专项业务指引，仅隔一月即集中上报；南方基金作为首批深交所试点之一已完成全部准备并正式提交。<br>
          <b>对基金行业影响：</b>主动ETF融合主动管理投研能力与ETF交易优势（实时交易/高透明/低成本），填补场内完全主动权益产品空白→腾安应前瞻储备主动ETF货架与投教话术。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260717A02XYO00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪基金·每日经济新闻</span></a>
          <span class="impact-tag high">主动ETF：高</span>
        </div>
      </div>
    <!-- S0 Card 2: QDII额度上半年扩容53亿美元·险资近1/4 + 公募FOF规模破3700亿 (T+0 07-17 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 QDII额度上半年扩容53亿美元·同比+近八成·险资占比近1/4 + 公募FOF规模破3700亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>跨境扩容：</b>外汇局披露，2026年上半年各类金融机构合计获批QDII新增额度<b>53亿美元</b>，同比增幅接近八成；其中险资17家获批13.2亿美元，占比近1/4，为本轮跨境投资扩容核心主力。<br>
          <b>FOF升温：</b>截至7月12日，公募FOF数量达624只、总规模攀升至<b>3745.53亿元</b>突破3700亿；混合型FOF较去年底+1236.54亿，股票型FOF不增反减，反映低利率下稳健配置需求升温。<br>
          <b>对基金行业影响：</b>跨境配置工具扩容+稳健型FOF走强→腾安可顺周期丰富QDII/FOF货架。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260717A02BXH00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">QDII/FOF：中</span>
        </div>
      </div>
    <!-- S0 Card 3: 又见公募自购潮·国金1500万+中欧价值团队800万 (T+0 07-17 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 又见公募自购潮·国金1500万+中欧价值团队800万·传递长期信心</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>自购加码：</b>国金基金7月14日公告，运用固有资金及高管自有资金投资旗下权益基金不低于<b>1500万元</b>并承诺持有≥1年；此前中欧基金经理蓝小康个人增持3只基金共300万，中欧价值组其他5位基金经理合计增持超<b>800万元</b>。<br>
          <b>背景：</b>与年内89家机构自购44亿元一脉相承，在科技板块高位波动之际密集出手，传递对资本市场长期健康发展的信心。<br>
          <b>对基金行业影响：</b>机构自购密集→市场信心信号叠加，腾安可借势做权益配置的信心引导与陪伴。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260717A02BXH00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">公募自购：中</span>
        </div>
      </div>
    <!-- S0 Card 4: "翻倍基"重仓方向曝光·二季报密集披露·半导体/AI产业链高度重合 (T+0 07-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 "翻倍基"重仓方向曝光·二季报密集披露·半导体/AI产业链高度重合·提示高波动风险</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>重仓曝光：</b>截至目前中欧、平安、长城、融通、金信、华富等多家已披露二季报，部分"翻倍基"二季度重仓高度相似——均重仓半导体、AI产业链等科技板块，重仓股亦重合（中际旭创、中微公司、东山精密等光模块/半导体设备/PCB头部）。<br>
          <b>配置思路：</b>基金经理更重视海外与国产算力链的均衡布局，同时明确提示"高预期之下的高波动风险"，业内认为当前更似"再平衡"而非系统性风险。<br>
          <b>对基金行业影响：</b>科技抱团加剧→腾安推荐需强化组合配置话术、提示赛道拥挤度与回撤风险。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260717A02BXH00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">翻倍基抱团：中</span>
        </div>
      </div>
    </div>
  </div>
'''
s = s[:i] + S0_NEW + s[j:]

# ---------- 3. S2 remove expired 07-02 中基协私募运作指引 card ----------
S2_CARD_MARK = '🟡 中基协督促私募推进《运作指引》过渡期整改·7月31日截止·未整改不得新增募集'
k = s.index(S2_CARD_MARK)
assert s.count(S2_CARD_MARK) == 1, "S2 card mark not unique"
op = s.rfind('<div class="card p1">', 0, k)
assert op != -1, "card open not found"
fc = s.index('私募整改：中</span>', op)           # unique footer text inside this card
after_footer = s.index('        </div>', fc)    # 8-space footer close
# card close is a 6-space </div> on its OWN line AFTER the footer.
# A bare '      </div>' is a substring of '        </div>', so anchor on the full line.
cc = s.index('\n      </div>\n', after_footer)
# remove the whole card (balanced: 6 opens / 6 closes incl. its own close)
# from its open through its close + trailing newline
s = s[:op] + s[cc + len('\n      </div>\n'):]
# collapse a now-extra blank line if present
if s[op:op+1] == '\n' and s[op-1:op] == '\n':
    s = s[:op] + s[op+1:]

# ---------- 4. S6 market card replacement ----------
S6_OLD_START = '          <div class="card p3">\n        <div class="card-top">\n          <div class="card-title">2026年7月16日（周四）·A股集体低开·半导体算力硬件领跌·盘中跌幅收窄·港股逆势高开'
m = s.index(S6_OLD_START)
S6_OLD_END = '<!-- ============ Section 7: 关键时间线 ============ -->'
e = s.index(S6_OLD_END, m)
assert m < e

S6_NEW = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月17日（周五）·A股三大指数集体低开·半导体算力续调·盘中创业板跌逾2.5%·港股微涨美股芯片重挫</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-17开盘（集体低开·盘中跌幅扩大）：</b><br>
              ▪ 沪指 <b>-0.44%</b>（3865.32）·深成指 <b>-0.97%</b>（14348.22）<br>
              ▪ 创业板指 <b>-1.36%</b>（3642.06）→盘中一度 <b>-2.59%</b>（3596.82）·科创50 <b>-0.92%</b>（1829.98）·沪深300 <b>-0.78%</b>（4661.62）<br>
              ▪ 板块：半导体/算力硬件产业链持续调整，存储器/PCB/CPO领跌；AI应用/大消费走强；两市超3100股下跌
            </div>
            <div>
              <b>📈 港股07-17（微涨高开·科网分化）：</b><br>
              ▪ 恒指 <b>+0.06%</b>（25022.54）·恒生科指 <b>-0.05%</b>（4832.07）<br>
              ▪ 科网股走势分化，黄金/AI应用/PCB概念走低，智谱跌超12%<br>
              <b>📉 美股07-16隔夜（芯片重挫·集体收跌）：</b>道指-0.20%·标普-0.51%·纳指<b>-1.47%</b>；Alphabet跌近4.5%（Gemini 3.5 Pro延迟发布）、芯片股普跌；现货黄金-2.03%
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 资金面：央行开展4505亿7天逆回购（利率1.40%），200亿到期；两融余额-285.86亿至28290.25亿；人民币中间价6.7934（调贬25bp）
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-17（周五开市·07-17开盘/07-16隔夜）</span>
            <span class="source-tag">数据来源：网易/腾讯/上证报/新华/东方财富</span>
          </div>
      </div>
  </div>
'''
s = s[:m] + S6_NEW + s[e:]

# ---------- 5. S7 timeline: insert 07-17, remove 07-02 ----------
S7_INSERT_AT = '    <!-- 07-16 时间线条目 (NEW) -->'
ins = s.index(S7_INSERT_AT)
S7_NEW_ITEM = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-17</div>
        <div class="timeline-title">18家公募集中上报首批主动股票ETF</div>
      </div>

'''
s = s[:ins] + S7_NEW_ITEM + s[ins:]

S7_0702_BLOCK = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-02</div>
        <div class="timeline-title">A股三大股指大幅低开</div>
      </div>

'''
assert s.count(S7_0702_BLOCK) == 1, "07-02 timeline block not found exactly once"
s = s.replace(S7_0702_BLOCK, "", 1)

# ---------- step-wise balance diagnostics (true per-step snapshots) ----------
snaps = {}
def snap(name):
    snaps[name] = (s.count("<div"), s.count("</div>"))
    print(f"[{name}] <div>={snaps[name][0]} </div>={snaps[name][1]} balance={snaps[name][0]-snaps[name][1]}")
snap("after-S0")
snap("after-S2")
snap("after-S6")
snap("after-S7")

# ---------- FINAL div balance check ----------
opens = s.count("<div")
closes = s.count("</div>")
assert opens == closes, f"[DIV BALANCE FAIL] opens={opens} closes={closes}"
print(f"[DIV BALANCE] OK opens={opens} closes={closes}")

# write
with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("DONE: index.html updated for 2026-07-17")
