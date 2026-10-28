# -*- coding: utf-8 -*-
"""基金看板 2026-10-28 每日更新（主任务）"""
import re, os, sys
from datetime import date, timedelta

CWD = r"c:\Users\kelvinyye\WorkBuddy\20260314103829"
sys.stdout = open(os.path.join(CWD, "_run_1028.txt"), "w", encoding="utf-8")
sys.stderr = sys.stdout
P = os.path.join(CWD, "index.html")
BAK = os.path.join(CWD, "_bak_1028.html")
TODAY = date(2026, 10, 28)
T14 = TODAY - timedelta(days=14)          # 2026-10-14

s = open(P, encoding="utf-8").read()
orig = s
open(BAK, "w", encoding="utf-8").write(s)

O0 = len(re.findall(r'<div\b', s)); C0 = len(re.findall(r'</div>', s))
print("BASE open=%d close=%d" % (O0, C0))

def oc(tag):
    o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
    print("  [%s] open=%d close=%d  drift_o=%+d drift_c=%+d" % (tag, o, c, o - O0, c - C0))

def sub1(old, new, tag, cnt=1):
    """单处替换，cnt 为期望出现次数"""
    global s
    n = s.count(old)
    assert n == cnt, "%s: anchor count=%d expect=%d :: %r" % (tag, n, cnt, old[:80])
    s = s.replace(old, new, 1)
    oc(tag)

# ============================================================
# 1) marker / fingerprint / description（第一步，闸0/闸6/闸8）
# ============================================================
sub1('<!-- daily-update: 2026-10-27 -->', '<!-- daily-update: 2026-10-28 -->', 'marker')

sub1('content="央行设立|运作办法|首批主动|债券型ET"',
     'content="公募三季|首批主动|私募自购|月内32只"', 'fingerprint')

sub1('content="央行设立债市非银大额赎回互换便利|运作办法修订打开公募资产配置新空间|'
     '首批主动ETF两日累计募集超250亿元|债券型ETF年内净流入2414亿元规模破万亿|'
     '沪指10月26日收3697.52点涨0.19%·港股恒指涨0.51%·美股三大指数齐涨"',
     'content="公募三季报收官债券基金规模超12.6万亿元创历史新高|'
     '首批主动ETF开售三天11只募满沪市7只合计163.3亿元|'
     '私募自购潮再起诚奇基金1亿元年内34家合计17.54亿元|'
     '月内32只FOF启动募集创历史单月新高年内已达194只|'
     '沪指10月27日收3648.30点跌1.33%·港股恒指跌0.73%·美股三大指数齐涨"', 'description')

# ============================================================
# 2) header 数据区间（动态计算）
# ============================================================
badge_new = "📅 数据区间：%s — %s（每日更新）" % (
    T14.strftime("%Y.%m.%d"), TODAY.strftime("%Y.%m.%d"))
s, n = re.subn(r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）",
               badge_new, s)
assert n == 1, "header badge subn=%d" % n
assert badge_new == "📅 数据区间：2026.10.14 — 2026.10.28（每日更新）", badge_new
oc('header-badge')

# ============================================================
# 3) Stats Bar（4 卡全换；替换块不含容器闭合）
# ============================================================
STATS_START = '    <div class="stat-card">'
STATS_END = '\n\n  </div>\n\n<div class="main">'
assert s.count(STATS_END) == 1, "STATS_END count=%d" % s.count(STATS_END)
c0 = s.find(STATS_START)
e0 = s.find(STATS_END)
assert 0 < c0 < e0, "stats range %d %d" % (c0, e0)
old_stats = s[c0:e0]
assert old_stats.count('<div class="stat-card">') == 4, "stat-card=%d" % old_stats.count('<div class="stat-card">')
assert old_stats.count('<div') == old_stats.count('</div>'), "stats unbalanced"

NEW_STATS = (
'    <div class="stat-card">\n'
'      <div class="stat-number">12.6万亿</div>\n'
'      <div class="stat-label">债券型基金总规模创历史新高·三季度增加超5000亿元</div>\n'
'      <div class="stat-change up">▲ 获净申购超2800亿份·七大类产品中净申购最多</div>\n'
'    </div>\n'
'    <div class="stat-card">\n'
'      <div class="stat-number">3648.30</div>\n'
'      <div class="stat-label">沪指10-27收盘·跌1.33%·沪深两市成交约1.46万亿元</div>\n'
'      <div class="stat-change down">▼ 深证成指跌2.50%·创业板指跌3.41%</div>\n'
'    </div>\n'
'    <div class="stat-card">\n'
'      <div class="stat-number">78.32%</div>\n'
'      <div class="stat-label">三季度末全部可比基金平均仓位·较二季度末降3.29个百分点</div>\n'
'      <div class="stat-change down">▼ 股票型88.04%·混合型76.78%</div>\n'
'    </div>\n'
'    <div class="stat-card">\n'
'      <div class="stat-number">21亿元</div>\n'
'      <div class="stat-label">首批主动ETF基金公司自购合计·沪市7只募满163.3亿元</div>\n'
'      <div class="stat-change up">▲ 三天11只募满·预计10月29日首批建仓</div>\n'
'    </div>\n'
)
assert NEW_STATS.count('<div') == NEW_STATS.count('</div>')
s = s[:c0] + NEW_STATS + s[e0:]
oc('stats-bar')

