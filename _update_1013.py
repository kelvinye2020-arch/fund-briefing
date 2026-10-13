#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update-2026-10-13 —— 基金看板每日更新（周二）"""
import re, sys
from datetime import date, timedelta

P = 'index.html'
TODAY = date.today()
CUTOFF = TODAY - timedelta(days=14)
EMO = '\U0001F4C5'

src = open(P, encoding='utf-8').read()
o0, c0 = len(re.findall(r'<div\b', src)), len(re.findall(r'</div>', src))
print('base div open=%d close=%d size=%d' % (o0, c0, len(src)))

def drift(tag):
    o, c = len(re.findall(r'<div\b', src)), len(re.findall(r'</div>', src))
    print('  [%s] open=%d(%+d) close=%d(%+d)' % (tag, o, o - o0, c, c - c0))

# ================= Step 0: marker / badge / fingerprint =================
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
             '<!-- daily-update: %s -->' % TODAY.isoformat(), src, count=1)

upper = TODAY.strftime('%Y.%m.%d')
lower = CUTOFF.strftime('%Y.%m.%d')
badge_new = '%s 数据区间：%s — %s（每日更新）' % (EMO, lower, upper)
src, n = re.subn(re.escape(EMO) + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
                 badge_new, src)
assert n == 1, 'badge replace n=%d' % n

FP = '节后公募|公募首份|ETF发行|ETF资金'
src, n = re.subn(r'<meta name="content-fingerprint" content="[^"]*">',
                 '<meta name="content-fingerprint" content="%s">' % FP, src)
assert n == 1
DESC = ('节后公募发行回暖|公募首份三季报出炉|ETF发行冷热并存|ETF资金流向分化|'
        '沪指10-13收3800.86')
src, n = re.subn(r'<meta name="description" content="[^"]*">',
                 '<meta name="description" content="%s">' % DESC, src)
assert n == 1
print('step0 ok; cutoff=%s' % CUTOFF)
drift('step0')

# ================= Step 1: Stats Bar 沪指卡 =================
old_num = '<div class="stat-number">3813.79</div>'
i = src.find(old_num)
assert i != -1
j = src.find('</div>', src.find('stat-change', i))
assert j != -1
new_stat = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3800.86</div>\n'
    '      <div class="stat-label">沪指10-13收盘·涨0.10%·沪深京三市成交1.69万亿·放量1382亿</div>\n'
    '      <div class="stat-change up">▲ 探底回升收复3800点·2909只上涨·70只涨停</div>'
)
k = src.rfind('    <div class="stat-card">', 0, i)
src = src[:k] + new_stat + src[j + len('</div>'):]
assert '3800.86' in src[src.find('stats-bar'):src.find('Priority Legend')]
drift('step1')

# ================= Step 2: S0 今日焦点 =================
S0_START = src.index('      <!-- S0 Card 1 (10-09 P0) -->')
S0_END = src.index('\n    </div>\n  </div>\n\n<!-- ============ Section 1', S0_START)

