# -*- coding: utf-8 -*-
import re, sys, hashlib
from datetime import date, timedelta

LOG = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\_update_1029_out.txt'
sys.stdout = open(LOG, 'w', encoding='utf-8')

P = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
orig = open(P, encoding='utf-8').read()
s = orig

TODAY = date(2026, 10, 29)
CUT = TODAY - timedelta(days=14)
print('TODAY', TODAY, 'CUTOFF', CUT)

def cnt(t, pat):
    return len(re.findall(pat, t))

def op(t): return cnt(t, r'<div\b')
def cl(t): return cnt(t, r'</div>')

BASE_O, BASE_C = op(s), cl(s)
print('BASE open/close', BASE_O, BASE_C)

# ---------------- STEP 1: marker / fingerprint / description ----------------
s_new = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
               '<!-- daily-update: %s -->' % TODAY.isoformat(), s, count=1)
assert s_new != s and s_new.count('<!-- daily-update: 2026-10-29 -->') == 1
s = s_new
print('STEP1 marker ok')

FP = '三季度新|主动权益|香港证监|摩根大盘'
s_new = re.sub(r'(<meta name="content-fingerprint" content=")[^"]*(")',
               r'\g<1>' + FP + r'\g<2>', s, count=1)
assert s_new.count('content="%s"' % FP) == 1
s = s_new
print('STEP1 fingerprint ok', FP)

DESC = ('三季度新进重仓股曝光|主动权益基金高仓位守主线|香港证监会零售基金指引|'
        '摩根大盘成长主动ETF成立|沪指10月28日收3681.47点涨0.91%·创业板指涨3.40%·美股三大指数齐涨')
s_new = re.sub(r'(<meta name="description" content=")[^"]*(")',
               r'\g<1>' + DESC + r'\g<2>', s, count=1)
assert s_new.count('content="%s"' % DESC) == 1
s = s_new
print('STEP1 description ok')

# ---------------- STEP 2: header data range badge ----------------
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
badge_new = '📅 数据区间：%s — %s（每日更新）' % (lower, upper)
s_new, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
                   badge_new, s, count=1)
assert n == 1, 'badge not replaced'
s = s_new
print('STEP2 badge ->', badge_new)

# ---------------- STEP 3: Stats Bar ----------------
STATS_START = '<!-- Stats Bar -->'
STATS_END = '\n\n  </div>\n\n<div class="main">'
i = s.find(STATS_START); j = s.find(STATS_END, i)
assert i > 0 and j > i
assert s.count(STATS_START) == 1 and s.count(STATS_END) == 1
old_stats = s[i:j]
print('STEP3 old stats open/close', op(old_stats), cl(old_stats))
assert old_stats.count('class="stat-card"') == 4

def stat(num, label, change, up=True):
    return ('    <div class="stat-card">\n'
            '      <div class="stat-number">%s</div>\n'
            '      <div class="stat-label">%s</div>\n'
            '      <div class="stat-change %s">%s</div>\n'
            '    </div>\n' % (num, label, 'up' if up else 'down', change))

new_stats = ('<!-- Stats Bar -->\n\n    <div class="stats-bar">\n'
             + stat('89.555%', '摩根大盘成长主动ETF认购确认比例·有效认购15256户·10月28日成立',
                    '▲ 首日触达20亿元上限·股东自购7500万美元')
             + stat('3681.47', '沪指10-28收盘·涨0.91%·沪深两市成交约1.63万亿元',
                    '▲ 深证成指涨2.02%·创业板指涨3.40%')
             + stat('428.52亿元', '长鑫科技获959只基金重仓·三季度新进重仓股首位',
                    '▲ 占流通股17.88%·前50大新进重仓股合计约525亿元')
             + stat('1989.15亿元', '全市场81只红利类ETF合计规模·较去年同期增长24.75%',
                    '▲ 10月以来9只红利相关基金启动募集')
             )
