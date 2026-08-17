# -*- coding: utf-8 -*-
import sys, re

PATH = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
s = open(PATH, encoding='utf-8').read()
orig_open = s.count('<div')
orig_close = s.count('</div>')

# ---------------- Phase 1: 全部锚点断言 ----------------
A_MARKER = '<!-- daily-update: 2026-07-30 -->'
A_FP = '<meta name="content-fingerprint" content="重仓股六进六出寒武纪北方华创新晋前十|翻倍基97.56%缩水|FOF光模块趋同避险弱化|指增破3200亿|沪市ETF分红208亿">'
A_BADGE = '<div class="date-badge">📅 数据区间：2026.07.16 — 2026.07.30（每日更新）</div>'
A_STAT_NUM = '''      <div class="stat-number">3832.56</div>
      <div class="stat-label">上证综指 · 07-30盘中+0.11%·探底回升翻红·大消费/传媒/券商走强</div>
      <div class="stat-change up">▲ 顶住日韩股市暴跌·超4200股上涨·食品饮料/游戏/教育活跃·半导体续跌</div>'''
A_S0_TITLE = '<span class="section-title">今日焦点（7月30日·A股探底回升沪指翻红顶住日韩暴跌科创50续跌2.16%·公募重仓股二季度史诗级重构寒武纪等六硬科技新晋前十·翻倍基锐减97.56%仅剩6只·公募FOF超配科技分散避险功能减弱）</span>'
A_S0_START = '      <!-- S0 Card 1:'
A_S1_MARK = '<!-- ============ Section 1: 重磅信息 ============ -->'
A_S6_MARK = '<!-- ============ Section 6: 市场行情速览 ============ -->'
A_S7_MARK = '<!-- ============ Section 7: 关键时间线 ============ -->'
A_S7_FIRST = '      <!-- 07-30 时间线条目 (NEW) -->'
A_S7_OLD = '''      <!-- 07-17 时间线条目 -->
'''

asserts = [A_MARKER, A_FP, A_BADGE, A_STAT_NUM, A_S0_TITLE, A_S0_START,
           A_S1_MARK, A_S6_MARK, A_S7_MARK, A_S7_FIRST]
fail = False
for a in asserts:
    c = s.count(a)
    if c != 1:
        print('ANCHOR FAIL count=%d :: %s' % (c, a[:80]))
        fail = True
if fail:
    sys.exit(1)

# S0 区块边界定位
i_s0 = s.index(A_S0_START)
i_s1 = s.index(A_S1_MARK)
s0_block = s[i_s0:i_s1]
if s0_block.count('<!-- S0 Card') != 4:
    print('ANCHOR FAIL: S0 card count=%d' % s0_block.count('<!-- S0 Card'))
    sys.exit(1)
# S0 区块末尾必须是 card-grid + section 两个闭合
tail = s0_block.rstrip()
if not tail.endswith('</div>'):
    print('ANCHOR FAIL: S0 block tail')
    sys.exit(1)
s0_tail_suffix = s0_block[s0_block.rindex('      </div>\n'):]  # card-grid close 之后的残余

# S6 卡片块定位
i_s6 = s.index(A_S6_MARK)
i_s7 = s.index(A_S7_MARK)
s6_block = s[i_s6:i_s7]
if s6_block.count('<div class="card p3">') != 1:
    print('ANCHOR FAIL: S6 card p3 count')
    sys.exit(1)
i_s6card = i_s6 + s6_block.index('          <div class="card p3">')
i_s6end = i_s7
s6_card_old = s[i_s6card:i_s6end]

# S7 第 12 条（07-17）需要删除
i_s7f = s.index(A_S7_FIRST)
RE_17 = r'\n      <div class="timeline-item">\n        <div class="timeline-dot [^"]*"></div>\n        <div class="timeline-date">2026-07-17</div>\n        <div class="timeline-title">[^\n]*</div>\n      </div>\n'
m_old17 = re.search(RE_17, s)
if not m_old17:
    print('ANCHOR FAIL: 07-17 timeline item not matched')
    sys.exit(1)
if s[m_old17.start():m_old17.end()].count('<div') != s[m_old17.start():m_old17.end()].count('</div>'):
    print('ANCHOR FAIL: 07-17 block div imbalance')
    sys.exit(1)

print('ALL ANCHORS OK')

