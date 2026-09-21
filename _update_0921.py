# -*- coding: utf-8 -*-
"""2026-09-21 每日更新：header区间 / S0 / S1 / S5 / S7 / marker / fingerprint"""
import re, sys, io
from datetime import date, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'index.html'
h = open(P, encoding='utf-8').read()
orig = h
TODAY = date(2026, 9, 21)


def drift(tag):
    o = len(re.findall(r'<div\b', h)); c = len(re.findall(r'</div>', h))
    print(f'  [{tag}] open={o} close={c} delta={o-c} len={len(h)}')
    return o, c


def must(cond, msg):
    if not cond:
        raise SystemExit('FAIL: ' + msg)


print('STEP0 baseline')
o0, c0 = drift('base')

# ---------- 1. marker ----------
h = h.replace('<!-- daily-update: 2026-09-20 -->', '<!-- daily-update: 2026-09-21 -->', 1)
must('<!-- daily-update: 2026-09-21 -->' in h, 'marker 未更新')

# ---------- 2. meta ----------
h = re.sub(r'<meta name="viewport" content="[^"]*">',
           '<meta name="viewport" content="被动指数债基破2万亿|摊余债基7只9-21开售|公募规模39.63万亿|秋季策略会再平衡|9-18沪指收3911.87">',
           h, count=1)
h = re.sub(r'<meta name="content-fingerprint" content="[^"]*">',
           '<meta name="content-fingerprint" content="被动指数|摊余成本|公募秋季|多只ETF募">',
           h, count=1)
must('被动指数|摊余成本|公募秋季|多只ETF募' in h, 'fingerprint 未更新')

# ---------- 3. header 数据区间（动态计算） ----------
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
badge_new = f'📅 数据区间：{lower} — {upper}（每日更新）'
h, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge_new, h)
must(n == 1, 'badge 替换数 != 1')
print('  badge ->', badge_new)

# ---------- 4. S0 ----------
h = h.replace('<span class="section-context">9月20日 · 4条今日要闻</span>',
              '<span class="section-context">9月21日 · 4条今日要闻</span>', 1)
must('9月21日 · 4条今日要闻' in h, 'S0 context 未更新')