print('STEP3 new stats open/close', op(new_stats), cl(new_stats))
assert op(new_stats) == op(old_stats) and cl(new_stats) == cl(old_stats)
s = s[:i] + new_stats + s[j:]
print('STEP3 stats replaced; open/close now', op(s), cl(s))

# ---------------- STEP 4: S0 ----------------
S0_START = '<!-- ============ Section 0'
S0_END = '<!-- ============ Section 1'
i = s.find(S0_START); j = s.find(S0_END, i)
assert i > 0 and j > i and s.count(S0_START) == 1 and s.count(S0_END) == 1
old_s0 = s[i:j]
print('STEP4 old S0 open/close', op(old_s0), cl(old_s0))
print('STEP4 old S0 tail', repr(old_s0[-40:]))

def card0(cls, pcls, pname, date_tag, emoji, title, body_html, links, impact):
    a = ''
    for href, txt in links:
        a += ('\n          <a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;">'
              '<span class="source-tag">%s</span></a>\n' % (href, txt))
    return ('      <div class="card %s">\n'
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
            '      </div>\n' % (cls, emoji, title, pcls, pname, date_tag, body_html, a, impact[0], impact[1]))

C1 = ('新华财经上海10月29日电（记者赵明超）：最新披露的公募基金三季报显示，新进重仓股明显向投资品、医药和信息技术等板块集中，科技含量显著提升。'
      '天相投顾数据显示，截至2026年三季度末，在基金新进前50大重仓股中，主要集中在科技和医药领域——科技方面包括MLCC龙头三环集团、PCB龙头景旺电子和芯碁微装、'
      '电子龙头立讯精密、模拟芯片龙头圣邦股份等；医药方面包括健友股份、科源制药、康泰生物、瑞普生物、义翘神州和海尔生物。<br>\n'
      '          <b>新股被竞相买入：</b>7月27日上市的存储龙头<b>长鑫科技</b>，截至三季度末被<b>959只</b>基金重仓持有，持仓市值高达<b>428.52亿元</b>，'
      '基金持仓占流通股比例高达<b>17.88%</b>；8月25日上市的半导体材料龙头高凯技术被<b>19只</b>基金重仓买入，持仓市值4.39亿元。'
      '前50大新进重仓股中还有<b>15家</b>港股上市公司，包括大模型公司MINIMAX-W、AI应用概念股阅文集团、计算机设备龙头联想控股，'
      '以及立讯精密、景旺电子、中际旭创、圣邦股份的H股。<br>\n'
      '          <b>合计规模：</b>截至三季度末，基金新进前50大重仓股合计持仓市值约<b>525亿元</b>，其中长鑫科技一只便达428.52亿元；'
      '基金持有中际旭创H股市值合计21.12亿元，持有光洋股份、高凯技术市值均超4亿元。从买入逻辑看，公募基金主要围绕两条主线布局——'
      '产业趋势向好、行业景气度高的细分方向，以及质地较好、业绩向好的公司股票。<br>\n'
      '          <b>对腾安启示：</b>新进重仓股名单是基金经理当季调仓的结果而非荐股清单，且新股上市初期被集中买入往往伴随流通盘小、波动大的特征；'
      '涉及"基金重仓""基金抱团"类内容的展示须标明数据截止日与统计口径（天相投顾、前50大新进重仓股），不得把"被多少只基金持有"演绎为上涨预期或安全保证。')

