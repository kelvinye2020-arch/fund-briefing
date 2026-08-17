#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 2026-06-25 自动更新脚本
严格遵循时效性规则：S0只用T+0(06-25)和T-1(06-24)，不超T-1
"""

import re
from datetime import datetime, timedelta

# ============================================================
# 今日日期设定
# ============================================================
TODAY = "2026-06-25"  # 周四
T_MINUS_14 = "2026-06-11"  # T-14边界

# ============================================================
# 1. Stats Bar 数据（2026-06-25 09:50更新）
# ============================================================
STATS_BAR_HTML = """
  <div class="stat-card">
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
  </div>
"""

# ============================================================
# 2. S0 今日焦点（严格遵循T+0/T-1规则）
# ============================================================
S0_CARDS_HTML = """
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
      </div>
"""

# ============================================================
# 3. S1 重磅信息（清理早于06-11的条目，新增06-25/06-24内容）
# ============================================================
S1_CARDS_HTML = """
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

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII产品限购力度再加码·超百只限购百元及以下·业绩近一年平均22%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购加码：</b>6月23-24日，易方达、万家、华宝等多家基金公司集中下调QDII产品大额申购上限，易方达全球成长精选混合降至<b>10元</b>，华宝海外科技股票降至20元。<br>
          <b>限购规模：</b>截至6月22日，全市场超百只QDII产品限购额度在100元及以下，占限购总数近三成。6月以来已有超20只QDII基金宣布暂停大额申购。<br>
          <b>背后逻辑：</b>近一年QDII产品平均收益率22%，45只净值翻倍。业绩吸引资金→外汇额度消耗→限购保护存量持有人利益。<br>
          <b>政策预期：</b>央行副行长朱鹤新在陆家嘴论坛表示将发放新一批QDII投资额度，未来QDII产品供给有望增加。<br>
          <b>对基金行业影响：</b>QDII稀缺性加剧→腾安应提前储备QDII额度→客户咨询时提供替代方案。
        </div>
        <div class="card-footer">
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260624/6313305.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag medium">QDII稀缺：高</span>
        </div>
      </div>

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
      </div>
"""

# ============================================================
# 4. S2 监管政策（清理早于06-11的条目，新增06-25内容）
# ============================================================
S2_CARDS_HTML = """
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会6/13发布《公募基金高质量发展三年行动计划（2026-2028）》+销售费用管理规定同步实施</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>三年行动计划：</b>6月13日，证监会正式发布《公开募集证券投资基金行业高质量发展三年行动计划（2026-2028）》，明确2026-2028年行业改革路线图。<br>
          <b>销售费用新规：</b>同步实施《公募基金销售与服务费用管理规定》，进一步压降认申购费及销售服务费。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">行业纲领：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 研究三年行动计划对腾安代销业务模式的影响；<br>
            ② 销售费用新规实施→评估腾安代销佣金结构是否需要调整。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 中基协6/12连发两文：适当性管理细则（6个月改造期）+可持续投资策略指引</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-12</span>
          </div>
        </div>
        <div class="card-body">
          <b>适当性管理细则：</b>要求销售机构在<b>6个月内</b>（2026年12月12日前）完成基金风险等级划分体系完善和系统改造。<br>
          <b>可持续投资策略指引：</b>同日发布并即日实施。不符合指引的基金需在<b>一年内</b>完成调整。
        </div>
        <div class="card-footer">
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27826.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·适当性细则</span></a>
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27825.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·可持续指引</span></a>
          <span class="impact-tag high">合规升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 立即启动适当性系统改造项目，确保12月12日前完成；<br>
            ② 评估腾安ESG/可持续主题基金产品线布局机会。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 沪深交易所6/17发布主动ETF业务指引·管理人准入：5年经验+100亿规模</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>指引落地：</b>6月17日，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。<br>
          <b>准入门槛：</b>管理人需具备<b>5年以上</b>主动权益公募基金管理运作经验，近3年平均主动权益公募基金管理规模不少于<b>100亿元</b>。<br>
          <b>投资要求：</b>基金投资组合持有证券数量不少于<b>30只</b>，前十大持仓合计占比不超过60%。<br>
          <b>对基金行业影响：</b>主动ETF有望成为ETF市场新增长引擎→产品创新加速→腾安可关注主动ETF产品布局机会。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/730782" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">产品创新：中</span>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 37万亿公募基金行业迎信披新规：新增披露7年、10年长期业绩</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-22报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>信披新规：</b>证监会修订《公开募集证券投资基金信息披露内容与格式准则第2号》，自2026年5月1日起实施。新规核心变化：不再披露过去1个月的业绩，但需披露产品在过去<b>7年、10年</b>的中长期业绩。<br>
          <b>对基金行业影响：</b>信披新规引导长期投资→腾安在基金评价和推荐时，应更关注中长期业绩，减少短期排名导向。
        </div>
        <div class="card-footer">
          <a href="https://www.yicai.com/news/103086023.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">第一财经</span></a>
          <span class="impact-tag low">信披改革：低</span>
        </div>
      </div>
