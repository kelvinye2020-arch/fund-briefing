# -*- coding: utf-8 -*-
import io, re, sys
from datetime import date, timedelta

P = 'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = io.open(P, encoding='utf-8').read()
o0 = len(re.findall(r'<div\b', s)); c0 = len(re.findall(r'</div>', s))
print('BASE open=%d close=%d UFFFD=%d' % (o0, c0, s.count('\ufffd')))

def div_bounds(t, cs):
    gt = t.find('>', cs)
    assert gt != -1, 'no > after %d' % cs
    depth = 1
    i = gt + 1
    while depth > 0:
        mo = t.find('<div', i)
        mc = t.find('</div>', i)
        assert mc != -1, 'unbalanced at %d' % i
        if mo != -1 and mo < mc:
            depth += 1
            i = mo + 4
        else:
            depth -= 1
            i = mc + 6
    return cs, i

def card_bounds(t, cs):
    a, b = div_bounds(t, cs)
    assert t[a:b].count('<div class="card p') == 1, 'card_bounds hit %d cards' % t[a:b].count('<div class="card p')
    return a, b

def oc(tag):
    o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
    print('  %-12s open=%d close=%d drift_o=%+d drift_c=%+d' % (tag, o, c, o - o0, c - c0))

TODAY = date(2026, 10, 27)
T14 = TODAY - timedelta(days=14)
print('TODAY=%s T14=%s' % (TODAY, T14))

# ============ STEP 1: marker (闸0) ============
m = re.search(r'<!-- daily-update: (\d{4}-\d{2}-\d{2}) -->', s)
assert m, 'marker not found'
s = s[:m.start()] + '<!-- daily-update: 2026-10-27 -->' + s[m.end():]
print('STEP1 marker ok')

# ============ STEP 2: header 区间 badge (闸1) ============
upper = TODAY.strftime('%Y.%m.%d')
lower = T14.strftime('%Y.%m.%d')
badge_new = '📅 数据区间：%s — %s（每日更新）' % (lower, upper)
s2, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge_new, s)
assert n == 1, 'badge sub n=%d' % n
s = s2
print('STEP2 badge ->', badge_new)

# ============ STEP 3: fingerprint (闸6) + description (闸8) ============
FP = '央行设立|运作办法|首批主动|债券型ET'
mf = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', s)
assert mf, 'fingerprint meta missing'
s = s[:mf.start(1)] + FP + s[mf.end(1):]
print('STEP3 fingerprint ->', FP)

DESC = ('央行设立债市非银大额赎回互换便利|运作办法修订打开公募资产配置新空间|'
        '首批主动ETF两日累计募集超250亿元|债券型ETF年内净流入2414亿元规模破万亿|'
        '沪指10月26日收3697.52点涨0.19%·港股恒指涨0.51%·美股三大指数齐涨')
md = re.search(r'<meta name="description" content="([^"]*)">', s)
assert md, 'description meta missing'
s = s[:md.start(1)] + DESC + s[md.end(1):]
print('STEP4 description ok')

# ============ STEP 5: Stats Bar ============
SB_START = '<!-- Stats Bar -->'
SB_END = '\n\n  </div>\n\n<div class="main">'
a = s.find(SB_START); b = s.find(SB_END)
assert a != -1 and b != -1 and a < b, 'stats anchor fail a=%d b=%d' % (a, b)
assert s[a:b].count('class="stat-card"') == 4, 'stat-card count %d' % s[a:b].count('class="stat-card"')
def statcard(num, label, cls, chg):
    return ('    <div class="stat-card">\n'
            '      <div class="stat-number">%s</div>\n'
            '      <div class="stat-label">%s</div>\n'
            '      <div class="stat-change %s">%s</div>\n'
            '    </div>\n') % (num, label, cls, chg)
sb_new = (SB_START + '\n\n    <div class="stats-bar">\n'
    + statcard('250亿', '首批18只主动ETF两日累计募集·7只触及20亿元上限', 'up', '▲ 沪市9只中5只募满·预计带来逾350亿元增量资金')
    + statcard('3697.52', '沪指10-26收盘·涨0.19%·沪深两市成交16088亿元', 'up', '▲ 深证成指跌1.19%·创业板指跌1.71%')
    + statcard('2414亿', '债券型ETF年内申赎净流入·截至10月22日Wind口径', 'up', '▲ 53只合计规模10814亿元·占ETF总规模21.93%')
    + statcard('25.83万亿', '私募基金管理规模·截至9月末连续12个月创新高', 'up', '▲ 较8月末增0.08万亿·私募证券9.13万亿')
    + '\n')
