# -*- coding: utf-8 -*-
"""
_update_0918.py — 基金看板 2026-09-18 日更
铁律：Phase1 全套断言通过才写文件；尾部闭合硬编码为常量；锚点 repr 已实测。
预期 div 漂移 = +3（S0 新增 1 个 P0 action-box） -6（S5 清 1 张 09-03 越界卡） = -3
"""
import io
import re
from datetime import date, timedelta

SRC = 'index.html'
TODAY = date.today()
UPPER = TODAY.strftime('%Y.%m.%d')
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
BADGE_NEW = '📅 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)
MARKER_NEW = '<!-- daily-update: %s -->' % TODAY.strftime('%Y-%m-%d')

FP_NEW = '上海证监|谢治宇乔|5只63个|外围扰动'

src = io.open(SRC, encoding='utf-8').read()
O_OPEN = src.count('<div')
O_CLOSE = src.count('</div>')
EXPECTED_DRIFT = 0


def dc(t):
    return t.count('<div')


def card_bounds(s, idx):
    """返回包含 idx 的 <div class="card pX"> 块的 (start, end)。
    depth 初值必须为 1（卡片自身 div 未计入扫描），否则会在 card-top 的 </div> 提前返回。"""
    start = s.rfind('<div class="card p', 0, idx)
    assert start > 0, 'card 起点定位失败'
    i = start + 4
    depth = 1
    pat = re.compile(r'<div|</div>')
    while depth > 0:
        m = pat.search(s, i)
        assert m, 'div 扫描越界'
        depth += 1 if m.group(0) == '<div' else -1
        i = m.end()
    return start, i


# ============================================================
# 1. marker（闸0）
# ============================================================
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', MARKER_NEW, src, count=1)

# ============================================================
# 2. header 数据区间 badge（动态计算）
# ============================================================
BADGE_RE = r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）'
assert len(re.findall(BADGE_RE, src)) == 1, 'badge 锚点不唯一'
src = re.sub(BADGE_RE, BADGE_NEW, src, count=1)

# ============================================================
# 3. content-fingerprint（闸6）
# ============================================================
FP_RE = r'(<meta name="content-fingerprint" content=")[^"]*(">)'
assert len(re.findall(FP_RE, src)) == 1, 'fingerprint 锚点不唯一'
src = re.sub(FP_RE, lambda m: m.group(1) + FP_NEW + m.group(2), src, count=1)

# ============================================================
# 4. Stats Bar：沪指卡 09-16 -> 09-17 收盘
# ============================================================
STATS_OLD = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3891.60</div>\n'
    '      <div class="stat-label">沪指9-16收盘·涨0.71%·沪深两市成交1.84万亿·放量2264亿</div>\n'
    '      <div class="stat-change up">▲ 创业板+1.96%·科创50+4.14%·超4100股上涨</div>\n'
    '    </div>'
)
STATS_NEW = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3875.60</div>\n'
    '      <div class="stat-label">沪指9-17收盘·跌0.41%·沪深两市成交1.82万亿·缩量160亿</div>\n'
    '      <div class="stat-change down">▼ 创业板-0.40%·科创50-0.61%·超2800股下跌</div>\n'
    '    </div>'
)
sb = src.find('<div class="stats-bar">')
sb_end = src.find('\n  </div>', sb)
assert sb > 0 and sb_end > sb, 'stats-bar 段定位失败'
assert src.count(STATS_OLD) == 1, 'Stats Bar 沪指卡锚点不唯一（可能误命中 S6）'
seg = src[sb:sb_end]
assert '3891.60' in seg and '3875.60' not in seg
src = src.replace(STATS_OLD, STATS_NEW, 1)

