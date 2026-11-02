# -*- coding: utf-8 -*-
import io, re, sys
from datetime import date, timedelta

P = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
LOG = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\_update_1102_out.txt'
sys.stdout = io.open(LOG, 'w', encoding='utf-8')

s = io.open(P, encoding='utf-8').read()
TODAY = date(2026, 11, 2)
O0, C0 = s.count('<div'), s.count('</div>')
print('BASE open=%d close=%d' % (O0, C0))

def counts(tag):
    o, c = s.count('<div'), s.count('</div>')
    print('  [%s] open=%d close=%d  drift_o=%+d drift_c=%+d' % (tag, o, c, o-O0, c-C0))
    return o, c

# ---------------- 1. marker / description / fingerprint ----------------
s = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', '<!-- daily-update: 2026-11-02 -->', s, count=1)
assert '<!-- daily-update: 2026-11-02 -->' in s

NEW_DESC = ('15只主动ETF顶格完成募集·18只中14只启动比例配售|'
            '公募加码医药·药明康德成第三大重仓股|'
            '中小公募寻求差异化突围·运作办法拟下调门槛|'
            '10月8只宽基ETF净流入超百亿合计超2686亿|'
            '沪指10月30日收3599.02点跌1.44%·纳指跌2.86%·COMEX12月黄金跌3.29%')
s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+NEW_DESC+m.group(2), s, count=1)
assert NEW_DESC in s

NEW_FP = '15只主动|公募加码|中小公募|10月8只'
s = re.sub(r'(<meta name="content-fingerprint" content=")[^"]*(")', lambda m: m.group(1)+NEW_FP+m.group(2), s, count=1)
assert NEW_FP in s

# ---------------- 2. header 数据区间 ----------------
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
badge_new = '📅 数据区间：%s — %s（每日更新）' % (lower, upper)
s2 = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge_new, s)
assert s2 != s and badge_new in s2, 'badge replace failed'
s = s2
print('BADGE ->', badge_new)
counts('meta+badge')

# ---------------- 3. Stats Bar ----------------
def stat_card(num, label, chg, cls='up'):
    return ('<div class="stat-card">\n'
            '      <div class="stat-number">%s</div>\n'
            '      <div class="stat-label">%s</div>\n'
            '      <div class="stat-change %s">%s</div>\n'
            '    </div>' % (num, label, cls, chg))

STATS = [
 stat_card('15只',
   '首批主动ETF顶格完成募集·18只中15只结募、14只启动比例配售（中国证券报，11月2日）',
   '▲ 预计11月下旬集中上市·18只全部募满将带来360亿元增量'),
 stat_card('3599.02',
   '沪指10-30收盘·跌1.44%·沪深两市成交16744.63亿元（新华财经·中国经济网，10月30日收盘）',
   '▼ 深证成指跌2.73%·创业板指跌4.13%', 'down'),
 stat_card('2686亿元',
   '10月8只宽基ETF净流入额均超百亿元·合计净流入超2686亿元（Wind，每日经济新闻11月2日）',
   '▲ 截至10-30全市场ETF份额36702.57亿份·规模49677.42亿元'),
 stat_card('1.94个百分点',
   '医药为三季度主动权益基金加仓最多行业·加仓幅度1.94个百分点（国盛证券测算，新华财经11月2日）',
   '▲ 药明康德成公募第三大重仓股·1083只基金重仓'),
]
sb_open = '<div class="stats-bar">'
i0 = s.find(sb_open)
assert i0 > 0
END_STATS = '\n\n  </div>\n\n<div class="main">'
i1 = s.find(END_STATS, i0)
assert i1 > i0
seg = s[i0:i1]
assert seg.count('<div class="stat-card">') == 4, seg.count('<div class="stat-card">')
new_seg = sb_open + '\n    ' + '\n    '.join(STATS) + '\n'
s = s[:i0] + new_seg + s[i1:]
assert s.count('<div class="stat-card">') == 4
counts('stats-bar')

# ---------------- 4. S0 整块换卡 ----------------
def action_box(items):
    return ('        <div class="action-box">\n'
            '          <div class="action-label">⚡ 腾安行动建议</div>\n'
            '          <div class="action-text">\n'
            '            ' + '<br>\n            '.join(items) + '\n'
            '          </div>\n'
            '        </div>')

def card0(pcls, ptag, ptext, dtag, title, body, links, action=None):
    h = '      <div class="card %s">\n' % pcls
    h += '        <div class="card-top">\n'
    h += '          <div class="card-title">%s</div>\n' % title
    h += '          <div class="card-meta">\n'
    h += '            <span class="priority-tag %s">%s</span>\n' % (ptag, ptext)
    h += '            <span class="date-tag">%s</span>\n' % dtag
    h += '          </div>\n'
    h += '        </div>\n'
    h += '        <div class="card-body">\n          %s\n        </div>\n' % body
    h += '        <div class="card-footer">\n'
    for u, t in links:
        h += ('          <a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;">'
              '<span class="source-tag">%s</span></a>\n' % (u, t))
    h += '          <span class="impact-tag high">影响：高</span>\n'
    h += '        </div>\n'
    if action:
        h += action_box(action) + '\n'
    h += '      </div>'
    return h