sb_new = sb_new.rstrip('\n') + '\n'
s = s[:a] + sb_new + s[b:]
oc('stats')
assert s.count('class="stat-card"') == 4, 'stat-card total %d' % s.count('class="stat-card"')

# ============ STEP 6: S0 卡片整块替换 ============
S0_A = '      <!-- S0 Card 1'
S0_B = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 1'
a = s.find(S0_A); b = s.find(S0_B)
assert a != -1 and b != -1 and a < b, 'S0 anchor fail a=%d b=%d' % (a, b)
old = s[a:b]
assert old.count('<div class="card p') == 4, 'S0 old cards %d' % old.count('<div class="card p')
assert old.count('action-box') == 1, 'S0 old action-box %d' % old.count('action-box')

C1 = '''      <!-- S0 Card 1 (10-27 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 央行设立债市非银大额赎回互换便利·公募基金管理人可借入央行票据应对赎回</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-27</span>
          </div>
        </div>
        <div class="card-body">
          人民日报10月27日报道（记者吴秋余）：中国人民银行10月26日发布公告，决定设立债市非银大额赎回互换便利（Bond Market NBFI Swap Facility，简称BNSF）。在资管机构面临群体性流动性风险、债券市场出现系统性压力的特定情景下，支持具有系统性影响的银行理财子公司、公募基金管理人（或对应母行、证券母公司等），从中国人民银行借入央行票据用于市场回购融资，以购买本公司（或资管子公司）遭赎回公募产品的符合条件的债券或产品份额，并向中国人民银行抵押；参与机构应持续满足金融市场审慎管理要求、维护市场纪律。<br>
          <b>落地背景：</b>人民银行行长潘功胜此前在2026金融街论坛年会上表示，将会同金融监管总局、中国证监会设立应对非银机构大额赎回的流动性支持工具，BNSF设立意味着此项工具正式落地。中国经济网10月27日报道显示，截至2025年末银行理财产品存续规模达33万亿元、公募基金资产净值达38万亿元，资管机构已成为债券市场的重要参与力量，其流动性状况与市场交易、资产定价的联系更加紧密。<br>
          <b>适用边界：</b>中国人民银行有关部门负责人表示，BNSF是在特定情景下使用，不是日常流动性供应，仅限于债市出现大幅波动、资管机构群体性流动性风险的极端情形；设立目的是在债市出现大幅波动时阻断“赎回—抛售”循环，守住不发生系统性风险的底线。一般情况下，因机构自身信用状况恶化、信用债违约等产生的信用风险，仍按照市场化、法治化原则妥善处理，与工具应对流动性风险的功能定位有所区别。<br>
          <b>为何设立：</b>正常市场情况下，资管产品赎回通常可通过现金储备、资产到期回款和正常市场交易应对；当多家机构同时面临较大赎回压力时，集中出售债券可能带低市场价格，进一步影响产品净值和投资者预期，形成赎回与抛售相互强化的循环。<br>
          <b>对腾安启示：</b>BNSF是面向极端情形的应急流动性安排，不等于对债基类产品的隐性背书，对客传播严禁演绎为“债基不会跌、赎回有兜底”；固收及“固收+”货架须在极端行情下同步前置巨额赎回、延时到账与净值波动提示；涉及银行理财子公司与公募基金管理人的适用范围差异，须按产品管理人类型分别说明，不得笼统概括。
        </div>
        <div class="card-footer">
          <a href="https://finance.people.com.cn/n1/2026/1027/c1004-40822036.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民网·人民日报·10-27</span></a>
          <a href="https://www.ce.cn/xwzx/gnsz/gdxw/202610/t20261027_3272329.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-27</span></a>
          <a href="https://www.cnfin.com/yw-lb/detail/20261027/4486728_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-27</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 表述合规→债基、“固收+”与理财类页面不得引用BNSF作安全背书，仅在风险揭示中说明极端情形下存在央行应急流动性机制，且须注明“特定情景使用、非日常流动性供应”；<br>
            ② 赎回提示→在行情大幅波动时前置展示巨额赎回条款、确认时点与到账时效，避免投资者把应急机制理解为随时可退出；<br>
            ③ 适用范围→对客说明须区分银行理财子公司与公募基金管理人两类主体，不得把工具覆盖面概括为“所有固收产品”。
          </div>
        </div>
      </div>
'''