C2 = ('证券日报10月29日报道（记者吴珊、昌校宇，新华财经转载）：2026年公募基金三季报披露收官。截至三季度末，今年以来共有<b>2435只</b>主动权益基金'
      '（仅统计主代码）实现净值增长，占全市场主动权益基金的<b>49%</b>，其中<b>121只</b>产品期间净值增长率超50%。天相投顾数据显示，'
      '仓位上主动权益基金股票仓位整体保持在<b>72%以上</b>；按申万一级行业划分，重仓前十行业合计持仓占比<b>86.31%</b>，'
      '电子、通信、医药生物为前三大重仓行业，持仓比例分别为<b>36.48%</b>、<b>15.21%</b>、<b>9.46%</b>。<br>\n'
      '          <b>高仓位样本：</b>易方达供给改革混合今年以来回报率达<b>115.67%</b>，三季度回撤幅度9.42%，同期股票仓位维持在80%以上，'
      '前十大重仓股合计占基金资产净值<b>52.23%</b>；融通通鑫灵活配置混合前三季度回报率超50%，股票市值占基金资产净值比例从二季度末的84.72%增至<b>93.67%</b>，'
      '前十大重仓股重点布局半导体全产业链。<br>\n'
      '          <b>基金经理观点：</b>易方达杨宗昌表示继续看好人工智能产业发展前景，也会加大力度研究传统行业优质公司，短期逆风可能带来好的价格和买入时机；'
      '申万菱信卜忠林结构上看好受益于算力通胀逻辑的后道测试等环节、光通信产业链中供需格局良好的模拟芯片，以及技术升级趋势明朗的NPO（近封装光学）等细分环节的优质个股；'
      '融通王迪认为把观察周期拉长，决定股价走向的核心变量将不断收敛，更多聚焦于企业自身的经营质量与成长能力。<br>\n'
      '          <b>口径提示：</b>本卡"主动权益基金股票仓位72%以上"为天相投顾口径、统计对象为主动权益基金（普通股票型、偏股混合型、平衡混合型、灵活配置型）；'
      '10月28日已披露的"全部可比基金平均仓位78.32%"统计对象为全部可比基金，两者口径不同、不可直接比较。<br>\n'
      '          <b>对腾安启示：</b>高仓位与高行业集中度是同一枚硬币的两面——电子单一行业持仓已超36%，产品页须把行业集中度与业绩比较基准偏离做成常驻字段，'
      '并在科技主题产品上同步展示回撤与波动区间，不得以"基金经理长期看好"替代风险提示。')

C3 = ('中国基金报报道（记者叶诗婕）：10月28日，香港证券及期货事务监察委员会发布指引，协助基金业界为实施经修订的《单位信托及互惠基金守则》'
      '（下称《单位信托守则》）做好准备，经修订的《单位信托守则》将于<b>2026年11月1日</b>生效。香港证监会表示，经修订守则与国际标准接轨、加强投资者保障，'
      '有助于确保香港的零售基金制度保持稳健及与时并进。<br>\n'
      '          <b>主要变更：</b>就管理基金的衍生工具风险承担采用风险价值（VaR）计算法、流动性风险管理，以及加强适用于货币市场基金的投资及披露规定；'
      '指引包含多份通函，涵盖新基金认可申请、衍生工具的使用，以及《单位信托守则》对UCITS（可转让证券集体投资计划）基金的适用范围。<br>\n'
      '          <b>过渡安排：</b>香港证监会就现有基金及新基金的实施和过渡安排发出具体指引，包括为期<b>12个月</b>的过渡期与过渡安排、'
      'VaR计算法的计算方法及准则、流动性风险管理补充通函、认可货币市场基金可投资的合资格优质货币市场工具的最低信贷质素标准，'
      '以及适用于提供固定资产净值的货币市场基金的经加强产品资料概要披露规定；此外还就备兑认购期权策略、投资于杠杆及反向产品与虚拟资产交易所买卖产品的'
      '证监会认可基金的投资限制、代币化产品的进阶代币化功能等提供指引。<br>\n'
      '          <b>监管表态：</b>香港证监会投资产品部执行董事吴家俐表示，这些指引列明本会在经修订守则下设定的监管要求，并进一步厘清若干关乎认可基金的现行做法，'
      '以支援业界落实并遵守经优化的香港零售基金制度，维持香港作为卓越的资产及财富管理中心的竞争力。<br>\n'
      '          <b>对腾安启示：</b>涉及香港互认基金、港股通ETF及跨境产品的内容，须在11月1日生效节点前后同步更新产品资料概要中的产品分类与流动性风险管理工具披露；'
      'VaR计算法取代原有方式衡量衍生工具风险承担，意味着相关产品的风险等级标注口径可能变化，不得以旧口径继续对客解释。')

