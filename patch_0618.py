#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补位更新 index.html 到 2026-06-18 版本"""

with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========== 1. 更新 Header 日期区间 ==========
old_header = '数据区间：2026.06.03 — 2026.06.17（今日自动更新）'
new_header = '数据区间：2026.06.04 — 2026.06.18（今日自动更新）'
content = content.replace(old_header, new_header)

# ========== 2. 更新 Section 0 标题 ==========
old_s0_title = '今日焦点（6月17日·周二·陆家嘴论坛开幕·公募自购75亿·QDII溢价后续）'
new_s0_title = '今日焦点（6月18日·周三·美联储议息结果落地·陆家嘴论坛收官·沪深300ETF净流出137亿）'
content = content.replace(old_s0_title, new_s0_title)

# ========== 3. 更新 S0 第1张卡片（陆家嘴论坛→美联储议息） ==========
old_card1 = '''        <div class="card-title">🔴 2026陆家嘴论坛今日开幕！央行/证监会/金融监管总局"一把手"集体发声，上海国际金融中心政策礼包落地</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>今日开幕：</b>6月17日上午，由央行、金融监管总局、证监会和上海市政府共同主办的2026陆家嘴论坛在沪正式开幕，主题为"全球治理倡议下的金融发展与合作：新愿景、新挑战和新机遇"。金融监管总局局长丁向群、上海市市长龚正担任共同轮值主席，70余名中外嘉宾参会。<br>
          <b>政策礼包：</b>各监管部门将在论坛期间集中通报上海国际金融中心建设最新进展与下一步规划，市场预期将发布跨境金融、数字人民币、对外开放等相关政策礼包。历届陆家嘴论坛曾多次发布重大金融政策（2019年科创板开板即在一届论坛开幕式宣布）。<br>
          <b>对基金行业影响：</b>①上海国际金融中心政策礼包→跨境投资便利化可能提速，QDII额度扩容预期升温；②数字人民币国际运营中心首批26家金融机构签约→数字人民币在基金申购场景的应用可能加速；③金融监管高层集体发声→公募行业相关政策信号值得高度关注。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1868206338493938890" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·今日开幕</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1868207585035009624" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">大河财立方</span></a>
          <span class="impact-tag high">政策信号：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 密切关注论坛期间监管高层发言→重点捕捉公募行业、代销业务、跨境投资相关政策信号；<br>
            ② 上海国际金融中心政策礼包→评估跨境投资便利化对腾安QDII基金代销的潜在利好；<br>
            ③ 数字人民币应用场景拓展→关注数字人民币在基金申购/赎回中的落地进展，提前研究接入方案。
          </div>
        </div>'''

new_card1 = '''        <div class="card-title">🔴 美联储6月议息落地！沃什首秀维持利率不变但点阵图转鹰，年底利率中值升至3.75%-4.0%</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-18</span>
          </div>
        </div>
        <div class="card-body">
          <b>议息结果（北京时间6/18 02:00）：</b>美联储宣布维持联邦基金利率目标区间在<b>3.50%-3.75%不变</b>，符合市场预期。新任美联储主席沃什举行上任后首次新闻发布会。<br>
          <b>点阵图转鹰：</b>最新点阵图中值显示，年底利率预期升至<b>3.75%-4.0%</b>（暗示年内可能加息一次），较3月预期（年底中值3.4%，降息一次）大幅转鹰。2027年底利率中值3.6%，降息窗口显著延后，高盛预判最早2027年6月才可能降息。<br>
          <b>经济预测调整（滞胀特征）：</b>2026全年GDP增速预测从2.4%下调至2.2%（经济放缓），核心PCE通胀上调（通胀居高），失业率维持低位（就业韧性）。美联储陷入"经济增长放缓+通胀居高"的滞胀困境。<br>
          <b>对基金行业影响：</b>①QDII美股产品波动风险上升→加息预期升温压制科技股估值；②全球债券收益率上行→国内QDII美元债/美债基金面临净值压力；③欧央行已加息25bp+美联储转鹰→全球央行政策分化加剧，跨境资产配置难度上升。
        </div>
        <div class="card-footer">
          <a href="https://caifuhao.eastmoney.com/news/20260618085447365963720" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·点阵图</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1868233595962137194" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·资产配置</span></a>
          <span class="impact-tag high">全球央行：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 美联储转鹰→QDII纳斯达克100产品客户可能集中咨询，提前准备解释话术；<br>
            ② 全球央行政策分化→关注美元债QDII产品净值波动，做好客户陪伴；<br>
            ③ 滞胀预期→固收+产品再平衡压力上升，关注持有美债的QDII产品。
          </div>
        </div>'''

