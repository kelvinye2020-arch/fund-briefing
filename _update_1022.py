# -*- coding: utf-8 -*-
"""2026-10-22 daily update：marker / meta / badge / Stats Bar / S0 / S6 / S7"""
import io, re, sys
from datetime import date, timedelta

P = "c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"
src = io.open(P, encoding="utf-8").read()
TODAY = date.today()

RED = "\U0001F534"
YEL = "\U0001F7E1"
BLU = "\U0001F535"

o0 = len(re.findall(r"<div\b", src))
c0 = src.count("</div>")

# ---------- 锚点预检 ----------
A_MARK = "<!-- daily-update: 2026-10-21 -->"
A_S0S = "      <!-- S0 Card 1 (10-20 P0) -->"
A_S0E = "    </div>\n  </div>\n\n<!-- ============ Section 1"
A_S6S = "<!-- ============ Section 6: 市场行情速览 ============ -->"
A_S6T = "      </div>  </div>"
A_S7S = "<!-- ============ Section 7: 关键时间线 ============ -->"
A_SBAR = '    <div class="stats-bar">'
for a in (A_MARK, A_S0S, A_S0E, A_S6S, A_S6T, A_S7S, A_SBAR):
    assert src.count(a) == 1, "ANCHOR_COUNT!=1: %r -> %d" % (a, src.count(a))

# ================= 1. marker / meta / badge =================
src = src.replace(A_MARK, "<!-- daily-update: %s -->" % TODAY.isoformat())

DESC = ("首批18只主动ETF定档10月23日开售|公募投研迎基准锚定大考|郑巍山卸任全部在管基金产品|"
        "公募多策并举提升投资者持有体验|沪指10-21收3713.03 纳指涨1.05%")
FP = "首批18|公募投研|郑巍山卸|公募多策"
assert src.count('<meta name="description" content=') == 1
src = re.sub(r'<meta name="description" content="[^"]*">',
             '<meta name="description" content="%s">' % DESC, src, count=1)
assert src.count('<meta name="content-fingerprint" content=') == 1
src = re.sub(r'<meta name="content-fingerprint" content="[^"]*">',
             '<meta name="content-fingerprint" content="%s">' % FP, src, count=1)

lo = (TODAY - timedelta(days=14)).strftime("%Y.%m.%d")
hi = TODAY.strftime("%Y.%m.%d")
BADGE_RE = r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）"
assert re.search(BADGE_RE, src)
src = re.sub(BADGE_RE, "📅 数据区间：%s — %s（每日更新）" % (lo, hi), src, count=1)

# ================= 2. Stats Bar =================
sb_i = src.find(A_SBAR)
sb_e = src.find("\n  </div>", sb_i) + len("\n  </div>")
assert sb_e > sb_i
assert src[sb_i:sb_e].count('class="stat-card"') == 4
assert src[sb_i:sb_e].count('<div class="stat-change') == 4
STATS = '''    <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">18只</div>
      <div class="stat-label">首批主动ETF 10月23日集中开售·单只募集上限20亿元·合计约360亿元</div>
      <div class="stat-change up">▲ 年管理费均为1%·托管费率0.1%—0.15%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3713.03</div>
      <div class="stat-label">沪指10-21收盘·跌0.60%·沪深北三市成交14421亿元</div>
      <div class="stat-change down">▼ 创业板指跌1.62%·恒生指数跌0.90%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">364位</div>
      <div class="stat-label">年内离任基金经理·同期新上任基金经理达606名</div>
      <div class="stat-change neutral">● 郑巍山卸任银河基金全部在管产品</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">60亿元</div>
      <div class="stat-label">10月以来基金分红总额·超200只基金宣布分红</div>
      <div class="stat-change up">▲ 仅10月21日就有25只基金发布分红公告</div>
    </div>
  </div>'''
src = src[:sb_i] + STATS + src[sb_e:]

# ================= 3. S0 卡片 =================
s0_i = src.find(A_S0S)
s0_e = src.find(A_S0E)
assert 0 < s0_i < s0_e