# ============================================================
# 5. S0 今日焦点：整块替换 4 张卡（2×09-18 + 2×09-17，卡1 P0 带 action-box）
# ============================================================
S0_CARDS = u'''      <!-- S0 Card 1 (09-18 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 上海证监局明确网络营销六大要求·9月30日实施·严禁与“网络大V”合作</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-18</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月18日「券商基金早参」（记者彭水萍）：上海证监局近日向辖区内的基金管理人、资产管理机构、基金销售机构下发关于做好《金融产品网络营销管理办法》（以下简称《办法》）落实工作的通知。《办法》已于2026年4月21日公布，<b>将于9月30日起正式实施</b>。<br>
          <b>六大要求：</b>①<b>合作主体</b>——不得与第三方互联网平台以外的任何其他组织或者个人（包括“网络大V”）合作开展金融产品网络营销；②<b>业务边界</b>——与第三方互联网平台合作应坚持业务独立、技术安全、数据保密，不得允许平台介入投资者招揽、开立账户、处理交易指令、办理清算交收、基金销售等证券基金业务环节；③<b>收费红线</b>——向第三方互联网平台支付费用不得直接或间接与客户开户量、交易量、手续费、资金量等业务指标挂钩或变相挂钩，不得通过支付不合理费用开展不正当竞争、扰乱市场秩序；④<b>事前评估</b>——委托平台提供服务时须建立事前评估机制，重点评估是否介入业务环节、是否混淆服务提供主体、是否保障投资者数据安全、是否合理收费且质价相符；⑤<b>转接渠道</b>——不得与未完成信息技术系统备案的第三方互联网平台开展涉及基金申购赎回转接渠道的合作，<b>存量转接渠道合作须在《办法》正式实施1年内完成整改</b>；⑥<b>信息报送</b>——每季度结束后10个工作日内报送与第三方互联网平台合作开展的转接渠道网络营销有关情况。<br>
          <b>自营App：</b>通知要求加强自主运营的移动应用程序（App）建设，引导投资者优先使用自身运营管理的App办理业务，并保障充足、稳定的信息技术投入，确保第三方互联网平台发生技术故障等突发事件时仍可持续提供服务；第三方互联网平台发生技术故障影响客户交易的，上海证监局将依法依规予以处置。<br>
          <b>每经点评：</b>上海证监局明确六大要求、严禁与“网络大V”合作，推动行业回归持牌经营本质。新规促使基金公司强化自营App建设，短期或影响流量依赖型机构的获客效率，但长期有利于降低营销成本、提升投资者适当性管理，促进行业竞争回归产品力与服务质量。<br>
          <b>对腾安启示：</b>距9月30日仅剩12天，须把“合作主体—业务边界—收费口径—事前评估—系统备案”五项做成可留痕清单逐项体检；其中最容易被穿透的是“按开户量/交易量挂钩结算”的历史合作协议，须在正式实施前完成重签或终止，否则1年整改期内的存量转接合作将始终带病运行。
        </div>
        <div class="card-footer">
          <a href="https://www.mrjjxw.com/articles/2026-09-18/4585050.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-18</span></a>
          <a href="https://jnzstatic.cs.com.cn/zzb/htmlInfo/133537.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·09-17</span></a>
          <a href="https://www.cs.com.cn/tzjj/etf/2026/09/18/detail_2026091810040022.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-18</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 合作体检→9月30日前完成全部第三方平台合作逐项评估与留档，重点核查是否存在按开户量/交易量/手续费挂钩结算的条款；<br>
            ② 备案核查→逐户确认合作平台信息技术系统备案状态，未备案的一律暂停基金申赎转接渠道合作，存量部分排定1年内整改时间表；<br>
            ③ 报送机制→建立“季度结束后10个工作日内”转接渠道营销情况报送流程与责任人，同步落地自营App承接预案。
          </div>
        </div>
      </div>


      <!-- S0 Card 2 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 谢治宇乔迁10.81亿参与通富微电定增·5只基金集体获配</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月17日报道（记者赵明超）：9月16日兴证全球基金公告，谢治宇管理的兴全社会价值三年持有混合、兴全合润混合、兴全合宜混合，以及乔迁管理的兴全新视野混合、兴全商业模式混合共<b>5只</b>基金参加通富微电非公开定向增发，<b>合计获配10.81亿元</b>。其中兴全合润获配<b>4.1亿元</b>、兴全商业模式优选获配<b>3.5亿元</b>、兴全合宜获配<b>2.3亿元</b>；谢治宇管理的3只合计<b>6.53亿元</b>，乔迁管理的2只合计<b>4.28亿元</b>。<br>
          <b>建仓成本：</b>通富微电向特定对象发行股票发行情况报告书显示，本次发行价格为<b>55.38元/股</b>，为发行底价的<b>106.15%</b>；截至9月16日通富微电股价<b>59.21元</b>。基金2026年中期报告显示，截至6月底上述几只基金均未持有通富微电，属全新仓位。<br>
          <b>基本面：</b>通富微电为集成电路封装测试服务商，今年上半年实现营业收入<b>160.41亿元</b>、同比增长<b>23.03%</b>，归母净利润<b>17.17亿元</b>、同比增长<b>316.77%</b>；本次募集资金总额<b>42.2亿元</b>，投向存储芯片封测产能提升、汽车等新兴应用领域封测产能提升、晶圆级封测产能提升等项目。<br>
          <b>经理观点：</b>谢治宇在中期报告中表示，上半年对海外算力、半导体设备、创新药等成长板块重点配置，“AI的飞速发展和传统行业的企稳才是投资主线”；同时提示当AI硬件投资进入第四年后，众多可投标的将进入去伪存真的分化阶段。Choice数据显示，截至二季度末谢治宇管理规模<b>392.75亿元</b>、乔迁<b>279.42亿元</b>。<br>
          <b>对腾安启示：</b>明星经理大额参与定增会成为短期话题与流量入口，但定增份额有锁定期、成本价与市价存在折溢价，客户若按“明星经理同款”跟买ETF或主题基金，承担的是完全不同的风险收益结构；详情页应把“定增参与”与“可申购基金持仓”明确区分，避免概念混同。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/791439" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 3 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 5只63个月摊余成本债基9月21日集体首发·80亿上限·认购费率分化</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报9月17日报道：包括路博迈、贝莱德、红土创新、财信、兴华基金在内的<b>5只</b>63个月封闭式摊余成本法债券基金将于<b>9月21日</b>集体首发。9月16日、17日，各家公募陆续发布基金份额发售公告，发行时间均定于9月21日起售，投资人可通过直销或代销渠道认购。<br>
          <b>发行安排：</b>路博迈、财信、兴华基金募集截止日暂定<b>12月18日</b>；贝莱德基金募集信心更足，拟于<b>10月20日</b>结束募集。<b>募集上限普遍为80亿元</b>。<br>
          <b>费率分化：</b>路博迈安瑞、贝莱德稳利初档认购费率为<b>0.3%</b>（贝莱德100万元以下0.3%、100万—500万元0.2%）；兴华安硕63个月封闭式债基则低至<b>0.15%</b>，且适用于500万元以下认购金额，500万元以上按笔收取1000元。投资者通过直销机构认购均不收取认购费用。<br>
          <b>产品来源：</b>这批产品属于9月14日获批的首批15只摊余成本法债基，发行主体还包括尚正、国融、华西、鹏安、百嘉、朱雀、联博、兴合、安联、易米等基金公司。有研报分析指出，摊余债基申报进一步扩围有望为债市带来结构性增量资金，配债需求预计将随产品获批、成立及建仓逐步释放。<br>
          <b>对腾安启示：</b>63个月封闭期叠加摊余成本法估值，净值曲线平滑、几乎无回撤，是存款搬家最直接的承接品种；但5年以上锁定期会显著牺牲客户资金灵活性，销售端必须把封闭期、估值方法与流动性代价前置披露，并按“底仓替代”而非“理财替代”定位推荐，同时对首发期费率差异做透明展示。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR1232bfaa-3273-2e05-4d33-3a23c1d4db5f" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·09-17</span></a>
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202609/t20260917_3219560.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 4 (09-18 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 外围扰动不改长期趋势·基金公司看好A股韧性·“科技+红利”杠铃成共识</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-18</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月18日报道（记者朱妍）：北京时间9月17日凌晨，美联储宣布将联邦基金利率目标区间上调25个基点，这场此前被市场预判为偏向“鸽派”的加息最终释放偏“鹰”信号。多家基金公司判断，货币紧缩带来的是短期扰动，叠加国内货币政策具有独立性且A股基本面具备支撑，长期可保持乐观，当下可采取<b>“科技+红利”的杠铃配置思路</b>。<br>
          <b>分歧在路径：</b>朱雀基金投研人士称“美联储没有说服市场这是一个预防式加息，反而一定程度上推升了‘加息周期开启’的预期”；永赢基金表示会议后市场对今年12月和2027年加息的预期进一步提升；宏利基金认为是否有第三次加息较大程度上取决于油价压力；国泰基金认为需等待数据推翻“增长强势、通胀黏性”的判断。<br>
          <b>对A股影响：</b>前海开源基金首席经济学家杨德龙表示，A股经过三季度大幅调整后科技股去泡沫过程基本完成，此前下跌已提前消化估值偏高与加息预期，影响是短期的；国联安基金认为美债高利率或带来外部估值约束，但国内利率仍处低位且存在下行空间，A股盈利有望进入修复通道，短期偏谨慎、长期乐观。<br>
          <b>配置落点：</b>金鹰基金宏观策略研究员金达莱表示近期偏向“科技+红利”杠铃——AI产业链短期仍需震荡整固，不宜追高科技，可在调整中关注供需偏紧、业绩确定性较强的核心环节；年末窗口预计高股息、低估值风格相对占优，除银行外可关注油气开采、航运港口、白色家电、乳品。汇丰晋信基金经理许廷全认为港股近一个月已先行反应，本次加息或仅带来短期震荡。永赢基金提示大类资产上铜的避险属性突出，美债和黄金可逢低关注但布局偏左侧。<br>
          <b>对腾安启示：</b>机构口径已从“要不要防风险”转向“如何在科技与红利之间配比例”，建议把投顾组合与主题页的默认展示改成杠铃结构（一端科技成长、一端高股息低波），并对追高型单主题产品加挂波动率与回撤提示，降低加息扰动期的非理性申赎。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/792021" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·09-18</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''

s0_start = src.find('      <!-- S0 Card 1')
S0_TAIL = '\n\n\n    </div>\n  </div>\n'
s0_end = src.find(S0_TAIL, s0_start)
assert s0_start > 0 and s0_end > s0_start, 'S0 段定位失败'
assert src.count('      <!-- S0 Card 1') == 1, 'S0 Card1 锚点不唯一'
old_s0 = src[s0_start:s0_end]
EXPECTED_DRIFT += dc(S0_CARDS) - dc(old_s0)
src = src[:s0_start] + S0_CARDS + src[s0_end:]

# S0 section-context 单独改
CTX_OLD = '<span class="section-context">9月17日 · 4条今日要闻</span>'
CTX_NEW = '<span class="section-context">9月18日 · 4条今日要闻</span>'
assert src.count(CTX_OLD) == 1, 'S0 section-context 锚点不唯一'
src = src.replace(CTX_OLD, CTX_NEW, 1)

# ============================================================
# 6. S1：清 2 张 09-03 越界卡（T-14 边界 09-04），补 2 张新卡
# ============================================================
S1_NEW_A = u'''      <!-- S1 Card: 含权债基规模3.35万亿 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 含权债基总规模达3.35万亿创新高·二级债基2.3万亿成主力·承接存款搬家</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          中证网9月17日报道：据中金公司测算，<b>2026年居民定期存款到期规模约75万亿元</b>，而多家银行定期存款利率已降至“1字头”，传统理财收益空间持续收窄。华源证券数据显示，截至2026年二季度末，全市场含权债基总规模已达<b>3.35万亿元</b>，较一季度末环比增长<b>10.8%</b>，再创历史新高，其中二级债基规模达<b>2.3万亿元</b>，稳居主力地位。<br>
          <b>产品逻辑：</b>在“资产荒+高波动”并存的环境下，“能投股但不全靠股”的含权债基成为承接居民财富再配置的重要工具——权益上行与结构性行情中，权益及可转债仓位捕捉机会、提升组合弹性；市场转入调整阶段时，80%以上的固收底仓对冲权益波动、平滑回撤。<br>
          <b>供给节奏：</b>低利率环境下含权债基发行提速，富国嘉裕债券型基金（A类028964、C类028965）于<b>9月18日</b>结束募集，定位二级债基，债券资产投资比例不低于基金资产的<b>80%</b>，股票、存托凭证、股票型与混合型基金及可转债等权益类资产合计投资比例为<b>5%—20%</b>。<br>
          <b>对腾安启示：</b>存款到期潮叠加含权债基规模创新高，是线上“理财替代”需求最确定的承接方向；建议把二级债基/含权债基单列一层，并突出“权益仓位区间+最大回撤+持有期”三要素，避免客户仅按近一年收益率排序、在权益仓位悄然抬升后承受超预期波动。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/ssgs/07/2026/09/17/detail_2026091710039847.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''