content = content.replace(old_card1, new_card1)

# ========== 4. 更新 S0 第2张卡片（公募自购→陆家嘴论坛政策礼包） ==========
old_card2 = '''        <div class="card-title">🟡 公募自购今年以来已达3341次，净申购75.99亿元！权益基金占比25.63%创近期新高</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>最新数据（截至6月16日）：</b>公募排排网数据显示，今年以来公募基金行业已实施自购<b>3341次</b>，累计净申购金额达<b>75.99亿元</b>，较2025年同期的69.90亿元增长<b>8.71%</b>。<br>
          <b>权益基金成核心方向：</b>今年以来公募申购旗下权益基金达<b>287次</b>，净申购金额达<b>19.48亿元</b>，占到总额的<b>25.63%</b>，占比较前期明显提升，反映基金公司对权益市场的看好态度。<br>
          <b>行业信号：</b>公募自购是机构对市场底部区域的重要信心信号。今年以来自购频次和金额双升，叠加新基金发行"权益回暖"特征，显示公募行业对后市的判断趋于乐观。上半年主动权益基金发行数量同比翻倍，与自购数据相互印证。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3964003.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">机构信心：中高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 公募自购升温→可作为腾安对客沟通的信心参考指标，在行情震荡时用作市场底部区域判断依据；<br>
            ② 权益基金自购占比提升→与"注重权益投资"监管定调相呼应，腾安可加大权益类产品推荐权重。
          </div>
        </div>'''

new_card2 = '''        <div class="card-title">🔴 陆家嘴论坛政策礼包落地！央行6项新政+证监会支持主动ETF+吴清定调中小基金差异化发展</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>央行6项新政（潘功胜）：</b>完善短端利率调控机制、创设境外央行回购工具、在上海自贸区开展离岸人民币外汇交易试点、研究设立特定情景非银流动性支持工具等。<br>
          <b>证监会（吴清）：</b>表示将"进一步推动健全跨境监管协调机制，开正门、堵偏门"，支持中小基金公司差异化发展，缓解行业"马太效应"加剧问题。证监会同时宣布支持在沪深交易所推出<b>主动管理ETF</b>，将填补场内主动权益产品空白。<br>
          <b>深交所业务指引：</b>6月17日发布主动管理ETF业务指引，对产品准入、投资运作、信息披露、持续监督等各环节作出规定，为主动ETF落地铺路。<br>
          <b>对基金行业影响：</b>主动ETF落地→场内投资新工具即将问世，券商和头部公募率先受益；中小基金差异化发展定调→监管有意缓解头部集中趋势，中小机构业务创新空间可能扩大。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1868227272984806169" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·full cover</span></a>
          <a href="https://www.nbd.com.cn/articles/2026-06-17/4429172.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经·主动ETF</span></a>
          <span class="impact-tag high">政策礼包：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 主动ETF落地→关注沪深交易所主动ETF产品推出进度，评估是否纳入腾安货架；<br>
            ② 中小基金差异化发展→关注监管对中小机构创新业务的扶持政策，寻找合作机会；<br>
            ③ 跨境监管协调→"开正门、堵偏门"定调，跨境代销合规要求可能进一步收紧。
          </div>
        </div>'''

content = content.replace(old_card2, new_card2)

# ========== 5. 更新 S0 第3张卡片（QDII溢价→6/17 A股科创50暴涨） ==========
old_card3 = '''        <div class="card-title">🟡 QDII科技ETF高溢价警示：纳指ETF易方达等6/16复牌后溢价回落，监管关注持续</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>复牌后续：</b>6月16日10:30起，纳指ETF易方达(159696)、纳指ETF国泰(513100)、纳指科技ETF景顺(159807)、创业板ETF富国(159971)等集体复牌。复牌后高溢价有所回落，但部分产品溢价率仍高于理性区间，需持续关注。<br>
          <b>监管态度：</b>深交所已对纳指ETF广发等溢价严重的基金发出关注函，要求基金公司说明溢价原因及风险提示措施。监管对QDII ETF异常溢价的关注度明显上升，后续可能出台规范措施。<br>
          <b>市场背景：</b>QDII科技ETF高溢价反映境内投资者对美股科技板块的追捧情绪，但溢价率超10%已明显偏离理性区间。美联储议息结果（6/18公布）将影响美股走势，进而传导至QDII产品溢价水平。<br>
          <b>风险警示：</b>高溢价QDII ETF存在溢价回落导致的价格下跌风险，投资者需谨慎。腾安代销的相关产品需做好风险提示和客户解释准备。
        </div>
        <div class="card-footer">
          <a href="https://www.egsea.com/news/detail/2302695.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯·纳指ETF停牌</span></a>
          <span class="impact-tag medium">溢价风险：持续</span>
        </div>
      </div>

    </div>
  </div>'''

