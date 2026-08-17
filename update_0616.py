#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 2026-06-16 每日更新脚本
"""

import re

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Header 数据区间更新
# ============================================================
old_header = '数据区间：2026.06.01 — 2026.06.15（周度巡检更新）'
new_header = '数据区间：2026.06.02 — 2026.06.16（今日自动更新）'
content = content.replace(old_header, new_header)

# ============================================================
# 2. HTML注释更新（每日更新标记）
# ============================================================
content = re.sub(r'<!-- daily-update: 2026-06-\d+ -->', '<!-- daily-update: 2026-06-16 -->', content)
content = re.sub(r'<!-- daily-updaye: 2026-06-\d+ -->', '<!-- daily-update: 2026-06-16 -->', content)

# ============================================================
# 3. Stats Bar 更新（4个卡片）
# ============================================================
old_stats = '''  <div class="stat-card">
    <div class="stat-number">证监会三年计划</div>
    <div class="stat-label">证监会6/13正式发布《公募基金高质量发展三年行动计划（2026-2028）》+销售费用新规同步实施</div>
    <div class="stat-change up">▲ 行业纲领性文件落地·费率改革深化·代销机构影响深远</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">美联储议息倒计时</div>
    <div class="stat-label">6/16-17美联储议息会议·6/18公布结果·欧央行已重启加息25bp·全球央行政策分化加剧</div>
    <div class="stat-change up">▲ QDII产品波动风险上升·固收+再平衡压力·关注点阵图变化</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">适当性改造倒计时</div>
    <div class="stat-label">中基协6/12发布适当性管理细则·6个月改造期（12月12日截止）·可持续指引即日实施</div>
    <div class="stat-change up">▲ 腾安需立即启动系统改造·ESG基金产品线扩展迎来政策支持</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4031·端午前</div>
    <div class="stat-label">上周五6/12沪指4031(+1.12%)·全周成交13.95万亿创近5周新低·明日6/16周一开盘+端午假期临近</div>
    <div class="stat-change down">▼ 6/19-21端午休市·节前避险情绪升温·关注明日开盘量能变化</div>
  </div>'''

new_stats = '''  <div class="stat-card">
    <div class="stat-number">主题风格新规</div>
    <div class="stat-label">6/15多项公募新规落地：主题风格管理指引(12/1施行)+适当性细则修订+公私兼任禁令</div>
    <div class="stat-change up">▲ 风格漂移硬约束·适当性升级·基金经理公私兼任全面禁止</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">ETF溢价潮</div>
    <div class="stat-label">6/16纳指ETF易方达/国泰/景顺+创业板ETF富国集体停牌(10:30复牌)·溢价套利风险激增</div>
    <div class="stat-change up">▲ 多只QDII科技ETF高溢价·停牌期间可赎回·关注10:30复牌后走势</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">新基发行翻倍</div>
    <div class="stat-label">6月前11天114只新基发行创历史同期新高·上半年主动权益基金发行数量同比翻倍</div>
    <div class="stat-change up">▲ 权益回暖·科技主导·吴清定调"公募注重权益投资"加速落地</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4096·科技强</div>
    <div class="stat-label">昨日6/15沪指4096(+1.61%)·今日上午创业板指+2.05%科技强势·端午假期前最后交易周</div>
    <div class="stat-change up">▲ 科技/建材领涨·端午前最后交易周·6/19-21休市</div>
  </div>'''

content = content.replace(old_stats, new_stats)

# ============================================================
# 4. S0 今日焦点 更新
#    规则：T+0/T-1优先，date-tag必须真实
#    新内容：06-15公募新规(T-1) + 06-16 ETF停牌(T+0) + 06-16新基发行(T+0)
# ============================================================
old_s0_cards = '''    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会6月13日正式发布《公募基金高质量发展三年行动计划（2026-2028）》！同步实施销售费用管理规定</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>纲领性文件落地：</b>6月13日，证监会正式发布《公开募集证券投资基金行业高质量发展三年行动计划（2026-2028）》，这是继2025年5月《推动公募基金高质量发展行动方案》之后，行业首份<b>三年期系统性行动纲领</b>。同步实施《公募基金销售与服务费用管理规定》，进一步压降销售费用、规范代销行为。<br>
          <b>核心方向：</b>三年行动计划明确2026-2028年行业改革路线图，重点包括：①完善业绩比较基准约束机制；②深化费率改革（销售费用新规同步落地）；③强化基金评价长期化导向；④提升行业合规风控水平；⑤支持中长期资金入市。<br>
          <b>对代销机构影响：</b>销售费用新规直接压缩代销佣金空间，持牌机构需加速从"销售佣金驱动"向"买方投顾服务费驱动"转型。腾安作为腾讯系平台，需提前规划收费模式切换。<br>
          <b>下一步：</b>各基金公司将在3个月内提交本单位落实三年行动计划的实施方案，行业将进入密集政策落地期。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867898160227504225" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·智通财经</span></a>
          <span class="impact-tag high">行业纲领：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 三年行动计划落地→研究对腾安代销业务模式的影响，提前规划收费模式转型；<br>
            ② 销售费用新规同步实施→评估腾安代销佣金结构是否需要调整，关注费率披露合规要求；<br>
            ③ 关注各基金公司在3个月内的落实方案，提前对接业务调整需求。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 央行6月13日双工具加码：互换便利扩至3000亿+股票回购增持再贷款延期，稳市工具走向常态化</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>互换便利扩围：</b>6月13日，中国人民银行宣布将"证券、基金、保险公司互换便利"操作规模从前期水平扩大至<b>3000亿元</b>，进一步提升非银机构流动性获取能力，支持资本市场稳定发展。<br>
          <b>再贷款工具优化：</b>同步宣布延长"股票回购增持再贷款"工具期限，并优化质押品范围，引导金融机构向上市公司和主要股东提供贷款，推动市值管理工具常态化使用。截至2026年3月末，已签定贷款合同金额约<b>3700亿元</b>，已发放超<b>1800亿元</b>。<br>
          <b>政策信号：</b>央行在同一日连续出台两项支持资本市场的货币政策工具，且表述中提出"探索常态化的制度安排"，标志着中国特色稳市机制建设进入新阶段。<br>
          <b>对基金行业影响：</b>互换便利扩容→券商/基金/险资流动性改善→有助于ETF等产品的做市能力和申购赎回稳定性；回购增持再贷款延期→上市公司增持回购动力增强→权益市场底部支撑力度加大。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">央行工具：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 互换便利扩至3000亿→ETF流动性改善，关注腾安代销ETF产品的折溢价稳定性；<br>
            ② 稳市工具常态化→权益市场底部支撑增强，中长期利好权益基金发行和销售；<br>
            ③ 关注央行后续是否有更多创新性货币政策工具支持资本市场。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 中基协6月12日连发两文：适当性管理细则（6个月改造期）+可持续投资策略指引（即日实施）</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-12</span>
          </div>
        </div>
        <div class="card-body">
          <b>适当性管理细则（中基协发〔2026〕13号）：</b>6月12日发布，要求各基金管理人、基金销售机构在发布之日起<b>6个月内</b>（即2026年12月12日前）完成基金风险等级划分体系完善和相关系统改造。这是继《推动公募基金高质量发展行动方案》后，销售端合规要求的具体落地。<br>
          <b>可持续投资策略指引（中基协发〔2026〕15号）：</b>同日发布并<b>即日实施</b>，规范公募基金可持续投资策略应用，保护投资者合法权益。不符合指引第十一条（业绩比较基准相关规定）的基金需按证监会基准指引调整，其他不符合规定的需在<b>一年内</b>完成调整。<br>
          <b>双重合规压力：</b>销售机构需在6个月内完成适当性系统改造，同时一年内完成可持续投资策略相关调整→IT成本和合规成本双升，中小代销机构压力更大，行业集中度进一步提升。<br>
          <b>对腾安影响：</b>腾讯系技术能力优势可支撑快速合规，适当性系统改造是展示合规能力的机会，可持续投资指引为ESG基金产品线扩展提供政策支持。
        </div>
        <div class="card-footer">
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27826.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·适当性细则</span></a>
          <a href="https://www.amac.org.cn/xwfb/xhyw/202606/t20260612_27825.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中基协·可持续指引</span></a>
          <span class="impact-tag high">合规升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 适当性细则6个月改造期→立即启动腾安适当性系统改造项目，确保12月12日前完成；<br>
            ② 可持续投资指引即日实施→评估腾安ESG/可持续主题基金产品线布局机会；<br>
            ③ 合规成本上升→中小代销机构压力加大，腾安作为头部平台受益集中度提升。
          </div>
        </div>
      </div>

    </div>'''

new_s0_cards = '''    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 多项公募新规6/15落地：主题风格管理指引(12/1施行)+适当性细则修订+基金经理公私兼任全面禁止</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-15</span>
          </div>
        </div>
        <div class="card-body">
          <b>主题投资风格管理指引（核心新规）：</b>6月12日发布，12月1日施行，设置12个月整改过渡期。明确要求：①主题基金合同中必须以可识别、可量化方式明确约定投资风格和范围；②建立专属投资风格库，80%以上非现金资产须投资风格库内证券；③建立"监测-预警-纠偏"闭环机制，将风格漂移"软约束"转为"硬约束"；④针对严重偏离投资方向、投资集中度过高情形建立差异化管控机制，<b>防范过度抱团风险</b>。<br>
          <b>适当性管理细则修订：</b>同步修订，针对65周岁以上普通投资者销售高风险基金，需制定更审慎销售流程（追加信息了解、强化风险提示、增加回访频次）。<br>
          <b>基金经理公私兼任新规：</b>修订后的《基金经理兼任私募资产管理计划投资经理工作指引》明确：公募基金经理不得兼任非中长期资金委托管理的私募资管计划投资经理；禁止兼任人员及直系亲属投资其管理的私募资管计划；兼任人员考核不得与私募资管计划浮动管理费挂钩，<b>防范利益冲突</b>。<br>
          <b>信息出处：</b>新华网转载《经济参考报》6月15日报道，中国证券投资基金业协会官方发布。
        </div>
        <div class="card-footer">
          <a href="https://www.xinhuanet.com/fortune/20260615/9b4ec86c760a4acd83e7f86fea0cc001/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华网·经济参考报</span></a>
          <span class="impact-tag high">监管新规：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 主题风格管理指引12/1施行→立即排查腾安代销主题基金的风格披露合规性，提前12个月准备；<br>
            ② 适当性细则修订→关注65周岁以上客户高风险基金销售流程是否需要升级；<br>
            ③ 公私兼任禁令→关注合作基金公司基金经理变更公告，评估对相关基金业绩的影响。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 6/16多只QDII科技ETF集体停牌！纳指ETF易方达/国泰/景顺+创业板ETF富国因高溢价暂停交易</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>停牌清单（6/16开市起停牌，10:30起复牌）：</b><br>
          ① <b>纳指ETF易方达(159696)</b>：二级市场交易价格明显高于IOPV，出现较大幅度溢价<br>
          ② <b>纳指ETF国泰(513100)</b>：同上，高溢价触发停牌机制<br>
          ③ <b>纳指科技ETF景顺(159807)</b>：6/15收盘价2.740元，IOPV仅2.2292元，溢价率超<b>22%</b><br>
          ④ <b>创业板ETF富国(159971)</b>：6/15尾盘异常拉升涨停，收盘价1.606元，IOPV仅1.4065元，溢价率高达<b>14.18%</b>，当日成交额8218万元，尾盘集合竞价疑似"乌龙指"<br>
          <b>风险提示：</b>停牌期间赎回业务照常办理，但若复牌后溢价幅度未有效回落，基金有权采取进一步停牌措施。高溢价ETF存在溢价回落导致的价格下跌风险，投资者需谨慎。<br>
          <b>背景：</b>QDII科技ETF高溢价反映市场对美股科技板块的追捧情绪，但溢价率超10%已明显偏离理性区间，需警惕情绪退潮后的溢价回归风险。
        </div>
        <div class="card-footer">
          <a href="https://www.egsea.com/news/detail/2302695.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯·纳指ETF易方达</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1868056725899604004" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·创业板ETF富国溢价</span></a>
          <span class="impact-tag high">溢价风险：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① QDII科技ETF高溢价→立即排查腾安代销的纳指/创业板ETF是否也存在高溢价，及时发布风险提示；<br>
            ② 关注10:30复牌后价格走势→溢价回落可能引发客户投诉，提前准备解释话术；<br>
            ③ 创业板ETF富国尾盘异常拉升疑似乌龙指→关注监管是否介入调查，评估对创业板ETF整体溢价的影响。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 6月前11天114只新基发行创历史同期新高！上半年主动权益基金发行数量同比翻倍</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>6月发行热潮：</b>据Choice数据，6月1-11日全市场共有<b>114只</b>新基金启动发行，创历史同期新高。从产品结构看：股票型48只、混合型55只（偏股混合型25只）、债券型22只、FOF12只、QDII2只。权益类产品（股票型+偏股混合型）合计<b>73只</b>，占总量的64.04%。<br>
          <b>上半年翻倍：</b>2026年以来新成立基金数量达<b>750只</b>，合计募集资金<b>5535.50亿元</b>。较2025年同期主动权益基金发行数量<b>翻倍</b>增长（222只 vs 103只）。6月9-13日当周已有21只新基金启动发行，发行节奏持续加速。<br>
          <b>监管政策配合：</b>吴清6月6日在中基协第四届会员代表大会上明确"公募业要注重权益投资"，新基金发行节奏正体现这一政策方向。科技赛道（AI、半导体、光通信）成为机构核心布局方向。<br>
          <b>行业意义：</b>新基金发行"权益回暖、主题扎堆、发起式放量"三大特征明显，指数基金仍是发行主力，公募行业在监管政策鼓励下进入新一轮扩张周期。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867779792839003854" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·6月新基发行</span></a>
          <a href="https://finance.eastmoney.com/a/202606093765177780.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·权益回暖</span></a>
          <span class="impact-tag medium">发行热潮：中高</span>
        </div>
      </div>

    </div>'''

content = content.replace(old_s0_cards, new_s0_cards)

# ============================================================
# 5. S0 Section 标题更新
# ============================================================
old_s0_title = '今日焦点（6月13日·周五·证监会三年行动计划发布·央行双工具加码·中基协双指引落地）【周日6/15例行更新·无重大新新闻】'
new_s0_title = '今日焦点（6月16日·周一·公募新规严控风格漂移·QDII科技ETF集体停牌·6月新基发行创同期新高）'
content = content.replace(old_s0_title, new_s0_title)

old_s0_badge = '周日更新'
new_s0_badge = '周一更新'
content = content.replace(old_s0_badge, new_s0_badge)

# ============================================================
# 6. S1 重磅信息 更新
#    删除超期条目（T-14=06-02，需删除06-01及更早）
#    当前S1有6条：06-05/06-06/06-01/06-09~13/06-07~13/06-11
#    需删除：06-01（创业板超越上证·已超14天）
#    新增：06-15公募新规 + 06-16 ETF溢价潮
# ============================================================

# 删除06-01的S1卡片（创业板指首次收盘超越上证指数）
old_s1_card1 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 创业板指首次收盘超越上证指数！天弘创业板ETF创16年里程碑</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">05-28~06-01</span>
          </div>
        </div>
        <div class="card-body">
          <b>历史首次：</b>2026年5月28日，创业板指历史上首次收盘点位超越上证指数，标志着成长股对价值股的阶段性"逆袭"完成。同日创业板指数正式发布满16周年。<br>
          <b>资金追捧：</b>天弘基金旗下创业板ETF天弘(159977)作为国内较早深耕创业板赛道的产品，在5月末至6月初持续获得资金净流入，场内成交活跃度创近期新高。<br>
          <b>行业意义：</b>创业板超越上证→市场风格从"大盘价值"向"成长科技"的结构性切换已通过指数层面得到确认。科技/新能源/创新药等成长赛道ETF有望持续受益。<br>
          <b>后续关注：</b>6月12日宇树科技科创板上市、SpaceX IPO传闻→科技成长风格催化剂密集。
        </div>
        <div class="card-footer">
          <a href="https://xueqiu.com/2994748381/392400655" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">雪球</span></a>
          <a href="https://caifuhao.eastmoney.com/news/20260601073455766835490" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <span class="impact-tag high">风格切换：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 创业板超越上证→关注腾安创业板/科创相关ETF推荐权重是否需上调；<br>
            ② 成长风格确认→适当增加科技成长类基金曝光，但注意提示估值回调风险；<br>
            ③ 宇树/SpaceX催化→关注相关主题基金配置机会。
          </div>
        </div>
      </div>'''

content = content.replace(old_s1_card1, '')

# 在S1 card-grid末尾（</div>之前）新增2条
new_s1_cards = '''
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 多项公募新规6/15落地：主题风格硬约束+适当性升级+公私兼任全面禁止</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-15</span>
          </div>
        </div>
        <div class="card-body">
          <b>主题投资风格管理指引（12/1施行）：</b>要求主题基金以可量化方式明确约定投资风格，建立专属风格库，80%以上非现金资产须投资风格库内证券，建立"监测-预警-纠偏"闭环机制，<b>防范过度抱团风险</b>。<br>
          <b>适当性细则修订：</b>65周岁以上普通投资者销售高风险基金需制定更审慎流程（追加了解、强化提示、增加回访）。<br>
          <b>公私兼任禁令：</b>公募基金经理不得兼任非中长期资金私募资管计划投资经理，禁止兼任人员及直系亲属投资其管理的私募资管计划。<br>
          <b>行业影响：</b>三份文件同日落地，公募基金"强监管"周期全面开启，行业合规成本大幅上升，头部机构受益集中度提升。
        </div>
        <div class="card-footer">
          <a href="https://www.xinhuanet.com/fortune/20260615/9b4ec86c760a4acd83e7f86fea0cc001/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华网·经济参考报</span></a>
          <span class="impact-tag high">监管升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 主题风格硬约束→立即排查腾安代销主题基金的风格披露合规性；<br>
            ② 适当性细则修订→评估65周岁以上客户高风险基金销售流程升级需求；<br>
            ③ 三份文件同日落地→关注证监会后续是否有更多配套细则发布。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 6/16多只QDII科技ETF高溢价触发停牌：纳指ETF+创业板ETF溢价率最高超22%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>停牌清单：</b>纳指ETF易方达(159696)、纳指ETF国泰(513100)、纳指科技ETF景顺(159807)（溢价率超22%）、创业板ETF富国(159971)（溢价率14.18%，尾盘疑似乌龙指）。全部于6/16开市起停牌，10:30起复牌。<br>
          <b>溢价成因：</b>QDII额度受限+美股科技板块强势→场内QDII ETF供需失衡→溢价率持续走阔。纳指科技ETF景顺(159807)6/15收盘价2.740元，IOPV仅2.2292元。<br>
          <b>风险提示：</b>高溢价ETF存在溢价回落导致的价格下跌风险。若复牌后溢价未有效回落，基金有权采取进一步停牌措施。投资者需警惕情绪退潮后的溢价回归风险。<br>
          <b>对基金行业影响：</b>QDII ETF高溢价反映境内资金对海外科技资产的强烈配置需求，但溢价率超10%已偏离理性区间→监管可能介入规范，基金公司也可能通过新增份额的方式平抑溢价。
        </div>
        <div class="card-footer">
          <a href="https://stock.10jqka.com.cn/20260615/c677471994.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺·纳指科技ETF</span></a>
          <a href="https://m.jrj.com.cn/madapter/24h/2026/06/15172957472519.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">金融界·创业板ETF富国</span></a>
          <span class="impact-tag high">溢价风险：极高</span>
        </div>
      </div>
'''

# 在S1的 </div> 之前（最后一个card之后，section结尾之前）插入新卡片
# 找到S1 card-grid的结束标签
s1_end_marker = '    </div>\n\n  </div>\n\n  <!-- ============ Section 2'
content = content.replace(s1_end_marker, '    </div>' + new_s1_cards + '\n\n  </div>\n\n  <!-- ============ Section 2')

# ============================================================
# 7. S2 监管政策 更新
#    删除超期条目（T-14=06-02）
#    当前S2有4条：06-13/06-12/06-05/06-01~04
#    需删除：06-01~04（多规并行，已超14天）
#    新增：06-15主题风格管理指引（已在S0收录，但属于监管政策，需去重）
#    去重规则：S0已收录的06-15公募新规不再放入S2，S2放纯监管类
# ============================================================

# 删除S2中06-01~04的多规并行卡片
old_s2_card4 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 公募基金6月"多规并行"：基准换新+货基渠道整治+QDII额度收紧+债券ETF协议回购扩容</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-01~04</span>
          </div>
        </div>
        <div class="card-body">
          <b>①基准换新（6/1生效）：</b>12家基金195只产品基准调整集中落地，严禁风格漂移。<br>
          <b>②货基渠道整治：</b>货币基金销售渠道管理新规同步推进，规范第三方平台持续营销行为。<br>
          <b>③QDII额度收紧（6月初）：</b>全市场360只QDII近半数限购，20+只场内QDII ETF发溢价风险提示，富国纳斯达克100等热门产品单日限额1万元。<br>
          <b>④债券ETF制度利好（5/27公告）：</b>沪深交易所将债券ETF纳入协议回购质押券范围（深交所10/26施行），8000亿债券ETF市场再获流动性支持。<br>
          <b>影响：</b>多项监管规定集中落地→公募行业进入"高合规+高透明"新周期。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260601A055PS00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·晨报</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1866352514306240160&wfr=spider&for=pc" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·债券ETF</span></a>
          <span class="impact-tag high">多规并行：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① QDII限购→关注腾安代销QDII产品申购额度调整情况，及时更新客户提示；<br>
            ② 货基渠道整治→确认腾安货基营销合规（禁止收益暗示、禁止变相承诺收益）；<br>
            ③ 基准换新→检查超额收益展示逻辑是否已同步更新。
          </div>
        </div>
      </div>'''

content = content.replace(old_s2_card4, '')

# ============================================================
# 8. S6 市场行情速览 更新
# ============================================================
old_s6 = '''    <div class="card p3">
      <div class="card-top">
        <div class="card-title">上周收盘回顾（6/9-13）+ 下周关注（6/16-22）：美联储议息·端午休市·A股开盘前瞻</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 上周收盘（6/13周五）：</b>沪指4031点(+1.12%)，全周成交<b>13.95万亿</b>创近5周新低。两融本周净卖出逾<b>330亿元</b>。电子/电力设备遭净卖出，有色金属/基础化工获主力净流入。<br><br>
            <b>📊 端午假期效应：</b>6/19-21端午休市，节前避险情绪已升温。历史规律显示端午后A股上涨概率偏高，但需关注假期期间<b>6/18美联储议息结果</b>带来的海外市场波动风险。<br><br>
            <b>📊 明日开盘前瞻（6/16周一）：</b>关注美联储议息前市场情绪、科技板块能否延续强势、成交能否放量突破13.95万亿低点。
          </div>
          <div>
            <b>📊 下周关键事件（6/16-6/22）：</b><br>
            ▪ <b>6/16-17 美联储议息会议</b>→6/18公布结果<br>
            ▪ 6/19-21 端午节休市·A股港股通暂停<br>
            ▪ 6/22 开市后关注假期期间海外市场变化<br>
            ▪ 欧央行已重启加息→美联储若按兵不动将加剧政策分化<br><br>
            <b>📊 对基金行业影响：</b><br>
            ▪ 美联储议息→QDII纳斯达克/欧元债产品波动<br>
            ▪ 端午休市→节前避险情绪压制权益基金销售<br>
            ▪ 缩量震荡→固收+产品性价比凸显
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">westock-data·上周收盘</span>
        <span class="source-tag">同花顺iFind MCP</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>'''

new_s6 = '''    <div class="card p3">
      <div class="card-top">
        <div class="card-title">今日行情（6/16上午）+ 近期回顾：科技强势创业板指+2.05%·建材领涨·端午前最后交易周</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 今日上午收盘（6/16）：</b>上证指数涨<b>0.06%</b>，深证成指涨<b>1.17%</b>，创业板指涨<b>2.05%</b>，科创综指涨1.20%。主要行业板块：建筑材料领涨（盘中涨幅超4%），国际复材盘中大涨超14%。科技板块延续强势，但整体表现较为温和。<br><br>
            <b>📊 昨日收盘（6/15）：</b>上证指数<b>4096.47点(+1.61%)</b>，全市场普涨，31个申万一级行业多数收涨，科技板块"一枝独秀"的分化行情有所收敛。非科技板块（机械设备、基础化工、电力设备）获机构密集调研。<br><br>
            <b>📊 本周关键：</b>6/19-21端午休市，本周为节前最后交易周，避险情绪升温但科技成长风格仍占优。
          </div>
          <div>
            <b>📊 本周关键事件（6/16-6/21）：</b><br>
            ▪ <b>6/16-17 美联储议息会议</b>→6/18公布结果（欧央行已重启加息）<br>
            ▪ 6/19-21 端午节休市·A股港股通暂停<br>
            ▪ 6/16 多只QDII ETF停牌后复牌（10:30）→关注溢价回落风险<br><br>
            <b>📊 对基金行业影响：</b><br>
            ▪ 科技强势→科技成长类ETF和主动权益基金持续受益<br>
            ▪ 美联储议息→QDII产品波动，关注点阵图变化<br>
            ▪ 端午休市→节前权益基金销售承压，固收+性价比凸显<br>
            ▪ QDII ETF高溢价→监管可能介入规范，关注后续政策
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">web_search·今日行情</span>
        <span class="source-tag">同花顺iFind MCP</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>'''

content = content.replace(old_s6, new_s6)

# ============================================================
# 9. S7 时间线 更新
#    删除超期条目（T-14=06-02，需删除06-02及更早）
#    当前S7有11条：06-13/06-12/06-11/06-10/06-09/06-08/06-06/06-05/06-04/06-03/06-02/06-01
#    需删除：06-02（腾讯暴涨）、06-01（宇树IPO）— 已超14天
#    新增：06-16（QDII ETF停牌）、06-15（公募新规落地）
# ============================================================

# 删除06-02时间线条目
old_tl_0602 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-02（腾讯暴涨10.46%创2021来最大涨幅·恒生科技+4.72%·AI Agent突破）</div>
          <div class="timeline-title">腾讯控股+10.46%（AI Agent开发平台+云降价97.5%）/ 恒生科技+4.72% / A股创业板+2.66%深V修复</div>
          <div class="timeline-desc">腾讯单日暴涨10%创4年来最大涨幅，AI Agent开发平台+云降价97.5%双重催化。恒生科技大涨，美团+9%。A股探底回升，MLCC/CPO/机器人爆发。成交2.79万亿。成交额前20科技股全部收红。</div>
        </div>
      </div>'''

content = content.replace(old_tl_0602, '')

# 删除06-01时间线条目
old_tl_0601 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-01（宇树科技IPO过会·195只基金基准换新生效·指数样本6/12调整公告）</div>
          <div class="timeline-title">宇树科技科创板IPO过会（拟募42亿·人形机器人第一股）/ 195只基金业绩基准正式换新 / 沪深300等指数样本6/12调整</div>
          <div class="timeline-desc">宇树科技IPO过会，冲刺科创板"具身智能第一股"，受理仅73天。195只基金总规模近4000亿业绩基准正式调整生效。沪深300换19只/中证500换50只样本6/12收盘后生效，千亿被动资金调仓。</div>
        </div>
      </div>'''

content = content.replace(old_tl_0601, '')

# 在时间线开头（第一个timeline-item之前）插入新条目
new_tl_items = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-16（多只QDII科技ETF停牌·6月新基发行创同期新高·A股科技延续强势）</div>
          <div class="timeline-title">纳指ETF易方达/国泰/景顺+创业板ETF富国因高溢价6/16停牌（10:30复牌）/ 6月前11天114只新基发行创历史同期新高 / A股今日上午创业板指+2.05%</div>
          <div class="timeline-desc">多只QDII科技ETF因二级市场交易价格明显高于IOPV（溢价率最高超22%）于6/16开市起停牌，10:30起复牌，停牌期间赎回业务照常办理。6月前11天114只新基发行创历史同期新高，上半年主动权益基金发行数量同比翻倍。A股今日上午科技延续强势，创业板指+2.05%，建筑材料板块领涨。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-15（多项公募新规落地·A股普涨科技收敛·中期分红热潮来袭）</div>
          <div class="timeline-title">主题投资风格管理指引+适当性细则修订+公私兼任禁令三文同落 / A股沪指4096(+1.61%)普涨 / 中期分红热潮数百家上市公司</div>
          <div class="timeline-desc">多项公募基金新规同日公布（新华社报道）：主题投资风格管理指引（12/1施行，12个月过渡期）将风格漂移软约束转为硬约束；适当性细则修订加强65周岁以上高风险基金销售管理；公私兼任禁令防范利益冲突。A股今日普涨，科技板块一枝独秀行情收敛，非科技板块获机构密集调研。中期分红热潮来袭，数百家上市公司发布中期分红预案。</div>
        </div>
      </div>
'''

# 在S7的card div内、第一个timeline-item之前插入新条目
s7_insert_marker = '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-13'
content = content.replace(s7_insert_marker, new_tl_items + '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-13')

# ============================================================
# 10. S8 待办跟踪 更新
# ============================================================
old_s8_title = '今日待办建议清单（6月15日周日更新）'
new_s8_title = '今日待办建议清单（6月16日周一更新）'
content = content.replace(old_s8_title, new_s8_title)

# 更新S8表格内容
old_s8_table = '''          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">证监会三年行动计划（2026-2028）落地→研究对腾安代销业务模式的影响，提前规划收费模式转型</td>
            <td style="padding:10px 12px;color:var(--gray-500);">证监会6/13发布</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">适当性系统改造立即启动：中基协要求6个月内完成→确保12月12日前完成改造</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/12细则</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月20日前立项</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">美联储6/18议息结果应对：欧央行已重启加息→准备QDII产品客户沟通材料，关注点阵图变化</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/16-17会议·6/18公布</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月17日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">跨境券商客户承接跟进：富途/老虎禁令已执行→制定存量客户迁移承接方案，主动营销腾安QDII/港股通</td>
            <td style="padding:10px 12px;color:var(--gray-500);">跨境禁令6/12执行</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月20日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">端午节假期营销安排：6/19-21休市→节前避险情绪升温，节后上涨概率偏高，制定假期前后营销策略</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/19-21端午休市</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月18日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">央行互换便利+再贷款工具加码→评估对腾安代销ETF流动性和权益基金发行的政策支持效果</td>
            <td style="padding:10px 12px;color:var(--gray-500);">央行6/13双工具加码</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">ESG基金产品线布局评估：中基协可持续投资指引即日实施→评估腾安ESG主题基金覆盖是否充分</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/12指引</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月底前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">基金清盘潮排查：年内124只基金清盘→排查腾安代销产品中是否有清盘风险基金，做好客户预警</td>
            <td style="padding:10px 12px;color:var(--gray-500);">清盘同比+16%</td>
            <td style="padding:10px 12px;color:var(--primary);font-weight:600;">本周</td>
          </tr>
          <tr>
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">国办私募指导意见研读：23万亿私募全链条监管升级→评估高净值客户资金转公募机会</td>
            <td style="padding:10px 12px;color:var(--gray-500);">国办函〔2026〕54号</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月中旬</td>
          </tr>'''

new_s8_table = '''          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">主题风格管理指引落地→立即排查腾安代销主题基金风格披露合规性，提前12个月准备（12/1施行）</td>
            <td style="padding:10px 12px;color:var(--gray-500);">06-15新规·12/1施行</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">QDII科技ETF高溢价风险应对：多只ETF停牌→排查腾安代销QDII产品溢价情况，及时发布风险提示</td>
            <td style="padding:10px 12px;color:var(--gray-500);">06-16 ETF集体停牌</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">今日完成</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">适当性系统改造项目立项：中基协要求6个月内完成→确保12月12日前完成改造</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/12细则</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月20日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">美联储6/18议息结果应对：欧央行已重启加息→准备QDII产品客户沟通材料，关注点阵图变化</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/16-17会议·6/18公布</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月17日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">端午节假期营销安排：6/19-21休市→节前避险情绪升温，制定假期前后营销策略和休市提醒</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/19-21端午休市</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月18日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">6月新基发行翻倍→梳理腾安代销新基金清单，制定营销推广计划，捕捉发行热潮红利</td>
            <td style="padding:10px 12px;color:var(--gray-500);">上半年发行同比翻倍</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">ESG基金产品线布局评估：中基协可持续投资指引即日实施→评估腾安ESG主题基金覆盖是否充分</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/12指引</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月底前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">基金清盘潮排查：年内124只基金清盘→排查腾安代销产品中是否有清盘风险基金，做好客户预警</td>
            <td style="padding:10px 12px;color:var(--gray-500);">清盘同比+16%</td>
            <td style="padding:10px 12px;color:var(--primary);font-weight:600;">本周</td>
          </tr>
          <tr>
            <td style="padding:10px 12px;"><span class="priority-tag normal">P2</span></td>
            <td style="padding:10px 12px;font-weight:600;">适当性细则修订跟进：65周岁以上客户高风险基金销售流程升级→评估腾安现有流程是否符合新要求</td>
            <td style="padding:10px 12px;color:var(--gray-500);">06-15适当性修订</td>
            <td style="padding:10px 12px;color:var(--primary);font-weight:600;">6月底前</td>
          </tr>'''

content = content.replace(old_s8_table, new_s8_table)

# ============================================================
# 11. Footer 更新
# ============================================================
old_footer = '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月15日（周日例行更新） · 信息来源：证券时报、中基协、同花顺财经、新浪财经、证监会、上交所、深交所、东方财富、财联社、央视网、上海证券报、中国证券报、新华网、中国经济网、腾讯新闻、欧央行、太空日报等公开渠道'
new_footer = '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月16日（今日自动更新） · 信息来源：新华网、人民财讯、东方财富、同花顺财经、中国证券报、百家号、金融界、证监会、中基协、证券时报、新浪财经等公开渠道'
content = content.replace(old_footer, new_footer)

# ============================================================
# 12. 更新 HTML 注释中的日期标记
# ============================================================
content = re.sub(r'<!-- daily-update: 2026-06-\d+ -->', '<!-- daily-update: 2026-06-16 -->', content)

# 写入文件
with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ index.html 更新完成！")
print(f"文件长度: {len(content)} 字符")

# 验证关键更新
checks = [
    ('数据区间', '2026.06.02 — 2026.06.16'),
    ('S0标题', '今日焦点（6月16日·周一'),
    ('S0卡片1日期', '06-15'),
    ('S0卡片2日期', '06-16'),
    ('S0卡片3日期', '06-16'),
    ('S6行情', '今日行情（6/16上午）'),
    ('S7时间线06-16', '2026-06-16（多只QDII'),
    ('S7时间线06-15', '2026-06-15（多项公募新规'),
    ('S8日期', '6月16日周一更新'),
    ('Footer日期', '2026年6月16日'),
]
print("\n🔍 验证关键更新：")
for name, keyword in checks:
    found = keyword in content
    print(f"  {'✅' if found else '❌'} {name}: {'找到' if found else '未找到'} '{keyword}'")