C4 = ('上海证券报·中国证券网10月28日报道（记者赵明超）：10月28日，摩根基金发布公告，旗下摩根大盘成长主动股票ETF（证券代码<b>581000</b>）正式成立。'
      '该基金有效认购户数达<b>15256户</b>，发行首日即触达<b>20亿元</b>募集规模上限，募集期内有效认购申请确认比例结果为<b>89.555%</b>；'
      '据记者了解，基金管理人将于近期启动建仓。<br>\n'
      '          <b>两个"唯一"：</b>在首批获批的18只主动ETF中，该产品是唯一来自外资公募的主动ETF，也是唯一以成长指数作为业绩比较基准的产品；'
      '由摩根基金"双十"基金经理<b>李博</b>掌舵——Wind数据显示，截至9月30日，李博自2014年12月开始管理摩根核心成长股票基金A已逾十年、年化回报超10%，'
      '其将长期践行的GARP策略装入ETF载体，产品每日公开披露持仓，个股布局、行业配置、仓位比例清晰可查。<br>\n'
      '          <b>股东自购：</b>发行前夕摩根基金率先披露，公司股东将通过关联方摩根资产管理（亚太）有限公司以<b>7500万美元</b>（约合5亿元人民币）'
      '自有资金投资公司首只主动ETF，相关投资将在基金上市后开展。摩根资产管理中国CEO王琼慧表示，希望将成熟的全球主动ETF实践经验引入中国市场，'
      '并结合本土主动权益投研能力，为境内外投资者提供透明、专业、具备差异化特征的主动管理产品选择。<br>\n'
      '          <b>建仓节奏：</b>据经济参考网、证券日报网10月28日报道，首日结募的两家基金管理人将于<b>10月29日</b>开始建仓；截至10月27日，'
      '沪市9只产品中的7只已募满20亿元、合计募集资金163.3亿元，6家沪市管理人通过自有资金或股东相关方资金自购合计21亿元，'
      '首批产品成立后预计为市场带来增量资金超<b>350亿元</b>。<br>\n'
      '          <b>对腾安启示：</b>主动ETF进入建仓与上市阶段后，货架须补齐"每日披露持仓（PCF）""不跟踪特定指数、由基金经理自主选股与择时"'
      '"比例配售导致部分认购资金退回"三项说明；产品页不得用股东自购金额或认购户数暗示收益保障，也不得与宽基ETF混排比较。')

new_s0 = ('<!-- ============ Section 0: 今日焦点 ============ -->\n\n'
          '  <div class="section">\n\n'
          '    <div class="section-header">\n\n'
          '      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>\n\n'
          '      <div class="section-title-group">\n\n'
          '        <span class="section-title">今日焦点</span>\n\n'
          '        <span class="section-context">10月29日 · 4条今日要闻</span>\n\n'
          '      </div>\n\n'
          '      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>\n\n'
          '    </div>\n\n\n\n'
          '    <div class="card-grid">\n\n'
          + '            <!-- S0 Card 1 (10-29 P1) -->\n'
          + card0('p1', 'important', 'P1 重要关注', '10-29', '🟡',
                  '三季度新进重仓股曝光·长鑫科技被959只基金重仓428.52亿元·占流通股17.88%', C1,
                  [('https://m.cnfin.com/gs-lb//zixun/20261029/4487920_1.html', '新华财经·10-29')],
                  ('medium', '影响：中'))
          + '\n      <!-- S0 Card 2 (10-29 P1) -->\n'
          + card0('p1', 'important', 'P1 重要关注', '10-29', '🟡',
                  '主动权益基金三季度高仓位守主线·电子持仓36.48%居首·前十行业合计86.31%', C2,
                  [('https://m.cnfin.com/yw-lb//zixun/20261029/4487913_1.html', '新华财经·证券日报·10-29')],
                  ('medium', '影响：中'))
          + '\n      <!-- S0 Card 3 (10-28 P1) -->\n'
          + card0('p1', 'important', 'P1 重要关注', '10-28', '🟡',
                  '香港证监会发布实施指引·经修订《单位信托守则》11月1日生效·引入VaR计算法', C3,
                  [('https://new.qq.com/rain/a/20261028A0DSI900', '腾讯新闻·中国基金报·10-28')],
                  ('medium', '影响：中'))
          + '\n      <!-- S0 Card 4 (10-28 P1) -->\n'
          + card0('p1', 'important', 'P1 重要关注', '10-28', '🟡',
                  '摩根大盘成长主动股票ETF率先成立·有效认购15256户·确认比例89.555%', C4,
                  [('https://www.cnstock.com/commonDetail/817264', '上海证券报·中国证券网·10-28'),
                   ('https://www.jjckb.cn/20261028/a7f6205022fc4da58888db7646923b7a/c.html', '经济参考网·10-28')],
                  ('medium', '影响：中'))
          + '\n    </div>\n\n  </div>\n\n\n\n')