new_card3 = '''        <div class="card-title">🟡 6/17 A股科创50暴涨超4%！但沪深300ETF净流出137亿，机构资金高位兑现</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>6/17收盘：</b>A股低开后震荡走高，沪指<b>4108.57点(+0.40%)</b>，深成指<b>15775.03点(+1.31%)</b>，创业板指<b>4120.18点(+1.56%)</b>，科创50指数<b>涨超4%</b>，芯片股午后大幅走强（兆易创新涨停+10%，普冉股份+20%涨停）。<br>
          <b>资金背离信号：</b>6月17日，4只沪深300ETF合计<b>净流出超137亿元</b>（前一交易日净流出超100亿元），机构资金在指数上涨背景下高位兑现，显示机构对后市看法分歧加大。<br>
          <b>端午前效应：</b>6月19-21日端午休市，节前避险情绪升温，机构选择落袋为安。历史规律显示端午假期后A股上涨概率偏高，但需关注节日期间海外市场波动风险（特别是美联储议息结果）。<br>
          <b>对基金行业影响：</b>芯片/科创基金单日大涨→科技主题基金净值大幅回升，客户关注度上升；但机构资金净流出→指数基金申赎波动加大，代销平台需做好流动性管理。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202606173774635827.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·资金流向</span></a>
          <a href="https://www.nbd.com.cn/articles/2026-06-18/4430113.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经·ETF净流出</span></a>
          <span class="impact-tag high">资金背离：高</span>
        </div>
      </div>

    </div>
  </div>'''

content = content.replace(old_card3, new_card3)

# ========== 6. 更新 Stats Bar ==========
old_stats = '''  <div class="stat-card">
    <div class="stat-number">陆家嘴论坛开幕</div>
    <div class="stat-label">6/17央行/证监会/金融监管总局"一把手"集体发声·上海国际金融中心政策礼包落地</div>
    <div class="stat-change up">▲ 70余名中外嘉宾参会·跨境金融/数字人民币/对外开放政策礼包</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">公募自购75.99亿</div>
    <div class="stat-label">今年以来公募申购旗下基金达3341次·权益基金占比25.63%·机构信心持续升温</div>
    <div class="stat-change up">▲ 自购金额同比+8.71%·权益方向成核心·与发行翻倍相互印证</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4094·温和涨</div>
    <div class="stat-label">今日上午沪指4094(+0.05%)·深成指+0.77%·创业板指+0.30%·科技风格延续</div>
    <div class="stat-change up">▲ 今日陆家嘴论坛开幕·明日美联储议息结果公布·端午前最后交易周</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">美联储议息倒计时</div>
    <div class="stat-label">6/17-18议息会议·6/18公布结果·欧央行已重启加息25bp·全球央行政策分化加剧</div>
    <div class="stat-change up">▲ 点阵图是否反映"降息次数减少"·QDII产品波动风险上升·关注明日结果</div>
  </div>'''

new_stats = '''  <div class="stat-card">
    <div class="stat-number">美联储转鹰·沃什首秀</div>
    <div class="stat-label">6/18议息维持不变但点阵图中值升至3.75%-4.0%·暗示年内可能加息一次·2027年降息窗口延后</div>
    <div class="stat-change up">▲ 沃什首秀·滞胀困境（增长放缓+通胀居高）·QDII产品波动风险上升</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">陆家嘴论坛收官</div>
    <div class="stat-label">央行6项新政+证监会支持主动ETF+吴清定调中小基金差异化发展·主动管理ETF业务指引落地</div>
    <div class="stat-change up">▲ 上海国际金融中心政策礼包·跨境监管"开正门堵偏门"·公募行业政策信号密集</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4108·科创+4%</div>
    <div class="stat-label">6/17收盘沪指4108(+0.40%)·科创50涨超4%·芯片股午后大幅走强·沪深300ETF净流出137亿</div>
    <div class="stat-change up">▲ 科技风格延续但机构高位兑现·端午前最后交易周·关注海外市场波动</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">端午休市倒计时</div>
    <div class="stat-label">6/19-21端午休市·节前避险情绪升温·A股缩量震荡·机构资金净流出·节后上涨概率偏高</div>
    <div class="stat-change up">▲ 节日期间海外市场波动风险·美联储转鹰传导·QDII产品需重点关注</div>
  </div>'''

