# -*- coding: utf-8 -*-
# 基金行业资讯看板 每日更新 - 2026-07-13 (周一)
# 整块替换（含开闭标签）避免 div 失衡；逐步打印平衡，仅当平衡才写盘。
import io, sys

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

def bal(s):
    return s.count("<div"), s.count("</div>")

base_o, base_c = bal(html)
print("BASE div: open=%d close=%d" % (base_o, base_c))

def step(name, new_html, old, new):
    assert new_html.count(old) == 1, "[%s] old 出现 %d 次" % (name, new_html.count(old))
    o, c = bal(new_html)
    new_html = new_html.replace(old, new, 1)
    o2, c2 = bal(new_html)
    print("[%s] delta open=%+d close=%+d  -> now %d/%d" % (name, o2-o, c2-c, o2, c2))
    return new_html

new_html = html

# R1 marker
new_html = step("marker", new_html,
    "<!-- daily-update: 2026-07-11 -->",
    "<!-- daily-update: 2026-07-13 -->")

# R2 viewport
new_html = step("viewport", new_html,
    '<meta name="viewport" content="科创债ETF全面入库|创新药基金破1300亿|消费基金延长募集|发行募资6598亿|沪指高开半导体领涨">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">')

# R3 fingerprint
new_html = step("fingerprint", new_html,
    '<meta name="content-fingerprint" content="科创债ETF全面入库|创新药基金破1300亿|消费基金延长募集|发行募资6598亿|沪指高开半导体领涨">',
    '<meta name="content-fingerprint" content="二季报首披长期业绩|K型分化218pct|提前结募244只|沪指低开半导体领跌">')

# R4 Stats Bar
STATS_OLD = '''<!-- Stats Bar -->
<div class="stats-bar">
  <div class="stat-card">
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
  </div>
</div>
<div class="main">'''
STATS_NEW = '''<!-- Stats Bar -->
<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">39.48万亿</div>
    <div class="stat-label">公募总规模（截至2026年5月底·二季报披露季·科技持仓主导）</div>
    <div class="stat-change up">▲ 二季报首披7/10年长期业绩·高仓位重仓AI</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">3966.02</div>
    <div class="stat-label">上证综指 · 07-13开盘（跌0.75%·科创50-1.29%·半导体领跌）</div>
    <div class="stat-change down">▼ 深成指-0.92%·创业板-0.86%·油气煤炭医药逆势</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">90.24%</div>
    <div class="stat-label">已披露主动权益基金平均股票仓位（二季报·维持高仓位）</div>
    <div class="stat-change neutral">■ 重仓AI算力链·基金经理提示估值风险</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">244只</div>
    <div class="stat-label">年内提前结募基金（权益占大半·日光基集中量化/FOF/REITs）</div>
    <div class="stat-change neutral">■ 提前结募244只 vs 延长101只</div>
  </div>
</div>
<div class="main">'''
new_html = step("stats", new_html, STATS_OLD, STATS_NEW)

# R5 S0 title
new_html = step("s0title", new_html,
    '      <span class="section-title">今日焦点（7月11日·周六·二季报含科量成业绩密码·公募人才变局·7月新发121只·周五科创50暴跌5.53%）</span>',
    '      <span class="section-title">今日焦点（7月13日·周一·二季报首披7/10年长期业绩·K型分化218pct·年内244只提前结募·A股低开半导体领跌）</span>')

# R6 S0 四张旧卡 -> 三张新卡（整块替换：从 Card1 注释到 Card4 关闭标签）
S0_OLD = '''      <!-- S0 Card 1: 公募二季报披露拉开帷幕·含科量成业绩密码 (T+0 07-11) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露拉开帷幕·含科量成业绩密码·10只主动权益8只Q2净值增长超70%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>二季报开闸：</b>截至7月10日，已有同泰、红土创新、中银旗下<b>13只</b>基金披露2026年二季报，10只主动权益类基金报告期内均实现净值正增长，其中<b>8只Q2净值增长率超70%</b>。同泰数字经济股票A、同泰行业优选股票A Q2分别增长<b>101.98%</b>、<b>73.62%</b>；盖俊龙管理的红土创新多只产品Q2增长率均超90%；前十大重仓普遍含中际旭创、新易盛、东山精密等AI算力链。<br>
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
      </div>'''
