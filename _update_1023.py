# -*- coding: utf-8 -*-
"""2026-10-23 每日更新：marker/区间/StatsBar/S0/S2清旧/S6/S7"""
import re, sys, io
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(open('_upd_1023.txt', 'wb'), encoding='utf-8', write_through=True)

TODAY = date(2026, 10, 23)
T14 = TODAY - timedelta(days=14)
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
UPPER = TODAY.strftime('%Y.%m.%d')

src = open('index.html', encoding='utf-8').read()
o0, c0 = len(re.findall(r'<div\b', src)), src.count('</div>')
print('baseline open/close', o0, c0)
assert o0 == c0 == 243

def drift(tag):
    o, c = len(re.findall(r'<div\b', src)), src.count('</div>')
    print(f'{tag}: open={o} close={c} drift_o={o-o0} drift_c={c-c0}')
    return o, c

def sub1(old, new, tag):
    global src
    assert src.count(old) == 1, f'{tag}: anchor count={src.count(old)}'
    src = src.replace(old, new, 1)

# ---------------- Step 0: marker + description + fingerprint ----------------
sub1('<!-- daily-update: 2026-10-22 -->', '<!-- daily-update: 2026-10-23 -->', 'marker')
sub1(
    '<meta name="description" content="首批18只主动ETF定档10月23日开售|公募投研迎基准锚定大考|郑巍山卸任全部在管基金产品|公募多策并举提升投资者持有体验|沪指10-21收3713.03 纳指涨1.05%">',
    '<meta name="description" content="首批18只主动ETF今日正式发行|ETF资金10月22日净流入592.83亿元|证监会部署持续深化公募基金改革|主动ETF拟任基金经理集体发声|沪指10-22收3658.03 纳指跌2.60%">',
    'description')
sub1('<meta name="content-fingerprint" content="首批18|公募投研|郑巍山卸|公募多策">',
     '<meta name="content-fingerprint" content="首批18只|ETF资金|证监会部|主动ETF">', 'fingerprint')
drift('step0')

# ---------------- Step 1: header 区间 ----------------
new_badge = f'📅 数据区间：{LOWER} — {UPPER}（每日更新）'
src, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', new_badge, src)
assert n == 1, f'badge replace n={n}'
print('badge ->', new_badge)
drift('step1')

# ---------------- Step 2: Stats Bar ----------------
s = src.find('    <div class="stats-bar">')
assert s > 0
em = '\n\n  </div>\n\n<div class="main">'
e = src.find(em, s)
assert e > s
seg = src[s:e]
assert seg.count('<div class="stat-card"') == 4, seg.count('<div class="stat-card"')
new_stats = '''    <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-number">18只</div>
      <div class="stat-label">首批主动ETF 10月23日正式发行·5家公募自购合计约13亿元</div>
      <div class="stat-change up">▲ 管理费均1.0%·托管费0.10%—0.15%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3658.03</div>
      <div class="stat-label">沪指10-22收盘·跌1.48%·沪深北三市成交1.54万亿元</div>
      <div class="stat-change down">▼ 创业板指跌4.37%·恒生指数跌3.03%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">592.83亿</div>
      <div class="stat-label">10-22 ETF净流入·创7月21日以来单日新高</div>
      <div class="stat-change up">▲ 股票型ETF净流入464.81亿元</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">364位</div>
      <div class="stat-label">年内离任基金经理·同期新上任基金经理达606名</div>
      <div class="stat-change neutral">● 郑巍山卸任银河基金全部在管产品</div>
    </div>
'''
assert new_stats.count('<div class="stat-card"') == 4
src = src[:s] + new_stats + src[e:]
drift('step2')

# ---------------- Step 3: S0 四卡全换 ----------------
a = '      <!-- S0 Card 1 (10-22 P0) -->'
b = '\n\n    </div>\n\n  </div>\n\n\n\n<!-- ============ Section 1'
s = src.find(a); e = src.find(b, s)
assert s > 0 and e > s
seg = src[s:e]
print('S0 seg cards', seg.count('<div class="card p'), 'action-box', seg.count('action-box'))