# ============================================================
# 4) S0 今日焦点：整块换卡（4 张，无 P0 → 无 action-box）
# ============================================================
S0_END = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 1'
assert s.count(S0_END) == 1, "S0_END count=%d" % s.count(S0_END)
s0s = s.find('Section 0')
c1 = s.find('<!-- S0 Card 1', s0s)
e1 = s.find(S0_END)
assert 0 < c1 < e1, "S0 range %d %d" % (c1, e1)
old_s0 = s[c1:e1]
assert old_s0.count('<div class="card p') == 4, "S0 old cards=%d" % old_s0.count('<div class="card p')
assert old_s0.count('action-box') == 1, "S0 old action-box=%d" % old_s0.count('action-box')

def card(pri_cls, pri_tag, emoji, title, dtag, body, links, impact, impact_cls='medium'):
    a = ''
    for u, t in links:
        a += ('\n          <a href="%s" target="_blank" '
              'style="color:#1890ff;text-decoration:none;">'
              '<span class="source-tag">%s</span></a>\n' % (u, t))
    return (
'      <div class="card %s">\n'
'        <div class="card-top">\n'
'          <div class="card-title">%s %s</div>\n'
'          <div class="card-meta">\n'
'            <span class="priority-tag %s">%s</span>\n'
'            <span class="date-tag">%s</span>\n'
'          </div>\n'
'        </div>\n'
'        <div class="card-body">\n'
'          %s\n'
'        </div>\n'
'        <div class="card-footer">%s\n'
'          <span class="impact-tag %s">%s</span>\n'
'        </div>\n'
'      </div>' % (pri_cls, emoji, title, pri_cls, pri_tag, dtag, body, a, impact_cls, impact))

B1 = ('中国证券报电子版10月28日报道（记者张凌之）：10月27日，公募基金2026年三季报披露完毕。'
 '从基金规模看，截至三季度末，债券型基金总规模超过<b>12.6万亿元</b>，创历史新高；'
 '相较于二季度末，债基规模增加超<b>5000亿元</b>，获净申购超过<b>2800亿份</b>，'
 '成为股票型基金、混合型基金、债券型基金、货币型基金、商品型基金、QDII、FOF等七大类基金中获净申购最多的一类。<br>\n'
 '          <b>权益端收缩：</b>三季度主动权益基金（包括普通股票型、偏股混合型、平衡混合型、灵活配置型基金）'
 '规模合计减少超<b>9000亿元</b>，规模超200亿元的主动权益产品数量减少至<b>5只</b>；'
 '不过三季度仍有东方人工智能主题、银华集成电路、财通成长优选、信澳业绩驱动、富国新兴产业等一批科技风格基金获资金增持。<br>\n'
 '          <b>重仓股名单：</b>最新前十大重仓股依次为中际旭创、新易盛、药明康德、长鑫科技、源杰科技、东山精密、'
 '宁德时代、寒武纪、北方华创、沪电股份；与2026年二季度末相比，药明康德、长鑫科技、沪电股份三只个股新进，'
 '其中<b>药明康德</b>成为公募基金增持市值最多的个股。<br>\n'
 '          <b>对腾安启示：</b>债基承接、权益收缩的结构性变化须在货架分层上如实体现——固收与“固收+”'
 '不得以“权益赚钱效应”话术引流；主动权益产品页须同时展示规模变动与持有期收益，'
 '不得用短期赛道排名掩盖规模缩水与集中度上升。')

B2 = ('中国基金报10月28日报道（记者闫军）：18只首批主动ETF自10月23日集中开售以来，已有<b>11只</b>产品完成20亿元发行目标；'
 '10月27日，汇添富基金、大成基金、招商基金、天弘基金旗下主动ETF募集规模先后达到20亿元上限并提前结束募集，'
 '其中大成红利智选主动ETF仅用3个交易日募满——上海证券报电子版10月28日刊登的大成基金公告显示，'
 '该基金原定募集截止日11月5日提前至10月27日，自10月28日起不再接受认购申请。<br>\n'
 '          <b>认购结构：</b>沪市9只产品中已募满7只，合计募集资金达<b>163.3亿元</b>，近<b>10万户</b>参与沪市主动ETF认购，'
 '其中机构投资者认购占比超<b>20%</b>。<br>\n'
 '          <b>自购与建仓：</b>摩根、易方达、富国、华夏、汇添富、华安、工银瑞信、平安等多家基金公司'
 '通过自有资金或股东相关方资金自购旗下主动ETF产品，自购金额合计<b>21亿元</b>；'
 '首日结募的两家基金管理人将于<b>10月29日</b>开始建仓，据估算首批主动ETF预计为市场带来增量资金逾<b>350亿元</b>。<br>\n'
 '          <b>对腾安启示：</b>主动ETF是场内主动权益新品类，货架须将其与被动ETF明确区分——'
 '不跟踪特定指数、由基金经理自主选股与择时，须在页面显著位置披露投资策略、持仓集中度'
 '与每日披露申购赎回清单（PCF）带来的持仓透明度差异，不得与宽基ETF混排比较。')

