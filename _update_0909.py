# -*- coding: utf-8 -*-
"""daily-update 2026-09-09 —— 两阶段：Phase1 全套断言通过后才写文件"""
import re, sys, shutil
from datetime import date, timedelta

P = 'index.html'
s = open(P, encoding='utf-8').read()
ORIG_OPEN = len(re.findall(r'<div\b', s))
ORIG_CLOSE = s.count('</div>')
TODAY = date(2026, 9, 9)
T14 = TODAY - timedelta(days=14)

print('=== baseline ===')
print('open', ORIG_OPEN, 'close', ORIG_CLOSE, 'bal', ORIG_OPEN - ORIG_CLOSE)

# ---------------- 1. header 数据区间 ----------------
upper = TODAY.strftime("%Y.%m.%d")
lower = (TODAY - timedelta(days=14)).strftime("%Y.%m.%d")
BADGE = "📅 数据区间：%s — %s（每日更新）" % (lower, upper)
s2, n = re.subn(r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）", BADGE, s)
assert n == 1, 'header badge 替换次数 %d' % n
assert BADGE in s2
print('[1] header badge ->', BADGE)
s = s2

# ---------------- 2. Stats Bar 沪指卡 ----------------
OLD_ST = '''    <div class="stat-card">
      <div class="stat-number">3932.70</div>
      <div class="stat-label">沪指9-7收盘·涨0.07%·两市成交1.95万亿·创业板涨3.41%</div>
      <div class="stat-change up">▲ 深成指+1.91%·创业板+3.41%·科创50涨2.42%</div>
    </div>'''
NEW_ST = '''    <div class="stat-card">
      <div class="stat-number">3940.55</div>
      <div class="stat-label">沪指9-8收盘·涨0.20%·两市成交1.96万亿·创业板跌1.15%</div>
      <div class="stat-change up">▲ 超3400只个股上涨·农业有色领涨·科技回调</div>
    </div>'''
assert s.count(OLD_ST) == 1, 'stats 沪指卡锚点 %d' % s.count(OLD_ST)
s = s.replace(OLD_ST, NEW_ST)
print('[2] stats bar 沪指卡 -> 3940.55 (09-08收盘)')

# ---------------- 3. S0 整块替换 ----------------
S0_HEAD = '<!-- S0 Card 1'
S1_MARK = '<!-- ============ Section 1: 重磅信息 ============ -->'
i0 = s.find(S0_HEAD)
i1 = s.find(S1_MARK)
assert i0 > 0 and i1 > i0
S0_TAIL = s[i1 - len('    </div>\n  </div>\n\n'):i1]
assert S0_TAIL == '    </div>\n  </div>\n\n', repr(S0_TAIL)

A = 'href="%s" target="_blank" style="color:#1890ff;text-decoration:none;"'

S0_C1 = '''<!-- S0 Card 1 (09-09 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批8只北交所三个月持有期主题基金获批·锁定期由两年大幅缩短</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-09</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月9日（记者陈玥）：9月8日，首批8只北交所三个月持有期主题基金获批，管理人包括华夏、汇添富、易方达、南方、嘉实、东财、富国、中信建投8家。该批产品于7月24日上报，为主动管理型开放式基金，投资者买入并持有满3个月即可自由赎回，锁定期较首批两年定开产品大幅缩短。<br>
          <b>政策背景：</b>此次获批是落实证监会《关于高质量建设北京证券交易所的意见》中"持续丰富产品体系"要求的举措，旨在拓宽增量资金入市渠道、提升北交所市场活跃度、助力创新型中小企业估值修复。<br>
          <b>北交所五年数据：</b>截至2026年9月1日，上市公司由开市之初81家扩容至339家（4倍以上），总市值由不足3000亿增至超8500亿元，合格投资者由402万户增至超1100万户，日均成交额由不足10亿元跃升至超200亿元，国家级专精特新"小巨人"占比由不足五成升至超六成。<br>
          <b>对腾安启示：</b>三个月持有期显著提升产品对个人投资者的适配性，北交所主题基金有望成为四季度代销增量品类；建议提前准备北交所主题选品对比、投资者适当性提示与投教素材，最快下周即有产品启动募集。
        </div>
        <div class="card-footer">
          <a ''' + (A % 'https://www.cnstock.com/commonDetail/787398') + '''><span class="source-tag">上海证券报·09-09</span></a>
        </div>
      </div>

'''

S0_C2 = '''      <!-- S0 Card 2 (09-09 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 本周48只新基金启动发行·被动指数占47.92%·年内新基首尾业绩差超100个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-09</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月9日（记者郝健）：本周（9月7日—13日）全市场共48只新基金启动发行。类型上被动指数型23只占47.92%稳居主力，固收类14只（债券型8只、偏债混合6只）占29.17%，另有FOF 3只、普通股票型3只、增强指数2只、偏股混合2只、REITs 1只。<br>
          <b>主题分布：</b>金融科技4只（建信/景顺长城/华泰柏瑞同推创业板金融科技ETF、万家布局中证金融科技ETF），算力与AI方向3只（国泰/南方创业板算力基础设施ETF、华泰柏瑞科创创业AI ETF联接），卫星产业2只（平安/南方），粮食产业成新热点（南方、易方达发行国证粮食产业ETF联接，永赢发行国证粮食产业ETF），消费方向有朱雀消费动力、中欧消费新机遇。<br>
          <b>发行与业绩：</b>上周（8月31日—9月6日）82只新基进入发行期创单周新高；截至9月8日，三季度以来共成立基金335只，较2025年同期增长10.2%。但今年成立的新基金业绩显著分化，首尾差距超过100个百分点，科技主题内部冷热不均、新能源主题承压。<br>
          <b>对腾安启示：</b>被动指数供给持续井喷，同主题多只产品同发已成常态，货架选品须以跟踪误差、费率、流动性为核心建立对比机制；同时须强化"新基金业绩分化"的投资者预期管理。
        </div>
        <div class="card-footer">
          <a ''' + (A % 'https://www.cnfin.com/gs-lb/detail/20260909/4467191_1.html') + '''><span class="source-tag">新华财经·09-09</span></a>
        </div>
      </div>

'''

S0_C3 = '''      <!-- S0 Card 3 (09-08 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 瑞银基金销售按下暂停键·年内10家公募终止合作·代销尾部机构加速出清</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-08</span>
          </div>
        </div>
        <div class="card-body">
          9月8日大成基金公告，自9月30日起终止与瑞银基金销售（深圳）有限公司的基金销售业务合作；此前9月7日前海开源基金、摩根基金已先后公告将于9月21日起终止全部合作（前海开源另披露自9月14日起终止销售业务合作）。至此年内已有10家公募与这家瑞银集团全资持股的销售机构"分手"。<br>
          <b>处置安排：</b>投资者须于9月11日15:00前主动办理份额转托管或赎回；逾期未处理的，管理人将自动为其开立直销账户并将存量份额迁移至直销平台，投资者需补充完善身份验证与资料后方可查询、赎回或转换——份额数量不变、仅变更管理平台。<br>
          <b>出清背景：</b>瑞银基金销售成立于2018年、落户深圳前海，2022年推出亚太区首个数字化财富平台"瑞富众App"。今年以来中证金牛（北京）、浦领基金、凯石财富等多家销售机构已宣布关停。业内指向年初实施的基金销售新规——股混基金销售服务费由0.6%/年降至0.4%/年、指数与债券型由0.4%降至0.2%、货基由0.25%降至0.15%，叠加直销免认申购费形成双重挤压。<br>
          <b>对腾安启示：</b>独立第三方代销尾部机构正被费率改革加速出清，头部保有规模反而集中；须同步排查存量合作渠道的经营持续性，并提前准备份额迁移类客诉与投教话术。
        </div>
        <div class="card-footer">
          <a ''' + (A % 'https://new.qq.com/rain/a/20260908A08QNZ00') + '''><span class="source-tag">腾讯新闻·09-08</span></a>
        </div>
      </div>

'''

S0_C4 = '''      <!-- S0 Card 4 (09-09 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募权益基金仓位94.15%维持高位·有色金属逆势获主动增持</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-09</span>
          </div>
        </div>
        <div class="card-body">
          新华财经上海9月9日电：好买基金研究中心数据显示，截至9月4日公募权益类基金整体仓位94.15%，较前一周微降0.01个百分点，仍处历史中高位——普通股票型由94.74%升至94.75%，偏股混合型由94.03%降至94.01%，整体较一个月前的93.94%上升0.21个百分点。<br>
          <b>行业腾挪：</b>电子仍为第一大重仓行业；有色金属配置比例由5.47%升至5.50%，同期行业指数下跌5.01%，剔除涨跌影响后主动增持幅度达0.15个百分点，在申万一级行业中仅次于电子。二季度末基金等权口径有色配置4.95%，高于2025年中报4.84%、2024年年报3.56%。<br>
          <b>机构观点：</b>广发基金姚曦认为有色行情由商品价格与企业业绩双轮驱动——海外铜价金价强势，国内龙头矿企半年报业绩集中兑现，涨价正由商品价格传导至利润端。招商基金提示工业金属仍有低库存与供应扰动支撑但需观察下游需求；博时基金王祥提示贵金属短期受美债收益率、美元走势与美联储政策预期主导，波动加大。<br>
          <b>对腾安启示：</b>权益仓位高位运行叠加结构性调仓，有色/资源主题基金的阶段表现与波动同步放大，代销端应做好主题基金的波动预期提示与分散配置引导。
        </div>
        <div class="card-footer">
          <a ''' + (A % 'https://m.cnfin.com/gs-lb//zixun/20260909/4467050_1.html') + '''><span class="source-tag">新华财经·09-09</span></a>
        </div>
      </div>

'''

s = s[:i0] + S0_C1 + S0_C2 + S0_C3 + S0_C4 + S0_TAIL + s[i1:]
print('[3] S0 4 卡已替换')

# ---------------- 3b. S0 section-context ----------------
OLD_CTX = '<span class="section-context">9月8日 · 4条今日要闻</span>'
NEW_CTX = '<span class="section-context">9月9日 · 4条今日要闻</span>'
assert s.count(OLD_CTX) == 1, 'context 锚点 %d' % s.count(OLD_CTX)
s = s.replace(OLD_CTX, NEW_CTX)
print('[3b] S0 context ->', NEW_CTX)

# ---------------- 4. S2：删 08-25 过期卡 + 新增 09-07 中基协失联公告卡 ----------------
S3_MARK = '<!-- ============ Section 3: 竞争对手动态 ============ -->'
i3 = s.find(S3_MARK)
assert i3 > 0
dt0825 = s.find('<span class="date-tag">08-25</span>')
assert dt0825 > 0, '未找到 08-25 date-tag'
card_start = s.rfind('      <div class="card p1">', 0, dt0825)
assert card_start > 0 and card_start > s.find('监管政策动态'), '08-25 卡起点定位异常'
assert card_start < i3

NEW_S2 = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-07</span>
          </div>
          <div class="card-title">🔴 中基协点名9家"断联"私募·年内注销管理人已达858家·失联处置进入快车道</div>
        </div>
        <div class="card-body">
          中国证券投资基金业协会9月7日发布公告（中基协字〔2026〕296号，落款9月4日）：协会通过AMBERS系统登记的电话、电子邮件、短信等方式，无法与江西福乐投资、上海胤狮私募、北京金石致远投资、北京象渊私募、上海玖时私募、深圳力拓睿合、河北秦魏投资、北京金石致远资产、杭州迅动资产等9家私募基金管理人取得有效联系。<br>
          <b>处置流程：</b>上述机构须自公告发布之日起5个工作日内通过AMBERS系统提交情况报告；逾期将被认定失联并在官网失联机构专栏公示、于"机构诚信信息"栏标识；公示满一个月仍未完成的，协会将依据《私募基金管理人失联处理指引》注销其管理人登记。<br>
          <b>与信披新规联动：</b>9月1日施行的《私募投资基金信息披露监督管理办法》第二十八条明确，托管人履职中发现管理人涉嫌侵占、挪用或失联等情形的，须及时向基金业协会及注册地证监局报告——本次批量"点名"是新规落地后的首批执行案例。<br>
          <b>出清数据：</b>今年4月30日协会注销第47批失联私募12家、7月24日再注销9家；据中基协官网统计，截至9月8日年内注销私募基金管理人已达858家。本次名单中多家机构名下产品仍在运作，个别曾现身A股公司前十大流通股东。<br>
          <b>对腾安启示：</b>私募代销须强化管理人存续状态与诚信信息的日常监控，对进入失联公示程序的机构产品提前做好份额处置与客户沟通预案。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a ''' + (A % 'https://www.amac.org.cn/zlgl/sljg/sljgclgg/202609/t20260907_28070.html') + '''><span class="source-tag">中国基金业协会·09-07</span></a>
        </div>
      </div>

    </div>
  </div>
'''
s = s[:card_start] + NEW_S2 + s[i3:]
print('[4] S2 删 08-25 过期卡 + 新增 09-07 中基协失联公告卡')

# ---------------- 5. S6 行情卡替换 ----------------
S6_MARK = '<!-- ============ Section 6: 市场行情速览 ============ -->'
S7_MARK = '<!-- ============ Section 7: 关键时间线 ============ -->'
i6 = s.find(S6_MARK); i7 = s.find(S7_MARK)
assert i6 > 0 and i7 > i6
c6 = s.find('<div class="card p3">', i6)
assert c6 > 0 and c6 < i7
OLD_S6_O = len(re.findall(r'<div\b', s[c6:i7]))
OLD_S6_C = s[c6:i7].count('</div>')

NEW_S6 = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-08）·沪指3940.55 +0.20%·创业板指跌1.15%·成交1.96万亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-08</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-08收盘·周期股走强）</b><br>
              上证指数 <b>3940.55</b> <span style="color:#f5222d;">+0.20%</span><br>
              深证成指 <b>13703.21</b> <span style="color:#52c41a;">-0.52%</span><br>
              创业板指 <b>3359.72</b> <span style="color:#52c41a;">-1.15%</span><br>
              科创综指 <b>1880.10</b> <span style="color:#52c41a;">-1.09%</span><br>
              沪深两市成交 <b>1.96万亿</b>·超3400只个股上涨·74股涨停<br>
              农业掀涨停潮·铜板块发力·半导体消费电子回调
            </div>
            <div>
              <b>港股与美股（09-08收盘）</b><br>
              恒生指数 <b>25317.18</b> <span style="color:#52c41a;">-0.38%</span><br>
              恒生科技 <b>4454.85</b> <span style="color:#52c41a;">-1.61%</span><br>
              国企指数 <b>8397.32</b> <span style="color:#52c41a;">-0.38%</span><br>
              道琼斯 <b>52786.07</b> <span style="color:#52c41a;">-1.18%</span><br>
              纳斯达克 <b>26421.41</b> <span style="color:#52c41a;">-0.32%</span><br>
              标普500 <b>7673.52</b> <span style="color:#52c41a;">-0.58%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:8px;border-top:1px solid #f0f0f0;">
              <b>结构焦点：</b>9月8日A股风格再度切换，农业、有色等周期板块走强带动沪指飘红，半导体等科技题材下挫拖累双创指数收跌——沪指涨0.20%报3940.55，深成指跌0.52%、创业板指跌1.15%、科创综指跌1.09%，沪深两市合计成交19604亿元；全市场超3400只个股上涨、74只涨停，农业板块掀涨停潮（中粮科技、亚盛集团等多股涨停），LME铜价创历史新高推动铜板块拉升，化肥、煤化工涨幅领先；电力设备、电子、计算机跌幅居前。港股9月8日三大指数集体走弱，恒指跌0.38%报25317.18、恒生科技跌1.61%、国企指数跌0.38%，主板成交2061.7亿港元，南向资金净流入61.28亿港元。美股9月8日全线收跌，道指重挫628.18点跌1.18%报52786.07、标普500跌0.58%、纳指跌0.32%，芯片股逆势爆发（费城半导体指数涨1.3%、英特尔涨9.05%、AMD涨5.9%），主因中东局势升级推升油价、加剧通胀担忧。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-09-08收盘</span>
            <span class="source-tag">数据来源：新华社/上海证券报/国际金融报（09-08）</span>
          </div>
      </div>  </div>
'''
NEW_S6_O = len(re.findall(r'<div\b', NEW_S6))
NEW_S6_C = NEW_S6.count('</div>')
assert (OLD_S6_O, OLD_S6_C) == (NEW_S6_O, NEW_S6_C), \
    'S6 div 不匹配 old(%d,%d) new(%d,%d)' % (OLD_S6_O, OLD_S6_C, NEW_S6_O, NEW_S6_C)
s = s[:c6] + NEW_S6 + s[i7:]
print('[5] S6 更新为 09-08 收盘（div %d/%d）' % (NEW_S6_O, NEW_S6_C))

# ---------------- 6. S7 时间线整块替换 ----------------
i7b = s.find(S7_MARK)
t_start = s.find('<div class="timeline-item">', i7b)
assert t_start > 0
T_END = '    </div>\n\n  </div>\n\n</div>\n\n'
t_end = s.find(T_END, t_start)
assert t_end > t_start, 'S7 尾锚未找到'

def item(d, title):
    return ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot red"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>\n' % (d, title))

S7 = [
    ('2026-09-09', '首批8只北交所三个月持有期基金获批'),
    ('2026-09-09', '公募权益仓位94.15%·有色获增持'),
    ('2026-09-09', '瑞银基金销售暂停·10家公募终止合作'),
    ('2026-09-08', '首批18只主动ETF获批在即·10月集中募集'),
    ('2026-09-08', '公募定增获配473.46亿·增168.71%'),
    ('2026-09-07', '证监会就私募募集办法公开征求意见'),
    ('2026-09-07', '个人养老金扩容“固收+”赛道'),
    ('2026-09-06', '下周44只新基金启动发售'),
    ('2026-09-05', '首批10家基金上报科创债场外指数基金'),
    ('2026-09-04', 'A股放量下跌·沪指3930.12收跌0.30%'),
    ('2026-09-04', '单周82只新基金启动发行·创单周纪录'),
    ('2026-09-03', '交易外接新规落地·中证协中基协联合发布'),
]
new_s7 = '\n'.join(item(d, t) for d, t in S7)
s = s[:t_start] + new_s7 + s[t_end:]
print('[6] S7 重写为 %d 条' % len(S7))

# ================= Phase1 断言 =================
print('\n=== Phase1 断言 ===')
o = len(re.findall(r'<div\b', s)); c = s.count('</div>')
print('div open %d close %d bal %d (drift open %+d / close %+d)' %
      (o, c, o - c, o - ORIG_OPEN, c - ORIG_CLOSE))
assert o == c, 'div 失衡 %d/%d' % (o, c)
assert (o - ORIG_OPEN) == 0, 'div 总数漂移 %+d（预期 0）' % (o - ORIG_OPEN)

assert 'Section 8' not in s and '待办跟踪' not in s and '腾安行动清单' not in s
print('S8 不存在 ✓')

assert '\ufffd' not in s
print('U+FFFD 零残留 ✓')

# S0 校验
s0 = s[s.find('<!-- S0 Card 1'):s.find(S7_MARK)]
s0 = s0[:s0.find(S1_MARK)] if S1_MARK in s0 else s0
s0 = s[s.find('<!-- S0 Card 1'):s.find('<!-- ============ Section 1')]
n_s0 = s0.count('<div class="card p')
print('S0 卡数', n_s0)
assert n_s0 == 4, 'S0 卡数 %d' % n_s0
st = re.search(r'<span class="section-title">([^<]*)</span>', s[:s.find(S1_MARK)][-3000:])
titles = re.findall(r'<span class="section-title">([^<]*)</span>', s)
# S0 的 title 是第 2 个（第 1 个是 header? 实际 header 无 section-title）
s0_title = re.findall(r'<span class="section-title">([^<]*)</span>',
                      s[s.find('Section 0: 今日焦点'):s.find('Section 1: 重磅信息')])
assert s0_title == ['今日焦点'], 'S0 title %s' % s0_title
print('S0 title 精确「今日焦点」✓')
ctx = re.findall(r'<span class="section-context">([^<]*)</span>', s)
assert ctx[0] == '9月9日 · 4条今日要闻', 'context %s' % ctx[0]
print('S0 context', ctx[0], '✓')
s0_dates = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s0)
print('S0 date-tags', s0_dates)
for mm, dd in s0_dates:
    assert date(2026, int(mm), int(dd)) >= date(2026, 9, 8), 'S0 过期 %s-%s' % (mm, dd)