C1_BODY = ('中国证券报电子版11月2日报道（记者张舒琳）：首批主动ETF发行接近收官。自<b>10月23日</b>启动发行以来，'
 '首批主动管理ETF掀起一轮认购热潮。截至<b>10月30日</b>，首批<b>18只</b>主动ETF中已有<b>15只</b>相继公告结束募集，'
 '其中<b>14只</b>产品因募集规模超过<b>20亿元</b>上限而启动比例配售。<br>\n'
 '          <b>结募节奏：</b>10月23日发行首日，摩根资产管理（中国）、易方达基金、富国基金旗下产品率先一日售罄，单日募集规模达20亿元上限；'
 '10月26日南方基金、华泰柏瑞基金、华夏基金、平安基金旗下产品达上限提前结募；10月27日大成基金、天弘基金、招商基金、汇添富基金旗下产品提前结募；'
 '10月28日华安基金、10月29日永赢基金、10月30日工银瑞信基金与国泰基金旗下产品陆续提前结束募集并启动末日比例配售。<br>\n'
 '          <b>自购与员工认购：</b>除基金公司固有资金自购外，高管、基金经理及其他从业人员也密集认购，华泰柏瑞价值精选主动ETF、'
 '摩根大盘成长主动ETF等获得员工认购上百万份；10月30日建信基金公告，将运用固有资金<b>1亿元</b>在认购期投资建信均衡优选主动管理ETF，'
 '并承诺持有期限不低于1年。<br>\n'
 '          <b>持有人与增量测算：</b>持有人数量最多的是南方均衡配置主动管理ETF，达<b>26874户</b>；其次是华泰柏瑞价值精选主动ETF，达<b>25002户</b>；'
 '招商价值智选、易方达品质均衡、大成红利智选认购户数均超过2万户。目前仍有<b>3只</b>主动ETF在募集期，若18只全部募满，'
 '预计为市场带来<b>360亿元</b>增量资金，市场普遍预计于11月下旬迎来产品集中上市。<br>\n'
 '          <b>对腾安启示：</b>主动ETF由"发行热度"转入"上市运作"，货架须同步补齐策略标签（均衡／红利／价值／量化／大盘成长）'
 '与PCF每日披露入口，上市后持续跟踪做市质量与折溢价；推介口径不得只讲"顶格募集"，须提示建仓期与业绩基准偏离风险。')

C1_ACT = [
 '1. 货架侧：为首批主动ETF单设"主动ETF"专区，按五大策略（均衡／红利／价值／量化／大盘成长）分组，'
 '并同步展示业绩比较基准、PCF每日披露入口与做市商信息，11月下旬集中上市前完成页面预埋。',
 '2. 内容侧：撰写"主动ETF与被动ETF、普通主动权益基金有何不同"科普，重点解释每日披露持仓带来的透明度提升，'
 '以及建仓期净值波动与基准偏离的可能，避免投资者把"基金公司自购"直接理解为收益保障。',
 '3. 合规侧：复核主动ETF的宣传素材，不得使用"顶格募集""一日售罄"等暗示稀缺或收益的表述；'
 '员工及高管自购信息须与基金份额持有人信息一并如实披露，不得单独放大解读。',
]

C2_BODY = ('新华财经上海11月2日电（记者赵明超）：近期医药板块重回公募投资主线。最新披露的公募基金2026年三季报显示，'
 '主动权益类基金三季度加仓医药行业。据国盛证券测算，剔除行业涨跌带来的权重变化后，三季度医药是主动权益基金加仓最多的行业，'
 '加仓幅度为<b>1.94个百分点</b>。<br>\n'
 '          <b>重仓结构：</b>天相投顾数据显示，截至三季度末有<b>9只</b>医药股位居公募前五十大重仓股，主要集中在创新药和CXO领域；'
 '其中药明康德成为基金第三大重仓股，获<b>1083只</b>基金重仓持有，并新晋谢治宇管理的兴全合润混合基金前十大重仓股。<br>\n'
 '          <b>基金经理动向：</b>睿远成长价值混合傅鹏博、鹏华新兴成长混合梁浩均在三季报中表示增加了医药股持仓；'
 '易方达供给改革混合（杨宗昌）二季度末前十大重仓股中没有医药股，三季度末药明康德、康龙化成进入且药明康德为第一大重仓股；'
 '华安汇宏精选混合（桑翔宇）药明康德、金斯瑞生物科技、药明生物新晋前十大重仓股。<br>\n'
 '          <b>调研与发行：</b>截至10月29日，近一个月机构调研热度前十的细分行业中有三个属于医药板块（医疗器械、化学制药、生物医药）；'
 '同期有<b>5只</b>医药主题基金正在或即将发行，中欧基金同时推出2只。<br>\n'
 '          <b>对腾安启示：</b>医药主题基金集中发行叠加资金涌入，货架须按"创新药／CXO／医疗器械"细分打标并前置估值与临床兑现提示；'
 '对单季规模爆发式增长的产品须标注规模骤增对策略容量的影响，不得以短期规模增长作为推荐依据。')

C3_BODY = ('中国证券报11月2日报道：今年6月，证监会主席吴清在陆家嘴论坛提出推出支持中小基金公司规范健康发展的一揽子措施，'
 '坚持分类监管、突出特色，在产品布局与业务准入等方面给予适当倾斜；此后已有地方证监局走访辖区多家代表性中小公募机构调研经营现状。'
 '近日证监会就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，'
 '盈米基金研究院认为本次修订的多项条款对资源禀赋相对有限的中小公募机构构成实质性利好。<br>\n'
 '          <b>三方面利好：</b>一是权益类基金成立门槛大幅下调，中小机构可在市场底部逆周期布局有长期价值的产品，'
 '为"以产品力换生存空间"提供制度通道；二是注册程序提速，缩短新产品上市周期，产品策略可更敏捷响应市场需求；'
 '三是工具箱拓宽，在自建投研团队覆盖不足的领域可通过ETF等工具化配置承接客户需求，以"类FOF"模式实现差异化资产配置能力。<br>\n'
 '          <b>机构实践：</b>长安基金表示将储备"固收+"、公募REITs作为差异化突围主线——"固收+"按回撤控制目标搭建分层梯度产品矩阵，'
 '公募REITs协同股东万联证券挖掘项目机会；华银基金表示新规体现监管鼓励权益产品发展、重持营轻首发、重视长期业绩积累的思路。<br>\n'
 '          <b>渠道与评价：</b>有观点建议引导银行、保险、理财、养老金等机构资金建立中小特色基金白名单机制；'
 '晨星（中国）基金研究中心总监孙珩表示，行业评价更加重视长期业绩、风格稳定性和投资者回报，有助于弱化单纯"以规模论英雄"的竞争逻辑。<br>\n'
 '          <b>对腾安启示：</b>中小机构产品将更聚焦细分赛道，货架须按策略与赛道颗粒度做标签化呈现，避免只按公司规模排序；'
 '引入中小机构产品时须核验其长期业绩与风格稳定性，不以首发规模作为主要筛选条件。')