S1_NEW_B = u'''      <!-- S1 Card: 投教纳入国民教育体系 (09-18 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 基金公司与高校共建学分课·投教纳入国民教育体系走深走实</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-18</span>
          </div>
        </div>
        <div class="card-body">
          中证网9月18日报道：多家公募已把投资者教育做成<b>计入学分</b>的正式课程。鹏华基金自2022年起已先后推出六期线下国民教育高质量投教学分课程；易方达基金自2022年以来持续在武汉大学、华南理工大学、中国政法大学等高校开课，其中武汉大学“公募基金投资运作与ESG实践”已合作第五年、累计约<b>400名</b>学生选课，华南理工大学“公募基金理论与实践”三年累计覆盖<b>200余名</b>本科生；广发基金与华南理工大学、中山大学合作开设学分制选修课已有四年，累计覆盖学生超<b>300人</b>；德邦基金自2022年起参与授课支持，累计覆盖师生超<b>1600人次</b>。<br>
          <b>数字化扩散：</b>2025年春季鹏华基金联合上海财经大学等推出的“资产配置一线实战课程”获得<b>50万+</b>播放量、覆盖<b>15所</b>高校；招商基金提供“产品经理说ETF”等线上投教内容作为课外延伸阅读材料，博时基金输出标准化课件、基金基础知识、模拟投资教学案例与投教短视频素材，诺安基金自主开发大学生专属投教课件。<br>
          <b>可复制化：</b>诺安基金计划把成功案例形成可复制、可落地、可推广的形式推向更多院校；博时基金的中长期目标是推动形成稳定、可持续的校企共建学分课程。<br>
          <b>对腾安启示：</b>投教正从“营销物料”升级为“可计入学分的基础金融素养课程”，内容生产出现明显的规模化与低成本化；代销平台可把高校投教内容做二次分发，在年轻客群中建立品牌心智与首次开户入口，这比单纯的收益率榜单更具长期留存价值。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/tjdh/2026/09/18/detail_2026091810039989.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-18</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>'''