B3 = ('中国基金报10月28日报道：10月27日，百亿量化私募上海诚奇私募基金管理有限公司发布公告称，'
 '基于对我国资本市场长期健康发展的坚定信念，将于近期使用自有资金人民币<b>1亿元</b>跟投公司旗下各类私募证券基金产品。'
 '公开资料显示，诚奇基金成立于2013年9月，2020年规模突破100亿元、2021年突破400亿元。<br>\n'
 '          <b>年内全景：</b>10月以来上海衍合私募、海南无量资本、凯丰投资、汉和资本等私募机构密集宣布自购；'
 '据记者不完全统计，今年以来市场上已有<b>34家</b>私募宣布自购，自购金额合计达<b>17.54亿元</b>。'
 '其中11家百亿私募合计自购超10亿元、占比六成以上；上海希瓦、止于至善投资、汉和资本年内自购均不少于2次；'
 '龙旗科技、睿郡资产、灵均投资、平方和投资、因诺资产自购均超1亿元。<br>\n'
 '          <b>机构观点：</b>高毅资产表示，今年以来万得全A指数下跌10%，而半年报盈利增速为16%，'
 '若全年可保持这一利润增速，简单测算目前估值贡献度已接近<b>-26%</b>；考虑到中国长端债券收益率持续下行，'
 '沪深300指数的股息率已显著高于十年期国债利率。中欧瑞博认为，中国经济中长期竞争力坚实，'
 '人工智能与绿色能源双领先构筑技术与能源安全优势。<br>\n'
 '          <b>对腾安启示：</b>私募管理人自购是对市场中长期配置价值的表态，不等于短期净值托底；'
 '涉及私募相关内容的展示须明确合格投资者门槛与不保本保收益属性，'
 '严禁把管理人自购金额解读为收益承诺或隐性担保。')

B4 = ('证券日报10月28日报道（记者彭衍菘，中国网财经转载）：10月以来FOF（基金中基金）发行持续活跃，'
 '多资产配置成为公募机构产品布局的重要方向。万得数据显示，按认购起始日统计，截至10月27日，'
 '月内已有<b>32只</b>FOF启动募集，创历史单月新高，另有1只产品计划于10月28日开启发行；'
 '今年以来FOF已启动募集<b>194只</b>（未计入10月28日及之后发行的产品数量）。<br>\n'
 '          <b>多资产成主流：</b>本月已启动募集的32只FOF中，名称包含“多资产”或“多元”的产品有<b>13只</b>，'
 '华安盈盛多资产6个月持有混合（FOF）、苏新知行致远多资产6个月持有混合（FOF）、'
 '兴全盈远多元配置三个月持有混合（FOF）等相继启动募集。<br>\n'
 '          <b>制度配套：</b>证监会近期就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，'
 '拟将FOF成立门槛从规模2亿元降至<b>5000万元</b>、份额从2亿份降至<b>5000万份</b>，并允许FOF投资ETF联接基金。<br>\n'
 '          <b>对腾安启示：</b>FOF正从“小众补充”转为多资产配置主货架，须把底层资产类别、穿透后权益仓位'
 '与波动区间做成可比字段，并在产品页提示双重收费与最短持有期安排，'
 '避免投资者把FOF简单理解为“低波动固收替代”。')

C1 = card('p1', 'P1 重要关注', '🟡',
          '公募三季报收官·债券基金规模超12.6万亿元创历史新高·净申购超2800亿份', '10-28', B1,
          [('https://epaper.cs.com.cn/zgzqb/html/2026-10/28/nw.D110000zgzqb_20261028_3-A01.htm', '中国证券报电子版·10-28'),
           ('https://news.qq.com/rain/a/20261028A02HBU00', '腾讯新闻·10-28')],
          '影响：中')

C2 = card('p1', 'P1 重要关注', '🟡',
          '首批主动ETF开售三天11只募满·沪市9只中7只合计募资163.3亿元', '10-28', B2,
          [('https://www.chnfund.com/article/AR70d2a19d-b2bc-0b8b-8c0a-3a24917ddbcf', '中国基金报·10-28'),
           ('https://paper.cnstock.com/html/2026-10/28/content_2282076.htm', '上海证券报电子版·10-28')],
          '影响：中')

C3 = card('p1', 'P1 重要关注', '🟡',
          '私募自购潮再起·诚奇基金1亿元跟投·年内34家私募自购合计17.54亿元', '10-28', B3,
          [('https://www.chnfund.com/article/ARd1e2b52a-c992-b455-0dd9-3a248fa1c839', '中国基金报·10-28')],
          '影响：中')

C4 = card('p2', 'P2 建议了解', '🔵',
          '月内32只FOF启动募集创历史单月新高·年内已达194只', '10-28', B4,
          [('https://finance.china.com.cn/money/fund/20261028/6326915.shtml', '中国网财经·证券日报·10-28')],
          '影响：中')

