# -*- coding: utf-8 -*-
"""基金行业资讯看板 2026-08-06 每日更新（两阶段：Phase1 全断言 → Phase2 写文件）"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'index.html'
s0 = open(P, encoding='utf-8').read()
s = s0
ORIG_OPEN, ORIG_CLOSE = s.count('<div'), s.count('</div>')
print('BASELINE div:', ORIG_OPEN, ORIG_CLOSE)
assert ORIG_OPEN == ORIG_CLOSE, 'baseline already unbalanced'

LINK = '<a href="{u}" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">{n}</span></a>'

# ============================================================
# STEP 1: Stats Bar
# ============================================================
ST_A = '    <div class="stat-card">\n      <div class="stat-number">2.52万亿</div>'
ST_B = '</div>\n  </div>\n<div class="main">'
i1 = s.index(ST_A)
j1 = s.index(ST_B, i1)
assert s.count(ST_A) == 1 and s.count(ST_B) == 1, 'stats anchor not unique'

STATS = '''    <div class="stat-card">
      <div class="stat-number">3878.43</div>
      <div class="stat-label">上证指数 · 08-05收盘 · 三大指数集体收涨</div>
      <div class="stat-change up">▲ 涨56.15点(+1.47%)·深成指+1.86%·创业板指+1.32%·两市成交2.6万亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">20/20</div>
      <div class="stat-label">非货前20公募 · 已全部布局ETF市场</div>
      <div class="stat-change up">▲ 中欧基金08-04上报首只ETF·前20全员入场5万亿级赛道</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">40%+</div>
      <div class="stat-label">8月新发基金 · 稳健配置型产品占比</div>
      <div class="stat-change up">▲ 较6月28%/7月36%显著提升·15只FOF+14只二级债基·年内FOF增超千亿</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">25只</div>
      <div class="stat-label">7月回撤超40%却仍维持R3中风险的主动权益基金</div>
      <div class="stat-change down">▼ 占73只深度回撤基金的34.25%·风险标识与真实波动错配</div>
    '''
s = s[:i1] + STATS + s[j1:]
b = s.count('<div') - s.count('</div>')
print('after step1 stats, bal =', b)
assert b == 0, 'step1 unbalanced'

# ============================================================
# STEP 2: S0 今日焦点 (context + 4 cards)
# ============================================================
OLD_CTX = '<span class="section-context">8月5日 · 4条今日要闻</span>'
assert s.count(OLD_CTX) == 1
s = s.replace(OLD_CTX, '<span class="section-context">8月6日 · 4条今日要闻</span>')

S0_START = '      <!-- S0 Card 1:'
# 尾部锚点硬编码为常量：仅 card-grid close + section close，禁止用正则推断
S0_TAIL = '    </div>\n  </div>\n\n'
S0_END = S0_TAIL + '<!-- ============ Section 1: 重磅信息 ============ -->'
i2 = s.index(S0_START)
j2 = s.index(S0_END)
assert s.count(S0_END) == 1, 'S0 end anchor not unique'
# 旧 S0 段（不含尾部常量）应自平衡；替换后由 S0_TAIL 补回 2 个 close
_oldS0 = s[i2:j2]
print('  old S0 body diff =', _oldS0.count('<div') - _oldS0.count('</div>'))

S0 = '''      <!-- S0 Card 1: 基金风险评级摒弃纸面合规 (T+0 08-06 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">08-06</span>
          </div>
          <div class="card-title">🔴 基金风险评级须摒弃"纸面合规"·7月73只主动权益回撤超40%·25只仍挂R3占34.25%</div>
        </div>
        <div class="card-body">
          证券日报8月6日刊发评论指出，近期公募风险等级调整密集，多家基金公司将权益类产品由R3中风险上调至R4中高风险。但Wind数据显示，7月共有73只主动权益基金（主份额口径）净值回撤超40%，其中25只至今仍维持R3中风险等级，占比34.25%，风险标识与真实波动明显不匹配。根源在于评级长期停留在"完成合规流程"的纸面导向，各机构在指标选取、权重设置、观测周期、风险阈值上标准不一，"同基不同级"现象普遍。2026年6月发布的《公开募集证券投资基金投资者适当性管理细则》要求定量与定性结合综合评定风险等级，并给出六个月整改窗口，基金管理人与销售机构须在期限内完善划分体系、完成系统改造。
        </div>
        <div class="card-footer">
          ''' + LINK.format(u='http://www.zqrb.cn/review/zibenluntan/2026-08-06/A1785916523597.html', n='证券日报') + '''
          <span class="impact-tag high">合规影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-title">⚡ 腾安行动建议</div>
          <div class="action-content">适当性细则六个月整改窗口已进入后半程，代销侧须同步推进两件事：一是对在架权益产品做一次"评级—实际回撤"错配盘查，重点排查长期股票仓位≥80%却仍标R3的产品，提前对齐管理人上调节奏，避免上调集中落地时出现存量持有人适当性冲突；二是把风险测评有效期与产品评级变更做联动提醒，评级上调的产品在客户端明确弹窗提示，留存告知痕迹以备后续检查。</div>
        </div>
      </div>

      <!-- S0 Card 2: 稳健型基金占据发行C位 (T+0 08-06 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-06</span>
          </div>
          <div class="card-title">🟡 稳健型基金占据发行"C位"·8月新发占比超40%·年内FOF规模增超千亿</div>
        </div>
        <div class="card-body">
          中国证券报8月6日报道，市场震荡调整下资金偏好明显生变。Wind数据显示，截至8月5日已公布发行公告且8月开始发行的基金共85只，其中15只FOF、14只混合二级债基、1只混合一级债基、5只偏债混合型基金，稳健配置型合计占比超40%；对比7月新发161只中稳健型占36%、6月183只中仅占28%，提升趋势清晰。FOF规模持续扩张，截至二季度末总规模3490.89亿元，较年初增加1049亿元；截至8月4日偏股混合型FOF年内平均回报1.78%，偏债混合型FOF为0.62%，均为正收益。多家公募判断A股风格剧烈调整或逐步进入收尾阶段，债券、港股、原油、黄金等大类资产各具结构性机会。
        </div>
        <div class="card-footer">
          ''' + LINK.format(u='https://www.163.com/dy/article/L3KOQVAT05568W0A.html', n='中国证券报') + '''
          <span class="impact-tag high">业务影响：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 中欧上报首只ETF 前20全员布局 (T-2 08-04 事件 / 08-06 每经复盘 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-06</span>
          </div>
          <div class="card-title">🟡 非货前20公募已全部布局ETF·中欧上报首只中证机器人ETF·5万亿赛道全员入场</div>
        </div>
        <div class="card-body">
          每日经济新闻8月6日复盘，8月4日证监会网站显示中欧基金正式递交中欧中证机器人ETF申报材料，拟跟踪中证机器人指数（H30590.CSI），为中欧旗下首只ETF。随其入场，非货规模排名前20的基金公司已全部布局ETF市场。去年以来兴证全球、交银施罗德、东方红资管、农银汇理等主动权益大厂陆续上报首只ETF产品。业内认为，ETF已从"规模利器"升级为竞争创新产品的"入场券"——6月17日证监会主席吴清在陆家嘴论坛明确支持推出主动ETF，同日沪深交易所发布业务指引，7月中旬首批18只主动ETF集体上报，ETF市场正从"被动工具化"迈向"策略多元化"。中欧二季度末主动权益规模2724.77亿元、全行业第3。
        </div>
        <div class="card-footer">
          ''' + LINK.format(u='https://www.cnr.cn/jingji/ycbd/20260804/t20260804_527747512.shtml', n='央广网') + '''
          <span class="impact-tag high">竞争影响：高</span>
        </div>
      </div>

      <!-- S0 Card 4: 建信基金直销费率优惠 (T-2 08-04 公告 / 08-06 每经 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">08-06</span>
          </div>
          <div class="card-title">🔵 又有公募加码直销费率优惠·建信基金全线免认申购及定投手续费</div>
        </div>
        <div class="card-body">
          据每日经济新闻8月6日梳理，建信基金8月4日公告，即日起通过公司网上直销平台购买旗下所有公募基金产品，免收认购、申购及定投手续费，转换业务免收申购补差费；优惠覆盖官网、App、微信公众号等自有渠道，仅限直销。此前嘉实基金今年已通过网上直销开展认购、申购、转换费率优惠并进一步拓展至直销柜台，宝盈基金也曾推出直销渠道费率优惠。公募自有渠道降费动作趋于常态化，直销与第三方代销的费率差正在拉大，对代销平台的客户留存与费率策略构成直接压力。
        </div>
        <div class="card-footer">
          ''' + LINK.format(u='https://new.qq.com/rain/a/20260806A03HQA00?refer=cp_1009', n='每日经济新闻') + '''
          <span class="impact-tag medium">渠道影响：中</span>
        </div>
      </div>

'''
s = s[:i2] + S0 + s[j2:]
b = s.count('<div') - s.count('</div>')
print('after step2 S0, bal =', b)
assert b == 0, 'step2 unbalanced'

# ============================================================
# STEP 3: S6 市场行情速览
# ============================================================
i6 = s.index('Section 6')
j6 = s.index('Section 7')
seg6 = s[i6:j6]
m = re.search(r'<div class="card-body">(.*?)</div>\s*<div class="card-footer">', seg6, re.S)
assert m, 'S6 card-body not found'
# 保持与旧结构完全一致的嵌套（grid 容器 + 左右两栏 + 焦点条），
# 计数：card-body(1) + grid(1) + 左栏(1) + 右栏(1) + 焦点条(1) = 5 open，
# 闭合 5 个但末尾 card-body 的 </div> 由锚点带出 → open 6 / close 5 对齐旧片段。
NEW6 = '''<div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股08-05收盘（三大指数集体收涨·芯片算力领涨）：</b><br>
              ▪ 上证 <b>3878.43</b>（<b>+1.47%</b>，涨56.15点）·深成指 <b>14144.20</b>（<b>+1.86%</b>，涨258.49点）·创业板指 <b>3535.14</b>（<b>+1.32%</b>，涨46.18点）<br>
              ▪ 成交：两市总成交额逾 <b>2.6万亿元</b>，较前一交易日继续放量<br>
              ▪ 涨跌家数：涨跌比 <b>3725:1621</b>，全市场约<b>3700只</b>个股上涨；涨停 <b>104家</b>、跌停仅1家<br>
              ▪ 领涨：存储芯片全天强势（正帆科技20%涨停）、光刻机（沃格光电2连板）、贵金属（四川黄金涨停）、小金属（云南锗业/中钨高新涨停）、电子化学品、MLCC、PCB、锂电池、半导体、医药<br>
              ▪ 领跌：油气开采及服务、银行、白酒、中药、医药商业<br>
              ▪ 换手前五：森合高科64.29%、嘉立创53.12%、维琪科技51.17%、欣兴工具50.05%、托伦斯49.63%
            </div>
            <div>
              <b>📉 上一交易日08-04收盘：</b>上证 3822.28（<b>+0.33%</b>）·深成指 13885.71（+3.25%）·创业板指 3488.97（<b>+5.64%</b>）·科创50 +4.09%，成交2.21万亿<br>
              <b>📈 港股08-05收盘：</b>恒生指数 <b>25915.82</b>（<b>+0.24%</b>）·国企指数 8603.73（+0.34%）·恒生科技 <b>4933.07</b>（<b>+0.97%</b>）·红筹指数 4158.15<br>
              <b>📉 美股08-05收盘（涨势分化·纳指回落）：</b>道指 <b>54349.12</b>（<b>+0.49%</b>）·标普500 <b>7723.55</b>（<b>-0.17%</b>）·纳指 <b>26363.44</b>（<b>-0.83%</b>）；半导体分歧凸显，存储芯片与部分设备股维持韧性，AMD等大幅回调，费城半导体指数冲高回落<br>
              <b>📈 亚太其他：</b>日经225 66300.44（<b>+3.66%</b>）·韩国KOSPI 6598.26（<b>+3.76%</b>）<br>
              <b>📊 大宗与汇率：</b>现货黄金 <b>4248.64</b>美元/盎司（+0.04%）·上金所黄金9999 <b>925.00元/克</b>（<b>+2.22%</b>）·沪金主连928.10元/克（+3.58%）；WTI原油75.06美元/桶（-0.21%）·布伦特79.45美元/桶（+0.11%）；美元指数99.6830（-0.17%）·离岸人民币6.7489
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：8月5日A股在连续放量反攻后<b>延续升势并实现普涨</b>，与08-04"沪弱深强"的极致分化不同，本日沪指反而以 <b>+1.47%</b> 领先创业板指的 +1.32%，风格从单极成长扩散为全面开花，涨跌比3725:1621、涨停104家显示赚钱效应明显扩散。结构上有三点值得注意：① <b>主线由算力切向存储与上游材料</b>，存储芯片、电子化学品、小金属、MLCC接棒光模块，正帆科技20CM涨停、云南锗业等多股封板，产业链利润正从中游模组向上游材料与设备转移；② <b>贵金属独立走强</b>，上金所黄金9999单日涨2.22%、沪金主连涨3.58%，与美元指数走弱（-0.17%）形成呼应，避险与抗通胀配置需求同步抬升；③ <b>外围出现背离信号</b>，美股08-05纳指跌0.83%、标普跌0.17%，费城半导体冲高回落结束前一日暴涨，AMD大幅调整，A股芯片链能否延续需观察外围情绪传导。同时银行、白酒等红利资产继续跑输，高切低资金流向未见逆转。<b>A股/港股/美股均为08-05收盘口径。</b>
          </div>
        </div>
          <div class="card-footer">'''
s = s[:i6] + seg6[:m.start()] + NEW6 + seg6[m.end():] + s[j6:]
b = s.count('<div') - s.count('</div>')
print('after step3 S6, bal =', b)
assert b == 0, 'step3 unbalanced'

# ============================================================
# STEP 4: S7 时间线 —— 删最旧(07-25) + 插入 08-06
# ============================================================
i7 = s.index('Section 7')
seg7 = s[i7:]
k = seg7.index('timeline-date">2026-07-25<')
st = seg7.rindex('<div class="timeline-item">', 0, k)
CLOSE = '\n      </div>\n'
en = seg7.index(CLOSE, k) + len(CLOSE)
removed = seg7[st:en]
assert removed.count('<div') == removed.count('</div>'), 'removed S7 block unbalanced'
assert '2026-07-25' in removed and removed.count('timeline-item') == 1, 'bad S7 removal'
seg7 = seg7[:st] + seg7[en:]

first = seg7.index('<div class="timeline-item">')
NEW7 = '''<div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-06</div>
        <div class="timeline-title">基金风险评级滞后·25只回撤超40%仍挂R3</div>
      </div>
      '''
seg7 = seg7[:first] + NEW7 + seg7[first:]
s = s[:i7] + seg7
b = s.count('<div') - s.count('</div>')
print('after step4 S7, bal =', b)
assert b == 0, 'step4 unbalanced'

# ============================================================
# STEP 4.5: S1/S2 过期清理（T-14 = 07-23，07-22 已出窗）
# ============================================================
CUTOFF = '07-23'
REMOVED_CARDS = 0
for nm, aa, bb, marker in [('S1', 'Section 1', 'Section 2', '<!-- S1'),
                           ('S2', 'Section 2', 'Section 3', '<!-- S2')]:
    while True:
        ia, ib = s.index(aa), s.index(bb)
        sg = s[ia:ib]
        expired = [d for d in re.findall(r'date-tag">([^<]*)', sg) if d < CUTOFF]
        if not expired:
            break
        d = expired[0]
        k = sg.index('date-tag">' + d)
        st = sg.rindex(marker, 0, k)
        nxt = sg.find(marker, k)
        if nxt > 0:
            en = nxt
        else:
            # 末张卡：切到卡片自身闭合（独立行 6 空格 </div>），保留 section 尾部
            en = sg.index('\n      </div>\n', k) + len('\n      </div>\n')
        block = sg[st:en]
        assert block.count('<div') == block.count('</div>'), \
            f'{nm} expired block unbalanced ({block.count("<div")}/{block.count("</div>")})'
        assert block.count('<div class="card ') == 1, f'{nm} block not exactly 1 card'
        print(f'  removing {nm} expired card dated {d} '
              f'(divs {block.count(chr(60) + "div")})')
        s = s[:ia] + sg[:st] + sg[en:] + s[ib:]
        REMOVED_CARDS += 1

b = s.count('<div') - s.count('</div>')
print('after step4.5 expiry cleanup, bal =', b)
assert b == 0, 'step4.5 unbalanced'

# ============================================================
# STEP 5: marker / badge 日期
# ============================================================
s = re.sub(r'(更新[：:]\s*)2026-08-05', r'\g<1>2026-08-06', s)
s = s.replace('2026-08-05 更新', '2026-08-06 更新')

# ============================================================
# PHASE 1 断言全集
# ============================================================
print('\n===== PHASE 1 VALIDATION =====')
o, c = s.count('<div'), s.count('</div>')
# 预期漂移 = 清理过期卡片带走的 div 数（每张 S1/S2 卡 6 个），其余步骤均为等量替换
EXPECTED_DRIFT = -6 * REMOVED_CARDS
print(f'div: {o}/{c} | drift={o - ORIG_OPEN} expected={EXPECTED_DRIFT} '
      f'(removed {REMOVED_CARDS} expired card)')
assert o == c, f'div UNBALANCED {o}/{c}'
assert o - ORIG_OPEN == EXPECTED_DRIFT, \
    f'unexplained div drift {o - ORIG_OPEN} vs expected {EXPECTED_DRIFT}'

for k in ['Section 8', '待办跟踪', '腾安行动清单']:
    assert k not in s, f'S8 residue: {k}'
print('S8 clean: OK')

# S0 段校验
a = s.index('<!-- S0 Card 1:')
bq = s.index('Section 1: 重磅信息')
s0seg = s[a:bq]
n_card = s0seg.count('<div class="card ')
n_meta = s0seg.count('card-meta')
n_top = s0seg.count('card-top')
n_link = s0seg.count('source-tag')
n_abox = s0seg.count('action-box')
n_p0 = s0seg.count('<div class="card p0">')
dts = re.findall(r'date-tag">([^<]*)', s0seg)
print(f'S0 cards={n_card} top={n_top} meta={n_meta} links={n_link} p0={n_p0} dates={dts}')
assert n_card == 4 and n_top == 4 and n_meta == 4 and n_link == 4, 'S0 card structure bad'
assert n_p0 == 1, 'S0 p0 count != 1'
assert n_abox == 2, 'S0 action-box markup count != 2 (title+wrapper)'
assert all(d == '08-06' for d in dts), f'S0 date not all T+0: {dts}'

assert '<span class="section-title">今日焦点</span>' in s, 'S0 title bad'
assert '今日焦点（' not in s and '今日焦点(' not in s, 'S0 title has extra'
assert '<span class="section-context">8月6日 · 4条今日要闻</span>' in s, 'S0 context bad'
print('S0 header: OK')

# S1 / S2 时效
for nm, aa, bb, cap in [('S1', 'Section 1', 'Section 2', 6), ('S2', 'Section 2', 'Section 3', 4)]:
    sg = s[s.index(aa):s.index(bb)]
    ds = re.findall(r'date-tag">([^<]*)', sg)
    lk = sg.count('source-tag')
    print(f'{nm}: {ds} links={lk}')
    assert len(ds) <= cap, f'{nm} over cap'
    assert lk >= len(ds), f'{nm} missing links'
    for d in ds:
        assert d >= '07-23', f'{nm} expired entry {d}'

# S7 校验
sg7 = s[s.index('Section 7'):]
d7 = re.findall(r'timeline-date">([^<]*)', sg7)
t7 = re.findall(r'timeline-title">([^<]*)', sg7)
print(f'S7 count={len(d7)} max_len={max(len(x) for x in t7)}')
assert 10 <= len(d7) <= 12, f'S7 count {len(d7)} out of range'
assert len(d7) == len(set(d7)), f'S7 duplicate dates: {d7}'
assert d7 == sorted(d7, reverse=True), 'S7 not descending'
assert 'timeline-desc' not in sg7, 'S7 has timeline-desc'
for d in d7:
    assert d >= '2026-07-23', f'S7 expired {d}'
over = [x for x in t7 if len(x) > 25]
assert not over, f'S7 title too long: {over}'
assert len(d7) == len(t7), 'S7 date/title mismatch'

# card-meta 包裹全局校验（排除 style 段与 CSS 行）
body = s[s.index('</style>'):]
bad = [ln.strip()[:70] for ln in body.split('\n')
       if 'priority-tag' in ln and not ln.strip().startswith('.') and '{' not in ln
       and 'card-meta' not in body[max(0, body.index(ln) - 200):body.index(ln)]]
print('unwrapped priority-tag lines:', len(bad))

print('\n===== ALL ASSERTIONS PASSED =====')

# ============================================================
# PHASE 2: 写文件
# ============================================================
open(P, 'w', encoding='utf-8').write(s)
print('WRITTEN OK, bytes =', len(s.encode('utf-8')))
