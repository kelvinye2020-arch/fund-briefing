# -*- coding: utf-8 -*-
import sys

PATH = r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html'
with open(PATH, 'r', encoding='utf-8') as f:
    html = f.read()

def count_divs(s):
    return s.count('<div'), s.count('</div>')

before = count_divs(html)
print('BEFORE divs:', before)

def step(name, s, old, new):
    c = s.count(old)
    if c != 1:
        raise AssertionError('[%s] old 出现 %d 次（期望1）' % (name, c))
    return s.replace(old, new, 1)

FP_NEW = '首批二季报出炉|244只提前结募|新发转向防御|四大公募举牌创新药|公募人才流动双创新高'

# ---------- R1 marker ----------
html = step('marker', html,
    '<!-- daily-update: 2026-07-11 -->',
    '<!-- daily-update: 2026-07-13 -->')

# ---------- R2 viewport ----------
html = step('viewport', html,
    '<meta name="viewport" content="科创债ETF全面入库|创新药基金破1300亿|消费基金延长募集|发行募资6598亿|沪指高开半导体领涨">',
    '<meta name="viewport" content="%s">' % FP_NEW)

# ---------- R3 fingerprint ----------
html = step('fingerprint', html,
    '<meta name="content-fingerprint" content="科创债ETF全面入库|创新药基金破1300亿|消费基金延长募集|发行募资6598亿|沪指高开半导体领涨">',
    '<meta name="content-fingerprint" content="%s">' % FP_NEW)

# ---------- R4 date-badge ----------
html = step('date-badge', html,
    '    <div class="date-badge">\U0001F4C5 数据区间：2026.06.27 — 2026.07.11（每日更新）</div>',
    '    <div class="date-badge">\U0001F4C5 数据区间：2026.06.29 — 2026.07.13（每日更新）</div>')

# ---------- R5 S0 title ----------
html = step('s0title', html,
    '      <span class="section-title">今日焦点（7月11日·周六·二季报含科量成业绩密码·公募人才变局·7月新发121只·周五科创50暴跌5.53%）</span>',
    '      <span class="section-title">今日焦点（7月13日·周一·首批二季报出炉·年内244只提前结募·新发转向防御·四大公募举牌创新药）</span>')

# ---------- R6 stats bar (slice) ----------
NEW_STATS = '''<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">39.48万亿</div>
    <div class="stat-label">公募总规模（截至2026年5月底·首批二季报亮相·含科量成业绩密码）</div>
    <div class="stat-change up">\u25B2 同泰等首批二季报聚焦AI算力链·10年业绩首披露</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">3966.02</div>
    <div class="stat-label">上证综指 · 07-13开盘（跌0.75%·科创50-1.29%·半导体领跌）</div>
    <div class="stat-change down">\u25BC 深成指-0.92%·创业板-0.86%·油气煤炭医药逆势</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">236人</div>
    <div class="stat-label">年内基金经理离任（新聘376人·双双创同期新高）</div>
    <div class="stat-change neutral">\u25A0 去明星化提速·平台化投研建设加速</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">244只</div>
    <div class="stat-label">年内基金提前结募（远超延长募集101只·发行热度攀升）</div>
    <div class="stat-change neutral">\u25A0 7月新发转向偏债/红利/均衡防御赛道</div>
  </div>
</div>
'''
ms = html.find('<div class="stats-bar">')
me = html.find('<div class="main">')
if ms == -1 or me == -1:
    raise AssertionError('stats anchor not found')
html = html[:ms] + NEW_STATS + html[me:]

# ---------- R7 S0 cards (slice) ----------
card1 = '''      <!-- S0 Card 1: 首批公募二季报出炉·年内244只基金提前结募 (T+0 07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E0 首批公募二季报出炉·同泰4只聚焦AI算力链·年内244只基金提前结募</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>二季报开闸：</b>7月9日同泰基金旗下<b>4只</b>产品率先披露2026年二季报（同泰数字经济股票、同泰行业优选股票、同泰同欣混合、同泰恒盛债券），前十大重仓聚焦中际旭创、新易盛、海光信息、寒武纪等AI算力链，二季度末重点布局光通信、存储、芯片。<br>
          <b>提前结募成主流：</b>截至7月9日，年内提前结束募集基金达<b>244只</b>，延长募集期仅101只，打新热度与投资者认购情绪持续回暖。<br>
          <b>对基金行业影响：</b>二季报密集披露期→腾安可强化科技持仓解读与净值波动应对话术，提示单一赛道拥挤风险。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260713A02NLG00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经·腾讯新闻</span></a>
          <span class="impact-tag high">二季报：高</span>
        </div>
      </div>'''
