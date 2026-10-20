# -*- coding: utf-8 -*-
import re, io, sys
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = open(P, encoding='utf-8').read()
TODAY = date.today()
o0, c0 = s.count('<div'), s.count('</div>')
print('BASE div open/close =', o0, c0)


def dr(tag):
    print('  [dr:%s] open=%d close=%d  (drift_o=%+d drift_c=%+d)'
          % (tag, s.count('<div'), s.count('</div>'),
             s.count('<div') - o0, s.count('</div>') - c0))


def one(s, sub):
    assert s.count(sub) == 1, '锚点不唯一(%d): %r' % (s.count(sub), sub[:60])
    return s.index(sub)


# ==================== Phase 0: head 元信息（闸0/闸6/闸8/闸1） ====================
s2 = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
            '<!-- daily-update: %s -->' % TODAY, s, count=1)
assert s2 != s
s = s2
assert '<!-- daily-update: %s -->' % TODAY in s
print('OK marker ->', TODAY)

FP = '首批18只|央行拟设|监管通报|ETF资金'
s2 = re.sub(r'<meta name="content-fingerprint" content="[^"]*">',
            '<meta name="content-fingerprint" content="%s">' % FP, s, count=1)
assert s2 != s
s = s2

DESC = ('首批18只主动ETF获批 沪深各9只|央行拟设非银流动性支持工具|'
        '监管通报境外调研违规 5家机构|ETF资金净流入307亿元|'
        '沪指10-19收3730.92 纳指涨1.11%')
s2 = re.sub(r'<meta name="description" content="[^"]*">',
            '<meta name="description" content="%s">' % DESC, s, count=1)
assert s2 != s
s = s2
print('OK fingerprint/description')

lo = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
hi = TODAY.strftime('%Y.%m.%d')
s2 = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
            '📅 数据区间：%s — %s（每日更新）' % (lo, hi), s, count=1)
assert s2 != s
s = s2
print('OK 数据区间 ->', lo, '—', hi)

# ==================== Phase 1: Stats Bar ====================
STATS = '''    <div class="stat-card">
      <div class="stat-number">18只</div>
      <div class="stat-label">首批主动ETF获批·沪深各9只·最快10月23日开售·单只上限20亿元</div>
      <div class="stat-change up">▲ 18只产品有望带来约360亿元增量资金</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3730.92</div>
      <div class="stat-label">沪指10-19收盘·涨0.39%·全市场成交14488亿·缩量1203亿</div>
      <div class="stat-change up">▲ 银行石化家电军工领涨·超3100只个股下跌</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">56只</div>
      <div class="stat-label">本周（10月19日—23日）新基金发行·指数型27只·FOF 10只</div>
      <div class="stat-change up">▲ 仅10月19日就有43只启动·上周13只成立近40亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">307亿</div>
      <div class="stat-label">10-19 ETF九大类全线净流入·宽基212亿占近七成·货币39.53亿</div>
      <div class="stat-change up">▲ 中证500ETF南方单只净流入41.39亿居首</div>
    </div>
'''
st = s.index('    <div class="stat-card">')
en = one(s, '  </div>\n<div class="main">')
assert s.count('    <div class="stat-card">') == 4
assert s[st:en].count('<div class="stat-card">') == 4
old = s[st:en]
s = s[:st] + STATS + s[en:]
print('OK Stats Bar'); dr('stats')

