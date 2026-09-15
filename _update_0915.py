# -*- coding: utf-8 -*-
"""daily-update 2026-09-15 — 基金行业资讯看板"""
import re, sys
from datetime import date, timedelta

P = 'index.html'
src = open(P, encoding='utf-8').read()
orig = src
O0, C0 = src.count('<div'), src.count('</div>')
print('baseline div open/close:', O0, C0)

TODAY = date(2026, 9, 15)
T14 = TODAY - timedelta(days=14)
print('TODAY', TODAY, 'T-14 boundary', T14)

# ============ STEP 1: marker（第一步，最高优先级） ============
new_marker = '<!-- daily-update: 2026-09-15 -->'
assert src.count('<!-- daily-update: 2026-09-14 -->') == 1, 'marker anchor not unique'
src = src.replace('<!-- daily-update: 2026-09-14 -->', new_marker)
assert new_marker in src
print('[1] marker ->', new_marker)

# ============ STEP 2: header 数据区间（动态计算） ============
upper = TODAY.strftime('%Y.%m.%d')
lower = T14.strftime('%Y.%m.%d')
badge_new = f'\U0001F4C5 数据区间：{lower} — {upper}（每日更新）'
pat = re.compile(r'\U0001F4C5 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
assert len(pat.findall(src)) == 1, 'badge anchor not unique'
src = pat.sub(lambda m: badge_new, src)
assert badge_new in src
print('[2] badge ->', badge_new)

# ============ STEP 3: S0 整块替换 ============
A_S0 = src.index('      <!-- S0 Card 1 (09-14 P0) -->')
I_S1 = src.index('<!-- ============ Section 1: 重磅信息 ============ -->')
END = '    </div>\n  </div>\n'
B_S0 = src.rindex(END, A_S0, I_S1)
assert B_S0 > A_S0
removed_s0 = src[A_S0:B_S0]

CARDS = (
    # ---------- Card 1 (P0, 09-15) ----------
    '      <!-- S0 Card 1 (09-15 P0) -->\n'
    '      <div class="card p0">\n'
    '        <div class="card-top">\n'
    '          <div class="card-title">\U0001F534 中国结算整合发布公募登记数据交换平台指引·9月11日施行·三份旧规同步废止</div>\n'
    '          <div class="card-meta">\n'
    '            <span class="priority-tag urgent">P0 紧急必看</span>\n'
    '            <span class="date-tag">09-15</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-body">\n'
    '          证券日报9月15日报道（记者彭衍菘）：中国证券登记结算有限责任公司整合制定《中国证券登记结算有限责任公司公募基金行业注册登记数据中央交换平台运作指引》（下称《指引》），<b>自9月11日起施行</b>，中国结算此前发布的三份相关业务文件同步废止。当前公募基金规模已接近<b>40万亿元</b>，基金产品日益丰富、销售渠道更加多元，对登记业务的数据交互、业务处理和运行效率提出更高要求。<br>\n'
    '          <b>规范范围：</b>《指引》围绕公募基金行业注册登记数据中央交换平台，对平台参与人管理、数据交换、集中备份、监督对账、互认基金参数报送、概要转发、数据查询及推送等业务作出具体规范；并把互认基金参数报送、基金产品资料概要转发纳入统一框架，明确通过<b>基金E账户App</b>等渠道向自然人投资者提供本人基金账户及相关持仓信息查询服务。<br>\n'
    '          <b>销售机构相关：</b>《指引》明确份额登记机构应于<b>T+1日21:00前</b>将T日备份数据报送至平台，每日报送增量备份数据、并适时报送全量备份数据；平台对数据进行格式检查，检查不合格的由发送方及时补正。销售资金监督对账机制下，平台根据<b>销售机构申请</b>向监督机构转发相关公募基金业务数据，监督机构按规报送基金销售结算资金等数据，通过不同主体数据的一致性核对加强对销售结算资金流转的监督。<br>\n'
    '          <b>行业评价：</b>晨星（中国）基金研究中心总监孙珩表示，统一的平台和规范有助于减少机构之间重复开发、逐一对接以及人工核验的工作量；苏商银行特约研究员武泽伟认为，集中备份与监督对账有助于进一步强化数据留痕和核验能力。<br>\n'
    '          <b>对腾安启示：</b>《指引》已生效，销售机构需确认与份额登记机构、销售结算资金监督机构之间的数据报送与对账链路是否按新口径运行，重点核查报送时限、格式检查不合格的补正流程与留痕。\n'
    '        </div>\n'
    '        <div class="card-footer">\n'
    '          <a href="https://finance.china.com.cn/money/fund/20260915/6324298.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·中国网财经·09-15</span></a>\n'
    '          <span class="impact-tag high">影响：高</span>\n'
    '        </div>\n'
    '        <div class="action-box">\n'
    '          <div class="action-label">⚡ 腾安行动建议</div>\n'
    '          <div class="action-text">\n'
    '            ① 口径核对→对照《指引》核查腾安作为销售机构在中央交换平台的参与人登记、数据报送与对账接口是否符合新规；<br>\n'
    '            ② 时限排查→确认份额登记机构 T+1 21:00 前的报送链路无延迟，建立格式检查不合格数据的补正闭环与留痕台账；<br>\n'
    '            ③ 对账复核→与监督机构核对基金销售结算资金数据一致性，异常项建立"发现—复核—整改"记录以备检查。\n'
    '          </div>\n'
    '        </div>\n'
    '      </div>\n\n\n'
    # ---------- Card 2 (P1, 09-15) ----------
    '      <!-- S0 Card 2 (09-15 P1) -->\n'
    '      <div class="card p1">\n'
    '        <div class="card-top">\n'
    '          <div class="card-title">\U0001F7E1 主动权益基金业绩首尾差超210个百分点·权益仓位94.12%·超2000只近一年负收益</div>\n'
    '          <div class="card-meta">\n'
    '            <span class="priority-tag important">P1 重要关注</span>\n'
    '            <span class="date-tag">09-15</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-body">\n'
    '          上海证券报9月15日报道（记者陈玥）：Choice数据显示，截至2026年9月11日，普通股票型基金、偏股混合型基金与灵活配置型基金<b>近一年业绩首尾相差已超过210个百分点</b>。截至9月11日，三类基金近一年平均回报分别为6.93%、6.52%和7.59%；有24只产品近一年净值增长率超过100%，其中易方达供给改革混合与易方达产业机遇混合分别达<b>165.6%</b>和<b>157.43%</b>，9只产品超过120%，今年以来几乎全部重仓科技方向；与此同时<b>超过2000只</b>主动权益类基金近一年净值增长率为负。<br>\n'
    '          <b>仓位与配置：</b>好买基金数据显示，9月7日至11日公募权益类基金整体仓位下降0.03个百分点至<b>94.12%</b>（普通股票型94.75%、偏股混合型93.98%），总体处于历史中位偏高水平。配置比例居前三的申万一级行业为电子（30.28%）、通信（9.91%）、医药生物（8.41%）；当周主要增持医药生物、非银金融与电力设备，主要减持通信、电子与建筑材料。<br>\n'
    '          <b>机构态度：</b>沪上一家中大型基金公司权益投资负责人表示，"市场正在选择方向，但我们并不悲观"，在市场韧性与确定的产业趋势下需要多一分定力与耐心；南方基金认为后续重点关注FOMC会议结果及利率路径指引，若美联储政策并未超预期收紧，A股超跌成长板块存在修复空间。<br>\n'
    '          <b>对腾安启示：</b>首尾差扩大意味着"选基"风险显著高于"选市"，基金列表与榜单页应同步展示近一年回报分位、最大回撤与行业集中度，弱化单纯按收益率排序的引导。\n'
    '        </div>\n'
    '        <div class="card-footer">\n'
    '          <a href="https://www.cnstock.com/commonDetail/790197" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-15</span></a>\n'
    '          <span class="impact-tag medium">影响：中</span>\n'
    '        </div>\n'
    '      </div>\n\n\n'
    # ---------- Card 3 (P1, 09-15) ----------
    '      <!-- S0 Card 3 (09-15 P1) -->\n'
    '      <div class="card p1">\n'
    '        <div class="card-top">\n'
    '          <div class="card-title">\U0001F7E1 ETF资金"大进大出"成常态·规模先抑后扬至4.9万亿·倒逼运作管理升级</div>\n'
    '          <div class="card-meta">\n'
    '            <span class="priority-tag important">P1 重要关注</span>\n'
    '            <span class="date-tag">09-15</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-body">\n'
    '          上海证券报9月15日报道（记者何漪）：今年以来A股结构性分化显著、热点板块快速轮动，ETF资金流向因此呈现高频波动，整体规模走出<b>"先抑后扬"</b>曲线。Choice数据显示，截至6月末ETF规模从去年末的<b>6.02万亿元</b>回落至<b>4.75万亿元</b>，降幅超过两成；下半年市场风格快速切换、资金持续流入，截至9月初ETF规模回升至<b>4.9万亿元</b>。<br>\n'
    '          <b>份额波动：</b>截至9月11日，今年以来沪深300ETF华泰柏瑞、沪深300ETF华夏的基金份额均下降逾七成，金融ETF国泰、科创创业人工智能ETF鹏华份额降幅均超过七成；短期看，数百只ETF的单周基金份额波动率超过5%，资金买卖频率较高。<br>\n'
    '          <b>结构分化：</b>瑞银证券中国股票策略分析师孟磊分析，宽基指数ETF规模在上半年回落后企稳回升，科技相关主题产品推动行业与主题ETF规模持续提升；景顺长城基金研究显示，股票型ETF以机构投资者为主导，个人投资者则成为撑起ETF新发市场的核心力量。<br>\n'
    '          <b>运作挑战：</b>业内人士表示，资金大进大出迫使管理人在短时间内大规模买卖成分股、调整持仓结构，交易冲击成本上升并易造成跟踪误差阶段性扩大；极端行情下，部分需要现金替代的全市场ETF可能面临流动性压力。多家基金公司正加大AI投入，用于申赎预测、风险识别与PCF参数优化。<br>\n'
    '          <b>对腾安启示：</b>ETF份额高频波动会放大客户短期申赎体验差异，产品页应补充份额变动、跟踪误差与流动性指标提示，避免把短期规模冲高解读为资金持续看好。\n'
    '        </div>\n'
    '        <div class="card-footer">\n'
    '          <a href="https://www.cnstock.com/commonDetail/790196" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-15</span></a>\n'
    '          <span class="impact-tag medium">影响：中</span>\n'
    '        </div>\n'
    '      </div>\n\n\n'
    # ---------- Card 4 (P2, 09-15) ----------
    '      <!-- S0 Card 4 (09-15 P2) -->\n'
    '      <div class="card p2">\n'
    '        <div class="card-top">\n'
    '          <div class="card-title">\U0001F535 5055只基金首披盈利投资者占比·中位数91.79%·83只满盈、8只定开为零</div>\n'
    '          <div class="card-meta">\n'
    '            <span class="priority-tag normal">P2 建议了解</span>\n'
    '            <span class="date-tag">09-15</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-body">\n'
    '          新华财经9月15日报道：2026年基金中报首次披露"盈利投资者数量占比"指标，统计区间为2025年7月1日至2026年6月30日。混合型与股票型基金中共有<b>5055只</b>产品披露该数据，占比中位数<b>91.79%</b>、平均数<b>78.14%</b>；2724只基金该指标大于等于90%，<b>83只</b>达到100%（主要为混合型，含银华基金、富国基金、广发基金旗下部分产品），同时有<b>8只</b>为0.00%，这8只全部为定期开放型基金。<br>\n'
    '          <b>背离样本：</b>949只基金该指标不足50%；净值回报超50%但盈利投资者占比不足50%的基金共<b>38只</b>——泰信发展主题近一年净值涨98.54%，盈利投资者占比仅26.02%。占比为0的产品中，信澳博见成长一年定开A区间回报-34.98%、跑输业绩比较基准超64个百分点，景顺长城集英成长两年定开区间回报-5.01%。<br>\n'
    '          <b>正向样本：</b>银华战略新兴灵活配置定期开放混合发起式近一年盈利投资者占比100%、区间回报131.99%，基金经理在中报中称上半年紧抓AI科技主线，并在业绩期阶段性参与业绩较好、估值较低的锂电板块。<br>\n'
    '          <b>对腾安启示：</b>该指标已纳入《推动公募基金高质量发展行动方案》考核体系，可作为产品页"持有体验"标签的量化基础；对净值涨幅高但盈利占比低的产品须加挂"择时风险"提示。\n'
    '        </div>\n'
    '        <div class="card-footer">\n'
    '          <a href="https://finance.sina.com.cn/roll/2026-09-15/doc-inirwfqk3975799.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·新浪财经·09-15</span></a>\n'
    '          <span class="impact-tag low">影响：中</span>\n'
    '        </div>\n'
    '      </div>\n\n\n'
)

src = src[:A_S0] + CARDS + src[B_S0:]

# 3b: section-context 单独改（整块替换不带 header）
old_ctx = '<span class="section-context">9月14日 · 4条今日要闻</span>'
new_ctx = '<span class="section-context">9月15日 · 4条今日要闻</span>'
assert src.count(old_ctx) == 1
src = src.replace(old_ctx, new_ctx)
print('[3] S0 replaced; context ->', new_ctx)

# ============ STEP 4: Stats Bar 沪指卡 ============
old_stat = (
    '      <div class="stat-number">3888.11</div>\n'
    '      <div class="stat-label">沪指9-11收盘·跌1.18%·全市场成交1.99万亿·较上日放量3248亿</div>\n'
    '      <div class="stat-change down">▼ 有色化工地产领跌·仅643只个股上涨</div>\n'
)
new_stat = (
    '      <div class="stat-number">3885.33</div>\n'
    '      <div class="stat-label">沪指9-14收盘·跌0.07%·全市场成交1.63万亿·较上日缩量3427亿</div>\n'
    '      <div class="stat-change down">▼ 创业板-1.10%·科创50-1.62%·超3100股上涨</div>\n'
)
assert src.count(old_stat) == 1, 'stats bar anchor fail'
sb = src.index('<div class="stats-bar">')
sb_end = src.index('</div>\n<div class="main">', sb)
assert '3888.11' in src[sb:sb_end]
src = src.replace(old_stat, new_stat)
sb2 = src.index('<div class="stats-bar">')
sb2_end = src.index('</div>\n<div class="main">', sb2)
assert '3888.11' not in src[sb2:sb2_end] and '3885.33' in src[sb2:sb2_end]
print('[4] stats bar 沪指卡 -> 3885.33 (09-14 收盘)')

# ============ STEP 5: S6 行情卡 ============
SEC6 = src.index('<!-- ============ Section 6: 市场行情速览 ============ -->')
A6 = src.index('            <div class="card p3">', SEC6)
B6 = src.index('      </div>  </div>\n', SEC6)
assert A6 < B6
removed_s6 = src[A6:B6]
print('   S6 old card chars', len(removed_s6))

S6_NEW = (
    '            <div class="card p3">\n'
    '        <div class="card-top">\n'
    '          <div class="card-title">\U0001F4C8 上一交易日收盘（2026-09-14）·沪指3885.33 -0.07%·全市场成交1.63万亿缩量3427亿</div>\n'
    '          <div class="card-meta">\n'
    '            <span class="priority-tag light">P3 知悉即可</span>\n'
    '            <span class="date-tag">09-14</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-body">\n'
    '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">\n'
    '            <div>\n'
    '              <b>A股（09-14收盘·缩量蓄势）</b><br>\n'
    '              上证指数 <b>3885.33</b> <span style="color:#52c41a;">-0.07%</span><br>\n'
    '              深证成指 <b>13384.57</b> <span style="color:#52c41a;">-0.64%</span><br>\n'
    '              创业板指 <b>3285.58</b> <span style="color:#52c41a;">-1.10%</span><br>\n'
    '              沪深300 <b>4480.08</b> <span style="color:#52c41a;">-0.67%</span><br>\n'
    '              科创50 <b>1528.27</b> <span style="color:#52c41a;">-1.62%</span><br>\n'
    '              全市场成交 <b>1.63万亿</b>·较上日缩量3427亿·连续多日低于2万亿<br>\n'
    '              超3100只个股上涨·PCB/CRO/MLCC逆势活跃\n'
    '            </div>\n'
    '            <div>\n'
    '              <b>港股与美股（09-14收盘）</b><br>\n'
    '              恒生指数 <b>24917.60</b> <span style="color:#dc2626;">+0.45%</span><br>\n'
    '              恒生科技 <b>4317.94</b> <span style="color:#52c41a;">-0.06%</span><br>\n'
    '              国企指数 <b>8284.58</b> <span style="color:#dc2626;">+0.46%</span><br>\n'
    '              道琼斯 <b>52421.20</b> <span style="color:#52c41a;">-0.29%</span><br>\n'
    '              纳斯达克 <b>26186.41</b> <span style="color:#52c41a;">-0.56%</span><br>\n'
    '              标普500 <b>7619.98</b> <span style="color:#52c41a;">-0.48%</span><br>\n'
    '              费城半导体指数 <span style="color:#52c41a;">-5.86%</span>·布伦特原油106.18美元 <span style="color:#dc2626;">+1.5%</span>·伦敦金现4298.46美元 <span style="color:#52c41a;">-1.13%</span>\n'
    '            </div>\n'
    '            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">\n'
    '              <b>结构焦点：</b>缩量蓄势、结构分化——指数小幅收跌但个股普涨，算力硬件（PCB方向）领涨，超声电子、中京电子、天通股份等多股涨停，培育钻石与MLCC同步走强；CRO概念活跃，近岸蛋白、万邦医药20%涨停，医药生物行业获主力资金净流入29.08亿元居首；粮食、旅游、煤炭、养殖业、国防军工跌幅居前。港股汽车与生物医药板块走强，广汽集团涨超8%。美股方面，AI硬件股集体下挫，费城半导体指数跌5.86%创7月1日以来最大跌幅，光通信与存储芯片领跌，网络安全股逆市大涨；美国10年期国债收益率盘中一度突破5%，为2023年10月以来首次。\n'
    '            </div>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="card-footer">\n'
    '          <span class="source-tag">同花顺iFind·2026-09-14收盘</span>\n'
    '          <span class="source-tag">数据来源：中国证券网/新华社/上海证券报（09-14—09-15）</span>\n'
    '        </div>\n'
)
src = src[:A6] + S6_NEW + src[B6:]
print('[5] S6 -> 09-14 收盘')

# ============ STEP 6: S7 时间线 ============
SEC7 = src.index('<!-- ============ Section 7: 关键时间线 ============ -->')
ITEM_RE = re.compile(r'      <div class="timeline-item">\n.*?      </div>\n', re.S)
items = ITEM_RE.findall(src[SEC7:])
assert len(items) == 12, f'S7 item count {len(items)} != 12'
print('[6] S7 items =', len(items))

DROP_TITLES = [
    '绩优基金主动降仓保收益',
    '公募布局白盒固收+·规模超2.28万亿',
    '两大主题ETF集中申报·18家',
    'A股放量调整·成交1.99万亿',
]
kept = []
dropped = []
for it in items:
    t = re.search(r'<div class="timeline-title">([^<]+)</div>', it).group(1)
    if t in DROP_TITLES:
        dropped.append(t)
    else:
        kept.append(it)
assert len(dropped) == 4, f'dropped {len(dropped)} != 4: {dropped}'
print('   dropped:', dropped)

def mk(dot, d, title):
    assert len(title) <= 25, f'title too long ({len(title)}): {title}'
    return (f'      <div class="timeline-item">\n'
            f'        <div class="timeline-dot {dot}"></div>\n'
            f'        <div class="timeline-date">{d}</div>\n'
            f'        <div class="timeline-title">{title}</div>\n'
            f'      </div>\n')

new_items = [
    mk('red', '2026-09-15', '中国结算发布公募登记数据交换指引'),
    mk('blue', '2026-09-15', '主动权益首尾业绩差超210个百分点'),
    mk('blue', '2026-09-15', 'ETF资金大进大出倒逼运作升级'),
    mk('blue', '2026-09-15', '盈利投资者占比中位数91.79%'),
] + kept

assert len(new_items) == 12, f'new S7 count {len(new_items)}'
dates = [re.search(r'timeline-date">(\d{4}-\d{2}-\d{2})', i).group(1) for i in new_items]
assert dates == sorted(dates, reverse=True), f'S7 not descending: {dates}'
assert all(date.fromisoformat(d) >= T14 for d in dates), f'S7 out of window: {dates}'

blk_start = src.index(items[0], SEC7)
blk_end = src.index(items[-1], SEC7) + len(items[-1])
src = src[:blk_start] + ''.join(new_items) + src[blk_end:]
print('   S7 new head dates:', dates[:5])

# ============ STEP 7: 删除 S4 过期卡（08-31 盈利投资者占比，已升格进 S0） ============
KEY = '基金中报首披"盈利投资者占比"'
assert src.count(KEY) == 1, f'S4 key count {src.count(KEY)}'


def card_bounds(s, idx):
    """从卡片内部某点回溯到 <div class="card pX"> 起点，再用嵌套深度扫描定位闭合"""
    a = s.rindex('<div class="card p', 0, idx)
    depth = 1  # 起点 div 自身已计入（09-15 修复：初值 0 会提前在 card-top 闭合处返回）
    pos = a
    while True:
        nxt_open = s.find('<div', pos + 1)
        nxt_close = s.find('</div>', pos + 1)
        if nxt_close == -1:
            raise RuntimeError('unbalanced')
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open
        else:
            depth -= 1
            pos = nxt_close
            if depth == 0:
                return a, pos + len('</div>')


ki = src.index(KEY)
a4, b4 = card_bounds(src, ki)
removed_s4 = src[a4:b4]
assert '08-31' in removed_s4, 'removed S4 card is not the 08-31 one'
src = src[:a4] + src[b4:]
print('[7] S4 删除过期卡 08-31 盈利投资者占比, len', len(removed_s4))

# ============ Phase1 断言 ============
O1, C1 = src.count('<div'), src.count('</div>')
exp_o = -(removed_s4.count('<div>') ) if False else None
# 预期漂移：仅 S4 删 1 张卡；S0/S6 为等量替换（结构一致）
drift_o = O1 - O0
drift_c = C1 - C0
rm_o = removed_s4.count('<div')
rm_c = removed_s4.count('</div>')
# S0/S6 替换为同构结构，其漂移单独算
add_o = CARDS.count('<div') - removed_s0.count('<div')
add_c = CARDS.count('</div>') - removed_s0.count('</div>')
add_o += S6_NEW.count('<div') - removed_s6.count('<div')
add_c += S6_NEW.count('</div>') - removed_s6.count('</div')
print(f'   div drift: open {O0}->{O1} ({drift_o:+d}), close {C0}->{C1} ({drift_c:+d})')
print(f'   expected : open {add_o - rm_o:+d}, close {add_c - rm_c:+d}')
print(f'   S0 delta {CARDS.count("<div") - removed_s0.count("<div"):+d}/'
      f'{CARDS.count("</div>") - removed_s0.count("</div>"):+d}; '
      f'S6 delta {S6_NEW.count("<div") - removed_s6.count("<div"):+d}/'
      f'{S6_NEW.count("</div>") - removed_s6.count("</div>"):+d}; '
      f'S4 removed {rm_o}/{rm_c}')

assert O1 == C1, f'div 不平衡 {O1}/{C1}'
assert drift_o == add_o - rm_o, f'open drift {drift_o} != expected {add_o - rm_o}'
assert drift_c == add_c - rm_c, f'close drift {drift_c} != expected {add_c - rm_c}'
assert 'S8' not in src and '待办跟踪' not in src and '腾安行动清单' not in src
assert src.count('</div>>') == 0, '游离 </div>>'
assert '\ufffd' not in src, 'U+FFFD'

# S0 断言
s0a = src.index('<!-- ============ Section 0: 今日焦点 ============ -->')
s0b = src.index('<!-- ============ Section 1: 重磅信息 ============ -->')
seg0 = src[s0a:s0b]
assert seg0.count('<span class="section-title">今日焦点</span>') == 1
assert seg0.count(new_ctx) == 1
assert seg0.count('<div class="card p') == 4, f'S0 cards {seg0.count("<div class=\"card p")}'
assert seg0.count('<span class="date-tag">09-15</span>') == 4, 'S0 date-tag 09-15 != 4'
# 本日 S0 含 1 张 P0 卡 → 'action-box' 字面量出现 1 次（class="action-box"）
assert seg0.count('action-box') == 1, f'S0 action-box {seg0.count("action-box")}'
assert seg0.count('腾安行动建议') == 1
assert seg0.count('<a href=') == 4, f'S0 links {seg0.count("<a href=")}'
assert seg0.count('card-meta') == 4
for bad in ['stcn.com', 'cls.cn', '21jingji', 'yicai.com', 'toutiao', 'so.html5.qq.com',
            '163.com/dy', 'weibo.com', 'k.sina.com.cn', 'jrj.com.cn']:
    assert bad not in seg0, f'S0 命中黑名单 {bad}'

# S1/S2 数量与时效
s1a = src.index('<!-- ============ Section 1: 重磅信息 ============ -->')
s2a = src.index('<!-- ============ Section 2: 监管政策 ============ -->')
s3a = src.index('<!-- ============ Section 3: 竞争对手动态 ============ -->')
seg1, seg2 = src[s1a:s2a], src[s2a:s3a]
assert seg1.count('<div class="card p') == 6, f'S1 {seg1.count("<div class=\"card p")}'
assert seg2.count('<div class="card p') == 4, f'S2 {seg2.count("<div class=\"card p")}'

# 全局 date-tag 时效
tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src)
bad = [t for t in tags if date(2026, int(t[0]), int(t[1])) < T14]
assert not bad, f'超 T-14 date-tag: {bad}'
print('   date-tag 全量:', sorted(set(tags)))

# S7 结构
s7seg = src[src.index('<!-- ============ Section 7: 关键时间线 ============ -->'):]
items2 = ITEM_RE.findall(s7seg)
assert len(items2) == 12, f'S7 final {len(items2)}'
for it in items2:
    assert it.count('timeline-dot') == 1 and it.count('timeline-date') == 1 \
        and it.count('timeline-title') == 1 and 'timeline-desc' not in it
    assert it.count('<div') == it.count('</div>')

# 全局黑名单
for bad2 in ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'toutiao',
             'so.html5.qq.com', '163.com/dy', 'weibo.com', 'k.sina.com.cn']:
    assert bad2 not in src, f'全文件命中黑名单 {bad2}'

open(P, 'w', encoding='utf-8').write(src)
print('\n✅ Phase1 全部断言通过，已写入 index.html')
print('   div', O1, '/', C1, ' S0 cards 4, S1 6, S2 4, S7 12')
