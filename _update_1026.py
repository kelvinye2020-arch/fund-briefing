# -*- coding: utf-8 -*-
import re, io, sys
from datetime import date, timedelta

P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = io.open(P, encoding='utf-8').read()
orig_open = len(re.findall(r'<div\b', s))
orig_close = s.count('</div>')
print('BASE open=%d close=%d' % (orig_open, orig_close))

TODAY = date(2026, 10, 26)
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
UPPER = TODAY.strftime('%Y.%m.%d')

def cnt_open(x):
    return len(re.findall(r'<div\b', x))

def rep(old, new, n=1, tag=''):
    global s
    c = s.count(old)
    assert c == n, 'ANCHOR FAIL %s count=%d expect=%d' % (tag, c, n)
    s = s.replace(old, new, 1)
    print('OK %s' % tag)

# ---------------- 1. header badge ----------------
badge_new = '📅 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)
n_badge = len(re.findall(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', s))
assert n_badge == 1, 'badge count %d' % n_badge
s = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge_new, s)
assert ('📅 数据区间：2026.10.12 — 2026.10.26（每日更新）') in s
print('OK badge ->', badge_new)

# ---------------- 2. daily-update marker ----------------
rep('<!-- daily-update: 2026-10-23 -->', '<!-- daily-update: 2026-10-26 -->', 1, 'DU')

# ---------------- 3. fingerprint ----------------
rep('<meta name="content-fingerprint" content="首批18只|ETF资金|证监会部|主动ETF">',
    '<meta name="content-fingerprint" content="运作办法|首批18|公募万亿|逆势放开">', 1, 'FP')

# ---------------- 4. description ----------------
rep('content="首批18只主动ETF今日正式发行|ETF资金10月22日净流入592.83亿元|证监会部署持续深化公募基金改革|主动ETF拟任基金经理集体发声|沪指10-22收3658.03 纳指跌2.60%"',
    'content="运作办法征求意见稿拟下调权益类基金成立门槛至5000万元|首批18只主动ETF首日认购约150亿元|公募万亿活水入科创逾350只科技主题ETF|逆势放开限购万家国企动力混合取消限额|沪指10-23收3690.48 纳指跌0.21%"',
    1, 'DESC')

# ---------------- 5. Stats Bar ----------------
STATS_START = s.find('    <div class="stats-bar">')
STATS_END = s.find('\n\n  </div>\n\n<div class="main">')
assert STATS_START > 0 and STATS_END > STATS_START
seg = s[STATS_START:STATS_END]
assert seg.count('stat-card') == 4, 'stat-card=%d' % seg.count('stat-card')
assert seg.count('<div class="stat-card">') == 4

NEW_STATS = '''    <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">150亿</div>
      <div class="stat-label">首批18只主动ETF首日认购·易方达摩根富国3只一日售罄</div>
      <div class="stat-change up">▲ 7家管理人自购合计约15亿元·券商代销约130亿元</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3690.48</div>
      <div class="stat-label">沪指10-23收盘·涨0.89%·沪深两市成交约1.96万亿元</div>
      <div class="stat-change up">▲ 创业板指涨4.16%·深证成指涨2.79%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1.3万亿</div>
      <div class="stat-label">逾350只科技主题ETF总规模·截至10月23日Wind统计口径</div>
      <div class="stat-change up">▲ 主动股混基金科创板配比26.16%创历史新高</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">5000万</div>
      <div class="stat-label">权益类基金、FOF拟降成立门槛·现为规模2亿元、份额2亿份</div>
      <div class="stat-change neutral">● 运作办法征求意见·反馈截止11月8日</div>
    </div>
'''
s = s[:STATS_START] + NEW_STATS + s[STATS_END:]
print('OK stats open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 6. S0 context ----------------
A0 = s.find('<!-- ============ Section 0')
A1 = s.find('<!-- ============ Section 1')
assert A0 > 0 and A1 > A0
assert s[A0:A1].count('10月23日 · 4条今日要闻') == 1
s = s[:A0] + s[A0:A1].replace('10月23日 · 4条今日要闻', '10月26日 · 4条今日要闻') + s[A1:]
print('OK S0 context')

# ---------------- 7. S0 cards ----------------
A0 = s.find('<!-- ============ Section 0')
CG = s.find('    <div class="card-grid">', A0)
END0 = s.find('\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 1', CG)
assert CG > 0 and END0 > CG
old0 = s[CG:END0]
assert old0.count('<div class="card p') == 4, 'old S0 cards=%d' % old0.count('<div class="card p')

C1 = '''      <!-- S0 Card 1 (10-26 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 运作办法征求意见稿：权益类基金、FOF成立门槛降至5000万元·投顾份额获制度确认</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月26日报道（记者朱妍）：中国证监会近日就新修订形成的《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，修订要点贯穿基金募集、投资运作与存续退出全链条。<br>
          <b>成立门槛下调：</b>股票基金、混合基金、FOF等产品的成立门槛，由规模<b>2亿元</b>、份额<b>2亿份</b>分别降低至<b>5000万元</b>、<b>5000万份</b>，固收类基金成立门槛保持不变。中国基金报10月20日报道（记者曹雯璟）指出，征求意见稿第八条要求基金管理人根据市场容量、流动性、估值水平和自身投资管理能力等因素加强基金产品的逆周期布局管理，第十八条明确上述门槛下调安排。<br>
          <b>投资方向界定：</b>基金名称显示投资方向的，基金合同、招募说明书应当使用可识别或者可量化的方式清晰界定基金名称所示投资方向，且<b>80%以上</b>的基金总资产属于投资方向确定的内容。<br>
          <b>新增类别与投顾份额：</b>修订在主流产品外新增期货和衍生品基金类别，股指期货和国债期货轧差后可计入对应资产；同时明确基金管理人可针对个人养老金、基金投资顾问及中国证监会规定的其他业务设立单独的份额类别，按规定对管理费、托管费实施费率优惠，业内期待已久的“投顾份额”有望在制度层面得到确认。<br>
          <b>配套要求：</b>要求混合基金明确约定各类资产的配置比例，并分类别提出针对性监管要求，促进混合基金风险评级与实际风险特征相匹配。<br>
          <b>对腾安启示：</b>成立门槛下调后，小规模、短成立年限的新产品供给将明显增加，货架选品须把“成立规模、成立时间、流动性、策略稳定性”从加分项升为必审项，不得以“新规支持逆周期发行”暗示产品风险更低；基金名称与投资方向的80%量化界定属合同约束，对客标签须与基金合同口径一致，不得沿用“赛道标签”式简称；投顾份额若落地，涉及单独份额类别与费率优惠，须在详情页区分同一产品不同份额的费率与适用业务，不得与普通份额混排展示。
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-10/26/content_2280964.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-26</span></a>
          <a href="https://www.chnfund.com/article/AR857f0933-5782-3e6a-f9ce-3a2468f9979f" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-20</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 选品口径→把“成立门槛降至5000万元”解读为产品数量可能增加而非风险下降，新发与小规模产品的展示须补充成立规模、成立年限与流动性字段；<br>
            ② 名称合规→产品标签须与基金合同约定的投资方向界定一致，禁止用赛道简称或热点词汇替代合同口径；<br>
            ③ 投顾份额→如后续落地，须在费率页单独列示投顾份额对应的管理费、托管费优惠与适用业务范围，不得与普通份额混排。
          </div>
        </div>
      </div>'''

C2 = '''      <!-- S0 Card 2 (10-25 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批18只主动ETF首日认购约150亿元·易方达摩根富国3只一日售罄</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-25</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻10月25日报道（记者彭水萍、编辑肖芮冬）：<b>10月23日</b>，境内首批18只主动管理型ETF正式开售，发行首日合计认购规模约<b>150亿元</b>。摩根大盘成长主动股票ETF、易方达品质均衡主动管理ETF、富国价值优选量化选股主动ETF先后触及<b>20亿元</b>首次募集规模上限并宣布提前结束募集，对有效认购申请采取比例配售；其中易方达与摩根旗下产品在当日下午2点20分左右便宣布达到募集上限。<br>
          <b>其余产品：</b>华夏基金、大成基金旗下产品首日募集规模也超过<b>10亿元</b>，其他已开售产品中另有多只落在<b>5亿元至10亿元</b>区间；若18只产品后续全部触及20亿元上限，预计将为A股带来约<b>360亿元</b>增量资金。<br>
          <b>自购与渠道：</b>截至10月24日，易方达、华夏、富国、汇添富4家管理人各运用固有资金自购<b>2亿元</b>，华安、工银瑞信各<b>1亿元</b>，6家合计<b>10亿元</b>；加上摩根基金股东通过摩根资产管理（亚太）有限公司以<b>7500万美元</b>（约合<b>5亿元</b>人民币）的投资，7家管理人自购总额合计约<b>15亿元</b>。渠道端，券商贡献的销售规模约<b>130亿元</b>，其中国泰海通发行首日销售规模约<b>40亿元</b>。<br>
          <b>产品机制：</b>首批18只产品中<b>15只</b>采用双基金经理配置，最常见组合为“一名主动管理基金经理＋一名指数化投资经理”；管理费统一为<b>1%</b>、托管费<b>0.1%—0.15%</b>；按沪深交易所业务指引，单只产品持股不少于<b>30只</b>、前十大重仓合计不超过<b>60%</b>，并每日披露申购赎回清单（PCF）。<br>
          <b>对腾安启示：</b>“一日售罄”“比例配售”属募集进度结果，对客展示须与产品业绩、风险等级严格分离，不得演绎为热度推荐或收益预期；自购为管理人及股东固有资金的认购安排，须标注拟认购金额、持有承诺与实施前提，摩根部分须注明为股东通过关联方投入且于基金上市后开展；比例配售意味着实际确认份额可能低于申请份额，须在认购流程中前置说明确认与退款规则。
        </div>
        <div class="card-footer">
          <a href="https://www.nbd.com.cn/articles/2026-10-25/4616270.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·10-25</span></a>
          <a href="https://news.qq.com/rain/a/20261024A08E4K00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·央视财经·10-24</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>'''

C3 = '''      <!-- S0 Card 3 (10-26 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募万亿活水入科创·逾350只科技主题ETF合计规模约1.3万亿元</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          证券时报10月26日报道（记者余世鹏）：公募基金正以万亿级科技产品矩阵，把分散的居民财富聚拢为浇灌硬科技的“源头活水”。据Wind统计，截至<b>10月23日</b>，纳入统计的逾<b>350只</b>科技主题ETF总规模约<b>1.3万亿元</b>，呈三个层次——一是科创板宽基ETF，<b>20只</b>产品合计规模近<b>2000亿元</b>、单只最大规模超千亿元，科创100、科创综指、科创200等逾<b>40只</b>科创板细分宽基品种规模近<b>300亿元</b>；二是半导体、芯片ETF，芯片整体、芯片设计、半导体材料设备、中韩半导体等均有独立指数与产品，单只最大规模超<b>400亿元</b>；三是人工智能、算力、通信、5G、卫星等赛道细分环节，均出现百亿级规模产品。<br>
          <b>主动端配比：</b>券商统计数据显示，截至二季度末，主动权益基金规模接近<b>5万亿元</b>，主动股混基金在创业板、科创板的市值配置比例分别为<b>29.85%</b>、<b>26.16%</b>，较上季度末分别增加<b>4.40个</b>和<b>9.83个</b>百分点，公募在科创板上的配比创历史新高；重仓市值前十的股票中有<b>九只</b>为以AI产业链为代表的科技公司。<br>
          <b>时差错配：</b>报道指出，当短期排名的指挥棒遇上十年磨一剑的技术周期，当追涨杀跌的申赎习惯撞上科技资产的高波动，资金与产业之间的“时差错配”开始显现；公募赋能科创的真正考题已不再是规模够不够大，而是这套以年度为刻度运转的资管体系，能否长出匹配科技长周期的机制与耐心。<br>
          <b>对腾安启示：</b>科技主题ETF数量逾350只、规模约1.3万亿元，货架须按“科创板宽基／半导体芯片／AI算力通信”三层结构分类展示，避免以“科技”单一标签堆叠同质产品；主动股混基金科创板配比创新高属持仓统计，须标注统计时点与口径来源，不得演绎为板块行情判断；“时差错配”提示须转化为持有期与波动风险的对客说明，不得以长期产业逻辑替代短期回撤提示。
        </div>
        <div class="card-footer">
          <a href="https://fund.10jqka.com.cn/20261026/c681059289.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·证券时报·10-26</span></a>
          <a href="https://www.nbd.com.cn/articles/2026-10-26/4617109.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·10-26</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''

C4 = '''      <!-- S0 Card 4 (10-26 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 逆势放开限购·万家国企动力混合自10月26日起取消5万元大额申购限制</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报10月26日报道（本报记者万宇）：市场调整之际，部分主动权益基金逆势放宽甚至取消限购，其中不乏知名基金经理管理的产品。万家基金<b>10月24日</b>公告，为满足广大投资者需求，自<b>10月26日</b>起取消对万家国企动力混合单日单个基金账户单笔或多笔累计金额<b>5万元以上</b>的大额申购（含转换转入、定期定额投资）限制，该调整适用于全部分级份额，万家国企动力混合A与C同步恢复大额申购权限。<br>
          <b>其他案例：</b>易方达基金<b>10月19日</b>公告，自10月20日起，基金经理郑希管理的易方达信息行业精选股票、易方达信息产业混合取消单日单个基金账户在全部销售机构累计申购不超过<b>50万元</b>（含）的限制，恢复办理大额申购与转换转入；其管理的QDII基金易方达全球成长精选混合同步恢复申购及定投，人民币份额恢复单日不超过<b>1万元</b>、美元份额不超过<b>1400美元</b>，为该基金自7月初暂停申购后首次放开。上海国泰海通证券资产管理有限公司自10月19日起恢复国泰海通创新成长混合的大额申购及定投业务。<br>
          <b>机构判断：</b>业内人士表示，市场经历调整后放宽申购，是公募机构基于对中长期市场机会的判断，避免投资者在低位因限购而错失布局机会；华夏基金基金经理徐猛表示，从估值角度看，经历前期调整后A股和港股部分板块的估值水平已回落至历史相对较低区间，权益资产的配置性价比逐步显现。<br>
          <b>对腾安启示：</b>限购放开属申购安排调整，对客展示须标注生效日期与具体限额，不得解读为基金经理看多或市场见底信号；QDII恢复申购涉及额度与币种限制，须同步提示汇率与额度风险；同一产品A/C份额、人民币/美元份额的限额差异须分别列示，不得以“取消限购”概括全部份额。
        </div>
        <div class="card-footer">
          <a href="https://epaper.cs.com.cn/zgzqb/html/2026-10/26/nw.D110000zgzqb_20261026_2-J02.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·10-26</span></a>
          <a href="https://www.cs.com.cn/tzjj/01/2026/10/26/detail_2026102610047052.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·中国证券报·10-26</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''

NEW0 = '    <div class="card-grid">\n\n' + '\n\n'.join([C1, C2, C3, C4]) + '\n'
s = s[:CG] + NEW0 + s[END0:]
print('OK S0 cards open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 8. S1 delete 10-11 card ----------------
c1 = s.find('<!-- S1 Card: 顶流大V')
c2 = s.find('<!-- S1 Card: 内地公募香港子公司')
assert c1 > 0 and c2 > c1
blk = s[c1:c2]
assert blk.count('<div class="card p') == 1, 'S1 del block cards=%d' % blk.count('<div class="card p')
s = s[:c1] + s[c2:]
print('OK S1 delete open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 9. S1 insert new card ----------------
anchor_s1 = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 2'
assert s.count(anchor_s1) == 1, 'S1 anchor=%d' % s.count(anchor_s1)
S1C = '''
      <!-- S1 Card: 基金三季报密集披露 科技持仓回撤引发集体反思 (10-26 P1) -->

      <div class="card p1">

        <div class="card-top">

          <div class="card-title">🟡 基金三季报密集披露·科技持仓回撤引发基金经理集体反思·四季度应对风格再平衡</div>

          <div class="card-meta">

            <span class="priority-tag important">P1 重要关注</span>

            <span class="date-tag">10-26</span>

          </div>

        </div>

        <div class="card-body">

          上海证券报10月26日报道（记者陈玥）：随着2026年基金三季报陆续披露，重仓科技股的主动权益类基金净值出现回撤，多位基金经理在季报中就操作得失作出说明。<br>

          <b>反思样本：</b>中欧科技成长混合基金经理杜厚良在三季报中表示，一是对流动性冲击的预判和应对不足——二季度末组合股票仓位接近满仓、持仓集中在AI算力硬件方向，外部流动性收缩、A股科技成长板块在7月调整时没有及时降低组合波动、分散持仓，回撤幅度明显大于基准；二是港股配置比例较高——二季度末组合港股持仓市值约占基金资产净值的<b>30%</b>，所持港股标的多为中小市值科技硬件公司、交易流动性偏弱，市场波动加大使流动性折价放大，调仓冲击成本偏高。<br>

          <b>坚守样本：</b>中欧科创主题混合基金经理邵洁、卢纯青在三季报中表示，市场调整主要由交易结构变化驱动而非产业趋势逆转，因此在下跌过程中逐步将主要投资方向朝AI产业链集中，并以模型能力能否持续提升、CAPEX（资本性支出）是否继续高增长、AI对社会和就业的冲击是否过大三项指标作为判断AI行情的关键。<br>

          <b>应对再平衡：</b>平安研究智选混合基金经理张荫先认为，本轮AI赛道行情的演变与2021年初“茅指数”行情有共同点，“短期市场是投票机，长期市场终将是称重机”；银河基金量化与FOF投资部基金经理蒋敏表示，再平衡本质上是极致行情发生后风格分化的均值回归，应在成长主线与价值红利之间动态倾斜、在行业上关注受益于能源涨价的上游资源与低估值板块，并沿均值回归过程分批动态再优化。<br>

          <b>对腾安启示：</b>三季报中的持仓调整与归因属基金经理事后说明，对客展示须标注报告期与发言人，不得摘取“回调释放估值压力”“依然看好AI”一类表述作为买入建议；港股持仓占比较高导致的流动性折价与调仓冲击成本属组合运作风险，相关产品须同步提示跨境流动性与汇率因素；风格再平衡的讨论应转化为“分散配置、分批参与”的持有期提示，不得简化为板块轮动推荐。

        </div>

        <div class="card-footer">

          <a href="https://www.cnstock.com/commonDetail/810112" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-26</span></a>

          <a href="https://finance.china.com.cn/money/fund/20261026/6326741.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网财经·上海证券报·10-26</span></a>

          <span class="impact-tag medium">影响：中</span>

        </div>

      </div>'''
i1 = s.find(anchor_s1)
s = s[:i1] + S1C + s[i1:]
print('OK S1 insert open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 10. S2 delete two 10-09 cards ----------------
cA = s.find('<!-- S2 Card: 新规落地首周')
cB = s.find('<!-- S2 Card: 中基协发布后续职业培训大纲')
assert cA > 0 and cB > cA and s[cA:cB].count('<div class="card p') == 1
s = s[:cA] + s[cB:]
print('OK S2 del A open=%d close=%d' % (cnt_open(s), s.count('</div>')))

anchor_s2 = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 3'
assert s.count(anchor_s2) == 1, 'S2 anchor=%d' % s.count(anchor_s2)
cC = s.find('<!-- S2 Card: 百亿私募杭州图灵')
eC = s.find(anchor_s2)
assert cC > 0 and eC > cC and s[cC:eC].count('<div class="card p') == 1
s = s[:cC] + s[eC:]
print('OK S2 del C open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 11. S2 insert two new cards ----------------
assert s.count(anchor_s2) == 1
S2A = '''
      <!-- S2 Card: 中基协集中修订八项基金估值指引 (10-22 P1 / A级官方源) -->

      <div class="card p1">

        <div class="card-top">

          <div class="card-title">🟡 中基协集中修订八项基金估值指引·中基协字〔2026〕349号·反馈截止10月30日</div>

          <div class="card-meta">

            <span class="priority-tag important">P1 重要关注</span>

            <span class="date-tag">10-22</span>

          </div>

        </div>

        <div class="card-body">

          中国证券投资基金业协会<b>10月22日</b>发布中基协字〔2026〕349号通知（落款2026年10月19日）：为进一步规范证券投资基金的估值业务，协会对已发布估值指引进行评估，拟对《证券投资基金停牌股票投资估值指引》等<b>八项</b>自律规则作出修订并公开征求意见，意见反馈截止时间为<b>10月30日</b>。<br>

          <b>扩展适用范围：</b>《黄金交易型开放式证券投资基金估值指引》纳入黄金集中定价合约交易；《证券投资基金港股通投资估值指引》纳入香港联合交易所上市基金；《证券投资基金投资资产管理产品估值指引》纳入除证券投资基金外的其他资产管理产品；《证券投资基金投资流通受限证券估值指引》纳入首次公开发行时取得的带限售期的股票、存托凭证、公募REITs，以及通过定向可转债转股等方式取得的带限售期的股票；《证券投资基金固定收益品种投资估值指引》纳入境外交易所上市的固定收益品种。<br>

          <b>细化业务场景：</b>《证券投资基金停牌股票投资估值指引》增加ETF和ETF联接基金持有停牌股票的估值处理，同时将北交所股票纳入AMAC指数；《证券投资基金港股通投资估值指引》增加港股通投资的供股权证的估值处理；《私募投资基金非上市股权投资估值指引》进一步明确新三板挂牌但交易不活跃企业的估值处理，并在收益法下增加股利折现法。修订同时删除会计核算相关规定、修改部分自律规则名称。<br>

          <b>修订背景：</b>协会自2012年起陆续发布会计核算和估值业务自律规则共计<b>十五项</b>，部分规则因发布年份较早，逐渐出现投资品种不全、业务场景缺失等问题。<br>

          <b>对腾安启示：</b>估值指引直接决定净值计算口径，涉及黄金ETF、港股通产品、公募REITs、限售股与境外固收品种的展示页须同步更新估值方法说明，不得沿用旧口径解释净值波动；北交所股票纳入AMAC指数、ETF持有停牌股处理规则变化，可能导致个别产品估值切换时出现净值跳变，相关提示须前置；本次修订处于征求意见阶段、尚未生效，对客材料不得表述为已实施规则。

        </div>

        <div class="card-footer">

          <a href="https://www.amac.org.cn/xwfb/tzgg/202610/t20261022_28187.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券投资基金业协会·10-22</span></a>

          <a href="https://www.jjckb.cn/20261022/388491cfbff442be84fd609958dd45f1/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济参考网·10-22</span></a>

          <span class="impact-tag high">影响：高</span>

        </div>

      </div>'''

S2B = '''
      <!-- S2 Card: 机构监管通报优化新模式浮动费率产品注册安排 (10-26 P1) -->

      <div class="card p1">

        <div class="card-top">

          <div class="card-title">🟡 机构监管通报优化新模式浮动费率产品注册安排·头部不低于60%·中型不低于30%</div>

          <div class="card-meta">

            <span class="priority-tag important">P1 重要关注</span>

            <span class="date-tag">10-26</span>

          </div>

        </div>

        <div class="card-body">

          上海证券报10月26日报道（记者赵明超）：近期监管部门发布机构监管通报《优化新模式浮动费率产品注册安排 纵深推进公募基金改革》，按照分类监管、稳步推进的原则，将新模式浮动管理费产品的参与机构范围拓展至主动权益类基金管理规模居前的中型基金管理人。<br>

          <b>差异化安排：</b>头部基金管理人发行的新模式浮费产品数量，原则上不低于其主动管理权益类基金发行数量的<b>60%</b>；新纳入的中型基金管理人，原则上不低于<b>30%</b>；支持中小基金管理人结合自身实际主动布局。此外鼓励基金管理人结合存量产品运作情况，先对持有人基础较好、投资者认同度较高的存量固定费率产品探索改造，稳妥变更为新模式浮费产品。<br>

          <b>产品进展：</b><b>2025年5月23日</b>，首批<b>26只</b>新模式浮动管理费基金集中获批；截至<b>2026年10月23日</b>，新模式浮动管理费基金数量已超过<b>120只</b>。<br>

          <b>费率机制：</b>费率锚定业绩基准和投资者每笔真实收益——持有期间产品实际业绩表现符合同期业绩比较基准的适用基准档费率，明显低于同期业绩比较基准的适用低档费率，显著超越同期业绩比较基准的适用升档费率；持有人持有超过<b>1年</b>享受更低的费率。<br>

          <b>对腾安启示：</b>浮动费率产品的管理费随业绩与持有期浮动，货架展示须把“基准档／低档／升档”三档费率与挂钩基准做成可比字段，并以持有期口径说明优惠条件，不得只展示单一费率数字；存量固定费率产品改造为浮动费率产品涉及合同变更，须前置提示持有人并区分改造前后的费率口径；产品数量增加后，筛选维度须从“是否为浮动费率”细化到挂钩基准、档位规则与持有期门槛。

        </div>

        <div class="card-footer">

          <a href="https://paper.cnstock.com/html/2026-10/26/content_2280950.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-26</span></a>

          <a href="https://fund.10jqka.com.cn/20261026/c681058972.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·上海证券报·10-26</span></a>

          <span class="impact-tag medium">影响：中</span>

        </div>

      </div>'''
i2 = s.find(anchor_s2)
s = s[:i2] + S2A + S2B + s[i2:]
print('OK S2 insert open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 12. S6 card ----------------
A6 = s.find('<!-- ============ Section 6')
S6S = s.find('<div class="card p3">', A6)
S6E = s.find('      </div>  </div>', S6S) + len('      </div>')
assert S6S > 0 and S6E > S6S
olds6 = s[S6S:S6E]
assert olds6.count('<div class="card p') == 1, 'S6 old cards=%d' % olds6.count('<div class="card p')

S6NEW = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股、港股、美股统一10-23收盘·沪指3690.48 +0.89%｜创业板指涨4.16%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-23</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-23收盘）</b><br>
              上证指数 <b>3690.48</b> <span style="color:#dc2626;">+0.89%</span>（+32.45点）<br>
              深证成指 <b>11673.83</b> <span style="color:#dc2626;">+2.79%</span>（+316.51点）<br>
              创业板指 <b>2684.10</b> <span style="color:#dc2626;">+4.16%</span>（+107.20点）<br>
              科创综指 <b>1606.48</b> <span style="color:#dc2626;">+3.68%</span>｜北证50 <b>984.90</b> <span style="color:#dc2626;">+1.88%</span><br>
              沪深两市成交 <b>约1.96万亿元</b><br>
              其中沪市约 <b>8986.67亿元</b> ＋ 深市约 <b>10575.91亿元</b>
            </div>
            <div>
              <b>港股（10-23收盘）与美股（美东10-23收盘）</b><br>
              恒生指数 <b>23093.37</b> <span style="color:#dc2626;">+0.69%</span>（+158.69点）<br>
              国企指数 <b>7756.25</b> <span style="color:#dc2626;">+0.87%</span>（+67.06点）<br>
              恒生科技 <b>3871.66</b> <span style="color:#dc2626;">+2.05%</span>（+77.73点）<br>
              道琼斯 <b>52215.16</b> <span style="color:#52c41a;">-1.23%</span>（-652.82点）<br>
              纳斯达克 <b>25955.34</b> <span style="color:#52c41a;">-0.21%</span>（-53.52点）<br>
              标普500 <b>7623.68</b> <span style="color:#52c41a;">-0.52%</span>（-39.75点）<br>
              港股主板成交 <b>2497.84亿港元</b><br>
              纽约12月交货原油 <b>103.27美元/桶</b> <span style="color:#dc2626;">+3.82%</span><br>
              伦敦12月交货布伦特 <b>116.72美元/桶</b> <span style="color:#dc2626;">+3.14%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>10月23日收盘</b>（10月23日为交易日且已收盘）；上证指数、深证成指、创业板指收盘点位与涨跌幅经行情数据终端与公开报道双源交叉印证；沪市约<b>8986.67亿元</b>、深市约<b>10575.91亿元</b>为沪深两市分市场成交额（中国经济网、新华财经口径），合计约1.96万亿元，本期仅并列列出、不与沪深北三市等其他口径混用；科创综指、北证50取新华财经10月23日收评口径。港股取<b>10月23日收盘</b>（新华社香港10月23日电，与行情数据终端互相印证）。美股取<b>美东10月23日收盘</b>（新华社纽约10月23日电，对应北京时间10月24日凌晨）。国际原油取<b>10月23日收盘</b>（新华财经：纽约商品交易所12月交货轻质原油期货价格、12月交货伦敦布伦特原油期货价格）。贵金属本期未取得可在同一源内交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-23）：</b>三大指数集体上涨、午后走出V形反转，创业板指涨4.16%领涨，沪指涨0.89%收复3690点。新华财经10月23日收评显示，早盘各股指普遍显著低开并进一步下探，午后宁德时代、长鑫科技快速拉升涨近8%，摩尔线程涨逾11%、沐曦股份涨逾13%、宇树科技20%涨停，板块标志性龙头大幅上涨显著提振市场人气；MLOps、科创成长层、科创板次新、电机、软件服务、减速器、人形机器人、机器视觉、多模态AI等多板块大幅上涨。行业方面电机、自动化设备、软件开发涨幅居前，银行、电力、元件跌幅居前。<br>
              <b>港股（10-23）：</b>新华社香港10月23日电，香港恒生指数涨158.69点、涨幅<b>0.69%</b>收报<b>23093.37</b>点，全日主板成交<b>2497.84亿港元</b>；国企指数涨67.06点、涨幅0.87%收<b>7756.25</b>点；恒生科技指数涨77.73点、涨幅2.05%收<b>3871.66</b>点。蓝筹股方面腾讯控股涨<b>0.94%</b>收报386港元、香港交易所涨0.98%收报370.8港元、中国移动跌0.32%收报77.1港元、汇丰控股跌1.04%收报142.5港元。<br>
              <b>美股（美东10-23）：</b>新华社纽约10月23日电，纽约股市三大股指23日下跌。道琼斯工业平均指数比前一交易日下跌652.82点、跌幅<b>1.23%</b>收于<b>52215.16</b>点；标准普尔500种股票指数下跌39.75点、跌幅<b>0.52%</b>收于<b>7623.68</b>点；纳斯达克综合指数下跌53.52点、跌幅<b>0.21%</b>收于<b>25955.34</b>点。板块方面，标普500指数十一大板块八跌三涨，必需消费品板块以<b>1.83%</b>跌幅领跌，能源板块和科技板块分别以<b>2.51%</b>和<b>0.35%</b>涨幅领涨。<br>
              <b>对腾安提示：</b>A股在10月22日大幅调整后于10月23日走出V形反转，创业板指单日涨逾4%，货架与持仓页须按各自市场分别刷新净值日期与估值口径，不得用单日反弹概括趋势；港股与美股当日走势分化，恒生科技涨2.05%而美股三大指数齐跌，跨境与QDII产品的净值波动提示与申赎确认时点须分别前置；国际油价连续上涨，涉及原油、商品类主题基金的估值提示须同步更新。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-23收盘，美股为美东2026-10-23收盘</span>
          <span class="source-tag">数据来源：中国经济网、新华财经（A股）；新华社（港股、美股）；新华财经（国际原油）</span>
        </div>
      </div>'''
s = s[:S6S] + S6NEW + s[S6E:]
print('OK S6 open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- 13. S7 timeline ----------------
A7 = s.find('<!-- ============ Section 7')
IT = s.find('<div class="timeline-item">', A7)
assert IT > 0
n_items = s.count('<div class="timeline-item">', A7)
assert n_items == 12, 'S7 items=%d' % n_items
LAST = s.rfind('<div class="timeline-item">')
LASTEND = s.find('      </div>\n\n    </div>', LAST) + len('      </div>')
assert LASTEND > LAST
assert s[IT:LASTEND].count('<div class="timeline-item">') == 12

items = [
    ('red', '2026-10-26', '权益基金成立门槛拟降至5000万'),
    ('blue', '2026-10-26', '部分权益基金逆势放开限购'),
    ('red', '2026-10-25', '主动ETF首日认购约150亿元'),
    ('blue', '2026-10-24', '工银瑞信1亿元自购主动ETF'),
    ('red', '2026-10-23', '首批18只主动ETF正式开售'),
    ('blue', '2026-10-23', '沪指涨0.89%收3690.48点'),
    ('blue', '2026-10-23', '创业板指涨4.16%领涨'),
    ('blue', '2026-10-22', '中基协修订八项基金估值指引'),
    ('blue', '2026-10-22', '沪指跌1.48%失守3700点'),
    ('blue', '2026-10-22', '布伦特原油涨4%收113美元'),
    ('blue', '2026-10-20', '央行拟设非银流动性支持工具'),
    ('red', '2026-10-16', '首批新能源金属50ETF获批'),
]
buf = []
for dot, d, t in items:
    assert len(t) <= 25, 'S7 title too long: %s' % t
    buf.append('      <div class="timeline-item">\n        <div class="timeline-dot %s"></div>\n        <div class="timeline-date">%s</div>\n        <div class="timeline-title">%s</div>\n      </div>' % (dot, d, t))
NEW7 = '\n'.join(buf)
s = s[:IT] + NEW7 + s[LASTEND:]
print('OK S7 open=%d close=%d' % (cnt_open(s), s.count('</div>')))

# ---------------- FINAL ASSERTS ----------------
fin_open = cnt_open(s)
fin_close = s.count('</div>')
print('FINAL open=%d close=%d (base %d/%d)' % (fin_open, fin_close, orig_open, orig_close))
assert fin_open == fin_close == orig_open, 'DIV IMBALANCE %d/%d base %d' % (fin_open, fin_close, orig_open)
assert s.count('</div>>') == 0
assert s.count('\ufffd') == 0, 'U+FFFD found'
assert 'Section 8' not in s
assert s.count('待办跟踪') == 0 and s.count('腾安行动清单') == 0

def bnd(n):
    a = s.find('<!-- ============ Section %d' % n)
    b = s.find('<!-- ============ Section %d' % (n + 1))
    if b < 0:
        b = len(s)
    return a, b

# S0 checks
a0, a1 = bnd(0)
seg0 = s[a0:a1]
assert seg0.count('<div class="card p') == 4, 'S0 cards=%d' % seg0.count('<div class="card p')
assert seg0.count('class="section-title"') == 1
m = re.search(r'<span class="section-title">([^<]*)</span>', seg0)
assert m.group(1) == '今日焦点', 'S0 title=%r' % m.group(1)
m = re.search(r'<span class="section-context">([^<]*)</span>', seg0)
assert m.group(1) == '10月26日 · 4条今日要闻', 'S0 context=%r' % m.group(1)
assert seg0.count('action-box') == 1, 'S0 action-box=%d' % seg0.count('action-box')
assert seg0.count('腾安行动建议') == 1
tags0 = re.findall(r'date-tag">(\d{2})-(\d{2})<', seg0)
assert tags0 == [('10','26'), ('10','25'), ('10','26'), ('10','26')], 'S0 tags=%s' % tags0
assert seg0.count('<a href=') == 8, 'S0 links=%d' % seg0.count('<a href=')
assert seg0.count('class="card-meta"') == 4

# S1
a1b, a2 = bnd(1)
seg1 = s[a1b:a2]
assert seg1.count('<div class="card p') == 6, 'S1 cards=%d' % seg1.count('<div class="card p')
assert seg1.count('<!-- S1 Card') == 6, 'S1 comments=%d' % seg1.count('<!-- S1 Card')
t1 = re.findall(r'date-tag">(\d{2})-(\d{2})<', seg1)
assert all(t >= ('10','12') for t in t1), 'S1 tags=%s' % t1

# S2
a2b, a3 = bnd(2)
seg2 = s[a2b:a3]
assert seg2.count('<div class="card p') == 3, 'S2 cards=%d' % seg2.count('<div class="card p')
assert seg2.count('<!-- S2 Card') == 3, 'S2 comments=%d' % seg2.count('<!-- S2 Card')
t2 = re.findall(r'date-tag">(\d{2})-(\d{2})<', seg2)
assert all(t >= ('10','12') for t in t2), 'S2 tags=%s' % t2

# S3/S4/S5 date window
for n in (3, 4, 5):
    x, y = bnd(n)
    segx = s[x:y]
    tt = re.findall(r'date-tag">(\d{2})-(\d{2})<', segx) + re.findall(r'<td>(\d{2})-(\d{2})</td>', segx)
    assert all(t >= ('10','12') for t in tt), 'S%d tags=%s' % (n, tt)

# S6
a6, a7x = bnd(6)
seg6 = s[a6:a7x]
assert seg6.count('<div class="card p') == 1
assert seg6.count('10-23') >= 3
assert '3658.03' not in seg6

# S7
a7b, a8 = bnd(7)
seg7 = s[a7b:a8]
its = re.findall(r'<div class="timeline-item">', seg7)
assert len(its) == 12, 'S7 items=%d' % len(its)
ds = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', seg7)
assert len(ds) == 12
assert ds == sorted(ds, reverse=True), 'S7 not desc: %s' % ds
assert all(d >= '2026-10-12' for d in ds), 'S7 out of window: %s' % ds
assert seg7.count('timeline-desc') == 0
for t in re.findall(r'<div class="timeline-title">([^<]*)</div>', seg7):
    assert len(t) <= 25, 'long title %s' % t

# fingerprint / desc
fp = re.search(r'content-fingerprint" content="([^"]*)"', s).group(1)
segs = fp.split('|')
assert len(segs) == 4, 'fp segs=%d' % len(segs)
titles0 = re.findall(r'<div class="card-title">([^<]*)</div>', seg0)
for sg in segs:
    assert any(sg[:4] in t for t in titles0), 'fp seg %s not in titles' % sg
desc = re.search(r'name="description" content="([^"]*)"', s).group(1)
dsegs = desc.split('|')
assert len(dsegs) == 5, 'desc segs=%d' % len(dsegs)
for sg in dsegs[:4]:
    assert any(sg[:4] in t for t in titles0), 'desc seg %s not in titles' % sg

# blacklist
BL = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com',
      'toutiao.com', 'so.html5.qq.com', '163.com/dy', 'cqcb.com', 'weibo.com',
      'k.sina.com.cn', 'dy.163.com', 'q.fund.sohu.com', 'topnews.cn',
      'futunn.com', 'jiantou8.com', 'cofool.com', 'yanglee.com']
for b in BL:
    assert b not in s, 'BLACKLIST HIT %s' % b

# stats bar
j = s.find('<div class="stats-bar">')
k2 = s.find('\n\n  </div>\n\n<div class="main">')
assert s[j:k2].count('stat-card') == 4

print('ALL ASSERTS PASSED')
io.open(P, 'w', encoding='utf-8').write(s)
print('WRITTEN size=%d' % len(s))
