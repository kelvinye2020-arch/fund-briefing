#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基金看板 2026-06-11 补位更新脚本（兜底检查 automation-8）"""

import re

HTML_PATH = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def do_replace(content, old, new, label):
    if old in content:
        content = content.replace(old, new, 1)
        print(f'  ✅ {label}: 替换成功')
        return content
    else:
        print(f'  ❌ {label}: 未找到匹配文本！')
        # 打印旧文本的片段用于调试
        idx = content.find(old[:50])
        print(f'    调试：在内容中搜索前50字符，位置={idx}')
        return content

def main():
    content = read_file(HTML_PATH)
    original_len = len(content)
    print(f'原始文件长度: {original_len} 字符')

    # ========== 1. 更新 daily-update 标记（文件第2行 + 文件末尾） ==========
    # 第2行：<!-- daily-update: 2026-06-10 -->
    content = do_replace(content,
        '<!-- daily-update: 2026-06-10 -->',
        '<!-- daily-update: 2026-06-11 -->',
        'daily-update 第2行标记')

    # 文件末尾标记
    content = do_replace(content,
        '<!-- daily-update: 2026-06-09 -->',
        '<!-- daily-update: 2026-06-11 -->',
        'daily-update 末尾标记')

    # ========== 2. 更新 Header 日期区间 ==========
    content = do_replace(content,
        '<div class="date-badge">📅 数据区间：2026.05.27 — 2026.06.10（今日自动更新）</div>',
        '<div class="date-badge">📅 数据区间：2026.05.28 — 2026.06.11（今日自动更新）</div>',
        'Header 日期区间')

    # ========== 3. 更新 Footer 数据采集时间 ==========
    content = do_replace(content,
        '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月10日 · 信息来源',
        '腾安基金 · 行业情报看板 · 数据采集时间 2026年6月11日 · 信息来源',
        'Footer 数据采集时间')

    # ========== 4. 更新 Section 0 标题 ==========
    content = do_replace(content,
        '<span class="section-title">今日焦点（6月10日·周三·CPI公布日：今晚20:30美国5月CPI揭晓·A股低开高走）</span>',
        '<span class="section-title">今日焦点（6月11日·周四·SpaceX定价+美股重挫·A股震荡分化）</span>',
        'S0 标题')

    # ========== 5. 更新 Stats Bar ==========
    # Card 1: CPI → 已公布结果
    content = do_replace(content,
        '<div class="stat-number">CPI今夜</div>\n    <div class="stat-label">今晚20:30美国5月CPI揭晓·预期同比4.2%-4.3%创2023年6月来新高·三种情景预案</div>\n    <div class="stat-change up">▲ 中国5月CPI已公布温和回升·美国非农翻倍后CPI成最后变量</div>',
        '<div class="stat-number">CPI 4.2%</div>\n    <div class="stat-label">美国5月CPI同比4.2%符合预期·创2023年6月来新高·美联储加息预期升温</div>\n    <div class="stat-change up">▲ 6/18美联储议息成下一焦点·高利率环境持续压制估值</div>',
        'Stats Card 1: CPI')

    # Card 2: 沪指
    content = do_replace(content,
        '<div class="stat-number">沪指4010</div>\n    <div class="stat-label">6/9收盘4010(+1.28%)·今日低开0.62%·4000点支撑再次测试</div>\n    <div class="stat-change down">▼ 今日低开获利回吐·今晚CPI前市场谨慎·关注4000点得失</div>',
        '<div class="stat-number">沪指3974</div>\n    <div class="stat-label">6/11收盘3974(-0.47%)·深成指-0.81%·创业板指-0.99%·量能萎缩至2.64万亿</div>\n    <div class="stat-change down">▼ 科技虹吸效应持续·传统蓝筹修复乏力·关注今晚美股指引</div>',
        'Stats Card 2: 沪指')

    # Card 3: SpaceX
    content = do_replace(content,
        '<div class="stat-number">SpaceX明定价</div>\n    <div class="stat-label">SpaceX IPO 明（6/11）定价·后日（6/12）纳斯达克挂牌·估值1.75-2.0万亿</div>\n    <div class="stat-change up">▲ 获1500亿美元认购（目标750亿的2倍）·史上最大超额认购</div>',
        '<div class="stat-number">SpaceX明挂牌</div>\n    <div class="stat-label">SpaceX IPO今日定价135美元/股·明日（6/12）正式纳斯达克挂牌·估值1.77万亿</div>\n    <div class="stat-change up">▲ 史上最大IPO·750亿美元募资·全球科技资金虹吸效应持续</div>',
        'Stats Card 3: SpaceX')

    # Card 4: 指数调样
    content = do_replace(content,
        '<div class="stat-number">指数调样后日</div>\n    <div class="stat-label">沪深300换19只/中证500换50只·后日（6/12）收盘后生效·千亿被动资金调仓</div>\n    <div class="stat-change up">▲ 宇树科技同步6/12科创板上市·机器人赛道双催化剂叠加</div>',
        '<div class="stat-number">双催化明日</div>\n    <div class="stat-label">明日（6/12）SpaceX正式挂牌+指数调样+宇树上市·三重催化科技成长</div>\n    <div class="stat-change up">▲ 千亿被动资金明日调仓·关注相关ETF折溢价套利机会</div>',
        'Stats Card 4: 双催化')

    # ========== 6. 更新 S0 卡片（今日焦点） ==========
    # 卡片1：美国CPI + 美股重挫
    old_card1 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 今晚20:30！美国5月CPI重磅揭晓，预期同比4.2%-4.3%创2023年6月来新高</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>超级周核心事件：</b>今晚<b>20:30</b>美国5月CPI数据公布，市场预期名义CPI同比升至<b>4.2%-4.3%</b>（前值为3.8%），核心CPI同比预计升至<b>2.9%</b>（前值2.8%），这将是2023年6月以来最高水平。数据直接决定<b>6/18美联储议息</b>基调，若超预期将引发全球市场剧烈震荡。<br>
          <b>三种情景预判：</b>①数据超预期（>4.3%）→加息预期骤升，美股承压、美元走强、QDII净值波动；②符合预期（4.2%-4.3%）→市场已充分定价，反应温和；③低于预期（<4.0%）→加息预期降温，全球风险资产反弹。<br>
          <b>中国5月CPI（已公布）：</b>中国5月CPI/PPI于6/9同期公布，CPI温和回升、PPI降幅收窄，内需修复信号逐步明确。
        </div>
        <div class="card-footer">
          <a href="https://stock.10jqka.com.cn/20260610/c677344394.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺</span></a>
          <a href="http://finance.sina.cn/hkstock/ggyw/2026-06-10/detail-iniawicy6101708.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经</span></a>
          <span class="impact-tag high">超级周：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 今晚20:30美国CPI→提前准备三种情景预案（超预期/符合预期/低于预期），覆盖QDII/港股ETF客户应急话术；<br>
            ② 明日6/12指数调样千亿被动调仓→评估腾安代销ETF受影响情况，做好客户提示；<br>
            ③ SpaceX IPO明日（6/11）定价→后日（6/12）挂牌，关注美股科技虹吸效应对纳斯达克100 ETF的影响。
          </div>
        </div>
      </div>'''

    new_card1 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 美国5月CPI=4.2%符合预期公公布！美联储加息预期升温，美股昨夜重挫</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>CPI结果揭晓：</b>美国5月CPI同比<b>4.2%</b>（符合预期4.2%-4.3%），核心CPI同比<b>2.9%</b>，双双创2023年6月以来最高水平。数据公布后市场短暂震荡，美股昨夜（6/10）三大指数集体收跌：道指<b>-1.88%</b>、纳指<b>-1.98%</b>、标普<b>-1.61%</b>，费城半导体指数重挫。<br>
          <b>加息预期升温：</b>CPI持续高位→市场彻底放弃2026年降息预期，部分机构开始定价"重启加息"风险。6/18美联储议息会议成为全球市场下一焦点，当前市场预期"不降息、不加息"为基准情形。<br>
          <b>对A股影响：</b>高利率环境持续→美股承压→纳斯达克100 QDII产品净值波动→需准备客户沟通话术。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867614452199905165" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·财联社</span></a>
          <a href="http://invest.10jqka.com.cn/20260611/c677372807.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺</span></a>
          <span class="impact-tag high">美联储：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① CPI符合预期→加息预期升温，QDII纳斯达克100产品客户可能集中咨询，准备应急话术；<br>
            ② 美股重挫→关注今日A股开盘情绪传导，科技成长板块可能承压；<br>
            ③ 6/18美联储议息→未来一周全球市场高波动，提前准备客户风险提示模板。
          </div>
        </div>
      </div>'''

    content = do_replace(content, old_card1, new_card1, 'S0 卡片1: CPI结果')

    # 卡片2：SpaceX 定价
    old_card2 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 A股6/9暴力反弹后今日低开！沪指4010→低开0.62%，科技股分化加剧</div>'''

    new_card2 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 SpaceX IPO今日定价135美元/股！明日正式挂牌纳斯达克，史上最大IPO估值1.77万亿</div>'''

    # 实际上需要替换整张卡片2
    old_card2_full = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 A股6/9暴力反弹后今日低开！沪指4010→低开0.62%，科技股分化加剧</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-10</span>
          </div>
        </div>
        <div class="card-body">
          <b>6月9日收盘（昨日）：</b>沪指<b>4010.03点（+1.28%）</b>收复4000点；深证成指<b>+2.50%</b>；创业板指<b>3811.79点（+3.93%）</b>暴力反弹；科创50<b>+4.17%</b>。两市成交约<b>2.9万亿元</b>，量能放大明显，半导体/AI方向强势领涨。<br>
          <b>今日（6/10）开盘：</b>三大指数集体低开，沪指低开<b>0.62%</b>，深成指低开<b>1.35%</b>，创业板指低开<b>1.62%</b>，科创综指低开0.55%。主因：今晚CPI公布前市场谨慎，获利盘逢高减仓。<br>
          <b>核心逻辑：</b>昨日反弹验证"调整接近尾声"信号，但今晚CPI是关键变量→若数据温和，明日有望继续反弹；若超预期，可能再次测试4000点支撑。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867571987130189303" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·央广财经</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1867536851942047302" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·行情分析</span></a>
          <span class="impact-tag high">A股关键点：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 今日低开→关注沪指4000点支撑是否有效，如跌破需准备客户安抚话术；<br>
            ② 科技基金持有人在昨日大涨后情绪修复→主动推送市场解读，引导长期持有而非追涨杀跌；<br>
            ③ 今晚CPI公布后→根据结果分类准备客户通知模板（三种情景）。
          </div>
        </div>
      </div>'''

    new_card2_full = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 SpaceX IPO今日定价135美元/股！明日正式挂牌纳斯达克，史上最大IPO估值1.77万亿</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>定价确认：</b>SpaceX于今日（6/11）正式确定IPO发行价为<b>135美元/股</b>，发行约<b>5.556亿股</b>，募资规模<b>750亿美元</b>，对应完全稀释后估值<b>1.77万亿美元</b>，超越沙特阿美（294亿美元）成为全球史上最大IPO。<br>
          <b>挂牌时间：</b>明日（<b>6月12日</b>）正式在纳斯达克挂牌，股票代码<b>SPCX</b>。全球资金已录得超<b>2500亿美元</b>认购需求（目标750亿的3.3倍）。<br>
          <b>业务拆解：</b>市场认识到SpaceX=火箭（Starlink现金牛）+AI算力双引擎。2025年亏损49亿美元（星链投入期），2026年Q1营收8.18亿美元，商业化路径逐步清晰。<br>
          <b>对A股影响：</b>全球科技资金虹吸效应持续→A股科技板块面临资金分流压力，但国内星网产业链（光通信/卫星）可能受带动炒作。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1867384383114889729" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·IPO拆解</span></a>
          <a href="https://m.jrj.com.cn/madapter/usstock/2026/06/11082857424121.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">金融界</span></a>
          <span class="impact-tag high">史上最大IPO：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① SpaceX IPO虹吸效应→关注纳斯达克100 QDII和美股ETF的申购/赎回异动，提前准备客户提示；<br>
            ② 明日6/12挂牌→美股可能剧烈波动，QDII产品需关注折溢价风险；<br>
            ③ 国内卫星互联网产业链（星网集团等）可能受情绪带动，关注相关主题基金机会。
          </div>
        </div>
      </div>'''

    content = do_replace(content, old_card2_full, new_card2_full, 'S0 卡片2: SpaceX定价')

    # 卡片3（原卡片3变为卡片3）：A股6/11震荡
    old_card3 = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 SpaceX IPO明（6/11）定价！获1500亿美元认购需求（目标750亿的2倍）·后日挂牌纳斯达克</div>'''

    new_card3_full = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 A股6/11震荡分化：沪指3974(-0.47%)·科技虹吸持续·量能萎缩至2.64万亿</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>今日（6/11）收盘：</b>沪指<b>3974.60点（-0.47%）</b>；深证成指<b>14832.72点（-0.81%）</b>；创业板指<b>3816.39点（-0.99%）</b>。两市成交约<b>2.64万亿元</b>，量能较昨日（2.9万亿）明显萎缩。<br>
          <b>结构特征：</b>科技股虹吸效应持续，PCB/半导体材料方向盘中活跃但整体修复不理想。传统蓝筹（地产/消费/金融）未被明显虹吸，但自主修复力度有限，市场呈现"科技强、全盘弱"格局。<br>
          <b>关键变量：</b>今晚美股（CPI后夜盘）和明日SpaceX挂牌是下一阶段A股科技板块的核心外部变量。机构普遍建议"哑铃策略"：科技成长+红利价值两端配置。
        </div>
        <div class="card-footer">
          <a href="https://www.zhihu.com/question/2045900295251796462/answer/2048172479080820761" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">知乎·今日复盘</span></a>
          <a href="https://xueqiu.com/5337320774/394101037" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">雪球</span></a>
          <span class="impact-tag medium">A股结构：中高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 量能萎缩+科技虹吸→关注客户持仓集中度风险，主动提示分散配置；<br>
            ② 哑铃策略（科技+红利）→在腾安推荐算法中提高红利价值类基金曝光；<br>
            ③ 明日SpaceX挂牌+指数调样→双重催化下科技板块可能高波动，提前准备客户陪伴内容。
          </div>
        </div>
      </div>'''

    # 找到原卡片3（SpaceX那张），替换为新卡片3
    old_card3_full = content[content.find('<!-- S0 今日焦点 -->'):]
    old_card3_full = old_card3_full[:old_card3_full.find('<!-- ============ Section 1')]
    # 提取第3张卡片（SpaceX那张）
    cards_end = content.find('<!-- ============ Section 1')
    s0_section = content[content.find('<!-- ============ Section 0'):cards_end]
    # 找到第3张卡片的起止位置
    card3_start = s0_section.find('<div class="card p0">\n        <div class="card-top">\n          <div class="card-title">🔴 SpaceX IPO明')
    if card3_start == -1:
        print('  ❌ 未找到S0第3张卡片')
    else:
        card3_end = s0_section.find('</div>\n\n  </div>', card3_start) + len('</div>\n\n  </div>')
        old_card3_actual = s0_section[card3_start:card3_end]
        print(f'  S0 第3张卡片长度: {len(old_card3_actual)} 字符')
        # 但这张已经在上面被替换过了（它是第2张）...
        # 让我重新理清：原HTML里S0有3张卡片：
        # 1. CPI（已替换为新卡片1）
        # 2. A股低开（已替换为新卡片2：SpaceX定价）
        # 3. SpaceX IPO明日定价（需要替换为新卡片3：A股震荡）
        # 所以这里应该找 SpaceX IPO明（6/11）那张
        pass

    print('⚠️ S0 卡片3 替换需要更精准的定位，将在下一步处理')

    # 先写回文件，然后做更精准的替换
    write_file(HTML_PATH + '.bak', content)
    print(f'\n备份已写入: {HTML_PATH}.bak')
    print(f'当前文件长度: {len(content)} 字符')

if __name__ == '__main__':
    main()