C1 = '''      <!-- S0 Card 1 (10-13 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 节后公募发行回暖·本周65只新基金开启认购·FOF单周发行创历史新高</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          新华财经10月13日报道（记者可达）：国庆长假后公募基金发行市场迅速回暖。公募排排网数据显示，按认购起始日统计，本周（10月12日—10月18日）全市场共计<b>65只</b>新基金开启认购，较上周环比增长<b>209.52%</b>，创下近6周发行新高。<br>
          <b>权益类为主力：</b>65只新发基金中权益基金占<b>36只</b>，包括19只股票型基金和17只偏股混合型基金，合计占比<b>55.38%</b>；发行阵容覆盖权益、FOF、"固收+"等多类型产品，适配不同风险偏好资金。<br>
          <b>FOF单周数量刷新历史新高：</b>本周开启认购的FOF基金高达<b>16只</b>，占总量<b>24.62%</b>。按认购截止日统计，截至10月11日，今年以来FOF发行数量达<b>162只</b>、发行份额<b>1492.93亿份</b>、截止日份额1415.12亿份，三项指标均创历年新高。<br>
          <b>发行机构：</b>本周65只新发基金来自<b>44家</b>公募机构，其中14家机构本周发行不少于2只；博时基金以<b>5只</b>居首，广发基金、汇添富基金、平安基金、永赢基金各有3只开启认购，大成、富国、华泰柏瑞等9家机构各有2只。<br>
          <b>机构解读：</b>融智投资FOF基金经理李春瑜认为，回暖一是市场预期修复、机构把握低位建仓窗口；二是长假后居民资金回流、理财资金寻求多元资产布局；三是产品供给丰富，契合震荡轮动下普通投资者择基难度提升的理财诉求。<br>
          <b>对腾安启示：</b>FOF单周发行创历史新高叠加权益类占半壁，货架须把"持有期＋权益仓位中枢＋业绩比较基准"前置排序，并对3个月/6个月持有期FOF加注流动性约束提示，避免用户把FOF直接等同于低波动理财替代。
        </div>
        <div class="card-footer">
          <a href="https://m.cnfin.com/gs-lb//zixun/20261013/4480014_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·10-13</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C2 = '''      <!-- S0 Card 2 (10-13 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 公募首份三季报出炉·南方港股医药加仓CXO·权益仓位降至59.21%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          10月13日证监会官网披露，南方港股医药行业混合发起（QDII，019415）发布2026年第三季度报告，为公募基金行业<b>首份三季报</b>。报告期内A、C份额净值增长率分别为<b>18.49%</b>、<b>17.73%</b>，均跑输<b>21.85%</b>的业绩比较基准；三季度实现本期利润合计<b>943.01万元</b>（A类495.18万元、C类447.83万元），期末基金资产净值<b>1.29亿元</b>。<br>
          <b>仓位与持仓：</b>权益投资占比由二季度末的<b>78.74%</b>降至三季度末的<b>59.21%</b>；凯莱英持仓由2.36万股增至<b>6.97万股</b>（增幅约<b>66.1%</b>），药明康德、恒瑞医药、药明合联生物、百奥赛图持仓数量明显提升，康龙化成、药明生物、金斯瑞生物、劲方医药新进前十大重仓；科伦博泰生物由第一大重仓降至第九大。<br>
          <b>基金经理观点：</b>叶震南、李晓光表示组合未采取"All in式"投资，更重视临床数据质量、适应症空间、合作方能力、现金储备以及估值所隐含的成功率，在产业长期趋势与短期风险收益比之间保持平衡；四季度继续看好创新药及创新药产业链的中长期机会，CXO也有望受益于全球研发需求修复。<br>
          <b>对腾安启示：</b>三季报窗口已开启，产品页须把"区间净值增长率 vs 业绩比较基准"并列展示，防止用户只看绝对收益而忽略跑输基准；对"权益仓位大幅下调但重仓集中度上升"的基金加注仓位与集中度背离提示，避免用单季业绩推导持续能力。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.cn/2026-10-13/detail-iniuzzhk0479196.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·10-13</span></a>
          <a href="https://www.chnfund.com/article/f59a354a-430d-4ab4-f7b0-3a24458aa8f2" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-13</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C3 = '''      <!-- S0 Card 3 (10-13 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 ETF发行冷热并存·前三季度206份延募公告·110份来自ETF</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          环球网财经10月13日报道（同花顺iFind数据）：前三季度全市场共发布<b>206份</b>基金延长募集期公告，其中<b>110份</b>来自ETF。<br>
          <b>延募集中在细分赛道：</b>发布延募公告的产品高度集中在科技、资源、新能源、粮食养殖、工程机械等赛道，均有3只以上同类产品在同一时间段延募。前三季度有<b>32只</b>产品发布两次及以上延长募集期公告，其中<b>17只</b>是ETF；延募次数最多的是鹏华基金旗下港股通金融ETF，7月14日至8月7日<b>四度</b>延长募集期，航空航天ETF汇添富、光伏ETF工银、食品ETF招商、养殖ETF易方达均两次延募。<br>
          <b>另一面是提前结募：</b>同期有<b>98只</b>ETF及联接基金提前结束募集，主要集中在有色金属、电力及公用事业、电池与红利质量、创业板算力、创业板新能源、工程机械、机器人、稀有金属、红利低波等主题。<br>
          <b>成因：</b>7月以来权益市场有所调整，存量基金收益承压，投资者风险偏好回落，认购新基金意愿下降；资金高度集中于AI、半导体等科技赛道及低波动固收产品，新能源、消费等非热门主题权益基金缺乏赚钱效应。<br>
          <b>对腾安启示：</b>延募与提前结募并存反映赛道冷热极端分化，货架须把"募集进度＋结募/延募公告"设为产品页动态字段；同时向用户明示延募不等于产品风险变化、提前结募也不等于额度稀缺，避免用募集节奏替代风险揭示。
        </div>
        <div class="card-footer">
          <a href="http://finance.sina.com.cn/roll/2026-10-13/doc-iniuzuyp7281275.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·环球网·10-13</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C4 = '''      <!-- S0 Card 4 (10-13 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 ETF资金流向分化·宽基净流入38.47亿·信用债指数ETF净流出44.48亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇10月13日报道：<b>10月12日</b>ETF市场资金面整体呈净流入格局，九大类ETF中六类流入、三类流出，六类流入合计约85.91亿元、三类流出合计约50.25亿元，整体净流入约<b>35.66亿元</b>。<br>
          <b>流入端：</b>宽基指数ETF以<b>38.47亿元</b>净流入居各大类之首，创业板ETF易方达（6.17亿元）、沪深300ETF华泰柏瑞（6.03亿元）、中证1000ETF南方（5.23亿元）居前，两只科创50ETF合计净流入约7.17亿元；货币ETF净流入17.85亿元居次，银华日利ETF（12.56亿元）、华宝添益ETF（10.29亿元）两只千亿级品种包揽全市场净流入前两位。<br>
          <b>流出端：</b>信用债指数ETF净流出<b>44.48亿元</b>为当日最大流出大类——短融ETF海富通净流出<b>41.41亿元</b>居全市场首位、科创债ETF嘉实净流出25.52亿元居第二，而信用债ETF海富通、信用债ETF华夏等5只同板块品种合计净流入约20.42亿元；策略风格ETF净流出5.63亿元，红利低波50ETF南方与红利低波ETF易方达合计净流出约4.71亿元。<br>
          <b>板块内"一入一出"：</b>中证1000ETF南方净流入5.23亿元对应中证1000ETF广发净流出2.29亿元；两只30年国债ETF合计净流入约10.66亿元对应国债政金债ETF招商、国开债ETF博时合计净流出约6.64亿元；两只科创50ETF合计净流入约7.17亿元对应4只半导体相关ETF合计净流出约5.61亿元。<br>
          <b>对腾安启示：</b>宽基与货币持续吸金、信用债内部"短融与科创债流出、其他信用品种流入"的切换特征突出，资金流向标签须细化到单品层面并标注统计日，避免用"债券ETF整体流入/流出"的笼统表述误导配置判断。
        </div>
        <div class="card-footer">
          <a href="https://www.gelonghui.com/live/2707432" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·10-13</span></a>
          <a href="https://finance.sina.cn/2026-10-13/detail-iniuzqst8256565.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·格隆汇·10-13</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

s0_new = C1 + '\n' + C2 + '\n' + C3 + '\n' + C4
src = src[:S0_START] + s0_new + src[S0_END:]

# context
i = src.find('今日焦点')
assert i != -1
src = src[:i] + src[i:].replace('<span class="section-context">10月12日 · 4条今日要闻</span>',
                                '<span class="section-context">10月13日 · 4条今日要闻</span>', 1)
assert '10月13日 · 4条今日要闻' in src
seg0 = src[src.find('Section 0'):src.find('Section 1')]
assert seg0.count('action-box') == 0, 'S0 不应有 action-box'
assert len(re.findall(r'date-tag">(\d{2})-(\d{2})<', seg0)) == 4
assert re.findall(r'date-tag">(\d{2})-(\d{2})<', seg0).count(('10', '13')) == 4
assert seg0.count('href="http') == 6, seg0.count('href="http')
print('step2 ok')
drift('step2')

# ================= Step 3: S4 行业趋势（删 09-28 过期卡 + 补红利限购卡） =================
S4A = '      <!-- S4 Card: 商业不动产REITs扩容 (09-28 P1) -->'
S4B = '      <!-- S4 Card: 9月基金发行冰火两重天 (10-02 P1) -->'
i, j = src.index(S4A), src.index(S4B)
NEW_S4 = '''      <!-- S4 Card: 高股息资产热度升温·红利基金密集限购 (10-13 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 高股息资产热度升温·节后18只红利基金密集限购·新品同步提速</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          中国经济网10月13日报道（Wind数据）：国庆假期以来红利基金掀起一轮"限购潮"，截至10月12日，节后已有<b>18只</b>红利主题基金发布暂停或限制大额申购相关公告，成为本轮限购主力品种。<br>
          <b>限购清单：</b>银河基金将银河中证红利低波动100指数、银河上证国有企业红利ETF发起式联接基金单日申购限额设定为<b>100万元</b>，自10月13日起恢复办理大额申购；交银中证红利低波动100指数、景顺长城中证沪港深红利成长低波动指数同样设定100万元单日限额；天弘旗下两只红利基金单日单账户限购<b>500万元</b>；富国恒生港股通红利低波动ETF联接对单账户日累计超<b>1000万元</b>的申购予以暂停；招商中证红利ETF联接对非个人投资者实施单日<b>10万元</b>限额。<br>
          <b>风格再平衡：</b>Wind数据显示，今年上半年上证红利指数下跌6%，同期上证指数、深证成指、创业板指分别上涨3.16%、19.82%、35.58%；下半年以来截至10月12日，上证红利指数涨超<b>14%</b>，三大宽基指数则出现不同程度回调。全市场81只名称含"红利"的ETF中，<b>70只</b>近三个月回报为正，<b>12只</b>近三个月净值增长超10%，华泰柏瑞、融通、富国旗下央企红利ETF均超13%。<br>
          <b>供需双向扩容：</b>路博迈红利量化选股股票基金提前结束募集（原定募集截止日10月16日）；嘉实、汇添富分别提交中证全指红利质量ETF募集申请，工银瑞信、万家、易方达、南方、富国等多家提交中证红利增长ETF申请；10月12日博时恒生港股通红利低波动ETF、银华中证全指红利质量ETF、广发中证红利低波动ETF同步启动发行。<br>
          <b>对腾安影响：</b>红利赛道"存量限购＋新品提速"双向扩容，货架须把限购状态、恢复日期与单日限额前置展示，避免用户在限额期内产生申购失败体验；同时提示红利资产行业集中于银行、资源、公用事业、交运，不得把短期风格切换包装成无风险收益。
        </div>
        <div class="card-footer">
          <a href="https://www.ce.cn/xwzx/gnsz/gdxw/202610/t20261013_3255557.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-13</span></a>
          <a href="https://paper.cnstock.com/html/2026-10/12/content_2276193.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-12</span></a>
          <span class="impact-tag medium">供给结构：中</span>
        </div>
      </div>

'''
src = src[:i] + NEW_S4 + src[j:]
print('step3 ok')
drift('step3')

# ================= Step 4: S6 市场行情速览 =================
S6_START = src.index('                        <div class="card p3">', src.find('Section 6'))
ANCHOR = '      </div>  </div>'
k = src.index(ANCHOR, S6_START)
S6_END = k + len(ANCHOR)

NEW_S6 = '''                        <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股、港股为10-13收盘·美股为10-12收盘·沪指3800.86 +0.10%｜探底回升收复3800点</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-13</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-13收盘）</b><br>
              上证指数 <b>3800.86</b> <span style="color:#dc2626;">+0.10%</span><br>
              深证成指 <b>12353.70</b> <span style="color:#52c41a;">-0.25%</span><br>
              创业板指 <b>2958.34</b> <span style="color:#52c41a;">-0.18%</span><br>
              科创50 <b>1427.18</b> <span style="color:#dc2626;">+0.03%</span><br>
              科创综指 <span style="color:#52c41a;">-0.08%</span>　北证50 <span style="color:#52c41a;">-0.31%</span><br>
              沪深300 <b>4275.68</b> <span style="color:#52c41a;">-0.29%</span><br>
              沪深京三市成交 <b>1.69万亿</b>·较上一交易日放量约1382亿<br>
              全市场2909只上涨·2486只下跌·70只涨停·10只跌停
            </div>
            <div>
              <b>港股（10-13收盘）与美股（10-12收盘）</b><br>
              恒生指数 <b>24312.64</b> <span style="color:#dc2626;">+0.17%</span>（+41.44点）<br>
              国企指数 <b>8164.11</b> <span style="color:#52c41a;">-0.05%</span><br>
              道琼斯 <b>51850.55</b> <span style="color:#dc2626;">+0.38%</span>（+195.60点）<br>
              纳斯达克 <b>27245.90</b> <span style="color:#52c41a;">-0.44%</span>（-120.27点）<br>
              标普500 <b>7807.24</b> <span style="color:#52c41a;">-0.06%</span>（-4.30点）<br>
              费城半导体 <b>12236.79</b> <span style="color:#52c41a;">-2.67%</span><br>
              WTI原油93.16美元 <span style="color:#dc2626;">+1.43%</span>·COMEX黄金4195.9美元/盎司 <span style="color:#52c41a;">-0.48%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股、港股取<b>10月13日收盘</b>（10月13日为交易日且已收盘）；美股取<b>10月12日收盘</b>（美东10月12日收盘对应北京时间10月13日凌晨）。恒生科技指数本期未取得可交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-13）：</b>三大指数低开后探底回升，沪指盘中最低下探<b>3741.53</b>点、午后收复3800点关口，收报<b>3800.86</b>点涨0.10%；深证成指收<b>12353.70</b>点跌0.25%，创业板指收<b>2958.34</b>点跌0.18%，科创50收<b>1427.18</b>点涨0.03%，科创综指跌0.08%，北证50跌0.31%，沪深300收<b>4275.68</b>点跌0.29%。沪深京三市成交约<b>1.69万亿</b>元，较前一交易日放量约1382亿元，全市场2909只股票上涨、2486只下跌，70只涨停、10只跌停。行业板块涨多跌少，元件、地面兵装、航海装备、互联网电商、航空装备、旅游及景区涨幅居前，保险、电池、风电设备跌幅居前；PCB概念爆发（迅捷兴20CM涨停，超声电子、中京电子、协和电子、澳弘电子涨停），军工与冰雪经济活跃，固态电池概念调整。<br>
              <b>港股（10-13）：</b>恒生指数涨41.44点、涨幅0.17%收报<b>24312.64</b>点，主板成交约<b>1628.66亿港元</b>；国企指数收<b>8164.11</b>点跌0.05%。<br>
              <b>美股（10-12）：</b>道琼斯工业平均指数涨195.60点、涨幅0.38%收<b>51850.55</b>点，纳斯达克综合指数跌120.27点、跌幅0.44%收<b>27245.90</b>点，标普500指数跌4.30点、跌幅0.06%收<b>7807.24</b>点；费城半导体指数跌2.67%报<b>12236.79</b>点，存储与光通信板块普跌（闪迪跌5.97%、SK海力士跌4.02%、Lumentum跌9.78%）。标普500十一大板块八涨三跌，能源（+1.48%）与必需消费品（+1.22%）领涨，科技（-0.90%）与非必需消费品（-0.73%）领跌。商品方面，WTI原油期货当月连续合约涨1.31美元、涨幅1.43%收于每桶<b>93.16美元</b>；COMEX黄金期货跌20.40美元、跌幅0.48%报<b>4195.9美元/盎司</b>，现货黄金跌0.54%报4171.77美元/盎司。<br>
              <b>对腾安提示：</b>A股低开高走但深证成指与创业板指仍收跌，指数与结构背离明显，货架与持仓页须同步刷新净值日期与估值口径，不得沿用旧净值呈现。境外端美股科技、存储与光通信回调而能源与必需消费品走强，须把"高利率压制长久期估值"与"板块内部高低切换"两股力量并列提示，不得把单日涨跌直接解读为趋势反转。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-13收盘，美股为2026-10-12收盘</span>
          <span class="source-tag">数据来源：新华财经、中新经纬、东方财富、格隆汇（10-13）</span>
        </div>
      </div>  </div>'''
src = src[:S6_START] + NEW_S6 + src[S6_END:]
print('step4 ok')
drift('step4')

# ================= Step 5: S7 时间线 =================
S7_START = src.index('      <div class="timeline-item">', src.find('Section 7'))
ANCHOR7 = '    </div>\n\n  </div>'
k = src.index(ANCHOR7, S7_START)
S7_END = k + len(ANCHOR7)

items = [
    ('blue', '2026-10-13', '本周65只新基开售·FOF单周新高'),
    ('blue', '2026-10-13', '公募首份三季报出炉'),
    ('blue', '2026-10-13', 'ETF延募潮·前三季度206份'),
    ('blue', '2026-10-13', '沪指探底回升收复3800点'),
    ('blue', '2026-10-12', 'A股高开低走沪指跌0.43%'),
    ('blue', '2026-10-10', '证监会召开资本市场专家座谈会'),
    ('red',  '2026-10-09', '公募运作办法迎12年来大修'),
    ('blue', '2026-10-09', '公募自购超14亿设120只发起式'),
    ('blue', '2026-10-09', '三季度翻倍基仅剩2只'),
    ('blue', '2026-10-08', '汇添富零售直销迁移子公司'),
    ('red',  '2026-10-08', '浙江证监局两家私募被警示'),
    ('blue', '2026-10-07', '恒生科技指数扩至50只'),
]
blk = ''
for dot, d, t in items:
    assert len(t) <= 25, t
    blk += ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>\n' % (dot, d, t))
src = src[:S7_START] + blk + ANCHOR7 + src[S7_END:]
print('step5 ok')
drift('step5')

# ================= Phase1 全量断言 =================
errs = []
o, c = len(re.findall(r'<div\b', src)), len(re.findall(r'</div>', src))
if o != c:
    errs.append('div 不平衡 %d/%d' % (o, c))
if o - o0 != -3:
    errs.append('div 漂移 %d，预期 -3（移除 1 个 P0 action-box）' % (o - o0))
if 'S8' in src:
    errs.append('S8 残留')
if '\ufffd' in src:
    errs.append('U+FFFD 乱码')
if '</div>>' in src:
    errs.append('stray </div>>')
if src.count('class="section"') != 8:
    errs.append('section 数 %d' % src.count('class="section"'))
# date-tag T-14
for (m1, d1) in re.findall(r'date-tag">(\d{2})-(\d{2})<', src):
    y = 2026
    dd = date(y, int(m1), int(d1))
    if dd < CUTOFF:
        errs.append('date-tag 越界 %s-%s < %s' % (m1, d1, CUTOFF))
# S0 标题精确
m = re.search(r'Section 0.*?<span class="section-title">(.*?)</span>', src, re.S)
if not m or m.group(1).strip() != '今日焦点':
    errs.append('S0 section-title = %r' % (m.group(1) if m else None))
# S1/S2 卡数
for sec, exp in (('Section 1', 6), ('Section 2', 4)):
    s = src[src.find(sec):src.find('Section %d' % (int(sec[-1]) + 1))]
    n = len(re.findall(r'<!-- S[12] Card', s))
    if n != exp:
        errs.append('%s 卡数 %d != %d' % (sec, n, exp))
tl = re.findall(r'<div class="timeline-item">', src)
if len(tl) != 12:
    errs.append('timeline 条目 %d != 12' % len(tl))
# 黑名单
for bad in ['stcn.com', 'cls.cn', 'toutiao.com', '21jingji.com', '163.com/dy',
            'so.html5.qq.com', 'caifuhao.eastmoney', 'jrj.com.cn', 'yicai.com']:
    if bad in src:
        errs.append('黑名单命中 %s' % bad)
# S0 段内链接
seg0 = src[src.find('Section 0'):src.find('Section 1')]
if seg0.count('href="http') != 6:
    errs.append('S0 链接数 %d != 6' % seg0.count('href="http'))

if errs:
    print('ASSERT FAILED:')
    for e in errs:
        print('  -', e)
    sys.exit(2)

open(P, 'w', encoding='utf-8').write(src)
print('WRITE OK div %d/%d (drift %d) size=%d' % (o, c, o - o0, len(src)))
