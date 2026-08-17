# -*- coding: utf-8 -*-
"""基金行业资讯看板 2026-08-08 每日更新（两阶段：先全断言，后写盘）"""
import io, re, sys

P = 'index.html'
s = open(P, encoding='utf-8').read()
ORIG = s
ORIG_OPEN = s.count('<div')
ORIG_CLOSE = s.count('</div>')
print('BASE open/close =', ORIG_OPEN, ORIG_CLOSE)
assert ORIG_OPEN == ORIG_CLOSE, 'baseline已失衡'

steps = []  # (name, expected_div_delta)

def snap(tag, cur):
    o = cur.count('<div'); c = cur.count('</div>')
    print(f'  [{tag}] open={o} close={c} bal={o-c} drift={o-ORIG_OPEN}')
    assert o == c, f'{tag} 失衡'
    return o - ORIG_OPEN

# ============ 锚点预检 ============
ANCHORS = {
    'marker':          '<!-- daily-update: 2026-08-07 -->',
    'header_range':    '📅 数据区间：2026.07.24 — 2026.08.07（每日更新）',
    's0_ctx':          '<span class="section-context">8月7日 · 4条今日要闻</span>',
    's0_start':        '      <!-- S0 Card 1: 银行密集上调基金风险评级 (T+0 08-07 P0 带action-box) -->',
    's0_end':          '\n<!-- ============ Section 1: 重磅信息 ============ -->',
    's6_start':        '<!-- ============ Section 6: 市场行情速览 ============ -->',
    's6_end':          '\n<!-- ============ Section 7: 关键时间线 ============ -->',
    'stats_start':     '<!-- Stats Bar -->',
    'stats_end':       '</div>\n<div class="main">',
    's7_first':        '      <!-- 08-07 时间线条目 -->',
    's7_oldest':       '      <!-- 07-27 时间线条目 (NEW) -->',
}
for k, v in ANCHORS.items():
    n = s.count(v)
    print(f'anchor {k}: {n}')
    assert n == 1, f'锚点 {k} 命中 {n} 次（需恰好1次）'

# ============ 1. marker + header 区间 ============
s = s.replace(ANCHORS['marker'], '<!-- daily-update: 2026-08-08 -->')
s = s.replace(ANCHORS['header_range'], '📅 数据区间：2026.07.25 — 2026.08.08（每日更新）')
snap('marker+header', s)

# ============ 2. Stats Bar 整块替换 ============
ST_A = ANCHORS['stats_start']
ST_B = ANCHORS['stats_end']
i = s.index(ST_A); j = s.index(ST_B, i)
STATS_BODY = '''<!-- Stats Bar -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">3940.04</div>
      <div class="stat-label">上证指数 · 08-07收盘 · 四连阳·全周涨2.81%</div>
      <div class="stat-change up">▲ 涨1.02%·深成指14311.01(+1.42%)·创业板指3563.12(+1.35%)·成交2.66万亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">16家</div>
      <div class="stat-label">08-07上报创业板算力/金融科技ETF的公募</div>
      <div class="stat-change up">▲ 创业板行业主题指数产品化"从0到1"·算力10家+金融科技6家</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">19只</div>
      <div class="stat-label">截至08-07 年内净值涨超10%的医药类基金</div>
      <div class="stat-change up">▲ 最高近25%·医药基总规模2767亿年内增近300亿·创新药主题1517亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">75只</div>
      <div class="stat-label">8月新发基金总数 · 创2026年内月度新低</div>
      <div class="stat-change down">▼ 仅48家公募参与·较6月182只近乎腰斩·ETF占比不足15%</div>
    </div>
  '''
s = s[:i] + STATS_BODY + s[j:]
d = snap('stats', s)
assert d == 0, f'Stats Bar 漂移 {d}，应为 0'

# ============ 3. S0 整块替换（4卡全新） ============
S0_A = s.index(ANCHORS['s0_start'])
S0_B = s.index(ANCHORS['s0_end'])
S0_TAIL = '    </div>\n  </div>\n\n'   # card-grid close + section close，硬编码常量