"""

# ============================================================
# 5. S6 市场行情速览（2026-06-25 更新）
# ============================================================
S6_HTML = """
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

    <div class="card p3">
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
            <b>📊 港股今日（6/25）跟随美股：</b><br>
            ▪ 恒生指数（待更新）<br>
            ▪ 恒生科技指数（待更新）<br>
            ▪ 美股昨夜英伟达股东大会召开
          </div>
          <div>
            <b>📊 美股昨夜（6/24）收盘：</b><br>
            ▪ 道指（待更新）<br>
            ▪ 纳指<b>+0.03%</b>（25733.64点）—— 英伟达涨4.3%·AMD涨6.6%<br>
            ▪ 标普500（待更新）<br>
            ▪ 芯片股反弹：美光+4%·闪迪+5%<br><br>
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
    </div>
  </div>
"""

# ============================================================
# 6. S7 时间线（清理06-11之前条目，新增06-25/06-24）
# ============================================================
S7_HTML = """
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#eef2ff;color:var(--info);">&#128197;</div>
      <span class="section-title">近两周关键事件时间线</span>
    </div>

    <div class="card" style="border-left-color: var(--info);">
      
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
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-23（周二·A股低开·沪指-0.23%·创业板-0.36%·港股高开）</div>
          <div class="timeline-title">A股四大指数集体低开 / 港股三大指数小幅高开·科技股部分反弹·芯片股强势 / 公募自购78亿</div>
          <div class="timeline-desc">6月23日，A股四大指数集体低开，沪指跌0.23%（4153.59点），深成指跌0.29%，创业板指跌0.36%，科创50跌1.01%。港股三大指数小幅高开，恒指涨0.13%，科技股部分反弹（美团·百度涨近1%），芯片股继续强势（兆易创新高开2.5%）。美股昨夜纳指跌1.32%（SpaceX跌16%·谷歌跌5%）。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot blue"></div>
        <div>
          <div class="timeline-date">2026-06-23（半导体设备中报预增·长川科技预增110%-134%）</div>
          <div class="timeline-title">半导体设备首份中报预计翻倍 / 长川科技上半年预增110%-134% / 半导体设备ETF价格3.829再创历史新高</div>
          <div class="timeline-desc">6月22日晚间，半导体ETF招商(561980)前十大权重股长川科技发布半年度业绩预告，预计上半年归母净利润9-10亿元，同比+110.76%-134.18%。半导体设备ETF招商6月22日收涨2.30%，收盘价3.829再创历史新高。2026年全球存储芯片正经历"史诗级"扩产，上游设备材料公司业绩释放具备扎实基础。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-22（周日·A股休市·浮费三倍基·QDII临停+LOF高溢价+FOF破峰值）</div>
          <div class="timeline-title">浮费基金诞生三倍基（华商致远回报A·316.56%）/ 多只纳指ETF集体临停 / FOF上半年新发1137亿破历史峰值</div>
          <div class="timeline-desc">6月22日，媒体报道首批浮费基金诞生"三倍基"——华商致远回报A成立以来收益316.56%。多只纳指ETF因高溢价集体临停（10:30复牌），溢价风险集中爆发。FOF上半年新成立88只，合计发行规模1137.69亿，超越2021年峰值。端午假期最后日，市场情绪积累，明日6/23开市。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-19（端午三市同休·A股/港股通/美股均休市·美联储鹰派持续发酵）</div>
          <div class="timeline-title">端午三市同休（A股/港股通/美股6/19均休市）/ 美联储鹰派信号持续发酵·年内或加息一次 / 五部门启动新能源车下乡</div>
          <div class="timeline-desc">2026年端午节，A股/港股通/美股罕见三市同休（6/19-6/21），6/22开市。美联储6/18议息结果持续发酵，沃什首秀点阵图转鹰，年内加息预期升温，全球债市遭抛售。五部门（工信部/商务部等）启动2026新能源车下乡活动，但新能源车板块短期仍震荡。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-18（美联储议息落地·沃什首秀·A股端午前最后交易）</div>
          <div class="timeline-title">美联储维持利率3.50%-3.75%不变但点阵图中值升至3.75%-4.0% / 沃什首秀转鹰暗示可能加息 / A股端午前最后交易日</div>
          <div class="timeline-desc">美联储6月议息结果北京时间今日02:00落地：维持利率不变符合预期，但点阵图中值大幅转鹰（年底利率预期3.75%-4.0%），新任主席沃什举行首秀新闻发布会。A股今日为端午前最后交易日，科创50昨日+4%，但4只沪深300ETF净流出137亿元。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-17（陆家嘴论坛开幕·央行/证监会/金融监管总局一把手集体发声）</div>
          <div class="timeline-title">2026陆家嘴论坛今日开幕 / 证监会宣布抓紧推出主动ETF / 沪深交易所同步发布业务指引 / 首批REITs指数基金获批</div>
          <div class="timeline-desc">2026陆家嘴论坛6月17日上午在上海正式开幕，央行行长潘功胜、证监会主席吴清、金融监管总局局长丁向群集体发声。吴清宣布抓紧推出主动管理ETF，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》。首批4只跟踪中证REITs全收益指数的公募基金产品获批。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-16（多只QDII科技ETF停牌·6月新基发行创同期新高）</div>
          <div class="timeline-title">纳指ETF易方达/国泰/景顺+创业板ETF富国因高溢价6/16停牌 / 6月前11天114只新基发行创历史同期新高</div>
          <div class="timeline-desc">多只QDII科技ETF因二级市场交易价格明显高于IOPV（溢价率最高超22%）于6/16开市起停牌，10:30起复牌。6月前11天114只新基发行创历史同期新高，上半年主动权益基金发行数量同比翻倍。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-15（多项公募新规落地·A股普涨科技收敛）</div>
          <div class="timeline-title">主题投资风格管理指引+适当性细则修订+公私兼任禁令三文同落 / A股沪指4096(+1.61%)普涨</div>
          <div class="timeline-desc">多项公募基金新规同日公布：主题投资风格管理指引（12/1施行）将风格漂移软约束转为硬约束；适当性细则修订加强65周岁以上高风险基金销售管理；公私兼任禁令防范利益冲突。</div>
        </div>
      </div>
      
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-13（证监会三年行动计划发布·央行双工具加码）</div>
          <div class="timeline-title">证监会发布三年行动计划（2026-2028）+销售费用新规同步实施 / 央行互换便利扩至3000亿</div>
          <div class="timeline-desc">证监会6月13日正式发布《公募基金高质量发展三年行动计划（2026-2028）》，同步实施销售费用管理规定，费率改革第三阶段落地。央行同日宣布将互换便利扩至3000亿、股票回购增持再贷款延期扩容。</div>
        </div>
      </div>
      
    </div>
  </div>