content = content.replace(old_stats, new_stats)

# ========== 7. 更新 S6 市场行情 ==========
old_s6 = '''    <div class="card-title">今日行情（6/17上午10:13）+ 近期回顾：陆家嘴论坛开幕·科技风格延续·美联储议息前屏息</div>'''
new_s6 = '''    <div class="card-title">今日行情（6/18上午10:30）+ 美联储议息落地·陆家嘴论坛收官·端午前最后交易周</div>'''
content = content.replace(old_s6, new_s6)

old_s6_body = '''        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 今日上午盘中（6/17 10:13）：</b>上证指数<b>4094.14点(+0.05%)</b>，深证成指<b>15795.99点(+0.77%)</b>，创业板指<b>4115.44点(+0.30%)</b>。科技风格延续但涨幅温和，市场等待今日陆家嘴论坛政策信号。成交金额：沪市5073亿元，深市6467亿元。<br><br>
            <b>📊 昨日收盘（6/16）：</b>上证指数<b>4091.89点(-0.11%)</b>，深成指+0.93%，创业板指+1.72%。科技板块延续强势，但沪指小幅回调，市场呈现分化格局。<br><br>
            <b>📊 本周关键：</b>今日陆家嘴论坛开幕（央行/证监会/金融监管总局一把手集体发声），明日6/18美联储议息结果公布。6/19-21端午休市，本周为节前最后交易周。
          </div>
          <div>
            <b>📊 本周关键事件（6/17-6/21）：</b><br>
            ▪ <b>6/17 陆家嘴论坛开幕</b>→央行/证监会/金融监管总局政策信号（今日）<br>
            ▪ <b>6/18 美联储议息结果公布</b>→欧央行已重启加息，关注点阵图变化<br>
            ▪ 6/19-21 端午节休市·A股港股通暂停<br><br>
            <b>📊 对基金行业影响：</b><br>
            ▪ 陆家嘴论坛政策礼包→跨境金融/数字人民币/对外开放，关注公募相关信号<br>
            ▪ 美联储议息→QDII产品波动，欧央行加息加剧全球央行政策分化<br>
            ▪ 端午休市→节前权益基金销售承压，固收+性价比凸显<br>
            ▪ 科技风格延续→科技成长类ETF和主动权益基金持续受益
          </div>
        </div>'''

new_s6_body = '''        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 昨日收盘（6/17）：</b>上证指数<b>4108.57点(+0.40%)</b>，深证成指<b>15775.03点(+1.31%)</b>，创业板指<b>4120.18点(+1.56%)</b>，科创50指数<b>涨超4%</b>。芯片股午后大幅走强，兆易创新涨停+10%。<br><br>
            <b>📊 今日上午盘中（6/18 10:30）：</b>市场关注美联储议息落地后的A股反应，科创/半导体板块能否延续强势。4只沪深300ETF昨日净流出137亿元，机构高位兑现信号明显。<br><br>
            <b>📊 端午前效应：</b>明日（6/19）起端午休市3天，今日为节前最后交易日。历史规律显示端午后A股上涨概率偏高，但需关注节日期间海外市场波动（美联储转鹰）。
          </div>
          <div>
            <b>📊 美联储议息结果（6/18 02:00落地）：</b><br>
            ▪ 维持利率3.50%-3.75%不变，符合预期<br>
            ▪ 点阵图中值升至3.75%-4.0%，暗示可能加息一次<br>
            ▪ 2026 GDP增速下调至2.2%，核心PCE通胀上调（滞胀）<br>
            ▪ 沃什首秀，降息窗口延后至2027年<br><br>
            <b>📊 对基金行业影响：</b><br>
            ▪ 美联储转鹰→QDII美股产品波动风险上升<br>
            ▪ 全球债券收益率上行→QDII美元债基金承压<br>
            ▪ 端午休市→节前申赎波动，节后关注补涨机会
          </div>
        </div>'''

content = content.replace(old_s6_body, new_s6_body)

# ========== 8. 更新 S6 card-footer ==========
old_s6_footer = '''        <span class="source-tag">NeoData·今日行情10:13</span>
        <span class="source-tag">web_search·陆家嘴论坛</span>'''
new_s6_footer = '''        <span class="source-tag">NeoData·6/17收盘</span>
        <span class="source-tag">美联储议息·6/18落地</span>'''
content = content.replace(old_s6_footer, new_s6_footer)