C1 = '''      <!-- S0 Card 1 (10-22 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">''' + RED + ''' 首批18只主动ETF明日开售·10月23日集中发行·单只上限20亿元·年管理费1%</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-22</span>
          </div>
        </div>
        <div class="card-body">
          证券时报10月22日报道（记者李明珠）：根据披露的发售公告，10月19日获批的18只主动ETF发行日期正式敲定为<b>10月23日</b>，单只产品募集上限均为<b>20亿元</b>，按上限静态测算，18只产品有望最多带来<b>360亿元</b>增量资金。<br>
          <b>发行节奏：</b>易方达、华夏、华泰柏瑞、招商、南方、华安<b>6家</b>公司旗下产品发行期定为10月23日至10月29日，募集周期仅<b>5个工作日</b>；富国、汇添富产品募集期稍长，至10月30日收官，合计<b>6个工作日</b>；工银瑞信、建信、华宝等<b>10家</b>公募则将募集截止日期安排在11月初。<br>
          <b>费率与托管：</b>依托场内ETF的产品形态，主动ETF费率水平普遍优于场外主动权益基金。从已披露文件看，18只产品年管理费均为<b>1%</b>，托管费率落在<b>0.1%至0.15%</b>之间。托管人共涉及<b>12家机构</b>（7家银行、5家券商），招商银行、工商银行、建设银行、浦发银行、农业银行、中国银行、兴业银行累计揽下<b>11只</b>主动ETF的托管；券商方面广发证券托管<b>2只</b>，国信证券、国泰海通、中信证券、申万宏源各托管1只。<br>
          <b>策略与管理方式：</b>18只产品覆盖18家基金管理人，在沪深交易所上市的产品各<b>9只</b>；按主要投资风格划分为均衡策略<b>9只</b>、价值策略<b>4只</b>、红利策略<b>3只</b>、质量策略与大盘成长策略各<b>1只</b>。管理方式上<b>13只</b>采用基本面主动选股策略、<b>5只</b>采用量化策略；<b>15只</b>采用“主动＋被动”双基金经理模式，仅华夏基金、富国基金、摩根资产管理旗下3只选择单基金经理负责制。<br>
          <b>投资者适配：</b>鹏华基金建议投资者首先厘清自身投资风格、匹配对应产品策略——风险承受能力偏低、追求长期稳健增值的投资者可优先关注均衡价值、红利策略类主动ETF，这类策略换手率适中、持仓分散，更适配每日透明披露的运作模式；习惯于短线频繁交易、追逐短期题材行情的投资者则需谨慎参与，主动ETF受持仓透明规则约束，很难实现快速轮动博弈。<br>
          <b>对腾安启示：</b>18只主动ETF明日起集中开售且募集期最短仅5个工作日，货架须在10月23日开售前完成品类建档与风险揭示，把“募集上限20亿元”“合计约360亿元”标注为按上限静态测算的上限值而非实际募集规模；费率须按“管理费1%＋托管费0.1%—0.15%”分列展示，不得合并宣传为“总成本1%”；对红利、价值、均衡等不同策略产品须分栏陈列并标注业绩比较基准差异，不得以“主动ETF”单一标签替代策略区分，也不得把双基金经理配置包装为收益保障。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-10-22/doc-inivziwc6096668.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·证券时报·10-22</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 上架准备→10月23日开售前完成18只主动ETF建档，字段须包含“策略风格（均衡／价值／红利／质量／大盘成长）”“管理方式（基本面／量化）”“基金经理模式（双／单）”“募集期与首募上限”“管理费与托管费”，并与被动宽基ETF分栏陈列；<br>
            ② 销售话术→“合计约360亿元”“管理费1%”一律标注为按20亿元上限的静态测算值与已披露费率，禁止写成预计募集规模或总成本；<br>
            ③ 适当性→持仓每日透明不等于低风险，须在详情页前置“主动ETF受持仓透明规则约束、不适配短线轮动博弈”的提示，并同步提示比例确认与配售规则。
          </div>
        </div>
      </div>

'''