print('STEP4 new S0 open/close', op(new_s0), cl(new_s0))
assert op(new_s0) == op(old_s0) and cl(new_s0) == cl(old_s0), 'S0 div mismatch'
s = s[:i] + new_s0 + s[j:]
print('STEP4 S0 replaced; open/close now', op(s), cl(s))

# ---- STEP 4b: assert S0 header exact ----
k = s.find(S0_START); k2 = s.find(S0_END, k)
seg = s[k:k2]
assert seg.count('<span class="section-title">今日焦点</span>') == 1
assert seg.count('<span class="section-context">10月29日 · 4条今日要闻</span>') == 1
assert seg.count('<div class="card p') == 4, seg.count('<div class="card p')
assert seg.count('class="action-box"') == 0
assert seg.count('<span class="priority-tag urgent">') == 0
print('STEP4b S0 header/cards verified: cards=4, action-box=0')

# ---------------- STEP 5: S6 ----------------
S6_START = '<!-- ============ Section 6'
S6_END = '      </div>  </div>\n\n<!-- ============ Section 7'
i = s.find(S6_START); j = s.find(S6_END, i)
assert i > 0 and j > i and s.count(S6_START) == 1 and s.count(S6_END) == 1
old_s6 = s[i:j]
print('STEP5 old S6 open/close', op(old_s6), cl(old_s6))

