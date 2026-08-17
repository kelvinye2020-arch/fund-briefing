# -*- coding: utf-8 -*-
import io

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

REPLS = []

# 1) daily-update marker
REPLS.append(("marker",
    "<!-- daily-update: 2026-07-10 -->",
    "<!-- daily-update: 2026-07-11 -->"))

# 2) data-interval badge
REPLS.append(("badge",
    "📅 数据区间：2026.06.26 — 2026.07.10（每日更新）",
    "📅 数据区间：2026.06.27 — 2026.07.11（每日更新）"))

# 3) Stats Bar
REPLS.append(("stats",
"""  <div class="stat-card">
    <div class="stat-number">39.48万亿</div>
    <div class="stat-label">公募总规模（截至2026年5月底·逼近40万亿）</div>
    <div class="stat-change up">▲ 固收+贡献主力·权益份额仍处低位</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">4053.64</div>
    <div class="stat-label">上证综指 · 07-10盘中（开盘-0.13%·盘中回升+0.42%）</div>
    <div class="stat-change up">▲ 创业板+0.97%·科创50+1.93%·CPO/半导体领涨</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">96.38亿</div>
    <div class="stat-label">科创50ETF · 7月累计吸金（逆转二季度净流出）</div>
    <div class="stat-change up">▲ 半导体设备ETF国泰破500亿创新高·AI赛道ETF大举吸金</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">5668亿</div>
    <div class="stat-label">科技主题主动权益基金规模（178只·截至7月8日）</div>
    <div class="stat-change neutral">■ 科技成长仍是下半年公募重点配置方向</div>
  </div>""",
"""  <div class="stat-card">
    <div class="stat-number">39.48万亿</div>
    <div class="stat-label">公募总规模（截至2026年5月底·二季报披露季开启）</div>
    <div class="stat-change up">▲ 二季报含科量成业绩密码·科技持仓主导</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">3996.16</div>
    <div class="stat-label">上证综指 · 07-10收盘（跌1.00%·失守4000点·科创50-5.53%）</div>
    <div class="stat-change down">▼ 创业板-4.37%·半导体一日游后暴跌·成交3.41万亿</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">85家</div>
    <div class="stat-label">年内公募高管变动（人才大年·基金经理离任232人次）</div>
    <div class="stat-change neutral">■ 诺安总经理齐斌离任·去明星化提速</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">5668亿</div>
    <div class="stat-label">科技主题主动权益基金规模（178只·含科量成业绩密码）</div>
    <div class="stat-change neutral">■ 基金经理逻辑转向"业绩兑现"</div>
  </div>"""))

# 3b) S0 section title
REPLS.append(("s0title",
    '      <span class="section-title">今日焦点（7月10日·周五·AI赛道ETF大举吸金·科创50ETF成净流入最多宽基·首批REITs全收益基金结募·科技主题基金破5600亿）</span>',
    '      <span class="section-title">今日焦点（7月11日·周六·二季报含科量成业绩密码·公募人才变局·7月新发121只·周五科创50暴跌5.53%）</span>'))