# ==================== Phase 2: S0 四卡全换 ====================
C1 = '''      <!-- S0 Card 1 (10-20 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 首批18只主动ETF获批·沪深各9只·最快10月23日开售·单只上限20亿元</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-20</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月20日报道（记者闫军、方丽）：首批18只主动ETF于<b>10月19日晚间</b>获批，基金公司火速定档，最快<b>10月23日（本周五）</b>开售，不少公司称“只卖5天”；记者从渠道处了解到各家基本维持<b>20亿元</b>销售上限，18只产品有望带来约<b>360亿元</b>增量资金。另有券商人士表示，按当前排期节奏，首批18只主动ETF或于<b>11月23日</b>上市。<br>
          <b>18家名单（每经券商基金早参）：</b>上交所9只来自<b>易方达、华夏、永赢、摩根、华泰柏瑞、汇添富、华安、招商、平安</b>基金；深交所9只来自<b>南方、富国、大成、鹏华、工银瑞信、华宝、国泰、天弘、建信</b>基金。新华财经10月20日早报称，证监会同意首批18只主动ETF注册，沪深交易所表示将认真做好发行上市工作、推动产品平稳落地。<br>
          <b>机制与效率：</b>富国基金对比场外主动基金指出，主动ETF可在交易时段内实时买卖、盘中锁定价格，卖出后资金当日即可用，而场外基金按当日收市净值申赎、无法事先预知成交价，赎回款通常需数个交易日到账；信息披露上，场外基金按季度公布前十大重仓股，主动ETF则每个交易日披露PCF申赎清单。平安基金表示旗下主动ETF将增设<b>季度可评估分红</b>设计。<br>
          <b>策略定位：</b>首批产品整体聚焦市场容量空间较大的稳健型策略，基金名称中多见“红利、均衡、质量”等关键词。大成基金称红利资产在低利率环境下比较优势愈发凸显，可与科技成长构成“哑铃型”配置；汇添富指数与量化投资部副总监吴振翔指出，均衡策略的核心并非行业权重平均分配，而是“风险与收益的均衡、短期波动与长期成长的均衡”。<br>
          <b>回应“每日持仓披露是否掣肘主动管理”：</b>华泰柏瑞主动权益投资部联席总监杨景涵认为，与其说是限制，不如说是一种促使提升的力量——机制上要求基金经理风格定位清晰、谨守投资原则与流程、不盲目过度换手，并十分注重投资标的流动性；天弘基金量化投资部基金经理表示，量化投资持仓很分散、建仓周期很可能只需1天，“抄作业”没有意义。<br>
          <b>机构备战：</b>南方基金搭建“主动基金经理＋ETF运营”双轨管理模式，并完成投研制度、技术系统、风控流程全流程升级；鹏华基金在等待获批的三个月中开展“主动ETF专项调研活动”，反馈显示投资者对运作透明度、策略稳定性、流动性安排、申赎机制及风险揭示最为关心。<br>
          <b>对腾安启示：</b>主动ETF打通“场内交易＋主动管理＋每日透明”，货架须新增“主动／被动＋场内／场外＋持仓披露频率”三维标签，禁止把主动ETF与被动指数ETF并列混排；宣传“360亿元增量资金”须同步提示其为发行上限推算值而非实际募集规模，首批产品策略以红利、均衡等稳健型为主，不得暗示高弹性收益。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR32628dfa-33ed-195b-a234-3a2466eb9152" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-20</span></a>
          <a href="https://new.qq.com/rain/a/20261020A042CU00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·10-20</span></a>
          <a href="https://finance.sina.com.cn/jjxw/2026-10-20/doc-inivvnpt7555440.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·新华财经·10-20</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 货架标签→新增“主动ETF”独立分类，把管理费档位、PCF每日披露、策略类型（红利／均衡／质量／大盘成长）与发行上限做成默认字段，与被动宽基ETF分开陈列；<br>
            ② 销售话术→“只卖5天”“单只上限20亿元”须写清起止日期与配售规则，禁止把募集额度上限包装成收益预期或“稀缺抢购”；<br>
            ③ 适当性→每日持仓透明不等于低风险，详情页须前置业绩比较基准、风格定位与最大回撤口径，并对跟随每日持仓“抄作业”的行为做明确风险提示。
          </div>
        </div>
      </div>

'''