new_s6 = ('<!-- ============ Section 6: 市场行情速览 ============ -->\n\n'
 '  <div class="section">\n\n'
 '    <div class="section-header">\n\n'
 '      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>\n\n'
 '      <span class="section-title">市场行情速览</span>\n\n'
 '      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>\n\n'
 '    </div>\n\n\n\n'
 '                                <div class="card p3">\n'
 '        <div class="card-top">\n'
 '          <div class="card-title">📈 A股、港股、美股统一10-28收盘·沪指3681.47 +0.91%｜创业板指涨3.40%</div>\n'
 '          <div class="card-meta">\n'
 '            <span class="priority-tag fyi">P3 知悉即可</span>\n'
 '            <span class="date-tag">10-28</span>\n'
 '          </div>\n'
 '        </div>\n'
 '        <div class="card-body">\n'
 '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">\n'
 '            <div>\n'
 '              <b>A股（10-28收盘）</b><br>\n'
 '              上证指数 <b>3681.47</b> <span style="color:#dc2626;">+0.91%</span><br>\n'
 '              深证成指 <b>11473.18</b> <span style="color:#dc2626;">+2.02%</span><br>\n'
 '              创业板指 <b>2634.76</b> <span style="color:#dc2626;">+3.40%</span><br>\n'
 '              科创综指 <b>1560.38</b> <span style="color:#dc2626;">+3.20%</span><br>\n'
 '              北证50指数 <span style="color:#dc2626;">+1.63%</span><br>\n'
 '              沪深两市成交 <b>16285亿元</b>（约1.63万亿元），较上一交易日放量约1675亿元\n'
 '            </div>\n'
 '            <div>\n'
 '              <b>港股（10-28收盘）与美股（美东10-28收盘）</b><br>\n'
 '              恒生指数 <b>23094.83</b> <span style="color:#dc2626;">+0.23%</span>（+53.51点）<br>\n'
 '              国企指数 <b>7791.63</b> <span style="color:#dc2626;">+0.32%</span>（+24.72点）<br>\n'
 '              恒生科技 <b>3853.72</b> <span style="color:#dc2626;">+1.4%</span>（+53.29点）<br>\n'
 '              道琼斯 <b>52475.10</b> <span style="color:#dc2626;">+0.19%</span>（+97.53点）<br>\n'
 '              纳斯达克 <b>26549.85</b> <span style="color:#dc2626;">+0.27%</span>（+72.04点）<br>\n'
 '              标普500 <b>7743.98</b> <span style="color:#dc2626;">+0.28%</span>（+21.38点）<br>\n'
 '              港股主板成交 <b>1814.28亿港元</b><br>\n'
 '              纽约12月交货原油 <b>102.78美元/桶</b> <span style="color:#dc2626;">+2.88%</span><br>\n'
 '              伦敦12月交货布伦特 <b>115.32美元/桶</b> <span style="color:#dc2626;">+1.26%</span><br>\n'
 '              COMEX12月黄金 <b>4081.2美元/盎司</b> <span style="color:#dc2626;">+0.16%</span><br>\n'
 '              COMEX12月白银 <b>54.040美元/盎司</b> <span style="color:#52c41a;">-0.87%</span>\n'
 '            </div>\n'
 '            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">\n'
 '              <b>取数口径：</b>A股取<b>10月28日收盘</b>（10月28日为交易日且已收盘）：上证指数3681.47点、涨0.91%，深证成指11473.18点、涨2.02%，'
 '创业板指2634.76点、涨3.40%，科创综指1560.38点、涨3.20%，北证50指数涨1.63%，五项涨跌幅同出中国经济网10月29日《资金情绪回暖 科技股带动A股市场放量反弹》一篇；'
 '上海证券报电子版10月29日《昨日A股两创指数齐涨超过3% 多重利好共振 AI产业链集体反弹》载沪深两市合计成交<b>16285亿元</b>、较前一日放量1675亿元，'
 '中国经济网同日口径为1.64万亿元、较前一交易日增加1692亿元，两者同为沪深两市口径但数值略有差异，本期仅并列列出、不与沪深北三市等其他口径混用。'
 '港股取<b>10月28日收盘</b>（新华社香港10月28日电，中证网转载）：恒生指数涨53.51点收报23094.83点，国企指数涨24.72点收报7791.63点，'
 '恒生科技指数涨53.29点收报3853.72点，全日主板成交1814.28亿港元。美股取<b>美东10月28日收盘</b>（新华财经纽约10月28日电，记者刘亚南）：'
 '道琼斯工业平均指数涨97.53点收于52475.10点、标准普尔500种股票指数涨21.38点收于7743.98点、纳斯达克综合指数涨72.04点收于26549.85点，'
 '标普500指数十一大板块八涨三跌，科技板块和能源板块分别以0.48%和0.41%的涨幅领涨，公用事业板块和房地产板块分别以0.88%和0.65%的跌幅领跌；'
 '美国联邦储备委员会28日结束为期两天的货币政策会议，宣布将联邦基金利率目标区间维持在<b>3.75%至4%</b>不变，联邦公开市场委员会以<b>10:2</b>的投票结果作出该决定，'
 '美联储理事莉萨·库克与克利夫兰联储银行行长贝丝·哈马克在投票中主张继续加息25个基点，主席沃什在记者会上宣布从2027年到2028年将逐渐减少货币政策会议的议息频次。'
 '国际原油取<b>10月28日收盘</b>（中国基金报10月29日电，与新华社纽约10月28日电口径一致）：纽约商品交易所12月交货轻质原油期货收于每桶102.78美元、上涨2.88美元、涨幅2.88%，'
 '12月交货伦敦布伦特原油期货收于每桶115.32美元、上涨1.44美元、涨幅1.26%。贵金属取<b>10月28日收盘</b>（新华财经纽约10月28日电，记者徐静）：'
 '12月交割黄金期价上涨6.6美元、收于每盎司4081.2美元、涨幅0.16%，12月交割白银期货下跌47.3美分、收于每盎司54.040美元、跌幅0.87%；'
 '另有央视财经口径为12月黄金期价报每盎司4051.60美元、跌幅0.56%，12月白银期价报每盎司53.666美元、跌幅1.55%，两套口径涨跌幅方向相反，'
 '本期统一采用新华财经口径、不与其他来源混用。<br>\n'
 '              <b>A股（10-28）：</b>三大指数高开高走、全天放量反弹，上证报称盘面呈现普涨格局，AI产业链上下游集体升温带动双创指数全天领涨，'
 '创新药、商业航天等成长板块涨幅居前，仅银行、白酒等少数防御性板块出现调整。中国经济网数据显示，A股市场上涨股票数<b>4156只</b>、73只涨停，'
 '下跌1239只、6只跌停；申万一级行业中通信、电子、机械设备分别上涨5.01%、3.97%、3.66%居涨幅前列，食品饮料、农林牧渔、非银金融分别下跌1.46%、0.76%、0.63%居跌幅前列。'
 '资金面上，截至10月27日10月以来股票型ETF累计净流入超<b>3300亿元</b>，10月28日沪深两市主力资金净流入超<b>140亿元</b>。'
 '上证报归因：海外方面，存储巨头SK海力士于北京时间10月28日发布业绩，2026财年第三季度营业收入和营业利润双双刷新历史最高纪录、环比分别增长32%和38%，'
 '单季营业收入首次突破100万亿韩元；国内方面，上海市经信委10月27日印发《上海市加快发展新一代智能制造行动方案》，A股科技企业三季报亦频频报喜。<br>\n'
 '              <b>美股（美东10-28）：</b>三大股指连续第三个交易日上涨并集体收涨，美联储维持利率不变但保留进一步加息可能；'
 '板块上科技与能源领涨、公用事业与房地产领跌，防御属性板块承压。\n'
 '            </div>\n'
 '          </div>\n'
 '        </div>\n'
 '        <div class="card-footer">\n'
 '          <a href="https://paper.cnstock.com/html/2026-10/29/content_2282878.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报电子版·10-29</span></a>\n'
 '          <a href="https://finance.ce.cn/stock/gsgdbd/202610/t20261029_3274905.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-29</span></a>\n'
 '          <a href="https://www.cs.com.cn/gppd/ggzx/2026/10/28/detail_2026102810047995.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·新华社·港股·10-28</span></a>\n'
 '          <a href="https://www.cnfin.com/gs-lb/detail/20261029/4487882_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·美股·10-29</span></a>\n'
 '          <a href="https://www.chnfund.com/article/ae83c8af-3d90-f409-dce6-3a249629eaef" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·原油·10-29</span></a>\n'
 '          <a href="https://m.cnfin.com/dz-lb//zixun/20261029/4487868_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·贵金属·10-29</span></a>\n'
 '          <span class="impact-tag medium">辅助决策</span>\n'
 '        </div>\n')