NEW_S0 = ('      <!-- S0 Card 1 (10-28 P1) -->\n' + C1 +
          '\n\n      <!-- S0 Card 2 (10-28 P1) -->\n' + C2 +
          '\n\n      <!-- S0 Card 3 (10-28 P1) -->\n' + C3 +
          '\n\n      <!-- S0 Card 4 (10-28 P2) -->\n' + C4)
assert NEW_S0.count('<div class="card p') == 4
assert NEW_S0.count('<div') == NEW_S0.count('</div>')
s = s[:c1] + NEW_S0 + s[e1:]
oc('S0-cards')
# 旧块有 1 个 P0 action-box（+3/+3），新块无 → 预期 open/close 各 -3

# ---- 另一步：改 section-context ----
sub1('<span class="section-context">10月27日 · 4条今日要闻</span>',
     '<span class="section-context">10月28日 · 4条今日要闻</span>', 'S0-context')

# ============================================================
# 5) S1：删 10-13 越界卡 + 新增 10-27 卡
# ============================================================
s1s = s.find('Section 1')
k1 = s.find('<!-- S1 Card:', s1s)
k2 = s.find('<!-- S1 Card:', k1 + 12)
blk = s[k1:k2]
assert blk.count('<div class="card p') == 1, "S1 del block cards=%d" % blk.count('<div class="card p')
assert '10-13' in blk, "S1 del block has no 10-13"
s = s[:k1] + s[k2:]
oc('S1-del')

# 追加新卡到 S1 末张卡之后（挂在 card-grid 内部，不能插到 section 闭合之后）
def append_after_last_card(sec_start, next_marker, new_block):
    global s
    b = s.find(next_marker)
    assert 0 < sec_start < b, "range %d %d" % (sec_start, b)
    lc = s.rfind('<div class="card p', sec_start, b)
    assert lc > 0, "last card not found"
    cp = s.find('\n      </div>', lc)
    assert cp > 0 and cp < b, "card close not found"
    cp = cp + 1 + len('      </div>')
    s = s[:cp] + new_block + s[cp:]

s1s = s.find('Section 1')
B_S1 = ('证券日报/中国证券报10月27日报道（Wind数据）：截至10月23日，10月以来股票型ETF资金累计净流入超<b>2800亿元</b>，'
 '上市公司累计回购超<b>170亿元</b>。随着市场连续震荡，A股估值已到相对低位，'
 '分析人士认为A股市场整体估值已回落至历史均值以下，横向与纵向比较均已具备较好投资吸引力，'
 '当前A股不宜过度悲观，短期或以震荡筑底和结构性机会为主。<br>\n'
 '          <b>资金结构：</b>增量资金的主体是宽基ETF——宽基指数产品是机构实施大类底仓配置的标准化工具，'
 '在市场调整阶段出现持续、逆势大额净流入，表明有一部分机构资金基于当前估值与股权风险溢价等指标，'
 '认可A股在当前点位具备配置价值。<br>\n'
 '          <b>对腾安启示：</b>“越跌越买”的ETF净流入是机构底仓行为，不等于散户申购信号；'
 '货架与内容侧须把“ETF资金流向”与“主动权益申赎”分开呈现，'
 '并在指数产品页标注估值分位与股权风险溢价口径，不得把资金净流入直接演绎为上涨预期。')
C_S1 = ('\n\n\n\n<!-- S1 Card: 增量资金入市力度加大 股票型ETF月内净流入超2800亿 (10-27 P2) -->\n\n'
        + card('p2', 'P2 建议了解', '🔵',
               '增量资金入市力度加大·10月以来股票型ETF净流入超2800亿元·回购超170亿元', '10-27', B_S1,
               [('https://news.qq.com/rain/a/20261027A02VYS00', '腾讯新闻·10-27')],
               '影响：中'))
assert C_S1.count('<div') == C_S1.count('</div>')
append_after_last_card(s1s, '<!-- ============ Section 2', C_S1)
oc('S1-add')

# ============================================================
# 6) S2：新增证监会私募母基金新规（10-23）
# ============================================================
s2s = s.find('Section 2')
B_S2 = ('证监会10月23日消息，根据《中华人民共和国证券投资基金法》《私募投资基金监督管理条例》等法律法规，'
 '起草了《私募投资母基金管理规定（征求意见稿）》并向社会公开征求意见。'
 '据央视网财经10月27日梳理，《母基金规定》全文二十三条，从概念认定、分散投资比例、投资层级豁免'
 '到管理人资质、运作管理和投资负面清单给出一套可量化规则。<br>\n'
 '          <b>身份门槛：</b>母基金投资于其他私募基金份额的金额不得低于其资产净值的<b>80%</b>；'
 '名称须含“母基金”字样，以公司、合伙企业形式设立的经营范围须包含“从事母基金投资活动”字样。'
 '按投向分为私募证券投资母基金、私募股权投资母基金、创业投资母基金与复合型母基金四类，穿透后投资范围须与类型匹配。<br>\n'
 '          <b>四条比例红线：</b>投资单只基金不超过资产净值的<b>25%</b>；穿透后单一底层项目不超过<b>20%</b>'
 '（100亿元以上收紧至10%）；同一实际控制人旗下不超过<b>30%</b>；符合条件的母基金可豁免计入一层投资层级，'
 '但母基金之间嵌套的，投资层级只能豁免一次。<br>\n'
 '          <b>管理人要求：</b>须配备达标专职投资人员、不得让渡投资决策权，基金财产须强制托管并穿透披露；'
 '本规定所称私募基金、母基金不包含证券期货经营机构等设立的私募资产管理计划。'
 '对存量私募基金中符合母基金条件的，证监会将指导中国证券投资基金业协会明确类型变更的统一标准和程序。<br>\n'
 '          <b>对腾安启示：</b>母基金首次获得统一监管口径，“80%＋25%”的双重比例把“基金中的基金”'
 '从营销概念变成可核验标准；凡涉及FOF、多资产组合与私募相关内容的展示，'
 '须按穿透后底层资产类别与集中度披露，不得用“分散投资”笼统概括，也不得把豁免投资层级演绎为监管放松。')