cutoff = (TODAY - timedelta(days=14)).strftime('%m-%d')
s1_hdr = src.find('Section 1')
s2_hdr = src.find('Section 2')
old_idx = []
for m in re.finditer(r'date-tag">(\d{2})-(\d{2})<', src):
    if s1_hdr < m.start() < s2_hdr:
        tag = '%s-%s' % (m.group(1), m.group(2))
        if tag < cutoff:
            old_idx.append(m.start())
assert len(old_idx) == 2, 'S1 越界卡数 != 2（实际 %d）' % len(old_idx)
b1 = card_bounds(src, old_idx[0])
b2 = card_bounds(src, old_idx[1])
assert b1[1] < b2[0], 'S1 越界卡顺序异常'
# 每张卡后紧跟 '\n\n' 分隔符，一并删除
rem = src[b1[0]:b2[1]]
assert src[b2[1]:b2[1] + 2] == '\n\n', 'S1 越界卡尾部分隔符异常'
EXPECTED_DRIFT -= dc(rem)
EXPECTED_DRIFT += dc(S1_NEW_A) + dc(S1_NEW_B)
src = src[:b1[0]] + S1_NEW_A + '\n\n' + S1_NEW_B + '\n\n' + src[b2[1] + 2:]

# ============================================================
# 7. S5：清 1 张 09-03 越界卡（T-14 边界 09-04）
# ============================================================
s5_hdr = src.find('Section 5')
s6_hdr = src.find('Section 6')
old5 = []
for m in re.finditer(r'date-tag">(\d{2})-(\d{2})<', src):
    if s5_hdr < m.start() < s6_hdr:
        tag = '%s-%s' % (m.group(1), m.group(2))
        if tag < cutoff:
            old5.append(m.start())
