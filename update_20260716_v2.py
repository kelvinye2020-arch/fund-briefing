# -*- coding: utf-8 -*-
import re, sys

P = "index.html"
src = open(P, encoding="utf-8").read()
errs = []

def need(cond, msg):
    if not cond:
        errs.append("[FAIL] " + msg)

# Structure anchors that MUST exist
need(src.count("<!-- S0 Card 1:") == 1, "S0 Card 1 comment")
need(src.count("<!-- ============ Section 1: 重磅信息 ============ -->") == 1, "Section 1 marker")
need(src.count('<div class="stats-bar">') == 1, "stats-bar")
need(src.count("<!-- ============ Section 6: 市场行情速览 ============ -->") == 1, "Section 6 marker")
need(src.count("<!-- ============ Section 7: 关键时间线 ============ -->") == 1, "Section 7 marker")
if errs:
    print("\n".join(errs)); sys.exit(123)

def replace_card_by_marker(marker, new_card):
    global src
    if marker not in src:
        return False
    pos = src.index(marker)
    start = src.rfind('\n      <div class="card', 0, pos) + 1
    rest = src[start:]
    m = re.search(r'\n      </div>\n', rest)
    end = start + m.end()
    src = src[:start] + new_card + src[end:]
    return True

# ---------- Stats Bar refresh ----------
i = src.index('<div class="stats-bar">')
j = src.index('\n<div class="main">', i)
new_stats = '''<div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">271只</div>
      <div class="stat-label">上半年公募基金清盘（创近7年新高·发起式占比过半·同质化加速出清）</div>
      <div class="stat-change up">▲ 行业从"快车道"驶向"稳车道"·迷你发起式成高发地</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3912.38</div>
      <div class="stat-label">上证综指 · 07-16低开-1.09%·盘中跌幅收窄·半导体算力硬件领跌</div>
      <div class="stat-change down">▼ 创业板-2.48%→-1.21%·科创50-2.82%→-0.59%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">315只</div>
      <div class="stat-label">货基7日年化跌破1%（收益率持续走低·部分恢复/下调管理费）</div>
      <div class="stat-change down">▼ 超低利率下现金管理吸引力走弱·需求外溢短债</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">41只</div>
      <div class="stat-label">本周新基发行（权益占58.54%·红利偏债12只·再平衡并行）</div>
      <div class="stat-change neutral">■ 供给结构均衡化·攻守兼备</div>
    </div>
  </div>'''
src = src[:i] + new_stats + src[j:]

# ---------- S1: remove expired 07-01 card, add 发行再平衡 (07-16) ----------
S1_NEW = '''      <!-- S1 Card NEW: 公募基金发行再平衡·科技与红利共发·本周41只新基 (07-16) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募基金发行再平衡·科技与红利共发·本周41只新基·权益占58.54%·红利偏债12只</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>供给均衡：</b>公募排排网数据，7月13日—19日全市场41只新基开启募集，较前一周增7.89%；权益类24只占58.54%，但科技主题已非单一主角，产品拓展至化工、医药、地产、新能源等多元方向。<br>
          <b>防御补位：</b>41只中红利主题+偏债型基金合计12只、占近三成；多家公募在把握科技主线同时加快布局红利等低波动产品，产品矩阵"攻守兼备"。<br>
          <b>对基金行业影响：</b>发行结构再平衡→腾安货架应从单一科技扩至"科技+红利+固收"组合，匹配再平衡下的客户配置需求。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260716015132a6d61334" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯证券·上海证券报</span></a>
          <span class="impact-tag medium">发行再平衡：中</span>
        </div>
      </div>'''
r1 = replace_card_by_marker("金融产品网络营销管理办法9月30日施行", S1_NEW)
print("S1 expired 07-01 card replaced:", r1)