S0_NEW = '''      <!-- S0 Card 1: 公募二季报披露大幕拉开·首披7/10年长期业绩·高仓位重仓AI (T+0 07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露大幕拉开·首披7/10年长期业绩·高仓位90.24%重仓AI·基金经理提示估值风险</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>二季报开闸：</b>截至7月12日，金信、红土创新、同泰、华富等<b>23只</b>产品率先披露2026年二季报；为响应信披新规，金信转型创新成长等<b>首批产品首次披露7年、10年长期业绩</b>，意在扭转"过度聚焦短期业绩"怪象、引导长期投资。<br>
          <b>高仓位重仓AI：</b>已披露主动权益基金二季末平均股票仓位<b>90.24%</b>（较一季度微升0.16pct）；红土创新多只产品维持94%+仓位，国产芯片/光通信/半导体设备获加仓，同泰数字经济前十大重仓多为AI算力链核心标的。<br>
          <b>对基金行业影响：</b>二季报强化"含科量"业绩叙事→腾安可借二季报做科技持仓解读与持营，同时提示科技高位估值波动风险、引导哑铃配置。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260713A038F000" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·证券日报</span></a>
          <a href="https://www.chnfund.com/article/AR20260712041135513" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <span class="impact-tag high">二季报：高</span>
        </div>
      </div>

      <!-- S0 Card 2: 上半年K型分化·199只科技基翻倍 vs 消费基腰斩·首尾差218pct (T+0 07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 上半年K型分化·199只科技基翻倍 vs 消费基腰斩·首尾业绩差高达218个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>科技赚钱效应：</b>经济参考报统计，截至6月30日全市场<b>199只</b>主动权益基金业绩翻倍，方正富邦核心优势A以<b>183.7%</b>领跑；AI算力链驱动的硬科技成上半年主线。<br>
          <b>消费深蹲：</b>首尾业绩差值高达约<b>218个百分点</b>，信澳博见成长A上半年跌<b>34.8%</b>居首；近三成亏损超20%基金重仓白酒/家电，消费主题基金规模从1.1万亿腰斩至5150亿。<br>
          <b>对基金行业影响：</b>极端分化警示单一赛道风险→腾安选品应强化"景气成长+低估值价值"哑铃配置与投资者教育，避免追涨杀跌。
        </div>
        <div class="card-footer">
          <a href="https://cj.sina.com.cn/article/norm_detail?url=https%3A%2F%2Ffinance.sina.com.cn%2Fjjxw%2F2026-07-13%2Fdoc-inihrhff7493453.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济参考报·新浪财经</span></a>
          <span class="impact-tag high">业绩分化：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 年内244只基金提前结募·权益占大半·日光基集中量化/FOF/REITs (T+0 07-13) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 年内244只基金提前结募·权益占大半·"日光基"集中量化/FOF/REITs指数</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>结募提速：</b>Wind数据显示，截至7月9日年内提前结束募集基金达<b>244只</b>（去年同期199只），延长募集期仅<b>101只</b>；权益产品占大半，其中被动指数80只、增强指数11只、主动偏股46只。<br>
          <b>"日光基"主线：</b>提前结募的日光基主要集中在公募量化基金、FOF以及首批REITs指数基金等热门赛道，发行端结构分化加剧。<br>
          <b>对基金行业影响：</b>提前结募升温→腾安可顺势丰富权益/指数/FOF货架，把握新发热度与持营窗口。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1N0QFAJ0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">发行热度：中</span>
        </div>
      </div>'''
new_html = step("s0cards", new_html, S0_OLD, S0_NEW)

# R7 S6 整块替换（含 card 开闭标签）
S6_OLD = '''      <div class="card p3">
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
      </div>'''
S6_NEW = '''      <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月13日（周一）·A股三大股指集体低开·沪指跌0.75%·半导体/算力硬件领跌·油气煤炭医药逆势</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-13开盘（集体低开）：</b><br>
              ▪ 沪指 <b>-0.75%</b>（3966.02）·深成指 <b>-0.92%</b>（14908.98）<br>
              ▪ 创业板指 <b>-0.86%</b>（3809.86）·科创50 <b>-1.29%</b>（2038.36）·科创综指 <b>-1.19%</b><br>
              ▪ 盘面上：半导体/算力硬件产业链调整，存储器/PCB/先进封装领跌；电子特气概念高开（九丰能源2连板）<br>
              ▪ 逆势：油气/煤炭/医药走强；两市1221涨、3716跌
            </div>
            <div>
              <b>📊 港股/美股（隔夜·周末无交易）：</b><br>
              ▪ 港股07-10收盘：恒指 <b>+0.6%</b>·恒生科技 <b>-0.21%</b><br>
              ▪ 美股07-10收盘：道指 <b>+0.29%</b>·纳指 <b>+0.29%</b>·标普 <b>+0.42%</b>；英伟达+3.5%重回5万亿、Meta+6%、SK海力士+13%<br>
              ▪ 本周焦点：二季报密集披露·科技高位波动·A股4000点下方缩量整理<br><br>
              <b>📌 周末要闻：</b>① 公募二季报大幕拉开·首披7/10年业绩；② 年内244只基金提前结募；③ 证监局基金销售合规摸底延续；④ 信披新规落地。
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-13（07-13开盘·美股07-10收盘）</span>
            <span class="source-tag">数据来源：金融界/澎湃/上证报·07-13开盘</span>
          </div>
      </div>'''
new_html = step("s6", new_html, S6_OLD, S6_NEW)