# 4) S0 cards (whole block)
REPLS.append(("s0cards",
"""    <div class="card-grid">

      <!-- S0 Card 1: AI赛道ETF大举吸金·科创50ETF成净流入最多宽基 (T+0 07-10) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 AI赛道ETF昨日大举吸金·科创50ETF成净流入最多宽基·半导体设备ETF破500亿创新高</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>资金回流硬科技：</b>Choice数据显示，7月9日20只科创50ETF净流入<b>22.14亿元</b>，成为市场净流入最多的核心宽基，本月已累计吸金<b>96.38亿元</b>，逆转此前二季度持续净流出态势。规模最大的科创50ETF华夏重回700亿关口至719.84亿。<br>
          <b>芯片细分更吸金：</b>跟踪半导体材料设备指数的5只产品单日吸金<b>59.4亿元</b>居首；半导体设备ETF国泰单日净流入48.75亿元，最新规模突破<b>500亿元</b>创新高至502.53亿；科创半导体ETF华夏、通信ETF国泰分别吸金21.72亿、12.12亿，均刷新纪录。<br>
          <b>对基金行业影响：</b>资金重新聚焦AI/半导体赛道→腾安可顺势强化科创50/半导体主题ETF货架，同时提示板块拥挤与高位波动风险。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1FFKHO505198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <span class="impact-tag high">ETF资金流：高</span>
        </div>
      </div>

      <!-- S0 Card 2: A股07-10开盘涨跌不一·CPO大涨·贵金属反弹 (T+0 07-10) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 A股07-10开盘涨跌不一·CPO/苹果产业链领涨·贵金属集体反弹·盘中三大指数翻红</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>盘面回升：</b>7月10日A股三大股指开盘涨跌不一，沪指-0.13%报4031.54点、深成指+0.53%、创业板指+0.59%；盘中震荡走高，沪指涨幅扩至<b>+0.42%</b>（4053.64）、创业板<b>+0.97%</b>、科创50<b>+1.93%</b>（2228.11）。<br>
          <b>热点扩散：</b>CPO概念延续强势，华天科技涨停、剑桥科技涨超8%、光迅/长电涨超5%；苹果产业链、6G、光芯片、内存概念涨幅居前；贵金属集体反弹。油气、教育、煤炭、能源金属走弱。<br>
          <b>对基金行业影响：</b>科技成长主线延续、避险板块反弹→腾安可提示科技类基金短线波动、关注哑铃配置价值。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1FFDB4H0519C6T9.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中新经纬</span></a>
          <span class="impact-tag medium">A股行情：中</span>
        </div>
      </div>

      <!-- S0 Card 3: 首批REITs全收益指数基金全部结募 (T+0 07-10) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 首批REITs全收益指数基金全部结募·4只带来12亿增量·REITs指数化投资加速</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行亮眼：</b>截至7月8日，首批<b>4只</b>中证REITs全收益指数基金全部结束募集，有的提前结募、有的一日售罄比例配售，按每只3亿元规模计将带来约<b>12亿元</b>增量资金，成立后陆续建仓入市。<br>
          <b>产品特征：</b>4只属FOF型指数产品，业绩比较基准为"中证REITs全收益指数收益率×95%+活期存款基准利率×5%"，投资标的指数成分券及备选券比例不低于基金资产净值的90%。<br>
          <b>对基金行业影响：</b>REITs进入指数化配置时代→腾安可补充REITs指数基金货架，作为客户资产配置中低相关性的另类工具。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260710A02E4J00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">REITs指数化：中</span>
        </div>
      </div>

      <!-- S0 Card 4: 科技主题主动权益基金规模超5600亿 (T+0 07-10) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 科技主题主动权益基金规模超5600亿·178只·基金经理转向"业绩兑现"逻辑</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模透视：</b>截至7月8日，名称含人工智能、半导体、通信设备、机器人等字样的主动权益基金产品达<b>178只</b>（仅统计主份额），合计规模约<b>5668.83亿元</b>，科技成长成为公募重仓主线。<br>
          <b>逻辑切换：</b>随着部分科技板块估值抬升，基金经理投资逻辑正从"关注产业趋势与估值扩张"转向"寻找业绩兑现能力更强的企业"；多位基金经理表示下半年科技成长仍是重点配置方向。<br>
          <b>对基金行业影响：</b>科技主题基金体量庞大→腾安推荐时需在"高景气"与"高拥挤"间平衡，引导客户关注业绩兑现确定性而非单纯题材。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260710A02E4J00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">科技主题基金：中</span>
        </div>
      </div>

    </div>
  </div>""",
"""    <div class="card-grid">

      <!-- S0 Card 1: 公募二季报披露拉开帷幕·含科量成业绩密码 (T+0 07-11) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露拉开帷幕·含科量成业绩密码·10只主动权益8只Q2净值增长超70%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>二季报开闸：</b>截至7月10日，已有同泰、红土创新、中银旗下<b>13只</b>基金披露2026年二季报，10只主动权益类基金报告期内均实现净值正增长，其中<b>8只Q2净值增长率超70%</b>。<br>
          <b>含科量密码：</b>同泰数字经济股票A、同泰行业优选股票A Q2分别增长<b>101.98%</b>、<b>73.62%</b>；盖俊龙管理的红土创新多只产品Q2增长率均超90%；前十大重仓普遍含中际旭创、新易盛、东山精密等AI算力链。<br>
          <b>对基金行业影响：</b>"含科量"成业绩分水岭→腾安可借二季报强化科技赛道基金解读与持营话术，同时提示单一赛道波动风险。
        </div>
        <div class="card-footer">
          <a href="http://m.ce.cn/cj/gd/202607/t20260711_3081918.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济日报</span></a>
          <span class="impact-tag high">二季报：高</span>
        </div>
      </div>

      <!-- S0 Card 2: 7月121只新基发行又见小高峰·指数化+固收+双主线 (T-1 07-10) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 7月121只新基发行又见小高峰·易方达8只领衔·指数化与固收+并进</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行小高峰：</b>Choice统计，仅计主代码，7月共有<b>121只</b>基金启动认购、由58家公募发行；104只集中在上半月（占全月超八成），首周68只、7月1日单日32只、3只一日售罄。<br>
          <b>双主线：</b>头部公募抢滩上半月，易方达新基最多（8只）、广发/华泰柏瑞/华夏/汇添富各5只；产品呈"指数化+固收+"双主线，化工赛道成7月布局热点，超九成认购天数≤30天。<br>
          <b>对基金行业影响：</b>发行回暖→腾安可丰富权益/主题ETF与固收+货架，把握新发与持营窗口。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260710090619a476a81b" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯证券·财联社</span></a>
          <span class="impact-tag medium">新发热度：中</span>
        </div>
      </div>

      <!-- S0 Card 3: 公募人才变局·诺安总经理齐斌离任·基金经理去明星化 (T+0 07-11) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募人才变局·诺安总经理齐斌离任·年内85家高管变动·基金经理去明星化提速</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>高管变动大年：</b>诺安基金公告总经理齐斌因个人原因离任、原副总刘翔升任，齐斌任职6年带领公司公募规模翻倍；截至7月10日年内已有<b>85家</b>公募机构发生高管变动、涉及193人次（20家换董事长、26家换总经理）。<br>
          <b>去明星化：</b>Wind显示，截至7月10日年内基金经理离任<b>232人次</b>、同比+22.11%，变动产品达3058只；基金公司通过增聘、共管平滑交接，从"个人能力驱动"转向"平台能力支撑"。<br>
          <b>对基金行业影响：</b>人才更替加速→腾安选品应更重投研平台稳定性与团队共管机制，弱化单一明星依赖。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1HVPTUH05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <a href="https://www.eeo.com.cn/2026/0711/952404.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济观察报</span></a>
          <span class="impact-tag medium">人才变局：中</span>
        </div>
      </div>

      <!-- S0 Card 4: 周五A股重挫·科创50暴跌5.53%·半导体一日游·科技主题基金净值波动 (T-1 07-10) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 周五A股重挫·沪指跌1%失守4000点·科创50暴跌5.53%·科技主题基金净值波动加剧</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>放量下跌：</b>7月10日A股集体收跌，沪指<b>-1.00%</b>（3996.16失守4000点）、深成指<b>-2.29%</b>、创业板指<b>-4.37%</b>、科创50<b>-5.53%</b>，全市场成交<b>34107亿</b>放量；超3700只个股上涨、权重砸盘、小票活跃。<br>
          <b>板块分化：</b>创新药/白酒/影视/商业航天逆势，半导体上演"一日游"（7/9 +6.52%→7/10 -5.28%）；商业航天受长征十号乙海上回收催化午后爆发。<br>
          <b>对基金行业影响：</b>科技主题基金短期净值回撤→腾安需提示高位波动、引导哑铃配置与低位补仓节奏。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260711/c678110923.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经早餐</span></a>
          <a href="https://xueqiu.com/1879823455/399609728" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">雪球</span></a>
          <span class="impact-tag high">组合波动：高</span>
        </div>
      </div>

    </div>
  </div>"""))

