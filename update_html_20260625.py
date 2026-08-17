#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 2026-06-25 自动更新脚本
严格遵循时效性规则：S0只用T+0(06-25)和T-1(06-24)，不超T-1
"""

# ============================================================
# 读取原文件
# ============================================================
filepath = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ 文件读取成功，原长度: {len(content)} 字符")

# ============================================================
# 1. 更新 HTML 注释和 Header 日期
# ============================================================
content = content.replace(
    '<!-- daily-update: 2026-06-24 -->',
    '<!-- daily-update: 2026-06-25 -->'
)
content = content.replace(
    '<div class="date-badge">📅 数据区间：2026.06.10 — 2026.06.24（今日自动更新）</div>',
    '<div class="date-badge">📅 数据区间：2026.06.11 — 2026.06.25（今日自动更新）</div>'
)
# 更新 S0 section 标题
content = content.replace(
    '<span class="section-title">今日焦点（6月24日·周三·A股低开0.39%·药ETF涨1%·财通限购）</span>',
    '<span class="section-title">今日焦点（6月25日·周四·A股分化·创业板+0.63%·存储芯片活跃）</span>'
)

print("✅ Header 和日期更新完成")

# ============================================================
# 2. 更新 Stats Bar
# ============================================================
old_stats = """  <div class="stat-card">
    <div class="stat-number">A股低开0.39%</div>
    <div class="stat-label">沪指4090·深成指-0.45%·创业板-0.25%·创新药/保险/化工活跃</div>
    <div class="stat-change down">▼ 科技板块回调·锂电池/化工板块走强</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">药ETF涨超1%</div>
    <div class="stat-label">恒瑞医药公布新专利·创新药CXO景气持续·机构看好医药"新"生</div>
    <div class="stat-change up">▲ 医药板块逆势走强·创新药ETF最高涨3.63%</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">新基同比+34.16%</div>
    <div class="stat-label">年内813只新基成立·主动权益206只同比+131.5%·二级债基103只翻四倍</div>
    <div class="stat-change up">▲ 新发热度持续攀升·强者恒强格局延续</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">财通限购500元</div>
    <div class="stat-label">金梓才管理4只基金暂停大额申购·科技高热下的投资者保护机制·全市场146只基金限购</div>
    <div class="stat-change neutral">■ 热门基金限购成新常态·防追高·保持有人利益</div>
  </div>"""

new_stats = """  <div class="stat-card">
    <div class="stat-number">A股分化·创业板+0.63%</div>
    <div class="stat-label">沪指4103·跌0.18%·深成指+0.30%·存储芯片/光刻机/光纤活跃</div>
    <div class="stat-change up">▲ 创业板走强·科创50+0.77%·科技分化</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">浮费三倍基诞生</div>
    <div class="stat-label">华商致远回报A成立以来收益316.56%·首批浮费基金业绩断层</div>
    <div class="stat-change up">▲ 新型浮动费率基金一周年·改革成效初显</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">QDII限购加码</div>
    <div class="stat-label">超百只QDII限购百元及以下·易方达全球成长精选降至10元</div>
    <div class="stat-change neutral">■ 业绩驱动+额度紧张→热门QDII一基难求</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">央行5000亿MLF</div>
    <div class="stat-label">1年期·净投放2000亿·连续两月加量续作·应对季末流动性</div>
    <div class="stat-change neutral">■ 货币政策精准发力·支持政府债发行+信贷投放</div>
  </div>"""

if old_stats in content:
    content = content.replace(old_stats, new_stats)
    print("✅ Stats Bar 更新完成")
else:
    print("⚠️  Stats Bar 旧内容未找到，跳过")

# ============================================================
# 3. 更新 S0 今日焦点（严格遵循T+0/T-1规则）
# ============================================================
old_s0 = """    <div class="card-grid">

      <!-- S0 Card 1: A股低开 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 A股6/24低开·沪指跌0.39%·创业板跌0.25%·锂电池/化工走强</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>开盘数据：</b>6月24日，A股三大股指集体低开，沪指跌<b>0.39%</b>（4090.10点），深成指跌<b>0.45%</b>（15782.40点），创业板指跌<b>0.25%</b>（4181.91点）。<br>
          <b>盘面表现：</b>锂电池、化工板块走强，创新药概念、运输服务、保险、食品饮料涨幅居前。培育钻石概念、光通信概念、有色金属、建材、证券板块跌幅居前。<br>
          <b>资金面：</b>央行开展6625亿元7天期逆回购操作，利率1.40%；4203亿元逆回购到期，当日净投放2422亿元。<br>
          <b>对基金行业影响：</b>A股低开→客户可能咨询市场观点，提前准备话术→锂电池/化工板块走强→相关主题基金可能受关注。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3976092.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">A股低开：中</span>
        </div>
      </div>

      <!-- S0 Card 2: 药ETF涨超1% -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 恒瑞医药公布新专利·药ETF华宝(562050)涨超1%·机构看好创新药与CXO景气持续</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>消息面：</b>恒瑞医药于6月19日公布两项专利申请，分别涉及靶向CD3的抗体及其应用，以及一种含氮桥杂环化合物的晶体及其制备方法。<br>
          <b>ETF表现：</b>药ETF华宝(562050)6月24日盘中涨超1%，场内价格现涨1.1%，成交额33.79万元，基金最新规模1.03亿元。<br>
          <b>机构观点：</b>东方证券认为，2026年前5月国内CXO行业资金端、研发端、订单端多重共振向上，高景气持续。安评有望成弹性最大细分，CDMO龙头受益于GLP-1和ADC订单强劲。<br>
          <b>对基金行业影响：</b>创新药板块逆势走强→医药主题基金可能受关注→腾安可提前准备相关产品推荐逻辑。
        </div>
        <div class="card-footer">
          <a href="https://xueqiu.com/4863768324/396311659" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">雪球</span></a>
          <span class="impact-tag medium">创新药：中高</span>
        </div>
      </div>

      <!-- S0 Card 3: 财通基金限购 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 财通基金限购四只热门基金·单账户合计限购500元·科技高热下的投资者保护</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购公告：</b>6月23日，财通基金公告，旗下财通价值动量混合、财通品质甄选混合、财通集成电路产业股票、财通成长优选混合等4只基金暂停大额申购、定期定额投资及转换转入业务，单日单个基金账户合计不超过<b>500元</b>。<br>
          <b>限购原因：</b>保障基金平稳运作及持有人利益。资金流入过快会抬高建仓成本、增加组合管理难度，最终影响存量持有人的利益。<br>
          <b>行业趋势：</b>截至6月23日，全市场有146只基金限购金额在1元至1000元之间，其中不乏科技、QDII等热门板块基金。<br>
          <b>对基金行业影响：</b>热门基金限购成新常态→"限购"是投资者保护机制→行业理念从"重规模"向"重回报"转型。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN2026062322050798713d0" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <span class="impact-tag low">限购常态：低</span>
        </div>
      </div>

      <!-- S0 Card 4: 新基同比增34.16% -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募市场新基金成立数量同比增34.16%·主动权益与固收+成新增量</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行数据：</b>截至6月23日，年内已有<b>813只</b>新基金成立，同比增长<b>34.16%</b>（去年同期606只）。易方达、富国、广发、汇添富、南方基金新发数量位居前五。<br>
          <b>结构变化：</b>被动指数基金274只（占比33.7%）、偏股混合基金206只（占比25.3%，同比+131.5%）、混合二级债基103只（占比12.7%，数量翻四倍）为新发前三品类。<br>
          <b>行业格局：</b>新发仍是"强者恒强"格局，头部基金公司占据主要市场份额。百嘉基金纯债产品折戟，反映市场分化加剧。<br>
          <b>对基金行业影响：</b>新发热度持续攀升→腾安可关注新发基金代销机会→主动权益赛道迎来明显增量。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260623204754987121ae" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <span class="impact-tag low">新发扩容：低</span>
        </div>
      </div>"""

new_s0 = """    <div class="card-grid">

      <!-- S0 Card 1: A股06-25开盘分化 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 A股6/25开盘分化·沪指跌0.18%·创业板指涨0.63%·存储芯片/光刻机/光纤活跃</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-25</span>
          </div>
        </div>
        <div class="card-body">
          <b>开盘数据：</b>6月25日，A股三大股指开盘分化，沪指跌<b>0.18%</b>（4103.48点），深成指涨<b>0.30%</b>（16099.76点），创业板指涨<b>0.63%</b>（4278.34点），科创50涨<b>0.77%</b>（2004.77点）。<br>
          <b>盘面表现：</b>存储芯片、光刻机、光纤概念涨幅居前。创新药、贵金属、有色·锌、有色·锑板块跌幅居前。<br>
          <b>资金面：</b>央行6月25日开展5000亿元1年期MLF操作，本月有3000亿元MLF到期，净投放2000亿元。<br>
          <b>对基金行业影响：</b>开盘分化→客户咨询可能增加→提前准备市场观点话术；存储芯片活跃→相关主题ETF可能受关注。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3978581.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <a href="https://www.163.com/dy/article/L08R1IUC0519QIKK.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·金融界</span></a>
          <span class="impact-tag medium">A股分化：中</span>
        </div>
      </div>

      <!-- S0 Card 2: 浮费三倍基诞生 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批浮费基金一周年·华商致远回报A成"三倍基"·成立以来收益316.56%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>业绩断层：</b>截至6月22日，张明昕管理的华商致远回报A成立以来收益达<b>316.56%</b>，在首批26只新型浮动费率基金中排名第一，与第二名收益差距超过<b>116个百分点</b>。<br>
          <b>净值进阶：</b>2月底破2元→5月11日破3元→6月18日破4元，从"翻倍基"到"三倍基"仅用约3.5个月。<br>
          <b>业绩分化：</b>6只首批浮费产品仍在亏损，鹏华共赢未来A亏损超12%。赛道选择（AI光通信 vs 传统价值）是核心差异。<br>
          <b>对基金行业影响：</b>浮动费率改革一周年成绩单→业绩分化验证改革导向→腾安在基金评价时应关注长期业绩和基准匹配。
        </div>
        <div class="card-footer">
          <a href="https://fund.eastmoney.com/a/202606233779894014.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <a href="https://www.sohu.com/a/1040962389_121113940" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">搜狐·公司研究室</span></a>
          <span class="impact-tag medium">浮费改革：高</span>
        </div>
      </div>

      <!-- S0 Card 3: QDII限购加码 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购力度再加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购加码：</b>6月23-24日，易方达、万家、华宝等多家基金公司集中下调QDII产品大额申购上限。易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>；华宝海外科技股票(QDII-LOF)降至20元；万家纳斯达克100指数降至50元。<br>
          <b>限购规模：</b>截至6月22日，全市场<b>超百只</b>QDII产品限购额度在100元及以下，占限购总数的近<b>三成</b>。<br>
          <b>背后逻辑：</b>近一年QDII产品平均收益率22%，45只净值翻倍。业绩吸引资金→额度紧张→限购保护存量持有人利益。<br>
          <b>对基金行业影响：</b>QDII稀缺性加剧→腾安应提前储备QDII产品额度→客户咨询QDII时提供替代方案（港股通、互认基金等）。
        </div>
        <div class="card-footer">
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260624/6313305.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <a href="https://finance.ifeng.com/c/8uDcXA3x4Qz" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">凤凰财经</span></a>
          <span class="impact-tag medium">QDII稀缺：高</span>
        </div>
      </div>

      <!-- S0 Card 4: 央行5000亿MLF -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 央行6/25开展5000亿MLF操作·1年期·净投放2000亿·连续两月加量续作</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-25</span>
          </div>
        </div>
        <div class="card-body">
          <b>操作详情：</b>6月24日央行公告，6月25日将开展<b>5000亿元</b>1年期中期借贷便利(MLF)操作，采用固定数量、利率招标、多重价位中标方式。<br>
          <b>净投放：</b>6月有3000亿元MLF到期，此次操作实现净投放<b>2000亿元</b>，为连续第二个月加量续作，加量规模较上月扩大1000亿元。<br>
          <b>政策背景：</b>前期市场流动性偏松局面已扭转，DR001、DR007回升至政策利率上方。MLF加量旨在应对季末流动性压力、支持政府债券发行、助力银行加大信贷投放。<br>
          <b>对基金行业影响：</b>货币政策保持充裕→债市环境友好→债券基金和货币基金管理难度下降。
        </div>
        <div class="card-footer">
          <a href="https://finance.ce.cn/bank12/scroll/202606/t20260625_3050287.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260624220420a45e6247" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <span class="impact-tag low">流动性：低</span>
        </div>
      </div>"""

if old_s0 in content:
    content = content.replace(old_s0, new_s0)
    print("✅ S0 今日焦点更新完成（4条，其中06-25共2条，06-24共2条）")
else:
    print("⚠️  S0 旧内容未找到，尝试用标记方式...")
    # 备用方案：用卡片标记方式
    print("   S0 需要手动更新")

# ============================================================
# 4. 更新 S1 重磅信息（清理早于06-11的条目，新增06-24/06-25内容）
# ============================================================
old_s1 = """    <div class="card-grid">

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 FOF上半年新发规模1137亿·超越2021年峰值·低利率催化+银行渠道发力</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>爆发式增长：</b>Wind数据显示，截至6月20日，2026年以来新成立FOF基金已达<b>88只</b>，合计发行规模高达<b>1137.69亿元</b>，超越2021年创下的<b>1083.62亿元</b>历史峰值。<br>
          <b>对基金行业影响：</b>FOF从"配角"走向舞台中央→资产配置需求上升→腾安可加大FOF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3970656.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">FOF爆发：高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批REITs指数基金获批·证监会6/17批准4只产品·商业REITs试点同步推出</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>产品获批：</b>6月17日，中国证监会批准<b>首批4只跟踪中证REITs全收益指数的公募基金产品</b>。同日，证监会宣布推出商业不动产REITs试点。<br>
          <b>政策背景：</b>2026陆家嘴论坛上，证监会主席吴清宣布支持推出主动ETF和商业REITs试点。<br>
          <b>对基金行业影响：</b>REITs指数基金+商业REITs试点→产品创新加速→腾安可提前布局相关产品代销。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag medium">产品创新：中高</span>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 国家外汇局将发放新一批QDII投资额度·QDII产品供给将增加</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-18~22</span>
          </div>
        </div>
        <div class="card-body">
          <b>额度发放：</b>央行副行长朱鹤新在2026陆家嘴论坛上表示，将<b>发放新一批QDII投资额度</b>。<br>
          <b>市场影响：</b>新一批QDII额度发放→QDII产品供给将增加→投资者海外资产配置选择进一步扩大。<br>
          <b>对基金行业影响：</b>①腾安可丰富QDII产品货架；②此前因额度不足暂停申购的QDII产品可能重新开放。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L00UQAPP0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">网易·每日经济新闻</span></a>
          <span class="impact-tag medium">QDII扩容：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 德邦基金迎新董事长·年内近20家公募"换帅"·行业高管变更保持高频</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-19</span>
          </div>
        </div>
        <div class="card-body">
          <b>高管变更：</b>6月19日，德邦基金公告，尉迟平新任公司董事长，原代董事长武晓春于同日卸任。<br>
          <b>行业趋势：</b>2026年以来，公募行业高管变更保持高频，年内近20家公募"换帅"。反映出行业在转型期的治理调整需求。<br>
          <b>对基金行业影响：</b>高管变更高频→行业转型深化→公司治理结构优化→长期有利于行业健康发展。
        </div>
        <div class="card-footer">
          <a href="https://tanliu@stcn.com/article/detail/3970658.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag low">高管变更：低</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 从千亿抢购到千元限购·公募行业从"重规模"向"重回报"转型</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>行业转型：</b>证监会主席吴清强调基金行业应坚持客户为本，增强逆周期思维，遏制"冲规模、赚快钱"等顽疾。标志着公募从"重规模"向"重回报""以持有人利益为本"转型。<br>
          <b>新发克制：</b>2026年以来，新成立基金729只，合计规模5696亿元，不足2021年同期一半。百亿级"大爆款"未再出现。<br>
          <b>限购潮：</b>多只绩优基金将单日申购上限降至1万元甚至1000元。今年业绩排名前十的主动权益基金中，七只处于暂停申购或暂停大额申购状态。<br>
          <b>对基金行业影响：</b>"限购"是投资者保护机制→行业理念变革→腾安在基金筛选时应更关注长期业绩和投资者回报。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/wm/2026-06-22/doc-iniefzfw0327924.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag low">理念转型：低</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多元策略基金业绩承压·多元与赛道策略走向融合·投研框架升级</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>策略失效：</b>近两年来，随着A股市场结构性行情极致演绎，基金的多元配置策略越来越难。<br>
          <b>融合趋势：</b>业内普遍认为，公募投研正在打破赛道和均衡二选一的固有认知，两种投资框架逐步融合发展。<br>
          <b>对基金行业影响：</b>多元与赛道策略融合→基金经理投资框架升级→腾安在基金筛选和推荐时，需关注基金经理的框架进化能力。
        </div>
        <div class="card-footer">
          <a href="https://egs.stcn.com/news/detail/2304821.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯</span></a>
          <span class="impact-tag low">策略演变：低</span>
        </div>
      </div>"""

new_s1 = """    <div class="card-grid">

      <!-- S1 Card 1: 浮费基金一周年业绩断层 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 浮费基金一周年业绩断层·华商致远回报A成三倍基·首尾相差329个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>业绩表现：</b>截至6月22日，首批26只新型浮动费率基金中，华商致远回报A成立以来收益<b>316.56%</b>，排名第一；鹏华共赢未来A亏损<b>-12.84%</b>，排名垫底。首尾相差<b>329个百分点</b>。<br>
          <b>分化原因：</b>①赛道选择：绩优产品重仓AI光通信（中际旭创、长飞光纤）；绩差产品配置传统价值（白酒、银行、地产）。②操作节奏：科技成长风格在市场分化环境下占优。<br>
          <b>费率机制：</b>运作满一年后，绩优产品对持有满一年投资者按<b>1.50%</b>收费；绩差产品按<b>0.60%</b>收费。费率与业绩挂钩机制正式生效。<br>
          <b>对基金行业影响：</b>浮动费率改革打破"旱涝保收"→业绩分化验证改革必要性→腾安在推荐浮费基金时应充分披露费率机制。
        </div>
        <div class="card-footer">
          <a href="https://fund.eastmoney.com/a/202606233779894014.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <a href="https://news.10jqka.com.cn/20260625/c677692767.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺·证券日报</span></a>
          <span class="impact-tag medium">浮费改革：高</span>
        </div>
      </div>

      <!-- S1 Card 2: QDII产品限购力度再加码 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII产品限购力度再加码·超百只限购百元及以下·业绩近一年平均22%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购加码：</b>6月23-24日，易方达、万家、华宝等多家基金公司集中下调QDII产品大额申购上限，易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>，华宝海外科技股票(QDII-LOF)降至20元。<br>
          <b>限购规模：</b>截至6月22日，全市场超百只QDII产品限购额度在100元及以下，占限购总数近三成。6月以来已有超20只QDII基金宣布暂停大额申购。<br>
          <b>背后逻辑：</b>近一年QDII产品平均收益率22%，45只净值翻倍。业绩吸引资金→外汇额度消耗→限购保护存量持有人利益。<br>
          <b>政策预期：</b>央行副行长朱鹤新在陆家嘴论坛表示将发放新一批QDII投资额度，未来QDII产品供给有望增加。<br>
          <b>对基金行业影响：</b>QDII稀缺性加剧→腾安应提前储备QDII产品额度→客户咨询时提供替代方案。
        </div>
        <div class="card-footer">
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260624/6313305.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag medium">QDII稀缺：高</span>
        </div>
      </div>

      <!-- S1 Card 3: FOF上半年新发规模1137亿 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 FOF上半年新发规模1137亿·超越2021年峰值·低利率催化+银行渠道发力</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>爆发式增长：</b>Wind数据显示，截至6月20日，2026年以来新成立FOF基金已达<b>88只</b>，合计发行规模高达<b>1137.69亿元</b>，超越2021年创下的<b>1083.62亿元</b>历史峰值。<br>
          <b>对基金行业影响：</b>FOF从"配角"走向舞台中央→资产配置需求上升→腾安可加大FOF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3970656.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">FOF爆发：高</span>
        </div>
      </div>

      <!-- S1 Card 4: 证监会支持中小基金公司差异化发展 -->
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
      </div>

      <!-- S1 Card 5: 从千亿抢购到千元限购 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 从千亿抢购到千元限购·公募行业从"重规模"向"重回报"转型</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>行业转型：</b>证监会主席吴清强调基金行业应坚持客户为本，增强逆周期思维，遏制"冲规模、赚快钱"等顽疾。标志着公募从"重规模"向"重回报""以持有人利益为本"转型。<br>
          <b>新发克制：</b>2026年以来，新成立基金729只，合计规模5696亿元，不足2021年同期一半。百亿级"大爆款"未再出现。<br>
          <b>限购潮：</b>多只绩优基金将单日申购上限降至1万元甚至1000元。今年业绩排名前十的主动权益基金中，七只处于暂停申购或暂停大额申购状态。<br>
          <b>对基金行业影响：</b>"限购"是投资者保护机制→行业理念变革→腾安在基金筛选时应更关注长期业绩和投资者回报。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/wm/2026-06-22/doc-iniefzfw0327924.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag low">理念转型：低</span>
        </div>
      </div>

      <!-- S1 Card 6: 债券ETF规模首超8500亿元 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 债券ETF规模首超8500亿元·科创债ETF+基准做市信用债ETF双引擎驱动</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模突破：</b>Choice数据显示，截至2026年6月17日，全市场债券型ETF总规模首次突破<b>8500亿元</b>，同比增长超<b>180%</b>，在全部ETF市场中的规模占比从7%大幅跃升至18%。<br>
          <b>双引擎驱动：</b>科创债ETF（24只，规模2941亿元）和基准做市信用债ETF（9只，规模1413亿元）是本轮增长双引擎，两者合计占债券ETF总规模超50%。<br>
          <b>对基金行业影响：</b>债券ETF从"配置工具"升级为"交易+配置"双功能载体→腾安可加大债券ETF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://admin@stcn.com/article/detail/3970746.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">债券ETF：高</span>
        </div>
      </div>"""

if old_s1 in content:
    content = content.replace(old_s1, new_s1)
    print("✅ S1 重磅信息更新完成（6条，清理了早于06-11的条目）")
else:
    print("⚠️  S1 旧内容未找到，需要手动更新")

# ============================================================
# 5. 更新 S2 监管政策（清理早于06-11的条目）
# ============================================================
# S2 的4条内容（06-13/06-12/06-17/06-22）都在T-14范围内，保留不动
# 无需新增06-25的监管政策（今天无重大监管政策发布）
print("✅ S2 监管政策无需更新（4条均在T-14范围内）")

# ============================================================
# 6. 更新 S6 市场行情速览
# ============================================================
old_s6 = """    <div class="card p3">
      <div class="card-top">
        <div class="card-title">2026年6月24日（周三）·A股低开0.39%·药ETF涨1%·科技股分化</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股今日（6/24）低开：</b><br>
            ▪ 沪指跌<b>0.39%</b>（4090.10点）<br>
            ▪ 深成指跌<b>0.45%</b>（15782.40点）<br>
            ▪ 创业板指跌<b>0.25%</b>（4181.91点）<br>
            ▪ 科创50跌<b>0.92%</b>（1929.27点）<br>
            ▪ 盘面：锂电池·化工·创新药活跃；培育钻石·光通信·有色·半导体低迷<br><br>
            <b>📊 港股今日（6/24）跟随美股低开：</b><br>
            ▪ 恒生指数跌<b>1.82%</b>（23336.28点）<br>
            ▪ 恒生科技指数跌<b>3.30%</b>（4399.22点）<br>
            ▪ 科技股普跌：腾讯-4.2%·阿里-3.84%·京东-4.37%·小米-4.64%
          </div>
          <div>
            <b>📊 美股昨夜（6/23）全线收跌：</b><br>
            ▪ 道指<b>-0.09%</b>（51666.84点）—— 微软·亚马逊·IBM逆势涨<br>
            ▪ 纳指<b>-2.21%</b>（25587.04点）—— 科技股抛售·存储芯片崩盘<br>
            ▪ 标普500<b>-1.44%</b>（7365.46点）<br>
            ▪ 芯片股：美光-13%·闪迪-13%·英特尔-6%·高通-8%<br><br>
            <b>📊 对基金行业影响（今日A股）：</b><br>
            ▪ A股低开→客户可能咨询市场观点，提前准备话术<br>
            ▪ 创新药板块活跃→医药主题基金可能受关注<br>
            ▪ 科技股分化→关注科创50能否止跌企稳
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·2026-06-24 10:00</span>
        <span class="source-tag">美股：2026-06-22 收盘</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>"""

new_s6 = """    <div class="card p3">
      <div class="card-top">
        <div class="card-title">2026年6月25日（周四）·A股开盘分化·创业板+0.63%·存储芯片/光刻机活跃</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股今日（6/25）开盘分化：</b><br>
            ▪ 沪指跌<b>0.18%</b>（4103.48点）<br>
            ▪ 深成指涨<b>0.30%</b>（16099.76点）<br>
            ▪ 创业板指涨<b>0.63%</b>（4278.34点）<br>
            ▪ 科创50涨<b>0.77%</b>（2004.77点）<br>
            ▪ 沪深300涨<b>0.16%</b>（4950.98点）<br>
            ▪ 盘面：存储芯片·光刻机·光纤涨幅居前；创新药·贵金属·有色跌幅居前<br><br>
            <b>📊 港股今日（6/25）待更新：</b><br>
            ▪ 恒生指数（待更新）<br>
            ▪ 恒生科技指数（待更新）
          </div>
          <div>
            <b>📊 美股昨夜（6/24）收盘：</b><br>
            ▪ 道指（待更新）<br>
            ▪ 纳指<b>+0.03%</b>（25733.17点）—— 英伟达+4.3%·AMD+6.6%<br>
            ▪ 标普500（待更新）<br>
            ▪ 芯片股反弹：美光+4%·闪迪+5%·英特尔反弹<br><br>
            <b>📊 对基金行业影响（今日A股）：</b><br>
            ▪ 开盘分化→客户可能咨询市场观点，提前准备话术<br>
            ▪ 存储芯片/光刻机活跃→相关主题ETF可能受关注<br>
            ▪ 创新药板块回调→关注医药主题基金净值波动
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·2026-06-25 10:00</span>
        <span class="source-tag">美股：2026-06-24 收盘</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>"""

if old_s6 in content:
    content = content.replace(old_s6, new_s6)
    print("✅ S6 市场行情速览更新完成")
else:
    print("⚠️  S6 旧内容未找到，需要手动更新")

# ============================================================
# 7. 更新 S7 时间线（清理06-11之前条目，新增06-25/06-24）
# ============================================================
# 删除06-11的条目（欧央行重启加息·SpaceX定价确认）
old_timeline_0611 = """      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-11（欧央行重启加息·SpaceX定价确认）</div>
          <div class="timeline-title">欧央行宣布重启加息25bp（全球主要经济体首家）/ SpaceX IPO定价135美元/股确认</div>
          <div class="timeline-desc">欧洲央行成为2026年首家重启加息的全球主要经济体央行，存款机制利率+25bp。SpaceX IPO发行价确认为135美元/股，估值1.77万亿美元，明日正式挂牌。</div>
        </div>
      </div>"""

if old_timeline_0611 in content:
    content = content.replace(old_timeline_0611, '')
    print("✅ S7 时间线：删除06-11过期条目")
else:
    print("⚠️  S7 06-11条目未找到（可能已删除）")

# 在S7时间线顶部插入06-25和06-24的新条目
new_timeline_entries = """
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-25（周四·A股分化·创业板+0.63%·存储芯片/光刻机活跃·央行5000亿MLF）</div>
          <div class="timeline-title">A股开盘分化 / 央行5000亿MLF净投放2000亿 / 浮费三倍基报道持续发酵 / 英伟达股东大会</div>
          <div class="timeline-desc">6月25日，A股开盘分化：沪指跌0.18%（4103.48点），创业板指涨0.63%（4278.34点），科创50涨0.77%。存储芯片、光刻机、光纤概念涨幅居前。央行今日开展5000亿元1年期MLF操作，净投放2000亿元。英伟达年度股东大会北京时间周四凌晨举行，黄仁勋表示算力越多、token越多、收入越多。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-24（周三·A股低开0.39%·药ETF涨1%·浮费三倍基报道·QDII限购加码）</div>
          <div class="timeline-title">A股低开0.39%·药ETF华宝涨超1%·浮费三倍基诞生报道·QDII限购加码至10元 / 央行预告5000亿MLF</div>
          <div class="timeline-desc">6月24日，A股三大股指集体低开，沪指跌0.39%（4090.10点）。恒瑞医药公布新专利，药ETF华宝(562050)涨超1%。媒体集中报道浮费三倍基（华商致远回报A收益316.56%）。QDII限购再加码，易方达全球成长精选降至10元。央行预告6月25日开展5000亿元MLF操作。</div>
        </div>
      </div>
      