S0_CARDS = '''      <!-- S0 Card 1 (09-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 被动指数债基规模首破2万亿·384只合计2.06万亿·债券ETF逼近万亿占全部ETF 19.78%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          同花顺财经9月21日报道：Wind数据显示，截至9月18日全市场共有<b>384只</b>被动指数型债券基金，总规模<b>2.06万亿元</b>，首次站上2万亿元关口；其中债券型ETF规模已达<b>9827亿元</b>、逼近万亿大关，占全部ETF规模的<b>19.78%</b>。<br>
          <b>资金驱动而非价格上涨：</b>9月以来至9月18日，债券型ETF净流入达<b>564.98亿元</b>，而8月净流入294.1亿元、7月为净流出15.45亿元——下半年权益震荡加剧，债券ETF的防御配置与流动性管理需求显著提速。<br>
          <b>头部集中：</b>海富通基金10只产品合计<b>1898.19亿元</b>居首，易方达、博时各12只均超1300亿元，富国8只<b>1268.37亿元</b>、南方11只<b>1086.13亿元</b>，全市场仅这5家站上千亿；其后广发955.6亿元、华夏901.48亿元、汇添富871.47亿元、鹏华811.14亿元、国泰686.90亿元。<br>
          <b>产品谱系：</b>53只规模超百亿、20只超200亿；最大为海富通中证短融ETF <b>881.78亿元</b>，其次博时中证可转债及可交换债券ETF <b>629.17亿元</b>、海富通上证城投债ETF <b>554.95亿元</b>，富国中债7-10年政金债ETF、平安中债-中高等级公司债利差因子ETF均超400亿元；品种已覆盖国债、地方债、政金债、信用债、科创债、可转债、短融。<br>
          <b>机构观点：</b>华夏基金认为基本面与货币环境仍支撑债市、存款利率调降推升配置需求，场内投资者甚至把短融ETF当作货基替代；海富通基金认为债券ETF凭借T+0、低费率、可质押、品类丰富放大资金流入效率，但投资者结构仍以机构为主、个人参与度有提升空间。<br>
          <b>对腾安启示：</b>债券ETF正从机构配置工具走向大众理财——货架端应补齐短融/城投债/政金债/可转债ETF的久期与信用风险横向对比，把"场内T+0、低费率、可质押"写成显性卖点；同时必须提示短融ETF"货基替代"背后的利率与净值波动差异，避免客户按存款预期持有。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260921/c680098981.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·09-21</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 2 (09-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 摊余成本债基7只今日开售·两批28只最高2240亿·锁定63个月利好5年高等级信用债</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月21日报道（证券时报 记者余世鹏）：9月14日获批的首批15只摊余成本法债基，截至9月19日已有<b>7只定档发行</b>——<b>国融聚达、贝莱德稳利、兴华安硕、财信聚鑫、红土创新瑞泽、路博迈安瑞6只今日（9月21日）起发行</b>，鹏安安瑞9月22日起发行，单只<b>募集上限统一为80亿元</b>，管理费年费率<b>0.15%</b>、托管费<b>0.05%</b>。<br>
          <b>托管行分布：</b>7只产品托管人均为银行，中信银行托管2只，其余5只分别来自江苏银行、建设银行、兴业银行、长沙银行、浦发银行——银行系托管与渠道资源是本轮发行的隐性推力。<br>
          <b>规模测算：</b>按80亿元上限，首批15只可形成<b>1200亿元</b>基金净资产，参考现有摊余债基约138%—140%的平均杠杆，扣除现金与流动性备付后预计形成约<b>1500亿元</b>有效配置需求；叠加9月11日上报的第二批13只（约1040亿元净资产），<b>两批28只最高募集规模2240亿元</b>。<br>
          <b>债市影响：</b>63个月封闭期对应5年期左右建仓久期，摊余成本法要求持仓通过SPPI测试，新基金有望集中配置5年期左右高等级信用债；申万固收周报认为供需错配下5年左右信用品种估值支撑较强，商金债、券商普通债、TLAC债等金融债亦可适度下沉。<br>
          <b>对腾安启示：</b>今日集中开售的6只+明日1只，是四季度低波固收货架最可预期的增量供给；销售端须把63个月封闭期、摊余估值法与流动性代价前置到购买页首屏，按"底仓替代"而非"灵活理财"定位，并对同批产品的费率差（0.15%与0.3%）做透明排序。
        </div>
        <div class="card-footer">
          <a href="https://www.mrjjxw.com/articles/2026-09-21/4586876.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-21</span></a>
          <a href="https://finance.sina.cn/2026-09-21/detail-inispchm1205951.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-21</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 3 (09-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募秋季策略会密集召开·四季度强调"再平衡"·AI从预期定价转向业绩验证</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          财联社9月21日讯（记者 陈永辉）：随着四季度临近，公募秋季策略会进入密集召开期——<b>建信基金"善建慧投"发布会暨2026秋季投资策略会9月21日举行</b>，汇丰晋信"秋播"策略会9月22日举行，华宝基金与上交所联合主办的"沪市ETF财富管理基地行·重庆站"暨秋季策略报告会已在重庆举办，华泰证券、国泰海通、广发证券等券商策略会相继召开。<br>
          <b>与上半年的关键差异：</b>由集中押注科技成长转向"再平衡"——AI仍是结构性主线，但配置重心正从预期定价转向<b>业绩验证</b>；债市大方向逻辑未变、预计维持震荡；商品中长期看好黄金、相对看好铜，油价仍需消化地缘影响。<br>
          <b>机构观点：</b>汇添富副总经理袁建军——宏观有韧性、流动性宽松、A股估值具性价比，巨量居民储蓄有望向权益迁移；易方达林伟斌——9月或延续震荡中的结构性演绎，风格向盈利质量与产业趋势更匹配的方向扩散；建信蒋严泽——全年非金融A股盈利预期已上调，"<b>杠铃策略有望回归</b>"；富国专场申万宏源傅静涛——年内AI决定性催化尚难确认，2027年有望迎来"科技牛"重建契机；建信江映德——科技投资已进入订单与业绩验证阶段，要"重跟踪、轻推演"，看好国产算力。<br>
          <b>共识配置：</b>"科技成长+红利防御"的杠铃型结构成为多数公募共识，科技内部的分歧集中在"继续买算力"还是"等应用与业绩再定价"。<br>
          <b>对腾安启示：</b>四季度主线共识是杠铃结构，但科技内部已出现实证派与动量派的分歧——配置页应提供杠铃比例工具与科技细分（算力/应用/硬件）的风险分层，陪伴话术从"押赛道"切换到"业绩验证进度"，避免用上半年科技单边的收益预期引导四季度申购。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260921A02KNV00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·09-21</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 4 (09-21 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多只ETF募集成功·9月31只ETF成立合计超100亿·算力主题领跑但七成不足3亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          中证网9月21日报道：Wind数据显示，上周有多只ETF成功募集，涵盖创业板算力、人工智能、恒生科技、红利低波等主题；截至9月20日，<b>9月共31只ETF成立，合计募集规模超100亿元</b>，平均单只<b>3.38亿元</b>、中位数<b>2.38亿元</b>，其中<b>22只规模不足3亿元、占比70.97%</b>。<br>
          <b>算力领跑：</b>募集规模最大的是创业板算力ETF易方达<b>14.77亿元</b>，其次创业板算力ETF广发<b>13.42亿元</b>；9月16日单日有8只ETF发布募集成功公告，其中4只为创业板算力主题——南方3.39亿元、大成4.61亿元、嘉实2.99亿元、鹏华4.32亿元。<br>
          <b>上周上市：</b>15只ETF上市交易，9月14日化工ETF景顺、家电ETF华安、汽车零部件ETF广发、红利质量ETF鹏华、沪深300现金流ETF易方达正式上市。<br>
          <b>在发与待发：</b>卫星ETF华夏、创业板软件ETF南方、大数据ETF前海开源、广发中证有色金属矿业主题ETF联接等在发；9月21日—25日还有5只启动认购，包括工银中证A500增强策略ETF联接、通信ETF易方达、永赢/易方达中证科创创业人工智能ETF联接、华夏国证粮食产业ETF联接。<br>
          <b>对腾安启示：</b>新发ETF呈现"数量多、个头小、主题高度集中"的特征——首页不宜按"新发"堆砌陈列，应按主题景气度与规模/流动性双维度筛选；对不足3亿元的品种须标注流动性与潜在清盘风险，算力主题同质化严重时更要突出费率与跟踪误差差异。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/01/2026/09/21/detail_2026092110040572.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-21</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>'''