# 5) S1: remove 2 expired cards (06-26, 06-25) and add 2 new cards
REPLS.append(("s1expired",
"""      <!-- S1 Card 1: 第二批公募基准调整全面铺开 (06-26) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 第二批公募业绩比较基准调整全面铺开·千余只产品·从试点走向系统推进</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>全面铺开：</b>6月26日，超90家基金管理人发布旗下部分存量产品业绩比较基准调整公告，涉及千余只产品，覆盖范围更广、产品数量更多、参与主体更加多元。<br>
          <b>调整逻辑：</b>按照"优先调整基准而非调整持仓"原则，管理人调整基准无需调仓，不会对市场运行造成冲击。基准调整的核心逻辑是让业绩比较基准更加贴近实际资产配置和投资风格。<br>
          <b>对基金行业影响：</b>基准改革全面铺开→产品定位更清晰→投资者选择基金更有依据→腾安可在营销中突出基准说明。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L0F7H3A405346RC6_pdya11y.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华社·中国证券报</span></a>
          <a href="https://www.toutiao.com/article/7655830765002867246" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">头条·证券时报</span></a>
          <span class="impact-tag medium">基准改革：极高</span>
        </div>
      </div>

      <!-- S1 Card 6: 证监会支持中小基金公司差异化发展 (06-25报道) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 证监会支持中小基金公司差异化发展·分类监管破局"规模竞赛"</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-25报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>政策方向：</b>2026年6月，证监会主席吴清在陆家嘴论坛表示，"推出支持中小基金公司规范健康发展一揽子措施，坚持分类监管、突出特色，在产品布局、业务准入等方面给予适当倾斜，积极支持中小基金公司差异化发展"。<br>
          <b>行业影响：</b>中小基金公司有望从"规模竞赛"转向"特色生存"，行业格局从"赢者通吃"向"多元共生"演变。<br>
          <b>对基金行业影响：</b>分类监管→中小基金公司差异化发展→腾安可关注特色化中小基金公司产品供给。
        </div>
        <div class="card-footer">
          <a href="https://finance.china.com.cn/money/fund/20260625/6313510.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag low">分类监管：低</span>
        </div>
      </div>""",
"""      <!-- S1 Card NEW: 上半年发行分析·科技赛道引领·股强债弱 (07-08) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 上半年发行分析·科技赛道引领·"股强债弱"·FOF成最大黑马</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-08</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行扩容：</b>Wind数据显示，2026年上半年全市场新发公募基金<b>883只</b>、总规模<b>6369.93亿元</b>，同比增20.11%；股票型+混合型基金新发3781.82亿元、同比大增57.31%占近六成，债基发行占比从46.73%降至19.98%，呈现明显"股强债弱"。<br>
          <b>结构亮点：</b>FOF成最大黑马，上半年新发95只、募资1177.42亿元，同比+259.5%；6月新成立208只、募资1205.02亿双创年内月度新高。业内提示权益发行占比过高、若科技回调或现赎回压力。<br>
          <b>对基金行业影响：</b>科技赛道虹吸效应放大收益鸿沟→腾安推荐需平衡景气与拥挤，强化组合配置话术。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260708094032979b65c3" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯证券·券商中国</span></a>
          <span class="impact-tag medium">发行结构：高</span>
        </div>
      </div>

      <!-- S1 Card NEW: 央行万亿投放+利率下行·居民资金向权益ETF分流 (07-11) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 央行万亿中长期资金投放+存款利率下行·居民闲钱向权益/ETF分流</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>流动性宽松：</b>央行7月初完成万亿级中长期资金投放，对冲缴税与解禁压力；银行存款利率持续下行、五年期大额存单重启，稳健理财收益走低。<br>
          <b>资金迁徙：</b>在"资产荒+低利率"环境下，居民闲钱持续向权益市场与ETF分流，为公募权益产品与指数化配置提供增量资金来源。<br>
          <b>对基金行业影响：</b>增量资金入场→腾安可顺势加大权益/ETF货架与投教，承接居民资产再配置需求。
        </div>
        <div class="card-footer">
          <a href="https://caifuhao.eastmoney.com/news/20260711073255117872680" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <span class="impact-tag low">资金面：中</span>
        </div>
      </div>"""))