new_s0 = '''      <!-- S0 Card 1 (10-23 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 首批18只主动ETF今日正式发行·易方达华夏富国汇添富各2亿自购·摩根约5亿元</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-23</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月23日报道：<b>10月23日</b>，首批<b>18只</b>主动ETF迎来正式发行，易方达品质均衡主动管理ETF（认购代码<b>581053</b>）等首批产品于同日开售。<br>
          <b>自购加码：</b>易方达基金公告将于10月23日募集期首日以固有资金<b>2亿元</b>认购旗下易方达品质均衡主动管理ETF。中国证券报10月23日报道，富国基金、华夏基金同样于10月22日公告各运用固有资金<b>2亿元</b>认购价值优选主动ETF富国、质量主动ETF华夏，汇添富基金亦公告以固有资金<b>2亿元</b>认购均衡智选主动ETF汇添富；摩根资产管理（中国）10月20日公告，公司股东将通过关联方摩根资产管理（亚太）有限公司以自有资金<b>7500万美元</b>（约合<b>5亿元</b>人民币）投资摩根大盘成长主动股票ETF，相关投资将在基金上市后开展。按公告初步统计，已有<b>5家</b>公募宣布自购旗下主动ETF，涉及金额合计约<b>13亿元</b>。<br>
          <b>产品机制：</b>18只产品均在名称中明确风格策略，其中采用均衡策略的有<b>9只</b>、占比一半。按沪深交易所业务指引，主动ETF持有证券数量不得低于<b>30只</b>，前十大持仓证券权重合计不得超过基金资产净值的<b>60%</b>，组合所持股票最近一年日均成交金额应位于所在交易所全部上市股票的前<b>80%</b>。18只产品管理费率均为<b>1.0%/年</b>，托管费率落在<b>0.10%—0.15%</b>之间，每个交易日披露基于真实投资组合的申购赎回清单（PCF）。<br>
          <b>获批背景：</b>中国证券报报道，<b>10月19日晚</b>首批18只主动ETF正式获得中国证监会批复，均自10月23日开始发售。主动ETF不以跟踪特定指数为投资目标，由基金管理人依据投资策略自主选股，最核心的机制创新在于每日持仓透明。<br>
          <b>对腾安启示：</b>18只主动ETF今日起陆续开售，货架须在开售前完成品类建档与风险揭示，并把“策略风格（均衡／价值／红利／质量／大盘成长）”“认购代码与募集期”“管理费1.0%＋托管费0.10%—0.15%”列为必填字段，不得以“主动ETF”单一标签替代策略区分；自购金额属公司固有资金的认购安排，须与产品业绩、风险等级严格分离展示；每日PCF披露属透明度机制，不得演绎为“持仓可复制”“收益可跟随”的暗示。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/ARf45e1152-3780-88ed-2b65-3a247843c478" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-23</span></a>
          <a href="https://finance.eastmoney.com/a/202610223904478086.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·中国证券报·10-23</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 上架准备→今日开售的18只主动ETF须完成建档并与被动宽基ETF分栏陈列，字段包含策略风格、认购代码、募集期、管理费与托管费、拟任基金经理及其模式；<br>
            ② 自购宣传→“5家自购合计约13亿元”须标注为按公告初步统计的拟认购金额，摩根部分须注明“基金上市后开展”，禁止写成已到账规模或收益保障；<br>
            ③ 适当性→详情页须前置“主动管理＋场内交易”双重风险提示，并说明持股不少于30只、前十大合计不超60%的集中度约束，明确每日PCF披露不等于低风险。
          </div>
        </div>
      </div>

      <!-- S0 Card 2 (10-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 ETF资金10月22日净流入592.83亿元·创7月21日以来单日新高·股票型464.81亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-23</span>
          </div>
        </div>
        <div class="card-body">
          新浪财经10月23日刊发《ETF资金日记》：10月22日A股、港股市场齐齐杀跌、上证指数跌破3700点，当日ETF净流入达<b>592.83亿元</b>，创<b>7月21日</b>以来单日资金净流入新高。其中股票型ETF成为吸金主力，净流入<b>464.81亿元</b>；债券型ETF净流入<b>88.43亿元</b>；跨境型ETF净流入<b>34.60亿元</b>。<br>
          <b>个券流向：</b>沪深300ETF华泰柏瑞净流入<b>104.51亿元</b>居首，沪深300ETF嘉实净流入<b>94.92亿元</b>、科创50ETF华夏净流入<b>66.53亿元</b>紧随其后；净流出方面，科创半导体ETF华夏净流出<b>12.28亿元</b>居首。<br>
          <b>规模与持续性：</b>财联社10月23日报道（记者周晓雅），沪深300ETF华泰柏瑞最新规模回升至<b>1344.97亿元</b>，沪深300ETF嘉实规模回升至<b>418.95亿元</b>；股票ETF已<b>连续14个交易日</b>净流入，9月28日以来累计净流入额达<b>2612.96亿元</b>。<br>
          <b>口径提示：</b>同期另有机构按iFinD口径统计当日ETF整体净流入<b>592.78亿元</b>、股票型净流入<b>464.81亿元</b>，与上述数值在统计范围上略有差异，本期统一采用单一来源口径并列展示，不做跨源合并或换算。<br>
          <b>对腾安启示：</b>指数下跌与ETF大额净流入同时出现，属典型的“指数承压—资金借道ETF加仓”背离结构，对客材料须把“净流入”表述为资金流向统计而非指数企稳或收益信号；展示单品规模与净流入时须标注统计日期与口径来源，禁止把累计净流入等同于产品实际盈利；宽基ETF吸金居前而半导体主题ETF净流出居首，须按品类分别提示结构分化，不做全市场概括。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-10-23/doc-iniweiyu8102212.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·财闻·10-23</span></a>
          <a href="https://news.qq.com/rain/a/20261023A03BT800" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·财联社·10-23</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

      <!-- S0 Card 3 (10-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 证监会部署持续深化公募基金改革·健全长周期考核机制·壮大市场稳定力量</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-23</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月23日报道（记者韩宋辉）：中国证监会主席吴清在2026金融街论坛年会上表示，推动进一步健全适配长期投资的<b>长周期考核机制</b>，扩大中长期资金来源、渠道和入市方式，持续深化<b>公募基金改革</b>，壮大市场稳定力量。<br>
          <b>长钱体量：</b>据证监会6月17日披露的数据，新“国九条”出台两年多来，社保、保险、年金等中长期资本持有A股流通市值增长<b>85%</b>，净买入A股约<b>1.3万亿元</b>。<br>
          <b>稳市机制：</b>吴清表示，坚持稳字当头，密切跟踪境内外市场动态，加强风险研判和政策工具储备，巩固完善稳市机制建设，着力加强新型业务风险防范，<b>高度警惕境外挂钩A股个股的杠杆产品</b>等新风险点，持续筑牢资本市场风险防波堤防浪堤。<br>
          <b>机构解读：</b>中原证券首席经济学家邓淑斌表示，中长期资金是资本市场稳定运行的“压舱石”，能够对冲短期资金追涨杀跌行为；招商证券表示，产品注册并不直接等于资金净流入，但中长期资金占比提高有利于降低市场对短期交易资金的依赖、改善波动结构；西南证券首席经济学家叶凡将其概括为“先筑堤，再引水”。<br>
          <b>对腾安启示：</b>“长周期考核＋长期资金入市”导向下，对客材料可把长期持有、定期定额与长期资金适配性作为合规表达重点，但不得把监管表态演绎为对市场点位或产品收益的背书；引用“社保、保险、年金持有A股流通市值增长85%”“净买入约1.3万亿元”须完整标注统计区间与新“国九条”口径，禁止截取为短期资金流向；对境外挂钩A股个股的杠杆产品风险提示须同步更新至风险揭示文案。
        </div>
        <div class="card-footer">
          <a href="https://www.cfbond.com/14740/14740zgcfw/ejy/yw/4896229444.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国财富网·上海证券报·10-23</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

      <!-- S0 Card 4 (10-23 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 主动ETF拟任基金经理集体发声·回调释放估值压力·分批均匀平稳建仓</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-23</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月23日报道（记者闫军、陆慧婧）：10月23日首批18只主动ETF正式发行，多位拟任基金经理围绕如何看待本轮回调、如何挖掘市场机会、如何平稳建仓三大问题发声——普遍认为回调释放了估值压力，建仓上“分批、均匀、平稳”成为高频词。<br>
          <b>看回调：</b>摩根大盘成长主动股票ETF拟任基金经理李博指出，A股年内平均估值水平已接近过去十年均值，TMT与红利股的40日滚动收益差回落至<b>历史极低位置</b>，AI硬件标的远期市盈率回落至2023年以来低点；天弘林心龙认为本轮回调与增长预期和估值重估有关，修复节奏可能有所反复；平安刘榕俊认为估值变化是主导，盈利变化虽有改善但交易结构与情绪占主导。<br>
          <b>选股框架：</b>李博采用GARP策略，量化为PEG小于<b>1</b>、未来三年复合增速超过<b>15%</b>、当年预测PE低于<b>20倍</b>三项指标，先在全市场初筛三四百只标的再收窄为核心股票池；富国王保合以<b>PB-ROE</b>框架构建基础投资池，认为成长风格向价值风格的切换正在进行；华安苏圻涵、王超采用“核心＋卫星”，核心仓位<b>六至七成</b>、卫星仓位<b>三至四成</b>。<br>
          <b>建仓节奏：</b>汇添富吴振翔表示将采取分批建仓、在封闭期内相对均匀建仓；林心龙计划分阶段较均匀地平稳建仓，以<b>上市前股票仓位达到90%以上</b>为参考目标，并随募集进度、市场环境和上市安排动态优化节奏。<br>
          <b>对腾安启示：</b>拟任基金经理的后市判断属个人观点而非业绩承诺，对客展示须标注发言人、所属机构与发言日期，禁止摘取“回调释放估值压力”一类表述作为买入建议；GARP、PB-ROE、“核心＋卫星”等策略名词须配通俗解释并标注为投资框架描述；建仓节奏属产品运作安排，不得与募集规模或预期收益并列展示。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/ARff1511f8-27e6-cad9-0b09-3a2476356210" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-23</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>'''