a = h.find('      <!-- S0 Card 1 (09-19 P1) -->')
must(a > 0, 'S0 card1 锚点未找到')
b = h.find('\n    </div>\n  </div>\n<!-- ============ Section 1', a)
must(b > a, 'S0 结束锚点未找到')
h = h[:a] + S0_CARDS + h[b:]
print('STEP4 S0 替换完成')
drift('S0')

# ---------- 5. S1：换掉 09-11 债券ETF卡，补 09-19 公募规模 ----------
S1_NEW = '''      <!-- S1 Card: 8月末公募规模39.63万亿 (09-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-19</span>
          </div>
          <div class="card-title">🟡 8月末公募规模回升至39.63万亿·单月增5293亿·混合基金+6.70%成反弹主力</div>
        </div>
        <div class="card-body">
          上海证券报（记者白丽斐）9月19日报道：中基协最新数据显示，截至2026年8月底，我国境内公募基金管理机构共<b>165家</b>（基金管理公司150家、取得公募资格的资产管理机构15家），管理的公募基金资产净值合计<b>39.63万亿元</b>，较7月底增长<b>5293.09亿元</b>、环比<b>+1.35%</b>，结束7月短暂下滑后迅速企稳，再度逼近40万亿元历史高位。<br>
          <b>结构拆解：</b>混合型基金8月末<b>4.08万亿元</b>、单月大增<b>2567.93亿元</b>（+6.70%），贡献接近一半增量，是7月缩水后的强力修复；股票基金<b>5.03万亿元</b>、增496.61亿元（+1.00%）；货币基金<b>16.30万亿元</b>、增1476.80亿元（+0.91%）；债券基金<b>11.96万亿元</b>、仅微增156.81亿元；QDII <b>1.03万亿元</b>、增138.36亿元（+1.36%）；<b>FOF降至3271.83亿元</b>、环比下降33.97亿元，是8月唯一规模与份额"双降"的品类。<br>
          <b>净值涨、份额降：</b>8月上证指数涨超4%、深证成指涨超3%、科创综指涨超8%，规模回升主要来自净值修复；但混合基金份额环比微降0.21%至2.48万亿份、股票基金份额单月减少789.15亿份，说明部分基民在反弹中选择落袋为安——华宝中证医疗ETF减少约73亿份、易方达沪深300医药ETF缩水超50亿份，另有30余只ETF单月份额减少超10亿份。<br>
          <b>对腾安启示：</b>本轮规模修复由净值驱动而非净申购——代销端须把"保有量增长"拆分为市值变动与真实净流入，避免用指数涨幅掩盖客户净赎回；反弹中的ETF份额流出提示应在高点加强持有期陪伴与再配置引导，而非顺势推高波动品种。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.cnstock.com/commonDetail/792701?commTag=true" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-19</span></a>
          <a href="https://www.cnr.cn/jingji/gundong/20260921/t20260921_527820018.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">央广网·09-21</span></a>
        </div>
      </div>

'''
a = h.find('      <!-- S1 Card: 债券ETF规模首破9500亿 (09-11 P1) -->')
must(a > 0, 'S1 待替换卡锚点未找到')
b = h.find('      <!-- S1 Card: 含权债基规模3.35万亿 (09-17 P1) -->', a)
must(b > a, 'S1 下一卡锚点未找到')
h = h[:a] + S1_NEW + h[b:]
print('STEP5 S1 替换完成')
drift('S1')