C2 = '''
      <!-- S0 Card 2 (10-27 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 运作办法修订打开公募资产配置新空间·FOF门槛降至5000万元·REITs按证券投资管理</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-27</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月27日报道（记者陈玥）：中国证监会近日就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，一系列针对公募资产配置的修订内容引发业内高度关注——将FOF成立门槛由2亿元降至5000万元，允许FOF投资ETF联接基金，将非FOF基金投资其他基金的比例上限由10%提高至30%，明确基金投资REITs按证券投资进行管理。<br>
          <b>发行端数据：</b>Choice数据显示，截至10月26日，今年以来公募FOF产品发行数量166只、发行份额1523.16亿份，占全市场新发基金比重达17.3%，均为2017年FOF类产品问世以来新高；今年以来全市场合计发行二级债基近200只、合计发行份额1379.86亿份。<br>
          <b>机构解读：</b>诺德基金分析称，成立门槛下调意味着差异化策略型产品门槛显著降低，部分规模有限、定位细分的FOF不必再为满足成立线而被动扩张；允许FOF投资ETF联接基金有望提升FOF配置效率、扩大可投标的池；非FOF基金投资其他基金比例上限由10%提升至30%，意味着“固收+”等中低波动产品能更大比例通过配置股票ETF实现收益增厚，“借道基金完成资产配置”不再局限于FOF单一品类。沪上一家中大型基金公司FOF基金经理表示，FOF底仓构建有望从“只能在场内ETF和主动基金之间选择”，逐步转向“ETF与联接基金双通道并行”，但联接基金仍面临双重收费、申赎效率、底层ETF流动性传导等问题，不会简单替代ETF。<br>
          <b>REITs身份转变：</b>博时基金REITs业务营运总监刘玄分析称，此次修订是公募基金参与REITs投资在制度层面的“松绑”，公募配置盘有望成为公募REITs市场从“供给驱动”转向“需求驱动”的关键变量。博时基金首席策略分析师陈显顺认为，投资者可用更低成本、更透明的工具买到与风险偏好更匹配的多元配置方案，集中于“固收+”等稳健型产品。<br>
          <b>行业布局：</b>2025年下半年兴证全球基金FOF投资与金融工程部更名为“多元资产配置部”；2026年初华夏基金提出打造可灵活拼接的“全球多资产全能平台”，总经理李一梅表示ETF是坚实底座、多元化产品是不断丰富的拼图元件。<br>
          <b>对腾安启示：</b>FOF门槛下调与互投比例放宽将带来更多小体量、细分策略的配置型产品，货架须补充“底层资产构成、双重收费、场内/场外份额差异”字段，禁止以“多元配置”笼统概括风险；REITs按证券投资管理后，涉及REITs持仓的产品须在风险等级与估值频率提示上同步更新；FOF发行份额创2017年以来新高属发行端统计，须标注统计时点与口径，不得演绎为收益预期。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/811816" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-27</span></a>
          <a href="https://www.cnfin.com/yw-lb/detail/20261027/4486728_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-27</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
'''