assert s0_dates.count(('09', '09')) >= 3, 'S0 T+0 不足 3 条'
assert s0.count('card-meta') == 4, 'card-meta %d' % s0.count('card-meta')
assert s0.count('source-tag') == 4, 'S0 出处 %d' % s0.count('source-tag')
print('S0 结构/出处/时效 ✓')
assert 'action-box' not in s0, 'S0 无 P0 不应有 action-box'
print('S0 无 P0 无 action-box ✓')

# S1 / S2
def seg(a, b):
    return s[s.find(a):s.find(b)]
s1 = seg('<!-- ============ Section 1: 重磅信息 ============ -->', '<!-- ============ Section 2')
s2s = seg('<!-- ============ Section 2: 监管政策 ============ -->', '<!-- ============ Section 3')
n_s1 = len(re.findall(r'<div class="card p\d">', s1))
n_s2 = len(re.findall(r'<div class="card p\d">', s2s))
print('S1 卡数', n_s1, '| S2 卡数', n_s2)
assert n_s1 == 6 and n_s2 == 4, 'S1/S2 数量异常'
for mm, dd in re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s1 + s2s):
    assert date(2026, int(mm), int(dd)) >= T14, 'S1/S2 过期 %s-%s' % (mm, dd)
print('S1/S2 均在 T-14 内 ✓')

