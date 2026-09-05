#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-05 (Saturday) 自动化更新脚本"""
import re
from datetime import date, timedelta

HTML = 'index.html'
src = open(HTML, encoding='utf-8').read()
orig = src

today = date.today()  # 2026-09-05
upper = today.strftime("%Y.%m.%d")
lower = (today - timedelta(days=14)).strftime("%Y.%m.%d")
print(f"today={today} upper={upper} lower={lower}")

def rep(old, new, label):
    global src
    assert src.count(old) == 1, f"[{label}] anchor count={src.count(old)} != 1"
    src = src.replace(old, new)
    print(f"[{label}] OK")

# 1. 顶部注释
rep('<!-- daily-update: 2026-09-04 -->', '<!-- daily-update: 2026-09-05 -->', 'comment')

# 2. header 数据区间（动态计算，正则覆盖，不依赖旧值）
badge_new = f"📅 数据区间：{lower} — {upper}（每日更新）"
src, n = re.subn(r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）", badge_new, src)
assert n == 1, f"[header] badge subn={n}"
print("[header] OK")

# 3. Stats Bar 沪指卡（09-04 收盘）
rep('''    <div class="stat-card">
      <div class="stat-number">3942.09</div>
      <div class="stat-label">沪指9-3收盘·微涨0.02%·两市成交1.76万亿·窄幅震荡</div>
      <div class="stat-change up">▲ 深成指+0.10%·创业板+0.01%·缩量企稳</div>
    </div>''',
'''    <div class="stat-card">
      <div class="stat-number">3930.12</div>
      <div class="stat-label">沪指9-4收盘·跌0.30%·沪深京成交2.05万亿·放量下探</div>
      <div class="stat-change down">▼ 深成指-0.79%·创业板-0.78%·科创50跌2.16%</div>
    </div>''', 'stats-shz')

# 4. S0 整段替换（marker 分割）
S0_MARK = '        <!-- ============ Section 0: 今日焦点 ============ -->'
S1_MARK = '<!-- ============ Section 1: 重磅信息 ============ -->'
assert src.count(S0_MARK) == 1 and src.count(S1_MARK) == 1
i = src.index(S0_MARK)
j = src.index(S1_MARK)

s0_new = '''        <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月5日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">

      <!-- S0 Card 1 (09-05 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批10家基金上报科创债场外指数基金·中小公司成申报主力</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报（记者昝秀丽）9月5日报道，9月4日<b>首批10家基金管理人上报科创债场外指数基金</b>，为投资者分享国家科技创新红利提供又一标准化、专业化配置渠道；本次上报的10家均为中小基金公司，覆盖中债-AAA科技创新债券指数、中债-高等级科技创新及绿色债券指数、上海清算所AAA科技创新债券指数3条指数。<br>
          <b>规模背景：</b>自2025年7月首批科创债ETF上市以来，全市场24只科创债ETF总规模已超3000亿元，场内科创债ETF嘉实规模突破300亿元。<br>
          <b>对腾安启示：</b>科创债产品谱系扩容、服务"科技金融"大文章，固收+科技主题货架可评估引入，强化"低波工具+严选"供给。
        </div>
        <div class="card-footer">
          <a href="https://epaper.cs.com.cn/zgzqb/html/2026-09/05/nw.D110000zgzqb_20260905_5-A05.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·09-05</span></a>
        </div>
      </div>

      <!-- S0 Card 2 (09-05 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 科技主题基金密集扩容·半导体ETF8月净流入超150亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月5日报道，围绕科技产业链公募密集布局：8月以来至9月4日<b>6只消费电子主题基金集中上报</b>（嘉实/汇添富/广发等），易方达/天弘等8家上报通信设备ETF，易方达/鹏华等10家上报创业板算力ETF，中欧/泰康等发力科技主题主动权益。<br>
          <b>资金动向：</b>据Choice测算，8月以来至9月3日半导体主题ETF资金净流入150亿元（半导体设备ETF国泰42.14亿居首），科创50相关ETF净流入33.37亿元。<br>
          <b>对腾安启示：</b>科技主题供给集中、同质化加剧，须以"严选+费率+投教"组合对冲，引导理性配置避免追高站岗。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260905A03HRJ00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-05</span></a>
        </div>
      </div>

      <!-- S0 Card 3 (09-05 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募基金持有人半年新增1.61亿户·货基21.48亿户居首</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          证券日报（记者彭衍菘）9月5日报道，基金半年报披露收官，Wind数据显示截至6月底各基金份额持有人户数合计<b>29.58亿户</b>，较2025年末增约1.61亿户；货币基金21.48亿户、半年增5673.64万户居绝对增量首位。<br>
          <b>结构变化：</b>被动指数型基金持有人+2478.8万户、偏股混合+2092.74万户，QDII股票型/混合型分别+1822.58万户、+1248.74万户——工具型产品持续获个人投资者青睐。<br>
          <b>对腾安启示：</b>持有人触达广度扩大，竞争从产品供给转向投后服务与陪伴，须强化风险提示与适当性匹配。
        </div>
        <div class="card-footer">
          <a href="http://www.zqrb.cn/fund/jijindongtai/2026-09-05/A1788514010191.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·09-05</span></a>
        </div>
      </div>

      <!-- S0 Card 4 (09-05 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 中银基金官宣新总裁·督察长陈卫星转任执行总裁</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报（记者若晖）9月5日报道，中银基金公告<b>督察长陈卫星转任执行总裁</b>，陈卫星长期在中国银行总行及深圳分行任职，2022年加入中银基金任督察长、副执行总裁。<br>
          <b>规模体量：</b>截至二季度末中银基金非货规模2777.68亿元（行业第24），公募管理总规模超7000亿元。<br>
          <b>对腾安启示：</b>银行系公募高管内部晋升利于战略延续，养老金融成其新增长点，代销合作可关注其养老产品与母行协同布局。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_5576a9bb06402652" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·09-05</span></a>
        </div>
      </div>

    </div>
  </div>
'''
src = src[:i] + s0_new + src[j:]
print("[S0] OK (block replaced)")

# 5. S6 整段替换（marker 分割）
S6_MARK = '<!-- ============ Section 6: 市场行情速览 ============ -->'
S7_MARK = '<!-- ============ Section 7: 关键时间线 ============ -->'
assert src.count(S6_MARK) == 1 and src.count(S7_MARK) == 1
i = src.index(S6_MARK)
j = src.index(S7_MARK)

s6_new = '''<!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-04）·沪指3930.12 -0.30%·放量下探·成交2.05万亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-04</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-04收盘·放量下探）</b><br>
              上证指数 <b>3930.12</b> <span style="color:#52c41a;">-0.30%</span><br>
              深证成指 <b>13516.97</b> <span style="color:#52c41a;">-0.79%</span><br>
              创业板指 <b>3286.55</b> <span style="color:#52c41a;">-0.78%</span><br>
              沪深京成交 <b>2.05万亿</b>（放量2708亿）<br>
              半导体算力硬件重挫·养殖消费逆势走强
            </div>
            <div>
              <b>港股与美股（09-04收盘）</b><br>
              恒生指数 <b>25650.87</b> <span style="color:#f5222d;">+1.74%</span><br>
              恒生科技 <b>4569.80</b> <span style="color:#f5222d;">+2.27%</span><br>
              国企指数 <b>8555.03</b> <span style="color:#f5222d;">+2.02%</span><br>
              道琼斯 <b>53414.25</b> <span style="color:#52c41a;">-0.51%</span><br>
              纳斯达克 <b>26506.99</b> <span style="color:#52c41a;">-0.29%</span><br>
              标普500 <b>7718.60</b> <span style="color:#52c41a;">-0.38%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:8px;border-top:1px solid #f0f0f0;">
              <b>结构焦点：</b>9月4日A股高开低走、放量下跌，沪指跌0.30%报3930.12，深成指跌0.79%、创业板指跌0.78%，沪深京成交2.05万亿放量2708亿；半导体、算力硬件集体回调，科创50跌2.16%，超2900只个股下跌，养殖、消费逆势走强。港股跟随外围反弹，恒指涨1.74%报25650.87；美股因8月非农大超预期推升加息预期而收跌，道指-0.51%。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-09-04收盘</span>
            <span class="source-tag">数据来源：新华社/国际金融报/证券时报（09-04）</span>
          </div>
      </div>  </div>
'''
src = src[:i] + s6_new + src[j:]
print("[S6] OK (block replaced)")

# 6. S7 时间线：删最旧 08-28 / 08-29，顶部新增 09-05 / 09-04
old_0829 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-29</div>
        <div class="timeline-title">盈利投资者占比披露超2000只·1081只超90%</div>
      </div>
'''
old_0828 = '''      <!-- 08-28 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-28</div>
        <div class="timeline-title">16只创业板算力/金融科技ETF闪电获批</div>
      </div>
'''
new_items = '''            <!-- 09-05 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-05</div>
        <div class="timeline-title">首批10家基金上报科创债场外指数基金</div>
      </div>
            <!-- 09-04 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-04</div>
        <div class="timeline-title">A股放量下跌·沪指3930.12收跌0.30%</div>
      </div>
'''

assert src.count(old_0829) == 1, "0829 anchor"
assert src.count(old_0828) == 1, "0828 anchor"
src = src.replace(old_0829, '')
src = src.replace(old_0828, '')

# 在 S7 容器开场后插入新条目（锚点：09-04 已有条目之前）
anchor = '''    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
            <!-- 09-04 时间线条目 (NEW) -->'''
assert src.count(anchor) == 1, "S7 container anchor"
src = src.replace(anchor, '''    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
''' + new_items + '''            <!-- 09-04 时间线条目 (NEW) -->''')
print("[S7] OK")

# 7. 校验
open_div = src.count('<div')
close_div = src.count('</div>')
print(f"div balance: open={open_div} close={close_div}")
assert open_div == close_div, "DIV IMBALANCE"

assert 'S8' not in src, "S8 leaked!"
assert '今日焦点（' not in src and '今日焦点 (' not in src, "S0 title polluted"

# 关键 marker 完整性
for mk in ['Section 0: 今日焦点', 'Section 1: 重磅信息', 'Section 2: 监管政策',
           'Section 6: 市场行情速览', 'Section 7: 关键时间线']:
    assert mk in src, f"missing marker {mk}"

open(HTML, 'w', encoding='utf-8').write(src)
print("\n✅ index.html written, all assertions passed")
