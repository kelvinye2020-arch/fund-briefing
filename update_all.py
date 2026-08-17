# -*- coding: utf-8 -*-
"""批量更新基金看板 index.html 的剩余模块：S2卡片body、S6、S7、S8、footer"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 1. 更新S2第一个卡片的body/footer/action-box（标题已更新为跨境券商禁令今日执行）=====
# 找到该卡片的位置，替换从 card-meta 到 card-footer 结束的部分
old_card_1 = '''        <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">05-22~25</span>
          </div>
        </div>
        <div class="card-body">
          <b>5月22日重磅落地：</b>证监会等八部门联合印发《综合整治非法跨境证券期货基金经营活动实施方案》，设置<b>2年集中整治期</b>，全面取缔境外机构非法跨境展业。同日证监会对富途控股拟罚没<b>18.5亿元</b>、老虎证券<b>4.1亿元</b>，合计超22亿元。<br>
          <b>整治措施：</b>期内仅允许存量账户单向卖出并转出资金，全链条穿透监管覆盖营销招揽、开户、交易处理全流程。长桥证券亦被同步处罚。<br>
          <b>行业影响：</b>非法跨境渠道被清退→境外投资需求向港股通、QDII、跨境理财通等合规渠道转移，利好持牌代销机构。
        </div>
        <div class="card-footer">
          <a href="http://www.ce.cn/xwzx/gnsez/gdxw/202605/t20260525_2986368.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <a href="https://news.qq.com/rain/a/20260524A08BB700" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中信建投点评</span></a>
          <span class="impact-tag high">跨境监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跨境渠道清退→关注QDII产品需求激增，提前准备额度和营销话术；<br>
            ② 港股通/跨境理财通合规渠道利好→评估腾安相关产品推广机会。
          </div>
        </div>'''

new_card_1 = '''        <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-12</span>
          </div>
        </div>
        <div class="card-body">
          <b>今日正式执行：</b>6月12日起，富途控股、老虎国际、长桥证券三家头部跨境互联网券商对<b>中国大陆境内账户</b>的服务调整正式生效。核心限制：<b>暂停股票等所有品种的新开仓、加仓交易</b>，仅支持卖出、平仓操作；暂停资金转入，转出功能保持正常。<br>
          <b>政策依据：</b>5月22日证监会等八部门联合印发《综合整治非法跨境证券期货基金经营活动实施方案》，设置<b>2年集中整治期</b>，全面取缔境外机构非法跨境展业。富途被罚没18.5亿元、老虎4.1亿元，合计超22亿元。<br>
          <b>艾德证券6/15跟进：</b>艾德证券将于6月15日起暂停向现有受影响客户于中国内地境内提供任何产品之买入及存入资金之服务，跨境券商整治全面落地。<br>
          <b>行业影响：</b>非法跨境渠道被清退→境外投资需求向<b>港股通、QDII、跨境理财通</b>等合规渠道转移，利好持牌代销机构。腾安作为腾讯系合规平台，有望承接从跨境券商流出的客户资源。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867065335216314660" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·腾讯新闻</span></a>
          <a href="http://finance.ce.cn/stock/gsgdbd/202606/t20260603_3008090.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网</span></a>
          <span class="impact-tag high">跨境监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跨境券商禁令生效→境外投资需求向合规渠道转移，主动营销腾安QDII/港股通产品；<br>
            ② 承接流出客户→制定跨境券商存量客户迁移承接方案和营销话术；<br>
            ③ 关注艾德6/15跟进情况，跨境整治可能在2年过渡期内持续加码。
          </div>
        </div>'''

if old_card_1 in content:
    content = content.replace(old_card_1, new_card_1)
    print("✅ S2卡片1 body/footer/action-box 已更新")
else:
    print("❌ S2卡片1 旧内容未找到，尝试模糊匹配...")
    # 尝试只匹配关键部分
    if '5月22日重磅落地' in content:
        print("   → 找到 '5月22日重磅落地'，但整体不匹配")
    else:
        print("   → 未找到 '5月22日重磅落地'")

# ===== 2. 更新S6 市场行情速览 =====
old_s6 = '''        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股6月11日（周四）收盘：</b>上证指数<b>3974.60点（-0.47%）</b>；深证成指<b>14832.72点（-0.81%）</b>；创业板指<b>3816.39点（-0.99%）</b>。两市成交约<b>2.64万亿元</b>，量能较昨日（2.9万亿）明显萎缩，科技虹吸效应持续。<br><br>
            <b>📊 港股6月11日收盘：</b>恒生指数承压（昨夜美股重挫传导），恒生科技跟随调整。南向资金净流入约百亿港元，底部支撑仍存。<br><br>
            <b>📊 美股6月10日（CPI公布后）收盘：</b>道指<b>-1.88%</b>；标普500<b>-1.61%</b>；纳指<b>-1.98%</b>。费城半导体指数重挫。主因：CPI=4.2%符合预期但绝对值高位→美联储加息预期升温。<br><br>
            <b>📊 关键数据：</b>两融余额约2.88万亿元 / SpaceX明日（6/12）正式挂牌纳斯达克 / 指数调样（6/12）千亿被动调仓
          </div>
          <div>
            <b>📊 昨日回顾（6/10）：</b><br>
            ▪ CPI 4.2%符合预期公布，美股期货先跌后涨<br>
            ▪ A股低开后震荡修复，沪指收于3993点<br>
            ▪ 科技股PCB/半导体材料方向活跃但修复不理想<br><br>
            <b>📊 今日关注（6/11周四）：</b><br>
            ▪ 美国CPI结果落地→美联储6/18议息预期重新定价<br>
            ▪ SpaceX IPO今日定价135美元/股→明日正式挂牌<br>
            ▪ A股量能萎缩至2.64万亿→关注4000点支撑<br><br>
            <b>📊 明日（6/12周五）：</b><br>
            ▪ SpaceX（SPCX）正式纳斯达克挂牌→史上最大IPO<br>
            ▪ 沪深300/中证500指数调样生效→千亿被动调仓<br>
            ▪ 宇树科技科创板上市→机器人赛道双催化
          </div>
        </div>'''

new_s6 = '''        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股6月12日（周五）盘中：</b>上证指数<b>4086点（+2.81%）</b>强势反弹；深证成指<b>15320点（+3.29%）</b>；创业板指<b>3950点（+3.51%）</b>。SpaceX正式挂牌催化科技板块，指数调样千亿资金今日尾盘调仓。<br><br>
            <b>📊 港股6月12日：</b>恒生指数跟随A股反弹，恒生科技涨幅扩大。南向资金持续净流入，港股科技板块受SpaceX挂牌情绪带动。<br><br>
            <b>📊 美股6月11日（隔夜）收盘：</b>道指<b>+1.87%（49918→50848）</b>强势反弹；标普500<b>+1.73%</b>；纳指<b>+2.04%</b>。欧央行加息25bp后美股不跌反涨，市场解读为"欧央行抢跑加息→美联储相对鸽派"。<br><br>
            <b>📊 关键数据：</b>两融余额约2.90万亿元 / SpaceX今日正式挂牌SPCX / 指数调样今日收盘后生效
          </div>
          <div>
            <b>📊 昨日回顾（6/11）：</b><br>
            ▪ SpaceX IPO定价135美元/股确认<br>
            ▪ A股震荡分化沪指3974(-0.47%)量能萎缩<br>
            ▪ 欧央行宣布重启加息25bp→全球首家<br><br>
            <b>📊 今日关注（6/12周五）：</b><br>
            ▪ SpaceX正式纳斯达克挂牌→史上最大IPO落地<br>
            ▪ 指数调样今日收盘后生效→尾盘千亿被动调仓<br>
            ▪ 跨境券商禁令今日正式执行→富途/老虎暂停买入<br><br>
            <b>📊 下周一（6/16）：</b><br>
            ▪ 美联储6/16-17议息会议→6/18公布结果<br>
            ▪ 关注点阵图是否反映降息次数减少
          </div>
        </div>'''

if old_s6 in content:
    content = content.replace(old_s6, new_s6)
    print("✅ S6 市场行情速览已更新")
else:
    print("❌ S6 旧内容未找到，跳过")

# ===== 3. 更新S7 时间线 =====
# 先删除超期条目（05-29及更早），再加入06-12新条目
# 当前S7条目：06-11/06-10/06-09/06-08/06-06/06-05/06-04/06-03/06-02/06-01
# T-14 = 05-29，所以05-29的MSCI条目需要删除（05-29 < 05-29? 等于边界，保留）
# 实际S7中没有05-29的独立条目（05-29是MSCI条目，date-tag=05-29，在边界上，保留）
# 需要加入06-12新条目，删除最老的一条（06-01）以保持不超过12条

new_timeline_items = '''
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-12（SpaceX正式挂牌·指数调样生效·跨境券商禁令执行·A股强势反弹）</div>
          <div class="timeline-title">SpaceX今日正式纳斯达克挂牌（代码SPCX）/ 指数调样今日收盘后生效·千亿被动调仓 / 跨境券商禁令正式执行 / A股沪指4086(+2.81%)强势反弹</div>
          <div class="timeline-desc">SpaceX以代码SPCX正式在纳斯达克挂牌，发行价135美元/股，估值1.77万亿美元，募资750亿美元，史上最大IPO。沪深300等10余只宽基指数样本调整今日收盘后正式生效，近9000亿指数基金被动调仓，尾盘可能出现异常波动。跨境券商禁令今日正式执行，富途/老虎/长桥境内账户暂停买入。A股今日强势反弹，沪指4086点(+2.81%)，科技板块受SpaceX挂牌催化。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-11（欧央行重启加息·SpaceX定价确认·A股量能萎缩）</div>
          <div class="timeline-title">欧央行宣布重启加息25bp（全球主要经济体首家）/ SpaceX IPO定价135美元/股确认 / A股沪指3974(-0.47%)量能萎缩至2.64万亿</div>
          <div class="timeline-desc">欧洲央行成为2026年首家重启加息的全球主要经济体央行，存款机制利率+25bp。SpaceX IPO发行价确认为135美元/股，估值1.77万亿美元，明日正式挂牌。A股今日震荡分化，沪指收3974.60(-0.47%)，深成指-0.81%，创业板指-0.99%，两市成交2.64万亿，量能较昨日萎缩。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-10（CPI=4.2%符合预期·美股重挫·A股缩量震荡）</div>
          <div class="timeline-title">美国5月CPI=4.2%符合预期 / 美股三大指数集体收跌（道指-1.88%·纳指-1.98%）/ A股沪指3993(+0.47%)缩量</div>
          <div class="timeline-desc">美国5月CPI数据昨晚20:30公布，同比4.2%符合预期，但未超预期→美联储加息预期进一步升温。受此影响，隔夜美股三大指数集体收跌：道指-1.88%、纳指-1.98%、标普-1.61%。A股今日缩量震荡，沪指收3993.23(+0.47%)，科技股虹吸效应持续，传统蓝筹修复乏力。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-09（A股暴力反弹收复4000点·美股分化·港股止跌）</div>
          <div class="timeline-title">A股沪指4010.03(+1.28%)收复4000点 / 创业板+3.93%暴力反弹 / 美股纳指+0.86% / 港股恒科+0.29%止跌</div>
          <div class="timeline-desc">A股全线反弹，沪指4010.03点（+1.28%）收复4000点，创业板指+3.93%，科创50+4.17%，科技股集体爆发。美股纳指+0.86%，英特尔+11.10%，美光+9.83%。港股恒生指数-0.37%，但恒生科技+0.29%止跌回升，腾讯+3%。今晚CPI前市场屏息。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-08（A股4000点保卫战打响·沪指失守3959点·超级周正式开局）</div>
          <div class="timeline-title">A股沪指3959.34(-1.70%)失守4000点 / 6/10中美CPI同日公布 / 6/12 SpaceX上市+指数调样千亿换仓</div>
          <div class="timeline-desc">6月8日周一A股全线下跌，沪指失守4000点收于3959.34点。主因：美国5月非农17.2万翻倍超预期→加息预期飙升→全球股市普跌。本周超级周正式开局：6/10中美CPI同日公布，6/12 SpaceX史上最大IPO纳斯达克挂牌+沪深300等指数样本调整生效，被动资金千亿级调仓。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-06（中基协换届刘晓艳当选会长·吴清四个坚持定调·翻倍基增至17只）</div>
          <div class="timeline-title">中基协第四届换届：易方达刘晓艳当选兼职会长 / 吴清定调"四个坚持" / 年内翻倍基增至17只</div>
          <div class="timeline-desc">中基协空缺两年后完成换届，刘晓艳为23年来首位头部公募女性掌门人。吴清在第四届会员代表大会上明确定调"四个坚持"。年内翻倍基增至17只引发抱团争议。华盛证券6/15起暂停内地新开仓，跟进跨境券商整治。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-05（国办私募顶层设计落地·中证金牛被集体解约·美国非农翻倍）</div>
          <div class="timeline-title">国办23万亿私募顶层设计落地 / 中证金牛被招商/嘉实等集体解约 / 美国5月非农17.2万翻倍→加息预期升温</div>
          <div class="timeline-desc">国办函〔2026〕54号全文发布，私募基金行业首份国务院层面顶层设计文件。中证金牛被多家公募集体终止合作，第三方代销出清加速。美国5月非农17.2万翻倍超预期→加息预期飙升，全球市场承压。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-04（A股缩量回调·央行国债净投放500亿·易方达ETF登顶第一）</div>
          <div class="timeline-title">A股沪指4057.78(-0.64%)缩量回调 / 央行5月国债净投放500亿 / 易方达ETF规模6185亿超越华夏登顶</div>
          <div class="timeline-desc">A股缩量回调，半导体/AI方向承压。央行5月公开市场国债买卖净投放500亿，延续宽松基调。易方达基金旗下ETF规模达6185.19亿元，超越华夏基金登顶全市场ETF规模第一，差距仅19亿元，竞争白热化。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-03（东吴115亿收购东海证券·标普首破7600·美股再创历史新高）</div>
          <div class="timeline-title">东吴证券115亿收购东海证券83.68%股份草案公告 / 标普500首破7600点创新高 / 央行国债净投放500亿</div>
          <div class="timeline-desc">百亿级券商合并案正式落地，东海100%股权评估137.65亿。央行延续宽松基调，5月公开市场国债买卖净投放500亿。美股三大指数再创新高，标普500首破7600点，Marvell+30%。A股创业板+2.66%深V修复。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-02（腾讯暴涨10.46%创2021来最大涨幅·恒生科技+4.72%·AI Agent突破）</div>
          <div class="timeline-title">腾讯控股+10.46%（AI Agent突破+云降价97.5%）/ 恒生科技+4.72% / A股创业板+2.66%深V修复</div>
          <div class="timeline-desc">腾讯单日暴涨10%创4年来最大涨幅，AI Agent开发平台+云降价97.5%双重催化。恒生科技大涨，美团+9%。A股探底回升，MLCC/CPO/机器人爆发。成交2.79万亿。成交额前20科技股全部收红。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-01（宇树科技IPO过会·195只基金基准换新生效·指数样本6/12调整公告）</div>
          <div class="timeline-title">宇树科技科创板IPO过会（拟募42亿·人形机器人第一股）/ 195只基金业绩基准正式换新 / 沪深300等指数样本6/12调整</div>
          <div class="timeline-desc">宇树科技IPO过会，冲刺科创板"具身智能第一股"，受理仅73天。195只基金总规模近4000亿业绩基准正式调整生效。沪深300换19只/中证500换50只样本6/12收盘后生效，千亿被动资金调仓。</div>
        </div>
      </div>
'''

# 找到S7部分并整体替换
s7_start_marker = '  <!-- ============ Section 7: 关键时间线 ============ -->'
s7_end_marker = '  <!-- ============ Section 8: 待办事项 ============ -->'

s7_start = content.find(s7_start_marker)
s7_end = content.find(s7_end_marker)

if s7_start != -1 and s7_end != -1:
    s7_section = content[s7_start:s7_end]
    # 找到 timeline items 的范围（从第一个 timeline-item 到最后一个）
    t_start = s7_section.find('<div class="timeline-item">')
    t_end = s7_section.rfind('</div>\n    </div>\n  </div>') + len('</div>\n    </div>\n  </div>')
    
    # 重新构造S7部分
    s7_before = s7_section[:t_start]
    s7_after = s7_section[s7_section.rfind('</div>\n    </div>\n  </div>'):]
    
    new_s7_section = s7_before + new_timeline_items + '    </div>\n  </div>\n'
    
    content = content[:s7_start] + new_s7_section + content[s7_end:]
    print("✅ S7 时间线已更新（新增06-12，保留06-01~06-11共10条）")
else:
    print("❌ S7 部分未找到，跳过")

# ===== 4. 更新S8 待办事项 =====
new_s8 = '''  <!-- ============ Section 8: 待办事项 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fff7ed;color:#ea580c;">✅</div>
      <span class="section-title">今日待办建议清单（6月12日更新）</span>
    </div>

    <div class="card" style="border-left-color: #ea580c;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="border-bottom:2px solid var(--gray-200);">
            <th style="text-align:left;padding:10px 12px;color:var(--gray-500);font-size:12px;width:8%">优先级</th>
            <th style="text-align:left;padding:10px 12px;color:var(--gray-500);font-size:12px;width:52%">待办事项</th>
            <th style="text-align:left;padding:10px 12px;color:var(--gray-500);font-size:12px;width:20%">关联事件</th>
            <th style="text-align:left;padding:10px 12px;color:var(--gray-500);font-size:12px;width:20%">建议完成时间</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">SpaceX今日正式挂牌SPCX！史上最大IPO→关注纳斯达克100 QDII和美股ETF申赎异动</td>
            <td style="padding:10px 12px;color:var(--gray-500);">SpaceX 6/12正式挂牌</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">今日完成</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">指数调样今日收盘后生效应对：沪深300等10余只宽基调样→评估腾安代销ETF受影响情况，做好投资者沟通</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/12收盘后生效</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">今日收盘后</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">跨境券商禁令今日正式执行→关注QDII/港股通需求激增，主动营销腾安合规跨境产品</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/12禁令正式执行</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">今日完成</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag urgent">P0</span></td>
            <td style="padding:10px 12px;font-weight:600;">美联储6/18议息会议准备：欧央行已重启加息→评估对QDII/港股产品影响，准备客户沟通材料</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/16-17会议·6/18公布</td>
            <td style="padding:10px 12px;color:var(--danger);font-weight:600;">6月17日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">A股强势反弹验证：沪指4086(+2.81%)→主动推送市场解读，避免客户恐慌性赎回</td>
            <td style="padding:10px 12px;color:var(--gray-500);">6/12科技板块强势反弹</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">今日收盘后</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">基准换新第三周跟踪：195只基金6/1生效已三周→收集客户咨询情况，确认超额收益展示逻辑已切换</td>
            <td style="padding:10px 12px;color:var(--gray-500);">195只基金基准6/1生效</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">本周内</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">跨境券商客户承接：富途/老虎禁令执行→制定存量客户迁移承接方案，主动营销腾安QDII</td>
            <td style="padding:10px 12px;color:var(--gray-500);">跨境禁令6/12执行</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">6月15日前</td>
          </tr>
          <tr style="border-bottom:1px solid var(--gray-100);">
            <td style="padding:10px 12px;"><span class="priority-tag important">P1</span></td>
            <td style="padding:10px 12px;font-weight:600;">中基协换届后续跟踪：刘晓艳当选会长→关注新一届理事会对代销机构政策倾向</td>
            <td style="padding:10px 12px;color:var(--gray-500);">中基协6/6换届</td>
            <td style="padding:10px 12px;color:var(--warning);font-weight:600;">持续关注</td>
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
          </tr>
        </tbody>
      </table>
    </div>
  </div>'''

# 找到旧S8部分并替换
s8_start_marker = '  <!-- ============ Section 8: 待办事项 ============ -->'
s8_end_marker = '<!-- Footer -->'

s8_start = content.find(s8_start_marker)
s8_end = content.find(s8_end_marker)

if s8_start != -1 and s8_end != -1:
    content = content[:s8_start] + new_s8 + '\n' + content[s8_end:]
    print("✅ S8 待办事项已更新")
else:
    print("❌ S8 部分未找到，跳过")

# ===== 5. 更新Footer =====
old_footer = '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月11日 · 信息来源：证券时报、中基协、同花顺财经、新浪财经、证监会、上交所、深交所、东方财富、财联社、央视网、上海证券报、中国证券报、新华网、中国经济网、腾讯新闻等公开渠道<br>'
new_footer = '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月12日 · 信息来源：证券时报、中基协、同花顺财经、新浪财经、证监会、上交所、深交所、东方财富、财联社、央视网、上海证券报、中国证券报、新华网、中国经济网、腾讯新闻、欧央行、太空日报等公开渠道<br>'

if old_footer in content:
    content = content.replace(old_footer, new_footer)
    print("✅ Footer 数据采集时间已更新")
else:
    print("❌ Footer 旧内容未找到，尝试查找...")
    if '数据采集时间 2026年6月11日' in content:
        content = content.replace('数据采集时间 2026年6月11日', '数据采集时间 2026年6月12日')
        print("✅ Footer 数据采集时间已通过部分匹配更新")
    else:
        print("❌ Footer 数据采集时间未找到")

# 更新 <!-- daily-update --> 标记
content = content.replace('<!-- daily-update: 2026-06-11 -->', '<!-- daily-update: 2026-06-12 -->')

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 所有更新已完成，文件已保存")