# ---------- 6. S5：补 1 张（周一巡检补卡） ----------
S5_NEW = '''<div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 兴证全球以"可信AI"构建资管流水线·取数有界生成有据输出可溯·责任在岗</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-15</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月15日报道：兴证全球基金本轮AI建设的核心并非模型能力堆叠，而是一套贯穿全流程的统一约束机制——<b>取数有界、生成有据、输出可溯、责任在岗</b>，AI不绕过、不修改、不替代既有业务规则体系。<br>
          <b>场景落地：</b>①自研<b>兴全AIWork</b>办公平台依托本地部署的Hermes为每位员工构建个人AI助理，邮箱/日程/文档按需逐项授权、助理空间相互隔离、全程留痕；②<b>营销物料智作平台</b>以可信结构化数据限定取数范围，实现"一份可信数据、多种物料形态"（文案、季报解读、PPT、长图、海报）；③风控AI助手<b>"风小应"</b>自动解析基金合同合规要素并映射为风控条目与参数方案，输出止步于"条目建议+参数方案"、须风控人员人工确认；④<b>头寸AI助理</b>实时预警缺口并推荐处置方案；⑤直销App上线AI诊基与AI持仓分析，形成"<b>AI生成→AI审校→人工终审</b>"三层机制；⑥数据侧"数小智"提供7×24小时数据故障诊断与血缘解析。<br>
          <b>演进脉络：</b>早在2023年公司即推出AI资金交易机器人"兴宝"，为业内首家将AI技术应用于资金交易领域的基金公司，此后由投研、交易逐步延伸至办公、营销、风控、电商与数据。<br>
          <b>对腾安启示：</b>行业AI竞争的胜负手正从"模型有多强"转向"责任边界有多清晰"——腾安若上线AI诊基/陪伴，须先定义取数边界、AI数字事实审核与人工终审链路，把留痕可审计做成对客合规卖点，而非只比拼生成速度。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/790576" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-15</span></a>
          <span class="impact-tag high">AI治理：高</span>
        </div>
      </div>

'''
anchor = '\n    </div>\n  </div>\n<!-- ============ Section 6'
must(h.count(anchor) == 1, 'S5 插入锚点不唯一')
h = h.replace(anchor, '\n' + S5_NEW + '    </div>\n  </div>\n<!-- ============ Section 6', 1)
print('STEP6 S5 补卡完成')
drift('S5')