# ---------- S2: remove expired 07-01 card, add 天弘罚单 (07-16) ----------
S2_NEW = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 天弘基金领罚单·未报送QDII境外投资报告·外汇局天津分局警告+罚4万·5年多来首次受罚</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>合规罚单：</b>6月底，国家外汇管理局天津市分局对天弘基金出具罚单：因未按规定报送财务会计报告、统计报表等资料，给予警告并罚款4万元。这是天弘基金5年多来首次受监管处罚，亦折射QDII等跨境业务数据报送合规要求趋严。<br>
          <b>行业警示：</b>业内指出，4万元罚款处法定区间低位、属操作性失误，但反映监管对金融数据报送及时性、准确性要求持续收紧；万亿级机构的内控细节不能因"规模光鲜"而被忽视。<br>
          <b>对基金行业影响：</b>跨境业务合规收紧→腾安代销QDII产品需关注机构报送合规状态，强化合作机构合规筛查。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/cj/2026-07-16/doc-inihycsk4447612.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag medium">QDII合规：中</span>
        </div>
      </div>'''
r2 = replace_card_by_marker("上交所《交易规则(2026修订)》7月6日实施", S2_NEW)
print("S2 expired 07-01 card replaced:", r2)

# ---------- S6: rewrite to 07-16 data ----------
S6_TITLE_OLD = "2026年7月15日（周三）·A股震荡收跌·沪指3955.58（-0.29%）·半导体跳水·医药银行护盘"
if S6_TITLE_OLD in src:
    s6a = src.index("<!-- ============ Section 6: 市场行情速览 ============ -->")
    s7a = src.index("<!-- ============ Section 7: 关键时间线 ============ -->")
    sec6 = src[s6a:s7a]
    card_start = sec6.index('          <div class="card p3">')
    sec_close = sec6.rfind('\n  </div>\n')
    S6_CARD = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月16日（周四）·A股集体低开·半导体算力硬件领跌·盘中跌幅收窄·港股逆势高开</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-16开盘（集体低开·盘中跌幅收窄）：</b><br>
              ▪ 沪指 <b>-1.09%</b>（3912.38）·深成指 <b>-1.91%</b>（14497.43）<br>
              ▪ 创业板指 <b>-2.48%</b>（3710.51）→10:32 <b>-1.21%</b>（3758.83）·科创50 <b>-2.82%</b>（1869.94）→<b>-0.59%</b>（1913.01）<br>
              ▪ 板块：存储芯片/CPO/PCB/半导体集体领跌（德明利、江丰电子等跌停）；AI手机概念逆势活跃；早盘超4200股下跌，随后跌幅收窄
            </div>
            <div>
              <b>📊 港股07-16（逆势高开·资金回流）：</b><br>
              ▪ 恒指 <b>+0.58%</b>（24825.02）→10:34 <b>+1.75%</b>（25113.41）·恒生科指高开0.15%后涨幅扩大<br>
              ▪ 阿里巴巴涨超5%、腾讯涨超2%；韩国央行意外加息25bp致KOSPI重挫，资金回流港股；创新药概念活跃<br>
              <b>📊 美股07-15隔夜：</b>标普+0.38%·道指+0.30%·纳指+0.62%；苹果+4%创新高（AI携手阿里完成备案），阿里+5%、中概+3%；芯片股回落（SK海力士-9%、英伟达盘中-3%收涨）
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-16（周四开市·07-16盘中/07-15隔夜）</span>
            <span class="source-tag">数据来源：腾讯财经/新浪/每经/网易财经/AAStocks</span>
          </div>
      </div>'''
    src = src[:s6a+card_start] + S6_CARD + src[s6a+sec_close:]
    print("S6 rewritten to 07-16: True")
else:
    print("S6 already 07-16 or marker changed: skip")

# ---------- Quality checks ----------
opens = src.count("<div"); closes = src.count("</div>")
need(opens == closes, f"DIV IMBALANCE opens={opens} closes={closes}")
need("待办跟踪" not in src, "S8 残留 detected!")
need('<!-- ============ Section 8' not in src, "S8 section re-created!")
# no expired 07-01 in S1/S2
need("金融产品网络营销管理办法9月30日施行" not in src, "S1 still has expired 07-01")
need("上交所《交易规则(2026修订)》7月6日实施" not in src, "S2 still has expired 07-01")
need(S6_TITLE_OLD not in src, "S6 still 07-15")
if errs:
    print("\n".join(errs)); sys.exit(124)

open(P, "w", encoding="utf-8").write(src)
print("OK: completion applied")
print(f"div opens={opens} closes={closes} balanced={opens==closes}")
