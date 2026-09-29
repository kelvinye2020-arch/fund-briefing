# -*- coding: utf-8 -*-
"""
_update_0929.py  —  基金行业资讯看板 2026-09-29 日更
更新范围：marker / header 区间 / meta / Stats Bar 沪指卡 / S0 四卡 / S6 行情 / S7 时间线
"""
import re, io, sys, shutil
from datetime import date, timedelta

HTML = 'index.html'
TODAY = date(2026, 9, 29)
DD = '09-29'
UPPER = TODAY.strftime('%Y.%m.%d')
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
EMO_CAL = '\U0001F4C5'
BADGE = EMO_CAL + ' 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)

src = open(HTML, encoding='utf-8').read()
o0, c0 = len(re.findall(r'<div\b', src)), src.count('</div>')
print('STEP0 open=%d close=%d' % (o0, c0))

def dr(tag):
    o = len(re.findall(r'<div\b', src)); c = src.count('</div>')
    print('  [%s] open=%d close=%d drift_o=%+d drift_c=%+d' % (tag, o, c, o - o0, c - c0))

# ============ 1. daily-update marker ============
MK_OLD = '<!-- daily-update: 2026-09-28 -->'
MK_NEW = '<!-- daily-update: 2026-09-29 -->'
assert src.count(MK_OLD) == 1, 'marker anchor'
src = src.replace(MK_OLD, MK_NEW)