C2 = '''      <!-- S0 Card 2 (10-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + YEL + ''' 公募投研迎“基准锚定”大考·业绩比较基准硬约束·80%总资产界定投资方向</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-22</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报10月22日报道（记者魏昭宇）：监管部门就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，多项围绕产品风险收益特征透明化的约束条款引发行业关注。<br>
          <b>两条关键约束：</b>一是基金管理人应当为基金设置业绩比较基准，建立全流程管理机制，确保基准有效表征投资风格、衡量业绩并<b>约束投资行为</b>；二是基金名称显示投资方向的，须以可识别或可量化方式清晰界定，且<b>80%以上基金总资产</b>属于该方向，并建立投资对象风格库；非行业主题基金不得集中投资单一行业或主题。<br>
          <b>口径收紧：</b>中金公司表示，计量端将80%比例的计算口径由“非现金基金资产”调整为“<b>基金总资产</b>”，避免产品通过保留高现金仓位稀释实际持有占比；命名端强调“符合市场基本常识和普遍认知、与投资方向直接相关”。<br>
          <b>混合基金细分：</b>偏股混合基金权益比例下限为<b>60%以上</b>，偏债混合基金上限为<b>30%以下</b>，其他混合基金上下限区间幅度原则上不超过<b>40个百分点</b>；权益比例可高于<b>80%</b>的产品按股票基金管理风险等级；权益与可转债、可交换债比例上限合计高于<b>30%</b>的混合基金，不得使用“固收增强”“稳健收益”等表述。<br>
          <b>新增禁止情形：</b>本次修订新增“他人下达投资指令或违规提供投资建议、为规避监管提供便利、非公平交易与利益输送、违规返还管理费、进行不必要交易”等禁止情形，并提高处罚幅度、增加对责任人员的处罚依据。<br>
          <b>负债端与持有人大会：</b>除特殊情形外，开放式基金不得接受导致单一投资者持有份额超过<b>50%</b>的申购，超过<b>20%</b>的须确认持有期不低于<b>3个月</b>且单日净赎回不超过总份额<b>10%</b>；投资比例微调、增加风险收益特征无重大差异的工具等常规优化，可由管理人与托管人协商一致、在开放期内提前<b>30日</b>公告后办理，仅在投资目标、范围、策略、运作方式发生重大变更时才需召开持有人大会。<br>
          <b>对腾安启示：</b>“业绩比较基准硬约束＋80%总资产投向界定”落地后，产品命名与风险收益特征的对应关系将显著收紧，货架须同步更新“基金名称—投资方向—业绩比较基准”三字段并列展示，禁止沿用仅按历史业绩或赛道热度的归类口径；混合基金须按偏股／偏债／其他三类重新标注风险等级，“固收增强”“稳健收益”等表述不得用于权益与可转债比例上限合计高于30%的产品；单一投资者持有比例与持有期限制属负债端安排，详情页不得将其解读为对收益的保证。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/01/2026/10/22/detail_2026102210046357.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·10-22</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

