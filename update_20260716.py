# -*- coding: utf-8 -*-
import re, sys

P = "index.html"
src = open(P, encoding="utf-8").read()
errs = []

def assert_once(sub, label):
    c = src.count(sub)
    if c != 1:
        errs.append(f"[FAIL] {label}: count={c}")
        return False
    return True

# ---------- Phase 1: anchor pre-check ----------
checks = [
    ("<!-- daily-update: 2026-07-15 -->", "daily-update marker"),
    ("数据区间：2026.07.01 — 2026.07.15（每日更新）", "date-badge"),
    ("今日焦点（7月15日·周三·清盘271只创新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交）", "S0 section-title"),
    ("清盘271只创新高|翻倍基瘦身225至74|费率改革三周年|主动ETF申请递交|半导体设备领涨", "meta keywords"),
    ("<!-- S0 Card 1:", "S0 first card comment"),
    ("<!-- ============ Section 1: 重磅信息 ============ -->", "Section 1 marker"),
    ("金融产品网络营销管理办法9月30日施行", "S1 07-01 card"),
    ("上交所《交易规则(2026修订)》7月6日实施", "S2 07-01 card"),
    ("2026年7月15日（周三）·A股开盘涨跌不一·创业板指高开0.74%·半导体设备/存储/光纤活跃·油气黄金走弱", "S6 card-title"),
    ('<div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">', "S7 timeline container"),
]
for sub, lbl in checks:
    assert_once(sub, lbl)

if errs:
    print("\n".join(errs))
    sys.exit(123)

# ---------- Phase 2: apply edits ----------

# Header
src = src.replace("<!-- daily-update: 2026-07-15 -->", "<!-- daily-update: 2026-07-16 -->", 1)
src = src.replace("数据区间：2026.07.01 — 2026.07.15（每日更新）", "数据区间：2026.07.02 — 2026.07.16（每日更新）", 1)
src = src.replace("今日焦点（7月15日·周三·清盘271只创新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交）",
                  "今日焦点（7月16日·周四·二季报科技调仓分歧·货基破1%·首披十年业绩·举牌创新药）", 1)
old_meta = "清盘271只创新高|翻倍基瘦身225至74|费率改革三周年|主动ETF申请递交|半导体设备领涨"
new_meta = "二季报科技调仓分歧|货基315只破1%|二季报首披十年业绩|公募举牌创新药|天弘领罚单"
assert src.count(old_meta) == 2
src = src.replace(old_meta, new_meta)

# Stats Bar
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

# S0 cards rebuild
i = src.index("<!-- S0 Card 1:")
j = src.index("<!-- ============ Section 1: 重磅信息 ============ -->")
S0_CARDS = '''      <!-- S0 Card 1: 基金二季报科技调仓现分歧·多只绩优基金维持高仓位 (T+0 07-16) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 基金二季报科技调仓现分歧·多只绩优基金维持高仓位·半导体估值高企进入业绩验证</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>调仓分歧：</b>截至7月16日，已有72只公募基金披露二季报。上半年领涨的科技板块出现明显内部分歧：融通先进制造一季度重仓的新易盛、长飞光纤、工业富联等8只个股二季度集体退出前十大重仓；但中欧、平安、融通、红土创新、金信等多家公募旗下绩优基金仍对科技股维持高仓位，多只产品单季取得超高收益。<br>
          <b>验证阶段：</b>基金经理普遍认为市场再平衡而非趋势逆转，AI交易主线从炒算力建设转向验证盈利兑现；国产半导体旺季扩产、存储涨价支撑中期逻辑，但短期波动率加大。<br>
          <b>对基金行业影响：</b>科技"高景气+高波动"→腾安需强化行业轮动与哑铃配置话术，提示客户关注中报验证。
        </div>
        <div class="card-footer">
          <a href="https://www.aastocks.com/tc/stocks/analysis/stock-aafn-con/06869/GLH/GLH2555570L/hk-stock-news" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·人民财讯</span></a>
          <span class="impact-tag high">二季报调仓：高</span>
        </div>
      </div>

      <!-- S0 Card 2: 超300只货基7日年化跌破1%·收益率持续走低 (T+0 07-16) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 超300只货基7日年化收益率跌破1%·315只破线·部分产品恢复/下调管理费</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>收益探底：</b>Wind统计显示，截至7月13日，全市场已有<b>315只</b>货币市场型基金7日年化收益率跌破<b>1%</b>；在超低利率环境下，货基作为最大品类的"现金管理"吸引力明显走弱。<br>
          <b>费率浮动：</b>多家基金公司集中公告，旗下货基相继恢复常规管理费率，亦有部分产品宣布下调管理费——费率浮动均指向基金收益率持续走低、竞争加剧。<br>
          <b>对基金行业影响：</b>货基收益破1%→现金管理需求外溢至短债/同业存单指数基金→腾安可顺势丰富闲钱理财货架与话术。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1UOOTKO0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">货基收益：中</span>
        </div>
      </div>

      <!-- S0 Card 3: 公募二季报首披十年长期业绩·信披新规落地首批 (T+0 07-16) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募二季报首披十年长期业绩·72只已披露·9只十年净值增长超300%·长期导向凸显</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>新规落地：</b>2026年二季报是证监会修订《公开募集证券投资基金信息披露内容与格式准则第2号》落地后的首批定期报告，成立满七/十年的基金首次披露过去7年、10年长期业绩。截至7月14日已有72只披露二季报，其中14只满十年基金均披露十年业绩，<b>9只净值增长率超300%</b>。<br>
          <b>考核转型：</b>同步落地的《基金管理公司绩效考核管理指引》强调"长周期考核""薪酬与投资者利益绑定"，公募考核指挥棒从规模/短期排名系统性转向长期主义。<br>
          <b>对基金行业影响：</b>长期业绩披露常态化→腾安选品可更多用中长期胜率说话，弱化短期排名营销。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_8826a5837f602552" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">信披新规：中</span>
        </div>
      </div>

      <!-- S0 Card 4: 头部公募密集举牌创新药·易方达/华夏/富国/汇添富增持 (T+0 07-16) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 头部公募密集调研举牌创新药·易方达/华夏/富国/汇添富6.10-7.11增持构成举牌</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>举牌潮：</b>港交所披露，6月10日至7月11日，易方达、华夏、富国、汇添富等多家头部公募出手增持创新药公司并构成举牌；自科技"硬科技"上半年吸金后，6月起公募调研风向明显切换，机构频频组团走访生物医药企业。<br>
          <b>风格切换：</b>业内认为这是资金从极致科技向医药等洼地再平衡的信号，创新药在政策（医保谈判温和化）+出海（BD大单）双驱动下重获机构青睐。<br>
          <b>对基金行业影响：</b>创新药成为再平衡主线→腾安可加大医药/创新药基金货架与投教，把握板块轮动机遇。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1UOOTKO0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">举牌创新药：中</span>
        </div>
      </div>'''
