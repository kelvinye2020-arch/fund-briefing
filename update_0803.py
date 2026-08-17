# -*- coding: utf-8 -*-
"""基金行业资讯看板 2026-08-03 每日更新（两阶段：全断言 -> 写文件）"""
import io, re, sys

P = 'index.html'
s = io.open(P, encoding='utf-8').read()
orig = s

# ============ Phase 1: 全部断言 + 构造新串（不写文件） ============

# --- 1. date-badge ---
A_BADGE = '<div class="date-badge">📅 数据区间：2026.07.19 — 2026.08.02（每日更新）</div>'
N_BADGE = '<div class="date-badge">📅 数据区间：2026.07.20 — 2026.08.03（每日更新）</div>'
assert s.count(A_BADGE) == 1, 'badge'

# --- 2. Stats Bar 整块替换 ---
ST_A = '<!-- Stats Bar -->\n  <div class="stats-bar">'
ST_B = '</div>\n  </div>\n<div class="main">'
i = s.index(ST_A); j = s.index(ST_B, i)
assert i < j, 'stats range'
NEW_STATS = ST_A + '''
    <div class="stat-card">
      <div class="stat-number">2只</div>
      <div class="stat-label">年内翻倍主动权益基金 · 较上半年199只锐减·前七月业绩大洗牌</div>
      <div class="stat-change down">▼ 均为易方达杨宗昌管理（供给改革+118.97%·产业机遇A+116.16%）·前20席位仍被科技AI主题包揽</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">790只</div>
      <div class="stat-label">7月跌超30%主动权益基金 · 其中280只仍维持R3中风险等级</div>
      <div class="stat-change down">▼ 逾三分之一评级滞后·24只R3基金月跌超40%·仅东吴/华泰柏瑞等极少数上调评级</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">5.10万亿</div>
      <div class="stat-label">建行公募托管资产 · 超越工行登顶·托管"一哥"易主</div>
      <div class="stat-change up">▲ 建行占比12.87%较年末+2627.77亿·工行5.05万亿缩水3171.51亿·宽基ETF集中赎回为主因</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1400亿+</div>
      <div class="stat-label">深市ETF 7月净申购 · 创业板指/人工智能/通信为三大主线</div>
      <div class="stat-change up">▲ 创业板相关ETF净申购617.93亿·深市人工智能ETF 45.34亿·深市通信ETF 39.40亿</div>
    ''' + ST_B
s = s[:i] + NEW_STATS + s[j + len(ST_B):]

# --- 3. S0 section-context ---
A_CTX = '<span class="section-context">8月2日 · 4条今日要闻</span>'
N_CTX = '<span class="section-context">8月3日 · 4条今日要闻</span>'
assert s.count(A_CTX) == 1, 'ctx'
s = s.replace(A_CTX, N_CTX)