src = src[:s] + new_s0 + src[e:]
drift('step3')

# ---------------- Step 3b: S0 section-context（换卡后必须另一步改，历史复发 2 次） ----------------
sub1('<span class="section-context">10月22日 · 4条今日要闻</span>',
     '<span class="section-context">10月23日 · 4条今日要闻</span>', 'S0 context')
drift('step3b')

# ---------------- Step 4: S2 删 10-08 越界卡 ----------------
a = '      <!-- S2 Card: 浙江证监局对两家私募出具警示函'
b = '      <!-- S2 Card: 新规落地首周'
s = src.find(a); e = src.find(b, s)
assert s > 0 and e > s
seg = src[s:e]
assert seg.count('<div class="card p') == 1, seg.count('<div class="card p')
src = src[:s] + src[e:]
drift('step4  (expect -6/-6)')

# ---------------- Step 5: S6 行情 ----------------
a = '                                <div class="card p3">'
b = '      </div>  </div>\n\n<!-- ============ Section 7'
s = src.find(a); e = src.find(b, s)
assert s > 0 and e > s
e += len('      </div>  </div>')
seg = src[s:e]
print('S6 seg open/close', len(re.findall(r'<div\b', seg)), seg.count('</div>'))

new_s6 = '''                                <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股、港股、美股统一10-22收盘·沪指3658.03 -1.48%｜纳指跌2.60%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-22</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-22收盘）</b><br>
              上证指数 <b>3658.03</b> <span style="color:#52c41a;">-1.48%</span>（-55.00点）<br>
              深证成指 <b>11357.32</b> <span style="color:#52c41a;">-2.96%</span>（-347.03点）<br>
              创业板指 <b>2576.90</b> <span style="color:#52c41a;">-4.37%</span>（-117.81点）<br>
              沪深北三市成交 <b>1.54万亿元</b><br>
              其中沪深两市约 <b>15287亿元</b>（沪市约7061亿元＋深市约8226亿元）<br>
              个股 上涨<b>535只</b>·下跌<b>4999只</b>（涨停33只·跌停55只）
            </div>
            <div>
              <b>港股（10-22收盘）与美股（美东10-22收盘）</b><br>
              恒生指数 <b>22934.68</b> <span style="color:#52c41a;">-3.03%</span>（-717.19点）<br>
              国企指数 <b>7689.19</b> <span style="color:#52c41a;">-3.20%</span>（-254.22点）<br>
              恒生科技 <b>3793.93</b> <span style="color:#52c41a;">-5.03%</span>（-200.84点）<br>
              道琼斯 <b>52867.98</b> <span style="color:#dc2626;">+0.02%</span>（+11.89点）<br>
              纳斯达克 <b>26008.86</b> <span style="color:#52c41a;">-2.60%</span>（-694.00点）<br>
              标普500 <b>7663.43</b> <span style="color:#52c41a;">-1.21%</span>（-93.74点）<br>
              港股主板成交 <b>2560.51亿港元</b><br>
              纽约12月交货原油 <b>99.47美元/桶</b> <span style="color:#dc2626;">+2.39%</span><br>
              伦敦12月交货布伦特 <b>113.17美元/桶</b> <span style="color:#dc2626;">+4.0%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>10月22日收盘</b>（10月22日为交易日且已收盘）；上证指数、深证成指、创业板指收盘点位与涨跌幅经行情数据终端与公开报道双源交叉印证；沪深北三市全天成交<b>1.54万亿元</b>、较前一交易日放量约千亿元，取自东方财富Choice数据（长沙晚报10月23日报道引述）；沪市约<b>7061亿元</b>、深市约<b>8226亿元</b>为沪深两市分市场成交额（东方财富Choice行情数据），合计约15287亿元，与沪深北三市口径统计范围不同，本期仅并列列出、不与上述数字混用；个股涨跌家数与涨跌停家数同为东方财富Choice口径。港股取<b>10月22日收盘</b>（新华社香港10月22日电，与行情数据终端互相印证）。美股取<b>美东10月22日收盘</b>（新华社纽约10月22日电／新华财经，记者刘亚南，对应北京时间10月23日凌晨）。国际原油取<b>10月22日收盘</b>（新华财经：纽约商品交易所12月交货轻质原油期货价格、12月交货伦敦布伦特原油期货价格）。贵金属本期未取得可在同一源内交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-22）：</b>三大指数放量下挫，沪指跌1.48%失守3700点整数关口，创业板指跌4.37%续创一年多新低。行业板块呈现普跌态势，仅医疗美容、机器人、工程机械板块逆市上涨，影视院线、广告营销、传媒、元件、教育、互联网电商、游戏板块跌幅居前；个股上涨535只、涨停33只，下跌4999只、跌停55只。银行板块局部回暖，工商银行、建设银行盘中双双创出历史新高。长沙晚报10月23日报道将当日大跌归因于三方面：地缘冲突升级推升避险情绪；AI交易可持续性质疑发酵，光模块、算力硬件等前期热门方向集中杀跌；宁德时代、亿纬锂能、湖南裕能等创业板权重股三季报单季利润增速不达预期，波及整个新能源链条。<br>
              <b>港股（10-22）：</b>新华社香港10月22日电，香港恒生指数跌717.19点、跌幅<b>3.03%</b>收报<b>22934.68</b>点，全日主板成交<b>2560.51亿港元</b>；国企指数跌254.22点、跌幅3.2%收<b>7689.19</b>点；恒生科技指数跌200.84点、跌幅5.03%收<b>3793.93</b>点。蓝筹股方面腾讯控股跌<b>2.89%</b>收报382.4港元、香港交易所跌1.5%收报367.2港元、中国移动跌0.26%收报77.35港元、汇丰控股跌1.23%收报144港元。<br>
              <b>美股（美东10-22）：</b>新华社纽约10月22日电，纽约股市三大股指22日涨跌不一。道琼斯工业平均指数比前一交易日上涨11.89点、涨幅0.02%收于<b>52867.98</b>点；标准普尔500种股票指数下跌93.74点、跌幅1.21%收于<b>7663.43</b>点；纳斯达克综合指数下跌694.00点、跌幅2.60%收于<b>26008.86</b>点。板块方面，标普500指数十一大板块六涨五跌，必需消费品板块和公用事业板块分别以<b>3.11%</b>和<b>1.98%</b>涨幅领涨，通信服务板块和科技板块分别以3.01%和3.00%跌幅领跌。<br>
              <b>对腾安提示：</b>本日A股、港股与美股科技板块同步承压，境内外风险偏好一致回落，货架与持仓页须按各自市场分别刷新净值日期与估值口径，不得用单一指数涨跌概括全市场；A股放量下跌的同时ETF单日净流入创近三个月新高，“指数下跌—资金借道ETF加仓”的背离结构须在对客材料中说明为资金流向统计、不等于指数企稳信号；恒生科技单日跌逾5%，港股主题产品的净值波动提示与申赎确认时点须同步前置；国际油价单日大涨，涉及原油、商品类主题基金的估值提示须同步更新。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-22收盘，美股为美东2026-10-22收盘</span>
          <span class="source-tag">数据来源：东方财富Choice（A股）；新华社（港股、美股）；新华财经（国际原油）</span>
        </div>
      </div>  </div>'''