# S7
s7 = seg('<!-- ============ Section 7: 关键时间线 ============ -->', '</body>')
n_t = s7.count('<div class="timeline-item">')
dts = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', s7)
ttl = re.findall(r'<div class="timeline-title">([^<]+)</div>', s7)
print('S7 条目', n_t, '日期', len(dts))
assert n_t == len(dts) == len(ttl) == 12, 'S7 结构 %d/%d/%d' % (n_t, len(dts), len(ttl))
assert 'timeline-desc' not in s7
for d in dts:
    assert date(*map(int, d.split('-'))) >= T14, 'S7 过期 %s' % d
for t in ttl:
    assert len(t) <= 25, 'S7 标题超 25 字：%s(%d)' % (t, len(t))
print('S7 结构/时效/标题长度 ✓')

# 全文件 date-tag
bad = [(m, d) for m, d in re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s)
       if date(2026, int(m), int(d)) < T14]
assert not bad, '全文件过期 date-tag %s' % bad
print('全文件 date-tag 均 ≥ T-14(%s) ✓' % T14)

# 黑名单 + D 级
NEW_SEG = s[s.find('<!-- S0 Card 1'):s.find('<!-- ============ Section 3')] + s7
for pattern in ['so.html5.qq.com', 'toutiao', '企鹅号', '网易号', '搜狐号',
                'stcn.com', 'cls.cn', '21jingji.com', 'yicai.com']:
    assert pattern not in NEW_SEG, '本轮新增段命中 D 级/黑名单：%s' % pattern
print('新增段无 D 级/黑名单信源 ✓')

# Stats Bar 口径
assert '3940.55' in s and '9-8收盘' in s
print('Stats Bar 沪指口径 = 09-08 收盘 ✓')

# 写文件
shutil.copy(P, P + '.bak0909')
open(P, 'w', encoding='utf-8').write(s)
print('\n=== 写入完成 ===')
print('final div', len(re.findall(r'<div\b', s)), s.count('</div>'))
