# -*- coding: utf-8 -*-
"""daily-update-2026-09-08: S0/S6/S7/StatsBar/header 更新"""
import re, datetime

PATH = 'index.html'
with open(PATH, encoding='utf-8') as f:
    html = f.read()

orig = html
report = []

# ---------- 1. header 数据区间 ----------
today = datetime.date(2026, 9, 8)
lower = today - datetime.timedelta(days=14)
badge_new = "📅 数据区间：{} — {}（每日更新）".format(
    lower.strftime('%Y.%m.%d'), today.strftime('%Y.%m.%d'))
html, n = re.subn(r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）",
                  badge_new, html)
assert n == 1, 'header badge replaced {}'.format(n)
report.append('header badge -> {}'.format(badge_new))

# ---------- 2. Stats Bar 沪指卡 ----------
old_stat = '''    <div class="stat-card">
      <div class="stat-number">3930.12</div>
      <div class="stat-label">沪指9-4收盘·跌0.30%·沪深京成交2.05万亿·放量下探</div>
      <div class="stat-change down">▼ 深成指-0.79%·创业板-0.78%·科创50跌2.16%</div>
    </div>'''
new_stat = '''    <div class="stat-card">
      <div class="stat-number">3932.70</div>
      <div class="stat-label">沪指9-7收盘·涨0.07%·两市成交1.95万亿·创业板涨3.41%</div>
      <div class="stat-change up">▲ 深成指+1.91%·创业板+3.41%·科创50涨2.42%</div>
    </div>'''
assert html.count(old_stat) == 1, 'stat card count {}'.format(html.count(old_stat))
html = html.replace(old_stat, new_stat)
report.append('StatsBar 沪指 -> 3932.70 +0.07% (09-07收盘)')