S0_BODY = '''      <!-- S0 Card 1: 16家公募上报创业板算力/金融科技ETF (T-1 08-07 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">08-07</span>
          </div>
          <div class="card-title">🔴 首批16家公募上报创业板算力/金融科技ETF·"创系列"指数产品化从0到1破冰</div>
        </div>
        <div class="card-body">
          8月7日晚证监会官网显示，首批<b>16家基金管理人</b>集中上报<b>创业板算力基础设施指数ETF</b>与<b>创业板金融科技指数ETF</b>。其中上报算力基础设施ETF的<b>10家</b>：易方达、华夏、南方、广发、富国、国泰、嘉实、天弘、鹏华、大成；上报金融科技ETF的<b>6家</b>：景顺长城、华泰柏瑞、万家、东财、长城、建信。这是创业板行业主题指数产品化<b>"从0到1"的突破</b>，标志"创系列"特色指数及ETF产品体系建设迈入实质推进阶段。<br>
          <b>指数设计：</b>创业板算力基础设施指数（<b>970083</b>）从创业板精选50只算力相关标的，覆盖计算、网络、存储、运维全环节，前十大权重含协创数据、软通动力、光环新网、景嘉微、润泽科技等；创业板金融科技指数（<b>970085</b>）同样选取50只标的，涵盖分布式技术、支付结算、互联网金融、金融安全与金融数字化服务上中下游，前十大权重含同花顺、东方财富、指南针、润和软件、拉卡拉等，与传统创业板宽基形成明显风险收益区隔。<br>
          <b>后续储备：</b>深圳证券信息公司此前已发布创业板算力、金融科技、电池、医疗、传媒、专精特新、通信、智能驾驶、机器人等多条行业主题指数，业内预计<b>近期将有更多创系列产品上报</b>，创业板"指数化投资工具箱"加速充实。此举被视为落实证监会《关于深化创业板改革 更好服务新质生产力发展的意见》中"优化创业板指数、ETF和期货期权产品体系"任务的重磅举措。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/ARc39e9199-0471-900e-1f8d-3a22ee147979" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <span class="impact-tag high">产品线影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            <b>①提前建立"创系列"货架预案：</b>16只产品集中申报意味着未来3—6个月将批量获批发行，腾安应提前梳理创业板算力（970083）与金融科技（970085）两条指数的成分、估值与历史波动，制定上架排期与首发合作管理人名单，避免产品密集上市时被动跟随。<br>
            <b>②警惕同质化与规模分层：</b>10家争抢一条算力指数、6家争抢金融科技指数，参考此前主题ETF经验，最终规模高度向前2—3家集中。选品应优先绑定做市与流动性能力强的头部管理人，不建议全量上架造成货架冗余。<br>
            <b>③客户教育口径：</b>创业板算力/金融科技与既有科创芯片、CPO、AI主题ETF在成分上存在明显重叠，需在推荐页明确标注重叠度，防止客户误以为是分散配置而实际加倍暴露于同一赛道。
          </div>
        </div>
      </div>

      <!-- S0 Card 2: 公募将"负责任AI"纳入治理议题 (T+0 08-08 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🟡 公募AI治理走向纵深·华夏等将"负责任AI"纳入新议题·永赢银华输出安全运营案例</div>
        </div>
        <div class="card-body">
          证券时报·券商中国8月8日报道，AI技术在基金业的运用边界在7月扩大到<b>治理领域</b>。内部治理方面，基金业在"AI内部安全治理"已取得基本共识：<b>永赢基金</b>通过安全GPT钓鱼检测大模型，高对抗钓鱼邮件检出率<b>超93%</b>、误报率降至<b>0.28%以下</b>、安全人员人工复核工作量减少<b>80%以上</b>；<b>银华基金</b>以AI原生智能体为核心的告警自动处置体系，日均原始告警从数千条压缩至数十条（噪声压缩率<b>超92%</b>）、单条告警研判时长从30分钟压缩至<b>3分钟以内</b>、设备异常发现时间从4小时以上压缩至<b>1小时以内</b>。中基协7月下旬与上交所、上海市基金同业公会举办基金行业数据要素培训班，260余人参加。<br>
          <b>外部治理：</b>截至8月3日，<b>华夏基金</b>等已将"负责任AI"作为新议题，纳入对涉及模型研发与商业化的科技公司治理考察，从治理架构、风险识别与评估、行业正外部影响力三个维度展开。华夏与紫顶发布的《AI浪潮下的ESG》报告提出"组织定责—数据筑基—技术兜底—产品落地"闭环。全球范围内，挪威主权财富基金（NBIM）、纽约州共同退休基金、安联全球投资已率先将负责任AI纳入尽责管理；美股AI相关股东提案从2023年16项增至2025年<b>26项</b>，独立股东平均支持率约<b>30%</b>，显著高于一般ESG提案的约16%。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L3Q1NLFF053469RG.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·券商中国</span></a>
          <span class="impact-tag medium">治理影响：中</span>
        </div>
      </div>

      <!-- S0 Card 3: 19只医药类基金年内涨超10% (T+0 08-08 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🟡 19只医药类基金年内涨超10%·最高近25%·医药基规模增至2767亿</div>
        </div>
        <div class="card-body">
          证券日报8月8日报道（记者王宁），Wind数据显示截至<b>8月7日</b>，年内<b>19只医药类基金</b>净值涨幅均超10%，最高涨幅近<b>25%</b>。<b>主动管理型包揽涨幅榜前十</b>：招商医药健康产业以近25%居全市场第一，鹏华创新医药A以24%紧随其后，永赢医药健康A保持20%以上，国泰医药健康A、汇添富医药保健A、交银医药创新A、嘉实医药健康A等在10%—20%区间。<br>
          <b>指数型分化明显：</b>天弘恒生沪深港创新药精选50ETF以<b>11.19%</b>领跑，跟踪中证创新药产业指数的ETF普遍在2%—8%；但多只港股医药指数基金表现不佳，某港股通医药A回撤<b>12.37%</b>、某恒生港股通创新药精选ETF回撤<b>11.79%</b>。<br>
          <b>规模端：</b>医药类基金总规模已增至<b>2767亿元</b>、年内增长近300亿元，5只产品跻身百亿阵营（广发中证香港创新药ETF 266亿、汇添富国证港股通创新药ETF 245亿、银华中证创新药产业ETF、易方达沪深300医药ETF、广发中证创新药产业ETF），另有48只规模在10亿—100亿元。创新药主题基金规模由年初<b>1192亿元</b>增至<b>1517亿元</b>，年内增超300亿。<br>
          <b>对基金行业影响：</b>医药成为科技回调后的主要接力赛道→腾安可在货架上强化医药/创新药主题的主动与被动双线布局，但需向客户提示A股与港股创新药标的年内表现严重背离的结构性风险。
        </div>
        <div class="card-footer">
          <a href="https://finance.ce.cn/stock/gsgdbd/202608/t20260808_3135834.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·中国经济网</span></a>
          <span class="impact-tag high">赛道影响：高</span>
        </div>
      </div>

      <!-- S0 Card 4: A股四连阳反弹格局确立 (T+0 08-08 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">08-08</span>
          </div>
          <div class="card-title">🔵 A股四连阳确立反弹格局·科创综指周涨10.96%·医药算力双主线领涨</div>
        </div>
        <div class="card-body">
          上海证券报8月8日报道（记者徐蔚），8月7日A股低开高走全线收红，四大股指涨幅悉数突破1%：上证指数报<b>3940.04</b>点（+1.02%）、深证成指<b>14311.01</b>点（+1.42%）、创业板指<b>3563.12</b>点（+1.35%）、科创综指大涨<b>3.35%</b>；沪深北三市成交额接近<b>2.7万亿元</b>，较上一日放量1359亿元，超2800只个股上涨、逾70只涨停。<br>
          <b>全周表现：</b>8月3日—7日主要指数全线反弹，上证累计<b>+2.81%</b>、深成指<b>+5.39%</b>、创业板指<b>+6.55%</b>，科创综指全周涨幅达<b>10.96%</b>，中证1000涨超8%，中小盘领跑；主要指数录得<b>四连阳</b>，全周日均成交维持在2.4万亿元上方。<br>
          <b>反弹规律：</b>招商证券复盘2015年以来A股九次大幅调整发现，调整后平均反弹窗口为<b>34个交易日</b>，万得全A平均反弹幅度<b>超19%</b>，且前期跌幅越大后期反弹空间往往越高；行业呈"两段式"轮动——前10个交易日高β、超跌板块领涨，20至60个交易日后转向有景气支撑的主线。创新药与算力硬件成为贯穿本周的两大核心主线，CRO掀涨停潮、CPO与PCB延续强势。<br>
          <b>对基金行业影响：</b>市场情绪明确修复→新发窗口有望在8月下旬回暖，腾安可关注反弹中后段从"高β超跌"切向"景气主线"的配置节奏切换，避免客户在反弹前段追高单一赛道。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260808A03OGO00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">市场影响：中</span>
        </div>
      </div>

'''
s = s[:S0_A] + S0_BODY + S0_TAIL + s[S0_B:]
d = snap('S0', s)
assert d == 0, f'S0 漂移 {d}，应为 0（4卡换4卡，1个action-box换1个）'