# ============ 2. header 数据区间 badge ============
BADGE_PAT = (re.escape(EMO_CAL)
             + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
src, n = re.subn(BADGE_PAT, lambda m: BADGE, src)
assert n == 1, 'badge replace n=%d' % n
assert BADGE in src
print('STEP2 badge ->', BADGE)

# ============ 3. meta description + fingerprint ============
DESC = ('个人养老金扩容“固收+”26只增设Y份额|72只基金定档10月发行|'
        '09-28全市场ETF净流入302亿|9-28沪指收3823.62')
src, n = re.subn(r'(<meta name="description" content=")[^"]*(")',
                 lambda m: m.group(1) + DESC + m.group(2), src)
assert n == 1, 'desc'
FP = '个人养老|72只基|ETF净|创新药科'
src, n = re.subn(r'(<meta name="content-fingerprint" content=")[^"]*(")',
                 lambda m: m.group(1) + FP + m.group(2), src)
assert n == 1, 'fingerprint'
print('STEP3 meta ok')

# ============ 4. Stats Bar 沪指卡 ============
OLD_STAT = '''    <div class="stat-card">
      <div class="stat-number">3888.37</div>
      <div class="stat-label">沪指9-24收盘·跌1.22%·沪深北三市成交1.67万亿·缩量1140亿</div>
      <div class="stat-change down">▼ 失守3900点·超4300股下跌·贵金属有色领跌</div>
    </div>'''
NEW_STAT = '''    <div class="stat-card">
      <div class="stat-number">3823.62</div>
      <div class="stat-label">沪指9-28收盘·跌1.67%·沪深北三市成交1.72万亿·放量495亿</div>
      <div class="stat-change down">▼ 创业板指跌4.53%·超4500股下跌·元件通信领跌</div>
    </div>'''
assert src.count(OLD_STAT) == 1, 'stat anchor'
src = src.replace(OLD_STAT, NEW_STAT)
dr('stats')

# ============ 5. S0 整块替换 ============
S0M = '<!-- ============ Section 0: 今日焦点 ============ -->'
S1M = '<!-- ============ Section 1: 重磅信息 ============ -->'
assert src.count(S0M) == 1 and src.count(S1M) == 1
i0, i1 = src.find(S0M), src.find(S1M)
assert 0 < i0 < i1

QUOT_L = '\u201c'
QUOT_R = '\u201d'

C1_TITLE = ('\U0001F534 首批' + QUOT_L + '固收+' + QUOT_R + '基金纳入个人养老金名录·'
            '26只增设Y份额·12只偏债混合+14只含权二级债基')
C2_TITLE = ('\U0001F7E1 72只基金定档10月发行·首批北交所3个月持有期主题基金集中启动·权益类占比过半')
C3_TITLE = ('\U0001F7E1 09-28全市场ETF净流入约302.38亿·宽基191亿居首·'
            '创业板ETF易方达28.79亿·科创债ETF合计43.89亿')
C4_TITLE = ('\U0001F535 上证创新药科创领先指数与上证科创板软件服务指数今日发布·各选40只样本')

LINK = ('<a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;">'
        '<span class="source-tag">%s</span></a>')

BODY1 = (
    '上海证券报记者何漪9月29日报道（腾讯新闻·上海证券报社官方账号 09-29 08:04 发布）：'
    '含权二级债基与偏债混合基金两型' + QUOT_L + '固收+' + QUOT_R + '基金获准纳入个人养老金基金产品名录，'
    '9月28日首批纳入的' + QUOT_L + '固收+' + QUOT_R + '基金正式亮相。<br>\n'
    '          <b>落地范围：</b>涉及易方达、汇添富、富国、工银瑞信、招商、平安等<b>26家基金公司</b>；'
    '华夏鼎泓债券、南方致远混合、建信稳健惠享债券等<b>26只基金同日公告，自9月29日起</b>增设'
    '针对个人养老金投资基金业务单独设立的<b>Y类基金份额</b>，并开放申购、赎回、定期定额投资业务。'
    '26只中<b>12只为偏债混合基金、14只为含权二级债基</b>。<br>\n'
    '          <b>政策脉络：</b>依据《关于做好含权二级债基、偏债混合基金纳入个人养老金基金产品名录工作的通知》。'
    '2018年公募行业推出养老目标基金，2022年11月个人养老金制度落地并明确专属Y份额与费率优惠，'
    '此后首批养老目标基金、权益类指数基金相继纳入名录，本次是货架的又一次关键扩容。<br>\n'
    '          <b>准入与观点：</b>晨星（中国）基金研究中心高级分析师吴粤宁表示，纳入条件覆盖成立年限、规模、'
    '权益仓位、<b>最大回撤</b>、持有人结构及管理人评价等多个维度，其中回撤控制与权益敞口约束筛选作用较强；'
    '华夏基金称' + QUOT_L + '固收+' + QUOT_R + '风险收益特征介于纯债与权益之间；南方基金认为其补齐了'
    '养老FOF与指数基金之间的风险收益空白。<br>\n'
    '          <b>对腾安启示：</b>个人养老金货架新增' + QUOT_L + '中间档' + QUOT_R + '——'
    '养老FOF与权益指数之间的稳健含权品种终于补齐，腾安需在<b>Y份额专区</b>按'
    '<b>权益仓位上限、近3年最大回撤、成立年限与规模</b>四项重做筛选与标签，'
    '并把' + QUOT_L + '管理费托管费五折' + QUOT_R + '与递延纳税优惠前置到产品页；'
    '同时提示Y份额赎回费阶梯（持有小于7日1.5%、7—30日1%、30—180日0.5%、超180日免收），'
    '避免用户因流动性预期错配而提前赎回。'
)
ACTION1 = '''        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 货架改造→9月30日前完成个人养老金Y份额专区改版，新增26只“固收+”产品并按权益仓位上限、近3年最大回撤、成立年限、最近4季末规模四项排序；<br>
            ② 话术与素材→同步上线“费率五折+递延纳税”对比表与Y份额赎回费阶梯说明，避免用户误判流动性；<br>
            ③ 准入跟踪→本次首批严控“一司一只”，跟踪后续常态化申报与动态奖惩名单，提前对接尚未入选的头部公司。
          </div>
        </div>'''

BODY2 = (
    '新华财经上海9月29日电（转上海证券报）：聚焦四季度投资机会，公募加紧布局新产品，'
    '<b>72只基金定档10月发行</b>。9月28日<b>12只基金</b>发布基金份额发售公告，均在10月启动发行。<br>\n'
    '          <b>结构：</b>权益类基金占比过半。中欧基金集中推出中欧中证工业有色金属主题指数、'
    '中欧全裕智选混合、中欧均衡增长混合、中欧金融优选混合等多只产品；投向集中在科技与新能源——'
    '人工智能主题、创业板软件主题、创业板电池主题、半导体主题等指数基金，'
    '以及数字经济主题、新能源主题等主动权益基金。含权类' + QUOT_L + '固收+' + QUOT_R + '亦是重点。<br>\n'
    '          <b>北交所主题：</b>多只<b>北交所3个月持有期主题基金</b>集中敲定发行日期，'
    '为首批北交所3个月持有期产品。截至9月28日，还有<b>56只基金正在发行</b>。<br>\n'
    '          <b>机构动向：</b>公募排排网数据显示，上周（9月21日—27日）<b>超100家基金管理人</b>调研A股上市公司，'
    '电子、计算机、机械设备三大行业调研热度居前；国盛证券测算，截至9月24日主动权益类基金<b>平均股票仓位约87.59%</b>，'
    '较9月17日<b>上升1.06个百分点</b>，重点增配医药、电力及公用事业、农林牧渔。<br>\n'
    '          <b>对腾安启示：</b>10月发行潮叠加国庆长假，是<b>节前预约、节后首发</b>的天然营销窗口——'
    '货架应提前上线' + QUOT_L + '10月新发日历' + QUOT_R + '并按主题（AI/电池/半导体/北交所/含权固收+）分组；'
    '北交所3个月持有期产品需显著提示锁定期与5亿元募集上限下的末日比例确认规则，'
    '避免用户误以为可随时赎回。'
)

BODY3 = (
    '格隆汇9月29日资金流向观察：9月28日ETF市场资金面整体呈大幅净流入格局，'
    '九大类ETF中<b>六类流入、三类流出，整体净流入约302.38亿元</b>。<br>\n'
    '          <b>宽基为吸金主力：</b>单日净流入<b>191亿元</b>居各大类之首、占整体净流入六成以上；'
    '净流入TOP20榜单中宽基占<b>11席、合计约129.32亿元</b>，'
    '创业板ETF易方达以<b>28.79亿元</b>居全市场首位，'
    '沪深300ETF华泰柏瑞净流入12.13亿元、对应<b>1067.05亿元</b>的千亿级规模。<br>\n'
    '          <b>成长方向集中配置：</b>创业板方向2只合计约35.90亿元，科创50方向2只合计约30.30亿元，'
    '中证1000方向2只合计约23.06亿元。<br>\n'
    '          <b>科创债延续获增持：</b>5只科创债ETF集体上榜、合计约<b>43.89亿元</b>，'
    '科创债ETF嘉实<b>18.99亿元</b>（规模456.38亿元）居债券类首位；公司债ETF南方净流入7.35亿元、'
    '信用债ETF海富通5.05亿元，债券类在榜单中合计约55.29亿元。<br>\n'
    '          <b>流出端温和：</b>三类流出合计约16.43亿元，不足整体净流入一成；'
    '净流出首位为货币类华宝添益ETF（8.23亿元），黄金方向3只合计净流出约8.76亿元；'
    '行业主题内部分化，通信ETF国泰净流入15.72亿元、芯片ETF华夏3.65亿元，'
    '而半导体设备ETF国泰净流出3.61亿元。<br>\n'
    '          <b>对腾安启示：</b>指数大跌当日宽基ETF反而净流入191亿元，是典型的'
    '<b>逆势加仓</b>信号——货架应把' + QUOT_L + '资金流向' + QUOT_R + '做成与净值涨跌并列的展示维度，'
    '并对科创债ETF这类' + QUOT_L + '机构主导+持续净流入' + QUOT_R + '品种标注二级流动性；'
    '黄金ETF在金价回调日出现净流出，需在黄金主题页同步给出' + QUOT_L + '价涨量减' + QUOT_R + '的风险提示。'
)

BODY4 = (
    '证券日报报道（中国经济网9月29日转刊）：9月29日，'
    '上海证券交易所和中证指数有限公司正式发布<b>上证创新药科创领先指数</b>与'
    '<b>上证科创板软件服务指数</b>。<br>\n'
    '          <b>编制口径：</b>上证创新药科创领先指数从科创板和上证主板上市公司中选取'
    '<b>40只研发水平高、成长性好的创新药领域</b>上市公司证券作为样本；'
    '上证科创板软件服务指数从科创板选取<b>40只软件开发、软件服务领域</b>证券作为样本，'
    '覆盖工业软件、基础软件、云计算、网络安全、AI应用软件等关键细分方向。<br>\n'
    '          <b>指数供给结构：</b>Wind数据显示，A股市场年内已累计迎来<b>605条新指数</b>，'
    '其中债券指数<b>353条</b>、股票指数196条、多资产指数56条，'
    '<b>债券指数占比跃居第一大品类</b>；新增供给正从泛科技赛道向半导体材料设备、芯片设计、'
    '算力基础设施等上游关键环节下沉。<br>\n'
    '          <b>专家观点：</b>接受采访的专家表示，精细化指数是连接科创产业与中长期资金的重要桥梁，'
    '相较传统宽基指数，细分赛道指数产业属性更纯粹、投资逻辑更清晰，可为机构提供专业化业绩比较基准与'
    '资产配置工具。<br>\n'
    '          <b>对腾安启示：</b>两条指数分别为创新药、国产软件提供了<b>可跟踪的基准锚</b>——'
    '货架可据此对现有创新药/软件主题基金做' + QUOT_L + '是否跑赢细分基准' + QUOT_R + '的归因展示，'
    '并提前跟踪后续挂钩产品的申报；同时提示用户，新指数发布初期往往伴随主题基金密集申报，'
    '需警惕' + QUOT_L + '指数先行、业绩待验' + QUOT_R + '的追高节奏。'
)

def card(cls, prio_cls, prio_txt, title, body, links, impact, action=''):
    ls = '\n          '.join(LINK % (u, t) for u, t in links)
    return (
        '      <div class="card %s">\n'
        '        <div class="card-top">\n'
        '          <div class="card-title">%s</div>\n'
        '          <div class="card-meta">\n'
        '            <span class="priority-tag %s">%s</span>\n'
        '            <span class="date-tag">%s</span>\n'
        '          </div>\n'
        '        </div>\n'
        '        <div class="card-body">\n'
        '          %s\n'
        '        </div>\n'
        '        <div class="card-footer">\n'
        '          %s\n'
        '          <span class="impact-tag %s">%s</span>\n'
        '        </div>\n'
        '%s'
        '      </div>\n'
    ) % (cls, title, prio_cls, prio_txt, DD, body, ls, impact[0], impact[1],
         (action + '\n') if action else '')

C1 = card('p0', 'urgent', 'P0 紧急必看', C1_TITLE, BODY1,
          [('https://new.qq.com/rain/a/20260929A02QB500', '腾讯新闻·上海证券报·09-29'),
           ('https://www.cnfin.com/yw-lb/detail/20260929/4475939_1.html', '新华财经·09-29')],
          ('high', '影响：高'), ACTION1)
C2 = card('p1', 'important', 'P1 重要关注', C2_TITLE, BODY2,
          [('https://www.cnfin.com/gs-lb/detail/20260929/4475950_1.html', '新华财经·09-29'),
           ('https://stock.10jqka.com.cn/20260929/c680337981.shtml', '同花顺财经·上海证券报·09-29')],
          ('mid', '影响：中'))
C3 = card('p1', 'important', 'P1 重要关注', C3_TITLE, BODY3,
          [('https://www.gelonghui.com/live/2692882', '格隆汇·09-29')],
          ('mid', '影响：中'))
C4 = card('p2', 'normal', 'P2 建议了解', C4_TITLE, BODY4,
          [('https://finance.ce.cn/stock/gsgdbd/202609/t20260929_3240197.shtml', '中国经济网·09-29'),
           ('https://news.qq.com/rain/a/20260929A037OE00', '腾讯新闻·央广财经·09-29')],
          ('mid', '影响：中'))

S0_NEW = (S0M + '\n'
    '  <div class="section">\n'
    '    <div class="section-header">\n'
    '      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">\U0001F525</div>\n'
    '      <div class="section-title-group">\n'
    '        <span class="section-title">今日焦点</span>\n'
    '        <span class="section-context">9月29日 · 4条今日要闻</span>\n'
    '      </div>\n'
    '      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>\n'
    '    </div>\n'
    '\n'
    '    <div class="card-grid">\n'
    '            <!-- S0 Card 1 (09-29 P0) -->\n'
    + C1 +
    '<!-- S0 Card 2 (09-29 P1) -->\n'
    + C2 +
    '<!-- S0 Card 3 (09-29 P1) -->\n'
    + C3 +
    '<!-- S0 Card 4 (09-29 P2) -->\n'
    + C4 +
    '    </div>\n'
    '  </div>\n')

src = src[:i0] + S0_NEW + src[i1:]
dr('s0')

# ============ 6. S6 行情卡替换 ============
S6M = '<!-- ============ Section 6: 市场行情速览 ============ -->'
S7M = '<!-- ============ Section 7: 关键时间线 ============ -->'
i6 = src.find(S6M)
cs = src.find('            <div class="card p3">', i6)
assert 0 < i6 < cs
TAIL6 = '      </div>  </div>\n'
te = src.find(TAIL6, cs)
assert te > cs
CUT6 = te + len('      </div>')

S6_NEW = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股09-28收盘·沪指3823.62 -1.67%沪深北成交1.72万亿｜港美股09-28收盘</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-29</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-28收盘·节前放量重挫）</b><br>
              上证指数 <b>3823.62</b> <span style="color:#52c41a;">-1.67%</span><br>
              深证成指 <b>12858.75</b> <span style="color:#52c41a;">-3.44%</span><br>
              创业板指 <b>3139.82</b> <span style="color:#52c41a;">-4.53%</span><br>
              沪深300 <b>4340.76</b> <span style="color:#52c41a;">-2.22%</span><br>
              科创50 <b>1555.98</b> <span style="color:#52c41a;">-4.06%</span><br>
              北证50 <b>1026.57</b> <span style="color:#52c41a;">-2.76%</span><br>
              沪深北三市成交 <b>1.72万亿</b>·较上一交易日放量约495亿<br>
              4554只下跌·898只上涨·105只平盘
            </div>
            <div>
              <b>港股与美股（09-28收盘）</b><br>
              恒生指数 <b>24642.51</b> <span style="color:#dc2626;">+0.54%</span><br>
              恒生科技 <b>4296.00</b> <span style="color:#52c41a;">-0.37%</span><br>
              国企指数 <b>8216.84</b> <span style="color:#dc2626;">+0.63%</span><br>
              道琼斯 <b>51481.51</b> <span style="color:#52c41a;">-0.67%</span><br>
              纳斯达克 <b>26820.38</b> <span style="color:#52c41a;">-0.92%</span><br>
              标普500 <b>7683.69</b> <span style="color:#52c41a;">-0.77%</span><br>
              布伦特原油105.28美元 <span style="color:#dc2626;">+0.92%</span>·COMEX黄金4148.50美元 <span style="color:#52c41a;">-4.00%</span>·美债10年期5.236%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>A股结构（09-28）：</b>呈现明显的\u201c高切低\u201d特征\u2014\u2014汽车整车、小家电、风电设备涨幅居前，汽车整车板块逆势涨超1%（江淮汽车、众泰汽车涨停），猪肉、白酒、电力、银行、中药、油气开采相对抗跌；元件板块大跌超6%，通信设备跌超6%（中际旭创跌超9%、光迅科技等跌停），电子化学、非金属材料、贵金属均跌超5%，半导体、消费电子跌超4%。<br>
              <b>港股（09-28）：</b>三大指数走势分化，恒指涨0.54%报24642.51点、国企指数涨0.63%报8216.84点、恒生科技跌0.37%报4296点，主板成交1774.82亿港元。科网股支撑大盘，网易涨近5%领涨蓝筹（暴雪嘉年华官宣《星际争霸》新作），快手涨超2%；煤炭板块走强，中国神华涨超3%；半导体股多数下跌，天数智芯跌超11%、中芯国际跌超3%；黄金股与有色下行，灵宝黄金跌10%、山东黄金跌超9%；内房股涨幅居前，中国金茂涨超6%。<br>
              <b>美股（09-28）：</b>美债收益率飙升拖累风险资产，10年期升至5.2%以上、30年期突破5.5%。存储与半导体普跌\u2014\u2014SK海力士跌超5%、英特尔跌超5%、高通跌超7%、ARM跌超8%，英伟达逆势涨超1%；金融股全线收跌；中概股多数上涨，纳斯达克中国金龙指数涨1.12%。COMEX黄金期货跌4.00%报4148.50美元、白银跌5.82%，布伦特原油涨0.92%报105.28美元。<br>
              <b>备注：</b>09-28为中秋假期后首个交易日，本期A股、港股、美股基准统一为09-28收盘。国庆假期安排：A股节前仅余09-29、09-30两个交易日，10月1日\u2014\u20147日休市、10月8日开市。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股 / 港股 / 美股均为2026-09-28收盘</span>
          <span class="source-tag">数据来源：中国经济网（证券日报）、中新经纬、新华社、新华财经、中国基金报、央广财经（09-28—09-29）</span>
        </div>
      </div>'''

src = src[:cs] + S6_NEW + src[CUT6:]
dr('s6')

# ============ 7. S7 时间线重写 ============
TAIL7 = '    </div>\n\n  </div>\n\n</div>\n\n\n</body>\n</html>\n'
assert src.endswith(TAIL7), 'tail7'
i7 = src.find(S7M)
f7 = src.find('<div class="timeline-item">', i7)
assert 0 < i7 < f7
e7 = len(src) - len(TAIL7)
assert f7 < e7

TL = [
    ('red',  '2026-09-29', '固收+基金纳入个人养老金名录'),
    ('red',  '2026-09-29', '72只基金定档10月发行'),
    ('blue', '2026-09-29', '两条科创细分指数发布'),
    ('blue', '2026-09-29', 'ETF单日净流入302亿'),
    ('red',  '2026-09-28', 'A股放量重挫创业板跌4.53%'),
    ('blue', '2026-09-28', '债券ETF规模首破万亿'),
    ('blue', '2026-09-28', '险资可投港股通ETF开闸'),
    ('blue', '2026-09-28', '商业不动产REITs三只获受理'),
    ('blue', '2026-09-28', '网易涨近5%领涨港股蓝筹'),
    ('red',  '2026-09-25', '湖南百亿未来产业基金落地'),
    ('red',  '2026-09-24', '中秋前A股缩量回调失守3900'),
    ('blue', '2026-09-24', '国新国证张鹏任总经理'),
]
for _, _, t in TL:
    assert len(t) <= 25, 'timeline title too long: %s (%d)' % (t, len(t))

ITEM = ('<div class="timeline-item">\n'
        '        <div class="timeline-dot %s"></div>\n'
        '        <div class="timeline-date">%s</div>\n'
        '        <div class="timeline-title">%s</div>\n'
        '      </div>')
S7_NEW = '\n      '.join(ITEM % (c, d, t) for c, d, t in TL)
src = src[:f7] + S7_NEW + src[e7:]
dr('s7')

# ============ Phase1 全量断言 ============
errs = []
def chk(cond, msg):
    if not cond:
        errs.append(msg)

o, c = len(re.findall(r'<div\b', src)), src.count('</div>')
chk(o == c, 'div 不平衡 open=%d close=%d' % (o, c))
chk(o - o0 == 3, 'div drift 应为 +3（新增1个action-box），实际 %+d' % (o - o0))
chk('\ufffd' not in src, '存在 U+FFFD 乱码')
chk(src.count('</div>>') == 0, "存在游离 '</div>>'")
chk('Section 8' not in src and 'S8' not in src, 'S8 残留')
chk(src.count(MK_NEW) == 1, 'marker')

# S0 断言
a = src.find(S0M); b = src.find(S1M)
s0 = src[a:b]
chk(re.search(r'<span class="section-title">今日焦点</span>', s0) is not None, 'S0 title 非「今日焦点」')
chk('<span class="section-context">9月29日 · 4条今日要闻</span>' in s0, 'S0 context 错')
chk(s0.count('<div class="card p') == 4, 'S0 卡数 %d != 4' % s0.count('<div class="card p'))
dts = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s0)
chk(dts == [('09', '29')] * 4, 'S0 date-tag %s' % dts)
chk(s0.count('<a href="http') == 7,
    'S0 链接数 %d != 7' % s0.count('<a href="http'))
chk(s0.count('class="action-box"') == 1, 'S0 action-box %d != 1' % s0.count('class="action-box"'))
s0titles = [re.sub(r'<[^>]+>', '', t) for t in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', s0, re.S)]
for seg in FP.split('|'):
    chk(any(seg[:4] in t for t in s0titles), 'fingerprint 段 %s 未命中 S0 标题' % seg)

# 黑名单（新增段）
BAD = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'toutiao', 'so.html5.qq.com',
       'guba.eastmoney', '163.com/dy', 'weibo.com', 'k.sina.com.cn', 'cqcb.com']
seg_new = src[src.find(S0M):]
for u in re.findall(r'href="(https?://[^"]+)"', seg_new):
    for bd in BAD:
        chk(bd not in u, '黑名单 %s : %s' % (bd, u))

# S6
s6 = src[src.find(S6M):src.find(S7M)]
chk('3823.62' in s6 and '24642.51' in s6 and '51481.51' in s6, 'S6 数据缺失')
chk('09-24' not in s6.split('备注')[0], 'S6 仍残留 09-24 基准')

# S7
s7 = src[src.find(S7M):]
chk(s7.count('<div class="timeline-item">') == 12, 'S7 条数 %d != 12' % s7.count('<div class="timeline-item">'))
s7d = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', s7)
chk(len(s7d) == 12, 'S7 date 数 %d' % len(s7d))
chk(s7d == sorted(s7d, reverse=True), 'S7 非降序')
chk('timeline-desc' not in s7, 'S7 出现 timeline-desc')

# Stats bar
sb = src[src.find('<!-- Stats Bar -->'):src.find('<!-- Priority Legend -->')]
chk('3823.62' in sb and '9-28收盘' in sb, 'Stats Bar 沪指卡未更新')

# header
chk(BADGE in src, 'header badge')

if errs:
    print('\n'.join('ERR ' + e for e in errs))
    print('Phase1 FAILED, 未写文件')
    sys.exit(1)

shutil.copy(HTML, '_bak_0929.html')
open(HTML, 'w', encoding='utf-8').write(src)
print('\nWROTE index.html  div %d -> %d (drift %+d)' % (o0, o, o - o0))
print('OK')