C4_BODY = ('每日经济新闻11月2日报道（每经记者肖芮冬、编辑赵云）：Wind数据显示，截至<b>10月30日</b>，'
 '10月资金净流入额居前20的ETF名单中有<b>8只</b>宽基ETF单月净流入额过百亿元，合计净流入额超<b>2686亿元</b>。<br>\n'
 '          <b>10月30日单日：</b>沪深300ETF华泰柏瑞份额增加13.91亿份、净流入额<b>56.72亿元</b>；'
 '创业板ETF易方达份额增加16.17亿份、净流入额<b>39.99亿元</b>；科创50ETF华夏份额增加22.71亿份、净流入额<b>28.48亿元</b>。'
 '流出方面，科创债ETF嘉实净流出21.99亿元、公司债ETF易方达净流出14.23亿元、信用债ETF海富通净流出10.34亿元。<br>\n'
 '          <b>总量与结构：</b>截至10月30日，全市场ETF份额为<b>36702.57亿份</b>、总规模为<b>49677.42亿元</b>；'
 '近一周份额增加最大的行业为金融（33只基金跟踪），份额增加最大的指数标的为中证A500（40只基金跟踪），'
 '收益最高的指数标的为国新港股通央企红利（+5.89%，3只基金跟踪）。<br>\n'
 '          <b>口径提示：</b>同日另有东方财富Choice口径称10月30日ETF资金整体净流入140.55亿元、其中股票型净流入272.14亿元，'
 '与上述单只产品统计范围不同，本期只采用每经／Wind口径、不与Choice口径混用。<br>\n'
 '          <b>对腾安启示：</b>宽基ETF持续吸金而科创债、信用债ETF净流出，说明资金在"权益底仓"与"固收避险"之间再平衡仍在延续；'
 '产品页须区分"宽基底仓"与"成长弹性"两类需求，不得把宽基净流入直接演绎为全市场上涨预期。')

S0_CARDS = [
 ('      <!-- S0 Card 1 (11-02 P0) -->\n      ' + card0(
    'p0', 'urgent', 'P0 紧急必看', '11-02',
    '🔴 15只主动ETF顶格完成募集·18只中14只启动比例配售·预计11月下旬集中上市',
    C1_BODY,
    [('https://epaper.cs.com.cn/zgzqb/html/2026-11/02/nw.D110000zgzqb_20261102_2-J06.htm', '中国证券报电子版·11-02'),
     ('https://finance.sina.com.cn/roll/2026-11-02/doc-inixicic0456745.shtml', '新浪财经·新华财经·11-02')],
    C1_ACT)),
 ('      <!-- S0 Card 2 (11-02 P1) -->\n      ' + card0(
    'p1', 'important', 'P1 重要关注', '11-02',
    '🟡 公募加码医药·三季度主动权益加仓最多行业·药明康德成第三大重仓股',
    C2_BODY,
    [('https://m.cnfin.com/gs-lb//zixun/20261102/4489531_1.html', '新华财经·11-02')])),
 ('      <!-- S0 Card 3 (11-02 P1) -->\n      ' + card0(
    'p1', 'important', 'P1 重要关注', '11-02',
    '🟡 中小公募寻求差异化突围·运作办法拟下调权益类成立门槛·注册提速',
    C3_BODY,
    [('https://epaper.cs.com.cn/zgzqb/html/2026-11/02/nw.D110000zgzqb_20261102_1-J04.htm', '中国证券报电子版·11-02'),
     ('https://www.cs.com.cn/tzjj/01/2026/11/02/detail_2026110210049040.html', '中证网·中国证券报·11-02')])),
 ('      <!-- S0 Card 4 (11-02 P2) -->\n      ' + card0(
    'p2', 'normal', 'P2 建议了解', '11-02',
    '🔵 10月8只宽基ETF净流入均超百亿·合计超2686亿元·全市场ETF规模4.97万亿元',
    C4_BODY,
    [('https://news.qq.com/rain/a/20261102A030WP00', '腾讯新闻·每日经济新闻·11-02'),
     ('https://stock.eastmoney.com/a/202611023917851343.html', '东方财富网·Choice口径·11-02')])),
]

a0 = s.find('Section 0')
g0 = s.find('<div class="card-grid">', a0)
assert g0 > 0
END_S0 = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 1'
e0 = s.find(END_S0, g0)
assert e0 > g0
old_s0 = s[g0:e0]
assert old_s0.count('<div class="card p') == 4, old_s0.count('<div class="card p')
n_act_new = sum(1 for c in S0_CARDS if 'action-box' in c)
n_act_old = old_s0.count('action-box')
s = s[:g0] + '<div class="card-grid">\n' + '\n\n'.join(S0_CARDS) + '\n' + s[e0:]
print('S0 action-box old=%d new=%d' % (n_act_old, n_act_new))
counts('S0 cards')

# ---- 另一步：S0 section-context ----
CTX_OLD = '10月30日 · 4条今日要闻'
CTX_NEW = '11月2日 · 4条今日要闻'
assert s.count(CTX_OLD) == 1, s.count(CTX_OLD)
s = s.replace(CTX_OLD, CTX_NEW, 1)
assert s.count(CTX_NEW) == 1
mm = re.search(r'section-context">([^<]*)<', s[s.find('Section 0'):])
assert mm.group(1) == CTX_NEW, mm.group(1)
print('S0 context ->', mm.group(1))
counts('S0 context')