# ---------------- Phase 2: 执行替换 ----------------
N_MARKER = '<!-- daily-update: 2026-07-31 -->'
N_FP = '<meta name="content-fingerprint" content="私募运作指引过渡期今日届满三不得|银行理财配公募2.52万亿创新高|翻倍基仅剩6只逆势修复|7月43只新基延长募集ETF超六成|QFII半年报增持名单出炉">'
N_BADGE = '<div class="date-badge">📅 数据区间：2026.07.17 — 2026.07.31（每日更新）</div>'
N_STAT = '''      <div class="stat-number">3804.69</div>
      <div class="stat-label">上证综指 · 07-30收盘-0.62%·深V修复·白酒/银行/汽车走强</div>
      <div class="stat-change down">▼ 深成指-2.73%·创业板-3.97%·科创50-5.38%·超3600股下跌·成交2.36万亿</div>'''

N_S0_TITLE = '<span class="section-title">今日焦点（7月31日·《私募证券投资基金运作指引》24个月过渡期今日届满未整改三不得·银行理财配置公募基金2.52万亿创近年新高二季度加仓科技ETF至32%·翻倍基锐减仅剩6只部分绩优基金高位止盈逆势修复·7月43只新基金延长募集ETF占比超六成）</span>'

N_S0 = '''      <!-- S0 Card 1: 私募运作指引过渡期今日届满 (T+0 07-31 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 《私募证券投资基金运作指引》24个月过渡期今日（7月31日）届满·未整改基金触发"三不得"·私募存续规模23.66万亿管理人年内减569家</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">07-31</span>
          </div>
        </div>
        <div class="card-body">
          <b>今日大限：</b>2024年8月1日起施行的《私募证券投资基金运作指引》约定的<b>24个月过渡期，截止日为2026年7月31日（今日）</b>。过渡期结束后未完成整改的存量私募证券基金将进入"<b>三不得</b>"状态——不得新增募集规模、不得新增投资者、不得展期，且<b>进入限制状态后不得恢复</b>，仅可按原合同运作至自然到期。<br>
          <b>整改双标准：</b>中基协明确须同时满足①基金合同条款符合《运作指引》②实际投资运作符合整改后合同条款。核心硬约束包括 <b>500万元存续规模红线、双25%分散投资、杠杆上限200%（受限类120%）、单一上市公司流通股≤30%、债券10%/25%集中度、嵌套层级≤2层</b>。<br>
          <b>行业出清成效：</b>截至2026年6月末，存续私募基金管理人从年初19231家降至<b>18662家（减少569家）</b>，而全市场私募基金总规模达<b>23.66万亿元</b>（较年初22.15万亿增长6.82%），呈现"机构数量降、管理规模升"的扶优限劣格局。
        </div>
        <div class="card-footer">
          <a href="https://stcn.com/article/detail/4010095.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·北京商报</span></a>
          <span class="impact-tag high">合规影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-title">⚡ 腾安行动建议</div>
          <div class="action-text">过渡期今日届满、明日起"三不得"生效，代销与产品端须立即行动：① <b>连夜排查代销货架上的私募证券产品</b>，逐只确认托管人端整改状态（合同修改+实质持仓双达标），标记出未整改产品并立即冻结新增募集与新增投资者；② 对已进入"三不得"的产品，提前准备客户告知话术——强调"可运作至自然到期、不影响存量份额"，避免误读为产品出问题引发挤兑式赎回；③ 存量客户续投/转投需求，引导切换至已完成整改的合规产品或公募替代方案；④ 建立私募管理人合规白名单机制，把"是否完成《运作指引》整改"纳入准入与续约的硬性指标，规避后续代销连带风险。</div>
        </div>
      </div>

      <!-- S0 Card 2: 银行理财配置公募基金2.52万亿创新高 (T+0 07-31 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 银行理财配置公募基金规模创新高·6月末达2.52万亿占比7%·Q2科技ETF持仓比从12%飙升至32%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-31</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模新高：</b>截至2026年6月末，理财产品配置公募基金合计<b>2.52万亿元</b>，占理财总投资资产比例<b>7%</b>，金额与占比<b>均创近年来新高</b>。二季度单季银行理财增配债券型基金约<b>6000亿元</b>。<br>
          <b>结构性切换：</b>权益端理财资金借道股票型ETF的切换尤为显著——开源证券数据显示，2026Q2理财大幅加仓科技行业ETF，<b>前十持仓比例从一季度12%跃升至32%</b>，主要聚焦半导体、通信和消费电子；同时减仓周期、金融地产及宽基ETF，并大幅减仓黄金ETF（减持幅度大于一季度）。<br>
          <b>行业含义：</b>银行理财已成为公募基金（尤其债基与行业ETF）最重要的机构增量资金之一，但Q2重仓科技ETF的择时恰逢7月科技板块深调，理财净值波动压力值得关注。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260731A035IZ00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">机构资金：中高</span>
        </div>
      </div>

      <!-- S0 Card 3: 翻倍基锐减仅剩6只·绩优基金高位止盈逆势修复 (T+0 07-31 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 翻倍基从199只锐减至6只·近200只翻倍基平均回撤超三成·易方达供给改革7月仅跌6%演绎"不赚最后一个铜板"</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-31</span>
          </div>
        </div>
        <div class="card-body">
          <b>翻倍基大缩水：</b>截至6月30日全市场年内翻倍的主动权益基金有<b>199只</b>；经7月一轮调整后，截至<b>7月28日收盘稳守翻倍收益的仅剩6只</b>。截至7月29日，上半年近200只翻倍基在下半年不到一个月内<b>平均回撤已超三成</b>，重仓存储芯片等腰斩个股的基金净值回撤甚至<b>超40%</b>。<br>
          <b>精准止盈样本：</b>易方达供给改革上半年涨幅<b>138.1%</b>，7月内仅跌约<b>6%</b>、本周甚至涨约2%——基金经理季报称"在持仓股票估值大幅上行后，二季度末逐步减持部分持仓"，并将短期逆风但中长期有吸引力的传统行业优质公司纳入持仓。此类逆势走强产品持仓多集中在<b>消费、汽车、银行</b>。<br>
          <b>回撤修复方：</b>嘉实新消费A、华宝品质生活、鹏华先进制造、中欧核心价值A等10只上半年表现不佳的基金，7月以来逆势上涨<b>超8.5%</b>，持仓集中于创新药、智能制造、智能家居、互联网平台等应用方向。
        </div>
        <div class="card-footer">
          <a href="https://news.yunnan.cn/system/2026/07/31/034103746.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·中国经济网</span></a>
          <span class="impact-tag high">客户情绪：高</span>
        </div>
      </div>

      <!-- S0 Card 4: 7月43只新基金延长募集ETF占比超六成 (T+0 07-31 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 7月以来43只新基金延长募集·54则延募公告·被动指数型26只占比超六成其中25只为ETF</div>
          <div class="card-meta">
            <span class="priority-tag suggest">建议了解</span>
            <span class="date-tag">07-31</span>
          </div>
        </div>
        <div class="card-body">
          <b>延募激增：</b>Wind数据显示，7月以来共有<b>54则</b>基金延长募集期公告，涉及<b>43只基金</b>，其中<b>10只基金曾两次及以上延长募集期</b>。<br>
          <b>延长幅度：</b>华泰柏瑞中证港股通信息技术综合ETF募集截止日由7月24日延至9月30日，<b>延长68天</b>；广发稳致、贝莱德行业轮动量化选股募集截止日均由7月31日延至8月31日。<br>
          <b>类型分布：</b>43只中<b>26只为被动指数型基金（占比超六成），其中25只为ETF</b>；另包括偏股混合型、普通股票型、偏债混合型及FOF等。折射出7月科技板块深调后新发市场认购意愿明显走弱、ETF同质化竞争加剧的现实压力。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L35IG0CT05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
          <span class="impact-tag medium">新发市场：中</span>
        </div>
      </div>

'''