# 6) S2: remove 2 expired 06-26 P0 cards, add 1 new 07-11 card
REPLS.append(("s2expired",
"""      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会五方面推动资本市场法治协同建设·推动修改证券投资基金法</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>法治协同规划：</b>中国证监会近日对推进资本市场法治协同建设作出规划，包括：配合做好金融法制定，<b>推动修改证券投资基金法</b>；严厉打击系统性财务造假、第三方配合造假和中介机构失职失守违法犯罪行为；探索研究将行政执法查封、冻结的证券期货违法涉案财产用于投资者民事诉讼赔偿。<br>
          <b>立法计划：</b>推动修订《证券公司监督管理条例》《证券、期货投资咨询管理暂行办法》，<b>制定上市公司监督管理条例</b>。完善域外适用规定和反长臂管辖、反制裁规定。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260626A02KQL00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·四大证券报</span></a>
          <span class="impact-tag high">法治升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跟踪证券投资基金法修改立法进展，评估对腾安业务影响；<br>
            ② 关注"行刑民"立体追责机制完善，加强内部合规管理。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产等罚款近6000万·私募基金"零容忍"监管再升级</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>处罚内容：</b>证监会对深圳前海玖瀛资产管理有限公司、深圳市前海腾创投资有限公司及相关责任人员利用私募基金向关联主体输送利益、报送虚假信息等违法违规行为作出行政处罚，合计罚款近<b>6000万元</b>，创"史上最重"罚单。<br>
          <b>配套措施：</b>同步对实际控制人采取<b>5年证券市场禁入</b>及<b>5年证券市场禁止交易</b>措施。惩治效果显著提高，体现证监会对私募基金严重违法违规行为"零容忍"的监管态度。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260626223459a6b8a584" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·证券时报</span></a>
          <span class="impact-tag high">私募严监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 关注私募监管升级态势，审查腾安代销的私募产品合规性；<br>
            ② 将"零容忍"监管信号纳入内部合规培训。
          </div>
        </div>
      </div>""",
"""      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 证监局密集开展基金销售合规摸底·核查认购费/销售服务费调降·整治预期收益宣传</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>合规整治：</b>监管层近期密集开展证券市场与基金销售领域合规整治。深圳证监局已对编造传播涉及上市公司虚假误导性信息立案调查；同时已有证监局对基金销售机构开展合规摸底，重点核查公募基金认购费、销售服务费率调降推进情况，及是否存在宣传预期收益率、承诺保本保收益等违规情形。<br>
          <b>考核导向：</b>监管推动机构将基金销售保有规模、投资人长期投资收益纳入考核体系，引导从"重销量"转向"重保有、重长期"。<br>
          <b>对基金行业影响：</b>基金销售合规收紧→作为持牌代销平台，腾安合规优势凸显，应强化销售合规与长期保有考核。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260711/c678110923.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经早餐</span></a>
          <span class="impact-tag medium">销售合规：高</span>
        </div>
      </div>"""))