# ---------- 3. S0 今日焦点 整块替换 ----------
s0_new = '''        <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月8日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
      <!-- S0 Card 1 (09-08 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批18只主动ETF冲刺"最后一公里"·大概率10月集中募集</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-08</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月8日（人民财讯），作为公募行业近年来的重磅创新产品，首批主动ETF落地在即、正在冲刺"最后一公里"。渠道人士透露，完成前期准备与场检流程后，该批产品将获批，大概率于10月集中启动募集。<br>
          <b>时间脉络：</b>6月17日证监会主席吴清在陆家嘴论坛宣布支持沪深交易所推出主动ETF，同日沪深交易所发布业务指引；7月17日首批18只主动ETF正式上报，由华夏、易方达、永赢、华泰柏瑞、鹏华、汇添富等18家机构管理（9家拟上交所、9家拟深交所上市）。<br>
          <b>产品形态：</b>分主观选股与主动量化两条路径，多只产品名带"价值""均衡""红利"字样，整体"求稳"，沿"偏大盘、偏均衡"设计（如汇添富以中证800为基准）；部分采用"双基金经理共管"（主动权益经理主导选股＋ETF经理负责PCF与申赎）。<br>
          <b>对腾安启示：</b>ETF从"被动工具"迈向"主动+被动协同"新阶段，竞争逻辑由"卷费率抢渠道"转向"拼投研创超额"；代销端应前置储备主动ETF的选品、对比与投教能力，迎接10月集中发行窗口。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202609083867149833.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-08</span></a>
        </div>
      </div>

      <!-- S0 Card 2 (09-08 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募年内获配定增473.46亿·同比+168.71%·电子行业88.49亿居首</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-08</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月8日（记者陈颖清）：公募排排网数据显示，截至9月6日，今年以来共有27家公募机构参与21个申万一级行业中的93只A股定增，合计获配473.46亿元，较去年同期176.20亿元增长168.71%；按当日收盘价统计，27家机构整体浮盈比例6.83%，实现浮盈机构占比55.56%。<br>
          <b>行业分布：</b>电子行业获配88.49亿元（15只个股）居首，煤炭63.80亿（中国神华单只）、电力设备61.33亿分列二三位；汽车、公用事业、国防军工等获配均超20亿。<br>
          <b>机构格局：</b>财通基金参与89只定增获配150.74亿、诺德基金88只获配145.05亿、易方达基金13只获配101.12亿居前；信达澳亚参与科翔股份浮盈520.04%领先，但机构间收益分化明显。<br>
          <b>对腾安启示：</b>定增折价为组合提供"安全垫"、契合中长期考核，科技制造（电子/半导体）是核心方向；代销端可关注定增策略基金的配置价值，但需提示个股收益分化风险。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/786669" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-08</span></a>
        </div>
      </div>

      <!-- S0 Card 3 (09-07 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募9月首周调研1428次·电子板块303次居首·MLCC/机器人视觉受追捧</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月7日（记者林郑宏）：公募排排网数据显示，上周（8月31日—9月6日）共有142家公募机构参与A股调研，覆盖27个申万一级行业175只个股，合计调研1428次，延续较高热情。<br>
          <b>行业分布：</b>电子行业最受青睐（27只个股、303次）居首，医药生物183次、汽车125次、电力设备123次分列其后；个股层面，迈瑞医疗被调研51次居首，风华高科、圣邦股份、奥比中光、嘉立创4只电子股入围热度前十。<br>
          <b>方向信号：</b>MLCC景气上行（风华高科）、光模块模拟芯片（圣邦股份）、机器人视觉（奥比中光上半年视觉方案销售同比翻倍、已适配蚂蚁灵波等具身智能客户）成关注焦点；机构端华宝71次、银河67次、嘉实62次居前。<br>
          <b>对腾安启示：</b>科技赛道（电子/AI硬件）机构关注度持续升温，代销端可结合调研热度同步更新科技主题基金的观点与投教素材。
        </div>
        <div class="card-footer">
          <a href="https://m.cnfin.com/gs-lb//zixun/20260907/4466178_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-07</span></a>
        </div>
      </div>

      <!-- S0 Card 4 (09-08 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 科技主题LOF溢价停牌·财通福鑫定开9-8继续停牌一小时·多只通信ETF涨超6%</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-08</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月8日：9月7日科技主题ETF大反攻，通信ETF银华、华夏净值分别涨6.36%、6.28%，多只科技主题ETF成交额超30亿元（科创半导体ETF华夏46.12亿居首）；重仓AI的LOF同步大涨，财通科创LOF、财通升级混合LOF涨幅均超7%。<br>
          <b>停牌提示：</b>因二级市场价格明显高于基金份额净值、出现较大溢价，财通福鑫定开混合（501046）9月7日盘中起暂停交易，并公告9月8日开盘起至10:30继续临时停牌一小时；财通科创LOF、纳指ETF国泰（513100）等多只产品亦发布溢价风险提示。<br>
          <b>新品动向：</b>8月以来6只消费电子主题基金（嘉实/汇添富/广发/工银瑞信/华安等）集中上报，8家基金公司上报通信设备主题ETF，10家上报创业板算力基础设施ETF，科技产业链新品供给密集。<br>
          <b>对腾安启示：</b>科技主题基金热度与溢价风险并存，代销端须强化场内LOF/跨境ETF高溢价风险提示，引导客户避免溢价追高。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/787136" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-08</span></a>
        </div>
      </div>
    </div>
  </div>

'''
s0_pat = re.compile(
    r'<!-- ============ Section 0: 今日焦点 ============ -->.*?'
    r'(?=<!-- ============ Section 1: 重磅信息 ============ -->)',
    re.DOTALL)
html, n = s0_pat.subn(s0_new, html, count=1)
assert n == 1, 'S0 replaced {}'.format(n)
report.append('S0 今日焦点 -> 4条 (09-08/09-08/09-07/09-08)')