src = src[:s] + new_s6 + src[e:]
drift('step5')

# ---------------- Step 6: S7 时间线 ----------------
a = '            <div class="timeline-item">'
s = src.find(a)
assert s > 0 and src.count(a) == 1
last = src.rfind('      <div class="timeline-item">')
assert last > s
e = src.find('      </div>\n\n    </div>', last)
assert e > last
e += len('      </div>')
seg = src[s:e]
print('S7 seg items', seg.count('class="timeline-item"'))

items = [
    ('red',   '2026-10-23', '首批18只主动ETF今日开售'),
    ('red',   '2026-10-23', '5家公募自购合计约13亿元'),
    ('blue',  '2026-10-23', 'ETF单日净流入创近三月新高'),
    ('blue',  '2026-10-23', '证监会部署深化公募基金改革'),
    ('red',   '2026-10-22', '沪指跌1.48%失守3700点'),
    ('blue',  '2026-10-22', '创业板指跌4.37%创一年新低'),
    ('blue',  '2026-10-22', '恒生科技跌5.03%破3800点'),
    ('blue',  '2026-10-22', '纳指跌2.60%科技股遭抛售'),
    ('blue',  '2026-10-22', '布伦特原油涨4%收113美元'),
    ('blue',  '2026-10-21', '沪指收3713.03点跌0.60%'),
    ('red',   '2026-10-20', '央行拟设非银流动性支持工具'),
    ('blue',  '2026-10-16', '首批新能源金属50ETF获批'),
]
for _, d, t in items:
    assert len(t) <= 25, t
    assert d >= T14.isoformat(), d