# ---------------- 5. S1 删旧卡 ----------------
def seg_bounds(sec_name, next_sec):
    a = s.find(sec_name); b = s.find(next_sec)
    return a, b

def depth_end(t, cs):
    gt = t.find('>', cs)
    depth = 1
    i = gt + 1
    while i < len(t):
        if t.startswith('<div', i):
            depth += 1; i += 4
        elif t.startswith('</div>', i):
            depth -= 1
            if depth == 0:
                return i
            i += 6
        else:
            i += 1
    raise AssertionError('depth_end not found')

def delete_cards_by_tag(sec_name, next_sec, bad_tags):
    global s
    for bt in bad_tags:
        a, b = seg_bounds(sec_name, next_sec)
        seg = s[a:b]
        found = False
        for m in re.finditer(r'<div class="card p\d">', seg):
            cs = m.start()
            ce = depth_end(seg, cs)
            sub = seg[cs:ce]
            if 'date-tag">%s<' % bt in sub:
                k = seg.rfind('<!--', 0, cs)
                assert k >= 0 and seg[k:cs].count('-->') == 1, 'comment not found'
                assert '</div>' not in seg[k:cs], 'comment belongs to previous card'
                assert seg[cs:ce].count('<div class="card p') == 1
                s = s[:a+k] + s[a+ce+len('</div>'):]
                found = True
                break
        assert found, 'card with tag %s not found in %s' % (bt, sec_name)

def append_card(sec_name, next_sec, newcard):
    global s
    a, b = seg_bounds(sec_name, next_sec)
    seg = s[a:b]
    lc = seg.rfind('<div class="card p')
    assert lc > 0
    ce = depth_end(seg, lc)
    assert seg[lc:ce + 6].count('<div class="card p') == 1
    ins = a + ce + len('</div>')
    s = s[:ins] + '\n\n' + newcard + s[ins:]

delete_cards_by_tag('Section 1', 'Section 2', ['10-16', '10-16', '10-16', '10-27'])
a, b = seg_bounds('Section 1', 'Section 2')
assert s[a:b].count('<div class="card p') == 2, s[a:b].count('<div class="card p')
counts('S1 delete')

CUR_SEC = 'S1'
def card1(pcls, ptag, ptext, dtag, title, body, links):
    h = '      <!-- %s Card (%s %s) -->\n\n      <div class="card %s">\n\n' % (CUR_SEC, dtag, pcls, pcls)
    h += '        <div class="card-top">\n\n'
    h += '          <div class="card-title">%s</div>\n\n' % title
    h += '          <div class="card-meta">\n\n'
    h += '            <span class="priority-tag %s">%s</span>\n\n' % (ptag, ptext)
    h += '            <span class="date-tag">%s</span>\n\n' % dtag
    h += '          </div>\n\n'
    h += '        </div>\n\n'
    h += '        <div class="card-body">\n\n          %s\n        </div>\n' % body
    h += '        <div class="card-footer">\n\n'
    for u, t in links:
        h += ('          <a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;">'
              '<span class="source-tag">%s</span></a>\n\n' % (u, t))
    h += '          <span class="impact-tag medium">影响：中</span>\n        </div>\n      </div>'
    return h

S1_A_BODY = ('经济参考报11月2日报道：近日，华夏基金与全球资管巨头富兰克林邓普顿在深圳签署战略合作谅解备忘录。'
 '根据备忘录，双方将围绕联合产品开发、市场洞察共享、投资专业知识交流等展开深度合作，并在获得相关监管部门批准的前提下，'
 '探索在香港、欧洲UCITS及美国ETF等不同架构下开发联名ETF产品。<br>\n'
 '          <b>合作进阶：</b>这是双方继9月底两只合作开发ETF在港交所上市之后合作层级的又一次跃升——9月29日华夏基金香港子公司'
 '与富兰克林邓普顿在港交所上市华夏富兰克林港美股票现金流聚焦ETF、华夏富兰克林富时创新药ETF，同步设有港元、美元及人民币交易柜台，'
 '为富兰克林邓普顿首批在亚洲市场挂牌上市的ETF。<br>\n'
 '          <b>行业背景：</b>从年初兴业基金获批设立香港子公司，到头部机构与境外资管巨头从"互挂"走向"联名"，头部公募出海提速明显；'
 '业内认为在中国资产全球配置价值重估与境内ETF市场竞争加剧的双重背景下，"出海"已从头部机构的可选项变为必答题，'
 '联名ETF或将成为中外资管合作的新范式。<br>\n'
 '          <b>对腾安启示：</b>联名ETF与跨境产品线扩容会带来"同一策略、多地份额"的展示难题，货架须按跟踪指数与费率口径横向比较，'
 '并对QDII额度、汇率与交易日历差异作前置提示，避免投资者仅凭产品名称判断底层资产。')

S1_B_BODY = ('上海证券报11月2日报道（记者陈玥）：天相投顾数据显示，截至2026年三季度末，全市场FOF产品共计<b>666只</b>，'
 '环比有所增加，但合计管理规模环比减少<b>83.16亿元</b>；三季度新发FOF募集规模环比减少186.9亿元，降幅为<b>38.38%</b>。'
 '三季度全市场新发FOF共计<b>59只</b>，环比增加17只，增幅40.48%。<br>\n'
 '          <b>配置结构：</b>财通证券研报统计，截至三季度末公募FOF对债券型基金、指数型基金、股票型基金的持有比例'
 '分别为<b>61.13%、22.83%和8.82%</b>，平衡型FOF与偏股型FOF三季度配置债券基金的比重明显上升；'
 '配置数量最多的指数型基金为短融ETF海富通（82只FOF持有），配置规模最大的指数型基金为城投债ETF海富通（合计持有20.93亿元）。<br>\n'
 '          <b>政策空间：</b>证监会近日就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，'
 '降低FOF的成立门槛、允许FOF投资ETF联接基金、将非FOF基金投资其他基金的比例上限从10%提高至30%、'
 '明确基金投资REITs按证券投资进行管理，业内预计公募FOF将从"选基金"发展到"选工具"。<br>\n'
 '          <b>对腾安启示：</b>FOF从"选基金"走向"选工具"，货架展示须把FOF的底层工具构成（债基／ETF／REITs占比）前置，'
 '避免投资者只按业绩曲线理解产品风险。')