# S0 context
s = s.replace(ANCHORS['s0_ctx'], '<span class="section-context">8月8日 · 4条今日要闻</span>')
snap('s0_ctx', s)

# ============ 4. S6 整块替换为 08-07 收盘（保留双栏 grid 五层嵌套） ============
S6_A = s.index(ANCHORS['s6_start'])
S6_B = s.index(ANCHORS['s6_end'])
S6_BODY = '''<!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年8月7日（周五·收盘）·A股四大指数齐涨超1%·沪指3940.04收复年内高地·科创综指涨3.35%·CRO掀涨停潮</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股08-07收盘（低开高走·全线收红·四连阳）：</b><br>
              ▪ 上证 <b>3940.04</b>（<b>+1.02%</b>，最高3940.93/最低3885.62）·深成指 <b>14311.01</b>（<b>+1.42%</b>）·创业板指 <b>3563.12</b>（<b>+1.35%</b>）·科创综指 <b>+3.35%</b><br>
              ▪ 成交：沪深两市成交额 <b>2.66万亿元</b>，较前一交易日2.53万亿<b>放量约1356亿元</b>（沪市12095亿·深市14549亿）；沪深北三市合计接近2.7万亿<br>
              ▪ 涨跌家数：全市场<b>超2800只个股上涨</b>，逾<b>70只涨停</b>；跌停含甘咨询、大晟文化、恒银科技、风范股份<br>
              ▪ 领涨：CRO概念掀涨停潮（义翘神州、昭衍新药、哈三联涨停，药康生物20cm涨停、百花医药4连板）、CPO（沃格光电4连板，一博科技/依顿电子/博敏电子/生益科技/红板科技/景旺电子涨停）、PCB延续涨势、小金属（中国稀土、云南锗业、有研新材涨停）、元件、电子化学品、贵金属、半导体<br>
              ▪ 领跌：多元金融、软件开发、游戏、煤炭开采加工、数字货币、共享单车、跨境支付、财税数字化<br>
              ▪ 换手率前五：展芯股份79.39%、津富士达62.20%、嘉立创54.79%、万邦医药48.92%、吉和昌46.48%
            </div>
            <div>
              <b>📉 上一交易日08-06收盘：</b>上证 3900.35（<b>+0.57%</b>）·深成指 14110.12（-0.24%）·创业板指 3515.56（-0.55%），成交2.53万亿<br>
              <b>📈 全周（08-03至08-07）：</b>上证累计 <b>+2.81%</b>·深成指 <b>+5.39%</b>·创业板指 <b>+6.55%</b>·科创综指 <b>+10.96%</b>·中证1000 涨超8%，主要指数录得<b>四连阳</b>，日均成交维持2.4万亿上方<br>
              <b>📈 港股08-07收盘（企稳回升）：</b>恒生指数 <b>25668.03</b>（<b>+0.54%</b>，涨137.75点）·国企指数 8531.58（<b>+0.39%</b>）·恒生科技 <b>4858.29</b>（<b>+0.78%</b>）；成交2596.86亿港元<br>
              <b>📈 美股08-07收盘（三大指数齐涨·AI算力领涨）：</b>道指 <b>54036.93</b>（<b>+0.28%</b>）·标普500 <b>7757.64</b>（<b>+0.62%</b>）·纳指 <b>26690.62</b>（<b>+1.30%</b>）；半导体内部分化，AI算力芯片与先进制造走强，存储芯片延续调整（SK海力士、希捷、西部数据继续承压）<br>
              <b>📈 欧股08-07收盘：</b>德国DAX30 26319.45（+0.69%）·法国CAC40 8714.93（+0.17%）·英国富时100 10901.09（+0.31%）·欧洲斯托克50 6523.86（+0.33%）<br>
              <b>📉 亚太其他：</b>日经225 65606.71（<b>-0.12%</b>）·韩国KOSPI 6258.77（<b>-0.60%</b>）<br>
              <b>📊 大宗与汇率：</b>现货黄金 <b>4342.18</b>美元/盎司（<b>+2.39%</b>）·COMEX黄金期货4401.30美元/盎司（+2.37%）·上金所黄金9999 <b>938.00元/克</b>（+0.81%）·沪金主连941.72元/克（+1.53%）；WTI原油78.18美元/桶（<b>+1.15%</b>）·布伦特83.55美元/桶（+1.29%）；伦铜14022美元/吨（-0.50%）·沪铜主连107160元/吨（-0.80%）
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：8月7日A股<b>四大指数齐涨超1%，四连阳确立反弹格局</b>，全周上证+2.81%、创业板指+6.55%、科创综指+10.96%，中小盘与成长风格全面领跑，市场情绪从7月末的恐慌性出清明显修复。三点值得注意：① <b>主线由煤炭等资源股切回创新药与算力硬件</b>，与前一日"沪强深弱"的高低切换形成反转——CRO掀涨停潮、CPO与PCB延续强势，药康生物中报预告归母净利同比增46.67%—60.78%，板块上涨具备业绩支撑而非纯情绪驱动；② <b>反弹节奏进入关键判定期</b>，招商证券复盘显示调整后平均反弹窗口34个交易日、万得全A平均反弹超19%，行业呈"前10个交易日高β超跌领涨、20—60个交易日转向景气主线"的两段式轮动，本周正处第一段末端，后续需警惕超跌反弹动能衰减；③ <b>外围同步转暖</b>，美股三大指数齐涨（纳指+1.30%）、港股恒指+0.54%企稳、黄金单日大涨2.39%创阶段新高，风险偏好与避险需求罕见同步抬升，反映市场对美联储政策路径分歧加大。<b>A股/港股/美股均为08-07收盘口径。</b>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-08-07收盘</span>
            <span class="source-tag">数据来源：同花顺iFind/上海证券报/证券时报/中新经纬/国际金融要情</span>
          </div>
      </div>
  </div>
'''
s = s[:S6_A] + S6_BODY + s[S6_B:]
d = snap('S6', s)
assert d == 0, f'S6 漂移 {d}，应为 0（结构等价替换）'