# --- 4. S0 卡片区整块替换（尾部硬编码 2 个闭合：card-grid + section） ---
S0_A = '      <!-- S0 Card 1: 公募备战主动ETF落地倒计时 (T+0 08-02 P0 带action-box) -->'
S0_B = '<!-- ============ Section 1: 重磅信息 ============ -->'
i = s.index(S0_A); j = s.index(S0_B, i)
assert i < j, 's0 range'
S0_NEW = '''      <!-- S0 Card 1: 公募前七月业绩大洗牌翻倍基仅剩2只 (T+0 08-03 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 公募前七月业绩大洗牌·年内翻倍基金从199只锐减至2只·科技主题基金集体回撤</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">08-03</span>
          </div>
        </div>
        <div class="card-body">
          <b>断崖式缩水：</b>Wind数据显示，截至<b>7月31日</b>，年内收益率超100%的主动权益基金<b>仅剩2只</b>，而上半年收官时这一数字高达<b>199只</b>（Wind全口径含指数产品曾达246只）。7月高位获利盘集中兑现、科技板块整体回调，重仓AI与半导体的产品净值遭遇明显回撤，市场赚钱效应显著降温。<br>
          <b>幸存双雄：</b>唯二守住翻倍线的产品均来自易方达基金经理<b>杨宗昌</b>——易方达供给改革以<b>118.97%</b>年内回报居首、易方达产业机遇A以<b>116.16%</b>紧随，包揽全市场前两名，回撤控制亦显著优于同类。东方人工智能主题、汇安趋势动力、诺安创新驱动、银华集成电路、国泰半导体制造精选等5只产品前七月收益率超90%。<br>
          <b>冠军失速：</b>上半年"冠军基"方正富邦核心优势A（半年+183.67%创历史纪录）7月单月回撤逾42%，年内收益率一度回落至63.64%；财通多策略福鑫（金梓才）同样大幅回吐。规模351.25亿元的东方人工智能主题近一月回撤达<b>27.04%</b>，高位资金兑现压力突出。红利、医药、中小盘品种则迎来逆势修复窗口。<br>
          <b>对基金行业影响：</b>业绩榜单一月内近乎重排，验证单赛道极致押注的脆弱性→腾安须警惕以短期排名为核心的营销话术，将选品与推荐口径转向回撤控制与长周期稳定性。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/4054199.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag high">业绩洗牌：高</span>
        </div>
        <div class="action-box">
          <div class="action-title">⚡ 腾安行动建议</div>
          <div class="action-content">① <b>榜单话术整改</b>：翻倍基一月内由199只降至2只，说明"年内收益率排名"作为推荐依据极不稳定，须立即下线以短期排名为卖点的展示位，改以近三年/最大回撤等长周期指标为主排序；② <b>持有人回访</b>：对6—7月高位申购科技主题产品的客户做主动回访与预期管理，提供加仓/持有/止盈的分层沟通脚本，避免净值二次探底时集中赎回；③ <b>货架再平衡</b>：红利、医药、中小盘正处修复窗口，建议提高均衡与低波品种的曝光权重，对冲单一AI主线的组合风险。</div>
        </div>
      </div>

      <!-- S0 Card 2: 基金风险评级滞后 (T+0 08-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 近300只中风险基金单月暴跌超30%·790只跌超30%产品中280只仍标R3·风险评级滞后待解</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">08-03</span>
          </div>
        </div>
        <div class="card-body">
          <b>评级与波动脱节：</b>证券时报报道，7月科技板块剧烈回调之下，<b>790只</b>主动权益基金跌幅超30%，其中<b>280只（占35.44%）</b>仍维持<b>R3中风险</b>等级、510只为R4，短期深度回撤未能同步反映在风险分级中。Wind数据显示，二季度末全市场持股市值占比超50%的4500余只基金风险等级分布于R2—R5，R3超1900只、R4超2600只。<br>
          <b>调整意愿不足：</b>在280只R3基金中，有<b>24只</b>7月跌幅超40%，不乏百亿级产品；财通成长优选、景顺长城沪港深精选等百亿基金7月以来跌幅亦超35%。多数公司选择按兵不动，仅极少数调整——东吴价值成长A、东吴多策略A（7月均跌超45%）已于4月底由R3上调至R4；华泰柏瑞7月20日更新了质量成长A、科技创新A等多只月跌超30%产品的评级。<br>
          <b>制度症结：</b>业内指出各机构评级标准与频率不一，存在<b>"同基不同级"</b>现象，机构缺乏主动调整动力，评级流于合规形式，需从破除现实障碍、理顺利益冲突入手。<br>
          <b>对基金行业影响：</b>风险评级失真直接冲击销售适当性管理→作为代销机构，腾安面临"以R3销售给保守型客户但实际波动达R4/R5"的适当性风险敞口，须自建波动率监测补位。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L3D35FUI0519D45U.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag high">适当性风险：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 公募托管一哥易主 (T+0 08-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募基金托管"一哥"易主·建行5.10万亿超越工行登顶·宽基ETF集中赎回成关键变量</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">08-03</span>
          </div>
        </div>
        <div class="card-body">
          <b>座次更替：</b>Wind数据显示，截至6月末<b>建设银行</b>公募基金托管总资产达<b>51040.15亿元</b>（市场占比12.87%）、较去年末增加2627.77亿元跃居首位；<b>工商银行</b>以50500.61亿元（占比12.73%）退居次席，上半年缩水<b>3171.51亿元</b>为缩量最大机构。招商、兴业、中信分列三至五位，托管资产分别为33224.10亿、31968.08亿、30878.46亿元。增量榜首为兴业银行（+2749.81亿元）。工行此前已连续四个季度居首。<br>
          <b>宽基赎回是主因：</b>上半年工行托管的宽基ETF规模由年初11701.81亿元收缩至3678.11亿元、缩水<b>超8000亿</b>，其中沪深300ETF华泰柏瑞净流出3361.21亿元、规模缩水至948.71亿元；权益类托管规模下降24.88%至17820.34亿元。资金从大盘宽基流向科技成长赛道，直接反映于托管数据。建行则凭代销渠道发力，权益类托管规模增277.18亿元、新发产品发行规模达4515亿元。<br>
          <b>格局特征：</b>托管业务"强者恒强"，上半年前五家合计占比约五成、前十家近八成且全为银行。"以销售换托管"惯例持续生效，指数化产品扩张对托管行的高频清算、流动性管理与综合服务能力提出更高要求。<br>
          <b>对基金行业影响：</b>托管份额与代销能力深度绑定→印证渠道议价权正是核心资产，腾安可借保有量优势在托管协同与费率谈判中争取更有利条件。
        </div>
        <div class="card-footer">
          <a href="https://www.ce.cn/xwzx/gnsz/gdxw/202608/t20260803_3123614.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·中国经济网</span></a>
          <span class="impact-tag medium">渠道格局：中</span>
        </div>
      </div>

      <!-- S0 Card 4: 中信证券称调整基本结束 (T+0 08-03 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 中信证券称A股调整基本结束·判定为拥挤交易修正而非去杠杆·8月修复概率提升</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">08-03</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心判断：</b>中信证券认为A股本轮调整更多是<b>拥挤交易的修正</b>，而非韩国式的去杠杆冲击，三点依据：① 整体杠杆水平安全，7月上涨股票数量接近全A一半、明显超过6月；② 相比全球历史上典型去杠杆行情，当前融资回落幅度并不算大；③ ETF市场呈现持续资金流入，科技类ETF提供充足流动性支持。局部流动性压力仍存于部分非核心AI股，但认为影响已基本消除。<br>
          <b>配置建议：</b>8月普遍修复概率提升，但并非简单超跌反弹——非AI板块负面叙事边际好转、资金环境支持适当修复。建议增配<b>能化、有色、非银和创新药</b>，科技内部需借反弹更加聚焦持仓。融通基金则提示流动性拐点渐近、AI产业趋势未改，科技或迎中期布局窗口；摩根士丹利基金判断当前是"由快速上涨向震荡整固的阶段转换，而非趋势反转"。<br>
          <b>外资印证：</b>截至二季度末沪深港通北向资金持仓市值<b>首次突破3万亿元</b>，QFII二季度调仓呈"头部化"特征；年内累计572家外资机构调研A股上市公司4161次，AI产业链吸引力持续凸显。<br>
          <b>对基金行业影响：</b>卖方主流观点由防御转向温和修复→腾安可适度恢复权益类产品的常规营销节奏，但须以均衡配置为主基调，避免重演单边押注。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L3D37QRL05568W0A.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·中信证券</span></a>
          <span class="impact-tag low">市场研判：中</span>
        </div>
      </div>

    </div>
  </div>

'''
s = s[:i] + S0_NEW + s[j:]