S1_C_BODY = ('证券日报网11月2日报道：万得数据显示，截至2026年三季度末，1500余家A股上市公司前十大流通股股东名单中'
 '出现QFII身影，QFII合计持股数量达<b>136.85亿股</b>；以三季度末收盘价核算，QFII持股市值合计达<b>2707.26亿元</b>，'
 '相较于去年三季度末，持股数量与持股市值同比分别增长<b>56.4%</b>与<b>79.87%</b>。<br>\n'
 '          <b>重仓结构：</b>持股市值居前个股依次为宁波银行468.30亿元、生益科技383.40亿元、南京银行272.58亿元、'
 '长鑫科技163.26亿元；半导体行业的长鑫科技是QFII第一大新进重仓个股，高盛国际、法国巴黎银行等现身其前十大流通股股东之列，'
 '另有世纪华通、燧原科技-U、杰瑞股份等479家上市公司获QFII新进重仓。<br>\n'
 '          <b>机构维度：</b>阿布达比投资局、高盛国际、法国巴黎银行、摩根士丹利国际、摩根大通证券等持仓市值均在100亿元以上；'
 '阿布达比投资局持有个股数量由二季度末的65只增至78只，持股市值增至252.79亿元。<br>\n'
 '          <b>对腾安启示：</b>外资持仓向银行等低估值防御资产与科技成长双向布局，跨境产品与外资重仓主题的展示'
 '须区分"防御"与"成长"两条主线，避免把QFII增持简单解读为单一风格信号。')

append_card('Section 1', 'Section 2', card1('p1', 'important', 'P1 重要关注', '11-02',
  '🟡 公募出海提速·华夏基金牵手富兰克林邓普顿·探索联名ETF', S1_A_BODY,
  [('http://jjckb.xinhuanet.com/20261102/fe76b79b19484ef8978d1aabd4b6f982/c.html', '经济参考报·11-02')]))
append_card('Section 1', 'Section 2', card1('p1', 'important', 'P1 重要关注', '11-02',
  '🟡 公募FOF四季度锚定结构性机会·三季度末全市场666只·规模环比减少83.16亿元', S1_B_BODY,
  [('https://www.cnstock.com/commonDetail/821988', '上海证券报·中国证券网·11-02')]))
append_card('Section 1', 'Section 2', card1('p2', 'normal', 'P2 建议了解', '11-02',
  '🔵 QFII三季度末持股市值超2700亿元·持股数量同比增56.4%', S1_C_BODY,
  [('http://www.zqrb.cn/fund/jijindongtai/2026-11-02/A1793554176348.html', '证券日报网·11-02')]))
a, b = seg_bounds('Section 1', 'Section 2')
assert s[a:b].count('<div class="card p') == 5, s[a:b].count('<div class="card p')
counts('S1 append')

# ---------------- 6. S2 删 1 换 1 ----------------
delete_cards_by_tag('Section 2', 'Section 3', ['10-16'])
a, b = seg_bounds('Section 2', 'Section 3')
assert s[a:b].count('<div class="card p') == 3, s[a:b].count('<div class="card p')
counts('S2 delete')

S2_BODY = ('新华财经《新华每日重点信息》11月2日刊载：<b>10月30日</b>，中国证监会党委书记、主席吴清主持召开党委（扩大）会议，'
 '传达贯彻党的二十届五中全会精神。会议要求，证监会系统要认真组织开展宣讲解读、分层分类做好全覆盖培训，'
 '持续在解决突出问题上下功夫；充分发挥全面从严治党的政治引领和政治保障作用，牢固树立大局意识、系统观念，'
 '<b>全力稳市场稳预期</b>，深化投融资综合改革，完善全链条监管体系，持续提升资本市场韧性和信心，'
 '确保"十五五"开局之年资本市场各项任务圆满完成。<br>\n'
 '          <b>同期监管动态：</b>同日重点信息还披露，金融监管总局发布《资产管理信托管理办法》，明确资产管理信托定位为'
 '基于信托法律关系的私募资产管理产品，坚持"卖者尽责、买者自负；卖者失责、依法赔偿"，面向具有风险识别和承受能力的合格投资者'
 '非公开发行且投资者数量不超过<b>200个</b>；要求信托公司对信托产品逐个划分风险等级、向投资者销售与其风险承受能力相匹配的产品，'
 '不得以任何形式承诺保本保收益，并严禁违规通道业务和资金池业务。<br>\n'
 '          <b>对腾安启示：</b>"稳市场稳预期＋完善全链条监管"的组合意味着销售端合规要求继续向信息披露与适当性管理延伸；'
 '资管信托新规与公募产品销售适当性规则方向一致，须统一投资者风险等级划分与产品匹配留痕，避免跨品类标准不一致。')

CUR_SEC = 'S2'
append_card('Section 2', 'Section 3', card1('p1', 'important', 'P1 重要关注', '11-02',
  '🟡 证监会党委扩大会议部署稳市场稳预期·深化投融资综合改革·资管信托管理办法落地', S2_BODY,
  [('https://thinktank.cnfin.com/yxyyj-lb/detail/20261102/4489507_1.html', '新华财经·重点信息·11-02')]))
a, b = seg_bounds('Section 2', 'Section 3')
assert s[a:b].count('<div class="card p') == 4, s[a:b].count('<div class="card p')
counts('S2 append')