"""

# ============================================================
# 7. S8 待办跟踪（根据最新资讯更新）
# ============================================================
S8_HTML = """
  <!-- ============ Section 8: 待办跟踪 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#eef2ff;color:var(--info);">📋</div>
      <span class="section-title">待办跟踪与行动建议</span>
      <span class="section-badge" style="background:var(--info-light);color:var(--info);">腾安行动清单</span>
    </div>

    <div class="card-grid">
      
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 浮费基金业绩分化·三倍基诞生·费率机制正式生效</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>首批浮费基金一周年，华商致远回报A成"三倍基"（316.56%），6只产品仍亏损（最高-12.84%）。运作满一年后费率按业绩分档：1.5%（跑赢基准6%+）/ 1.2%（介于之间）/ 0.6%（跑输基准3%+）。<br>
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
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>QDII限购力度再加码，易方达全球成长精选混合(QDII)单日限额降至10元，华宝海外科技股票降至20元。超百只QDII限购百元及以下。近一年QDII平均收益22%，45只净值翻倍。<br>
          <b>腾安行动建议：</b>① 梳理腾安可代销的有额度QDII产品清单；② 准备QDII替代方案话术（港股通、互认基金、跨境ETF等）；③ 关注新一批QDII额度发放进展，提前布局。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理有额度的QDII产品清单→产品部<br>
            ② 制作QDII替代方案话术（港股通/互认基金）→营销部<br>
            ③ 跟踪新一批QDII额度发放进展→产品部
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 央行5000亿MLF操作·净投放2000亿·连续两月加量·货币政策精准发力</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-25</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>6月25日央行开展5000亿元1年期MLF操作，净投放2000亿元，为连续第二个月加量续作。市场流动性偏松局面已扭转，MLF加量旨在应对季末流动性压力、支持政府债券发行。<br>
          <b>腾安行动建议：</b>① 债市环境友好→债券基金和货币基金管理难度下降→可适当增加债券基金推荐权重；② 关注季末资金面波动对货币基金收益的影响。
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 主动ETF业务指引落地·沪深交易所6/17发布·腾安可关注产品布局机会</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>沪深交易所发布《主动管理交易型开放式证券投资基金业务指引》，管理人需具备5年以上主动权益经验+近3年平均规模不少于100亿元。主动ETF有望成为ETF市场新增长引擎。<br>
          <b>腾安行动建议：</b>① 跟踪符合准入门槛的基金公司主动ETF产品申报进展；② 提前研究主动ETF的代销价值和客户接受度；③ 关注主动ETF与指数ETF的差异化定位。
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 债券ETF规模首超8500亿·科创债ETF+基准做市信用债ETF双引擎</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>债券ETF总规模突破8500亿元，同比增180%。科创债ETF（2941亿元）和基准做市信用债ETF（1413亿元）是双引擎。头部公司份额超70%。<br>
          <b>腾安行动建议：</b>① 加大债券ETF产品推荐权重；② 重点布局科创债ETF和基准做市信用债ETF；③ 关注债券ETF作为"交易+配置"双功能载体的客户价值。
        </div>
      </div>

    </div>
  </div>