# ============ 5. S7：删最旧(07-27) + 插入 08-08 ============
# 5a 删除 07-27 条目（含注释头 + 整块 timeline-item）
OLD27 = '''      <!-- 07-27 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-27</div>
        <div class="timeline-title">绩优基金提前减仓·公募对科技后市现巨大分歧</div>
      </div>

'''
assert s.count(OLD27) == 1, 'S7 07-27 块锚点异常'
s = s.replace(OLD27, '')
d = snap('S7-del', s)
assert d == -4, f'S7 删条目漂移 {d}，应为 -4（item+dot+date+title 各1个div）'

# 5b 插入 08-08 到最前
NEW08 = '''      <!-- 08-08 时间线条目 -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-08</div>
        <div class="timeline-title">19只医药基年内涨超10%·医药接力科技</div>
      </div>
'''
i = s.index(ANCHORS['s7_first'])
s = s[:i] + NEW08 + s[i:]
d = snap('S7-add', s)
assert d == 0, f'S7 增删净漂移 {d}，应为 0'

# ============ Phase 1 断言总集 ============
print('\n=== PHASE 1 ASSERT ===')
o, c = s.count('<div'), s.count('</div>')
assert o == c == ORIG_OPEN, f'最终 div 不平衡/漂移: {o}/{c} vs {ORIG_OPEN}'
print('OK div balance', o, c)

