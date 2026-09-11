#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-11
更新：header 区间 / Stats Bar 沪指卡 / S0 今日焦点(4条 T+0 09-11) / S6 行情(09-10收盘) / S7 时间线
S1/S2 均在 T-14 窗内不动；S8 永久废弃不重建。
"""
import re
import sys
from datetime import date, timedelta

HTML = 'index.html'
TODAY = date.today()
UPPER = TODAY.strftime('%Y.%m.%d')
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
BADGE = '\U0001F4C5 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)
MON, DAY = TODAY.month, TODAY.day
CONTEXT = '%d月%d日 · 4条今日要闻' % (MON, DAY)

src = open(HTML, encoding='utf-8').read()
orig = src
o_before = src.count('<div')
c_before = src.count('</div>')


# ---------------- helpers ----------------
def die(msg):
    print('ASSERT FAIL: ' + msg)
    sys.exit(1)


def block_end(s, start):
    """从 start 处的 <div ...> 起做嵌套深度扫描，返回该 div 闭合后的下标"""
    i = s.index('>', start) + 1
    depth = 1
    tag = re.compile(r'<(/?)div\b')
    while depth > 0:
        m = tag.search(s, i)
        if not m:
            die('depth scan 未闭合')
        depth += -1 if m.group(1) else 1
        i = m.end()
    return i


# ================= Phase 1: 断言 =================
if '<div class="card p1">' in src and False:
    pass
if 'S8' in src or '待办跟踪' in src or '腾安行动清单' in src:
    die('S8 残留')
# 锚点唯一性
for anchor in [
    '\U0001F4C5 数据区间：',
    '<div class="stat-number">3951.51</div>',
    '<!-- ============ Section 0: 今日焦点 ============ -->',
    '<!-- ============ Section 1: 重磅信息 ============ -->',
    '<!-- ============ Section 6: 市场行情速览 ============ -->',
    '<!-- ============ Section 7: 关键时间线 ============ -->',
    '<div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">',
]:
    n = src.count(anchor)
    if n != 1:
        die('锚点 %r 出现 %d 次（应为1）' % (anchor[:40], n))

# ================= Step 1: header 数据区间 =================
src, k = re.subn(r'\U0001F4C5 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', BADGE, src)
if k != 1:
    die('header badge 替换 %d 次' % k)
if BADGE not in src:
    die('badge 未生效')

# ================= Step 2: Stats Bar 沪指卡 =================
old_stat = src[src.index('    <div class="stat-card">\n      <div class="stat-number">3951.51</div>'):]
old_stat = old_stat[:old_stat.index('</div>\n    </div>') + len('</div>\n    </div>')]
new_stat = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3934.40</div>\n'
    '      <div class="stat-label">沪指9-10收盘·跌0.43%·全市场成交1.66万亿·创年内次低</div>\n'
    '      <div class="stat-change down">\u25bc 银行电力逆势走强·超4500只个股下跌</div>\n'
    '    </div>'
)
src = src.replace(old_stat, new_stat, 1)
sb_a = src.index('<div class="stats-bar">')
sb_b = src.index('<div class="main">', sb_a)
sb = src[sb_a:sb_b]
if '3934.40' not in sb or '3951.51' in sb:
    die('Stats Bar 沪指卡未更新')
if sb.count('<div class="stat-card">') != 4:
    die('Stats Bar 卡片数 %d != 4' % sb.count('<div class="stat-card">'))

# ================= Step 3: S0 整段替换（含 header） =================
s0a = src.index('<!-- ============ Section 0: 今日焦点 ============ -->')
s0b = src.index('<!-- ============ Section 1: 重磅信息 ============ -->')

LINK = '<a href="%s" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">%s</span></a>'

u_nbd_1 = 'https://www.nbd.com.cn/articles/2026-09-10/4577996.html'
u_cctv = 'https://ysxw.cctv.cn/article.html?item_id=13958200907971874126'
u_10jq = 'https://stock.10jqka.com.cn/20260911/c679801050.shtml'
u_qq_mrjj = 'https://news.qq.com/rain/a/20260911A03C7200'
u_nbd_2 = 'https://www.nbd.com.cn/articles/2026-09-11/4578687.html'

card1 = '''      <!-- S0 Card 1 (09-11 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">\U0001F534 金融强国“十五五”规划出台·证监会：大力发展权益类公募基金·抓紧修订证券投资基金法</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          每经网9月11日报道（记者杨建）：9月10日下午国新办“开局起步‘十五五’”主题发布会上，证监会副主席李超介绍“十五五”资本市场八个“进一步”重点任务——《金融强国建设“十五五”规划》已于近日正式出台。<br><b>与公募直接相关：</b>李超明确，将持续健全“长钱长投”的市场机制和生态，<b>推动中长期资金稳步提升入市规模和比例，大力发展权益类公募基金</b>，强化各类中长期资金“稳定器”功能；同时抓紧推动<b>证券投资基金法</b>、上市公司监管条例等重要法律法规的制定修改，修订后的证券公司监管条例有望于近期出台。<br><b>资金端数据：</b>据央视新闻，今年以来社保、年金、保险等中长期资金合计净买入A股<b>超6000亿元</b>，持有A股流通市值较2025年底<b>增长12.5%</b>；今年前8个月查办证券期货违法案件644件、罚没98.4亿元，为投资者挽回损失51.5亿元。<br><b>对腾安启示：</b>“大力发展权益类公募基金”写入金融强国顶层规划，权益产品供给与投资者回报考核进入政策红利期；建议提前布局权益基金持营工具，并跟踪证券投资基金法修订对销售适当性义务的连带影响。
        </div>
        <div class="card-footer">
          LINK1
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 产品→借“大力发展权益类公募基金”政策口径梳理权益基金池，首页增加长周期（3年/5年）收益与最大回撤展示；<br>
            ② 合规→证券投资基金法修订已列入证监会立法计划，提前梳理销售适当性、风险揭示与信息披露留痕流程，预留系统改造窗口；<br>
            ③ 内容→把“中长期资金净买入超6000亿、持股市值较去年底+12.5%”转化为“长钱长投”投教素材，强化长期持有心智。
          </div>
        </div>
      </div>
'''.replace('LINK1', LINK % (u_nbd_1, '每日经济新闻·09-11') + '\n          ' + LINK % (u_cctv, '央视新闻·09-10') + '\n          ' + LINK % (u_10jq, '同花顺·09-11'))

card2 = '''
      <!-- S0 Card 2 (09-11 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 头部公募争相布局“白盒固收+”·二级债基规模超2.28万亿·易方达汇添富中欧在列</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月11日（记者肖芮冬）：2026年二级债基规模持续走高，截至二季度末净值超<b>2.28万亿元</b>，“白盒固收+”成为行业新趋势。<br><b>产品逻辑：</b>区别于传统看不清权益配置的“黑盒固收+”，“白盒固收+”底仓为债券，权益部分<b>聚焦科技、消费、周期等明确赛道</b>，投资者可清晰知晓权益敞口；今年以来易方达、汇添富、中欧等头部公募纷纷通过增聘赛道型基金经理或发行新产品布局该方向。<br><b>风险面：</b>“白盒固收+”权益风格集中，行情不顺时回撤会高于均衡配置产品；业内人士提醒“风格清晰不等于风险更低”，普通投资者需匹配自身风险承受能力，勿盲目入场。<br><b>对腾安启示：</b>“固收+”正从黑盒走向透明化，选品维度需从“历史最大回撤”扩展到“权益敞口赛道标签”；建议给固收+产品打上赛道标签并在持仓页明示权益暴露，降低预期差客诉。
        </div>
        <div class="card-footer">
          LINK2
          <span class="impact-tag medium">产品：中</span>
        </div>
      </div>
'''.replace('LINK2', LINK % (u_qq_mrjj, '腾讯新闻·09-11'))

card3 = '''
      <!-- S0 Card 3 (09-11 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 全市场ETF规模4.90万亿·9月10日3只ETF净流入均超8亿·科创50逆势吸金</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          每经网9月11日（记者肖芮冬）：Wind数据显示，截至9月10日，全市场ETF份额<b>33993.43亿份</b>、总规模<b>48959.36亿元</b>（约4.90万亿元）。<br><b>9月10日净流入前三：</b>短融ETF海富通 +16.17亿元（份额增0.14亿份）、科创50ETF华夏 +8.52亿元（增5.13亿份）、恒生科技ETF华泰柏瑞 +8.05亿元（增14.97亿份）。<br><b>净流出前三：</b>上证50ETF华夏 -3.88亿元、A500ETF易方达 -2.94亿元、创新药ETF银华南方 -1.95亿元。<br><b>结构线索：</b>近一周份额增加最大的行业为金融（33只基金跟踪），主题为上证科创板芯片指数（11只），指数标的为科创50（20只）；收益最高的指数标的为智选船舶产业（+9.08%）。<br><b>对腾安启示：</b>调整市中资金呈“防御+逆势加仓科技”双线——短融与红利类承接避险，科创50/恒生科技获逆势申购；建议在这两条线上分别备好低波动持有与网格定投的推荐话术。
        </div>
        <div class="card-footer">
          LINK3
          <span class="impact-tag low">资金：中</span>
        </div>
      </div>
'''.replace('LINK3', LINK % (u_nbd_2, '每日经济新闻·09-11'))

card4 = '''
      <!-- S0 Card 4 (09-11 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 17只基金连续3年获员工自购增持·合计份额3年增超2.5倍·户均达中位数10倍</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月11日：截至6月末，有基金公司员工持仓的主动权益基金共计<b>4580余只</b>、合计持有份额超<b>54亿份</b>，与2025年末相比产品数量增长4.95%、持有总份额增长1.67%；其中<b>17只基金连续3年获基金公司员工增持</b>。<br><b>强度对比：</b>17只基金单只平均员工持有份额约<b>298万份</b>，是全部有员工持仓的主动权益基金份额中位数27.9万份的<b>十倍以上</b>；合计持有份额从2022年末约1443万份增至2026年6月末<b>5070万份</b>，累计增长超2.5倍。<br><b>对腾安启示：</b>“员工自购且连续增持”是市场上少有的可量化验证的利益绑定信号，可加工成“与持有人共进退”选基标签；但须同步提示自购不等于业绩承诺，仅作筛选参考而非推荐依据。
        </div>
        <div class="card-footer">
          LINK4
          <span class="impact-tag low">选品：中</span>
        </div>
      </div>
'''.replace('LINK4', LINK % (u_qq_mrjj, '腾讯新闻·09-11'))

S0_NEW = '''                <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">\U0001F525</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">CTX</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
C1
C2
C3
C4

    </div>
  </div>

'''.replace('CTX', CONTEXT).replace('C1', card1).replace('C2', card2).replace('C3', card3).replace('C4', card4)

src = src[:s0a] + S0_NEW + src[s0b:]

# S0 断言
s0a2 = src.index('<!-- ============ Section 0: 今日焦点 ============ -->')
s0b2 = src.index('<!-- ============ Section 1: 重磅信息 ============ -->')
seg0 = src[s0a2:s0b2]
if seg0.count('<span class="section-title">今日焦点</span>') != 1:
    die('S0 section-title 不唯一/不精确')
if ('<span class="section-context">%s</span>' % CONTEXT) not in seg0:
    die('S0 section-context 未更新为 %s' % CONTEXT)
if seg0.count('<div class="card p') != 4:
    die('S0 卡片数 %d != 4' % seg0.count('<div class="card p'))
if seg0.count('<span class="date-tag">09-11</span>') != 4:
    die('S0 非全 T+0')
if seg0.count('<div class="action-box">') != 1:
    die('S0 P0 action-box 数 %d != 1' % seg0.count('<div class="action-box">'))
if seg0.count('href="http') != 6:
    die('S0 链接数 %d != 6' % seg0.count('href="http'))
if seg0.count('class="card-meta"') != 4:
    die('S0 card-meta 数异常')
for bad in ['stcn', 'cls.cn', '21jingji', 'yicai', 'toutiao', 'so.html5.qq.com', '\ufffd']:
    if bad in seg0:
        die('S0 命中黑名单/乱码：' + bad)

# ================= Step 4: S6 行情卡 =================
s6a = src.index('<!-- ============ Section 6: 市场行情速览 ============ -->')
ca = src.index('<div class="card p3">', s6a)
cb = block_end(src, ca)
new_s6 = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 上一交易日收盘（2026-09-10）·沪指3934.40 -0.43%·全市场成交1.66万亿创年内次低</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-10</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-10收盘·缩量磨底）</b><br>
              上证指数 <b>3934.40</b> <span style="color:#52c41a;">-0.43%</span><br>
              深证成指 <b>13617.67</b> <span style="color:#52c41a;">-0.77%</span><br>
              创业板指 <b>3338.42</b> <span style="color:#52c41a;">-0.49%</span><br>
              科创综指 <span style="color:#52c41a;">-1.12%</span><br>
              北证50 <span style="color:#52c41a;">-2.81%</span><br>
              全市场成交 <b>1.66万亿</b>·较上日缩量2107亿·连续4日低于2万亿<br>
              仅955只个股上涨·40只涨停·4512只下跌·13只跌停
            </div>
            <div>
              <b>港股与美股（09-10收盘）</b><br>
              恒生指数 <b>24954.47</b> <span style="color:#52c41a;">-1.27%</span><br>
              恒生科技 <b>4330.49</b> <span style="color:#52c41a;">-2.04%</span><br>
              国企指数 <b>8274.78</b> <span style="color:#52c41a;">-1.13%</span><br>
              道琼斯 <b>52064.10</b> <span style="color:#52c41a;">-0.60%</span><br>
              纳斯达克 <b>26081.72</b> <span style="color:#52c41a;">-0.65%</span><br>
              标普500 <b>7591.70</b> <span style="color:#52c41a;">-0.58%</span><br>
              布伦特原油107.63美元 +6.34%·现货黄金4314.82美元 -1.91%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>缩量磨底、防御占优——申万一级行业中仅银行（+1.53%）、建筑材料（+0.62%）、公用事业（+0.45%）、非银金融（+0.27%）上涨，农林牧渔（-3.11%）、汽车（-2.12%）、美容护理（-1.93%）领跌；沪深两市主力资金净流出131.21亿元，较前一交易日扩大。ETF资金呈“防御+逆势加科技”双线：短融ETF海富通净流入16.17亿元居首，科创50ETF华夏、恒生科技ETF华泰柏瑞净流入均超8亿元。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-10收盘</span>
          <span class="source-tag">数据来源：中国证券报/中国经济网/每日经济新闻（09-10—09-11）</span>
        </div>
      </div>'''
src = src[:ca] + new_s6 + src[cb:]
if '3934.40' not in src[src.index('<!-- ============ Section 6'):src.index('</body>')]:
    die('S6 未更新')
if '2026-09-09' in src[src.index('<!-- ============ Section 6'):src.index('<!-- ============ Section 7')]:
    die('S6 残留旧日期 09-09')

# ================= Step 5: S7 时间线 =================
s7a = src.index('<!-- ============ Section 7: 关键时间线 ============ -->')
tl = src.index('<div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">', s7a)
te = block_end(src, tl)

items = [
    ('red', '2026-09-11', '金融强国“十五五”规划正式出台'),
    ('blue', '2026-09-11', '公募布局白盒固收+·规模超2.28万亿'),
    ('red', '2026-09-10', 'A股缩量调整·成交创年内次低'),
    ('red', '2026-09-10', '易方达4只ETF以TDR登陆泰交所'),
    ('red', '2026-09-10', '新基金低位快速建仓·9月99只'),
    ('blue', '2026-09-10', '粮食畜牧ETF走强·最高涨超20%'),
    ('red', '2026-09-09', '中金获批控股东兴基金信达澳亚'),
    ('red', '2026-09-09', '首批8只北交所三个月持有期基金获批'),
    ('red', '2026-09-09', '公募权益仓位94.15%·有色获增持'),
    ('red', '2026-09-09', '瑞银基金销售暂停·10家公募终止合作'),
    ('red', '2026-09-08', '首批18只主动ETF获批在即·10月集中募集'),
    ('red', '2026-09-07', '证监会就私募募集办法公开征求意见'),
]
for _, d, t in items:
    if len(t) > 25:
        die('S7 标题超25字：%s（%d）' % (t, len(t)))
dates = [d for _, d, _ in items]
if dates != sorted(dates, reverse=True):
    die('S7 未降序')

body = ''
for color, d, t in items:
    body += ('      <div class="timeline-item">\n'
             '        <div class="timeline-dot %s"></div>\n'
             '        <div class="timeline-date">%s</div>\n'
             '        <div class="timeline-title">%s</div>\n'
             '      </div>\n\n' % (color, d, t))
new_tl = ('<div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">\n'
          + body + '    </div>')
src = src[:tl] + new_tl + src[te:]

s7a2 = src.index('<!-- ============ Section 7: 关键时间线 ============ -->')
seg7 = src[s7a2:src.index('</body>')]
n_item = seg7.count('<div class="timeline-item">')
if n_item != 12:
    die('S7 条目 %d != 12' % n_item)
if seg7.count('timeline-desc') != 0:
    die('S7 残留 timeline-desc')
t14 = TODAY - timedelta(days=14)
for m in re.finditer(r'<div class="timeline-date">(\d{4})-(\d{2})-(\d{2})</div>', seg7):
    dt = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if dt < t14 or dt > TODAY:
        die('S7 日期越界 %s' % dt)

# ================= Phase 2: 全局断言 =================
o_after = src.count('<div')
c_after = src.count('</div>')
print('div open  %d -> %d (drift %+d)' % (o_before, o_after, o_after - o_before))
print('div close %d -> %d (drift %+d)' % (c_before, c_after, c_after - c_before))
if o_after != c_after:
    die('div 不平衡 %d/%d' % (o_after, c_after))
if 'S8' in src or '待办跟踪' in src or '腾安行动清单' in src:
    die('S8 残留')
if '\ufffd' in src:
    die('U+FFFD 乱码')
if src.count('<!-- ============ Section 0') != 1 or src.count('<!-- ============ Section 7') != 1:
    die('section marker 重复')
for bad in ['stcn.com', 'cls.cn', '21jingji', 'yicai.com', 'toutiao', 'so.html5.qq.com', 'guba.eastmoney']:
    if bad in src:
        die('全文件黑名单命中：' + bad)
# 全文件 date-tag T-14
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
    dt = date(TODAY.year, int(m.group(1)), int(m.group(2)))
    if dt < t14:
        die('date-tag 超 T-14：%s' % dt)

open(HTML, 'w', encoding='utf-8').write(src)
print('WRITE OK  badge=%s  context=%s' % (BADGE, CONTEXT))