C3 = '''
      <!-- S0 Card 3 (10-26 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批主动ETF开售两日累计募集超250亿元·7只产品触及20亿元上限</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          新华财经10月26日上海电（记者杜康）：10月23日首批主动ETF开售当日，沪市摩根、易方达两只产品宣布一日募满、提前结募；10月26日第二个交易日，华泰柏瑞、平安、华夏3只沪市产品触及20亿元上限并宣布结募，沪市9只主动ETF中已有5只募满20亿元。记者从渠道了解到，全市场主动ETF已累计募集约250亿元，其中沪市主动ETF累计募集金额已超150亿元；据估算，境内首批主动ETF预计为市场带来增量资金逾350亿元。第一财经10月26日统计的口径为约253亿元（新浪财经转载），两者差异源于统计时点与样本范围不同，本卡并列列出、不做混用。<br>
          <b>累计进度：</b>加上10月23日率先售罄的摩根、易方达、富国3只，已有7只产品完成20亿元募集目标；首批18只产品于10月19日获证监会准予注册批复，沪深两市各9只，原定募集截止日集中在10月29日至30日。第一财经测算，若18只产品全部达到20亿元首募规模上限，预计为A股市场带来约360亿元增量资金。<br>
          <b>发行节奏：</b>本轮认购热潮出现在A股深度调整后的低位震荡阶段；多家基金公司拟在本周内完成发行，首批主动ETF上市时间初步定在11月下旬，已结募产品最快本周成立且成立即建仓。<br>
          <b>自购与渠道：</b>易方达、华夏、富国、汇添富各以2亿元固有资金认购旗下主动ETF，华安、工银瑞信各1亿元，6家管理人合计10亿元；摩根基金股东关联方另拟在产品上市后投入7500万美元（约合5亿元）；国泰海通证券计划运用自有资金不超过6.7亿元认购多只主动ETF，10月23日已认购2.59亿元。据中国基金报按Wind与国信证券经济研究所整理的明细，基金公司、股东方与券商合计认购约21.7亿元。<br>
          <b>对腾安启示：</b>“两日售罄”“比例配售”属募集进度结果，须与产品业绩、风险等级严格分离展示，不得演绎为热度推荐；管理人自购、股东方投入与券商自营认购性质不同，须分别标注资金来源、持有承诺与实施前提；成立即建仓意味着净值波动在建仓期内可能不完全跟随指数，须在详情页补充建仓期风险提示。
        </div>
        <div class="card-footer">
          <a href="https://m.cnfin.com/gs-lb//zixun/20261026/4486630_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-26</span></a>
          <a href="https://finance.sina.com.cn/jjxw/2026-10-26/doc-iniwpwiv2252214.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·第一财经·10-26</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
'''