C_S2 = ('\n\n\n\n<!-- S2 Card: 证监会就私募投资母基金管理规定公开征求意见 (10-23 P1) -->\n\n'
        + card('p1', 'P1 重要关注', '🟡',
               '证监会就私募投资母基金管理规定公开征求意见·23条划定80%身份门槛与四条比例红线', '10-23', B_S2,
               [('https://finance.cctv.cn/2026/10/27/ARTI9p2EsNDpjy511jOXAZt2261027.shtml', '央视网财经·10-27'),
                ('https://www.ce.cn/xwzx/gnsz/gdxw/202610/t20261028_3274110.shtml', '中国经济网·10-28')],
               '影响：高', 'high'))
assert C_S2.count('<div') == C_S2.count('</div>')
append_after_last_card(s2s, '<!-- ============ Section 3', C_S2)
oc('S2-add')

# ============================================================
# 7) S4：替换 10-13 越界卡 → 10-28 公募仓位卡
# ============================================================
s4s = s.find('Section 4')
k1 = s.find('<!-- S4 Card:', s4s)
k2 = s.find('<!-- S4 Card:', k1 + 12)
blk = s[k1:k2]
assert blk.count('<div class="card p') == 1, "S4 block cards=%d" % blk.count('<div class="card p')
assert '10-13' in blk, "S4 block has no 10-13"
B_S4 = ('上海证券报10月28日报道（记者赵明超、王彭）：根据最新披露的公募基金三季报，'
 '光模块龙头中际旭创再度蝉联公募头号重仓股，新易盛和药明康德分列第二、第三重仓股；'
 '今年7月底上市的长鑫科技成为公募第四大重仓股。<br>\n'
 '          <b>持仓明细（天相投顾，截至2026年9月30日）：</b>共有<b>1557只</b>基金持有中际旭创，合计持仓市值<b>959.38亿元</b>；'
 '<b>1189只</b>基金重仓持有新易盛，合计<b>870.78亿元</b>；<b>1083只</b>基金重仓持有药明康德，合计<b>446.81亿元</b>；'
 '<b>959只</b>基金重仓持有长鑫科技，合计<b>428.52亿元</b>。前五十大重仓股主要分布在AI相关行业与医药行业，'
 '其中AI相关公司达<b>32只</b>、医药股<b>9只</b>。<br>\n'
 '          <b>仓位变化：</b>全部可比基金平均仓位由二季度末的<b>81.61%</b>降至三季度末的<b>78.32%</b>，'
 '降低3.29个百分点；其中股票型开放式基金平均仓位<b>88.04%</b>（降0.39个百分点）、'
 '混合型开放式基金<b>76.78%</b>（降3.76个百分点）。<br>\n'
 '          <b>调仓分歧：</b>易方达产业机遇混合基金经理杨宗昌表示，三季度增加了CXO、煤炭、有色金属及机械设备行业配置；'
 '嘉实成长增强混合基金经理陈涛表示，组合主要增加光通信、AI端侧、半导体测试以及有色金属方向持仓，'
 '减少前期涨幅较大的存储芯片、半导体设备和材料板块；嘉实科技创新混合基金经理王贵重表示，'
 '对AI算力部分持仓进行了减仓，同时增加AI应用和端侧AI标的。<br>\n'
 '          <b>对腾安启示：</b>公募整体仓位下调与重仓股结构向AI硬件＋医药CXO集中并存，'
 '货架展示须同时给出“仓位下降”与“结构集中”两个维度，避免用户把仓位变化误读为单一赛道景气；'
 '对上市不久即进入前十大重仓的个股，须在产品持仓页标注上市时点与建仓区间，'
 '不得以“公募重仓”替代风险揭示。')
C_S4 = ('      <!-- S4 Card: 公募三季度平均仓位降至78.32% 长鑫科技成第四大重仓股 (10-28 P1) -->\n\n'
        + card('p1', 'P1 重要关注', '🟡',
               '公募三季度平均仓位降至78.32%·长鑫科技上市3个月跻身第四大重仓股', '10-28', B_S4,
               [('https://paper.cnstock.com/html/2026-10/28/content_2282126.htm', '上海证券报电子版·10-28'),
                ('https://www.cnstock.com/commonDetail/814720', '中国证券网·10-28')],
               '影响：中') + '\n\n\n\n')