# --- 5. S2 新增一条：央行下阶段八大重点工作（08-03，P1）---
S2_ANCHOR = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 证监会召开财务造假综合惩防央地协同推进会'''
assert s.count(S2_ANCHOR) == 1, 's2 anchor'
S2_NEW = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 央行明确下阶段八大重点工作·发挥两项支持资本市场货币政策工具作用·深化金融开放</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">08-03</span>
          </div>
        </div>
        <div class="card-body">
          <b>风险化解：</b>中国人民银行会议明确下阶段八大重点工作。围绕稳妥化解重点领域风险，提出继续做好金融支持地方政府融资平台债务风险化解、推进融资平台市场化转型；强化宏观审慎管理和金融稳定保障体系，丰富宏观审慎和金融稳定管理工具箱，校正和阻断金融市场风险累积；<b>发挥好两项支持资本市场货币政策工具的作用</b>；提升存款保险履职效能；强化打击非法金融活动。<br>
          <b>改革开放：</b>要求积极稳妥开展央行间货币互换和本币结算合作；支持和便利更多境外机构参与<b>熊猫债</b>发行；统筹发展离岸人民币市场，支持上海提升跨境金融、离岸金融服务能力，巩固香港离岸人民币业务枢纽地位；深化跨境贸易和投融资便利化改革；推进人民币跨境支付系统建设，完善数字人民币跨境基础设施。会议同时提出综合运用并适时调整货币政策工具。<br>
          <b>对基金行业影响：</b>两项资本市场货币政策工具（证券基金保险互换便利、股票回购增持再贷款）继续发挥作用→为权益市场提供流动性托底预期，利好基金销售环境；跨境与离岸人民币深化则为QDII与跨境产品创造增量空间。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L3D37QRL05568W0A.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·中国人民银行</span></a>
          <span class="impact-tag medium">货币政策：中</span>
        </div>
      </div>

''' + S2_ANCHOR
s = s.replace(S2_ANCHOR, S2_NEW, 1)