# 7) S6 whole card (休市, 07-10收盘)
REPLS.append(("s6",
"""      <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月10日（周五）·A股开盘涨跌不一·盘中翻红·CPO/半导体领涨·贵金属反弹</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-10（开盘涨跌不一·盘中震荡走高翻红）：</b><br>
              ▪ 沪指 开盘<b>-0.13%</b>（4031.54）→盘中<b>+0.42%</b>（4053.64）<br>
              ▪ 深成指 <b>+0.53%</b>（15480.41）<br>
              ▪ 创业板指 开盘<b>+0.59%</b>→盘中<b>+0.97%</b>（4057.03）<br>
              ▪ 沪深300 <b>+0.23%</b>·科创50 盘中<b>+1.93%</b>（2228.11）<br>
              ▪ 板块：CPO/苹果产业链/6G/光芯片/内存/玻璃纤维/贵金属走强；油气·教育·煤炭·能源金属·石油石化走弱
            </div>
            <div>
              <b>📊 港股/美股：</b><br>
              ▪ 美股（07-09收盘·隔夜）：道指 <b>+0.27%</b>（52487.41）·标普 <b>+0.81%</b>（7543.64）·纳指 <b>+1.30%</b>（26206.89，收复26000点·存储/芯片领跑）<br>
              ▪ 港股07-09收盘：恒指 <b>-0.70%</b>（24030.18）·恒生科技 <b>+0.01%</b>（4731.56）；07-10开盘恒指回升约24245<br>
              ▪ WTI原油 71.74美元 <b>-0.49%</b>（特朗普对伊表态·油价回落）·现货黄金 4123.69美元<br><br>
              <b>📌 今日焦点：</b>① AI赛道ETF大举吸金，科创50ETF成净流入最多宽基、半导体设备ETF破500亿；② A股盘中三大指数翻红，CPO/半导体产业链领涨；③ 美股连续反弹、纳指收复26000点，科技情绪回暖。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-10 09:55</span>
            <span class="source-tag">数据来源：07-10 开盘/盘中·财联社/中新经纬/澎湃/新华财经</span>
          </div>
      </div>""",
"""      <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月11日（周六）·A股/港股休市·最新收盘为7月10日（周五）·沪指跌1.00%失守4000点·科创50暴跌5.53%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-10收盘（休市·展示最近收盘）：</b><br>
              ▪ 沪指 <b>-1.00%</b>（3996.16，失守4000点）·深成指 <b>-2.29%</b><br>
              ▪ 创业板指 <b>-4.37%</b>·科创50 <b>-5.53%</b>·成交 <b>34107亿</b>放量<br>
              ▪ 板块：创新药/影视/白酒/猪肉/房地产/商业航天/零售涨；半导体(-5.28%)/元件/能源金属/先进封装/氟化工/CPO/PCB跌<br>
              ▪ 半导体"一日游"：7/9 +6.52%→7/10 -5.28%，资金高低切换
            </div>
            <div>
              <b>📊 港股/美股（隔夜）：</b><br>
              ▪ 港股07-10收盘：恒指 <b>+0.6%</b>（24030附近）·恒生科技 <b>-0.21%</b><br>
              ▪ 美股07-10收盘：道指 <b>+0.29%</b>·纳指 <b>+0.29%</b>·标普 <b>+0.42%</b>；英伟达+3.5%重回5万亿、Meta+6%、SK海力士+13%<br>
              ▪ 本周复盘：4000点反复拉锯、创业板暴跌4.37%、商业航天爆发、成交维持3万亿+<br><br>
              <b>📌 周末要闻：</b>① 国常会定调数字中国·算力网络提速；② 两部门氦气出口管制(7/10盘后)；③ 《中医药振兴"十五五"规划》批复；④ 证监局基金销售合规摸底。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-11（周六休市·07-10收盘）</span>
            <span class="source-tag">数据来源：同花顺财经早餐/雪球/东方财富·07-10收盘</span>
          </div>
      </div>"""))

