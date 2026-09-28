#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-28（周一·中秋假期后首个交易日）

要点：
- 09-25 中秋、09-25—27 A股休市，09-28 恢复交易但早盘未收盘
  → Stats Bar / S6 的 A股基准维持 09-24（假期前最后交易日）收盘，港美股更新为 09-25 收盘
  → S6 另附 09-28 盘中快照（明确标注非收盘价）
- S0 四卡全换 09-28 T+0
- S1 删 09-13 代销百强榜（超 T-14），补 09-28 险资港股通ETF
- S4 删 09-12 券商56席 + 09-13 三方首超银行（双双超 T-14），补 2 张 09-28 卡
- S7 时间线重写 12 条
"""
import re, sys, collections
from datetime import date, timedelta

P = 'index.html'
h = open(P, encoding='utf-8').read()
orig_open = len(re.findall(r'<div\b', h))
orig_close = len(re.findall(r'</div>', h))
print(f'[init] div open={orig_open} close={orig_close}')

def diag(step):
    global h
    o = len(re.findall(r'<div\b', h)); c = len(re.findall(r'</div>', h))
    print(f'[{step}] open={o} close={c} drift_o={o-orig_open} drift_c={c-orig_close}')

def rep(old, new, step, cnt=1):
    global h
    n = h.count(old)
    assert n == cnt, f'{step}: expected {cnt} got {n} for {old[:70]!r}'
    h = h.replace(old, new, cnt)
    diag(step)

TODAY = date.today()
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')

# ============ 1. marker + header badge（闸0/闸1，必须第一步） ============
h = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
           f'<!-- daily-update: {TODAY} -->', h, count=1)
h = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
           f'📅 数据区间：{lower} — {upper}（每日更新）', h, count=1)
diag('01 marker/badge')

# ============ 2. S0 context ============
rep('<span class="section-context">9月25日 · 4条今日要闻</span>',
    '<span class="section-context">9月28日 · 4条今日要闻</span>', '02 s0-context')

# ============ 3. S0 四卡全换（09-28 T+0） ============
S0_START = '            <!-- S0 Card 1 (09-25 P1) -->'
S0_END = '<!-- ============ Section 1: 重磅信息 ============ -->'
i0 = h.index(S0_START); i1 = h.index(S0_END)

S0_NEW = '''            <!-- S0 Card 1 (09-28 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 债券型ETF规模首破万亿·53只合计10107.21亿·较年初增21.92%·科创债ETF成最大品类</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          证券时报基金研究院陈书玉9月28日报道（同花顺财经转刊）：在机构配置需求、产品创新及制度优化多重力量推动下，国内债券型ETF实现跨越式增长。数据显示，截至9月27日，全市场<b>53只债券型ETF合计规模达10107.21亿元</b>，<b>首次突破万亿关口</b>；较年初的8290.24亿元增加<b>1816.97亿元</b>，增幅<b>21.92%</b>。<br>
          <b>产品格局：</b>53只债券型ETF中<b>37只规模突破100亿元</b>——短融ETF海富通840.52亿元居首，可转债ETF博时607.98亿元、城投债ETF海富通555.35亿元次之，政金债ETF富国、公司债ETF平安、科创债ETF嘉实规模均超400亿元。按品类看，<b>科创债ETF是当前体量最大的品类，24只合计3595.13亿元</b>，其中科创债ETF嘉实437.36亿元最大，科创债ETF银华、汇添富、华夏规模均超200亿元。<br>
          <b>机构集中度：</b>全市场28家基金公司布局债券型ETF，<b>仅海富通（6只、1851.69亿元）与博时（5只、1077.93亿元）合计规模超千亿</b>；富国、华夏、易方达均超500亿元，平安、南方、国泰、嘉实均超400亿元。节奏上，2013年3月首只债券ETF成立，2024年5月总规模首破1000亿元，2025年2月破2000亿、7月破5000亿、年末8290亿，2026年9月首破万亿。<br>
          <b>成因：</b>多数债券型ETF机构持有比例超九成，理财净值化转型后机构资金对低波动、高流动性工具需求持续增长；债券ETF陆续纳入回购质押券范围、担保品使用场景拓宽，工具属性增强；近两年做市商、券商自营参与做市，流动性改善进一步吸引资金流入。华夏基金归纳四大优势：T+0二级买卖与申赎、交易门槛低、多数免印花税过户费且主流券商免佣金、部分可高比例质押融资。<br>
          <b>对腾安启示：</b>万亿级别的债券ETF已是机构资金的主流工具而非小众品种——货架应把债券ETF从“债基附属”提升为独立品类，并按<b>细分品类（科创债/短融/城投债/可转债/政金债）+久期+规模+质押资格</b>四维筛选；同时提示“机构持有超九成”意味着个人投资者需更关注二级流动性与折溢价，而非只看静态收益率。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260928/c680289535.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·证券时报·09-28</span></a>
          <a href="https://news.qq.com/rain/a/20260928A036Q600" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·09-28</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
<!-- S0 Card 2 (09-28 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 多元配置型FOF供需两旺·下半年新成立FOF 112只逾四成为多元配置·近一年平均回报超4%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报记者朱妍9月28日报道：曾经在单边行情中承压的多元配置策略近期价值重现，相关FOF产品迎来供需两旺。<br>
          <b>供给端：</b>Choice数据显示，今年下半年以来截至9月27日，新成立公募FOF<b>112只</b>（不同份额分开计算），其中<b>逾四成为多元配置型FOF</b>（近50只）；民生加银、中信建投等公司均有产品正在发售；10月还有鹏扬多元睿盈六个月持有混合（FOF）、中欧盛裕多元配置6个月持有混合（FOF）等启动发行。申报端同样密集——9月23日建信泓裕多元配置3个月持有期混合（ETF-FOF）上报，华商汇启多元配置3个月持有混合（FOF）、海富通聚盈稳健多元配置6个月持有期混合发起式（FOF）、万家启和多元配置三个月持有期混合（ETF-FOF）等纷纷在9月上报。<br>
          <b>需求端：</b>三季度以来多只相关产品首募规模超5亿元，汇添富多资产优选三个月持有混合（FOF）募集规模超<b>20亿元</b>，广发富泽多元配置三个月持有混合（ETF-FOF）首募超<b>10亿元</b>。业绩上，截至9月27日近一个月多元配置型FOF在FOF中业绩领先；近一年维度，有完整统计周期的多元配置型FOF<b>全部获得正回报、平均回报超4%，同期平均最大回撤约3%</b>，两项指标均优于同期全部FOF平均。<br>
          <b>机构观点：</b>中欧基金邓达表示，多元资产配置的底层框架是追求风险资产多元化与大类资产再平衡；格上基金谢诗琦认为三季度以来板块轮动加快、股债商驱动逻辑重新分化、资产间相关性回落，多元配置迎来更易发挥优势的阶段；鹏扬基金赵会龙建议权益采用哑铃结构（价值质量蓝筹＋回调后的科技成长），债券以中短端高等级为底仓；宏利基金张晓龙看好铜的配置逻辑（高通胀支撑工业需求＋映射AI算力与电力需求）。<br>
          <b>对腾安启示：</b>多元配置型FOF以“正回报＋低回撤”正在承接从单一赛道基金流出的资金——货架可把此类产品单列为“组合解决方案”层，并强制展示<b>近一年回报、最大回撤、持有期</b>三要素；对同一公司旗下名称相近的多只多元配置FOF，需做持仓穿透与策略区分，避免用户仅按名称盲选。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/795962" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-28</span></a>
          <a href="https://www.mrjjxw.com/articles/2026-09-28/4592493.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-28</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
<!-- S0 Card 3 (09-28 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 超千只基金近两年业绩翻倍·1427只收益超100%·排名前10%平均最大回撤31.9%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          证券时报基金研究院陈书玉9月28日报道（和讯网转刊）：在科技成长产业景气带动下，公募基金迎来一轮业绩大丰收。Wind数据显示，近两年截至2026年9月23日，全市场<b>11420只</b>基金（仅统计主份额）中，<b>1427只收益率超100%</b>、329只超200%、92只超300%、<b>5只超500%</b>；信澳业绩驱动A以<b>566.42%</b>拔得头筹，前海开源沪港深乐享生活、财通多策略福鑫、财通集成电路产业A、财通景气甄选一年持有A均超500%。全部基金收益率算术平均值<b>44.11%</b>、中位数<b>22.33%</b>，说明整体收益主要由头部产品拉动。<br>
          <b>两年斜率分化：</b>第一年（2024年9月下旬—2025年9月23日）正收益占比<b>99.2%</b>、中位数24.76%，几乎全员赚钱；第二年（2025年9月下旬—2026年9月23日）正收益占比回落至<b>76.8%</b>、中位数仅<b>2.69%</b>。盈利基金近两年收益中位数贡献约<b>74%来自第一年</b>，第二年转入震荡分化，未持仓AI、半导体方向的产品收益斜率显著走平。<br>
          <b>高收益的另一面：</b>收益排名<b>前10%的基金平均最大回撤达31.9%</b>，而后10%仅9.8%——高收益本质是对高波动的补偿。涨幅居前产品截至二季报普遍重仓光通信、半导体（如信澳业绩驱动A前十大含中际旭创、新易盛、天孚通信、源杰科技等）。<br>
          <b>ETF与经营逻辑：</b>全市场ETF规模从2024年9月约3.4万亿元增至目前约<b>4.9万亿元</b>、产品数由997只增至1696只；190只ETF近两年收益超100%，科创芯片ETF南方以330.41%居首。规模增长最大的反而是黄金ETF华安（增826.92亿元、已超千亿）与短融ETF海富通（增583.12亿元），说明<b>资金涌入方向并不与业绩表现一致</b>。更深层变化是行业经营逻辑从追逐爆款、依赖明星，转向搭建平台、经营“货架”，从“卖产品”转向“配资产”。<br>
          <b>对腾安启示：</b>“1427只翻倍”是极强的营销素材，但中位数22.33%、第二年正收益占比仅76.8%说明分化极大——<b>货架展示须用中位数而非头部极值做预期锚</b>，并把“最大回撤”与“收益来源年份拆解”前置到产品页；对近两年涨幅居前的算力/半导体主题基金，应同步加挂波动与集中度提示，避免用户把历史收益线性外推。
        </div>
        <div class="card-footer">
          <a href="https://stock.hexun.com/2026-09-28/225064095.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">和讯网·证券时报网·09-28</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
<!-- S0 Card 4 (09-28 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 医药主题基金霸榜三季度业绩·近三月主动权益前15名全为医药·招商李佳存包揽前四</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          证券时报记者安仲文9月28日报道（东方财富“券商基金早参”9月28日转载）：三季度即将收官，沉寂近半年的医药基金迎来强势反扑，从陪跑变成主跑。Wind数据显示，<b>近三个月全市场可统计主动权益基金中，区间涨幅前15名全部为医药主题产品</b>。<br>
          <b>榜单结构：</b>招商基金李佳存一人包揽前四位——招商前沿医疗保健<b>50.60%</b>、招商品质成长<b>49.67%</b>、招商创新增长<b>48.27%</b>、招商医药健康产业<b>46.03%</b>；华泰柏瑞医疗健康、广发医药精选股票、前海开源医疗健康等亦跻身前列。收益高度集中在三季度：招商前沿医疗保健年内收益55.47%、其中近三个月贡献50.60%；广发医药精选股票年内收益31.57%、近三个月达40.13%，上半年尚处亏损。<br>
          <b>驱动逻辑：</b>创新药出海叙事得到验证——9月14日国家药监局披露，2026年1—8月国内创新药对外授权（BD）交易总额突破<b>1200亿美元</b>、同比增长<b>36%</b>，已接近2025年全年1300亿美元规模；BD放量带动全球医药研发需求向国内转移，CXO景气预期与新增订单抬升。叠加前期AI、光模块、半导体等热门赛道拥挤度上升、波动放大，部分机构兑现浮盈后转向公募配置偏低的估值洼地。<br>
          <b>对腾安启示：</b>榜单“前15名全为医药”是典型的风格切换信号，但也是<b>短期业绩极值最容易诱导追高</b>的场景——货架与内容运营应把“近三月收益”与“近三年收益、最大回撤、仓位集中度”并列展示，并对单季度贡献绝大部分年内收益的产品加注“收益高度集中于单一季度”的说明；医药主题内部差异极大，须按创新药、CXO、医疗器械、中药等二级方向做区分，不能按“医药”一个标签整体推荐。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202609283884590923.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·券商基金早参·09-28</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>    </div>
  </div>
'''
h = h[:i0] + S0_NEW + h[i1:]
diag('03 s0-cards')

# ============ 4. fingerprint 同步（闸6） ============
rep('<meta name="content-fingerprint" content="德邦基金|新发基金|首批18只|ETF资金">',
    '<meta name="content-fingerprint" content="债券型ETF|多元配置|超千只基|医药主题">',
    '04 fingerprint')

# ============ 5. S1：删 09-13 代销百强榜（超 T-14），补 09-28 险资港股通ETF ============
s1_del_start = h.index('            <!-- S1 Card: 中基协代销百强榜 蚂蚁破2.2万亿 腾安跻身第五 (09-13 P0) -->')
s1_del_end = h.index('      <!-- S1 Card: 8月末公募规模39.63万亿 (09-19 P1) -->')

S1_NEW = '''      <!-- S1 Card: 险资可投港股通ETF监管口径明确 (09-28 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 监管明确险资可投港股通ETF·金融监管总局办公厅发函·9月20日起实施·港股通ETF共31只</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          证券日报9月28日报道（同花顺财经转刊）：多家险企近日收到国家金融监督管理总局办公厅下发的《关于明确保险资金投资港股通ETF监管口径的函》。函件明确，<b>按照监管规定可投资港股通股票的保险机构，可以投资内地与香港股票市场交易互联互通机制中的交易型开放式基金（港股通ETF），参照保险资金投资港股通股票的相关监管规定执行</b>，该监管口径自发布之日（<b>2026年9月20日</b>）起实施。数据显示，截至9月27日纳入港股通范围的ETF基金共<b>31只</b>，全部为股票型基金。<br>
          <b>为何关键：</b>此前险资只能通过港股通投资个股，或通过QDII投资港股ETF——前者工具单一，后者受额度制约。港股通ETF<b>不占用稀缺的QDII额度</b>，且配置权限与现有港股通资格直接挂钩、无需额外审批，从制度层面解决了险资境外配置的额度瓶颈。某保险资管公司人士称，此前境外投资占比仅小个位数，QDII额度长期紧张、审批存在不确定性。<br>
          <b>时间线：</b>2016年监管部门发布《关于保险资金参与沪港通试点的监管口径》，2017年深港通纳入险资投资范围；2022年ETF正式纳入内地与香港互联互通机制，但<b>尚未允许险资直接投资港股通ETF</b>；2026年8月金融监管总局提出支持内地保险机构通过沪深港通投资香港交易所买卖基金，本次《监管口径函》落地。<br>
          <b>体量与节奏：</b>金融监管总局数据显示，截至2026年二季度末险资运用余额已突破<b>40万亿元</b>，其中投向股票和证券投资基金合计余额达<b>6.39万亿元</b>。东吴证券研报认为港股通ETF中包含跨境投资产品，或成为内地险资境外投资新突破口，但海外高息固收资产更符合当前配置需求，海外权益短期尚不足以成为配置主力；受访人士提示港股通ETF在险资会计分类中默认计入FVTPL，实际增配节奏可能以试点配置和分阶段建仓为主。<br>
          <b>对腾安启示：</b>险资是典型的长期配置型资金，放开后对香港ETF市场是持续的南向“长钱”——面向机构与高净值客群，可提前准备港股通ETF的<b>标的清单、跟踪指数、规模与流动性、溢价率</b>四维展示模板；对个人投资者则须强调“险资开闸≠短期上涨”，跨境ETF仍受额度、汇率与溢价风险约束，避免在政策消息面放大情绪化申购。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260928/c680289519.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·证券日报·09-28</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

'''
h = h[:s1_del_start] + S1_NEW + h[s1_del_end:]
diag('05 s1')

# ============ 6. S4：删 09-12 券商56席 + 09-13 三方首超银行（均超 T-14），补 2 张 09-28 卡 ============
s4_del_start = h.index('            <div class="card p1">\n        <div class="card-top">\n          <div class="card-title">🟡 代销百强榜券商占56席')
s4_del_end = h.index('      <!-- S4 Card: 9月31只ETF成立 科技成长主线 (09-21 P1) -->')

S4_NEW = '''      <!-- S4 Card: 商业不动产REITs扩容 (09-28 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 商业不动产REITs稳慎扩容·3只同日获受理·华夏凯华或成首单纺织专业市场REIT</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报记者昝秀丽9月28日报道（同花顺财经转刊）：9月24日，<b>汇添富顺联商业REIT、华夏凯华商业REIT、华夏世纪金源商业REIT同日获受理</b>，商业不动产公募REITs又迎新成员，释放出有关部门稳慎推进商业不动产REITs发展的明确信号。<br>
          <b>资产类型持续拓宽：</b>9月20日招商资管招商蛇口封闭式商业不动产证券投资基金正式获批，底层资产为深圳太子广场与苏州昆山招商花园城项目，与蛇口产园REIT、蛇口租赁住房REIT及招商局商业房托共同形成覆盖产业园区、租赁住房、商业不动产及境外物业的全品类资本化矩阵。9月3日创金合信北京国资公司REIT在深交所挂牌，为全国首单“科技创新＋城市更新”主题商业不动产公募REIT、深交所首单获批上市项目。近期获受理的华夏凯华商业REIT首发底层资产为广州国际轻纺城AB区，若顺利上市将成为<b>国内首单纺织类专业市场REIT</b>。新城控股公告广发新城吾悦封闭式商业不动产证券投资基金9月3日获证监会注册。<br>
          <b>机构间REITs并行：</b>凯德投资发起的中金凯德商业持有型不动产资产支持专项计划（凯德优选）完成设立；国泰海通—电建地产不动产资产支持专项计划（机构间REIT）近期获受理。7月24日沪深交易所分别修订发布大类基础资产适用指引，<b>新增机构间REITs特别规定章节</b>，明确其需具备无外部增信、平层结构、无强制回购、主动管理等权益属性特征，分红比例原则上应达<b>90%以上</b>、扩募申请不设间隔期。高和资本周以升认为，成熟REITs市场应当是机构间与公募并行发展的多层次平台体系。<br>
          <b>对腾安影响：</b>REITs品类正从高速公路、产业园向商业不动产、纺织专业市场等细分资产扩张，且公募与机构间双轨并行——货架需按<b>底层资产类型＋分派率＋估值溢价率＋扩募历史</b>建立统一筛选口径，并对“首单某某资产”类产品加注资产单一集中风险；同时关注商业不动产REITs与地产链基金的持仓重叠，避免客户在同一风险敞口上重复配置。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260928/c680289773.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·中国证券报·09-28</span></a>
          <span class="impact-tag medium">供给扩容：中</span>
        </div>
      </div>

      <!-- S4 Card: 科技主题基金松绑限购 (09-28 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多只科技主题基金“松绑”限购·易方达信息产业混合单日申购上限由1万元上调至50万元</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          证券时报网9月28日报道（和讯网转刊）：易方达基金旗下<b>易方达信息行业精选股票与易方达信息产业混合</b>双双公告，单日单个基金账户在全部销售机构累计申购A类或C类份额金额调整为不超过<b>50万元</b>——而在3个月前，两只基金单日申购上限均为<b>1万元</b>。两只产品均为郑希在管，2026年上半年保持较高仓位，以信息产业成长性投资品种为核心，提升了AI算力、半导体配置比例，降低软件、消费电子配置，前十大重仓股均包括新易盛、中际旭创、三环集团、生益科技、源杰科技等。<br>
          <b>不止易方达：</b>自7月以来多只科技赛道主动权益基金陆续上调大额申购限额或取消限制——华商优势行业混合自7月21日起恢复大额申购、大额转换转入及大额定期定额投资；华商均衡成长混合单日申购上限由6月下旬的1000元连续上调至7月的10万元、200万元；财通成长优选混合自7月22日起取消申购、定投及转换转入金额限制。<br>
          <b>机构解读：</b>前海开源基金首席经济学家杨德龙对证券日报记者表示，此前部分主动权益基金主动收紧甚至暂停大额申购，是为保护持有人利益、规避资金集中涌入放大持仓波动；<b>随着科技板块显著回调、估值有所回落，相关产品相继放宽申购约束，也在一定程度上折射出公募机构判断市场调整已进入相对充分阶段</b>。多位业内人士继续看好AI相关投资机会。<br>
          <b>对腾安影响：</b>“限购—松绑”是管理人给出的隐性仓位与估值信号，比口头观点更有信息量——可建立<b>限购状态变更监控</b>，对同一基金经理在管产品的申购上限变化做时间序列展示，并在松绑时同步提示“管理人认为估值风险已部分释放”与“资金涌入可能摊薄后续收益”两面信息；同时注意松绑不等于推荐，仍需按持仓集中度与回撤水平做匹配。
        </div>
        <div class="card-footer">
          <a href="https://stock.hexun.com/2026-09-28/225064083.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">和讯网·证券时报网·09-28</span></a>
          <span class="impact-tag medium">供给节奏：中</span>
        </div>
      </div>

'''
h = h[:s4_del_start] + S4_NEW + h[s4_del_end:]
diag('06 s4')

# ============ 7. S6 行情：A股维持 09-24 收盘，港美股更新至 09-25 收盘 + 09-28 盘中快照 ============
s6_start = h.index('            <div class="card p3">', h.index('市场行情速览'))
s6_end = h.index('<!-- ============ Section 7')

S6_NEW = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股09-24收盘·沪指3888.37 -1.22%沪深北成交1.67万亿｜港美股09-25收盘｜09-28盘中重挫</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-28</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-24收盘·中秋假期前缩量回调）</b><br>
              上证指数 <b>3888.37</b> <span style="color:#52c41a;">-1.22%</span><br>
              深证成指 <b>13316.97</b> <span style="color:#52c41a;">-2.34%</span><br>
              创业板指 <b>3288.95</b> <span style="color:#52c41a;">-2.68%</span><br>
              沪深300 <b>4439.14</b> <span style="color:#52c41a;">-1.73%</span><br>
              科创50 <b>1621.87</b> <span style="color:#52c41a;">-2.35%</span><br>
              北证50 <b>1055.74</b> <span style="color:#52c41a;">-1.70%</span><br>
              沪深北三市成交 <b>1.67万亿</b>·较上日缩量1140亿<br>
              逾1100只上涨·逾50只涨停；超4300只下跌
            </div>
            <div>
              <b>港股与美股（09-25收盘）</b><br>
              恒生指数 <b>24510.09</b> <span style="color:#52c41a;">-1.01%</span><br>
              恒生科技 <b>4311.78</b> <span style="color:#52c41a;">-1.13%</span><br>
              国企指数 <b>8165.78</b> <span style="color:#52c41a;">-1.21%</span><br>
              道琼斯 <b>51828.62</b> <span style="color:#dc2626;">+0.93%</span><br>
              纳斯达克 <b>27068.72</b> <span style="color:#dc2626;">+0.48%</span><br>
              标普500 <b>7743.41</b> <span style="color:#dc2626;">+0.51%</span><br>
              WTI原油92.44美元 <span style="color:#52c41a;">-2.29%</span>·现货黄金4285.37美元 <span style="color:#dc2626;">+0.25%</span>·美债10年期维持5%以上
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>节后首日（09-28 盘中快照·约11:00）：</b>中秋假期后首个交易日A股大幅低开重挫，截至上午11点沪指跌<b>1.83%</b>报3817.26点、深证成指跌<b>3.45%</b>报12857.78点、创业板指跌<b>4.41%</b>报3143.92点、沪深300跌2.27%报4338.45点、科创50跌<b>4.29%</b>报1552.36点、北证50跌1.90%；算力硬件、有色金属、锂电、农业方向跌幅居前，沪深京三市下跌个股一度近4500只。<b>注：以上为盘中数据、非收盘价。</b><br>
              <b>假期外围（美股09-25收盘）：</b>美股三大指数全线上涨，道指涨0.93%报51828.62点、标普500涨0.51%报7743.41点、纳指涨0.48%报27068.72点；全周道指累涨0.28%（终结周线三连跌）、标普500涨1.21%、纳指涨2.06%。苹果涨1.53%报341.07美元创收盘新高、市值逼近5万亿美元；Meta因智能体Muse遭遇算力瓶颈周五跌3.33%，但全周仍涨12.99%；费城半导体指数周五涨1.41%、全周涨6.27%实现周线四连涨。伊朗提出七日内重开霍尔木兹海峡计划令油价自高位回落，WTI原油跌2.29%报92.44美元；COMEX黄金涨0.52%报4320.5美元、现货黄金涨0.25%报4285.37美元。<br>
              <b>港股（09-25收盘）：</b>A股休市、北水缺席下港股延续跌势，恒指跌1.01%报24510.09点、国企指数跌1.21%报8165.78点、恒生科技跌1.13%报4311.78点，大市成交额缩至1022亿港元；全周恒指累跌0.97%、恒生科技累跌2.13%、国企指数累跌0.72%。科网股普遍走弱，阿里巴巴跌1.5%、腾讯跌0.4%、美团跌0.8%、小米跌2.6%、京东跌1.8%；汽车股弱势，理想跌3.3%、比亚迪跌1.8%；医药逆势走强，药明生物涨2.1%、药明康德涨2.2%。9月28日早盘恒指回升至24675点附近、涨约0.68%（盘中数据）。<br>
              <b>备注：</b>9月24日为中秋假期前最后一个交易日，9月25日—27日A股休市、9月28日恢复交易；本期A股基准为假期前最后交易日（09-24）收盘，港股与美股基准为09-25收盘，09-28数据为盘中快照、仅供参考。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股2026-09-24收盘 / 港美股09-25收盘 · 09-28盘中快照</span>
          <span class="source-tag">数据来源：同花顺财经（四大证券报头版精华）、中国证券网、新华社、中新社/央广网、财联社、东方财富网（09-24—09-28）</span>
        </div>
      </div>  </div>
'''
h = h[:s6_start] + S6_NEW + h[s6_end:]
diag('07 s6')

# ============ 8. S7 时间线重写（12 条降序） ============
items = [
    ('red',   '2026-09-28', '债券ETF规模首破万亿'),
    ('red',   '2026-09-28', '多元配置型FOF供需两旺'),
    ('red',   '2026-09-28', 'A股节后首日重挫创业板跌逾4%'),
    ('blue',  '2026-09-28', '险资可投港股通ETF开闸'),
    ('blue',  '2026-09-28', '商业不动产REITs三只获受理'),
    ('red',   '2026-09-25', '湖南百亿未来产业基金落地'),
    ('red',   '2026-09-24', '中秋前A股缩量回调失守3900'),
    ('blue',  '2026-09-24', '国新国证张鹏任总经理'),
    ('blue',  '2026-09-24', '中基协发布团体标准管理办法'),
    ('blue',  '2026-09-24', '博道基金业绩比较基准修订生效'),
    ('blue',  '2026-09-23', '公募秋季策略会密集举办'),
    ('blue',  '2026-09-23', '机构称四季度有吃饭行情'),
]
tl = ''.join(
    '      <div class="timeline-item">\n'
    f'        <div class="timeline-dot {c}"></div>\n'
    f'        <div class="timeline-date">{d}</div>\n'
    f'        <div class="timeline-title">{t}</div>\n'
    '      </div>\n' for c, d, t in items)

k = h.index('关键时间线')
tl_start = h.index('      <div class="timeline-item">', k)
tl_end = h.index('\n    </div>\n\n  </div>', tl_start) + 1
h = h[:tl_start] + tl + h[tl_end:]
diag('08 s7')

# ============ 9. Phase1 全量断言 ============
def count_divs(s):
    return len(re.findall(r'<div\b', s)), len(re.findall(r'</div>', s))

o, c = count_divs(h)
assert o == c, f'div 不平衡 open={o} close={c}'
print(f'[final] open={o} close={c} drift_o={o-orig_open} drift_c={c-orig_close}')

assert 'S8' not in h, 'S8 出现！'
assert '待办跟踪' not in h, 'S8 残留「待办跟踪」'
assert h.count('\ufffd') == 0, 'U+FFFD 乱码'
assert h.count('</div>>') == 0, 'stray </div>>'

# S0 section 标题与 context
s0 = h[h.index('Section 0'):h.index('Section 1')]
titles = re.findall(r'<div class="card-title">([^<]+)</div>', s0)
assert len(titles) == 4, f'S0 卡数 {len(titles)} != 4'
assert '<span class="section-title">今日焦点</span>' in s0, 'S0 title 不是「今日焦点」'
assert '<span class="section-context">9月28日 · 4条今日要闻</span>' in s0, 'S0 context 未更新'
assert s0.count('action-box') == 0, '本日无 P0，不应有 action-box'
# S0 date-tag 全部 09-28（正则，返回元组）
dt0 = re.findall(r'date-tag">(\d{2})-(\d{2})<', s0)
assert dt0 == [('09', '28')] * 4, f'S0 date-tag 异常：{dt0}'
# S0 链接数：卡1=2 + 卡2=2 + 卡3=1 + 卡4=1 = 6
_n_link = s0.count('href="http')
assert _n_link == 6, f'S0 链接数 {_n_link} != 6'

# 指纹
fp = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', h).group(1)
for seg in [x for x in fp.split('|') if x.strip()]:
    assert any(seg[:4] in t for t in titles), f'指纹段 {seg} 未命中 S0 标题'

# section marker 完整
for n in range(0, 8):
    assert f'Section {n}' in h, f'Section {n} marker 缺失'

# S1=6 / S2=4 / S4=3 / S5=3 / S7=12
def n_cards(sec_name, nxt):
    seg = h[h.index(sec_name):h.index(nxt)]
    return len(re.findall(r'<div class="card p', seg))
assert n_cards('Section 1', 'Section 2') == 6, 'S1 卡数 != 6'
assert n_cards('Section 2', 'Section 3') == 4, 'S2 卡数 != 4'
assert n_cards('Section 4', 'Section 5') == 3, 'S4 卡数 != 3'
assert n_cards('Section 5', 'Section 6') == 3, 'S5 卡数 != 3'
seg7 = h[h.index('Section 7'):]
assert len(re.findall(r'<div class="timeline-item">', seg7)) == 12, 'S7 条目 != 12'

# 新增段黑名单自检
BAD = ['stcn.com', 'cls.cn', 'toutiao', '21jingji', 'yicai.com', '163.com/dy', 'sohu.com', 'guba.eastmoney']
new_seg = S0_NEW + S1_NEW + S4_NEW + S6_NEW
for b in BAD:
    assert b not in new_seg, f'新增段含黑名单/低质源 {b}'

# date-tag 全量 >= T-14
t14 = TODAY - timedelta(days=14)
for mo, d in re.findall(r'date-tag">(\d{2})-(\d{2})<', h):
    dt = date(TODAY.year, int(mo), int(d))
    assert dt >= t14, f'date-tag {dt} 超 T-14（{t14}）'

open(P, 'w', encoding='utf-8').write(h)
print('✅ 全部断言通过，已写入 index.html')
