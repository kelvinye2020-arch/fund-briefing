# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

# ---------- PRE-CHECK (all anchors must exist exactly once) ----------
checks = {
    "daily-update": "<!-- daily-update: 2026-07-18 -->",
    "badge": "数据区间：2026.07.04 — 2026.07.18（每日更新）",
    "s0title": "今日焦点（7月18日·周六·二季报首披十年业绩超600%·发起式清盘占比过半·A股周五暴跌·18家公募上报主动ETF）",
    "s0_card3": "    <!-- S0 Card 3:",
    "s0_card4": "    <!-- S0 Card 4:",
    "s6_title": "2026年7月18日（周六·休市）·展示07-17收盘·A股罕见暴跌",
    "s6_footer": "WebSearch·2026-07-18（周六休市·展示07-17收盘）",
    "no_s8": "<!-- ============ Section 8",
}
for name, anchor in checks.items():
    n = s.count(anchor)
    if name == "no_s8":
        assert n == 0, f"[PRE-CHECK FAIL] S8 section unexpectedly present ({n} times)"
    else:
        assert n == 1, f"[PRE-CHECK FAIL] anchor '{name}' appears {n} times (expected 1)"
print("[PRE-CHECK] all anchors OK; S8 confirmed absent")

# ---------- 1. daily-update + badge + s0title ----------
s = s.replace("<!-- daily-update: 2026-07-18 -->", "<!-- daily-update: 2026-07-19 -->", 1)
s = s.replace("数据区间：2026.07.04 — 2026.07.18（每日更新）",
              "数据区间：2026.07.05 — 2026.07.19（每日更新）", 1)
s = s.replace(
    "今日焦点（7月18日·周六·二季报首披十年业绩超600%·发起式清盘占比过半·A股周五暴跌·18家公募上报主动ETF）",
    "今日焦点（7月19日·周日·主动ETF正式上报·二季报密集披露重仓AI算力·二季报首披十年业绩·发起式清盘占比过半）", 1)

# ---------- 2. S0: remove 07-17 (T-2) cards 3&4, add fresh 07-19 + 07-18 ----------
# Card1 (07-18 十年业绩) and Card2 (07-18 发起式清盘) are T-1 -> KEPT.
# Card3 (07-17 暴跌 P0) and Card4 (07-17 主动ETF P2) are T-2 -> REMOVED.
i3 = s.index("    <!-- S0 Card 3:")
i4 = s.index("    <!-- S0 Card 4:", i3)
assert i3 < i4
# card4 close = first 6-space </div> on its own line AFTER card4 start
end = s.index("\n      </div>\n", i4) + len("\n      </div>\n")
assert end > i4

S0_NEW_34 = '''    <!-- S0 Card 3: 18只主动管理ETF正式上报·产品名称披露·费率测算·全球规模2.49万亿美元 (T+0 07-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 18只主动管理ETF正式上报·证监会"接收材料"·产品名称披露·费率较场外主动更低</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-19</span>
          </div>
        </div>
        <div class="card-body">
          <b>正式申报：</b>7月17日证监会官网显示，首批<b>18家</b>公募递交主动股票ETF注册申请进入"接收材料"阶段，沪深交易所各9只；产品名称同步披露（易方达品质未来、华夏质量价值甄选、工银瑞信红利、摩根核心成长等），策略覆盖价值/大盘/均衡/红利/成长五类。<br>
          <b>费率优势：</b>东吴证券测算，截至6月底主动权益平均管理费率约1.161%、指增ETF约0.571%、被动ETF约0.393%；主动ETF免销售服务费、综合持有成本低于场外主动基金，投资者端降费明确。<br>
          <b>对基金行业影响：</b>全球主动ETF规模已达2.49万亿美元（约16.88万亿人民币）、占全球ETF约10%→境内ETF迈入"主动时代"，腾安应前瞻储备主动ETF货架与投教话术。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-07-19/doc-iniihzcp0350846.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag medium">主动ETF：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 基金二季报密集披露·权益重仓AI算力·债券稳守信用底仓 (T-1 07-18 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 基金二季报密集披露·截至7月15日超102只·主动权益高仓位90%+、重仓AI算力产业链</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-18</span>
          </div>
        </div>
        <div class="card-body">
          <b>密集披露：</b>Wind数据显示，截至7月15日至少<b>102只</b>基金完成二季报；多只主动权益基金维持<b>90%以上</b>高仓位（中欧科技成长92.59%、长城半导体94.78%、红土创新科技创新94%+），"高低切换"成主调。<br>
          <b>持仓主线：</b>国产算力成多数基金加仓方向，AI算力产业链（寒武纪/中微公司/工业富联等）密集新晋十大重仓；部分产品减持涨幅过高的半导体细分，均衡布局高端制造。<br>
          <b>对基金行业影响：</b>债基以中高等级信用债为底仓、灵活参与利率债波段，业绩分化明显→腾安推荐需平衡景气与拥挤，强化组合配置话术。
        </div>
        <div class="card-footer">
          <a href="https://fund.eastmoney.com/a/202607173811380773.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·经济参考报</span></a>
          <span class="impact-tag medium">二季报持仓：中</span>
        </div>
      </div>
'''
s = s[:i3] + S0_NEW_34 + s[end:]

# ---------- 3. S6 market card refresh for Sunday 07-19 ----------
s = s.replace(
    "2026年7月18日（周六·休市）·展示07-17收盘·A股罕见暴跌·沪指-3.05%失守3800·创业板-7.15%·科创综指-8.13%",
    "2026年7月19日（周日·休市）·展示07-17收盘·A股罕见暴跌·沪指-3.05%失守3800·创业板-7.15%·科创综指-8.13%", 1)
s = s.replace(
    "WebSearch·2026-07-18（周六休市·展示07-17收盘）",
    "WebSearch·2026-07-19（周日休市·展示07-17收盘）", 1)
s = s.replace(
    "💡 资金面：央行开展4505亿7天逆回购（利率1.40%），200亿到期；两融余额-285.86亿至28290.25亿；人民币中间价6.7934（调贬25bp）。周末休市，下周一关注暴跌后资金修复与板块分化。",
    "💡 周末焦点：18只主动ETF正式获证监会\"接收材料\"、二季报密集披露（截至7/15已超102只·权益高仓位重仓AI算力）；央行4505亿7天逆回购（利率1.40%）；下周关注暴跌后资金修复与板块分化。", 1)

# ---------- step-wise balance (per-step snapshots) ----------
def snap(name):
    print(f"[{name}] <div>={s.count('<div')} </div>={s.count('</div>')} balance={s.count('<div')-s.count('</div>')}")
snap("after-all")

# ---------- FINAL div balance check ----------
opens = s.count("<div")
closes = s.count("</div>")
assert opens == closes, f"[DIV BALANCE FAIL] opens={opens} closes={closes}"
print(f"[DIV BALANCE] OK opens={opens} closes={closes}")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("DONE: index.html updated for 2026-07-19")