N_S6_CARD = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月30日（周四·收盘）·A股深V修复沪指收3804.69跌0.62%·白酒银行汽车逆势走强·科技续跌科创50跌5.38%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📉 A股07-30收盘（深V修复·科技续跌）：</b><br>
              ▪ 上证指数 <b>3804.69</b>（<b>-0.62%</b>）·深证成指 <b>13285.80</b>（<b>-2.73%</b>）·创业板指 <b>3244.62</b>（<b>-3.97%</b>）<br>
              ▪ 科创50 <b>-5.38%</b>·科创综指 1755.22（-5.70%）·沪深300 -1.10%·北证50 -1.43%<br>
              ▪ 沪深两市成交 <b>2.36万亿</b>（放量约467亿），全市场超<b>3600股下跌</b>；沪指盘中失守3800点后午后深V回升逾1个百分点<br>
              ▪ 涨：白酒/食品饮料/零售/银行（建行涨超3%）/汽车整车（江淮涨停）/油气/钢铁；跌：CPO/先进封装/半导体/存储芯片/光刻机
            </div>
            <div>
              <b>📈 港股07-30收盘（微幅收涨）：</b><br>
              ▪ 恒生指数 <b>25858.88</b>（<b>+0.20%</b>），盘中高见25971.63、低见25657.33<br>
              <b>📈 美股07-30收盘（科技强势反弹）：</b><br>
              ▪ 道琼斯 <b>52208.06</b>（<b>+1.19%</b>）·标普500 <b>7437.63</b>（<b>+1.66%</b>）·纳斯达克 <b>25122.18</b>（<b>+2.78%</b>）<br>
              ▪ 美股在前一日（07-29）道指-2.19%/纳指-1.74%重挫后强势反弹，微软云收入增超40%、资本支出低于预期提振情绪
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：07-30 A股延续"科技杀跌+消费银行防御"的结构性分化，科创50月内累计跌逾23%、电子板块月跌近32%。核心压制因素为全球科技估值消化、美联储维持利率3.5%~3.75%不变、科技赛道筹码拥挤出清。积极信号：7月以来近60家A股科技公司披露回购增持计划；07-30创业板ETF易方达成交163亿创年内次高，资金逆势抄底。美股隔夜大幅反弹，或对A股科技板块情绪形成边际支撑。<b>数据为上一交易日（07-30）收盘值。</b>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-30收盘</span>
            <span class="source-tag">数据来源：同花顺iFind/新华财经/证券时报/金十数据/华尔街见闻</span>
          </div>
      </div>
  </div>