C2 = '''      <!-- S0 Card 2 (10-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 央行拟设非银机构大额赎回流动性支持工具·适用银行理财子公司与公募基金管理人</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-20</span>
          </div>
        </div>
        <div class="card-body">
          新华社北京10月19日电（记者吴雨、潘禹杰；中国经济网、中国网10月20日转载）：中国人民银行行长潘功胜<b>10月19日</b>在2026金融街论坛年会开幕式上宣布，央行将会同金融监管总局、中国证监会<b>设立应对非银机构大额赎回的流动性支持工具</b>，目的是建立债券市场稳定机制，构成人民银行宏观审慎管理的一项新工具。<br>
          <b>启用情景与约束：</b>工具综合权衡防范金融市场体系的系统性风险和道德风险，在资管机构面临群体性流动性风险、债券市场出现“赎回—抛售”负向循环的特定情景时启用；与央行开展操作必须满足宏观审慎要求并<b>提供高等级抵押品</b>，以防止金融市场定价扭曲、形成兜底幻觉、维护市场纪律。潘功胜表示，将在公开市场业务公告中明确工具操作相关要素。<br>
          <b>适用机构：</b>银行理财子公司、<b>公募基金管理人</b>，以及对应的银行母行、证券母公司等。<br>
          <b>同批其他举措：</b>扩大常备借贷便利（SLF）适用机构范围，进一步纳入境内外资法人银行，并明确全国性银行适用同样操作安排，实现对境内存款类金融机构全覆盖；推动银行间与交易所债券市场互联互通落地；试点允许<b>8家</b>中资和外资人民币境外清算行在境内银行间外汇市场开展自营交易。<br>
          <b>配套文件：</b>同日中国人民银行会同科技部等10个部门发布《关于金融支持建设北京（京津冀）、上海（长三角）、粤港澳大湾区国际科技创新中心的指导意见》，推动再贷款、债券市场“科技板”、跨境投融资等政策在有关地区加大投入和先行先试。<br>
          <b>对腾安启示：</b>该工具把“资管机构赎回—抛售负向循环”纳入央行宏观审慎工具箱，但明确以高等级抵押品与宏观审慎要求为前置条件、强调防范兜底幻觉，属极端情景下的流动性后盾而非日常收益保障；债券型与“固收+”产品的风险提示不得引用该工具暗示“有央行兜底”，货架仍须按底层资产、久期与杠杆水平披露回撤来源，并在债市波动期同步提示赎回安排与流动性风险。
        </div>
        <div class="card-footer">
          <a href="https://www.ce.cn/xwzx/gnsz/gdxw/202610/t20261020_3264689.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·新华社·10-20</span></a>
          <a href="https://news.china.com.cn/2026-10/20/content_118740413.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网财经·新华社·10-20</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

'''

C3 = '''      <!-- S0 Card 3 (10-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 监管通报券商为基金境外调研买单·3家券商与2家基金公司被点名·3名责任人追责</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-20</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻“券商基金早参”（腾讯新闻10月20日刊发，每经记者彭水萍、编辑赵云）：监管最新集中通报一批证券基金公司投研人员调研行为违规的检查与处理情况，<b>3家证券公司、2家基金公司</b>被“点名”，另有<b>3名</b>相关责任人被直接追责。<br>
          <b>三类违规：</b>①部分基金公司参加证券公司研究所组织的境外调研活动时，存在由证券公司承担专家咨询、调研门票等费用的情形，反映相关证券公司、基金公司内部控制有效性不足；②个别基金公司从业人员因私出国旅游的往返机票、酒店等费用由证券公司支付，违反《证券期货经营机构及其工作人员廉洁从业规定》；③个别证券公司高管不配合检查，违反《证券基金经营机构董事、监事、高级管理人员及从业人员监督管理办法》。<br>
          <b>处理措施：</b>对存在不配合检查情形的G1证券公司采取监管谈话，对该公司副总裁兼研究所总经理胡某、研究所副所长孔某采取监管谈话并责令公司从严处分；对H、G2两家证券公司和F、H两家基金公司采取出具警示函；对H基金公司基金经理马某采取责令改正，并要求公司严肃内部追责。<br>
          <b>后续要求：</b>各证券基金公司须对照规则和监管要求开展自查自纠、举一反三、切实整改，退回超标或不当开支，对违反规定的人员开展内部问责；各证监局加强日常监管，将交易佣金使用管理情况纳入年度现场检查关注要点，聚焦佣金分配、对外调研、人员管理等重点领域补齐制度短板，健全事前教育提醒、事中监督约束、事后追责问责的闭环管理机制。<br>
          <b>行业背景：</b>自《公开募集证券投资基金证券交易费用管理规定》实施以来，券商研究所与基金公司之间以“派点”为轴心的利益生态正被打破，新规以“正面清单”和“费率封顶”圈定佣金能买什么、向谁买、买多贵、怎么分；本次通报说明监管排查已从佣金费率延伸到境外调研与人员行为管理等隐蔽环节。<br>
          <b>对腾安启示：</b>监管已把“券商研究所—基金经理”之间的费用往来列为佣金改革后的重点排查对象。腾安与券商研究所、外部专家的合作须建立费用承担与留痕台账，凡专家咨询、调研门票、差旅住宿一律不得由合作方代付；对投研人员外部调研活动须实行事前审批与事后凭证双核查，并把廉洁从业要求写进供应商与第三方服务协议。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20261020A042CU00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·10-20</span></a>
          <a href="https://finance.sina.com.cn/roll/2026-10-20/doc-inivvnpx6640756.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·10-20</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

'''