# ========== 9. 更新 S7 时间线（删除06-04及更早，新增06-18，保留06-05~06-17） ==========
# 删除 06-04 条目（易方达ETF登顶）
old_tl_0604 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-04（A股缩量回调·央行国债净投放500亿·易方达ETF登顶第一）</div>
          <div class="timeline-title">A股沪指4057.78(-0.64%)缩量回调 / 央行5月国债净投放500亿 / 易方达ETF规模6185亿超越华夏登顶</div>
          <div class="timeline-desc">A股缩量回调，半导体/AI方向承压。央行5月公开市场国债买卖净投放500亿，延续宽松基调。易方达基金旗下ETF规模达6185.19亿元，超越华夏基金登顶全市场ETF规模第一，差距仅19亿元，竞争白热化。</div>
        </div>
      </div>'''
content = content.replace(old_tl_0604, '')

# 删除 06-05 条目（国办私募顶层设计）
old_tl_0605 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-05（国办私募顶层设计落地·中证金牛被集体解约·美国非农翻倍）</div>
          <div class="timeline-title">国办23万亿私募顶层设计落地 / 中证金牛被招商/嘉实等集体解约 / 美国5月非农17.2万翻倍→加息预期升温</div>
          <div class="timeline-desc">国办函〔2026〕54号全文发布，私募基金行业首份国务院层面顶层设计文件。中证金牛被多家公募集体终止合作，第三方代销出清加速。美国5月非农17.2万翻倍超预期→加息预期飙升，全球市场承压。</div>
        </div>
      </div>'''
content = content.replace(old_tl_0605, '')

# 新增 06-18 时间线条目（插入到最前面，在06-17条目之前）
new_tl_0618 = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-18（美联储议息落地·沃什首秀点阵图转鹰·A股端午前最后交易·沪深300ETF净流出137亿）</div>
          <div class="timeline-title">美联储维持利率3.50%-3.75%不变但点阵图中值升至3.75%-4.0% / 沃什首秀转鹰暗示可能加息 / A股端午前最后交易日·科创50昨日+4% / 沪深300ETF净流出137亿</div>
          <div class="timeline-desc">美联储6月议息结果北京时间今日02:00落地：维持利率不变符合预期，但点阵图中值大幅转鹰（年底利率预期3.75%-4.0%，暗示可能加息一次），新任主席沃什举行首秀新闻发布会。A股今日为端午前最后交易日，昨日科创50涨超4%，但4只沪深300ETF净流出137亿元，机构高位兑现。欧美央行政策分化加剧，全球资产配置难度上升。</div>
        </div>
      </div>
'''

# 在 06-17 条目之前插入 06-18
old_tl_0617 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-17（陆家嘴论坛开幕·央行/证监会/金融监管总局一把手集体发声·A股温和上涨）</div>'''

new_tl_0617 = new_tl_0618 + '      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-17（陆家嘴论坛开幕·央行/证监会/金融监管总局一把手集体发声·A股温和上涨）</div>'

content = content.replace(old_tl_0617, new_tl_0617)

# ========== 10. 更新 Footer ==========
old_footer = '数据更新时间：2026年6月17日 10:30 · 近两周核心资讯（06-03 — 06-17）· <a href="https://kelvinye2020-arch.github.io/fund-briefing/" target="_blank" style="color:var(--primary);text-decoration:none;">基金行业资讯看板</a> 由 小A 自动更新'
new_footer = '数据更新时间：2026年6月18日 10:30 · 近两周核心资讯（06-04 — 06-18）· <a href="https://kelvinye2020-arch.github.io/fund-briefing/" target="_blank" style="color:var(--primary);text-decoration:none;">基金行业资讯看板</a> 由 小A 自动更新'
content = content.replace(old_footer, new_footer)

# ========== 11. 更新 daily-update 标记 ==========
content = content.replace('<!-- daily-update: 2026-06-16 -->', '<!-- daily-update: 2026-06-18 -->')

# 写入文件
with open('c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("补位更新完成！所有替换已执行。")
print("检查：")
print("1. Header日期区间：", '06.04 — 2026.06.18' in content)
print("2. S0卡片1（美联储）：", '美联储6月议息落地' in content)
print("3. S0卡片2（陆家嘴）：", '陆家嘴论坛政策礼包落地' in content)
print("4. S0卡片3（科创50）：", '科创50暴涨超4%' in content)
print("5. Stats Bar：", '美联储转鹰' in content)
print("6. S6市场行情：", '昨日收盘（6/17）' in content)
print("7. S7时间线06-18：", '2026-06-18（美联储议息落地' in content)
print("8. S7时间线06-04已删：", '2026-06-04（A股缩量回调' not in content)
print("9. Footer：", '2026年6月18日 10:30' in content)
print("10. daily-update标记：", 'daily-update: 2026-06-18' in content)