assert C_S4.count('<div class="card p') == 1
assert C_S4.count('<div') == C_S4.count('</div>')
s = s[:k1] + C_S4 + s[k2:]
oc('S4-replace')

# ============================================================
# 8) S6：市场行情速览 → 10-27 收盘
# ============================================================
s6s = s.find('Section 6')
c6 = s.find('<div class="card p3">', s6s)
e6s = s.find('<!-- ============ Section 7')
assert 0 < c6 < e6s
while s[e6s - 1] in ' \n\t':
    e6s -= 1
# 末尾多带一个 section 容器闭合 </div>，剥掉它
assert s[e6s - 6:e6s] == '</div>', repr(s[e6s - 30:e6s])
e6s -= 6
while s[e6s - 1] in ' \n\t':
    e6s -= 1
old6 = s[c6:e6s]
print("S6 old tail:", repr(s[e6s - 40:e6s + 30]))
assert old6.count('<div') == old6.count('</div>'), "S6 old unbalanced %d/%d" % (old6.count('<div'), old6.count('</div'))

NEW_S6 = (
'<div class="card p3">\n'
'        <div class="card-top">\n'
'          <div class="card-title">📈 A股、港股、美股统一10-27收盘·沪指3648.30 -1.33%｜创业板指跌3.41%</div>\n'
'          <div class="card-meta">\n'
'            <span class="priority-tag fyi">P3 知悉即可</span>\n'
'            <span class="date-tag">10-27</span>\n'
'          </div>\n'
'        </div>\n'
'        <div class="card-body">\n'
'          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">\n'
'            <div>\n'
'              <b>A股（10-27收盘）</b><br>\n'
'              上证指数 <b>3648.30</b> <span style="color:#52c41a;">-1.33%</span>（-49.22点）<br>\n'
'              深证成指 <b>11245.73</b> <span style="color:#52c41a;">-2.50%</span>（-288.65点）<br>\n'
'              创业板指 <b>2548.15</b> <span style="color:#52c41a;">-3.41%</span>（-90.08点）<br>\n'
'              科创综指 <b>1511.95</b> <span style="color:#52c41a;">-3.93%</span><br>\n'
'              沪深两市成交 <b>约1.46万亿元</b>，较上一交易日缩量约1478亿元<br>\n'
'              其中沪市约 <b>6724.14亿元</b> ＋ 深市约 <b>7885.27亿元</b>\n'
'            </div>\n'
'            <div>\n'
'              <b>港股（10-27收盘）与美股（美东10-27收盘）</b><br>\n'
'              恒生指数 <b>23041.32</b> <span style="color:#52c41a;">-0.73%</span>（-170.49点）<br>\n'
'              国企指数 <b>7766.91</b> <span style="color:#52c41a;">-0.45%</span>（-35.18点）<br>\n'
'              恒生科技 <b>3800.43</b> <span style="color:#52c41a;">-1.48%</span>（-57.10点）<br>\n'
'              道琼斯 <b>52377.57</b> <span style="color:#dc2626;">+0.03%</span>（+15.99点）<br>\n'
'              纳斯达克 <b>26477.81</b> <span style="color:#dc2626;">+1.18%</span>（+308.43点）<br>\n'
'              标普500 <b>7722.60</b> <span style="color:#dc2626;">+0.60%</span>（+45.83点）<br>\n'
'              港股主板成交 <b>1783.48亿港元</b><br>\n'
'              纽约12月交货原油 <b>99.90美元/桶</b> <span style="color:#52c41a;">-1.83%</span><br>\n'
'              伦敦12月交货布伦特 <b>113.88美元/桶</b> <span style="color:#52c41a;">-1.67%</span>\n'
'            </div>\n'
'            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">\n'
'              <b>取数口径：</b>A股取<b>10月27日收盘</b>（10月27日为交易日且已收盘）；上证指数、深证成指、创业板指的收盘点位与涨跌幅'
'经中国经济网10月27日《收评：沪指跌1.33% 电机板块逆势走强》与新华财经10月27日《收评：创业板指高开低走跌超3% 工商银行、建设银行再创新高》'
'双源交叉印证，科创综指1511.95点、跌3.93%取自新华财经同篇；沪深两市合计约<b>1.46万亿元</b>、较上一交易日缩量1478亿元为新华财经口径，'
'沪市约<b>6724.14亿元</b>、深市约<b>7885.27亿元</b>为中国经济网分市场成交额，两者合计约14609亿元，本期仅并列列出、'
'不与沪深北三市等其他口径混用。港股取<b>10月27日收盘</b>（新华社香港10月27日电）。'
'美股取<b>美东10月27日收盘</b>（新华社纽约10月27日电，对应北京时间10月28日凌晨），'
'板块方面标普500十一大板块六涨五跌，科技板块和非必需消费品板块分别以1.49%和1.36%的涨幅领涨，'
'能源板块和房地产板块分别以2.20%和0.91%的跌幅领跌。国际原油取<b>10月27日收盘</b>'
'（新华社纽约10月27日电：纽约商品交易所12月交货轻质原油期货、12月交货伦敦布伦特原油期货）。'
'贵金属本期未取得可在同一源内交叉验证的收盘点位，按铁律不补数值。<br>\n'
'              <b>A股（10-27）：</b>三大指数全天高开低走、尾盘快速回落，创业板指此前一度涨超1%。'
'银行板块逆势走强，工商银行、建设银行股价再创新高，沪农商行创年内新高；消费板块表现活跃，'
'食品饮料、零售方向领涨；半导体芯片股走低、医药板块走弱，软件开发、军工装备跌幅居前。'
'新华财经10月27日报道转述机构观点：中金公司认为AI办公是Agent迈向通用生产力的重要布局点；'
'招商证券判断27Q1将是端侧AI爆品出现的关键节点；中信证券认为端侧应用产业链今年初以来股价调整较为充分，'
'端侧有望首先迎来叙事及预期的改善。<br>\n'
'              <b>美股（美东10-27）：</b>三大股指齐涨、纳指涨超1%，存储与光通信板块继续走强，'
'与A股成长板块当日大幅回调形成对照。\n'
'            </div>\n'
'          </div>\n'
'        </div>\n'
'        <div class="card-footer">\n'
'          <a href="https://finance.ce.cn/stock/gsgdbd/202610/t20261027_3273131.shtml" target="_blank" '
'style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-27</span></a>\n'
'          <a href="https://m.cnfin.com/gs-lb//zixun/20261027/4486901_1.html" target="_blank" '
'style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-27</span></a>\n'
'          <a href="https://www.xinhuanet.com/fortune/20261027/0e20ae724d7643f1973529e0706c5505/c.html" target="_blank" '
'style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华社·港股·10-27</span></a>\n'
'          <a href="https://m.chinanews.com/wap/detail/chs/zw/jw694484.shtml" target="_blank" '
'style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国新闻网·美股·10-28</span></a>\n'
'          <span class="impact-tag medium">辅助决策</span>\n'
'        </div>\n'
'      </div>')
assert NEW_S6.count('<div') == NEW_S6.count('</div>'), "S6 new %d/%d" % (NEW_S6.count('<div'), NEW_S6.count('</div'))
s = s[:c6] + NEW_S6 + s[e6s:]
oc('S6')