assert len(old5) == 1, 'S5 越界卡数 != 1（实际 %d）' % len(old5)
c1 = card_bounds(src, old5[0])
assert src[c1[1]:c1[1] + 2] == '\n\n', 'S5 越界卡尾部分隔符异常'
EXPECTED_DRIFT -= dc(src[c1[0]:c1[1]])
src = src[:c1[0]] + src[c1[1] + 2:]

# ============================================================
# 8. S6 市场行情速览：09-16 -> 09-17 收盘
# ============================================================
S6_START = src.find('<div class="card p3">', src.find('Section 6'))
S6_TAIL = '      </div>  </div>\n'
s6_end = src.find(S6_TAIL, S6_START)
assert S6_START > 0 and s6_end > S6_START, 'S6 段定位失败'
S6_KEEP = len('      </div>')

S6_NEW = u'''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-17）·沪指3875.60 -0.41%·两市成交1.82万亿缩量160亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-17收盘·冲高回落）</b><br>
              上证指数 <b>3875.60</b> <span style="color:#52c41a;">-0.41%</span><br>
              深证成指 <b>13409.91</b> <span style="color:#52c41a;">-0.33%</span><br>
              创业板指 <b>3298.31</b> <span style="color:#52c41a;">-0.40%</span><br>
              沪深300 <b>4460.16</b> <span style="color:#52c41a;">-0.45%</span><br>
              科创50 <b>1606.29</b> <span style="color:#52c41a;">-0.61%</span><br>
              北证50 <b>1026.00</b> <span style="color:#52c41a;">-1.37%</span><br>
              沪深两市成交 <b>1.82万亿</b>·较上日缩量约160亿<br>
              全市场超2800只个股下跌
            </div>
            <div>
              <b>港股与美股（09-17收盘）</b><br>
              恒生指数 <b>24604.29</b> <span style="color:#52c41a;">-0.44%</span><br>
              恒生科技 <b>4310.74</b> <span style="color:#52c41a;">-0.34%</span><br>
              国企指数 <b>8175.36</b> <span style="color:#52c41a;">-0.38%</span><br>
              道琼斯 <b>51778.04</b> <span style="color:#dc2626;">+0.61%</span><br>
              纳斯达克 <b>26418.30</b> <span style="color:#dc2626;">+1.69%</span><br>
              标普500 <b>7637.76</b> <span style="color:#dc2626;">+1.14%</span><br>
              布伦特原油104.82美元 <span style="color:#52c41a;">-0.95%</span>·现货黄金4341.01美元 <span style="color:#dc2626;">+1.84%</span>·美债10年期回落至4.945%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>指数波澜不惊、结构大迁徙——贵金属板块重挫<b>5.37%</b>（11只成分股全数下跌，黄金概念主力净流出49.15亿元），白银跌6.00%、黄金跌5.15%，对隔夜金价跳水补跌；算力硬件全线退潮，PCB概念单日失血96.34亿元、元件净流出77.59亿元。资金转向低位：汽车行业全天净流入37.1亿元居首，种植业涨3.83%、种子涨7.86%领涨，CRO涨2.56%，医药板块相对强势；油运方向招商轮船涨停、中远海能A股涨6.61%。海外方面，美股在加息次夜集体修复，费城半导体指数涨<b>3.14%</b>，Arm涨8.57%、英特尔涨7.67%、AMD涨6.36%，英伟达CEO黄仁勋表态明年芯片销量将翻倍；10年期美债收益率跌破5%回落至4.945%，但CME FedWatch显示10月再加息25个基点概率升至53.1%。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-17收盘</span>
          <span class="source-tag">数据来源：上海证券报/中国证券网、每日经济新闻、中国基金报、新华社（09-17—09-18）</span>
        </div>
      </div>'''