# 8) S7 remove 06-26 entry (expired T-15)
REPLS.append(("s7remove",
"""      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-26（A股黑色星期五·半年度收官大跌·沪指-2.26%创业板-4.07%）</div>
          <div class="timeline-title">A股半年度收官集体重挫 / 上证-2.26%·深成指-3.44%·创业板-4.07% / 亚太股市同步走弱</div>
          <div class="timeline-desc">6月26日A股半年度收官，三大指数集体重挫，创业板指暴跌4.07%领跌主要指数。全市场超4600只个股下跌，成交额3.55万亿元。下跌受四重压力叠加：机构半年业绩结算+风格漂移严查→集中调仓；海外科技股大跌+韩国熔断→风险偏好传导；AI产业链价格传导不畅→盈利前景担忧。</div>
        </div>
      </div>""",
""))

# 9) S7 add 07-11 entry at top (before 07-10)
REPLS.append(("s7add",
"""    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
      <!-- 07-10 时间线条目 (NEW) -->""",
"""    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
      <!-- 07-11 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-07-11（二季报含科量成业绩密码·公募人才变局·7月新发121只·周五科创50暴跌5.53%）</div>
          <div class="timeline-title">公募二季报披露拉开帷幕·10只主动权益8只Q2净值增长超70% / 年内85家公募高管变动·基金经理去明星化 / 7月121只新基发行小高峰 / 周五A股重挫·科创50-5.53%</div>
          <div class="timeline-desc">7月11日，公募基金二季报披露拉开帷幕，截至7月10日13只基金披露二季报，10只主动权益中8只Q2净值增长率超70%，同泰数字经济A +101.98%、红土创新多只+90%以上，AI算力链持仓成业绩密码。同日，诺安基金总经理齐斌离任、年内至少85家公募高管变动，基金经理离任232人次、去明星化加速；7月121只新基金启动认购、指数化与固收+双主线。回顾前一交易日（7/10）A股重挫，沪指-1.00%失守4000点、创业板-4.37%、科创50-5.53%，半导体"一日游"后暴跌，商业航天/创新药逆势。</div>
        </div>
      </div>

      <!-- 07-10 时间线条目 (NEW) -->"""))