# ---------------- 6b. S5 换掉越界卡（周一巡检） ----------------
delete_cards_by_tag('Section 5', 'Section 6', ['10-17'])
a, b = seg_bounds('Section 5', 'Section 6')
assert s[a:b].count('<div class="card p') == 2, s[a:b].count('<div class="card p')
counts('S5 delete')

S5_BODY = ('证券日报网11月2日报道：随着A股三季报披露收官，多家公司在三季报及投资者交流活动中表示，'
 'AI（人工智能）产业快速发展、算力需求旺盛是业绩增长的主要动力。中国电子商务专家服务中心副主任郭涛表示，'
 '年内AI算力产业链迎来景气复苏——需求端，智算中心落地带动服务器、高速互联、存储扩容，拉动印制电路板、光模块、存储零部件订单放量；'
 '供给端，库存出清、产能修复叠加高附加值产品占比提升，共同推动行业向好。<br>\n'
 '          <b>业绩兑现：</b>服务器整机环节，浪潮信息前三季度实现营业收入<b>1293.29亿元</b>、同比增长7.18%，'
 '归属于上市公司股东的净利润<b>39.32亿元</b>、同比增长165.32%；紫光股份前三季度营业收入<b>1021.55亿元</b>、同比增长32.12%，'
 '归母净利润<b>27.73亿元</b>、同比增长97.53%，该公司相关负责人10月29日在投资者关系活动中表示，'
 '全球AI产业需求持续释放，算力供给正从"按卡租赁"转向"按Token（词元）交付"。<br>\n'
 '          <b>机构观点：</b>东吴证券研报显示，国产算力产业侧进展密集，竞争焦点已从"有没有单卡"转向"系统整合能力"，'
 '国产超节点规模化部署刚刚开始，从单柜到万卡集群的技术路线仍在快速迭代；国联民生证券研报称，个人Agent（智能体）'
 '正在成为头部企业布局重点，数据要素与AI产业发展有望形成正反馈。<br>\n'
 '          <b>对腾安启示：</b>AI算力是三季度公募调仓中分歧较大的方向，业绩高增与筹码出清并存；'
 '主题基金展示须同时呈现"业绩兑现度"与"持仓拥挤度"两类信息，避免投资者只凭产业链景气数据线性外推净值表现。')

CUR_SEC = 'S5'
append_card('Section 5', 'Section 6', card1('p1', 'important', 'P1 重要关注', '11-02',
  '🟡 AI算力产业链维持高景气度·三季报净利润大幅增长·机构看好景气延续', S5_BODY,
  [('http://www.zqrb.cn/stock/gupiaoyaowen/2026-11-02/A1793525511694.html', '证券日报网·11-02')]))
a, b = seg_bounds('Section 5', 'Section 6')
assert s[a:b].count('<div class="card p') == 3, s[a:b].count('<div class="card p')
counts('S5 append')

# ---------------- 7. S6 ----------------
S6_TITLE = '📉 A股、港股、美股统一10-30收盘·沪指3599.02 -1.44%｜纳指跌2.86%'
S6_BODY_LEFT = ('''\n            <div>\n'''
 '              <b>A股（10-30收盘）</b><br>\n'
 '              上证指数 <b>3599.02</b> <span style="color:#52c41a;">-1.44%</span>（-52.41点）<br>\n'
 '              深证成指 <b>10833.78</b> <span style="color:#52c41a;">-2.73%</span><br>\n'
 '              创业板指 <b>2413.63</b> <span style="color:#52c41a;">-4.13%</span><br>\n'
 '              科创综指 <b>1421.31</b> <span style="color:#52c41a;">-4.66%</span><br>\n'
 '              沪深两市成交 <b>16744.63亿元</b>（沪市7642.27亿＋深市9102.36亿）<br>\n'
 '              较上一交易日放量约1179亿元\n'
 '            </div>\n')
S6_BODY_RIGHT = ('''            <div>\n'''
 '              <b>港股（10-30收盘）与美股（美东10-30收盘）</b><br>\n'
 '              恒生指数 <b>23294.42</b> <span style="color:#e03131;">+1.46%</span>（+335.77点）<br>\n'
 '              国企指数 <b>7862.22</b> <span style="color:#e03131;">+1.37%</span>（+106.56点）<br>\n'
 '              恒生科技 <b>3754.90</b> <span style="color:#e03131;">+0.29%</span>（+10.76点）<br>\n'
 '              道琼斯 <b>51770.31</b> <span style="color:#52c41a;">-1.09%</span>（-572.25点）<br>\n'
 '              纳斯达克 <b>25437.00</b> <span style="color:#52c41a;">-2.86%</span>（-747.73点）<br>\n'
 '              标普500 <b>7580.07</b> <span style="color:#52c41a;">-1.82%</span>（-140.32点）<br>\n'
 '              港股主板成交 <b>2143.18亿港元</b><br>\n'
 '              纽约12月交货原油 <b>104.12美元/桶</b> <span style="color:#e03131;">+2.08%</span><br>\n'
 '              伦敦12月交货布伦特 <b>117.64美元/桶</b> <span style="color:#e03131;">+2.4%</span><br>\n'
 '              COMEX12月黄金 <b>3898.9美元/盎司</b> <span style="color:#52c41a;">-3.29%</span><br>\n'
 '              COMEX12月白银 <b>49.276美元/盎司</b> <span style="color:#52c41a;">-5.93%</span>\n'
 '            </div>\n')