EXPECTED_DRIFT += dc(S6_NEW) - dc(src[S6_START:s6_end + len(S6_TAIL)])
src = src[:S6_START] + S6_NEW + src[s6_end + S6_KEEP:]

# ============================================================
# 9. S7 时间线：重写 12 条（增 09-18×4，删 09-16 摊余债基获批 + 09-15 业绩差 + 09-14 + 09-11）
# ============================================================
S7_ITEMS = [
    ('red', '2026-09-18', '网络营销六大要求·9月底实施'),
    ('blue', '2026-09-18', '谢治宇乔迁10.81亿定增'),
    ('blue', '2026-09-18', '5只摊余债基9月21日首发'),
    ('blue', '2026-09-18', '基金公司看好A股韧性'),
    ('red', '2026-09-17', '年内新发基金规模破8000亿'),
    ('blue', '2026-09-17', '公募逆势布局冷门赛道'),
    ('blue', '2026-09-17', '次新基金快速建仓·机构调研'),
    ('blue', '2026-09-17', '公募密集调整QDII申购限额'),
    ('blue', '2026-09-16', '科技主题基金延长募集45天'),
    ('blue', '2026-09-16', '首批创业板算力ETF相继成立'),
    ('blue', '2026-09-16', '投顾组合腾挪·加码医药黄金'),
    ('red', '2026-09-15', '中国结算发布公募登记数据交换指引'),
]
s7_start = src.find('      <div class="timeline-item">')
S7_TAIL = '\n\n    </div>\n\n  </div>\n\n</div>'
s7_end = src.find(S7_TAIL, s7_start)
assert s7_start > 0 and s7_end > s7_start, 'S7 段定位失败'
assert src.count('      <div class="timeline-item">') == 12, 'S7 起点锚点数 != 12'