card2 = '''      <!-- S0 Card 2: 7月新发转向防御型·偏债/红利/均衡成主线 (T+0 07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E0 7月新发转向防御型·十余家头部公募集中推偏债·权益新品远离拥挤科技转均衡</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>风格切换初现：</b>证券时报指出，7月翻倍基批量"消失"后，南方、易方达、平安、富国、广发、博时、国泰等<b>十余家头部公募</b>集中在7月下旬推出偏债类产品——平安添颐债券、天弘稳健增利债券7月13日认购，南方荣信稳健债券7月14日发行。<br>
          <b>权益降级进攻：</b>7月新发主动权益基金命名多带"均衡""多元""价值"标签，拟任经理投资偏好与算力/光通信错位、转低估值高分红；富国和信回报、易方达智享混合将权益+可转债仓位上限严控≤30%。<br>
          <b>对基金行业影响：</b>科技拥挤后资金避险→腾安需优化新发货架结构、增加偏债/红利/均衡供给。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260713014745a47a3d12" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">发行风向：中</span>
        </div>
      </div>'''
card3 = '''      <!-- S0 Card 3: 四大公募南下举牌·创新药投资升温 (T+0 07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E0 四大公募南下举牌·易方达/富国/华夏/汇添富密集举牌港股创新药·医药赛道升温</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>南下举牌：</b>6月10日至7月11日，易方达、汇添富、华夏、富国四家头部公募旗下基金密集增持港股医药公司并构成举牌——富国、易方达分别增持百奥赛图至持股超<b>7%</b>（7月2日/7日），港股创新药龙头配置价值显著抬升。<br>
          <b>逻辑切换：</b>新版国家基本药物目录落地释放政策红利，国内创新药迈入技术爆发与出海商业化兑现周期、估值处历史低位，有望承接科技赛道流出资金。<br>
          <b>对基金行业影响：</b>医药赛道机会增强→腾安可借创新药/医药主题基金补位科技拥挤后的配置缺口。
        </div>
        <div class="card-footer">
          <a href="https://news.yunnan.cn/system/2026/07/13/034079846.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·云南网</span></a>
          <span class="impact-tag medium">医药机会：中</span>
        </div>
      </div>'''
card4 = '''      <!-- S0 Card 4: 公募人才流动提速·离任新聘双创新高 (T+0 07-13) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 公募人才流动提速·年内基金经理离任236人/新聘376人均创同期新高·去明星化加速</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>流动双创新高：</b>Wind数据显示，截至7月10日年内公募基金经理离任<b>236人</b>、新聘<b>376人</b>，均创下历年同期新高；林英睿7月10日离任广发多策略/广发聚富2只，余广7月卸任在管4只基金。<br>
          <b>去明星化：</b>行业从规模扩张转向高质量发展，费率改革、薪酬新规、业绩基准管理推动下，人才从中小公募向头部公募迁移，基金公司强化平台化、系统化投研建设。<br>
          <b>对基金行业影响：</b>人才更替加速→腾安选品应更重投研平台稳定性与团队共管机制，弱化单一明星依赖。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR20260712031211151" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报</span></a>
          <span class="impact-tag medium">人才变局：中</span>
        </div>
      </div>'''
NEW_S0_CARDS = card1 + '\n' + card2 + '\n' + card3 + '\n' + card4 + '\n'

s0s = html.find('      <!-- S0 Card 1:')
s0e = html.find('    </div>\n  </div>\n<!-- ============ Section 1:')
if s0s == -1 or s0e == -1:
    raise AssertionError('S0 anchor not found')
html = html[:s0s] + NEW_S0_CARDS + html[s0e:]

# ---------- R8 S6 market card (slice) ----------
NEW_S6 = '''      <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月13日（周一）·A股集体低开·沪指跌0.75%·科创50跌1.29%·半导体领跌·油气煤炭医药逆势</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>\U0001F4CA A股07-13开盘（集体低开·交易时段）：</b><br>
              ▪ 沪指 <b>-0.75%</b>（3966.02）·深成指 <b>-0.92%</b>（14908.98）<br>
              ▪ 创业板指 <b>-0.86%</b>（3809.86）·科创50 <b>-1.29%</b>（2038.36）·沪深300 -0.74%<br>
              ▪ 板块：油气/煤炭/医药/工业气体（九丰能源涨停）逆势走强；半导体/算力硬件/PCB/先进封装/存储领跌、贵金属跌幅居前
            </div>
            <div>
              <b>\U0001F4CA 港股/美股（外围）：</b><br>
              ▪ 港股07-13低开高走：恒指 <b>+0.79%</b>（24367）·恒生科技 <b>+1.22%</b>（4779）；创新药/AI应用活跃、半导体分化<br>
              ▪ 美股07-10收盘：道指 <b>+0.29%</b>·纳指 <b>+0.29%</b>·标普 <b>+0.42%</b>；SK海力士美股首日涨超12%<br>
              ▪ 周末要闻延续：证监局基金销售合规摸底、私募《运作指引》整改7/31截止
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-13（周一开市·07-13开盘/外围07-10收盘）</span>
            <span class="source-tag">数据来源：金融界/澎湃/证券时报/东方财富</span>
          </div>
      </div>
  </div>
'''
s6t = html.find('2026年7月11日（周六）·A股/港股休市')
if s6t == -1:
    raise AssertionError('S6 title anchor not found')