blocks = []
for dot, d, t in items:
    blocks.append(
        '      <div class="timeline-item">\n'
        f'        <div class="timeline-dot {dot}"></div>\n'
        f'        <div class="timeline-date">{d}</div>\n'
        f'        <div class="timeline-title">{t}</div>\n'
        '      </div>')
new_s7 = '\n'.join(blocks)
src = src[:s] + new_s7 + src[e:]
drift('step6')

# ---------------- 全量自检 ----------------
o, c = drift('FINAL')
# 预期漂移 = -6（S2 删 1 张 10-08 越界卡）；S0/S6/S7 结构同构、Stats Bar 同构 → 净 -6
assert o == c == 243 - 6, f'div imbalance {o}/{c}'
assert src.count('</div>>') == 0
assert src.count('\ufffd') == 0
assert 'Section 8' not in src
print('S8 absent OK')

# 全文件 mm-dd 越界
bad = []
for m in re.finditer(r'(\d{2})-(\d{2})', src):
    mo, d = int(m.group(1)), int(m.group(2))
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        continue
    try:
        dt = date(TODAY.year, mo, d)
    except ValueError:
        continue
    if dt > TODAY or dt < T14:
        bad.append((m.group(0), src[max(0, m.start()-60):m.start()+30].replace('\n', ' ')))