# ============================================================
# 9) S7：时间线重写 12 条降序
# ============================================================
s7s = s.find('Section 7')
first = s.find('<div class="timeline-item">', s7s)
last = s.rfind('<div class="timeline-item">')
assert first < last
e7 = s.find('\n      </div>', last)
assert e7 > 0, "S7 last item close not found"
e7 = e7 + 1 + len('      </div>')
old7 = s[first:e7]
assert old7.count('<div ') == old7.count('</div>'), "S7 old %d/%d" % (old7.count('<div '), old7.count('</div'))
assert old7.count('<div class="timeline-item">') == 12, "S7 old items=%d" % old7.count('<div class="timeline-item">')

ITEMS = [
    ('red',  '2026-10-28', '公募三季报债基创新高'),
    ('red',  '2026-10-28', '主动ETF三天募满11只'),
    ('blue', '2026-10-28', '公募仓位降至78.32%'),
    ('blue', '2026-10-28', '月内32只FOF发新创纪录'),
    ('blue', '2026-10-27', '沪指跌1.33%失守3700点'),
    ('blue', '2026-10-27', '私募规模升至25.83万亿'),
    ('red',  '2026-10-26', '央行设立债市非银赎回便利'),
    ('red',  '2026-10-23', '证监会母基金新规征求意见'),
    ('blue', '2026-10-23', '首批18只主动ETF开售'),
    ('blue', '2026-10-22', '中基协修订八项估值指引'),
    ('blue', '2026-10-19', '公募探寻产投销考稳市路径'),
    ('blue', '2026-10-16', '公募高质量发展新规满一年'),
]
parts = []
for col, d, t in ITEMS:
    assert len(t) <= 25, "S7 title too long: %s" % t
    assert len(d) == 10
    parts.append(
        '      <div class="timeline-item">\n'
        '        <div class="timeline-dot %s"></div>\n'
        '        <div class="timeline-date">%s</div>\n'
        '        <div class="timeline-title">%s</div>\n'
        '      </div>' % (col, d, t))
NEW_S7 = '\n'.join(parts)
assert NEW_S7.count('<div ') == NEW_S7.count('</div>')
assert NEW_S7.count('<div class="timeline-item">') == 12
s = s[:first] + NEW_S7 + s[e7:]
oc('S7')

# ============================================================
# 10) 自审
# ============================================================
o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
print("FINAL open=%d close=%d" % (o, c))
assert o == c == 240, "div balance %d/%d expect 240/240" % (o, c)
assert s.count('</div>>') == 0
assert s.count('\ufffd') == 0
assert 'Section 8' not in s and 'S8' not in s