print('STEP5 new S6 open/close', op(new_s6), cl(new_s6))
assert op(new_s6) == op(old_s6) and cl(new_s6) == cl(old_s6), 'S6 div mismatch %s/%s vs %s/%s' % (op(new_s6), cl(new_s6), op(old_s6), cl(old_s6))
s = s[:i] + new_s6 + s[j:]
print('STEP5 S6 replaced; open/close now', op(s), cl(s))

# ---------------- STEP 6: S7 ----------------
S7M = '<!-- ============ Section 7'
i7 = s.find(S7M)
assert i7 > 0
first = s.find('<div class="timeline-item">', i7)
last = s.rfind('<div class="timeline-item">')
assert first > 0 and last >= first
assert s.count('<div class="timeline-item">') == 12, s.count('<div class="timeline-item">')
end7 = s.find('\n\n    </div>', last)
assert end7 > last
old_items = s[first:end7]
print('STEP6 old items open/close', op(old_items), cl(old_items))

ITEMS = [
    ('red',   '2026-10-29', '三季度新进重仓股曝光'),
    ('blue',  '2026-10-29', '主动权益基金高仓位守主线'),
    ('red',   '2026-10-29', '首批主动ETF启动建仓'),
    ('red',   '2026-10-28', '摩根主动ETF率先成立'),
    ('blue',  '2026-10-28', '香港零售基金新规倒计时'),
    ('blue',  '2026-10-28', 'A股放量反弹创业板涨3.40%'),
    ('blue',  '2026-10-28', '红利基金上新与限购并行'),
    ('red',   '2026-10-28', '美联储维持利率不变'),
    ('red',   '2026-10-26', '央行设立债市非银赎回便利'),
    ('blue',  '2026-10-23', '证监会母基金新规征求意见'),
    ('blue',  '2026-10-23', '首批18只主动ETF开售'),
    ('blue',  '2026-10-22', '中基协修订八项估值指引'),
]
assert len(ITEMS) == 12
for _, _, t in ITEMS:
    assert len(t) <= 25, t
