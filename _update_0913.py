# -*- coding: utf-8 -*-
"""
2026-09-13（周日）基金看板日更
- header 数据区间动态计算
- S0 今日焦点 4 卡全换（周末休市无 T+0，全部为 09-12 T-1 原创新闻）
- S1/S2/S6/Stats Bar：均在窗内 / 周末无新交易日 → 不动
- S7 时间线：重写 12 条
"""
import re
import sys
from datetime import date, timedelta

HTML = 'index.html'
TODAY = date(2026, 9, 13)
T14 = TODAY - timedelta(days=14)
CUTOFF = T14  # 2026-08-30

src = open(HTML, encoding='utf-8').read()
orig = src
open_count_orig = len(re.findall(r'<div\b', src))
close_count_orig = len(re.findall(r'</div>', src))
print('STEP0 div open/close =', open_count_orig, close_count_orig)
print('STEP0 len =', len(src))

# ============================================================
# [1] header 数据区间（动态计算）
# ============================================================
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
badge_new = '\U0001F4C5 数据区间：' + lower + ' — ' + upper + '（每日更新）'
pat_badge = re.compile(r'\U0001F4C5 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
assert len(pat_badge.findall(src)) == 1, 'badge anchor not unique'
src = pat_badge.sub(badge_new, src)
assert badge_new in src
print('STEP1 badge ->', badge_new)

# ============================================================
# [2] S0 整块替换
# ============================================================
A_S0_HEAD = '      <!-- S0 Card 1'
A_S1 = '<!-- ============ Section 1: 重磅信息 ============ -->'
assert src.count(A_S0_HEAD) == 1, 'S0 head anchor not unique'
assert src.count(A_S1) == 1, 'S1 anchor not unique'
i0 = src.index(A_S0_HEAD)
i1 = src.index(A_S1)
assert i0 < i1

LINK = '<a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">%s</span></a>'

# ---- Card 1 : QDII 溢价风险 ----
u1a = 'http://www.zqrb.cn/fund/jijindongtai/2026-09-12/A1789133943826.html'
u1b = 'https://news.qq.com/rain/a/20260913A02WIA00'
b1 = (
    '证券日报9月12日报道：9月11日，易方达基金、华夏基金、富国基金、景顺长城基金等<b>同日发布旗下近20只QDII基金'
    '二级市场交易价格溢价风险提示公告</b>；截至9月11日收盘，<b>全市场仍有20只QDII基金的IOPV溢价率超过5%</b>，'
    '部分热门产品9月以来已累计发布11次溢价风险提示，保持“日更”节奏。以易方达MSCI美国50ETF（QDII）为例，'
    '9月10日二级市场收盘价1.835元，相对当日基金份额参考净值溢价<b>5.36%</b>，公司直言“投资者如果高溢价买入，'
    '可能面临较大损失”；若溢价未有效回落，基金公司或申请盘中临时停牌、延长停牌甚至连续停牌。'
    '<br><b>成因：</b>晨星（中国）基金研究中心总监孙珩表示，核心症结在于一级市场供给受限与二级市场需求旺盛之间的'
    '阶段性错配——境内投资者对美股与科技类资产配置需求旺盛，而QDII产品受外汇额度与申购限额约束，'
    '部分产品一级市场申购受限；境内外交易时差、汇率波动、流动性状况与短期情绪也会放大价格与净值的偏离。'
    '<br><b>机构观点：</b>华泰柏瑞基金相关人士表示，长期看二级市场价格必然向基金净值靠拢：'
    '其一，溢价本质是情绪驱动的短期价格偏离，热点退潮后资金流出将推动溢价收敛；'
    '其二，正向套利会持续发挥调节作用——一级市场申购增加份额、二级市场卖出增加供给，直至溢价被抹平。'
    '<br><b>对腾安启示：</b>QDII高溢价已呈“日更”常态化，行情页须实时展示IOPV与溢价率，'
    '对溢价超5%品种加挂强提示，并默认引导客户走场外申购或同类低溢价替代，严禁以场内溢价品种承接追高需求。'
)

# ---- Card 2 : 宽基ETF放量 ----
u2a = 'https://www.cnstock.com/commonDetail/789379'
b2 = (
    '上海证券报9月12日（记者赵明超）：9月11日多只宽基ETF成交显著放量——科创50ETF华夏成交<b>80.83亿元</b>'
    '（前一交易日36.75亿元）、创业板ETF易方达<b>63.2亿元</b>（前一交易日37.31亿元）、沪深300ETF华泰柏瑞44.09亿元、'
    '中证500ETF南方43.18亿元、中证1000ETF南方34.7亿元，多只呈V形反转，下跌阶段成交额激增。'
    '<br><b>资金流向：</b>据Choice测算，9月10日股票型ETF净流入25.51亿元；截至9月10日的近一周，'
    '<b>股票型ETF资金净流入109.25亿元</b>，其中科创50ETF华夏42.05亿元、中证500ETF南方29.75亿元居前，'
    '宽基ETF为“吸金”主力——市场震荡时ETF往往呈现净流入。'
    '<br><b>发行端：</b>Choice数据显示，截至9月11日有<b>133只新基金正在发行</b>，另有36只已发布基金份额发售公告、'
    '即将启动发行，权益类基金为新发主力军。'
    '<br><b>机构观点：</b>西南证券研报测算，基于2025年银行理财、公募基金、保险资金与信托资金规模及各类机构权益配置比例，'
    '当前资管体系中<b>权益类资产占比仅约9.84%</b>，居民资金少量从存款转向财富管理产品即可带来可观增量。'
    '<br><b>对腾安启示：</b>震荡期宽基ETF持续吸金说明客户“抄底”需求旺盛，应把宽基ETF入口前置，'
    '并配套定投与分批建仓工具，避免客户把宽基品种当短线博弈筹码。'
)

# ---- Card 3 : 南向资金近千亿 ----
u3a = 'https://paper.cnstock.com/html/2026-09/12/content_2268425.htm'
u3b = 'https://www.chnfund.com/article/73f9a867-64ff-6bd2-9f86-3a23a53287d9'
b3 = (
    '上海证券报9月12日报道，Wind数据显示：截至9月11日，<b>南向资金7月以来合计净买入985.8亿港元</b>'
    '（7月净买入628.7亿港元，较6月271.11亿港元增长逾130%；8月103.8亿港元；9月截至11日253.3亿港元）。'
    '资金推动下，7月以来截至9月11日恒生指数上涨8.41%，在全球重要指数中领先——同期日经225指数与韩国综合指数'
    '分别下跌8.64%和18.48%。'
    '<br><b>加仓方向：</b>据Choice统计，7月以来截至9月10日，南向资金对明略科技-W、禾赛-W、智谱等个股'
    '增持比例均超300%，云知声、天数智芯、壁仞科技、国恩科技、兆易创新等增持逾100%，科技龙头与红利资产为两大主线。'
    '<br><b>机构观点：</b>国海富兰克林基金量化与指数投资总监张志强表示，此轮港股反弹打破了此前的下行通道，'
    '部分投资日韩市场的资金开始流向港股，南向资金明显回流，港股或摆脱下行趋势进入震荡阶段；'
    '平安港股通红利精选基金经理丁琳认为，港股整体估值处于历史中等水平，H股相对A股仍存在一定折价，性价比突出。'
    '<br><b>对腾安启示：</b>港股“科技+红利”哑铃配置需求升温，相关港股通基金与跨境ETF须同步展示估值分位、'
    '汇率与额度风险，并对高溢价品种做前置提示。'
)

# ---- Card 4 : 厄尔尼诺 / 农产品 ----
u4a = 'https://epaper.cs.com.cn/zgzqb/html/2026-09/12/nw.D110000zgzqb_20260912_1-A04.htm'
u4b = 'https://finance.sina.com.cn/roll/2026-09-12/doc-inirpkck8634074.shtml'
b4 = (
    '中国证券报9月12日（记者葛瑶）：世界气象组织9月3日称<b>厄尔尼诺已经确立</b>，预计未来数月增强为超强事件、'
    '年底前后达到峰值，持续至2027年2月的概率接近100%。受此影响，全球部分产区极端天气风险上升，'
    'A股农业产业链从种植、种业到化肥、农药热度持续攀升。截至9月11日收盘，Wind农产品指数自6月29日低点以来'
    '累计上涨<b>21.68%</b>（近两个交易日有所回调）。'
    '<br><b>期货端：</b>CBOT玉米主力近一月涨14.51%至528.75美分/蒲式耳、小麦涨15.42%至739.75美分/蒲式耳'
    '（9月2日盘中一度触及795美分，创近两年新高）、大豆涨11.8%至约1319美分/蒲式耳；'
    'ICE 11号原糖9月10日跳涨至19.9美分/磅，近一月累计涨幅超18%。联合国粮农组织表示，'
    '欧洲高温干旱、亚洲部分主产国的厄尔尼诺相关天气与巴西中南部食糖产量下降共同影响供给预期。'
    '<br><b>机构提示：</b>各产区、各品种所受影响存在差异，行情能否延续仍需观察减产预期与实际供需的变化。'
    '<br><b>对腾安启示：</b>农业主题基金与ETF易受天气与情绪驱动短线上冲，须同步提示波动与回调风险，'
    '并以定投、分批等工具替代一次性追高。'
)


def card(comment, cls, ptag, ptext, date_tag, title, body, sources, impact_tag, impact_text):
    links = '\n          '.join(LINK % (u, t) for u, t in sources)
    return (
        '      <!-- S0 Card %s -->\n'
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
        '      </div>\n'
        % (comment, cls, title, ptag, ptext, date_tag, body, links, impact_tag, impact_text)
    )


c1 = card('1 (09-12 P1)', 'p1', 'important', 'P1 重要关注', '09-12',
          '\U0001F7E1 QDII基金密集提示溢价风险·近20只同日发公告·20只IOPV溢价率超5%',
          b1,
          [(u1a, '证券日报·09-12'), (u1b, '腾讯新闻·财经早餐·09-13')],
          'medium', '风险：中')

c2 = card('2 (09-12 P1)', 'p1', 'important', 'P1 重要关注', '09-12',
          '\U0001F7E1 宽基ETF成交放量·股票型ETF一周净流入109亿·133只新基金正在发行',
          b2,
          [(u2a, '上海证券报·09-12')],
          'medium', '影响：中')

c3 = card('3 (09-12 P2)', 'p2', 'normal', 'P2 建议了解', '09-12',
          '\U0001F535 南向资金7月以来净买入近千亿港元·科技龙头与红利资产成加仓主线',
          b3,
          [(u3a, '上海证券报·09-12'), (u3b, '中国基金报·09-12')],
          'low', '影响：中')

c4 = card('4 (09-12 P2)', 'p2', 'normal', 'P2 建议了解', '09-12',
          '\U0001F535 厄尔尼诺扰动供给·农产品期货集体升温·农业主题基金热度攀升',
          b4,
          [(u4a, '中国证券报·09-12'), (u4b, '新浪财经·09-12')],
          'low', '影响：中')

s0_new = c1 + '\n\n' + c2 + '\n\n' + c3 + '\n\n' + c4 + '\n'

src = src[:i0] + s0_new + '\n    </div>\n  </div>\n\n' + src[i1:]
print('STEP2 S0 cards replaced, len =', len(src))

# ============================================================
# [3] S0 section-context 单独改（整块替换不会带上 header）
# ============================================================
OLD_CTX = '<span class="section-context">9月12日 · 4条今日要闻</span>'
NEW_CTX = '<span class="section-context">9月12日 · 4条今日要闻</span>'
# 保险起见：先把任何旧 context 归一成目标值
pat_ctx = re.compile(r'<span class="section-context">[^<]*</span>')
hits = pat_ctx.findall(src)
assert len(hits) == 1, 'section-context not unique: %r' % hits
src = pat_ctx.sub(NEW_CTX, src)
assert NEW_CTX in src
print('STEP3 context ->', NEW_CTX)

# ============================================================
# [4] S7 时间线重写
# ============================================================
A_S7_FIRST = '      <div class="timeline-item">'
A_S7_END = '    </div>\n\n  </div>\n\n</div>'
assert src.count(A_S7_FIRST) >= 1, 'S7 first item anchor missing'
assert src.count(A_S7_END) == 1, 'S7 end anchor not unique'
k0 = src.index(A_S7_FIRST)
k1 = src.index(A_S7_END)
assert k0 < k1

ITEMS = [
    ('blue', '2026-09-12', '算力ETF进入上市期·天弘9-16挂牌'),
    ('blue', '2026-09-12', '第二批摊余成本法债基上报'),
    ('blue', '2026-09-12', '近一月1055家公司获机构调研'),
    ('blue', '2026-09-12', '中欧一基金二次召集持有人大会'),
    ('red', '2026-09-11', '金融强国“十五五”规划正式出台'),
    ('blue', '2026-09-11', '公募布局白盒固收+·规模超2.28万亿'),
    ('red', '2026-09-11', '两大主题ETF集中申报·18家'),
    ('red', '2026-09-11', 'A股放量调整·成交1.99万亿'),
    ('red', '2026-09-10', 'A股缩量调整·成交创年内次低'),
    ('red', '2026-09-10', '易方达4只ETF以TDR登陆泰交所'),
    ('red', '2026-09-10', '新基金低位快速建仓·9月99只'),
    ('blue', '2026-09-10', '全国首单水利REITs获批·15.83亿'),
]

TPL = (
    '      <div class="timeline-item">\n'
    '        <div class="timeline-dot %s"></div>\n'
    '        <div class="timeline-date">%s</div>\n'
    '        <div class="timeline-title">%s</div>\n'
    '      </div>\n'
)
s7_new = ''.join(TPL % it for it in ITEMS)
src = src[:k0] + s7_new + '\n' + src[k1:]
print('STEP4 S7 rewritten, len =', len(src))

# ============================================================
# Phase 1 全套断言（不通过就不写文件）
# ============================================================
errs = []

# --- div 平衡 ---
op = len(re.findall(r'<div\b', src))
cl = len(re.findall(r'</div>', src))
if op != cl:
    errs.append('div 不平衡 %d/%d' % (op, cl))
# 预期漂移：S0 4卡→4卡（均无 action-box）、S7 12条→12条 → drift 0
if (op - open_count_orig) != 0:
    errs.append('div open drift %d != 0' % (op - open_count_orig))
if (cl - close_count_orig) != 0:
    errs.append('div close drift %d != 0' % (cl - close_count_orig))

# --- 游离字符 ---
if src.count('</div>>') != 0:
    errs.append('游离 </div>> 出现 %d 次' % src.count('</div>>'))

# --- S8 不存在 ---
if 'S8' in src or '待办跟踪' in src or '腾安行动清单' in src:
    errs.append('S8 残留')

# --- U+FFFD ---
if src.count('\ufffd') != 0:
    errs.append('U+FFFD 乱码 %d 处' % src.count('\ufffd'))

# --- S0 段校验 ---
i0b = src.index(A_S0_HEAD)
i1b = src.index(A_S1)
seg0 = src[i0b:i1b]
if seg0.count('<div class="card p') != 4:
    errs.append('S0 卡数 %d != 4' % seg0.count('<div class="card p'))
if seg0.count('action-box') != 0:
    errs.append('S0 出现 action-box（本日无 P0）')
if seg0.count('<span class="date-tag">09-12</span>') != 4:
    errs.append('S0 date-tag 09-12 计数 %d != 4' % seg0.count('<span class="date-tag">09-12</span>'))
# 链接数 2+1+2+2 = 7
if seg0.count('<span class="source-tag">') != 7:
    errs.append('S0 source 链接数 %d != 7' % seg0.count('<span class="source-tag">'))
# 每条卡都有 card-meta
if seg0.count('card-meta') != 4:
    errs.append('S0 card-meta 数 %d != 4' % seg0.count('card-meta'))
# title 精确
m_title = re.search(r'<span class="section-title">今日焦点</span>', src)
if not m_title:
    errs.append('S0 section-title 不是「今日焦点」')
if NEW_CTX not in src:
    errs.append('S0 section-context 未生效')

# --- S1 / S2 ---
seg1 = src[src.index(A_S1):src.index('<!-- ============ Section 2: 监管政策 ============ -->')]
if seg1.count('<div class="card p') != 6:
    errs.append('S1 卡数 %d != 6' % seg1.count('<div class="card p'))
A_S3 = '<!-- ============ Section 3: 竞争对手动态 ============ -->'
seg2 = src[src.index('<!-- ============ Section 2: 监管政策 ============ -->'):src.index(A_S3)]
if seg2.count('<div class="card p') != 4:
    errs.append('S2 卡数 %d != 4' % seg2.count('<div class="card p'))

# --- S7 ---
seg7 = src[src.index('<!-- ============ Section 7: 关键时间线 ============ -->'):]
n_item = seg7.count('<div class="timeline-item">')
if n_item != 12:
    errs.append('S7 条目 %d != 12' % n_item)
if seg7.count('timeline-desc') != 0:
    errs.append('S7 出现 timeline-desc')
dates7 = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', seg7)
if len(dates7) != 12:
    errs.append('S7 timeline-date 数 %d != 12' % len(dates7))
if dates7 != sorted(dates7, reverse=True):
    errs.append('S7 日期未降序: %r' % dates7)
for d in dates7:
    y, mo, dd = int(d[0:4]), int(d[5:7]), int(d[8:10])
    if date(y, mo, dd) < CUTOFF:
        errs.append('S7 超 T-14: %s' % d)
titles7 = re.findall(r'<div class="timeline-title">([^<]+)</div>', seg7)
for t in titles7:
    if len(t) > 25:
        errs.append('S7 标题超25字(%d): %s' % (len(t), t))

# --- 全文件 date-tag T-14 ---
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
    mo, dd = int(m.group(1)), int(m.group(2))
    if date(TODAY.year, mo, dd) < CUTOFF:
        errs.append('date-tag 超 T-14: %02d-%02d' % (mo, dd))

# --- 黑名单（全文件） ---
BAD = ['so.html5.qq.com', 'toutiao', '企鹅号', '网易号', '搜狐号',
       'stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com']
for b in BAD:
    if b in src:
        errs.append('黑名单命中: %s' % b)

if errs:
    print('\n❌ Phase1 断言失败，未写文件：')
    for e in errs:
        print('   -', e)
    sys.exit(1)

# ============================================================
# 写文件
# ============================================================
open(HTML, 'w', encoding='utf-8', newline='').write(src)
print('\n✅ 写入完成')
print('div %d/%d -> %d/%d' % (open_count_orig, close_count_orig, op, cl))
print('S0 cards = 4 | S1 = 6 | S2 = 4 | S7 = 12')