print('mm-dd out of window:', len(bad))
for x in bad:
    print('  ', x)

# S0 六项
s0 = src[src.find('Section 0:'):src.find('Section 1:')]
assert s0.count('<div class="card p') == 4, s0.count('<div class="card p')
assert re.findall(r'<span class="section-title">([^<]*)</span>', s0) == ['今日焦点']
assert re.findall(r'<span class="section-context">([^<]*)</span>', s0) == ['10月23日 · 4条今日要闻']
assert s0.count('class="date-tag"') == 4
# 链接数按每卡实算：卡1×2（中国基金报＋中证报）+ 卡2×2（新浪＋财联社）+ 卡3×1 + 卡4×1 = 6
assert s0.count('<a href=') == 6, s0.count('<a href=')
assert s0.count('action-box') == 1
print('S0 checks OK; action-box', s0.count('action-box'))

# 黑名单
BL = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com', 'toutiao',
      'so.html5.qq.com', '163.com/dy', 'cqcb.com', 'weibo.com', 'k.sina.com.cn', 'dy.163.com',
      'q.fund.sohu.com', 'topnews.cn', 'futunn.com', 'jiantou8.com', 'cofool.com', 'yanglee.com']
hits = [(b, u) for u in re.findall(r'href="(https?://[^"]+)"', src) for b in BL if b in u]
print('blacklist hits:', hits)
assert not hits