# S8 三关键词
for k in ['Section 8', '待办跟踪', '腾安行动清单']:
    assert k not in s, f'S8 残留: {k}'
print('OK 无S8残留')

# S0 段校验
s0seg = s[s.index('<!-- S0 Card 1:'): s.index('Section 1: 重磅信息')]
assert s0seg.count('<div class="action-box">') == 1, 'S0 action-box 数量异常'
assert s0seg.count('<div class="card p0">') == 1, 'S0 p0 卡数异常'
assert s0seg.count('<div class="card-meta">') == 4, 'S0 card-meta 数异常'
assert s0seg.count('<div class="card-top">') == 4, 'S0 card-top 数异常'
assert s0seg.count('target="_blank"') == 4, 'S0 出处链接数异常'
dts = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s0seg)
assert dts == ['08-07', '08-08', '08-08', '08-08'], f'S0 date-tag 异常: {dts}'
print('OK S0', dts)

# section-title / context
assert s.count('<span class="section-title">今日焦点</span>') == 1, 'S0 title 异常'
assert s.count('<span class="section-context">8月8日 · 4条今日要闻</span>') == 1, 'S0 context 异常'
assert '今日焦点（' not in s, 'S0 title 堆料'
print('OK S0 header')

# S7 校验
s7seg = s[s.index('Section 7: 关键时间线'):]
assert 'timeline-desc' not in s7seg, 'S7 存在 timeline-desc'
d7 = re.findall(r'<div class="timeline-date">(2026-\d\d-\d\d)</div>', s7seg)
assert len(d7) == 12, f'S7 条目数 {len(d7)}，应为 12'
assert len(d7) == len(set(d7)), f'S7 日期重复: {d7}'
assert d7 == sorted(d7, reverse=True), f'S7 未严格降序: {d7}'
assert d7[-1] >= '2026-07-25', f'S7 存在超 T-14 条目: {d7[-1]}'
t7 = re.findall(r'<div class="timeline-title">(.*?)</div>', s7seg)
mx = max(len(x) for x in t7)
assert mx <= 25, f'S7 标题超25字: {[x for x in t7 if len(x) > 25]}'
assert s7seg.count('<div class="timeline-item">') == 12, 'S7 item 数异常'
print('OK S7', len(d7), 'items, maxlen', mx, 'range', d7[-1], '~', d7[0])