# marker / fingerprint / description
assert '<!-- daily-update: 2026-10-28 -->' in s
fp = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', s).group(1)
print("fingerprint:", fp)
assert fp == "公募三季|首批主动|私募自购|月内32只"

# S0 六项
s0 = s[s.find('Section 0'):s.find('Section 1')]
titles = [re.sub(r'<[^>]+>', '', m) for m in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', s0, re.S)]
assert len(titles) == 4, "S0 titles=%d" % len(titles)
assert re.search(r'<span class="section-title">今日焦点</span>', s0)
assert re.search(r'<span class="section-context">10月28日 · 4条今日要闻</span>', s0)
assert s0.count('<div class="card p') == 4
assert s0.count('action-box') == 0
assert len(re.findall(r'date-tag', s0)) == 4
print("S0 links=%d" % len(re.findall(r'href="', s0)))
assert len(re.findall(r'href="', s0)) == 6, "S0 links=%d" % len(re.findall(r'href="', s0))
for k in ['公募三季', '首批主动', '私募自购', '月内32']:
    assert any(k in t for t in titles), "fp key %s missing" % k

# 各 section 卡数
for i in range(0, 8):
    a = s.find('Section %d' % i); b = s.find('Section %d' % (i + 1))
    if a < 0: continue
    if b < 0: b = len(s)
    seg = s[a:b]
    print("S%d cards=%d comments=%d timeline=%d" % (
        i, len(re.findall(r'<div class="card ', seg)),
        len(re.findall(r'<!-- S%d Card:' % i, seg)),
        len(re.findall(r'<div class="timeline-item"', seg))))
sec = lambda i: s[s.find('Section %d' % i):(s.find('Section %d' % (i+1)) if s.find('Section %d' % (i+1))>0 else len(s))]
assert len(re.findall(r'<div class="card ', sec(1))) == 6
assert len(re.findall(r'<!-- S1 Card:', sec(1))) == 6
assert len(re.findall(r'<div class="card ', sec(2))) == 4
assert len(re.findall(r'<!-- S2 Card:', sec(2))) == 4
assert len(re.findall(r'<div class="card ', sec(4))) == 3
assert len(re.findall(r'<!-- S4 Card:', sec(4))) == 3
assert len(re.findall(r'<div class="card ', sec(5))) == 3
assert len(re.findall(r'<div class="card ', sec(6))) == 1
assert len(re.findall(r'<div class="timeline-item"', sec(7))) == 12
assert sec(7).count('timeline-desc') == 0

# date-tag T-14
bad = []
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s):
    mo, d = int(m.group(1)), int(m.group(2))
    if date(2026, mo, d) < T14:
        bad.append('%02d-%02d' % (mo, d))
print("date-tags:", re.findall(r'<span class="date-tag">([^<]*)</span>', s))
assert not bad, "超 T-14 date-tag: %s" % bad

# 全文件 mm-dd 越界（非 date-tag，人工确认）
mm = set()
for a, b in re.findall(r'(\d{2})-(\d{2})', s):
    if 1 <= int(a) <= 12 and 1 <= int(b) <= 31:
        mm.add('%s-%s' % (a, b))
print("all mm-dd:", sorted(mm))
over = [x for x in mm if date(2026, int(x[:2]), int(x[3:])) < T14]
print("越界 mm-dd:", sorted(over))

# 黑名单
BAD = ['stcn', 'cls.cn', '21jingji', 'yicai', 'guba.eastmoney', 'toutiao',
       'so.html5.qq.com', '163.com/dy', 'weibo.com', 'k.sina.com.cn',
       'q.fund.sohu.com', 'topnews.cn', 'futunn.com', 'jiantou8.com',
       'cofool.com', 'yanglee.com', 'cqcb.com', 'huangjinjiage.cn',
       'zhpd.dahe.cn', 'stockstar.com']
hits = [(u, b) for u in re.findall(r'href="(https?://[^"]+)"', s) for b in BAD if b in u]
print("blacklist hits:", hits)
assert not hits

# 深度法：卡片是否提前闭合
def depth_ok(seg):
    """所有 <div class="card pX"> 起始时所在的嵌套深度集合（长度 1 即未提前闭合）"""
    depths = []
    d = 0
    i = 0
    while i < len(seg):
        no = seg.find('<div', i); nc = seg.find('</div>', i)
        if no >= 0 and (nc < 0 or no < nc):
            if re.match(r'<div class="card p\d"', seg[no:no + 24]):
                depths.append(d)
            d += 1
            i = no + 4
        elif nc >= 0:
            d -= 1
            i = nc + 6
        else:
            break
    return sorted(set(depths))
for i in (0, 1, 2, 4, 5):
    print("S%d card-start depths: %s" % (i, depth_ok(sec(i))))
    assert depth_ok(sec(i)) == [2], "S%d depth %s" % (i, depth_ok(sec(i)))
print("S6 card-start depths: %s" % depth_ok(sec(6)))
assert depth_ok(sec(6)) == [1]

open(P, 'w', encoding='utf-8').write(s)
print("WRITE OK ->", P)
