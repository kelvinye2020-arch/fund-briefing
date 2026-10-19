# -*- coding: utf-8 -*-
"""
daily-update 2026-10-19（周一）
更新范围：marker / header 区间 / meta / Stats Bar / S0 / S1 / S2 / S6 / S7
S8 永久废弃：不生成、不补回（脚本内不做任何 S8 相关写入）
"""
import re, io, sys
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TODAY = date(2026, 10, 19)
T14 = TODAY - timedelta(days=14)          # 2026-10-05
EMO = '\U0001F4C5'

p = 'index.html'
h = open(p, encoding='utf-8').read()
orig = h
o0, c0 = h.count('<div'), h.count('</div>')
print(f'起点 div: open={o0} close={c0}')

def rep(old, new, n=1, tag=''):
    global h
    cnt = h.count(old)
    assert cnt == n, f'[{tag}] 期望 {n} 处，实际 {cnt} 处：{old[:60]!r}'
    h = h.replace(old, new, n)
    print(f'  ✓ {tag}')

def log(tag, o, c):
    print(f'  · {tag}: div {o}→{c} (drift {c-o:+d})')

# ============ 1. daily-update marker ============
rep('<!-- daily-update: 2026-10-16 -->', '<!-- daily-update: 2026-10-19 -->', 1, 'marker')