# ---------- 7. S7 时间线 ----------
TL = [
    ('blue',  '2026-09-21', '被动指数债基破2万亿'),
    ('blue',  '2026-09-21', '7只摊余债基今日开售'),
    ('blue',  '2026-09-21', '公募秋季策略会密集召开'),
    ('blue',  '2026-09-21', '9月31只ETF成立募超100亿'),
    ('blue',  '2026-09-19', '8月末公募规模39.63万亿'),
    ('blue',  '2026-09-19', '刘彦春卸任景顺长城副总'),
    ('blue',  '2026-09-19', '汇添富航天航空ETF提前结募'),
    ('red',   '2026-09-18', '证监会公示吹哨人奖励名单'),
    ('blue',  '2026-09-18', '韩创5只产品集中增聘'),
    ('blue',  '2026-09-18', 'A股放量反弹沪指站上3900'),
    ('blue',  '2026-09-17', '年内新发基金规模破8000亿'),
    ('blue',  '2026-09-17', '公募密集调整QDII申购限额'),
]
items = ''
for c, d, t in TL:
    items += (f'      <div class="timeline-item">\n'
              f'        <div class="timeline-dot {c}"></div>\n'
              f'        <div class="timeline-date">{d}</div>\n'
              f'        <div class="timeline-title">{t}</div>\n'
              f'      </div>\n')

s7 = h.find('<!-- ============ Section 7')
must(s7 > 0, 'S7 marker 未找到')
ts = h.find('      <div class="timeline-item">', s7)
must(ts > 0, 'S7 首个 item 未找到')
te = h.find('\n    </div>\n\n  </div>', ts)
must(te > ts, 'S7 结束锚点未找到')
h = h[:ts] + items + h[te + 1:]
print('STEP7 S7 重写完成（%d 条）' % len(TL))
drift('S7')

# ---------- 8. 校验 ----------
must(h.count('<div class="timeline-item">') == 12, 'S7 item 数 != 12')
must('Section 8' not in h and 'S8' not in h, 'S8 残留')
must('📅' in h and '�' not in h, 'U+FFFD 残留')
s0 = h[h.find('Section 0'):h.find('Section 1')]
must('<span class="section-title">今日焦点</span>' in s0, 'S0 title 被改')
tags = re.findall(r'date-tag">(\d{2})-(\d{2})</span>', s0)
must(tags.count(('09', '21')) == 4, f'S0 09-21 卡数 {tags.count(("09","21"))} != 4')
for sec in ['Section 1', 'Section 2', 'Section 5', 'Section 6', 'Section 7']:
    must(f'============ {sec}' in h, f'{sec} marker 缺失')

open(P, 'w', encoding='utf-8').write(h)
o1, c1 = drift('final')
print(f'\nDIV open {o0}->{o1}, close {c0}->{c1}; 净变化 open {o1-o0} / close {c1-c0}; '
      f'平衡 {o1 == c1}; 长度 {len(orig)}->{len(h)}')
print('OK 写入完成')