# ---------- 4. S6 行情速览 整块替换 ----------
s6_new = '''<!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-07）·沪指3932.70 +0.07%·创业板指涨3.41%·成交1.95万亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-07</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-07收盘·算力硬件领涨）</b><br>
              上证指数 <b>3932.70</b> <span style="color:#f5222d;">+0.07%</span><br>
              深证成指 <b>13774.91</b> <span style="color:#f5222d;">+1.91%</span><br>
              创业板指 <b>3398.68</b> <span style="color:#f5222d;">+3.41%</span><br>
              沪深两市成交 <b>1.95万亿</b>·超3100只个股上涨<br>
              算力硬件走强·CPO/PCB领涨·农业持续活跃
            </div>
            <div>
              <b>港股与美股（09-07收盘）</b><br>
              恒生指数 <b>25413.12</b> <span style="color:#52c41a;">-0.93%</span><br>
              恒生科技 <b>4527.71</b> <span style="color:#52c41a;">-0.92%</span><br>
              国企指数 <b>8429.73</b> <span style="color:#52c41a;">-1.46%</span><br>
              美股 <b>劳动节休市</b>（9-4收盘 道指53414.25 <span style="color:#52c41a;">-0.51%</span>）<br>
              纳斯达克 <b>26506.99</b> <span style="color:#52c41a;">-0.29%</span><br>
              标普500 <b>7718.60</b> <span style="color:#52c41a;">-0.38%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:8px;border-top:1px solid #f0f0f0;">
              <b>结构焦点：</b>9月7日A股三大指数集体收涨，沪指涨0.07%报3932.70，深成指涨1.91%、创业板指涨3.41%，科创50涨2.42%报1615.53，沪深两市成交1.95万亿，全市场超3100只个股上涨；算力硬件（CPO/PCB）领涨，泰金新能、迅捷兴20%涨停，农业板块持续活跃，贵金属、保险、煤炭、银行等跌幅居前。港股9月7日高开低走，恒指跌0.93%报25413.12、国企指数跌1.46%、恒生科技跌0.92%，主板成交2097亿港元；美股9月7日劳动节休市（上一交易日9月4日收盘：道指-0.51%、标普-0.38%、纳指-0.29%）。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-09-07收盘</span>
            <span class="source-tag">数据来源：人民财讯/新华社/证券时报（09-07）</span>
          </div>
      </div>  </div>
'''
s6_pat = re.compile(
    r'<!-- ============ Section 6: 市场行情速览 ============ -->.*?'
    r'(?=<!-- ============ Section 7: 关键时间线 ============ -->)',
    re.DOTALL)
html, n = s6_pat.subn(s6_new, html, count=1)
assert n == 1, 'S6 replaced {}'.format(n)
report.append('S6 行情 -> 09-07收盘 (沪3932.70+0.07%/创业+3.41%/恒指-0.93%)')

# ---------- 5. S7 时间线：顶部插2条 + 底部删2条 ----------
old_top = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-07</div>
        <div class="timeline-title">证监会就私募募集办法公开征求意见</div>
      </div>'''
new_top = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-08</div>
        <div class="timeline-title">首批18只主动ETF获批在即·10月集中募集</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-08</div>
        <div class="timeline-title">公募年内获配定增473.46亿·同比+168.71%</div>
      </div>
''' + old_top
assert html.count(old_top) == 1, 'S7 top count {}'.format(html.count(old_top))
html = html.replace(old_top, new_top)

old_bottom = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-02</div>
        <div class="timeline-title">本周12只FOF开募创9周新高·年内137只</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-01</div>
        <div class="timeline-title">盈利占比成绩单·中位数92.52%·120只满盈</div>
      </div>'''
assert html.count(old_bottom) == 1, 'S7 bottom count {}'.format(html.count(old_bottom))
html = html.replace(old_bottom, '')
report.append('S7 时间线 -> 顶部插09-08两条, 底部删09-01/09-02两条, 保持12条')

# ---------- 校验 ----------
open_div = html.count('<div')
close_div = html.count('</div>')
assert open_div == close_div, 'div 不平衡: {} vs {}'.format(open_div, close_div)
report.append('div 平衡: {}/{}'.format(open_div, close_div))

assert '\uFFFD' not in html, '存在 U+FFFD 乱码'
assert 'Section 8' not in html and '待办跟踪' not in html and '腾安行动清单' not in html, 'S8 残留'
report.append('S8 不存在 / 无乱码')

# S0 标题精确「今日焦点」
assert '<span class="section-title">今日焦点</span>' in html
assert '9月8日 · 4条今日要闻' in html
report.append('S0 标题=今日焦点, context=9月8日 · 4条今日要闻')

# 时间线条目计数（实际条目 = 计数 - 2 CSS 行）
tl = len(re.findall(r'timeline-item', html))
report.append('timeline-item 计数 {} (实际条目 {})'.format(tl, tl - 2))

with open(PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)

print('\n'.join(report))
print('\nOK - 已写入 index.html')