# S1 / S2 过期审计（T-14 = 2026-07-25）
CUT = '07-25'
s1seg = s[s.index('Section 1: 重磅信息'): s.index('Section 2: 监管政策')]
s2seg = s[s.index('Section 2: 监管政策'): s.index('Section 3: 竞争对手动态')]
d1 = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s1seg)
d2 = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s2seg)
assert all(x >= CUT for x in d1), f'S1 过期: {d1}'
assert all(x >= CUT for x in d2), f'S2 过期: {d2}'
assert len(d1) <= 6 and len(d2) <= 4, f'S1/S2 超上限: {len(d1)}/{len(d2)}'
assert s1seg.count('target="_blank"') == len(d1), 'S1 链接数不匹配'
assert s2seg.count('target="_blank"') == len(d2), 'S2 链接数不匹配'
print('OK S1', d1, '| S2', d2)

# 乱码 + marker
assert '\ufffd' not in s, 'U+FFFD 乱码残留'
assert s.count('<!-- daily-update: 2026-08-08 -->') == 1, 'marker 异常'
assert '2026.07.25 — 2026.08.08' in s, 'header 区间未更新'
# 口径一致性
assert s.count('3940.04') >= 3, '08-07 收盘点位引用不足'
print('OK 乱码/marker/header/口径')

print('\n=== PHASE 2 WRITE ===')
open(P, 'w', encoding='utf-8', newline='').write(s)
print('written', len(s), 'chars (was', len(ORIG), ')')