'''

N_S7_NEW = '''      <!-- 07-31 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-31</div>
        <div class="timeline-title">私募《运作指引》过渡期今日届满·未整改基金触发"三不得"</div>
      </div>

      <!-- 07-30 时间线条目 -->'''

# 逐项替换
s = s.replace(A_MARKER, N_MARKER, 1)
s = s.replace(A_FP, N_FP, 1)
s = s.replace(A_BADGE, N_BADGE, 1)
s = s.replace(A_STAT_NUM, N_STAT, 1)
s = s.replace(A_S0_TITLE, N_S0_TITLE, 1)

# S0 卡片区整体替换（保留 card-grid/section 闭合尾巴）
i_s0 = s.index(A_S0_START)
i_s1 = s.index(A_S1_MARK)
old_s0 = s[i_s0:i_s1]
# 提取尾部闭合（最后两个 </div> + 换行）
S0_TAIL = '    </div>\n  </div>\n\n'   # card-grid close + section close
s = s[:i_s0] + N_S0 + S0_TAIL + s[i_s1:]

# S6 卡片替换
i_s6 = s.index(A_S6_MARK)
i_s7 = s.index(A_S7_MARK)
blk = s[i_s6:i_s7]
j = blk.index('          <div class="card p3">')
s = s[:i_s6+j] + N_S6_CARD + s[i_s7:]

# S7: 头部插入 07-31，删除 07-17
s = s.replace('      <!-- 07-30 时间线条目 (NEW) -->', N_S7_NEW, 1)
m17 = re.search(RE_17, s)
s = s[:m17.start()] + s[m17.end():]

# ---------------- 后置校验 ----------------
no = s.count('<div'); nc = s.count('</div>')
print('div open/close: %d / %d (orig %d / %d)' % (no, nc, orig_open, orig_close))
if no != nc:
    print('FAIL: div imbalance')
    sys.exit(1)
if 'Section 8' in s or '腾安行动清单' in s:
    print('FAIL: S8 residue')
    sys.exit(1)
if 'timeline-desc' in s:
    print('FAIL: timeline-desc residue')
    sys.exit(1)
i0 = s.index('<!-- ============ Section 0'); i1 = s.index(A_S1_MARK)
tags = re.findall(r'date-tag">([\d-]+)<', s[i0:i1])
print('S0 date-tags:', tags)
if any(t not in ('07-31','07-30') for t in tags):
    print('FAIL: S0 date-tag violation')
    sys.exit(1)
tl = re.findall(r'timeline-date">([\d-]+)<', s)
print('timeline count=%d' % len(tl), tl)
if len(tl) > 12:
    print('FAIL: timeline > 12')
    sys.exit(1)
for k in range(9):
    if ('Section %d' % k) not in s:
        print('FAIL: missing Section %d' % k if k < 8 else '')
        if k < 8: sys.exit(1)

open(PATH, 'w', encoding='utf-8').write(s)
print('SUCCESS')