# R8 S7：新增07-13条目（插入到 07-11 条目之前）+ 删除06-29过期条目
assert new_html.count('      <!-- 07-11 时间线条目 (NEW) -->') == 1
NEW_0713 = '''      <!-- 07-13 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-07-13（二季报首披7/10年长期业绩·高仓位90.24%重仓AI·K型分化218pct·年内244只提前结募·A股低开半导体领跌）</div>
          <div class="timeline-title">公募二季报大幕拉开·首批产品首披7/10年长期业绩 / 已披露主动权益平均仓位90.24%重仓AI / 上半年199只科技基翻倍·首尾差218pct / A股三大股指集体低开</div>
          <div class="timeline-desc">7月13日，公募基金二季报披露大幕拉开：金信、红土创新、同泰等23只产品率先披露，为响应信披新规，金信转型创新成长等首批产品首次披露7年、10年长期业绩，引导长期投资；已披露主动权益基金二季末平均股票仓位90.24%、重仓国产芯片/光通信/半导体设备等AI算力链，基金经理同步提示科技板块估值风险。同日，经济参考报揭示上半年K型分化：199只科技基翻倍、首尾业绩差218pct、消费主题基金规模腰斩；年内244只基金提前结募、权益占大半。A股三大股指集体低开，沪指-0.75%、半导体/算力硬件领跌、油气煤炭医药逆势。</div>
        </div>
      </div>
'''
o, c = bal(new_html)
new_html = new_html.replace('      <!-- 07-11 时间线条目 (NEW) -->', NEW_0713 + '\n      <!-- 07-11 时间线条目 (NEW) -->', 1)
o2, c2 = bal(new_html)
print("[s7add] delta open=%+d close=%+d -> now %d/%d" % (o2-o, c2-c, o2, c2))

OLD_0629 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-29（公募基准改革全面铺开·FOF单周发行环比+175%·央行4575亿逆回购·中考倒计时）</div>
          <div class="timeline-title">公募基金第二批基准调整全面铺开 / 年内前十基金均已限购 / FOF单周发行环比+175%·年内新发FOF破100只 / 央行4575亿逆回购对冲半年末流动性</div>
          <div class="timeline-desc">6月26日第二批千余只公募基金基准调整公告落地，改革从"试点"转入"全面铺开"，年内收益前十基金全部限购。本周47只新基金启动募集，FOF赛道11只新品环比+175%，年内新发FOF破100只。央行6月29日开展1575亿7天期+3000亿隔夜逆回购，合计4575亿，精准对冲半年末流动性压力。基金中考倒计时，126只翻倍基业绩即将锁定。</div>
        </div>
      </div>
'''
assert new_html.count(OLD_0629) == 1, "06-29 block 未找到或重复"
o, c = bal(new_html)
new_html = new_html.replace(OLD_0629, "", 1)
o2, c2 = bal(new_html)
print("[s7del0629] delta open=%+d close=%+d -> now %d/%d" % (o2-o, c2-c, o2, c2))

# R9 S8 card1 整块替换
S8_OLD = '''      <!-- S8 Card NEW: 二季报披露季开启·含科量成业绩密码 (07-11) -->
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
      </div>'''
S8_NEW = '''      <!-- S8 Card NEW: 二季报披露·首披长期业绩·高仓位重仓AI·提示估值风险 (07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募二季报披露季·首披7/10年长期业绩·高仓位90.24%重仓AI·腾安需做持仓解读并提示估值风险</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>截至7月12日金信、红土创新、同泰等23只产品率先披露二季报；响应信披新规，首批产品首披7年/10年长期业绩；已披露主动权益平均仓位90.24%、重仓AI算力链，基金经理同步提示科技板块估值风险。<br>
          <b>腾安行动建议：</b>① 借二季报强化科技持仓解读与持营话术；② 提示单一赛道拥挤与高位波动、引导哑铃配置；③ 借"长期业绩披露"契机强化长期持有投教。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 准备科技持仓解读话术→投顾部<br>
            ② 提示拥挤交易与估值风险→营销部<br>
            ③ 借长期业绩披露做长期持有投教→投顾部
          </div>
        </div>
      </div>'''
new_html = step("s8card1", new_html, S8_OLD, S8_NEW)

# 最终校验
o, c = bal(new_html)
print("FINAL div: open=%d close=%d %s" % (o, c, "BALANCED" if o == c else "MISMATCH!!!"))
if o != c:
    print("未写盘（div 失衡）")
    sys.exit(2)

# 关键标记校验
for must in ["<!-- daily-update: 2026-07-13 -->",
             "数据区间：2026.06.29 — 2026.07.13",
             "今日焦点（7月13日·周一",
             "二季报披露大幕拉开·首披7/10年长期业绩",
             "2026年7月13日（周一）·A股三大股指集体低开",
             "2026-07-13（二季报首披7/10年长期业绩",
             "二季报披露季·首披7/10年长期业绩·高仓位90.24%"]:
    assert must in new_html, "缺失关键标记: " + must
assert "2026-06-29（公募基准改革全面铺开" not in new_html, "06-29 时间线条目未删除"

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(new_html)
print("WRITE OK ->", PATH)