# 各 section 卡起始 depth 单值
secs = [(m.group(1), m.start()) for m in re.finditer(r'Section (\d):', src)] + [('END', len(src))]
for i in range(len(secs) - 1):
    name, st = secs[i]
    en = secs[i + 1][1]
    sub = src[st:en]
    if sub.count('<div class="card p') == 0:
        continue
    depths = set()
    for m in re.finditer(r'<div class="card p', sub):
        gt = sub.find('>', m.end())
        cls = sub[m.end():gt]
        depth = 0
        pos = m.start()
        while True:
            nxt = sub.find('<div', pos + 1)
            if nxt == -1 or nxt > m.start():
                break
        # 用前缀统计
        prefix = sub[:m.start()]
        depth = len(re.findall(r'<div\b', prefix)) - prefix.count('</div>')
        depths.add(depth)
    print(f'S{name} card start depths:', sorted(depths), 'cards', sub.count('<div class="card p'))
    assert len(depths) == 1

# S7 条数
s7 = src[src.find('Section 7:'):]
assert s7.count('class="timeline-item"') == 12, s7.count('class="timeline-item"')
assert s7.count('timeline-desc') == 0
print('S7 items 12 OK')

# S1/S2 卡数
for name, a2, b2 in [('S1', 'Section 1:', 'Section 2:'), ('S2', 'Section 2:', 'Section 3:')]:
    sub = src[src.find(a2):src.find(b2)]
    print(name, 'cards', sub.count('<div class="card p'))
    assert sub.count('<!-- S%s Card' % name[1]) == sub.count('<div class="card p') or name == 'S1'

open('index.html', 'w', encoding='utf-8').write(src)
print('WRITE OK, len', len(src))