# --- 6. S6 整卡替换 ---
S6_A = '<!-- ============ Section 6: 市场行情速览 ============ -->'
S6_B = '<!-- ============ Section 7: 关键时间线 ============ -->'
i = s.index(S6_A); j = s.index(S6_B, i)
assert i < j, 's6 range'
S6_NEW = S6_A + '''
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年8月3日（周一·早盘实时）·三大股指集体低开沪指报3817附近·上一交易日07-31沪指收3832.26涨0.72%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📉 A股08-03早盘（集体低开·科技硬件走弱）：</b><br>
              ▪ 开盘：上证 <b>3812.61</b>（<b>-0.51%</b>）·深成指 13497.10（-0.60%）·创业板指 3320.09（-0.71%）·科创50 1619.29（-1.02%）·沪深300 4561.82（-0.57%）<br>
              ▪ 09:51 实时：上证 <b>3817.14</b>（<b>-0.39%</b>），振幅0.51%，量比3.03，最高3827.64/最低3807.91<br>
              ▪ 开盘涨跌家数：2152家上涨、2551家下跌、824家平盘<br>
              ▪ 跌：存储器/HBM/半导体材料/PCB/光刻机/算力硬件/油气开采；涨：可控核聚变（江苏神通涨超9%）/人形机器人/AI应用/PEEK材料<br>
              ▪ 资金：央行开展630亿元7天逆回购（利率1.40%）+3000亿元隔夜逆回购，今日9255亿元到期，单日<b>净回笼5625亿元</b>；两市融资余额增46.58亿元至25809.68亿元；人民币中间价6.7898调贬4基点
            </div>
            <div>
              <b>📈 上一交易日07-31收盘（月末反攻）：</b><br>
              ▪ 上证 <b>3832.26</b>（+0.72%）·深成指 13578.93（+2.21%）·创业板指 <b>3343.96</b>（+3.06%）·科创50 1635.96（+2.99%）<br>
              ▪ 成交约2.54万亿，4691只上涨/728只下跌，101只涨停0只跌停<br>
              ▪ 7月全月：双创指数<b>均跌超20%</b>（创业板50跌23.16%、科创50跌23.97%）·沪深300跌<b>7.86%</b>·北证50逆势涨近5%<br>
              <b>📈 港股07-31收盘：</b>恒生指数 <b>25884.43</b>（+0.10%）·恒生科技 4829.22（+0.53%）·国企指数 8612.15（-0.38%），7月累涨约13%<br>
              <b>📈 美股07-31收盘：</b>道指 <b>52485.03</b>（+0.53%）·标普500 7489.72（+0.70%）·纳指 25373.85（+1.00%）
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：8月首个交易日A股<b>低开承压</b>，此前领涨的存储器、HBM、半导体材料、PCB、光刻机集体走弱，仅可控核聚变、人形机器人、AI应用逆势走强，风格延续"科技硬件退潮、题材轮动"。资金面偏紧——央行单日<b>净回笼5625亿元</b>，为月初流动性回收常态；两融余额小幅回升至2.58万亿。外部扰动：美股科技巨头遭"<b>财报杀</b>"，苹果与Meta营收增长但股价双双大跌，微软与亚马逊则获资金追捧，反映AI叙事进入"逐项审视投入产出效率"阶段；特朗普取消对伊朗袭击计划并称8月3日启动谈判，<b>布伦特原油一度跌7.3%</b>至81.55美元/桶（7月曾飙升近四分之一）。机构观点分歧收敛：中信证券判定本轮调整为拥挤交易修正、8月修复概率提升，摩根士丹利基金定性为"震荡整固而非趋势反转"。<b>盘中数据为08-03 09:51 实时快照，收盘数据以07-31为最近完整交易日。</b>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-08-03 09:51实时</span>
            <span class="source-tag">数据来源：同花顺iFind/澎湃新闻/金融界/新浪财经/证券时报</span>
          </div>
      </div>
  </div>
'''
s = s[:i] + S6_NEW + s[j:]

