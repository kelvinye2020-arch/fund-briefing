#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-30 (周三)"""
import re, sys, io, shutil
from datetime import date, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PATH = 'index.html'
TODAY = date(2026, 9, 30)
T14 = TODAY - timedelta(days=14)      # 2026-09-16
MMDD = '09-30'
PREV = '09-29'

src = open(PATH, encoding='utf-8').read()
o0 = len(re.findall(r'<div\b', src)); c0 = len(re.findall(r'</div>', src))
print(f'[init] div open={o0} close={c0}')

# 备份
shutil.copy(PATH, 'index.html.bak_0930')

def drift(tag):
    o = len(re.findall(r'<div\b', src)); c = len(re.findall(r'</div>', src))
    print(f'  [{tag}] open={o} close={c} drift_o={o-o0} drift_c={c-c0}')
    return o - o0, c - c0

def card_bounds(s, title_key, start_from=0):
    """返回 (start, end)：完整 <div class="card pX"> ... </div> 区间（含尾随换行由调用方处理）"""
    ti = s.index(title_key, start_from)
    st = s.rindex('<div class="card p', 0, ti)
    depth = 1
    i = st
    while depth > 0:
        nd = s.find('<div', i + 4)
        nc = s.find('</div>', i + 4)
        if nc == -1:
            raise ValueError('unbalanced at %d' % i)
        if nd != -1 and nd < nc:
            depth += 1
            i = nd
        else:
            depth -= 1
            i = nc
    return st, i + len('</div>')

# ============ 1. marker ============
src, n = re.subn(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
                 f'<!-- daily-update: {TODAY} -->', src)
assert n == 1, f'marker sub n={n}'
print('[1] marker ->', TODAY)