blocks = []
for color, d, t in S7_ITEMS:
    assert len(t) <= 25, 'S7 标题超25字：%s (%d)' % (t, len(t))
    blocks.append(
        '      <div class="timeline-item">\n'
        '        <div class="timeline-dot %s"></div>\n'
        '        <div class="timeline-date">%s</div>\n'
        '        <div class="timeline-title">%s</div>\n'
        '      </div>' % (color, d, t)
    )
EXPECTED_DRIFT += dc('\n'.join(blocks)) - dc(src[s7_start:s7_end])
src = src[:s7_start] + '\n'.join(blocks) + src[s7_end:]

# ============================================================
# Phase1 断言（不通过不写文件）
# ============================================================
N_OPEN = src.count('<div')
N_CLOSE = src.count('</div>')
print('div: %d/%d -> %d/%d  drift=%d (expected %d)' % (
    O_OPEN, O_CLOSE, N_OPEN, N_CLOSE, N_OPEN - O_OPEN, EXPECTED_DRIFT))
assert N_OPEN - O_OPEN == EXPECTED_DRIFT, 'div 漂移与预期不符'
assert N_OPEN == N_CLOSE, 'div 不平衡'

assert src.count('</div>>') == 0, '存在游离 </div>>'
assert 'S8' not in src and '待办跟踪' not in src and '腾安行动清单' not in src, 'S8 残留'