# 10) S8 add 07-11 card at top of card-grid
REPLS.append(("s8add",
"""    <div class="card-grid">

      <!-- S8 Card NEW: AI赛道ETF吸金·科技主题基金过热 (07-10) -->""",
"""    <div class="card-grid">

      <!-- S8 Card NEW: 二季报披露季开启·含科量成业绩密码 (07-11) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露季开启·含科量成业绩密码·腾安需准备科技持仓解读与净值波动应对</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>截至7月10日13只基金披露二季报，10只主动权益中8只Q2净值增长超70%，同泰数字经济A +101.98%、红土创新多只+90%以上，AI算力链持仓成业绩分水岭。<br>
          <b>腾安行动建议：</b>① 借二季报强化科技赛道基金持营与持仓解读话术；② 提示单一赛道拥挤与高位波动风险、引导哑铃配置；③ 关注重仓科技基金净值波动与客户安抚。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 准备科技持仓解读话术→投顾部<br>
            ② 提示拥挤交易风险→营销部<br>
            ③ 关注重仓科技基金净值波动→客服部
          </div>
        </div>
      </div>

      <!-- S8 Card NEW: AI赛道ETF吸金·科技主题基金过热 (07-10) -->"""))

# 11) S8 remove one-time stale cards (≤06-30)
REPLS.append(("s8_rm_a",
"""      <!-- S8 Card 0: 基金中考收官 (NEW) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 基金中考今日收官·126只翻倍基·下半年资金流向重构</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-30</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>6月30日，2026年上半年公募基金"中考"正式收官。126只翻倍基业绩锁定，最高收益175%（财通多策略福鑫定开）。中考业绩将影响下半年资金流向和投资者偏好。<br>
          <b>腾安行动建议：</b>① 梳理上半年绩优基金经理名单，准备营销素材；② 翻倍基集中限购→准备替代产品清单；③ 业绩分化210pct→加强投资者教育。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理绩优基金经理名单→营销部<br>
            ② 准备替代产品清单→产品部<br>
            ③ 加强投资者教育→投顾部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_b",
"""      <!-- S8 Card 1: A股06-30涨跌不一 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 A股06-30涨跌不一·创业板+1%·科技板块活跃·收盘后净值解读</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-30</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>6月30日A股涨跌不一，创业板指涨逾1%，科创AI板块活跃。中考收官日市场情绪复杂，科技类基金净值继续分化。<br>
          <b>腾安行动建议：</b>① 准备收盘后基金净值解读话术；② 关注翻倍基净值变化；③ 科技类基金客户关怀。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 准备净值解读话术→营销部<br>
            ② 关注翻倍基净值→产品部<br>
            ③ 科技类基金客户关怀→客服部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_c",
"""      <!-- S8 Card 2: FOF单周发行环比+175% -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 FOF单周发行环比+175%·配置需求爆发·腾安加大FOF推荐权重</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-29</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>本周47只新基金启动募集，FOF赛道11只新品环比+175%。年内新发FOF破100只，总募资刷新历史纪录。<br>
          <b>腾安行动建议：</b>① 加大FOF产品推荐权重；② 研究FOF作为理财替代工具的卖点；③ 关注银行渠道FOF推广策略。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 加大FOF推荐权重→投顾部<br>
            ② 研究FOF卖点→营销部<br>
            ③ 关注银行渠道策略→产品部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_d",
"""      <!-- S8 Card: A股半年度收官大跌 (06-27) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 A股半年度收官大跌·创业板-4.07%·科技基金回调·赎回风险应对</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>6月27日A股半年度收官大跌，创业板指暴跌4.07%，科技类基金单日大幅回撤，预计客户咨询和赎回申请激增。<br>
          <b>腾安行动建议：</b>① 准备A股大跌解读话术和客户沟通模板；② 科技类基金回调后低位布局建议；③ 关注客户赎回风险，提前准备流动性应对方案。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 准备大跌解读话术→营销部<br>
            ② 低位布局建议方案→投资顾问<br>
            ③ 关注赎回风险→风控部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_e",
"""      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 浮费基金业绩分化·三倍基诞生·费率机制正式生效</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>首批浮费基金一周年，华商致远回报A成"三倍基"（316.56%），6只产品仍亏损（最高-12.84%）。运作满一年后费率按业绩分档正式生效。<br>
          <b>腾安行动建议：</b>① 评估腾安代销的浮费基金业绩表现，准备客户沟通话术；② 在基金详情页突出费率机制说明，避免销售误导；③ 关注浮动费率基金作为差异化产品卖点的营销机会。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理腾安代销浮费基金清单及业绩表现→产品部<br>
            ② 制作浮费基金费率机制说明话术→营销部<br>
            ③ 评估浮费基金作为差异化卖点的营销方案→运营部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_f",
"""      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>QDII限购力度再加码，易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>。超百只QDII限购百元及以下。近一年QDII平均收益22%，45只净值翻倍。<br>
          <b>腾安行动建议：</b>① 梳理腾安可代销的有额度QDII产品清单；② 准备QDII替代方案话术（港股通、互认基金、跨境ETF等）；③ 关注新一批QDII额度发放进展，提前布局。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理有额度的QDII产品清单→产品部<br>
            ② 制作QDII替代方案话术→营销部<br>
            ③ 跟踪新一批QDII额度发放进展→产品部
          </div>
        </div>
      </div>""",
""))

# 11b) S8 remove leftover 06-26 (T-15, expired) P0 action cards
REPLS.append(("s8_rm_g",
"""      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 第二批公募基准调整全面铺开·腾安需准备基准说明话术</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>第二批千余只公募基金产品业绩比较基准调整全面铺开，多数产品自7月27日起正式生效。基准校准让产品从"模糊标签"走向"清晰画像"。<br>
          <b>腾安行动建议：</b>① 在基金详情页突出业绩比较基准说明；② 准备基准调整相关的客户沟通话术；③ 梳理腾安代销产品中哪些参与了第二批基准调整。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理代销产品基准调整清单→产品部<br>
            ② 制作基准说明话术→营销部<br>
            ③ 更新基金详情页基准展示→技术部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_h",
"""      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产罚款近6000万·私募严监管升级</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>证监会对玖瀛资产等罚款近6000万元，创"史上最重"私募处罚纪录。同步对实际控制人采取5年证券市场禁入及禁止交易措施。<br>
          <b>腾安行动建议：</b>① 审查腾安代销的私募产品合规性；② 将"零容忍"监管信号纳入内部合规培训；③ 关注私募监管升级对行业的影响。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 审查代销私募产品合规性→合规部<br>
            ② 更新合规培训材料→法务部<br>
            ③ 关注后续私募监管政策→产品部
          </div>
        </div>
      </div>""",
""))