# ============ 2. header 数据区间 badge ============
EMO = '\U0001F4C5'
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
pat = re.compile(re.escape(EMO) + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
src, n = pat.subn(f'{EMO} 数据区间：{lower} — {upper}（每日更新）', src)
assert n == 1, f'badge sub n={n}'
print(f'[2] badge -> {lower} — {upper}')

# ============ 3. content-fingerprint ============
FP = '绩优基金|摊余成本|ETF资金|节前固收'
src, n = re.subn(r'<meta name="content-fingerprint" content="[^"]*">',
                 f'<meta name="content-fingerprint" content="{FP}">', src)
assert n == 1, f'fp sub n={n}'
print('[3] fingerprint ->', FP)

# ============ 4. Stats Bar 沪指卡 ============
OLD_STAT = '''    <div class="stat-card">
      <div class="stat-number">3823.62</div>
      <div class="stat-label">沪指9-28收盘·跌1.67%·沪深北三市成交1.72万亿·放量495亿</div>
      <div class="stat-change down">▼ 创业板指跌4.53%·超4500股下跌·元件通信领跌</div>
    </div>'''
NEW_STAT = '''    <div class="stat-card">
      <div class="stat-number">3830.45</div>
      <div class="stat-label">沪指9-29收盘·涨0.18%·沪深北三市成交1.42万亿·创近14个月地量</div>
      <div class="stat-change up">▲ 近3500股上涨·地产链领涨·科创50涨0.86%</div>
    </div>'''
assert OLD_STAT in src
src = src.replace(OLD_STAT, NEW_STAT)
print('[4] stats bar -> 3830.45 +0.18%')
drift('stats')

# ============ 5. S0 今日焦点：整块换卡 ============
S0_START = src.index('    <div class="card-grid">', src.index('Section 0: 今日焦点'))
S0_END = src.index('    </div>\n  </div>\n<!-- ============ Section 1')

SRC_A = 'https://finance.china.com.cn/money/fund/20260930/6325292.shtml'
SRC_A2 = 'https://www.cnstock.com/commonDetail/797369'
SRC_B = 'https://3w.huanqiu.com/a/c36dc8/4TPw7PaAEQi'
SRC_B2 = 'https://www.chnfund.com/article/ARbba699e3-9927-d7f6-4d24-3a23fe145817'
SRC_C = 'https://www.gelonghui.com/live/2694387'
SRC_D = 'https://m.cnfin.com/gs-lb/zixun/20260928/4475654_1.html'
SRC_D2 = 'https://finance.sina.cn/2026-09-29/detail-initpatz6137379.d.html'

def link(u, tag):
    return (f'<a href="{u}" target="_blank" style="color:#1890ff;text-decoration:none;">'
            f'<span class="source-tag">{tag}</span></a>')

CARDS = []

CARDS.append(f'''<!-- S0 Card 1 (09-30 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 绩优基金集中“松绑”限购·易方达信息产业混合与信息行业精选单日上限提至50万元</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报（记者朱妍）9月30日报道：绩优基金的限购金额调整，正在成为观察行情冷暖的一项参考指标。近期<b>易方达、汇安</b>等基金公司对旗下绩优基金放宽限购金额，且部分产品近一年业绩出彩。以<b>郑希</b>管理的易方达信息产业混合、易方达信息行业精选为例，相关公告显示，自<b>9月22日起</b>这两只基金调整大额申购及大额转换转入业务限制，单日单个基金账户在全部销售机构累计申购（含定期定额投资及转换转入）A类或C类份额金额不超过<b>50万元（含）</b>。高位限购防止资金追高涌入、市场回调后再放宽限制，已逐渐成为公募基金高质量发展之下的行业常态。<br>
          <b>三点归因：</b>格上基金研究员蒋睿对上海证券报记者表示，近期多只绩优基金放宽限购的原因有三——①上半年资金追捧带来的管理压力随着市场调整而缓释；②科技板块估值消化后，部分基金经理对后市信心修复，愿意逆势布局；③产品为承接配置需求、改善资金流入情况。放宽限购额度一定程度上释放出市场存在结构性机会的信号。<br>
          <b>节前节奏：</b>金鹰基金投研人士表示，多组关键宏观数据将在国庆假期期间公布，包括<b>10月2日公布的美国9月非农就业数据</b>等，地缘政治相关谈判亦可能在假期持续发酵，节前A股或更大概率延续防守姿态。国联安基金人士建议重点关注<b>节前最后一个交易日与节后首个交易日</b>两个布局窗口；汇丰晋信股票研究总监闵良超认为A股整体盈利处于上行周期，三季度以来高波动调整后市场拥挤度已有所缓解，科技类与AI相关行业仍可能有景气性机会。<br>
          <b>对腾安启示：</b>限购松紧是管理人给出的隐性仓位与估值信号，比口头观点更有信息量——建议把<b>“单日申购上限变更”做成货架可展示的时间序列标签</b>（上限上调/下调/暂停三态），对同一基金经理在管产品做联动提示，并在松绑时同步给出“管理人认为估值风险已部分释放”与“资金涌入可能摊薄后续收益”两面解读；同时提示节前最后一个交易日是全年少数几个申赎确认跨假期的时点，须在页面显著位置标注确认与到账规则。
        </div>
        <div class="card-footer">
          {link(SRC_A, '中国网财经·上海证券报·09-30')}
          {link(SRC_A2, '上海证券报·09-30')}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

CARDS.append(f'''<!-- S0 Card 2 (09-30 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 摊余成本法债基受捧·首批7只中4只提前结募·已成立3只均触及80亿元上限</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
          环球网9月30日报道（中国基金报同步披露）：继贝莱德、红土创新之后，<b>财信基金、路博迈基金</b>旗下63个月封闭式债券基金也提前结束募集。首批发行的7只摊余成本法债基中已有<b>4只提前结募</b>，其中<b>已成立的3只募集规模均触及80亿元上限</b>。<br>
          <b>最新两只：</b>9月29日财信基金公告，财信聚鑫63个月封闭式债券于9月21日开始募集、原定12月18日截止，为保护投资者利益提前至<b>9月28日</b>结束募集、自9月29日起不再接受认购；此前9月24日路博迈基金公告，路博迈安瑞63个月封闭式债券同样9月21日开募，提前至9月23日、9月24日起停止认购，<b>9月28日成立，有效认购总户数258户、净认购金额80亿元</b>。更早的9月22日与9月23日，红土创新瑞泽、贝莱德稳利已率先宣布提前结募，募集期分别仅三天与两天。<br>
          <b>政策节奏：</b>作为支持中小基金公司发展的重要举措，摊余成本法债基从上报、获批到发行明显加快——<b>8月14日</b>百嘉、贝莱德、路博迈、安联、联博、红土创新、尚正、朱雀、鹏安、财信、国融、华西、易米、兴合、兴华等15家中小基金公司率先获得申报资格，仅一个月后<b>9月14日</b>15只产品正式获批，其中7只率先启动发行、募集上限均为80亿元；9月11日汇泉、博远、东方阿尔法、泉果、益民、泰信、汇百川、瑞达、中海、博道、恒越、东财、苏新等13家已上报第二批，<b>两批合计28家</b>。<br>
          <b>对腾安启示：</b>63个月封闭期产品是“加强版定存”而非保本——货架必须把<b>封闭期/封闭期内不可申赎/摊余成本法不等于保本/底层债券违约仍需计提减值</b>四项前置到购买页，受众严格锁定五年以上闲置资金、厌恶净值波动的客群，不得与货基、短债并列在“灵活取用”入口；机构端可跟踪四季度集中建仓对5年期左右信用债的需求支撑，提前准备相关债券类产品的配置话术。
        </div>
        <div class="card-footer">
          {link(SRC_B, '环球网·09-30')}
          {link(SRC_B2, '中国基金报·09-29')}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

CARDS.append(f'''<!-- S0 Card 3 (09-30 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 ETF资金流·09-29债券与货币占TOP20十席·短融ETF海富通净流入31.76亿居首</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇9月30日资金流向观察：9月29日ETF资金净流入TOP20榜单中，<b>债券类ETF占据7席、货币类3只上榜</b>。<br>
          <b>债券类：</b>短融ETF海富通（511360）单日净流入<b>31.76亿元</b>居全市场净流入首位、最新规模872.48亿元；科创债ETF共4只上榜——银华14.61亿元（规模289.36亿元）、易方达10.26亿元（201.28亿元）、嘉实8.93亿元（465.42亿元）、工银2.94亿元（133.70亿元），<b>4只合计约36.74亿元</b>；30年国债ETF鹏扬净流入6.35亿元（386.17亿元）；信用债ETF海富通3.33亿元（213.09亿元）。<br>
          <b>货币类：</b>银华日利ETF净流入17.98亿元（规模1099.66亿元）、华宝添益ETF净流入11.87亿元（1076.84亿元），<b>两只千亿级品种合计约29.85亿元</b>；货币ETF易方达4.02亿元（50.89亿元）。<br>
          <b>解读：</b>节前倒数第二个交易日，资金明显从权益向“票息＋现金”迁移——债券与货币两类合计占据TOP20十席，与当日A股成交萎缩至<b>1.42万亿元</b>的地量相互印证，是典型的假期避险与闲置资金“过节”安排，而非风险偏好转向。<br>
          <b>对腾安启示：</b>长假前“闲钱去哪儿”是每年固定的高意图流量入口，货架应提前上线<b>节前资金安排专区</b>并按“可买/已限购/10月8日恢复”三态标注各货基与短债状态，同时给出通用回购逆回购等替代工具的门槛与计息规则说明，避免用户因申购被拒而流失。
        </div>
        <div class="card-footer">
          {link(SRC_C, '格隆汇·09-30')}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

CARDS.append(f'''<!-- S0 Card 4 (09-29 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 节前固收类基金批量限购·新华财经统计超120只、Wind口径约180只·多数10月8日恢复</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-29</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月28日报道（记者翟卓）：国庆长假临近，多只债券型基金、货币市场基金、同业存单指数基金“闭门谢客”。据不完全统计，截至9月28日已有<b>超120只基金</b>发布公告暂停申购或大额申购等业务，多数产品暂停起始日为9月29日、恢复日为10月8日。新浪财经9月29日援引Wind数据称，<b>自9月21日以来约180只基金</b>调整额度限制甚至暂停申购，主要为货币基金、债券型基金、同业存单指数基金，多数将恢复时间精准卡在长假后首个交易日。<br>
          <b>为何限购：</b>公告普遍说明暂停业务旨在维护基金规模良性增长、保护基金份额持有人利益。业内专家表示，以货基为例有两层考虑——①<b>保障收益公平</b>：假期市场休市但已确认份额仍按日计提收益，若节前大量资金涌入并完成确认，新增资金假期暂无投资标的却参与收益分配，将摊薄存量持有人收益；②<b>规模管理</b>：节前短期集中涌入的资金可能超出基金经理的配置能力与策略容量，干扰既定投资安排。<br>
          <b>扩散至权益：</b>节前限购潮亦延伸至部分权益与港股通产品——华泰柏瑞港股通量化自9月29日起限额1000元，中银港股通优势成长、中银中证港股通高股息投资指数、中银中证港股通互联网指数等在节前也有相关限制；业内人士称主因是港股通交易安排与A股不一致的时间窗口内，防止短期资金对存量持有人利益形成实质性摊薄。<br>
          <b>体量：</b>中基协数据显示，截至2026年8月底市场货币基金、债券基金分别有358只、4010只，规模达<b>16.31万亿元、11.97万亿元</b>，二者合计占公募基金总规模（39.63万亿元）超七成。<br>
          <b>对腾安启示：</b>固收类（货基＋债基）是腾安非货与货基保有量的基本盘，节前限购会直接造成“想买买不了”的体验断点——须把各产品的<b>限购状态、限额金额、恢复日期</b>做成可按日更新的字段并在申购前强提示，同时在专区给出未限购的替代品种与替代工具，把限购从“交易失败”转化为“资金安排建议”。
        </div>
        <div class="card-footer">
          {link(SRC_D, '新华财经·09-28')}
          {link(SRC_D2, '新浪财经·09-29')}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

s0_new = '    <div class="card-grid">\n' + '\n'.join(CARDS)
src = src[:S0_START] + s0_new + src[S0_END:]
print('[5] S0 4 cards rebuilt')
drift('s0')

# section-context
OLD_CTX = '<span class="section-context">9月29日 · 4条今日要闻</span>'
NEW_CTX = '<span class="section-context">9月30日 · 4条今日要闻</span>'
assert src.count(OLD_CTX) == 1
src = src.replace(OLD_CTX, NEW_CTX)
print('[5b] section-context ->', NEW_CTX)

# ============ 6. S4 删「科技主题基金松绑限购」卡（与 S0 Card1 同事件撞题） ============
A = src.index('      <!-- S4 Card: 科技主题基金松绑限购 (09-28 P2) -->')
B = src.index('      <!-- S4 Card: 9月31只ETF成立 科技成长主线 (09-21 P1) -->')
src = src[:A] + src[B:]
print('[6] S4 删除 09-28 松绑卡（去重）')
drift('s4')

# ============ 7. S5 删 09-15 兴证全球卡（T-14 越界） ============
st5, en5 = card_bounds(src, '兴证全球以"可信AI"构建资管流水线')
seg = src[st5:en5]
assert '09-15' in seg, seg[:200]
# 连同尾随空行一起删
tail = 0
while src[en5 + tail:en5 + tail + 1] == '\n':
    tail += 1
src = src[:st5] + src[en5 + tail:]
print('[7] S5 删除 09-15 兴证全球卡（T-14 越界，边界 %s）' % T14)
drift('s5')

# ============ 8. S6 行情卡：09-29 收盘 ============
S6_START = src.index('            <div class="card p3">', src.index('Section 6'))
S6_END = src.index('      </div>  </div>\n<!-- ============ Section 7')

GREEN = '#52c41a'   # 跌
RED = '#dc2626'     # 涨

s6_new = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股09-29收盘·沪指3830.45 +0.18%沪深北成交1.42万亿｜港股与美股09-29收盘</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-29收盘·节前地量小幅反弹）</b><br>
              上证指数 <b>3830.45</b> <span style="color:#dc2626;">+0.18%</span><br>
              深证成指 <b>12901.95</b> <span style="color:#dc2626;">+0.34%</span><br>
              创业板指 <b>3142.56</b> <span style="color:#dc2626;">+0.09%</span><br>
              沪深300 <b>4345.21</b> <span style="color:#dc2626;">+0.10%</span><br>
              科创50 <b>1569.34</b> <span style="color:#dc2626;">+0.86%</span><br>
              科创综指 <b>1848.72</b> <span style="color:#dc2626;">+0.69%</span><br>
              北证50 <b>1032.36</b> <span style="color:#dc2626;">+0.56%</span><br>
              沪深北三市成交 <b>1.42万亿</b>·创2025年7月8日以来地量·较上一交易日缩量约2950亿<br>
              近3500只上涨·近60只涨停
            </div>
            <div>
              <b>港股与美股（09-29收盘）</b><br>
              恒生指数 <b>24523.57</b> <span style="color:#52c41a;">-0.48%</span><br>
              恒生科技 <b>4249.62</b> <span style="color:#52c41a;">-1.08%</span><br>
              国企指数 <b>8178.81</b> <span style="color:#52c41a;">-0.46%</span><br>
              道琼斯 <b>51349.92</b> <span style="color:#52c41a;">-0.26%</span><br>
              纳斯达克 <b>26797.54</b> <span style="color:#52c41a;">-0.09%</span><br>
              标普500 <b>7670.84</b> <span style="color:#52c41a;">-0.17%</span><br>
              布伦特原油102.59美元 <span style="color:#52c41a;">-2.56%</span>·COMEX黄金4215.00美元 <span style="color:#dc2626;">+1.12%</span>·美债10年期5.232%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>A股结构（09-29）：</b>三大指数低开后全天红绿转换超10次、午后集体拉升、尾盘小幅回落，最终小幅收红。行业板块多数收涨——<b>元件、电池、房地产开发、广告营销、房地产服务、传媒、影视院线、能源金属</b>涨幅居前，航天装备跌幅居前；<b>房地产板块大涨</b>，万科A、深物业A、信达地产、华发股份、滨江集团、华联控股等涨停。资金方面元件净流入29.21亿元居首。成交1.42万亿元创2025年7月8日以来新低，较2026年1月14日历史天量39414.84亿元萎缩超六成，节前观望气氛浓厚。<br>
              <b>港股（09-29）：</b>恒指跌0.48%报24523.57点、恒生科技跌1.08%报4249.62点、国企指数跌0.46%报8178.81点，全日主板成交1846.30亿港元。<br>
              <b>美股（09-29）：</b>三大指数小幅收跌，美债收益率高位徘徊继续压制风险偏好——10年期报5.232%（跌0.41BP）、30年期升至5.567%（涨2.04BP），盘中10年期一度触及5.293%创2007年6月以来新高。大型科技股涨跌不一，脸书涨超3%、亚马逊涨0.21%、苹果跌超2%、英伟达跌0.72%；存储概念多数上涨，SK海力士涨超2%、美光科技涨超1%；能源股全线收跌。中概股多数下跌，纳斯达克中国金龙指数跌1.55%。油价因中东出口恢复与美伊斡旋信号显著回落，COMEX黄金反弹1.12%报4215.00美元；CME FedWatch显示10月加息25个基点概率由盘中近70%回落至<b>51.5%</b>。<br>
              <b>备注：</b>09-29为国庆假期前倒数第二个交易日，本期A股、港股、美股基准统一为09-29收盘。国庆假期安排：A股10月1日—7日休市、10月8日开市。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股 / 港股 / 美股均为2026-09-29收盘</span>
          <span class="source-tag">数据来源：新华财经、中新经纬、中国新闻网、新浪财经、格隆汇、东方财富行情（09-29—09-30）</span>
        </div>
'''
src = src[:S6_START] + s6_new + src[S6_END:]
print('[8] S6 -> 09-29 收盘')
drift('s6')

# ============ 9. S7 时间线重写 12 条 ============
S7_START = src.index('      <div class="timeline-item">', src.index('Section 7'))
_ANCH = '      </div>    </div>\n'
S7_END = src.index(_ANCH, S7_START) + len(_ANCH)   # 含容器闭合，一并替换

TL = [
    ('red',   '2026-09-30', '绩优基金集中松绑限购'),
    ('blue',  '2026-09-30', '摊余债基四只提前结募'),
    ('blue',  '2026-09-30', '固收基金节前批量限购'),
    ('blue',  '2026-09-30', 'ETF资金流向债券货币'),
    ('blue',  '2026-09-29', '半导体主题基金破3900亿'),
    ('red',   '2026-09-29', 'A股地量反弹成交1.42万亿'),
    ('blue',  '2026-09-29', '地产板块大涨多股涨停'),
    ('blue',  '2026-09-29', '恒指回落美股小幅收跌'),
    ('blue',  '2026-09-28', '债券ETF规模首破万亿'),
    ('blue',  '2026-09-28', '险资可投港股通ETF开闸'),
    ('blue',  '2026-09-28', '商业不动产REITs三只受理'),
    ('blue',  '2026-09-25', '湖南百亿未来产业基金落地'),
]
items = []
for c, d, t in TL:
    assert len(t) <= 25, f'title too long ({len(t)}): {t}'
    items.append(
        f'      <div class="timeline-item">\n'
        f'        <div class="timeline-dot {c}"></div>\n'
        f'        <div class="timeline-date">{d}</div>\n'
        f'        <div class="timeline-title">{t}</div>\n'
        f'      </div>\n'
    )
src = src[:S7_START] + ''.join(items) + '    </div>\n' + src[S7_END:]
print('[9] S7 -> %d 条' % len(TL))
drift('s7')

# ============ 10. 全量断言 ============
errs = []
o = len(re.findall(r'<div\b', src)); c = len(re.findall(r'</div>', src))
if o != c:
    errs.append(f'div 不平衡 {o}/{c}')

# S8
if 'Section 8' in src or '待办跟踪' in src or '腾安行动清单' in src:
    errs.append('S8 残留')

# S0
s0 = src[src.index('Section 0: 今日焦点'):src.index('Section 1:')]
if s0.count('<span class="section-title">今日焦点</span>') != 1:
    errs.append('S0 section-title 不等于「今日焦点」')
if NEW_CTX not in s0:
    errs.append('S0 section-context 未更新')
tags = re.findall(r'date-tag">(\d{2})-(\d{2})</span>', s0)
print('  S0 date-tags:', tags)
if tags != [('09', '30'), ('09', '30'), ('09', '30'), ('09', '29')]:
    errs.append(f'S0 date-tags 异常 {tags}')
if len(re.findall(r'<div class="card p\d"', s0)) != 4:
    errs.append('S0 卡数 != 4')
_nlink = s0.count('href="http')
if _nlink != 7:
    errs.append(f'S0 链接数 {_nlink} != 7')
if s0.count('action-box') != 0:
    errs.append('S0 不应含 action-box（本日无 P0）')

# 全文件 date-tag T-14
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
    mo, d = int(m.group(1)), int(m.group(2))
    dt = date(2026, mo, d)
    if dt < T14:
        before = src[max(0, m.start() - 1500):m.start()]
        ts = re.findall(r'<div class="card-title[^>]*>(.*?)</div>', before, re.S)
        errs.append(f'date-tag {dt} < T-14({T14})：{ts[-1][:40] if ts else "?"}')

# 卡片数
def ncard(sec):
    a = src.index(sec); b = src.find('<!-- ============ Section', a + 10)
    b = len(src) if b == -1 else b
    return len(re.findall(r'<div class="card p\d"', src[a:b]))
print('  S1=%d S2=%d S4=%d S5=%d' % (ncard('Section 1:'), ncard('Section 2:'),
                                     ncard('Section 4:'), ncard('Section 5:')))
if ncard('Section 1:') != 6: errs.append('S1 != 6')
if ncard('Section 2:') != 4: errs.append('S2 != 4')
if ncard('Section 5:') != 3: errs.append('S5 != 3')

# timeline 12 条
if src.count('<div class="timeline-item">') != 12:
    errs.append(f'timeline 条目 {src.count("<div class=" + chr(34) + "timeline-item" + chr(34) + ">")} != 12')

# 乱码 / 黑名单
if '\ufffd' in src:
    errs.append('U+FFFD 乱码')
BAD = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com', 'toutiao.com']
for b in BAD:
    if b in src:
        errs.append(f'黑名单域名 {b}')
if '</div>>' in src or '</div> </div>>' in src:
    errs.append('stray </div>>')

# fingerprint 4 段
mfp = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', src)
fps = [x for x in mfp.group(1).split('|') if x.strip()]
titles = [re.sub(r'<[^>]+>', '', t) for t in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', s0, re.S)]
if len(fps) != len(titles):
    errs.append(f'fp 段数 {len(fps)} != S0 卡数 {len(titles)}')
for seg in fps:
    if not any(seg.strip()[:4] in t for t in titles):
        errs.append(f'fp 段「{seg}」在 S0 标题中找不到')

if errs:
    print('\n❌ 断言失败：')
    for e in errs:
        print('   -', e)
    sys.exit(1)

open(PATH, 'w', encoding='utf-8').write(src)
print('\n✅ 写入 index.html 完成，全部断言通过')