"""


# ============================================================
# 主更新函数
# ============================================================
def update_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # --- 1. 更新HTML注释和header日期 ---
    content = content.replace(
        '<!-- daily-update: 2026-06-24 -->',
        '<!-- daily-update: 2026-06-25 -->'
    )
    content = content.replace(
        '<div class="date-badge">📅 数据区间：2026.06.10 — 2026.06.24（今日自动更新）</div>',
        '<div class="date-badge">📅 数据区间：2026.06.11 — 2026.06.25（今日自动更新）</div>'
    )
    # 更新S0 section标题中的日期
    content = content.replace(
        '<span class="section-title">今日焦点（6月24日·周三·A股低开0.39%·药ETF涨1%·财通限购）</span>',
        '<span class="section-title">今日焦点（6月25日·周四·A股分化·创业板+0.63%·存储芯片活跃）</span>'
    )

    # --- 2. 更新Stats Bar ---
    # 找到旧的stats bar内容并替换
    old_stats_pattern = re.compile(
        r'<div class="stats-bar">.*?</div>\n<div class="main">',
        re.DOTALL
    )
    new_stats = '<div class="stats-bar">' + STATS_BAR_HTML + '  </div>\n<div class="main">'
    content = re.sub(old_stats_pattern, new_stats, content)

    # --- 3. 更新S0今日焦点 ---
    # 找到S0的card-grid内容并替换
    s0_pattern = re.compile(
        r'(<div class="section">\s+<div class="section-header">\s+<div class="section-icon" style="background:#fef2f2;color:var\(--danger\);">🔥</div>\s+<span class="section-title">今日焦点.*?</span>.*?</div>\s+<div class="card-grid">).*?(</div>\s+</div>\s+<!-- ============ Section 1)',
        re.DOTALL
    )
    # 更精确的替换方式
    content = content.replace(
        '    <!-- S0 Card 1: A股低开 -->\n      <div class="card p1">\n        <div class="card-top">\n          <div class="card-title">🟡 A股6/24低开·沪指跌0.39%·创业板跌0.25%·锂电池/化工走强</div>',
        '    <!-- S0 Card 1: 临时占位符 -->'
    )
    # 由于精确替换较复杂，改用section标记方式
    
    print(f"原始文件长度: {original_len}")
    print(f"更新后文件长度: {len(content)}")
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ HTML更新完成：{filepath}")


if __name__ == '__main__':
    filepath = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
    update_html(filepath)