'''

C3 = '''      <!-- S0 Card 3 (10-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + BLU + ''' 郑巍山卸任银河基金全部在管产品·3只合计210.35亿元·年内364位基金经理离任</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-22</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月22日报道（记者曹雯璟）：10月22日，银河创新成长、银河和美生活、银河智联主题分别发布基金经理变更公告，郑巍山离任基金经理一职。至此，郑巍山卸任<b>全部在管产品</b>的基金经理职务，银河基金对其任职期间的贡献表示诚挚感谢。<br>
          <b>业绩与规模：</b>郑巍山是业内知名科技领域基金经理，深耕半导体产业链，其管理的3只基金产品合计规模达<b>210.35亿元</b>。Wind数据显示，截至10月21日，他管理的银河创新成长任职回报率高达<b>284.87%</b>，年化回报率达<b>19.82%</b>，同类排名<b>18/702</b>。<br>
          <b>履历：</b>郑巍山为硕士研究生学历，拥有<b>18年</b>证券行业从业经历、<b>7年</b>公募基金管理经历，曾先后就职于国元证券研究中心、景顺长城基金、兴业基金；2018年10月加入银河基金，此前担任过股票投资部总监。银河基金表示，本次变更前已完成投研工作交接，新任基金经理均为公司内部成熟投研人员，各基金投资目标、投资策略保持不变。<br>
          <b>行业流动：</b>Wind数据显示，截至10月21日，今年以来新上任基金经理达<b>606名</b>，离任的基金经理达<b>364位</b>，其中包括招商基金李崟、信达澳亚基金李晓西、广发基金傅友兴、兴证全球基金董理、华安基金蒋璆、华富基金陈启明，以及天弘基金原“固收+”名将姜晓丽、中银基金原核心基金经理郑宁等。<br>
          <b>公司层面：</b>银河基金成立于2002年，截至9月30日在管规模达<b>1212.80亿元</b>，较去年同期增长超<b>12%</b>；中国银河证券基金研究中心数据显示，截至9月30日其主动股票投资管理能力过去二十年排名<b>1/36</b>、过去十年<b>3/70</b>、过去三年<b>4/123</b>。<br>
          <b>对腾安启示：</b>基金经理变更属影响持有决策的重大信息，货架须在公告当日同步更新在管产品的基金经理字段与变更生效日，禁止继续展示离任经理的任职回报、年化回报与同类排名作为卖点；对“18年从业”“任职回报284.87%”一类历史业绩须标注统计截止日与产品范围，不得跨产品迁移使用；年内606名新任、364位离任的行业流动数据可用于说明“平台化投研”趋势，但不得据此暗示单一产品业绩的稳定性。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR01d7b90e-eee5-03f3-2d70-3a2473458eca" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-22</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

'''

C4 = '''      <!-- S0 Card 4 (10-22 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">''' + BLU + ''' 公募多策并举提升持有体验·10月以来分红超60亿元·港股基金申赎提速至T+1</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-22</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月22日报道（记者赵明超）：近期基金密集宣布分红，多只产品下调费率，港股主题基金申赎交易提速，公募行业多策并举持续提升投资者持有体验。<br>
          <b>分红：</b>10月21日有<b>25只</b>基金发布分红公告；10月以来已有超过<b>200只</b>基金宣布分红，分红总额超<b>60亿元</b>。多只权益类基金大手笔分红：红利ETF易方达分红<b>8亿元</b>，上证180ETF华安、易方达价值精选混合基金等10月分红均超过<b>1亿元</b>。业内人士表示，在震荡行情中基金分红让部分收益落袋为安，有助于提升持有体验。<br>
          <b>降费：</b>诺安基金10月20日公告，自<b>10月23日</b>起，诺安货币市场基金管理费年费率由<b>0.33%降至0.15%</b>、托管费年费率由<b>0.10%降至0.04%</b>，A类、C类、D类基金份额销售服务费年费率由<b>0.25%降至0.15%</b>。浦银基金10月21日公告，自10月22日起旗下浦银半导体产业混合基金新增招商银行为代销机构并开通定投业务，参加其费率优惠活动。<br>
          <b>提速：</b>中欧基金公告，自10月20日起调整中欧港股消费混合基金、中欧港股医药混合基金的估值时间和申赎确认时间，估值时间由<b>T+1日调整为T日</b>，申购赎回确认时间由<b>T+2日调整为T+1日</b>；长城港股医疗保健精选混合基金、长城港股价值优选股票基金自同日起作相同调整。<br>
          <b>政策背景：</b>监管部门机构监管通报《优化新模式浮动费率产品注册安排 纵深推进公募基金改革》明确，按照分类监管、稳步推进的原则，将新模式浮动费率产品参与机构范围拓展至主动权益类基金管理规模居前的中型基金管理人；对符合持有期要求的投资者，业绩符合同期基准适用基准档费率、明显低于基准适用低档、显著超越基准适用升档。<br>
          <b>对腾安启示：</b>分红、降费、申赎提速均属影响客户实际到账与体验的要素，货架须同步更新分红公告日期与每份派发金额、最新适用费率与生效日、港股基金的估值与确认时点，禁止沿用降费前的费率口径；展示“分红总额超60亿元”时须标明统计区间与只数口径，不得把分红等同于额外收益；浮动费率产品的三档费率须标注适用条件与持有期要求，不能简化为“多赚多收”的承诺。
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-10/22/content_2279866.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报电子版·10-22</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''
src = src[:s0_i] + C1 + C2 + C3 + C4 + src[s0_e:]

# S0 context
assert src.count('<span class="section-context">10月21日 · 4条今日要闻</span>') == 1
src = src.replace('<span class="section-context">10月21日 · 4条今日要闻</span>',
                  '<span class="section-context">10月22日 · 4条今日要闻</span>')

# ================= 4. S6 =================
s6i = src.find(A_S6S)
cs = src.find('<div class="card p3">', s6i)
ce = src.find(A_S6T, cs) + len("      </div>")
assert 0 < s6i < cs < ce

S6 = '''        <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股、港股、美股统一10-21收盘·沪指3713.03 -0.60%｜纳指涨1.05%领涨</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-21</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-21收盘）</b><br>
              上证指数 <b>3713.03</b> <span style="color:#52c41a;">-0.60%</span>（-22.34点）<br>
              深证成指 <b>11704.35</b> <span style="color:#52c41a;">-0.82%</span>（-96.94点）<br>
              创业板指 <b>2694.71</b> <span style="color:#52c41a;">-1.62%</span>（-44.49点）<br>
              科创综指 <b>1602.62</b> <span style="color:#52c41a;">-0.08%</span><br>
              沪深北三市成交 <b>14421亿元</b><br>
              其中沪深两市约 <b>14294亿元</b>（沪市约6428亿元＋深市约7866亿元）
            </div>
            <div>
              <b>港股（10-21收盘）与美股（美东10-21收盘）</b><br>
              恒生指数 <b>23651.87</b> <span style="color:#52c41a;">-0.90%</span>（-215.87点）<br>
              国企指数 <b>7943.41</b> <span style="color:#52c41a;">-1.08%</span>（-86.85点）<br>
              恒生科技 <b>3994.77</b> <span style="color:#52c41a;">-1.26%</span>（-51.14点）<br>
              道琼斯 <b>52856.09</b> <span style="color:#dc2626;">+0.69%</span>（+360.21点）<br>
              纳斯达克 <b>26702.86</b> <span style="color:#dc2626;">+1.05%</span>（+278.04点）<br>
              标普500 <b>7757.17</b> <span style="color:#dc2626;">+0.58%</span>（+44.60点）<br>
              港股主板成交 <b>1765.97亿港元</b>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>10月21日收盘</b>（10月21日为交易日且已收盘）；上证指数、深证成指、创业板指、科创综指收盘点位与沪深北三市全天成交<b>14421亿元</b>取自上海证券报·中国证券网（记者李雨琪、张玮华，10月22日07:51发布）；沪市约<b>6428亿元</b>、深市约<b>7866亿元</b>为同花顺iFinD分市场成交额口径，合计约14294亿元，与沪深北三市口径统计范围不同，本期仅并列列出、不与上述数字混用。港股取<b>10月21日收盘</b>（新华社香港10月21日电）。美股取<b>美东10月21日收盘</b>（新华社纽约10月21日电，对应北京时间10月22日凌晨）。国际原油与贵金属本期未取得可在同一源内交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-21）：</b>上海证券报10月22日报道，A股市场整体冲高回落，题材端依旧保持快速轮动特征，科技板块出现局部回暖迹象，但权重股表现仍相对较弱。端侧AI概念延续活跃，AI眼镜、AI手机方向涨幅居前，移远通信、日海智能收获2连板，利亚德、敏芯股份以<b>20%</b>幅度涨停；消息面上，DeepSeek于10月20日宣布全面开源内部推理框架DeepInfer，兼容英伟达与华为昇腾平台。光通信产业链延续回暖，CPO、光纤、光芯片等方向表现活跃，CPO概念中天洋新材走出3天2板，致尚科技涨幅超过<b>10%</b>，通宇通讯涨停，剑桥科技、天孚通信涨幅居前。机构观点方面，中金公司研报认为当前位置积极信号正在增多，此前调整已较充分反映近期多重超预期输入性风险挑战的不利影响，对A股市场中期走势不必悲观；华鑫证券研报称，经过连续调整后A股微观筹码出清的负反馈已渐入尾声。<br>
              <b>港股（10-21）：</b>新华社香港10月21日电，香港恒生指数跌215.87点、跌幅<b>0.9%</b>收报<b>23651.87</b>点，全日主板成交<b>1765.97亿港元</b>；国企指数跌86.85点、跌幅1.08%收<b>7943.41</b>点；恒生科技指数跌51.14点、跌幅1.26%收<b>3994.77</b>点。蓝筹股方面腾讯控股跌<b>4.04%</b>收报393.8港元、中国移动跌3.66%收报77.55港元、汇丰控股涨0.76%收报145.8港元、香港交易所涨0.11%收报372.8港元。<br>
              <b>美股（美东10-21）：</b>新华社纽约10月21日电，纽约股市三大股指21日上涨。道琼斯工业平均指数比前一交易日上涨360.21点、涨幅0.69%收于<b>52856.09</b>点；标准普尔500种股票指数上涨44.60点、涨幅0.58%收于<b>7757.17</b>点；纳斯达克综合指数上涨278.04点、涨幅1.05%收于<b>26702.86</b>点。板块方面，标普500十一大板块七涨四跌，科技板块和工业板块分别以<b>1.61%</b>和<b>0.91%</b>涨幅领涨，通信服务板块和房地产板块分别以1.33%和0.79%跌幅领跌。<br>
              <b>对腾安提示：</b>本日A股与港股同步回落、美股三大指数集体上行，境内外方向再度背离，货架与持仓页须按各自市场分别刷新净值日期与估值口径，不得用单一指数涨跌概括全市场；A股呈现“指数回落、题材轮动”的结构，科技板块仅局部回暖而权重股偏弱，展示产品业绩时须区分指数与主题两条主线；港股基金申赎确认时点已于近日调整为T+1，涉及港股主题产品的到账与确认提示须同步更新。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-21收盘，美股为美东2026-10-21收盘</span>
          <span class="source-tag">数据来源：上海证券报·中国证券网、同花顺iFinD（A股）；新华社（港股、美股）</span>
        </div>
      </div>'''
src = src[:cs] + S6 + src[ce:]

# ================= 5. S7 =================
s7i = src.find(A_S7S)
f7 = src.find('<div class="timeline-item">', s7i)
l7 = src.rfind('<div class="timeline-item">', s7i, src.find("</body>"))
e7 = src.find("      </div>\n    </div>", l7) + len("      </div>")
assert 0 < s7i < f7 <= l7 < e7
assert src[f7:e7].count('<div class="timeline-item">') == 12

ITEMS = [
    ("red", "2026-10-22", "首批18只主动ETF明日开售"),
    ("red", "2026-10-22", "公募投研迎基准锚定大考"),
    ("blue", "2026-10-22", "郑巍山卸任全部在管产品"),
    ("blue", "2026-10-22", "10月以来基金分红超60亿元"),
    ("blue", "2026-10-21", "沪指收3713.03点跌0.60%"),
    ("blue", "2026-10-21", "创业板指跌1.62%失守2700点"),
    ("blue", "2026-10-21", "恒指跌0.90%腾讯跌4.04%"),
    ("blue", "2026-10-21", "美股三大指数齐涨纳指领涨"),
    ("red", "2026-10-20", "央行拟设非银流动性支持工具"),
    ("blue", "2026-10-20", "ETF资金净流入206.50亿元"),
    ("red", "2026-10-19", "首批18只主动ETF获批"),
    ("blue", "2026-10-15", "122只发起式基金清盘创新高"),
]
blk = ""
for dot, d, t in ITEMS:
    assert len(t) <= 25, "TOO_LONG: " + t
    blk += ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>\n' % (dot, d, t))
blk = blk.rstrip("\n")
src = src[:f7] + blk + src[e7:]

# ================= 6. 写入与自检 =================
io.open(P, "w", encoding="utf-8").write(src)

o1 = len(re.findall(r"<div\b", src))
c1 = src.count("</div>")
log = io.open("c:/Users/kelvinyye/WorkBuddy/20260314103829/_update_1022.txt", "w", encoding="utf-8")
def w(*a):
    log.write(" ".join(str(x) for x in a) + "\n")
w("div open %d -> %d ; close %d -> %d ; drift %d/%d" % (o0, o1, c0, c1, o1 - o0, c1 - c0))
w("U+FFFD:", src.count("\ufffd"))
w("S8 exists:", "Section 8" in src)
w("marker:", re.search(r"<!-- daily-update: (\d{4}-\d{2}-\d{2}) -->", src).group(1))
w("badge:", re.search(r"数据区间：([\d\.]+) — ([\d\.]+)", src).groups())
w("context:", re.search(r'<span class="section-context">([^<]+)</span>', src).group(1))
w("S0 title:", re.search(r'<span class="section-title">([^<]+)</span>', src).group(1))
w("action-box:", src[src.find("Section 0"):src.find("Section 1")].count('action-box'))
s0seg = src[src.find("Section 0"):src.find("Section 1")]
w("S0 cards:", s0seg.count('<div class="card p'), "links:", len(re.findall(r'href="http', s0seg)))
w("S7 items:", src.count('<div class="timeline-item">'), "desc:", src.count("timeline-desc"))
w("bad '</div>>':", src.count("</div>>"))
log.close()
print("WROTE_OK div %d/%d" % (o1, c1))