# ============ 2. header 数据区间（动态计算） ============
upper = TODAY.strftime('%Y.%m.%d')
lower = T14.strftime('%Y.%m.%d')
badge_new = f'{EMO} 数据区间：{lower} — {upper}（每日更新）'
pat = re.compile(re.escape(EMO) + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
assert pat.search(h), 'badge 正则未命中'
h = pat.sub(badge_new, h, count=1)
print(f'  ✓ badge → {badge_new}')

# ============ 3. meta description / fingerprint ============
rep('<meta name="description" content="多家公私募逆势自购|多只主动ETF优化产品名称|ETF资金流向净流入563.79亿|首批新能源金属50ETF获批|沪指10-16收3716.28">',
    '<meta name="description" content="首批基金三季报披露 基金经理看好权益|资金避险升温 债基扎堆限购|本周56只新基金发行 指数型27只|新能源金属50ETF获批 华夏在列|沪指10-16收3716.28 纳指跌2.15%">',
    1, 'meta description')
rep('<meta name="content-fingerprint" content="多家公私募|多只主动ETF|ETF资金流向|首批新能源">',
    '<meta name="content-fingerprint" content="首批基金三季报披露|资金避险债基限购|本周56只新基金发行|新能源金属50ETF获批">',
    1, 'fingerprint')

# ============ 4. Stats Bar（第3、4张卡） ============
rep('''    <div class="stat-card">
      <div class="stat-number">162只</div>
      <div class="stat-label">年内FOF发行数量·截至10月11日·发行份额1492.93亿份</div>
      <div class="stat-change up">▲ 数量与份额双创历史新高·节后首周16只</div>
    </div>''',
'''    <div class="stat-card">
      <div class="stat-number">56只</div>
      <div class="stat-label">本周（10月19日—23日）新基金发行·指数型27只·FOF 10只</div>
      <div class="stat-change up">▲ 仅10月19日就有43只启动·上周13只成立近40亿</div>
    </div>''', 1, 'Stats 卡3')

rep('''    <div class="stat-card">
      <div class="stat-number">563.79亿</div>
      <div class="stat-label">10-15 ETF市场整体净流入·九大类全线净流入·宽基446亿居首</div>
      <div class="stat-change up">▲ 沪深300ETF易方达单只净流入188.03亿</div>
    </div>''',
'''    <div class="stat-card">
      <div class="stat-number">360.79亿</div>
      <div class="stat-label">10-16 ETF市场整体净流入·股票型250.39亿·宽基234.89亿</div>
      <div class="stat-change up">▲ 沪深300ETF华泰柏瑞单只净流入129.95亿</div>
    </div>''', 1, 'Stats 卡4')

# ============ 5. S0 今日焦点 ============
# 5.1 section-context
rep('<span class="section-context">10月16日 · 4条今日要闻</span>',
    '<span class="section-context">10月19日 · 4条今日要闻</span>', 1, 'S0 context')
assert '<span class="section-title">今日焦点</span>' in h, 'S0 title 被破坏'

S0_CARDS = '''      <!-- S0 Card 1 (10-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批基金三季报披露·金信南方东财率先出报·基金经理看好权益资产长期表现</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月19日报道（记者赵明超）：公募基金2026年三季报披露大幕正式拉开，<b>金信基金、南方基金、东财基金</b>等基金公司率先披露旗下部分基金三季报。整体看，三季度震荡行情中多只基金调整了持仓结构，部分次新基金则快速建仓；季报中多位基金经理对权益资产持乐观态度，看好企业盈利质量向好与产业长期发展空间广阔的公司。<br>
          <b>调仓主线：</b>金信精选成长混合基金经理孔学兵表示，围绕中国AI基础生态建设，国产先进逻辑芯片与高端存储均取得实质性进展；三季度在总体坚持“低渗透率环节国产化加速”核心配置策略的基础上，进一步<b>减持</b>估值扩张较大、市场预期较为充分的<b>前道设备</b>，同时<b>增持</b>国产化程度更低的<b>光刻制程核心零部件、高价值耗材</b>等基础性瓶颈环节。截至三季度末，精测电子、英诺激光、国力电子新晋该基金前十大重仓股；黄飙管理的金信深圳成长混合前十大重仓股变化较大，欣旺达、万孚生物、比亚迪、保隆科技、爱博医疗新晋。<br>
          <b>次新基金建仓：</b>孙辰阳管理的东财农业智选混合成立于8月18日，截至9月底权益投资占基金总资产比例为<b>92.19%</b>，重点投资以生猪养殖板块为主的农业上市公司，优先配置基本面稳健、抗风险能力较强的龙头企业，并谨慎评估二三线企业在猪周期底部的经营风险。<br>
          <b>后市观点：</b>黄飙认为市场回调与地缘政治波动未改变产业趋势方向，TMT、高端制造、医药生物、新消费的产品与商业模式创新依然层出不穷；孔学兵认为AI产业景气趋势并未系统性降温，科技投资交易重心将从无序资本开支、算力存力堆积走向可持续现金流与利润的验证；南方港股医药行业混合基金经理叶震南看好创新药及创新药产业链的中长期机会，但对AI制药赛道保持谨慎，认为真正的机会来自技术能力、实验验证和商业订单形成正向循环的企业。<br>
          <b>对腾安启示：</b>三季报披露期是持仓与观点的高频更新窗口，内容页须把“基金经理观点”与“实际持仓变动”并列呈现，禁止只摘乐观表态而隐去减持动作；对次新基金高仓位（92.19%）须同步提示建仓期风险与单一行业集中度，不得把“快速建仓”包装为“看好后市”的等价表述。
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-10/19/content_2278653.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-19</span></a>
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202610/t20261019_3262153.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 2 (10-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 资金避险需求升温·债基扎堆限购·近一周债券型ETF净申购超1.6亿份</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          证券时报·人民财讯10月19日转引上海证券报报道：权益市场震荡，资金避险需求升温，股债“跷跷板”效应再度显现。近期场内债券型ETF迎来资金流入盛况，而<b>博时基金、华宝基金、天弘基金</b>等多家基金公司纷纷收紧旗下场外债基的大额申购额度。<br>
          <b>限购实例：</b>10月16日兴华基金公告，即日起将旗下兴华安悦纯债申购、转换转入、定期定额投资业务金额限制设定为<b>100万元</b>；10月15日博时基金公告，10月15日至10月20日旗下博时信用债纯债、博时富添纯债单日每个基金账户申购、转换转入、定投累计金额调整为不超过<b>500万元</b>，10月21日起恢复至1000万元。<br>
          <b>成因：</b>德邦基金投研人士对上海证券报记者表示，一方面权益市场震荡下保险、银行理财等机构资金与部分个人投资者配置固收产品需求增加，债基申购需求明显上升；另一方面流动性环境友好，央行持续维护资金面平稳，节后银行间资金面进一步宽松，收益率下行至阶段性低位后，新申购的增量资金存在配置压力，容易摊薄存量持有人收益。限购核心目的是控制产品规模、平稳投资运作、保护现有基金份额持有人利益。<br>
          <b>场内资金：</b>Choice数据显示，截至10月18日，近一周（10月12日至10月18日）债券型ETF净申购份额超<b>1.6亿份</b>，海富通上证基准做市公司债ETF、华夏上证基准做市公司债ETF均被净申购逾3700万份，易方达上证基准做市公司债ETF、鹏扬中债-30年期国债ETF等亦获较多净申购。<br>
          <b>后市：</b>中欧基金人士表示，受前期利率快速下行过程中交易拥挤度较高、筹码风险未充分释放等扰动，债市或出现震荡调整；中期低利率环境不变，短期调整仍可视为配置机会，当前长债定价总体处在合理位置。<br>
          <b>对腾安启示：</b>债基限购是额度管理信号而非产品优劣信号，展示时须写明限购金额、适用期间与恢复安排，不得把限购包装成“稀缺抢购”；对债券ETF净申购数据须标明统计区间与数据源，不得与场外债基申赎混合表述，也不得以“避险资金涌入”暗示债基无风险。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-10-19/doc-inivtchx6280260.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·证券时报·10-19</span></a>
          <a href="https://fund.10jqka.com.cn/20261019/c680808666.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺基金·10-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 3 (10-19 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 本周56只新基金发行·指数型27只与FOF 10只成主力·仅10月19日就有43只</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月19日报道（Wind数据）：本周（<b>10月19日—10月23日</b>）全市场共<b>56只</b>新基金面市，仅10月19日就有<b>43只</b>启动发行。结构上，<b>27只指数型基金</b>成为发行主力，另有FOF <b>10只</b>、偏股混合型<b>9只</b>、“固收+”<b>6只</b>（含偏债混、一级、二级债基）、中长期纯债<b>2只</b>、公募REITs <b>2只</b>。上周（10月12日—10月16日）共<b>13只</b>新基金成立，总发行规模近<b>40亿元</b>，多资产、多元配置主题FOF受市场青睐。<br>
          <b>主动权益·双基金经理成常态：</b>中欧全裕智选为新模式浮动费率产品，拟任基金经理张聪（12年从业，历任IDG、华兴PE投资部、高瓴PE投资部）与宋婷（8年从业，其中近4年私募投资经验，擅长因子研究与中低频选股策略）；海富通沪港深消费由刘海啸（12年证券从业、含3年基金投资经验）与陈林海（14年证券从业、含5年基金投资经验）共同管理；东方锐见成长拟任严凯（15年证券从业，其中6年公募基金管理经验，现任东方基金权益投资部副总经理）；华商竞争优势混合拟由孙蔚管理（超10年证券从业，覆盖创新药、医疗器械、高端消费）。<br>
          <b>被动端：</b>27只被动指数型基金以主题ETF为主，覆盖畜牧养殖、生物科技、红利、电池、卫星等领域。<br>
          <b>对腾安启示：</b>新发货架须把“双基金经理”拆成两位经理各自的从业年限与策略标签分别展示，禁止合并为一句“强强联手”；浮动费率新品须把费率档位与挂钩基准做成可比字段；对窄基主题ETF须标注跟踪指数与成份股集中度，避免投资者把主题ETF误认为宽基。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR0de4af5d-288f-4b16-7819-3a2463e7eebc" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 4 (10-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 首批新能源金属50ETF获批·华夏华泰柏瑞华宝在列·跟踪中证新能源金属50指数</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻10月16日报道（每经记者黄小聪、编辑叶峰）：<b>华夏基金、华泰柏瑞基金、华宝基金</b>等多家基金公司旗下新能源金属50ETF产品已正式获批，这是首批跟踪<b>中证新能源金属50指数</b>的ETF产品。该指数选取不超过50只业务涉及锂、钴、镍、稀土等新能源领域广泛应用的金属材料相关上市公司证券作为样本，目前共<b>49只</b>成份股，个股平均流通市值约<b>175亿元</b>。<br>
          <b>结构：</b>从中证四级行业看，成份股主要分布于稀土金属（<b>24%</b>）、锂（<b>20%</b>）、钾肥（<b>15%</b>）、电池材料（<b>12%</b>）、钴镍（<b>8%</b>），分布相对分散；前十大权重股主要包括北方稀土、盐湖股份、藏格矿业等。<br>
          <b>业绩与波动（须如实展示）：</b>该指数近一年跌幅超过<b>20%</b>，近三年年化收益率超5%，但<b>近五年年化收益率低于-8%</b>；波动率偏高，近五年年化波动率超过<b>34%</b>。目前ETF中与金属相关的主题产品已超<b>20只</b>，主要跟踪中证有色金属、中证稀有金属主题、中证工业有色金属主题、中证细分有色金属产业主题等指数；近三年年化收益率最高的为中证细分有色金属产业主题指数，中证新能源金属50指数年化收益率最低。<br>
          <b>对腾安启示：</b>新品上架须同步给出指数近三年／近五年年化收益与年化波动率，禁止只呈现“战略资源”“能源转型”叙事而隐去近五年年化为负的事实；与既有有色金属类ETF并列展示时须标明跟踪指数、权重结构与波动率差异，防止投资者按名称相似性做同质化替换。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-10-16/doc-inivmazi7723851.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·每日经济新闻·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

    </div>
  </div>

'''

s0_start = h.find('      <!-- S0 Card 1 ')
s1_mk = h.find('<!-- ============ Section 1')
assert s0_start > 0 and s1_mk > s0_start, 'S0 边界定位失败'
o, c = h.count('<div'), h.count('</div>')
h = h[:s0_start] + S0_CARDS + h[s1_mk:]
log('S0 四卡全换', o, (h.count('<div'), h.count('</div>'))[1])
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S0: open {o}→{o1} ({o1-o:+d}), close {c}→{c1} ({c1-c:+d})')
assert o1 - o == c1 - c, f'S0 div 漂移不配对 {o1-o} vs {c1-c}'

# ============ 6. S1：清旧 1 张（10-04 越界）+ 补新 1 张（10-19） ============
d1 = h.find('<!-- S1 Card: 个人投资者涌入新上市ETF')
d2 = h.find('<!-- S1 Card: 年内122只发起式基金清盘创历史新高')
assert d1 > 0 and d2 > d1, 'S1 删除边界定位失败'
o, c = h.count('<div'), h.count('</div>')
h = h[:d1] + h[d2:]
log('S1 删 10-04', o, (h.count('<div'), h.count('</div>'))[1])
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S1 删卡: open {o1-o:+d}, close {c1-c:+d}')
assert o1 - o == c1 - c

S1_NEW = '''
      <!-- S1 Card: 外资公募量化版图加速扩容 (10-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 外资公募量化版图加速扩容·贝莱德路博迈联博3家已发8只量化产品</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          新浪财经10月19日报道：10月，外资公募<b>路博迈基金</b>旗下红利量化选股基金正式成立，首发规模约<b>2.72亿元</b>。Wind数据显示，5家新设外资公募中，已有<b>贝莱德基金、路博迈基金、联博基金</b>3家发行量化投资相关产品，合计<b>8只</b>，涵盖<b>指数增强与主动选股</b>两类策略。从以跟踪指数为主的“稳中求进”，到红利、行业轮动等策略的主动出击，外资公募的量化版图正加速扩容。<br>
          <b>策略延伸：</b>除股票量化外，外资公募还在探索多资产配置方向，将量化模型与基金经理判断相结合，以风险平价等方式平滑组合波动，满足投资者稳健收益需求。<br>
          <b>对腾安启示：</b>外资量化产品线已从“跟踪指数为主”转向红利、行业轮动等主动策略，做竞品对比时须按策略类型（指数增强／主动量化／多资产配置）而非“外资／内资”标签分类，并标明成立规模、策略口径与费率结构；对“量化”标签不得默认等同于低波动或稳健收益。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-10-19/doc-inivsstc6328463.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·10-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

s2_mk = h.find('<!-- ============ Section 2')
ins1 = h.rfind('    </div>\n  </div>', 0, s2_mk)
assert ins1 > 0, 'S1 插入点定位失败'
o, c = h.count('<div'), h.count('</div>')
h = h[:ins1] + '\n' + S1_NEW + h[ins1:]
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S1 补卡: open {o1-o:+d}, close {c1-c:+d}')
assert o1 - o == c1 - c

# ============ 7. S2：清旧 1 张（10-03 越界）+ 补新 1 张（10-09 决定书） ============
d3 = h.find('<!-- S2 Card: 第三方投顾罚单密集下发')
d4 = h.find('      <!-- S2 Card: 新规落地首周')
assert d3 > 0 and d4 > d3, 'S2 删除边界定位失败'
o, c = h.count('<div'), h.count('</div>')
h = h[:d3] + h[d4:]
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S2 删卡: open {o1-o:+d}, close {c1-c:+d}')
assert o1 - o == c1 - c

S2_NEW = '''
      <!-- S2 Card: 百亿私募杭州图灵一日收三份警示函 (10-09 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 百亿私募杭州图灵一日收三份警示函·七项违规·总经理与风控负责人双双被点名</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-09</span>
          </div>
        </div>
        <div class="card-body">
          浙江证监局于<b>10月9日</b>先后下发三份行政监管措施决定书（10月13日起媒体陆续披露）：对私募基金管理人<b>杭州图灵资产管理有限公司</b>、法定代表人兼总经理<b>王晓妍</b>、合规风控负责人<b>李琼</b>分别采取出具警示函的监督管理措施，相关记录记入证券期货市场诚信档案，三方须于收到决定书<b>15个工作日内</b>提交书面整改报告。<br>
          <b>七项违规（四项涉募集推介与信披）：</b>不配合监管机构依法开展的监督检查；宣传推介材料存在虚假记载；不公平对待同一基金的不同投资者、损害部分投资者利益；向投资者披露的信息不准确、不完整；未保持应有的独立性、与关联方人员混同办公；投资决策相关内部制度执行不到位；投资者适当性程序违规。<br>
          <b>条款对应：</b>不配合监督检查与投资者适当性程序违规对应《私募投资基金监督管理条例》第三十二条第一项；宣传推介材料虚假记载、不公平对待投资者、混同办公、内控执行不到位四项对应第三条第三款；披露信息不准确不完整对应第四十一条第二款。<br>
          <b>主体情况：</b>中基协登记信息显示，杭州图灵成立于2016年9月、2019年3月完成登记，机构类型为私募股权、创业投资基金管理人，管理规模在<b>100亿元</b>以上，全职员工19人；王晓妍为实际控制人，持股<b>82%</b>。截至2026年10月16日，年内新备案产品共<b>20只</b>（集中在1月至5月，5月之后未有新增），存续产品共计<b>56只</b>。<br>
          <b>对腾安启示：</b>监管已把合规岗位的实际履职情况单独审视——风控负责人与总经理并列被点名，说明“合规负责人是否只是挂名、履职是否留痕”正成为检查项；对合作机构的展示须同步呈现其监管措施记录与整改状态，不得以“明星投资人”“明星战绩”叙事覆盖合规瑕疵，也不得因规模百亿而弱化风险提示。
        </div>
        <div class="card-footer">
          <a href="https://www.mrjjxw.com/articles/2026-10-14/4604272.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·10-14</span></a>
          <a href="https://finance.ce.cn/stock/gsgdbd/202610/t20261013_3256410.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-13</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
'''

s3_mk = h.find('<!-- ============ Section 3')
ins2 = h.rfind('    </div>\n  </div>', 0, s3_mk)
assert ins2 > 0, 'S2 插入点定位失败'
o, c = h.count('<div'), h.count('</div>')
h = h[:ins2] + '\n' + S2_NEW + h[ins2:]
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S2 补卡: open {o1-o:+d}, close {c1-c:+d}')
assert o1 - o == c1 - c

# ============ 8. S6 市场行情：美股推进到 10-16 收盘 ============
rep('📈 A股、港股为10-16收盘·美股为10-15收盘·沪指3716.28 +0.24%｜缩量止跌军工爆发',
    '📈 A股、港股、美股统一10-16收盘·沪指3716.28 +0.24%｜纳指跌2.15%科技股遭抛售', 1, 'S6 标题')
rep('<b>港股（10-16收盘）与美股（10-15收盘）</b>', '<b>港股（10-16收盘）与美股（10-16收盘）</b>', 1, 'S6 分组标题')
rep('''              道琼斯 <b>52177.69</b> <span style="color:#dc2626;">+1.08%</span>（+556.21点）<br>
              纳斯达克 <b>26713.03</b> <span style="color:#dc2626;">+0.08%</span>（+20.16点）<br>
              标普500 <b>7744.06</b> <span style="color:#dc2626;">+0.33%</span>（+25.12点）<br>''',
'''              道琼斯 <b>52002.41</b> <span style="color:#52c41a;">-0.34%</span>（-175.28点）<br>
              纳斯达克 <b>26140.03</b> <span style="color:#52c41a;">-2.15%</span>（-572.99点）<br>
              标普500 <b>7659.44</b> <span style="color:#52c41a;">-1.09%</span>（-84.62点）<br>''', 1, 'S6 美股点位')
rep('美股取<b>10月15日收盘</b>（美东10月15日收盘对应北京时间10月16日凌晨）',
    '美股取<b>10月16日收盘</b>（美东10月16日收盘对应北京时间10月17日凌晨）', 1, 'S6 口径')

old_us = '''<b>美股（10-15）：</b>三大股指上涨。道琼斯工业平均指数涨556.21点、涨幅1.08%收<b>52177.69</b>点；标准普尔500种股票指数涨25.12点、涨幅0.33%收<b>7744.06</b>点；纳斯达克综合指数涨20.16点、涨幅0.08%收<b>26713.03</b>点。标普500十一大板块八涨三跌，医疗板块与材料板块分别以1.84%和1.71%的涨幅领涨，能源板块与科技板块分别以1.55%和0.54%的跌幅领跌（新华社）。'''
new_us = '''<b>美股（10-16）：</b>因人工智能相关科技股再次遭到抛售、国际油价显著走高，三大股指开盘涨跌不一、盘中显著走低、尾盘跌幅收窄，收盘均下跌。道琼斯工业平均指数跌175.28点、跌幅0.34%收<b>52002.41</b>点；标准普尔500种股票指数跌84.62点、跌幅1.09%收<b>7659.44</b>点；纳斯达克综合指数跌572.99点、跌幅2.15%收<b>26140.03</b>点。标普500十一大板块六涨五跌，能源板块与公用事业板块分别以2.47%和1.40%的涨幅领涨，科技板块与通信服务板块分别以2.54%和2.45%的跌幅领跌。全周看，纳斯达克综合指数累计下跌4.48%、道指累计上涨0.67%；衡量恐慌情绪的芝加哥期权交易所波动指数当日最高升至22.31、收于19.99，大幅上涨21.45%。美联储主席沃什16日表态后，市场对10月议息会议加息的预期进一步降温，CME“美联储观察”显示10月加息25个基点的概率由前一日的27.7%降至17.2%（新华社）。'''
rep(old_us, new_us, 1, 'S6 美股正文')

old_tip = '前一日宽基ETF单日净流入逾560亿元与今日指数止跌形成呼应，但属托底型资金特征'
new_tip = '10月16日ETF资金整体净流入360.79亿元（同花顺iFinD口径，股票型250.39亿、宽基234.89亿，沪深300ETF华泰柏瑞单只129.95亿居首）与当日指数止跌形成呼应，但属托底型资金特征'
rep(old_tip, new_tip, 1, 'S6 提示段')

rep('<span class="source-tag">数据基准：A股、港股为2026-10-16收盘，美股为2026-10-15收盘</span>',
    '<span class="source-tag">数据基准：A股、港股、美股均为2026-10-16收盘</span>', 1, 'S6 footer 基准')
rep('<span class="source-tag">数据来源：新华社、格隆汇、每日经济新闻、东方财富行情（10-16）</span>',
    '<span class="source-tag">数据来源：新华社（美股）、格隆汇·同花顺iFinD（ETF资金）、东方财富行情（10-19）</span>', 1, 'S6 footer 来源')

# ============ 9. S7 时间线重写（12 条降序） ============
s7_mk = h.find('<!-- ============ Section 7')
s7_start = h.find('      <div class="timeline-item">', s7_mk)
s7_end = h.find('\n    </div>\n', s7_start)
assert s7_start > 0 and s7_end > s7_start, 'S7 边界定位失败'

ITEMS = [
    ('2026-10-19', 'blue', '首批基金三季报披露开启'),
    ('2026-10-19', 'blue', '债基扎堆限购·避险资金涌入'),
    ('2026-10-19', 'blue', '本周56只新基金启动发行'),
    ('2026-10-19', 'blue', '外资公募量化产品扩至8只'),
    ('2026-10-16', 'blue', '首批新能源金属50ETF获批'),
    ('2026-10-16', 'blue', '沪指收3716.28点涨0.24%'),
    ('2026-10-16', 'blue', 'ETF单日净流入360.79亿元'),
    ('2026-10-16', 'blue', '纳指跌2.15%科技股遭抛售'),
    ('2026-10-15', 'blue', '122只发起式基金清盘创新高'),
    ('2026-10-13', 'blue', '公募首份三季报出炉'),
    ('2026-10-12', 'red', '公募运作办法公开征求意见'),
    ('2026-10-09', 'red', '浙江证监局警示杭州图灵'),
]
buf = []
for d, col, t in ITEMS:
    buf.append(
        f'      <div class="timeline-item">\n'
        f'        <div class="timeline-dot {col}"></div>\n'
        f'        <div class="timeline-date">{d}</div>\n'
        f'        <div class="timeline-title">{t}</div>\n'
        f'      </div>'
    )
NEW_S7 = '\n'.join(buf)
o, c = h.count('<div'), h.count('</div>')
h = h[:s7_start] + NEW_S7 + h[s7_end + 1:]
o1, c1 = h.count('<div'), h.count('</div>')
print(f'  · S7: open {o1-o:+d}, close {c1-c:+d}')
assert o1 - o == c1 - c

# ============ 10. 落盘与自检 ============
open(p, 'w', encoding='utf-8').write(h)

fo, fc = h.count('<div'), h.count('</div>')
print(f'\n终点 div: open={fo} close={fc}（起点 {o0}/{c0}）')
assert fo == fc, f'div 不配对 {fo} vs {fc}'
assert 'S8' not in h, '出现 S8 残留'
assert h.count('待办跟踪') == 0 and h.count('腾安行动清单') == 0, '出现 S8 残留元素'
assert '<span class="section-title">今日焦点</span>' in h, 'S0 title 异常'
assert '10月19日 · 4条今日要闻' in h, 'S0 context 异常'
for m in ['Section 0', 'Section 1', 'Section 2', 'Section 3', 'Section 4',
          'Section 5', 'Section 6', 'Section 7']:
    assert m in h, f'{m} marker 丢失'
print('结构自检通过：div 配对 / S8 不存在 / S0-S7 marker 完整')
