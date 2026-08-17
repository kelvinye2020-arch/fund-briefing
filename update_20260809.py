# -*- coding: utf-8 -*-
"""基金行业资讯看板 每日更新 2026-08-09（周六·休市）
两阶段：Phase1 全部断言通过后才写文件。
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = open(P, encoding='utf-8').read()
ORIG_OPEN = s.count('<div')
ORIG_CLOSE = s.count('</div>')
print('BASE open=%d close=%d' % (ORIG_OPEN, ORIG_CLOSE))
assert ORIG_OPEN == ORIG_CLOSE, 'baseline already unbalanced'

steps = []          # (name, before_s) 用于逐步快照
REMOVED_CARDS = 0   # S1/S2 清理的过期卡数量（每张 6 个 div）
S7_DEL = 0
S7_ADD = 0

# ========== 1. marker + 数据区间 ==========
assert s.count('daily-update: 2026-08-08 -->') == 1
s = s.replace('daily-update: 2026-08-08 -->', 'daily-update: 2026-08-09 -->')

OLD_RANGE = '📅 数据区间：2026.07.25 — 2026.08.08（每日更新）'
NEW_RANGE = '📅 数据区间：2026.07.26 — 2026.08.09（每日更新）'
assert s.count(OLD_RANGE) == 1
s = s.replace(OLD_RANGE, NEW_RANGE)

# ========== 2. Stats Bar（周六休市：不以指数点位打头，改行业结构性数据） ==========
ST_A = '<!-- Stats Bar -->\n  <div class="stats-bar">\n'
ST_B = '</div>\n  </div>\n<div class="main">'
assert s.count(ST_A) == 1, 'stats A anchor'
assert s.count(ST_B) == 1, 'stats B anchor'
i = s.index(ST_A) + len(ST_A)
j = s.index(ST_B)

NEW_STATS = '''    <div class="stat-card">
      <div class="stat-number">125只</div>
      <div class="stat-label">LOF退市新规拟涉及产品数 · 08-07沪深交易所征求意见</div>
      <div class="stat-change neutral">● 场内规模合计约260亿元·其中小规模LOF约91只仅约3亿·意见反馈截至08-22</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">16家</div>
      <div class="stat-label">08-07上报创业板算力/金融科技ETF的公募</div>
      <div class="stat-change up">▲ 创业板行业主题指数产品化"从0到1"·算力10家+金融科技6家</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">2000亿+</div>
      <div class="stat-label">"创系列"指数跟踪产品合计规模 · 截至08-07</div>
      <div class="stat-change up">▲ 已覆盖宽基/行业主题/策略多类型·细分赛道ETF加速扩容</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">75只</div>
      <div class="stat-label">8月新发基金总数 · 创2026年内月度新低</div>
      <div class="stat-change down">▼ 仅48家公募参与·较6月182只近乎腰斩·ETF占比不足15%</div>
  '''
# ST_B 常量自带最后一张 stat-card 的闭合 → body 必须是 16 open / 15 close
_old_stats = s[i:j]
assert _old_stats.count('<div') == 16 and _old_stats.count('</div>') == 15, \
    'old stats body shape changed: %d/%d' % (_old_stats.count('<div'), _old_stats.count('</div>'))
assert NEW_STATS.count('<div') == 16 and NEW_STATS.count('</div>') == 15, \
    'new stats body must be 16/15, got %d/%d' % (NEW_STATS.count('<div'), NEW_STATS.count('</div>'))
s = s[:i] + NEW_STATS + s[j:]

# ========== 3. S0 section-context ==========
OLD_CTX = '<span class="section-context">8月8日 · 4条今日要闻</span>'
NEW_CTX = '<span class="section-context">8月9日 · 4条今日要闻</span>'
assert s.count(OLD_CTX) == 1, 'S0 context anchor'
s = s.replace(OLD_CTX, NEW_CTX)

# ========== 4. S0 整块替换（尾部闭合硬编码） ==========
S0_A = '<!-- S0 Card 1:'
S0_TAIL = '    </div>\n  </div>\n\n\n'
i0 = s.index(S0_A)
# S0 结束于 Section 1 注释之前
i1 = s.index('<!-- ============ Section 1')
assert s[i1 - len(S0_TAIL):i1] == S0_TAIL, 'S0 tail constant mismatch: %r' % s[i1-60:i1]

NEW_S0 = '''<!-- S0 Card 1: 沪深交易所LOF退市新规 (T-2 08-07发布/08-08新华社跟进 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🔴 LOF退市新规落地在即·商品期货/QDII LOF最晚2027年底终止上市·约125只产品受影响</div>
        </div>
        <div class="card-body">
          8月7日沪深交易所同步就<b>《完善上市开放式基金（LOF）相关安排》公开征求意见</b>，8月8日新华社、《中国证券报》集中跟进报道。新规分类明确三类LOF应当终止上市：<br>
          <b>① 商品期货LOF、QDII LOF</b>——受期货持仓开仓限制、QDII外汇额度不足制约，场内份额供给受限易生高溢价，设<b>一年以上过渡期，最晚2027年12月31日前终止上市</b>，管理人最晚2027年11月12日提交文件；<br>
          <b>② 小规模LOF</b>——连续<b>60个交易日场内资产净值均低于1000万元</b>即触发终止上市，不设过渡期，自规则施行日起算；<br>
          <b>③ 风险提示前置</b>——商品期货/QDII LOF自施行日起场内简称前冠"*"；小规模LOF连续40个交易日低于1000万元起须逐日披露风险提示。<br>
          <b>影响测算：</b>业内测算沪深两所预计涉及退市的LOF<b>约125只、场内规模合计约260亿元</b>，其中小规模LOF约91只、场内规模仅约3亿元，整体数量与规模均不大。<b>关键澄清：LOF终止上市≠基金清盘</b>，不影响基金正常投资运作与场外份额申赎，场内持有人可在过渡期转托管至场外、或通过场内赎回/卖出，退市不涉及基金净卖出标的资产。意见反馈截止<b>2026年8月22日</b>。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">影响：高</span>
          <a href="https://www.stcn.com/article/detail/4064643.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <a href="https://www.cnfin.com/gs-lb/detail/20260807/4452705_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经</span></a>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            <b>1）代销货架排查（本周内）：</b>立即比对腾安代销池中的商品期货LOF、QDII LOF及场内净值低于1000万元的小规模LOF，形成受影响产品清单，明确存量持仓客户数与规模。<br>
            <b>2）客户沟通口径统一：</b>核心话术须强调"终止上市≠清盘、不影响场外申赎"，避免客户误读为产品清盘而恐慌赎回；同步提示切勿参与"炒退""炒差"，高溢价买入后退市只能按净值赎回。<br>
            <b>3）风险提示流程改造：</b>新规要求券商将相关LOF纳入重点监控名单并多渠道提示，需评估腾安端内是否需增设溢价率提示位与退市倒计时标识。<br>
            <b>4）反馈窗口：</b>意见征求截至08-22，如涉及自营/代销实操难点可在窗口期内提交反馈。
          </div>
        </div>
      </div>

      <!-- S0 Card 2: 创业板算力/金融科技ETF 16家上报 (T-2 08-07 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-07</span>
          </div>
          <div class="card-title">🟡 首批16家公募上报创业板算力/金融科技ETF·"创系列"指数产品化从0到1破冰</div>
        </div>
        <div class="card-body">
          8月7日证监会官网显示，首批<b>16家基金管理人</b>集中上报<b>创业板算力基础设施指数ETF</b>与<b>创业板金融科技指数ETF</b>。上报算力基础设施ETF的<b>10家</b>：易方达、华夏、南方、广发、富国、国泰、嘉实、天弘、鹏华、大成；上报金融科技ETF的<b>6家</b>：景顺长城、华泰柏瑞、万家、东财、长城、建信。<br>
          <b>指数设计：</b>创业板算力基础设施指数从创业板精选50只算力相关标的，覆盖计算、网络、存储、运维等环节，含景嘉微、中际旭创、天孚通信等；创业板金融科技指数同样选取50只标的，涵盖分布式技术、支付结算、互联网金融、金融安全及金融数字化服务全产业链，含东方财富、同花顺、润和软件等。<br>
          <b>行业意义：</b>这是创业板行业主题指数产品化"<b>从0到1</b>"的突破。深证信息此前已发布创业板算力、金融科技、电池、医疗、传媒、专精特新、通信、智能驾驶、机器人等多条行业主题指数，"创系列"指数跟踪产品规模已<b>合计超2000亿元</b>，后续或有更多主题ETF上报。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">影响：高</span>
          <a href="https://www.chnfund.com/article/ARc39e9199-0471-900e-1f8d-3a22ee147979" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <a href="https://qzswap.stcn.com/wap_newsDetail.html?id=622538&type=fast_info" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
        </div>
      </div>

      <!-- S0 Card 3: 8月8日多家公募基金经理密集变更 (T-1 08-08 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🟡 8月8日公募基金经理密集变更·华安/南方/汇添富/东海多只ETF与QDII换帅</div>
        </div>
        <div class="card-body">
          8月8日多家公募集中发布基金经理变更公告，指数与跨境产品为调整重灾区：<br>
          <b>华安基金：</b>刘璇子离任华安中证申万食品饮料ETF、信创产业指数发起式、CES半导体芯片指数发起式，顾昕离任上证科创板50ETF及其联接，均由<b>周泓灏</b>自8月10日接任；刘璇子未转任公司其他岗位，目前在管12只、规模超100亿。另许之彦因内部调整离任<b>华安中证全指自由现金流ETF</b>（8月10日生效），由王超单独管理。<br>
          <b>南方基金：</b>王鑫离任南方标普500ETF(QDII)、中证香港科技ETF(QDII)，由张其思单独管理；张其思同时离任南方东英富时亚太精选ETF(QDII)等三只，转由王鑫接手，并增聘为南方全球精选配置(QDII-FOF)基金经理。张其思在管15只、规模超350亿。<br>
          <b>汇添富：</b>马磊因内部调整离任北交所创新精选两年定开，助理<b>林炜转正</b>接任。<b>东海基金：</b>张立新离任东海社会安全指数基金，由汤伟杰单独管理。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://new.qq.com/rain/a/20260808A08YHZ00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">基金公告</span></a>
          <a href="https://finance.sina.cn/2026-08-09/detail-inimrzvc6029533.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪基金</span></a>
        </div>
      </div>

      <!-- S0 Card 4: 公募负责任AI治理 (T-1 08-08 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🔵 公募AI治理走向纵深·华夏等将"负责任AI"纳入新议题·永赢银华输出安全运营案例</div>
        </div>
        <div class="card-body">
          证券时报8月8日报道，AI技术在基金业的运用边界在7月扩大到<b>治理领域</b>，行业在"AI内部安全治理"层面已取得基本共识。<br>
          <b>外部治理：</b>截至8月3日，已有<b>华夏基金</b>等公募将"<b>负责任AI</b>"作为新议题，纳入对涉及模型研发和商业化的科技公司的治理考察中。该做法在海外成熟市场同样刚起步，但AI相关股东提案支持率显著高于一般提案。<br>
          <b>内部实践：</b>永赢基金通过安全GPT钓鱼检测大模型提升邮件安全能力，高对抗钓鱼邮件<b>检出率超93%</b>、误报率降至0.28%以下、人工复核工作量减少80%以上；银华基金以AI原生智能体(Agent)为核心构建告警自动处置体系，日均原始告警从数千条压缩至数十条高价值告警，<b>告警噪声压缩率超92%</b>。<br>
          中基协7月下旬联合上交所、上海市基金同业公会举办基金行业数据要素培训班，260余人参加。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L3Q1NLFF053469RG.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
        </div>
      </div>
'''
s = s[:i0] + NEW_S0 + S0_TAIL + s[i1:]

# ========== 5. S1 清理过期卡（07-25 < CUTOFF 07-26） ==========
i_s1 = s.index('<!-- ============ Section 1')
i_s2 = s.index('<!-- ============ Section 2')
seg1 = s[i_s1:i_s2]
assert seg1.count('<span class="date-tag">07-25</span>') == 1, 'S1 07-25 card locate'
# 定位该卡整块：从其 <div class="card 起，到随后独立行闭合
k = seg1.index('<span class="date-tag">07-25</span>')
cs = seg1.rindex('<div class="card ', 0, k)
# 卡片注释头（若有）一并删除
cmt = seg1.rfind('<!--', 0, cs)
if cmt != -1 and seg1.rfind('-->', 0, cs) > cmt:
    cs = cmt
# 卡片结尾用「footer闭合 + card闭合」双层序列锚定，避免 6空格 </div> 子串命中 footer 内部
CARD_CLOSE = '        </div>\n      </div>\n'
ce = seg1.index(CARD_CLOSE, k) + len(CARD_CLOSE)
removed = seg1[cs:ce]
assert removed.count('<div') == removed.count('</div>') == 6, \
    'S1 removed block must be 6/6 divs, got %d/%d' % (removed.count('<div'), removed.count('</div>'))
seg1 = seg1[:cs] + seg1[ce:]
REMOVED_CARDS += 1
s = s[:i_s1] + seg1 + s[i_s2:]
print('S1 removed expired 07-25 card (6 divs)')

# ========== 6. S6 卡片元信息（周末休市：沿用08-07收盘，标题同步注明） ==========
OLD6T = '2026年8月7日（周五·收盘）·A股四大指数齐涨超1%·沪指3940.04收复年内高地·科创综指涨3.35%·CRO掀涨停潮'
NEW6T = '2026年8月7日（周五·收盘）·周末休市·A股四大指数齐涨超1%·沪指3940.04·全周涨2.81%·科创综指周涨10.96%'
assert s.count(OLD6T) == 1, 'S6 title anchor'
s = s.replace(OLD6T, NEW6T)

# ========== 7. S7 时间线：删最旧(07-28) 再增 08-09 ==========
i_s7 = s.index('<!-- ============ Section 7')
seg7 = s[i_s7:]
OLD_ITEM_KEY = 'timeline-date">2026-07-28<'
assert seg7.count(OLD_ITEM_KEY) == 1, 'S7 oldest item anchor'
kk = seg7.index(OLD_ITEM_KEY)
istart = seg7.rindex('<div class="timeline-item">', 0, kk)
ITEM_CLOSE = '</div>\n      </div>\n'
iend = seg7.index(ITEM_CLOSE, kk) + len(ITEM_CLOSE)
del_block = seg7[istart:iend]
assert del_block.count('<div') == 4, 'timeline-item must be 4 divs, got %d' % del_block.count('<div')
assert del_block.count('</div>') == 4, 'timeline-item must close 4 divs, got %d' % del_block.count('</div>')
seg7 = seg7[:istart] + seg7[iend:]
S7_DEL += 1

# 清理历史遗留的空注释占位（不含 div，安全）
STALE = '\n      <!-- 07-25 时间线条目 (NEW) -->\n      \n'
if STALE in seg7:
    assert STALE.count('<div') == 0
    seg7 = seg7.replace(STALE, '\n')
    print('cleaned stale S7 comment placeholder')

# 插入 08-09 到最前（在 2026-08-08 条目之前）
NEW_ITEM = '''<div class="timeline-item">
          <div class="timeline-dot red"></div>
          <div class="timeline-date">2026-08-09</div>
          <div class="timeline-title">LOF退市新规征求意见·涉125只产品</div>
        </div>
        '''
assert NEW_ITEM.count('<div') == 4 and NEW_ITEM.count('</div>') == 4
key0808 = 'timeline-date">2026-08-08<'
assert seg7.count(key0808) == 1, 'S7 08-08 anchor'
k8 = seg7.index(key0808)
ins = seg7.rindex('<div class="timeline-item">', 0, k8)
seg7 = seg7[:ins] + NEW_ITEM + seg7[ins:]
S7_ADD += 1
s = s[:i_s7] + seg7

# ========== Phase 1 断言 ==========
o, c = s.count('<div'), s.count('</div>')
drift = o - ORIG_OPEN
expected_drift = -6 * REMOVED_CARDS + 4 * (S7_ADD - S7_DEL)
print('AFTER open=%d close=%d drift=%d expected=%d' % (o, c, drift, expected_drift))
assert o == c, 'DIV IMBALANCE open=%d close=%d' % (o, c)
assert drift == expected_drift, 'unexpected drift %d != %d' % (drift, expected_drift)

# S8 必须不存在
for bad in ['Section 8', '待办跟踪', '腾安行动清单']:
    assert bad not in s, 'S8 residue found: %s' % bad

# S0 段校验
a = s.index('<!-- S0 Card 1:')
b = s.index('<!-- ============ Section 1')
s0 = s[a:b]
assert s0.count('<div class="action-box">') == 1, 'S0 action-box must be 1, got %d' % s0.count('<div class="action-box">')
assert s0.count('<div class="card p0">') == 1, 'S0 p0 card must be 1'
assert s0.count('<div class="card-meta">') == 4, 'S0 card-meta must be 4'
d0 = re.findall(r'date-tag">([0-9-]+)<', s0)
assert len(d0) == 4, 'S0 must have 4 date-tags, got %d' % len(d0)
assert all(x in ('08-07', '08-08', '08-09') for x in d0), 'S0 date out of window: %s' % d0
assert s.count('<span class="section-title">今日焦点</span>') == 1
assert '今日焦点（' not in s
assert s.count('<span class="section-context">8月9日 · 4条今日要闻</span>') == 1
# 每张 S0 卡都要有出处链接
assert s0.count('target="_blank"') >= 4, 'S0 source links insufficient'

# S7 校验
i7 = s.index('<!-- ============ Section 7')
d7 = re.findall(r'timeline-date">([0-9-]+)<', s[i7:])
t7 = re.findall(r'timeline-title">(.*?)<', s[i7:])
assert len(d7) == len(t7), 'S7 date/title count mismatch'
assert 10 <= len(d7) <= 12, 'S7 count out of range: %d' % len(d7)
assert len(d7) == len(set(d7)), 'S7 duplicate dates: %s' % [x for x in d7 if d7.count(x) > 1]
assert d7 == sorted(d7, reverse=True), 'S7 not sorted desc'
assert all(x >= '2026-07-26' for x in d7), 'S7 expired entry: %s' % [x for x in d7 if x < '2026-07-26']
for t in t7:
    assert len(t) <= 25, 'S7 title too long (%d): %s' % (len(t), t)
    assert '/' not in t, 'S7 title stacking: %s' % t

# S1/S2 过期校验
CUT = '07-26'
for name, ia, ib in [('S1', s.index('<!-- ============ Section 1'), s.index('<!-- ============ Section 2')),
                     ('S2', s.index('<!-- ============ Section 2'), s.index('<!-- ============ Section 3'))]:
    ds = re.findall(r'date-tag">([0-9-]+)<', s[ia:ib])
    bad = [x for x in ds if x < CUT]
    assert not bad, '%s expired: %s' % (name, bad)
    print('%s dates ok: %s' % (name, ds))

# 乱码检查
assert '\ufffd' not in s, 'U+FFFD found'

print('PHASE1 ALL ASSERTIONS PASSED — writing file')
open(P, 'w', encoding='utf-8').write(s)
print('WRITTEN OK  S7 count=%d' % len(d7))