C4 = '''      <!-- S0 Card 4 (10-20 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 ETF资金全线净流入·10月19日九大类合计约307亿元·宽基212亿占近七成</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-20</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇10月20日ETF资金流向观察（新浪财经同日转载）：<b>10月19日</b>ETF市场资金面呈大幅净流入格局，<b>九大类ETF全线净流入、当日无一大类净流出</b>，合计净流入约<b>307亿元</b>。其中宽基指数ETF净流入<b>212亿元</b>、占全部净流入的近七成，位居首位；货币ETF净流入<b>39.53亿元</b>、行业主题ETF净流入<b>23.23亿元</b>、信用债指数ETF净流入<b>12.97亿元</b>，跨境与商品ETF分别净流入6.28亿元和5.27亿元。<br>
          <b>宽基内部：</b>净流入榜单中宽基ETF占据12席；<b>中证500ETF南方</b>（510500）单日净流入<b>41.39亿元</b>、最新规模436.35亿元，居全市场首位；中证500与中证1000方向6只产品合计净流入83.49亿元，中小盘方向增持力度突出。行业主题方面，科创半导体ETF华夏净流入<b>23.22亿元</b>居净流入榜单第三位，与半导体设备ETF国泰合计净流入30.72亿元，机器人ETF博时净流入5.34亿元。<br>
          <b>流出端：</b>整体温和，当日净流出榜单中仅国债政金债ETF招商一只产品净流出超过5亿元（<b>-8.24亿元</b>），其余产品单只流出均在3亿元以内；债券板块内部品种分化鲜明，信用债、超长端及长端国债方向3只产品合计净流入11.66亿元，国债政金债ETF招商却居净流出首位。<br>
          <b>对腾安启示：</b>宽基ETF持续获增持、且中小盘方向力度突出，说明本轮流入以指数化托底为主而非赛道押注，与同期科创50跌2.17%、半导体材料设备方向走弱形成对照。货架展示ETF资金流向时必须标明统计口径（大类／单品、净流入额与最新规模）与数据日期，不得把单日净流入等同于产品业绩，也不得用“九大类全线净流入”暗示无风险。
        </div>
        <div class="card-footer">
          <a href="https://www.gelonghui.com/live/2718738" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·10-20</span></a>
          <a href="https://finance.sina.com.cn/stock/bxjj/2026-10-20/doc-inivvnpx6635180.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·格隆汇·10-20</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

i0 = one(s, '<!-- ============ Section 0')
i1 = one(s, '<!-- ============ Section 1')
st = one(s, '      <!-- S0 Card 1')
assert i0 < st < i1
en = s.rindex('    </div>\n  </div>', i0, i1)
assert s[st:en].count('<div class="card p') == 4, s[st:en].count('<div class="card p')
s = s[:st] + C1 + C2 + C3 + C4 + '    </div>\n  </div>' + s[en + len('    </div>\n  </div>'):]
print('OK S0'); dr('S0')

# ==================== Phase 3: S6 行情卡 ====================
S6 = '''                        <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股、美股统一10-19收盘·沪指3730.92 +0.39%｜纳指涨1.11%芯片股结束八连跌</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-19收盘）</b><br>
              上证指数 <b>3730.92</b> <span style="color:#dc2626;">+0.39%</span>（+14.64点）<br>
              深证成指 <b>11817.42</b> <span style="color:#dc2626;">+0.13%</span>（+14.96点）<br>
              创业板指 <b>2746.29</b> <span style="color:#52c41a;">-0.94%</span>（-26.09点）<br>
              科创50 <b>1329.19</b> <span style="color:#52c41a;">-2.17%</span>（-29.46点）<br>
              沪深300 <b>4174.53</b> <span style="color:#dc2626;">+0.09%</span>（+3.92点）<br>
              科创综指 跌0.86%·万得全A 涨0.01%<br>
              全市场成交 <b>14488亿元</b>·较上一交易日缩量约1203亿元<br>
              全市场超 <b>3100只</b> 个股下跌
            </div>
            <div>
              <b>港股（10-16收盘·10-19休市）与美股（10-19收盘）</b><br>
              恒生指数 <b>24186.83</b> <span style="color:#dc2626;">+0.52%</span>（+124.11点）<br>
              国企指数 <b>8128.25</b> <span style="color:#dc2626;">+0.31%</span>（+24.98点）<br>
              恒生科技 <b>4108.24</b> <span style="color:#dc2626;">+1.16%</span>（+47.25点）<br>
              道琼斯 <b>51966.03</b> <span style="color:#52c41a;">-0.07%</span>（-36.38点）<br>
              纳斯达克 <b>26430.89</b> <span style="color:#dc2626;">+1.11%</span>（+290.85点）<br>
              标普500 <b>7690.73</b> <span style="color:#dc2626;">+0.41%</span>（+31.29点）<br>
              港股主板成交 <b>1782.07亿港元</b>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>10月19日收盘</b>（10月19日为交易日且已收盘）；港股因<b>10月19日为重阳节假期翌日休市一日</b>、南向与北向交易关闭、10月20日恢复交易，故仍取最近一个已收盘场次<b>10月16日收盘</b>；美股取<b>10月19日收盘</b>（美东10月19日收盘对应北京时间10月20日凌晨）。国际原油与COMEX黄金本期未取得可交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-19）：</b>大盘低开高走、震荡上行，沪指涨14.64点、涨幅0.39%收报<b>3730.92</b>点；深证成指涨14.96点、涨幅0.13%收<b>11817.42</b>点；创业板指跌26.09点、跌幅0.94%收<b>2746.29</b>点；科创50跌29.46点、跌幅2.17%收<b>1329.19</b>点；沪深300涨3.92点、涨幅0.09%收<b>4174.53</b>点；科创综指跌0.86%、万得全A涨0.01%。全市场成交约<b>14488亿元</b>（格隆汇口径），较上一交易日缩量约<b>1203亿元</b>，全市场超<b>3100只</b>个股下跌。板块方面银行、石化、家电、军工、煤炭、中药全天强势，午后人形机器人板块连续拉升，光通信、CRO板块回弹，工商银行涨逾1.5%再创历史新高；AI硬件侧继续分化，地产、农业、传媒板块调整。<br>
              <b>港股（10-16）：</b>恒生指数涨124.11点、涨幅0.52%收报<b>24186.83</b>点，全日主板成交<b>1782.07亿港元</b>；国企指数涨24.98点、涨幅0.31%收<b>8128.25</b>点；恒生科技指数涨47.25点、涨幅1.16%收<b>4108.24</b>点。因10月19日重阳节假期翌日休市，本期港股数据维持10月16日收盘不变。<br>
              <b>美股（10-19）：</b>上周科技股大幅抛售后迎来反弹，芯片与人工智能相关股票成为推动大盘回升的主要力量，三大股指收盘涨跌不一。道琼斯工业平均指数跌36.38点、跌幅0.07%收<b>51966.03</b>点；标准普尔500种股票指数涨31.29点、涨幅0.41%收<b>7690.73</b>点；纳斯达克综合指数涨290.85点、涨幅1.11%收<b>26430.89</b>点。标普500十一大板块七跌四涨，公用事业板块和房地产板块分别以1.97%和1.17%的跌幅领跌，非必需消费品板块和科技板块分别以2.73%和1.19%的涨幅领涨（新华社）。费城半导体指数结束连续<b>8个交易日</b>下跌，此前8连跌期间累计下挫约<b>15.7%</b>，为2008年10月以来最长连跌纪录。<br>
              <b>对腾安提示：</b>沪指缩量小幅收红，但创业板指跌0.94%、科创50跌2.17%、全市场超3100只个股下跌，指数与结构仍处背离，货架与持仓页须同步刷新净值日期与估值口径，不得沿用旧净值呈现。10月19日ETF九大类全线净流入约307亿元、宽基占近七成，属指数化托底型资金特征，须把“资金托底”与“科技硬件侧仍在调整”两股力量并列提示，不得把单日资金流入直接解读为趋势反转。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、美股为2026-10-19收盘，港股为2026-10-16收盘（10-19休市）</span>
          <span class="source-tag">数据来源：新华社（美股）、格隆汇（A股成交与板块）、东方财富行情接口（A股指数）</span>
        </div>