assert MARKER_NEW in src, 'marker 未更新'
assert BADGE_NEW in src, 'badge 未更新'
assert FP_NEW in src, 'fingerprint 未更新'

# S0 六项
s0 = src[src.find('Section 0'):src.find('Section 1')]
assert s0.count('<div class="card p') == 4, 'S0 卡数 != 4'
assert s0.count('class="action-box"') == 1, 'S0 action-box 数 != 1'
assert s0.count('date-tag') == 4, 'S0 date-tag 数 != 4'
tags = re.findall(r'date-tag">(\d{2})-(\d{2})<', s0)
assert tags.count(('09', '18')) == 2, 'S0 09-18 date-tag 数 != 2'
assert tags.count(('09', '17')) == 2, 'S0 09-17 date-tag 数 != 2'
assert '<span class="section-title">今日焦点</span>' in s0, 'S0 title 不是「今日焦点」'
assert '<span class="section-context">9月18日 · 4条今日要闻</span>' in s0, 'S0 context 错'
# 链接数实算：卡1=3（每经/中国证券报/中证网）+ 卡2=1 + 卡3=2（中国基金报/中国经济网）+ 卡4=1 = 7
assert s0.count('target="_blank"') == 7, 'S0 源链接数 != 7（实际 %d）' % s0.count('target="_blank"')

body = re.sub(r'<style.*?</style>', '', src, flags=re.S)
for m in re.finditer(r'<div class="card-meta">(.*?)</div>', body, re.S):
    inner = m.group(1)
    assert 'priority-tag' in inner and 'date-tag' in inner, 'card-meta 结构异常：%s' % inner[:60]

# S7 条数与降序
s7 = src[src.find('Section 7'):]
assert s7.count('      <div class="timeline-item">') == 12, 'S7 条数 != 12'
assert s7.count('timeline-desc') == 0, 'S7 存在 timeline-desc'
dates = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', s7)
assert dates == sorted(dates, reverse=True), 'S7 日期非降序'
for t in re.findall(r'<div class="timeline-title">(.*?)</div>', s7):
    assert len(t) <= 25, 'S7 标题超25字：%s' % t

# S1 / S2 数量
s1 = src[src.find('Section 1'):src.find('Section 2')]
s2 = src[src.find('Section 2'):src.find('Section 3')]
assert s1.count('<div class="card p') == 6, 'S1 卡数 != 6（实际 %d）' % s1.count('<div class="card p')
assert s2.count('<div class="card p') == 4, 'S2 卡数 != 4'

# T-14：所有 date-tag >= 09-04
for mm, dd in re.findall(r'date-tag">(\d{2})-(\d{2})<', src):
    assert '%s-%s' % (mm, dd) >= cutoff, 'date-tag 越界：%s-%s < %s' % (mm, dd, cutoff)

assert src.count('\ufffd') == 0, '存在 U+FFFD 乱码'

for bad in ('so.html5.qq.com', 'toutiao', 'stcn.com', 'cls.cn', '21jingji.com',
            'yicai.com', 'guba.eastmoney.com', '163.com/dy', 'dy.163.com',
            'jrj.com.cn', 'sohu.com', 'k.sina.com.cn'):
    assert bad not in src, '黑名单命中：%s' % bad

assert '企鹅号' not in src and '网易号' not in src and '搜狐号' not in src
assert '财经早报' not in src and '基金日报' not in src

print('Phase1 断言全部通过，写入文件…')
io.open(SRC, 'w', encoding='utf-8').write(src)
print('DONE')