# --- 7. S7：先删最旧 07-22，再插入 08-03 ---
def del_tl(txt, date):
    pat = re.compile(
        r'[ \t]*(?:<!--[^\n]*-->\n)?[ \t]*<div class="timeline-item">\s*'
        r'<div class="timeline-dot[^"]*"></div>\s*'
        r'<div class="timeline-date">' + re.escape(date) + r'</div>\s*'
        r'<div class="timeline-title">[^<]*</div>\s*</div>\n+')
    m = pat.search(txt)
    assert m, 'timeline delete fail: ' + date
    return txt[:m.start()] + txt[m.end():]

s = del_tl(s, '2026-07-22')

TL_ANCHOR = '''      <!-- 08-02 时间线条目 (NEW) -->'''
assert s.count(TL_ANCHOR) == 1, 'tl anchor'
TL_NEW = '''      <!-- 08-03 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-03</div>
        <div class="timeline-title">公募前七月业绩大洗牌·翻倍基仅剩2只</div>
      </div>

''' + TL_ANCHOR
s = s.replace(TL_ANCHOR, TL_NEW, 1)

# --- 8. badge ---
s = s.replace(A_BADGE, N_BADGE)

# ============ 断言校验 ============
assert s != orig, 'no change'
assert s.count('<div') == s.count('</div>'), f"div imbalance {s.count('<div')}/{s.count('</div>')}"
assert 'Section 8' not in s and '待办跟踪' not in s and '腾安行动清单' not in s, 'S8 leaked'
assert 'timeline-desc' not in s, 'timeline-desc leaked'
assert s.count(N_BADGE) == 1 and s.count(A_BADGE) == 0, 'badge'
assert s.count(N_CTX) == 1, 'ctx'

# S0 段校验
s0 = s[s.index('<!-- ============ Section 0'):s.index('<!-- ============ Section 1')]
assert s0.count('<span class="section-title">今日焦点</span>') == 1, 'S0 title not exact'
assert s0.count('class="card p') == 4, f"S0 cards={s0.count('class=\"card p')}"
assert s0.count('date-tag">08-03<') == 4, 'S0 date-tag not all 08-03'
assert s0.count('<div class="action-box">') == 1, f"S0 action-box={s0.count('<div class=\"action-box\">')}"
assert s0.count('class="card p0"') == 1, 'S0 p0 count'
assert s0.count('target="_blank"') == 4, 'S0 source links'
assert s0.count('<div class="card-meta">') == 4, 'S0 card-meta'

# S7 校验
s7 = s[s.index('<!-- ============ Section 7'):]
d = re.findall(r'timeline-date">(\d{4}-\d{2}-\d{2})<', s7)
assert len(d) == len(set(d)), f'S7 duplicate dates: {d}'
assert d == sorted(d, reverse=True), f'S7 not desc: {d}'
assert 10 <= len(d) <= 12, f'S7 count={len(d)}'
assert d[0] == '2026-08-03', f'S7 newest={d[0]}'
assert d[-1] >= '2026-07-20', f'S7 oldest expired: {d[-1]}'
assert 'timeline-title' in s7 and s7.count('timeline-item') == len(d), 'S7 item mismatch'
for t in re.findall(r'timeline-title">([^<]*)<', s7):
    assert '/' not in t and '（' not in t, f'S7 title stacking: {t}'

# S2 校验
s2 = s[s.index('<!-- ============ Section 2'):s.index('<!-- ============ Section 3')]
assert s2.count('class="card p') == 4, f"S2 cards={s2.count('class=\"card p')}"

# ============ Phase 2: 写文件 ============
io.open(P, 'w', encoding='utf-8').write(s)
print('WRITE OK')
print('div:', s.count('<div'), '/', s.count('</div>'))
print('S0 cards=4 all 08-03, action-box=1')
print('S2 cards=', s2.count('class="card p'))
print('S7 dates:', d)