src = src[:i] + S0_CARDS + "\n    </div>\n  </div>\n" + src[j:]

# Helper: replace a card by a unique marker substring
def replace_card_by_marker(marker, new_card):
    global src
    pos = src.index(marker)
    start = src.rfind('\n      <div class="card', 0, pos) + 1
    rest = src[start:]
    m = re.search(r'\n      </div>\n', rest)
    end = start + m.end()
    src = src[:start] + new_card + src[end:]

# S1: replace 07-01 网络营销 card with 发行再平衡 card
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
replace_card_by_marker("金融产品网络营销管理办法9月30日施行", S1_NEW)

# S2: replace 07-01 交易规则 card with 天弘罚单 card
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
replace_card_by_marker("上交所《交易规则(2026修订)》7月6日实施", S2_NEW)

# S6: replace the single card (07-15) with 07-16 card
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

# S7: rebuild timeline (remove 07-01, add 07-16, single-event titles)
c_open = '<div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">'
ci = src.index(c_open)
rest = src[ci:]
m = re.search(r'    </div>\n  </div>\n', rest)
ce = ci + m.end()
TIMELINE = '''      <!-- 07-16 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-16</div>
        <div class="timeline-title">A股集体低开·半导体算力硬件领跌</div>
      </div>

      <!-- 07-15 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-15</div>
        <div class="timeline-title">上半年公募基金清盘271只创近7年新高</div>
      </div>

      <!-- 07-13 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-13</div>
        <div class="timeline-title">首批公募二季报亮相</div>
      </div>

      <!-- 07-11 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-11</div>
        <div class="timeline-title">公募二季报披露拉开帷幕</div>
      </div>

      <!-- 07-10 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-10</div>
        <div class="timeline-title">科创50ETF 7月吸金96亿</div>
      </div>

      <!-- 07-09 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-09</div>
        <div class="timeline-title">科创债ETF全市场24只纳入回购质押库</div>
      </div>

      <!-- 07-08 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-08</div>
        <div class="timeline-title">自由现金流产品规模年内+42.79%</div>
      </div>

      <!-- 07-07 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-07</div>
        <div class="timeline-title">A股三大指数集体低开·半导体芯片领跌</div>
      </div>

      <!-- 07-06 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-06</div>
        <div class="timeline-title">A股交易新规7月6日正式实施</div>
      </div>

      <!-- 07-05 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-05</div>
        <div class="timeline-title">美股基金周流出172亿美元</div>
      </div>

      <!-- 07-03 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-03</div>
        <div class="timeline-title">上半年新基金发行883只</div>
      </div>

      <!-- 07-02 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-02</div>
        <div class="timeline-title">A股三大股指大幅低开</div>
      </div>'''
src = src[:ci] + c_open + "\n" + TIMELINE + "\n    </div>\n  </div>\n" + src[ce:]

# ---------- Quality checks ----------
opens = src.count("<div")
closes = src.count("</div>")
assert opens == closes, f"DIV IMBALANCE opens={opens} closes={closes}"
assert "待办跟踪" not in src, "S8 残留 detected!"
assert '<!-- ============ Section 8' not in src, "S8 section re-created!"

open(P, "w", encoding="utf-8").write(src)
print("OK: update applied")
print(f"div opens={opens} closes={closes} balanced={opens==closes}")
print("S8 absent:", "待办跟踪" not in src)