'''
st0 = one(s, '<div class="card p3">')
st = s.rindex('\n', 0, st0) + 1
en = s.index('      </div>  </div>', st0)
assert s.count('<div class="card p3">') == 1
seg = s[st:en]
assert seg.count('<div') == 10, seg.count('<div')
assert seg.count('</div>') == 9, seg.count('</div>')
s = s[:st] + S6 + s[en:]
print('OK S6'); dr('S6')

# ==================== Phase 4: S7 时间线 ====================
TL = [
    ('red', '2026-10-20', '首批18只主动ETF获批定档'),
    ('red', '2026-10-20', '央行拟设非银流动性支持工具'),
    ('red', '2026-10-20', '监管通报跨境调研违规5家机构'),
    ('blue', '2026-10-19', '沪指收3730.92点涨0.39%'),
    ('blue', '2026-10-19', 'ETF九大类净流入307亿元'),
    ('blue', '2026-10-19', '纳指涨1.11%芯片股结束八连跌'),
    ('blue', '2026-10-19', '首批基金三季报披露开启'),
    ('blue', '2026-10-19', '债基扎堆限购避险资金涌入'),
    ('blue', '2026-10-16', '首批新能源金属50ETF获批'),
    ('blue', '2026-10-15', '122只发起式基金清盘创新高'),
    ('red', '2026-10-12', '公募运作办法公开征求意见'),
    ('red', '2026-10-09', '浙江证监局警示杭州图灵'),
]
assert len(TL) == 12
for _, _, t in TL:
    assert len(t) <= 25, t
NEW_TL = ''
for c, d, t in TL:
    NEW_TL += ('      <div class="timeline-item">\n'
               '        <div class="timeline-dot %s"></div>\n'
               '        <div class="timeline-date">%s</div>\n'
               '        <div class="timeline-title">%s</div>\n'
               '      </div>\n' % (c, d, t))
i7 = one(s, '<!-- ============ Section 7')
st = s.index('      <div class="timeline-item">', i7)
en = s.index('      </div>    </div>', st) + len('      </div>')
seg = s[st:en]
assert seg.count('<div class="timeline-item"') == 12, seg.count('<div class="timeline-item"')
s = s[:st] + NEW_TL + s[en:]
print('OK S7'); dr('S7')

# ==================== Phase 5: 全量校验 ====================
o1, c1 = s.count('<div'), s.count('</div>')
assert o1 == c1, 'div 不平衡 %d/%d' % (o1, c1)
assert o1 == o0 + 3, 'div 漂移异常 %d -> %d（预期 +3）' % (o0, o1)
assert s.count('</div>>') == 0
assert '\ufffd' not in s
assert 'Section 8' not in s and s.count('Section 8') == 0
assert s.count('class="action-box') == 1
assert s.count('class="card p0"') == 1
assert s.count('class="timeline-item"') == 12
assert s.count('class="stat-card"') == 4
assert s.count('<!-- S0 Card') == 4
for c in ['class="card p1"', 'class="card p2"', 'class="card p3"']:
    print('   ', c, s.count(c))
# S0 action-box 必须落在 S0 段内
i0 = s.index('<!-- ============ Section 0')
i1 = s.index('<!-- ============ Section 1')
assert s.count('class="action-box', i0, i1) == 1
# 深度法：卡起始 depth 集合单值
for name, a, b, expect in [('S0', '<!-- ============ Section 0', '<!-- ============ Section 1', 2),
                           ('S1', '<!-- ============ Section 1', '<!-- ============ Section 2', 2),
                           ('S2', '<!-- ============ Section 2', '<!-- ============ Section 3', 2),
                           ('S4', '<!-- ============ Section 4', '<!-- ============ Section 5', 2),
                           ('S5', '<!-- ============ Section 5', '<!-- ============ Section 6', 2),
                           ('S6', '<!-- ============ Section 6', '<!-- ============ Section 7', 1)]:
    seg = s[s.index(a):s.index(b)]
    depths = set()
    for mm in re.finditer(r'<div class="card p', seg):
        gt = seg.find('>', mm.end())
        head = seg[mm.end():gt]
        depths.add(seg.count('<div', 0, mm.start()) - seg.count('</div>', 0, mm.start()))
    print('   depth[%s] =' % name, sorted(depths))
    assert len(depths) == 1, '%s 卡起始 depth 集合不单值 %s' % (name, depths)
# 黑名单
BAD = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com',
       'toutiao', 'so.html5.qq.com', '163.com/dy', 'cqcb.com', 'weibo.com',
       'k.sina.com.cn', 'dy.163.com', 'q.fund.sohu.com', 'topnews.cn',
       'futunn.com', 'jiantou8.com', 'cofool.com']
for b in BAD:
    assert b not in s, '黑名单命中：%s' % b
print('OK 全量校验通过')

open(P, 'w', encoding='utf-8').write(s)
print('WROTE', P, 'div', o0, '->', o1)