REPLS.append(("s8_rm_i",
"""      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会推动修改证券投资基金法·五方面法治协同建设</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>证监会近日公布五方面资本市场法治协同建设规划，包括推动修改<b>证券投资基金法</b>、制定上市公司监督管理条例、完善域外适用规定等。<br>
          <b>腾安行动建议：</b>① 跟踪证券投资基金法修改立法进展，评估对腾安业务影响；② 关注"行刑民"立体追责机制完善，加强内部合规管理；③ 提前研究基金法修改对代销模式的影响。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 跟踪基金法修改立法进展→法务部<br>
            ② 评估对腾安代销业务影响→产品部<br>
            ③ 加强内部合规管理→风控部
          </div>
        </div>
      </div>""",
""))

# ---- Apply with assertions (two-phase: assert all first, then write) ----
errors = []
for name, old, new in REPLS:
    cnt = html.count(old)
    if cnt != 1:
        errors.append("%s: expected 1 occurrence, found %d" % (name, cnt))

if errors:
    print("PRECHECK FAILED:")
    for e in errors:
        print("  -", e)
    raise SystemExit(1)

# All anchors present exactly once -> apply
for name, old, new in REPLS:
    html = html.replace(old, new, 1)

# ---- Quality checks ----
opens = html.count("<div")
closes = html.count("</div>")
assert opens == closes, "div imbalance: %d opens vs %d closes" % (opens, closes)
assert "daily-update: 2026-07-11" in html
assert "2026.06.27 — 2026.07.11" in html
# cross-module dedup sanity
assert html.count("公募二季报披露拉开帷幕") >= 1
assert "含科量成业绩密码·10只主动权益" in html  # S0 present
assert "证监局密集开展基金销售合规摸底" in html  # S2 new present
# ensure expired 06-25/06-26 entries gone from S1/S2
assert "第二批公募业绩比较基准调整全面铺开·千余只产品" not in html
assert "证监会支持中小基金公司差异化发展·分类监管" not in html
assert "证监会五方面推动资本市场法治协同建设" not in html
assert "证监会对玖瀛资产等罚款近6000万" not in html

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("OK: applied %d replacements; div balance %d=%d" % (len(REPLS), opens, closes))