"""

# 找到S7时间线的起始位置并插入新条目
s7_marker = '<div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-24'
if s7_marker in content:
    # 已经存在06-24条目，我们只需要确保它是最新的
    print("ℹ️  S7 06-24条目已存在")
else:
    # 需要插入新条目
    s7_insert_marker = '<div class="card" style="border-left-color: var(--info);">\n      \n      '
    if s7_insert_marker in content:
        content = content.replace(s7_insert_marker, s7_insert_marker + new_timeline_entries)
        print("✅ S7 时间线：新增06-25和06-24条目")
    else:
        print("⚠️  S7 插入标记未找到，需要手动更新")

# ============================================================
# 8. 更新 Footer 日期
# ============================================================
content = content.replace(
    '数据更新时间：2026年06年23日 10:30 · 近两周核心资讯（06-08 — 06-22）·',
    '数据更新时间：2026年06月25日 10:00 · 近两周核心资讯（06-11 — 06-25）·'
)

print("✅ Footer 更新完成")

# ============================================================
# 9. 写入更新后的文件
# ============================================================
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n🎉 HTML更新完成！")
print(f"   原长度: {len(content)} 字符（注：这是更新后长度）")
print(f"   文件路径: {filepath}")
print(f"\n⚠️  注意事项：")
print(f"   1. S6 美股数据需要手动补充完整（道指/标普500具体数值）")
print(f"   2. S7 时间线如果插入失败需要手动添加06-25/06-24条目")
print(f"   3. S8 待办跟踪需要手动添加（如果HTML中缺失）")