C4 = '''
      <!-- S0 Card 4 (10-27 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🔵 债券型ETF年内净流入2414亿元·53只合计规模突破万亿元</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-27</span>
          </div>
        </div>
        <div class="card-body">
          经济参考报10月27日报道（记者柳川）：低利率、净值化、工具化三股力量交织下，债券ETF正从固收市场的“补充品种”，成长为资本市场服务中长期资金入市的重要基础设施。Wind数据显示，截至10月22日，全市场53只债券型ETF合计规模达10814亿元，占ETF市场总规模的21.93%，年内申赎净流入2414亿元。<br>
          <b>结构分布：</b>信用债指数ETF 35只合计规模7765亿元、占比超七成；利率债指数ETF 16只合计2348亿元；可转债指数ETF 2只合计688亿元。单只债券ETF平均规模达203.83亿元，规模超百亿元的已有36只、合计约9743亿元，占债券ETF总规模九成以上，呈现高度头部化、机构化特征。<br>
          <b>科创债赛道分化：</b>全市场15只科创债ETF规模超百亿元、合计2946亿元，科创债ETF嘉实以408亿元领跑，科创债ETF银华290亿元、汇添富279亿元、易方达222亿元、华夏221亿元紧随其后，科创债ETF华安58亿元是唯一规模低于百亿元的品种。资金端，科创债ETF永赢年内申赎净流入94亿元、易方达88亿元、华夏65亿元；招商基金、富国基金、鹏华基金旗下科创债ETF净流出均超50亿元，其中科创债ETF招商净流出97亿元，为年内净流出前三名。<br>
          <b>驱动因素：</b>债券ETF从2024年5月首破千亿元，到2025年全年净流入5527亿元，再到2026年站稳万亿关口。易方达基金债券指数投资部总经理李一硕表示，债券ETF可将场外离散成交的底层债券资产转化为可连续场内成交的投资交易工具，流动性较底层资产大幅改善。配套机制方面，深交所明确上市债券ETF可作为质押券参与协议回购、自2026年10月26日起施行，上交所同样将债券ETF纳入协议回购优质担保品范畴。<br>
          <b>机构建议：</b>中信建投认为近期长债波动主因是权益走弱带来的避险情绪与资金再配置，短期宜重配置、轻交易，严控久期与回撤；中金公司建议配置机构保持5年左右非金融信用债仓位，交易资金适度跟随利率债波段，但禁止过度信用下沉。<br>
          <b>对腾安启示：</b>债券ETF高度头部化、机构化，货架展示须区分信用债/利率债/可转债三类底层与久期风险，不得以“债券ETF”单一标签并列；科创债ETF内部资金分化明显，同类产品不得按规模简单排序推荐；净流入为申赎资金统计、非收益指标，须标注统计区间与口径，严禁与净值表现并列暗示。
        </div>
        <div class="card-footer">
          <a href="https://www.jjckb.cn/20261027/72ceaad14d6a436a86e48de350f3be94/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济参考报·10-27</span></a>
          <a href="https://www.cnfin.com/yw-lb/detail/20261027/4486728_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-27</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

s0_new = C1 + C2 + C3 + C4
s = s[:a] + s0_new + s[b:]
oc('s0')
s0seg = s[s.find('Section 0'):s.find('Section 1')]
assert s0seg.count('<div class="card p') == 4, 'S0 new cards %d' % s0seg.count('<div class="card p')
assert s0seg.count('action-box') == 1, 'S0 new action-box %d' % s0seg.count('action-box')
assert s.count('<!-- S0 Card') == 4, 'S0 comments %d' % s.count('<!-- S0 Card')

# ============ STEP 7: S0 section-context ============
CTX_OLD = '<span class="section-context">10月26日 · 4条今日要闻</span>'
CTX_NEW = '<span class="section-context">10月27日 · 4条今日要闻</span>'
assert s.count(CTX_OLD) == 1, 'ctx old count %d' % s.count(CTX_OLD)
s = s.replace(CTX_OLD, CTX_NEW)
assert s.count('<span class="section-title">今日焦点</span>') == 1, 'S0 title broken'
print('STEP7 context ok')

# ============ STEP 8: S4 替换 10-12 越界卡 ============
k = s.find('<!-- S4 Card: 公募固收+发展迎来三重共振 (10-12 P1) -->')
assert k != -1, 'S4 10-12 comment not found'
cs = s.find('<div class="card p', k)
a, b = card_bounds(s, cs)
assert s[a:b].count('10-12') >= 1
NEW_S4 = '''<!-- S4 Card: 私募基金总规模升至25.83万亿元·连续12个月创新高 (10-27 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 私募基金总规模升至25.83万亿元·连续12个月刷新历史纪录</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-27</span>
          </div>
        </div>
        <div class="card-body">
          证券日报网10月27日报道：中国证券投资基金业协会10月26日晚发布的最新私募基金数据显示，截至2026年9月末，全市场存续私募基金管理人1.84万家，管理基金数量14.57万只，管理基金规模25.83万亿元，较8月末的25.75万亿元增长0.08万亿元，再创历史新高；自2025年10月末首次突破22万亿元以来，私募基金总规模已连续12个月刷新历史纪录。<br>
          <b>分类型：</b>截至9月末，存续私募证券投资基金8.43万只、规模9.13万亿元；存续私募股权投资基金2.95万只、规模11.93万亿元；存续创业投资基金3.13万只、规模4.51万亿元。与8月末相比，私募证券投资基金与创业投资基金规模均小幅增长，私募股权投资基金规模持平。<br>
          <b>发行端：</b>9月全市场新备案私募基金1788只、新备案规模813.11亿元，其中新备案私募证券投资基金1058只、规模245.97亿元，新备案创业投资基金557只、规模409.84亿元，新备案私募股权投资基金173只、规模157.30亿元；当月创业投资基金新备案规模超过私募证券投资基金，跃居第一大品类。与2025年10月末相比，私募基金总规模共增长3.78万亿元，其中私募证券投资基金规模增长2.12万亿元、占同期总规模增量的56.08%，是规模增长的主要动力。<br>
          <b>机构观点：</b>星石投资相关负责人表示，10月以来股市快速回调已对AI相关信用风险担忧和交易层面筹码出清进行了较充分定价，短期存在超跌修复机会；中长期看全球AI资本开支周期尚未结束、科技领域国产替代需求未变，同时宏观政策持续推动国内需求企稳，传统核心资产亦存在边际修复可能。
        </div>
        <div class="card-footer">
          <a href="http://www.zqrb.cn/fund/jijindongtai/2026-10-27/A1793000661236.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报网·10-27</span></a>
          <a href="https://finance.china.com.cn/money/fund/20261027/6326823.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网财经·证券日报·10-27</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''
s = s[:k] + NEW_S4 + s[b:]
oc('s4')
assert s.count('<!-- S4 Card') == 3, 'S4 comments %d' % s.count('<!-- S4 Card')

# ============ STEP 9: S5 替换 10-12 越界卡 ============
k = s.find('<!-- S5 Card: 工银瑞信以AI重塑投研基因 (10-12 P1) -->')
assert k != -1, 'S5 10-12 comment not found'
cs = s.find('<div class="card p', k)
a, b = card_bounds(s, cs)
NEW_S5 = '''<!-- S5 Card: 基金公司“AI研究员”上岗·投研智能体进入平台化供给期 (10-26 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 从分析到发问·基金公司“AI研究员”上岗·头部机构进入平台化供给期</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月26日报道（记者闫军、曹雯璟）：天弘基金“AI研究员”出席晨会并与投研团队互动的画面在业内引发关注——研究员的分享被共享屏幕上的提示打断：“你对公司业务模块的盈利预测，与券商研报的一致预期存在明显差异，请说明理由。”发出提示的是天弘投研人员称为“AI研究员”的AI Challenge，它会综合卖方、买方和内部过往报告与研究员互动，一旦讲述内容与既有信息出现较大差异就会当场发问，嵌入在自研投研平台“弘研智策TIRD”之中。<br>
          <b>政策与梯队：</b>2025年5月证监会发布《推动公募基金高质量发展行动方案》，鼓励基金公司加大对人工智能、大数据等新兴技术的研究应用。中国基金报调研显示，公募行业初步形成三个梯队：易方达、汇添富、南方、嘉实等已建成企业级AI能力平台，投研全流程基本实现AI渗透；工银瑞信、招商、国泰、富国等在养老金运营、固收交易、智能问答等场景实现深度应用；其他公司仍在局部试点。多家机构预判2026年或是“投研智能体元年”。<br>
          <b>落地形态：</b>汇添富在关键岗位建设研究、投资助理、规则化投资、交易等Agent集群，“AI研究员”作为任务驱动的岗位化Agent已接管研究员约40%的基础案头工作；易方达以EWork平台为智能化应用载体，建设投研信息检索整理、对话式问答、研究分析与材料生成等模块，强调不替代人工判断或投资决策；招商基金已从早期技术试点进入平台化供给阶段，落地智能纪要、个股AI洞察、研报翻译与问答、AI信评报告等应用；广发基金核心平台“阿基米德”一体化投研系统服务固收、主动权益、被动指数、跨境投资等核心业务线。<br>
          <b>边界与共识：</b>业内人士表示，未来AI将重塑资管行业的“生产方式”，但不会改变“生产主体”；北京一家大型基金公司认为AI大幅降低信息获取门槛，超额收益来源将从信息差转向认知差。深圳一家基金公司提示挑战集中在AI输出结果的鉴别与证伪、产业底层认知与软信息解读、风控与长期基本面洞察三方面，极端市场环境下投研人员的独立思考与逆向决策能力仍至关重要。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR20261025110750429" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-26</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''
s = s[:k] + NEW_S5 + s[b:]
oc('s5')
assert s.count('<!-- S5 Card') == 3, 'S5 comments %d' % s.count('<!-- S5 Card')

# ============ STEP 10: S6 行情 ============
k6 = s.find('<!-- ============ Section 6')
cs = s.find('<div class="card p3">', k6)
assert cs != -1, 'S6 card not found'
a, b = card_bounds(s, cs)
S6 = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股、港股、美股统一10-26收盘·沪指3697.52 +0.19%｜创业板指跌1.71%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-26</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-26收盘）</b><br>
              上证指数 <b>3697.52</b> <span style="color:#dc2626;">+0.19%</span>（+7.04点）<br>
              深证成指 <b>11534.38</b> <span style="color:#52c41a;">-1.19%</span>（-139.45点）<br>
              创业板指 <b>2638.23</b> <span style="color:#52c41a;">-1.71%</span>（-45.87点）<br>
              科创综指 <b>1573.83</b> <span style="color:#52c41a;">-2.03%</span>｜北证50 <b>963.95</b> <span style="color:#52c41a;">-2.13%</span><br>
              沪深两市成交 <b>约16088亿元</b>，较上周五缩量3475亿元<br>
              其中沪市约 <b>7465.28亿元</b> ＋ 深市约 <b>8622.65亿元</b>
            </div>
            <div>
              <b>港股（10-26收盘）与美股（美东10-26收盘）</b><br>
              恒生指数 <b>23211.81</b> <span style="color:#dc2626;">+0.51%</span>（+118.44点）<br>
              国企指数 <b>7802.09</b> <span style="color:#dc2626;">+0.59%</span>（+45.84点）<br>
              恒生科技 <b>3857.53</b> <span style="color:#52c41a;">-0.36%</span>（-14.13点）<br>
              道琼斯 <b>52361.58</b> <span style="color:#dc2626;">+0.28%</span>（+146.42点）<br>
              纳斯达克 <b>26169.38</b> <span style="color:#dc2626;">+0.82%</span>（+214.04点）<br>
              标普500 <b>7676.77</b> <span style="color:#dc2626;">+0.70%</span>（+53.09点）<br>
              港股主板成交 <b>1757.58亿港元</b><br>
              纽约12月交货原油 <b>101.76美元/桶</b> <span style="color:#52c41a;">-1.46%</span><br>
              伦敦12月交货布伦特 <b>115.81美元/桶</b> <span style="color:#52c41a;">-0.78%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>10月26日收盘</b>（10月26日为交易日且已收盘）；上证指数、深证成指、创业板指、科创综指、北证50收盘点位与涨跌幅经行情数据终端与上海证券报10月27日《红利资产走势强劲 沪指企稳回升收盘飘红》、中国证券报10月27日《增量资金入市力度加大》双源交叉印证；沪市约<b>7465.28亿元</b>、深市约<b>8622.65亿元</b>为沪深两市分市场成交额（行情数据终端口径），合计约16088亿元，与上海证券报“沪深两市合计成交16088亿元、较上周五缩量3475亿元”一致，本期仅并列列出、不与沪深北三市等其他口径混用。港股取<b>10月26日收盘</b>（新华社香港10月26日电）。美股取<b>美东10月26日收盘</b>（新华社纽约10月26日电，对应北京时间10月27日凌晨）。国际原油取<b>10月26日收盘</b>（新华社纽约10月26日电：纽约商品交易所12月交货轻质原油期货、12月交货伦敦布伦特原油期货）。贵金属本期未取得可在同一源内交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-26）：</b>主要股指走势分化，银行、白酒、石油石化等传统红利资产表现强势，带动沪指收盘小幅上涨；AI相关科技题材继续调整，PCB、存储芯片等硬件板块跌幅居前，拖累双创指数走弱。上海证券报10月27日报道显示，中证红利低波指数（H30269）当日上涨1.41%，月初至今累计上涨1.24%；中国石油收盘大涨4.94%，以复权价计算盘中创2008年5月以来逾18年新高；宇树科技涨7.69%，近7个交易日累计反弹接近70%。中国证券报10月27日报道显示，当日上涨股票2252只、59只涨停，下跌3157只；申万一级行业中石油石化、银行、交通运输分别上涨2.41%、1.76%、1.68%领涨，电子、通信、有色金属分别下跌3.79%、2.95%、2.79%领跌。<br>
              <b>港股（10-26）：</b>新华社香港10月26日电，香港恒生指数涨118.44点、涨幅<b>0.51%</b>收报<b>23211.81</b>点，全日主板成交<b>1757.58亿港元</b>；国企指数涨45.84点、涨幅0.59%收<b>7802.09</b>点；恒生科技指数跌14.13点、跌幅0.36%收<b>3857.53</b>点。蓝筹股方面腾讯控股涨0.1%收报386.4港元、香港交易所涨0.43%收报372.4港元、中国移动涨0.26%收报77.3港元、汇丰控股跌0.21%收报142.2港元；石油石化股方面中国石油股份涨5.78%收报10.16港元、中国海洋石油涨3.55%收报23.94港元。<br>
              <b>美股（美东10-26）：</b>新华社纽约10月26日电，纽约股市三大股指26日上涨。道琼斯工业平均指数比前一交易日上涨146.42点、涨幅<b>0.28%</b>收于<b>52361.58</b>点；标准普尔500种股票指数上涨53.09点、涨幅<b>0.70%</b>收于<b>7676.77</b>点；纳斯达克综合指数上涨214.04点、涨幅<b>0.82%</b>收于<b>26169.38</b>点。板块方面，标普500指数十一大板块七涨四跌，科技板块和工业板块分别以1.50%和1.40%的涨幅领涨，通信服务板块和必需消费品板块分别以1.42%和0.13%的跌幅领跌。<br>
              <b>对腾安提示：</b>A股10月26日呈现“红利走强、科技回调”的结构分化，沪指微涨而双创指数跌逾1%，货架与持仓页须按各自指数与行业分别刷新净值日期与估值口径，不得用沪指微涨概括全市场；国际油价26日回落、美股三大指数齐涨，涉及原油、商品主题基金与QDII产品的估值提示须按各自市场分别更新；债市方面央行当日设立非银大额赎回互换便利，固收类页面同步前置极端情形赎回提示。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-26收盘，美股为美东2026-10-26收盘</span>
          <span class="source-tag">数据来源：行情数据终端、上海证券报、中国证券报（A股）；新华社（港股、美股、国际原油）</span>
        </div>
      </div>'''
s = s[:a] + S6 + s[b:]
oc('s6')
assert s.count('date-tag">10-23<') == 0, 'stale 10-23 date-tag remains'

# ============ STEP 11: S7 时间线 ============
k7 = s.find('<!-- ============ Section 7')
first = s.find('<div class="timeline-item">', k7)
assert first != -1, 'S7 first item not found'
items = []
for mm in re.finditer(r'<div class="timeline-item">', s):
    if mm.start() > k7:
        items.append(mm.start())
assert len(items) == 12, 'S7 items %d' % len(items)
a, b_last_end = div_bounds(s, items[-1])
def item(dot, d, t):
    return ('<div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>') % (dot, d, t)
def itemn(dot, d, t):
    return ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>') % (dot, d, t)
blocks = [
    item('red',   '2026-10-27', '央行设立债市非银赎回便利'),
    itemn('red',  '2026-10-27', '公募资产配置制度补位'),
    itemn('blue', '2026-10-27', '债券型ETF年内流入2414亿'),
    itemn('red',  '2026-10-26', '主动ETF两日募资超250亿'),
    itemn('blue', '2026-10-26', '私募规模升至25.83万亿'),
    itemn('blue', '2026-10-26', '沪指涨0.19%收3697.52点'),
    itemn('red',  '2026-10-23', '首批18只主动ETF开售'),
    itemn('blue', '2026-10-22', '中基协修订八项估值指引'),
    itemn('blue', '2026-10-22', '沪指跌1.48%失守3700点'),
    itemn('blue', '2026-10-20', '央行拟设非银流动性工具'),
    itemn('blue', '2026-10-16', '公募高质量发展新规满一年'),
    itemn('red',  '2026-10-16', '首批新能源金属50ETF获批'),
]
new7 = '\n'.join(blocks)
s = s[:items[0]] + new7 + s[b_last_end:]
oc('s7')
s7 = s[s.find('Section 7'):]
assert s7.count('class="timeline-item"') == 12, 'S7 new items %d' % s7.count('class="timeline-item"')
assert 'timeline-desc' not in s7, 'timeline-desc found'
for blk in blocks:
    tt = re.search(r'<div class="timeline-title">([^<]+)</div>', blk).group(1)
    assert len(tt) <= 25, 'timeline title too long: %s' % tt

# ============ 终检 ============
o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
print('FINAL open=%d close=%d drift_o=%+d drift_c=%+d' % (o, c, o - o0, c - c0))
assert o == c == o0, 'div drift'
assert s.count('</div>>') == 0
assert s.count('\ufffd') == 0
assert 'Section 8' not in s
# date-tag >= T-14
for mm in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s):
    dt = date(2026, int(mm.group(1)), int(mm.group(2)))
    assert dt >= T14, 'date-tag out of window: %s' % dt
print('date-tag check ok')
# fingerprint / description 预检
s0seg = s[s.find('Section 0'):s.find('Section 1')]
titles = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', s0seg, re.S)]
print('S0 titles:', titles)
fps = [x for x in FP.split('|') if x.strip()]
assert len(fps) == len(titles), 'fp seg %d vs titles %d' % (len(fps), len(titles))
for seg in fps:
    assert any(seg[:4] in t for t in titles), 'fp seg %s not in titles' % seg
dsegs = [x.strip() for x in DESC.split('|') if x.strip()]
for seg in dsegs[:len(fps)]:
    assert any(seg[:4] in t for t in titles), 'desc seg %s not in titles' % seg
print('fp/desc precheck ok')
assert s.count('<span class="section-context">10月27日 · 4条今日要闻</span>') == 1
print('ALL ASSERT PASSED')

io.open(P, 'w', encoding='utf-8').write(s)
print('WRITTEN len=%d' % len(s))