S6_KJ = ('<b>取数口径：</b>A股取<b>10月30日收盘</b>（10月30日为10月最后一个交易日且已收盘）：上证指数报3599.02点、跌幅1.44%，'
 '深证成指报10833.78点、跌幅2.73%，创业板指报2413.63点、跌幅4.13%，科创综指报1421.31点、跌幅4.66%、成交2358亿元，'
 '四项同出新华财经10月30日收评（记者胡晨曦）；分市场成交额出自中国经济网10月30日收评——沪市7642.27亿元、深市9102.36亿元，'
 '合计沪深两市16744.63亿元，较上一交易日增加约1179亿元。另按深圳商报·读创财经10月30日口径，沪深北三市全市场成交额为16877亿元、'
 '放量1170亿元，与沪深两市口径统计范围不同，本期并列列出、不与其他口径混用；'
 '北证50与科创50未取得同源可交叉验证的收盘点位，本期不予列示。<br>\n'
 '              <b>港股与美股：</b>港股取<b>10月30日收盘</b>（新华社香港10月30日电）：恒生指数涨335.77点、涨幅1.46%，收报23294.42点，'
 '全日主板成交2143.18亿港元；国企指数涨106.56点、涨幅1.37%，收报7862.22点；恒生科技指数涨10.76点、涨幅0.29%，收报3754.90点；'
 '中国新闻网同日报道港股三大指数同步收涨，恒指全周累计上涨约201点、涨幅0.87%，结束此前连续两周的下跌走势。'
 '美股取<b>美东10月30日收盘</b>（新华社纽约10月30日电、央视新闻）：道琼斯工业平均指数跌572.25点、跌幅1.09%，收于51770.31点；'
 '标准普尔500种股票指数跌140.32点、跌幅1.82%，收于7580.07点；纳斯达克综合指数跌747.73点、跌幅2.86%，收于25437.00点，'
 '为6月以来最大单日跌幅、10月累计下跌5.3%；标普500十一大板块六涨五跌，能源板块和必需消费品板块分别以1.91%和1.38%的涨幅领涨，'
 '科技板块和工业板块分别以4.24%和1.57%的跌幅领跌。<br>\n'
 '              <b>商品与贵金属：</b>国际原油取<b>10月30日收盘</b>（央视新闻、央视财经）：纽约商品交易所12月交货轻质原油期货价格上涨2.12美元，'
 '收于每桶104.12美元，涨幅2.08%；12月交货伦敦布伦特原油期货价格上涨2.76美元，收于每桶117.64美元，涨幅2.4%，布伦特油价创六个月来新高。'
 '贵金属取<b>10月30日收盘</b>（央视财经，经澎湃新闻转载）：12月交割黄金期货价格下跌132.5美元，收于每盎司3898.9美元，跌幅3.29%；'
 '12月交割白银期货价格下跌3.104美元，收于每盎司49.276美元，跌幅5.93%，为2025年11月以来首次跌破每盎司50美元关口；'
 '另有新华财经口径为12月黄金期价收于每盎司3884.28美元、跌幅3.65%，12月白银期价收于49.12美元、跌幅6.23%，'
 '两套口径数值略有差异，本期统一采用央视财经／央视新闻口径、不混用。<br>\n'
 '              <b>A股（10-30）：</b>三大指数早盘大幅低开，沪指盘初失守3600点后回暖，午后一度集体翻红后再度回落，'
 '最终收于3600点下方，为本轮调整以来首次收在3600点下方；深证成指与创业板指双双创下今年6月下旬调整以来新低，创业板指10月累计跌超23%。'
 '盘面上白酒、医疗服务、CRO、港口航运、银行板块涨幅居前，影视院线、游戏、文化传媒、半导体板块跌幅居前，全市场超4600只个股下跌。<br>\n'
 '              <b>美股（美东10-30）：</b>字母表、英特尔、亚马逊等科技巨头三季度业绩弱于市场预期，引发市场对科技股估值过高'
 '与AI资本开支回报的担忧；霍尔木兹海峡商船遇袭推升油价、巩固通胀预期，市场对美联储12月重启紧缩的预期升温，'
 '纳指与本月创下的历史高点相比下跌近8%。')

S6_LINKS = [
 ('https://m.cnfin.com/yw-lb/zixun/20261030/4488837_1.html', '新华财经·A股收评·10-30'),
 ('https://finance.ce.cn/stock/gsgdbd/202610/t20261030_3277176.shtml', '中国经济网·A股收评·10-30'),
 ('https://news.qq.com/rain/a/20261030A09DF900', '腾讯新闻·读创财经·10-30'),
 ('https://app.xinhuanet.com/news/article.html?articleId=202610301f1b126658e14f8fb70710340394d8ec', '新华社·港股·10-30'),
 ('https://m.chinanews.com/wap/detail/cht/zw/10723632.shtml', '中国新闻网·港股·10-30'),
 ('https://ysxw.cctv.cn/article.html?item_id=1014509750509744495', '央视新闻·美股·10-30'),
 ('https://www.thepaper.cn/newsDetail_forward_34379007', '澎湃新闻·央视财经·原油贵金属·10-31'),
]

s6c = '                                <div class="card p3">\n'
s6c += '        <div class="card-top">\n'
s6c += '          <div class="card-title">%s</div>\n' % S6_TITLE
s6c += '          <div class="card-meta">\n'
s6c += '            <span class="priority-tag fyi">P3 知悉即可</span>\n'
s6c += '            <span class="date-tag">10-30</span>\n'
s6c += '          </div>\n        </div>\n'
s6c += '        <div class="card-body">\n'
s6c += '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">\n'
s6c += S6_BODY_LEFT + S6_BODY_RIGHT
s6c += '            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">\n'
s6c += '              ' + S6_KJ + '\n'
s6c += '            </div>\n'
s6c += '          </div>\n        </div>\n'
s6c += '        <div class="card-footer">\n'
for u, t in S6_LINKS:
    s6c += ('          <a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;">'
            '<span class="source-tag">%s</span></a>\n' % (u, t))
s6c += '          <span class="impact-tag medium">辅助决策</span>\n        </div>\n      </div>'

a6 = s.find('Section 6')
cs6 = s.find('<div class="card p3">', a6)
assert cs6 > 0
ANCHOR_S6 = '      </div>  </div>\n\n<!-- ============ Section 7'
e6 = s.find(ANCHOR_S6, cs6)
assert e6 > cs6
s = s[:cs6] + s6c + s[e6 + len('      </div>'):]
counts('S6')