dates = [d for _, d, _ in ITEMS]
assert dates == sorted(dates, reverse=True), dates

new_items = '\n'.join(
    ('      <div class="timeline-item">\n'
     '        <div class="timeline-dot %s"></div>\n'
     '        <div class="timeline-date">%s</div>\n'
     '        <div class="timeline-title">%s</div>\n'
     '      </div>' % (c, d, t)) for c, d, t in ITEMS)
print('STEP6 new items open/close', op(new_items), cl(new_items))
assert op(new_items) == op(old_items) and cl(new_items) == cl(old_items)
s = s[:first] + new_items + s[end7:]
print('STEP6 S7 replaced; open/close now', op(s), cl(s))

# ---------------- STEP 7: global assertions ----------------
assert op(s) == BASE_O and cl(s) == BASE_C, 'DRIFT %s/%s vs %s/%s' % (op(s), cl(s), BASE_O, BASE_C)
assert s.count('</div>>') == 0
assert s.count('\ufffd') == 0
assert s.count('Section 8') == 0 and s.count('待办跟踪') == 0 and s.count('腾安行动清单') == 0
assert s.count('<div class="timeline-item">') == 12
assert s.count('class="timeline-desc"') == 0
assert s.count('<div class="card p') == s.count('<div class="card p')
print('STEP7 global assertions ok; div %s/%s' % (op(s), cl(s)))

# date-tag cutoff
bad = []
for m in re.finditer(r'class="date-tag">(\d{2})-(\d{2})<', s):
    mo, dd = int(m.group(1)), int(m.group(2))
    d = date(2026, mo, dd)
    if d < CUT or d > TODAY:
        bad.append(m.group(0))
print('STEP7 date-tag out of window:', bad)
assert not bad, bad

# blacklist
BL = ['stcn', 'cls.cn', '21jingji', 'yicai.com', 'guba.eastmoney', 'toutiao', 'so.html5.qq.com',
      '163.com/dy', 'dy.163.com', 'cqcb.com', 'weibo.com', 'k.sina.com.cn', 'q.fund.sohu.com',
      'topnews.cn', 'futunn.com', 'jiantou8.com', 'cofool.com', 'yanglee.com', 'mp.weixin.qq.com']
hits = [b for b in BL if b in s]
print('STEP7 blacklist hits:', hits)
assert not hits, hits

open(P, 'w', encoding='utf-8').write(s)
print('WROTE', P)
print('md5', hashlib.md5(s.encode('utf-8')).hexdigest())
print('LEN', len(s))