s6s = html.rfind('      <div class="card p3">', 0, s6t)
s6e = html.find('<!-- ============ Section 7:')
if s6s == -1 or s6e == -1:
    raise AssertionError('S6 anchor not found')
html = html[:s6s] + NEW_S6 + html[s6e:]

# ---------- R9 S7 timeline: insert 07-13 + remove 06-29 ----------
NEW_S7_ITEM = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-07-13（首批二季报出炉·年内244只提前结募·7月新发转向防御·四大公募南下举牌创新药·公募人才流动双创新高）</div>
          <div class="timeline-title">首批公募二季报亮相（同泰4只聚焦AI算力）·年内244只基金提前结募 / 7月新发转向偏债红利均衡防御 / 四大公募南下举牌港股创新药 / 基金经理离任新聘双创新高</div>
          <div class="timeline-desc">7月13日，公募首批二季报出炉（同泰旗下4只产品率先披露，前十大重仓聚焦中际旭创、新易盛、海光信息等AI算力链），截至7月9日年内提前结募基金达244只、远超延长募集101只；7月新发风向转向偏债/红利/均衡等防御赛道，十余家头部公募7月下旬集中推偏债产品，主动权益新品远离拥挤科技、转均衡价值。同日，易方达、富国、华夏、汇添富四大公募密集南下举牌港股创新药公司（富国/易方达增持百奥赛图超7%举牌），创新药承接科技流出；截至7月10日年内基金经理离任236人、新聘376人均创同期新高，去明星化与平台化投研加速。A股集体低开，沪指-0.75%、半导体/算力硬件领跌，油气煤炭医药逆势。</div>
        </div>
      </div>'''
anchor_s7 = '      <!-- 07-11 时间线条目 (NEW) -->'
if html.count(anchor_s7) != 1:
    raise AssertionError('S7 anchor 07-11 出现 %d 次' % html.count(anchor_s7))
html = html.replace(anchor_s7, '      <!-- 07-13 时间线条目 (NEW) -->\n' + NEW_S7_ITEM + '\n\n' + anchor_s7, 1)

s7_start = html.find('      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-29（')
s7_end = html.find('      <!-- 06-30 时间线条目')
if s7_start == -1 or s7_end == -1:
    raise AssertionError('S7 06-29 anchor not found (start=%d end=%d)' % (s7_start, s7_end))
html = html[:s7_start] + html[s7_end:]

# ---------- R10 S8: insert new action card ----------
NEW_S8_CARD = '''      <!-- S8 Card NEW: 7月新发转向防御型·偏债红利均衡 (07-13) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E0 7月新发转向防御型·偏债/红利/均衡成主线·腾安需优化新发货架结构并提示科技拥挤</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>证券时报指出，7月翻倍基批量"消失"后，南方、易方达、平安、富国、广发、博时、国泰等十余家头部公募集中在7月下旬推出偏债类产品，权益新发拟任经理转均衡/价值红利、规避拥挤科技；富国和信回报、易方达智享混合将权益+可转债仓位上限严控≤30%。<br>
          <b>腾安行动建议：</b>① 优化新发货架结构，增加偏债/红利/均衡供给、匹配避险需求；② 同步提示科技基金高位拥挤与波动风险，引导哑铃配置；③ 结合二季报与分红潮强化"获得感"叙事。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 优化新发货架结构→产品部<br>
            ② 提示科技拥挤风险→投顾部<br>
            ③ 引导哑铃均衡配置→营销部
          </div>
        </div>
      </div>'''
anchor_s8 = '      <!-- S8 Card NEW: 二季报披露季开启·含科量成业绩密码 (07-11) -->'
if html.count(anchor_s8) != 1:
    raise AssertionError('S8 anchor 出现 %d 次' % html.count(anchor_s8))
html = html.replace(anchor_s8, NEW_S8_CARD + '\n\n' + anchor_s8, 1)

# ---------- balance check (global opens must equal closes) ----------
after = count_divs(html)
print('AFTER divs:', after)
if after[0] != after[1]:
    raise AssertionError('div全局不平衡: opens=%s closes=%s' % (after[0], after[1]))

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print('OK written, divs balanced (%d/%d)' % after)