# ---------------- 8. S7 ----------------
ITEMS = [
 ('red',   '2026-11-02', '15只主动ETF顶格完成募集'),
 ('blue',  '2026-11-02', '公募加大医药板块布局力度'),
 ('blue',  '2026-11-02', '中小公募寻求差异化突围'),
 ('blue',  '2026-11-02', '10月宽基ETF吸金超2686亿'),
 ('red',   '2026-10-31', '美股三大指数显著下跌'),
 ('red',   '2026-10-31', '国际金价跌至一年新低'),
 ('red',   '2026-10-30', '沪指失守3600点10月收官'),
 ('blue',  '2026-10-30', '港股恒指涨1.46%结束连跌'),
 ('blue',  '2026-10-30', '百亿私募收警示函存违规'),
 ('blue',  '2026-10-29', '宽基ETF单日吸金171亿元'),
 ('blue',  '2026-10-28', '公募平均仓位降至78.32%'),
 ('blue',  '2026-10-26', '运作办法征求意见稿发布'),
]
def titem(color, d, t):
    return ('<div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>' % (color, d, t))
new_items = '\n      '.join(titem(*x) for x in ITEMS)

a7 = s.find('Section 7')
first = s.find('<div class="timeline-item">', a7)
assert first > 0
old_n = s[first:].count('<div class="timeline-item">')
print('S7 old items =', old_n)
last = s.rfind('<div class="timeline-item">')
te = s.find('      </div>\n\n    </div>', last)
assert te > last
s = s[:first] + new_items + s[te + len('      </div>'):]
assert s.count('<div class="timeline-item">') == len(ITEMS)
counts('S7')

# ---------------- 9. 自审 ----------------
o, c = s.count('<div'), s.count('</div>')
assert o == c, (o, c)
print('FINAL open=%d close=%d (expect 237)' % (o, c))
assert o == 237, o
print('OK 237')
assert s.count('</div>>') == 0
assert '�' not in s
assert 'Section 8' not in s and s.count('待办跟踪') == 0
assert s.count('class="action-box"') == 1

# S0 六项
seg0 = s[s.find('Section 0'):s.find('Section 1')]
assert seg0.count('<div class="card p') == 4
assert seg0.count('date-tag">11-02<') == 4
assert seg0.count('action-box') == 1
assert re.search(r'section-title">今日焦点<', seg0)
assert re.search(r'section-context">11月2日 · 4条今日要闻<', seg0)
n_link = seg0.count('target="_blank"')
print('S0 links =', n_link)
assert n_link >= 4

# date-tag 越界
t14 = TODAY - timedelta(days=14)
bad = []
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s):
    d = date(2026, int(m.group(1)), int(m.group(2)))
    if d < t14:
        bad.append(m.group(0))
print('date-tag out of window:', bad)
assert not bad

# 黑名单自检
BL = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com', 'toutiao',
      'so.html5.qq.com', '163.com/dy', 'dy.163.com', 'k.sina.com.cn', 'mp.weixin.qq.com',
      'weibo.com', 'q.fund.sohu.com', 'futunn.com', 'jiantou8.com', 'cofool.com',
      'yanglee.com', 'topnews.cn', 'cqcb.com']
hits = [b for b in BL if b in s]
print('blacklist hits:', hits)
assert not hits

# S7 标题长度
for m in re.finditer(r'<div class="timeline-title">([^<]*)</div>', s):
    assert len(m.group(1)) <= 25, m.group(1)
assert 'timeline-desc' not in s

# S1/S2 数量
seg1 = s[s.find('Section 1'):s.find('Section 2')]
seg2 = s[s.find('Section 2'):s.find('Section 3')]
print('S1 cards=%d S2 cards=%d S7 items=%d' % (
    seg1.count('<div class="card p'), seg2.count('<div class="card p'),
    s.count('<div class="timeline-item">')))
assert seg1.count('<div class="card p') == 5
assert seg2.count('<div class="card p') == 4

# 注释数 == 卡数
for name, segx in (('S1', seg1), ('S2', seg2)):
    cn = len(re.findall(r'<!-- S[12] Card', segx))
    kn = segx.count('<div class="card p')
    print('%s comments=%d cards=%d' % (name, cn, kn))
    assert cn == kn, (name, cn, kn)

# 深度法
def depth_check(name, a, b):
    segx = s[a:b]
    ds = set()
    for m in re.finditer(r'<div class="card p\d">', segx):
        d = 0
        i = 0
        while i < m.start():
            if segx.startswith('<div', i):
                d += 1; i += 4
            elif segx.startswith('</div>', i):
                d -= 1; i += 6
            else:
                i += 1
        ds.add(d)
    print('%s card-start depths = %s' % (name, sorted(ds)))
    assert len(ds) == 1, (name, ds)
for nm, x, y in (('S0', 'Section 0', 'Section 1'), ('S1', 'Section 1', 'Section 2'),
                 ('S2', 'Section 2', 'Section 3'), ('S4', 'Section 4', 'Section 5'),
                 ('S5', 'Section 5', 'Section 6'), ('S6', 'Section 6', 'Section 7')):
    depth_check(nm, s.find(x), s.find(y))

# 全文件 mm-dd 越界（含 S3 td / 注释）
allb = []
for mo, dd in re.findall(r'(\d{2})-(\d{2})', s):
    if 1 <= int(mo) <= 12 and 1 <= int(dd) <= 31:
        d = date(2026, int(mo), int(dd))
        if d < t14:
            allb.append('%s-%s' % (mo, dd))
print('all mm-dd out of window:', sorted(set(allb)))

print('ALL ASSERT PASSED')
data = s.encode('utf-8')
io.open(P, 'wb').write(data)
print('WROTE %d bytes' % len(data))
