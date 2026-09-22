# -*- coding: utf-8 -*-
"""基金看板 2026-09-22 每日更新：Stats Bar / S0 / S1换卡 / S6 / S7 + header 区间"""
import re, sys
from datetime import date, timedelta

sys.stdout.reconfigure(encoding='utf-8')
P = 'index.html'
h = open(P, encoding='utf-8').read()
orig = h
o0, c0 = len(re.findall(r'<div\b', h)), len(re.findall(r'</div>', h))
print('BASE open=%d close=%d' % (o0, c0))


def dr(tag):
    o, c = len(re.findall(r'<div\b', h)), len(re.findall(r'</div>', h))
    print('  [%s] open=%d close=%d drift_o=%+d drift_c=%+d' % (tag, o, c, o - o0, c - c0))
    return o, c


TODAY = date.today()
UP = TODAY.strftime('%Y.%m.%d')
LOW = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
CUT = (TODAY - timedelta(days=14)).strftime('%m-%d')
print('TODAY=%s WINDOW %s ~ %s  CUTOFF=%s' % (TODAY, LOW, UP, CUT))

# ---------- Step 0: marker + header 区间 ----------
assert h.count('<!-- daily-update: 2026-09-21 -->') == 1, 'marker anchor'
h = h.replace('<!-- daily-update: 2026-09-21 -->', '<!-- daily-update: 2026-09-22 -->')

BADGE_NEW = '📅 数据区间：%s — %s（每日更新）' % (LOW, UP)
h, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', BADGE_NEW, h)
assert n == 1, 'badge sub n=%d' % n
assert BADGE_NEW in h
dr('step0 marker+badge')

# ---------- Step 1: Stats Bar 沪指卡 09-18 -> 09-21 收盘 ----------
OLD_STATS = '''    <div class="stat-card">
      <div class="stat-number">3911.87</div>
      <div class="stat-label">沪指9-18收盘·涨0.94%·沪深两市成交2.08万亿·放量2540亿</div>
      <div class="stat-change up">▲ 创业板+2.25%·科创综指+3.23%·超4200股上涨</div>
    </div>'''
NEW_STATS = '''    <div class="stat-card">
      <div class="stat-number">3949.91</div>
      <div class="stat-label">沪指9-21收盘·涨0.97%·沪深北三市成交2.05万亿·缩量448亿</div>
      <div class="stat-change up">▲ 医药板块领涨·4536股上涨105只涨停</div>
    </div>'''
assert h.count(OLD_STATS) == 1, 'stats anchor'
h = h.replace(OLD_STATS, NEW_STATS)
assert '3949.91' in h and OLD_STATS not in h
dr('step1 stats')

# ---------- Step 2: S0 全量换卡（4 张） ----------
S0_A = '<!-- S0 Card 1 (09-21 P1) -->'
S0_B = '<!-- ============ Section 1'
i0, i1 = h.index(S0_A), h.index(S0_B)
assert i0 < i1
old_s0 = h[i0:i1]
print('  old S0 region: open=%d close=%d' % (
    len(re.findall(r'<div\b', old_s0)), len(re.findall(r'</div>', old_s0))))
assert old_s0.rstrip().endswith('</div>')
assert old_s0.count('card p') == 4

CARDS = []

# --- S0 Card 1 (09-22 P1) 算力主题基金 ---
CARDS.append('''      <!-- S0 Card 1 (09-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募加码布局算力主题·8只创业板算力ETF已募50.97亿·9月又上报7只含首批场外指数</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-22</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报记者赵明超9月22日报道：8月28日首批10只创业板算力主题ETF获批，截至9月21日已有<b>8只</b>成立，发行规模合计<b>50.97亿元</b>——创业板算力ETF易方达<b>14.77亿元</b>、广发<b>13.42亿元</b>居前，富国已结束募集待成立、国泰正在发行。<br>
          <b>上市节奏：</b>天弘、华夏、易方达3只已上市交易，其余<b>5只</b>集中在9月22日至24日上市。<br>
          <b>新品仍在申报：</b>Choice数据显示，9月16日以来又有<b>7只</b>创业板算力主题基金上报，含2只ETF与<b>5只</b>场外指数基金，后者为首批上报的创业板算力场外指数基金。<br>
          <b>持有人现身：</b>上市交易公告书显示首批产品频现机构身影，创业板算力ETF嘉实截至9月17日前十大持有人包括安联人寿－财富成长、招商证券、盛冠达泓冲价值投资私募证券投资基金等。<br>
          <b>机构观点：</b>创业板算力ETF易方达基金经理肖宛远认为，前沿模型在预训练、后训练环节仍需大量算力，智能体与AI应用渗透将打开需求空间；华安基金称国产HBM迎来突破窗口，国产算力核心矛盾在供给端、行业有望重回上行；工银瑞信TMT团队认为“国模国芯”深度融合正拉动国产算力需求。<br>
          <b>对腾安启示：</b>算力主题从ETF扩展到场外指数，意味着没有股票账户的客户也能参与——货架端应把“场内ETF vs 场外指数/联接”并列展示并标注费率与跟踪误差差异；5只新品集中上市首日需提示溢价风险，避免客户在上市初期炒作高点追入。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/793708" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·09-22</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>''')

# --- S0 Card 2 (09-22 P1) 第三方渠道非货基保有首超银行 ---
CARDS.append('''      <!-- S0 Card 2 (09-22 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 第三方渠道非货基保有规模首超银行·上周ETF净流入243.35亿·债券型ETF吸金193.85亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-22</span>
          </div>
        </div>
        <div class="card-body">
          渤海证券研究所9月22日公募基金周报（分析师宋旸、张笑晨，统计区间9月14日—18日）：本周市场热点之一为<b>第三方渠道非货基保有规模首次超过银行</b>，公募销售渠道格局出现标志性变化。<br>
          <b>基金表现：</b>偏股型基金平均上涨<b>2.26%</b>、正收益占比76.89%；量化基金平均涨2.20%、正收益占比86.14%；固收+基金涨0.28%、正收益占比79.24%；纯债型基金涨0.09%、正收益占比98.17%；养老目标FOF涨0.19%、正收益占比72.86%；QDII基金平均<b>下跌0.07%</b>、正收益占比仅39.06%。<br>
          <b>ETF资金：</b>上周ETF市场整体净流入<b>243.35亿元</b>，其中债券型净流入约<b>193.85亿元</b>、商品型39.80亿元，股票型净流出约36.59亿元、跨境型净流出9.57亿元；AAA科创债、科创半导体材料设备分别净流入85.01亿元、66.82亿元，中证短融（净）与中证A500分别净流出23.20亿元、22.06亿元。日均成交额<b>4488.74亿元</b>、日均换手率7.36%。<br>
          <b>仓位与发行：</b>主动权益基金9月18日测算仓位<b>78.20%</b>，较9月11日下降<b>4.37个百分点</b>；加仓靠前的是房地产、美容护理、环保，减仓靠前的是医药生物、商贸零售、电力设备。上周新发行基金<b>30只</b>（较前期减少20只）、新成立<b>46只</b>（增加8只），新基金共募集<b>201.56亿元</b>（增加40.45亿元）。<br>
          <b>对腾安启示：</b>第三方渠道保有规模首超银行，标志代销主战场完成切换——腾安作为互联网渠道应承接银行端流出的债基与固收+需求；但上周主动权益仓位环比降4.37pct、股票型ETF净流出36.59亿，说明机构在反弹中反而减仓，货架端不宜用“机构加仓”话术引导客户追高。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/stock/stockzmt/2026-09-22/doc-inisscmi7148968.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">渤海证券·新浪财经·09-22</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>''')

# --- S0 Card 3 (09-21 P1) 业绩比较基准第三批 ---
CARDS.append('''      <!-- S0 Card 3 (09-21 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募业绩比较基准第三批调整今起生效·97家管理人1685只基金2.15万亿·年内最大一批</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          上海证券基金评价研究中心（分析师赵威、徐一帆等）9月21日发布深度研究：第三批公募基金业绩比较基准集中调整于<b>2026年9月21—22日生效</b>，涉及<b>97家</b>基金管理人、约<b>1685只</b>基金，截至2026年二季度末合计规模<b>2.15万亿元</b>，是2026年基准整改进程中规模最大的一批（前两批分别于6月1日、7月27日生效，共涉约1400只基金，整改过渡期为1年）。<br>
          <b>结构：</b>混合型基金调整数量最多共<b>986只</b>（占59%），债券型基金调整规模最大达<b>1.05万亿元</b>（占49%）；78.2%的基准同时调整了成分与权重。分公司看，调整数量前三位为鹏华71只、博时69只、广发56只；调整规模前三位为永赢1373.80亿元、广发1230.65亿元、易方达989.97亿元。<br>
          <b>三条主线：</b>①偏股混合基金基准中权益成分占比均值由<b>78.0%升至85.9%</b>，落在80%—90%区间的基金数量占比从9.3%跃升至78.8%；②490只灵活配置基金中<b>178只</b>（36.3%）由股债倾向模糊转为明确偏股或偏债；③497只偏债类基金中变更后<b>98.4%</b>的纯债指数采用“中债系”，<b>270只</b>（54.3%）由无久期改为标注久期且集中在1—3年、1—5年中短端。<br>
          <b>两项出清：</b>全部<b>59条</b>绝对收益类基准（偏股29条、偏债30条）改为锚定指数；FOF新增商品（黄金为主）与港股/海外成分，演进为“境内股+境内债+港股/海外+商品”的多元基准结构。<br>
          <b>对腾安启示：</b>基准是评价的“标尺”，标尺一变，历史业绩排名与风格标签将不可直接纵向比较——货架端的基金画像、风格标签与“同类排名”需在10月内同步刷新，避免继续用旧基准下的超额收益做卖点；偏股混合权益占比抬升至85.9%意味着客户持有产品的真实波动高于旧基准认知，风险揭示需相应加强。
        </div>
        <div class="card-footer">
          <a href="https://fund.10jqka.com.cn/20260921/c680122902.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺基金·09-21</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>''')

# --- S0 Card 4 (09-21 P2) 首单煤电REIT ---
CARDS.append('''      <!-- S0 Card 4 (09-21 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 首单煤电REIT启动询价·华能煤电REIT发10亿份询价区间2.716—3.319元·全市场REITs约93只2300亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻记者陈晨9月21日报道：9月21日盘后，长城华能燃煤发电REIT基金管理人发布《询价公告》，成为市场首单启动询价发售的煤电REITs，我国煤电资产公募REITs实现“零的突破”。本次初始发售份额<b>10亿份</b>，询价区间<b>2.716元/份—3.319元/份</b>，网下询价时间为2026年9月28日9:00—15:00。<br>
          <b>注册背景：</b>9月20日证监会准予2只煤电REITs注册（长城华能燃煤发电REIT、华夏华润电力燃煤发电REIT），同日招商资管招商蛇口商业不动产REIT亦获批复；9月以来获批的首发REITs已达<b>8只</b>、年内达<b>28只</b>。2024年7月国家发改委部署基础设施REITs常态化发行时，首次将清洁低碳、灵活高效的燃煤发电（含热电联产煤电）纳入申报范围。<br>
          <b>底层资产：</b>华能煤电REIT底层为华能青岛项目，位于青岛市黄岛区董家口经济区，核心资产为2台350MW热电联产机组及配套供热设施，2022年投运，收入来自发电、供汽、供暖，基金合同期限27年；华夏华润电力燃煤发电REIT底层为华润焦作电厂2×660MW超超临界燃煤热电联产机组，合同期限20年、募集份额总额7亿份。<br>
          <b>市场规模：</b>Wind数据显示，截至9月21日全市场已成立公募REITs达<b>93只</b>、总规模约<b>2300亿元</b>；能源基础设施REITs已上市12只，覆盖风电、光伏、水电、燃气发电等，煤电此前为空白。<br>
          <b>对腾安启示：</b>REITs货架可新增“能源基础设施”细分标签，把煤电与已上市的风电、光伏、水电项目并列比较（现金流来源、机组装机、合同期限、分派率）；需注意煤电REIT收益受容量电价与辅助服务机制影响，与新能源REITs结构不同，首单询价期间不宜用“打新必赚”话术。
        </div>
        <div class="card-footer">
          <a href="https://www.nbd.com.cn/articles/2026-09-21/4587778.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-21</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>''')

new_s0 = '\n\n'.join(CARDS) + '\n    </div>\n  </div>\n'
no0, nc0 = len(re.findall(r'<div\b', new_s0)), len(re.findall(r'</div>', new_s0))
no1, nc1 = len(re.findall(r'<div\b', old_s0)), len(re.findall(r'</div>', old_s0))
print('  new S0 region: open=%d close=%d (old %d/%d)' % (no0, nc0, no1, nc1))
assert no0 == no1 and nc0 == nc1, 'S0 div mismatch'
h = h[:i0] + new_s0 + h[i1:]
dr('step2 S0')

# S0 header context
OLD_CTX = '<span class="section-context">9月21日 · 4条今日要闻</span>'
NEW_CTX = '<span class="section-context">9月22日 · 4条今日要闻</span>'
assert h.count(OLD_CTX) == 1
h = h.replace(OLD_CTX, NEW_CTX)
s0 = h[h.index('<!-- ============ Section 0'):h.index('<!-- ============ Section 1')]
assert s0.count('<span class="section-title">今日焦点</span>') == 1
assert s0.count('card p') == 4
_dts = re.findall(r'date-tag">(\d{2})-(\d{2})<', s0)
assert _dts == [('09', '22'), ('09', '22'), ('09', '21'), ('09', '21')], 'S0 date-tags=%s' % _dts
dr('step2b S0 ctx')

# ---------- Step 3: S1 换卡 1 张（ETF资金卡 09-20 -> 贝莱德QDII 09-18，避免与 S0 卡2 撞题） ----------
S1_A = '<!-- S1 Card: ETF资金向科技成长切换 (09-20 P2) -->'
S1_B = '<!-- ============ Section 2'
j0, j1 = h.index(S1_A), h.index(S1_B)
old_s1 = h[j0:j1]
assert old_s1.count('card p') == 1
new_s1 = '''<!-- S1 Card: 贝莱德基金获批QDII资格 (09-18 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-18</span>
          </div>
          <div class="card-title">🟡 贝莱德基金获批QDII资格·首家新设外资公募·全市场QDII规模已破1.03万亿</div>
        </div>
        <div class="card-body">
          上海证券报记者申一辰报道：证监会发布《关于核准贝莱德基金管理有限公司合格境内机构投资者资格的批复》，贝莱德基金获批QDII资格，成为国内<b>首家</b>获批该资格的新设外资独资公募——此前摩根基金、宏利基金、摩根士丹利基金均在中外合资阶段取得资格，转为外商独资后延续保留。批复要求公司在<b>6个月内</b>完成境外证券投资管理业务筹备。<br>
          <b>准入门槛：</b>证监会相关指南要求基金管理公司净资产不少于<b>2亿元</b>、经营基金管理业务达<b>2年以上</b>、最近一个季度末资产管理规模不低于<b>200亿元</b>或等值外汇资产，并具备相应的境外投资管理人员与治理、内控制度。Choice数据显示，截至目前贝莱德基金公募管理规模<b>181.88亿元</b>、在管基金39只（不同份额分开计算）。<br>
          <b>行业扩容：</b>中基协数据显示，截至2026年8月31日全市场QDII基金总份额达<b>8574.77亿份</b>、整体规模突破<b>1.03万亿元</b>；国家外汇管理局数据显示，2026年3月末QDII获批额度较2025年末新增<b>53亿美元</b>，8月底新一轮下发<b>68.4亿美元</b>创2021年6月以来最高单批额度，国内<b>196家</b>机构累计获批额度达<b>1830.09亿美元</b>。<br>
          <b>后续看点：</b>2026年7月另一家外商独资公募路博迈基金也已上报QDII业务资格申请；贝莱德基金总经理郁蓓华表示，将整合全球投研平台资源与本土专业团队，为国内投资者提供更丰富的跨境投资标的与资产配置方案。<br>
          <b>对腾安启示：</b>外资公募补齐QDII牌照后跨境产品供给将扩容，货架端可提前规划“全球配置”专区；但必须区分QDII额度约束下的限购与溢价风险——此前多只跨境ETF溢价超8%，上架时应同步展示溢价率与额度状态提示。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.cnstock.com/commonDetail/792813" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·09-18</span></a>
        </div>
      </div>
    </div>
  </div>

'''
o_a = len(re.findall(r'<div\b', old_s1)); c_a = len(re.findall(r'</div>', old_s1))
o_b = len(re.findall(r'<div\b', new_s1)); c_b = len(re.findall(r'</div>', new_s1))
print('  S1 old %d/%d new %d/%d' % (o_a, c_a, o_b, c_b))
assert o_a == o_b and c_a == c_b, 'S1 div mismatch'
h = h[:j0] + new_s1 + h[j1:]
dr('step3 S1')

# ---------- Step 4: S6 行情 09-18 -> 09-21 收盘 ----------
S6_A = '<!-- ============ Section 6'
S6_B = '<!-- ============ Section 7'
k0 = h.index(S6_A); k1 = h.index(S6_B)
cs = h.index('            <div class="card p3">', k0)
old_s6 = h[cs:k1]
assert old_s6.count('<div class="card p3">') == 1
assert old_s6.rstrip().endswith('</div>  </div>'), repr(old_s6[-40:])

new_s6 = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-21）·沪指3949.91 +0.97%·沪深北三市成交2.05万亿缩量448亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-21</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-21收盘·医药领涨）</b><br>
              上证指数 <b>3949.91</b> <span style="color:#dc2626;">+0.97%</span><br>
              深证成指 <b>13730.02</b> <span style="color:#dc2626;">+0.65%</span><br>
              创业板指 <b>3399.59</b> <span style="color:#dc2626;">+0.80%</span><br>
              沪深300 <b>4539.57</b> <span style="color:#dc2626;">+0.71%</span><br>
              科创50 <b>1657.48</b> <span style="color:#dc2626;">+0.29%</span><br>
              北证50 <b>1058.18</b> <span style="color:#dc2626;">+1.33%</span><br>
              沪深北三市成交 <b>2.05万亿</b>·较上日缩量448亿<br>
              4536只上涨·105只涨停；936只下跌·2只跌停
            </div>
            <div>
              <b>港股与美股（09-21收盘）</b><br>
              恒生指数 <b>25042.71</b> <span style="color:#dc2626;">+1.18%</span><br>
              恒生科技 <b>4423.29</b> <span style="color:#dc2626;">+0.40%</span><br>
              国企指数 <b>8339.63</b> <span style="color:#dc2626;">+1.39%</span><br>
              道琼斯 <b>52048.83</b> <span style="color:#dc2626;">+0.71%</span><br>
              纳斯达克 <b>27122.09</b> <span style="color:#dc2626;">+2.26%</span><br>
              标普500 <b>7764.70</b> <span style="color:#dc2626;">+1.49%</span><br>
              布伦特原油100.30美元 <span style="color:#52c41a;">-3.40%</span>·现货黄金4351.99美元 <span style="color:#dc2626;">+0.19%</span>·美债10年期回落至4.948%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>医药领涨、量能回落——医疗服务板块涨逾<b>5%</b>，化学制药、生物制品均涨超4%，医疗器械涨逾3%；房地产、零售、旅游及酒店同步活跃，绿地控股、我爱我家、金融街、华发股份涨停；大金融午后发力，南华期货、华金资本直线涨停；<b>贵金属板块下跌</b>，为当日少数回调方向。全市场4536只个股上涨、105只涨停。成交端沪深北三市2.05万亿元，较上一交易日<b>减少448亿元</b>，指数上涨但量能回落。9月16日—21日上证指数累计上涨<b>2.22%</b>，深证成指、创业板指分别累计上涨3.33%、4.67%。海外方面，美股9月21日强势反弹，<b>纳斯达克涨2.26%创收盘新高</b>，标普500涨1.49%、道指涨0.71%；标普十一大板块七涨四跌，通信服务涨3.86%、科技涨2.46%领涨，能源跌2.57%领跌；费城半导体指数涨<b>5.29%</b>，ARM涨17.16%、英特尔涨12.14%、超威半导体涨9.95%、脸书涨11.43%。伊朗总统将出席联大、美方不排除会面，布伦特原油跌至100.30美元、单日跌3.40%，美债10年期回落至4.948%。中信建投策略分析师夏凡捷认为，随着油价与长端美债利率回落，外部宏观压力缓释，市场主线重回业绩景气。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：2026-09-21收盘</span>
          <span class="source-tag">数据来源：上海证券报/中国证券网、中国证券报、中国经济网、新华社、中新经纬（09-21—09-22）</span>
        </div>
      </div>  </div>
'''
o_a = len(re.findall(r'<div\b', old_s6)); c_a = len(re.findall(r'</div>', old_s6))
o_b = len(re.findall(r'<div\b', new_s6)); c_b = len(re.findall(r'</div>', new_s6))
print('  S6 old %d/%d new %d/%d' % (o_a, c_a, o_b, c_b))
assert o_a == o_b and c_a == c_b, 'S6 div mismatch'
h = h[:cs] + new_s6 + h[k1:]
dr('step4 S6')

# ---------- Step 5: S7 时间线重写 12 条 ----------
S7_A = '<!-- ============ Section 7'
m0 = h.index(S7_A)
fs = h.index('      <div class="timeline-item">', m0)
TAIL = '    </div>\n\n  </div>\n\n</div>'
te = h.index(TAIL, fs)
old_s7 = h[fs:te]
print('  old S7 items=%d' % len(re.findall(r'class="timeline-item"', old_s7)))
assert len(re.findall(r'class="timeline-item"', old_s7)) == 12

IT = [
    ('2026-09-22', '鹏安安瑞63个月债基开售'),
    ('2026-09-22', '红土创新瑞泽提前结募'),
    ('2026-09-22', '中邮卓享混合延长募集期'),
    ('2026-09-21', '上银基金姚秦出任总经理'),
    ('2026-09-21', '本周16只新发基金启动'),
    ('2026-09-21', '113家公募上周调研406次'),
    ('2026-09-20', '刘彦春卸任景顺长城副总'),
    ('2026-09-20', '3只REIT获证监会注册'),
    ('2026-09-20', '年内公募打新获配338亿'),
    ('2026-09-18', '贝莱德基金获批QDII资格'),
    ('2026-09-18', '被动指数债基首破2万亿'),
    ('2026-09-14', '首批15只摊余成本债基获批'),
]
for d, t in IT:
    assert len(t) <= 25, 'title too long: %s (%d)' % (t, len(t))
    assert d[5:] >= CUT, 'S7 out of window: %s' % d

new_s7 = '\n'.join(
    '      <div class="timeline-item">\n'
    '        <div class="timeline-dot blue"></div>\n'
    '        <div class="timeline-date">%s</div>\n'
    '        <div class="timeline-title">%s</div>\n'
    '      </div>' % (d, t) for d, t in IT) + '\n'
o_a = len(re.findall(r'<div\b', old_s7)); c_a = len(re.findall(r'</div>', old_s7))
o_b = len(re.findall(r'<div\b', new_s7)); c_b = len(re.findall(r'</div>', new_s7))
print('  S7 old %d/%d new %d/%d' % (o_a, c_a, o_b, c_b))
assert o_a == o_b and c_a == c_b, 'S7 div mismatch'
h = h[:fs] + new_s7 + h[te:]
dr('step5 S7')

# ---------- Phase 2: 全局校验 ----------
o1, c1 = len(re.findall(r'<div\b', h)), len(re.findall(r'</div>', h))
print('FINAL open=%d close=%d (base %d/%d) drift_o=%+d drift_c=%+d' % (o1, c1, o0, c0, o1 - o0, c1 - c0))
assert o1 == c1, 'div unbalanced'
assert o1 == o0 and c1 == c0, 'div drift != 0'

assert h.count('\ufffd') == 0, 'U+FFFD found'
assert h.count('</div>>') == 0, 'stray </div>>'
assert 'Section 8' not in h, 'S8 exists!'
assert '<!-- daily-update: 2026-09-22 -->' in h
assert BADGE_NEW in h

# S8 永久废弃
assert '待办跟踪' not in h and '腾安行动清单' not in h

# S0 六项
s0 = h[h.index('<!-- ============ Section 0'):h.index('<!-- ============ Section 1')]
assert s0.count('card p') == 4
assert '<span class="section-title">今日焦点</span>' in s0
assert '9月22日 · 4条今日要闻' in s0
assert s0.count('date-tag') == 4
assert len(re.findall(r'date-tag">(\d{2})-(\d{2})<', s0)) == 4
assert s0.count('action-box') == 0, 'no P0 today -> action-box must be 0'
assert s0.count('target="_blank"') == 4, 'S0 links=%d' % s0.count('target="_blank"')

# 全 section date-tag 不越界
for m in re.finditer(r'<!-- =+ Section (\d)', h):
    pass
marks = [(m.group(1), m.start()) for m in re.finditer(r'<!-- =+ Section (\d)', h)]
marks.append(('END', len(h)))
for i in range(len(marks) - 1):
    nm, s = marks[i]; e = marks[i + 1][1]
    seg = h[s:e]
    for d in re.findall(r'date-tag">(\d{2})-(\d{2})<', seg):
        assert ('-'.join(d)) >= CUT, 'S%s out of window: %s' % (nm, '-'.join(d))
    for d in re.findall(r'timeline-date">(\d{4})-(\d{2})-(\d{2})<', seg):
        assert d[1] + '-' + d[2] >= CUT, 'S%s timeline out: %s' % (nm, d)

# S7 条数与降序
s7 = h[h.index('<!-- ============ Section 7'):]
tl = re.findall(r'timeline-date">([^<]+)<', s7)
assert len(tl) == 12, 'S7 count=%d' % len(tl)
assert tl == sorted(tl, reverse=True), 'S7 not desc'
assert s7.count('timeline-desc') == 0

# 黑名单域
BL = ['stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com',
      'toutiao.com', 'so.html5.qq.com', '163.com/dy', 'cqcb.com', 'weibo.com',
      'k.sina.com.cn', 'jrj.com.cn']
for b in BL:
    assert b not in h, 'blacklist hit: %s' % b

open(P, 'w', encoding='utf-8').write(h)
print('WRITE OK  len %d -> %d' % (len(orig), len(h)))
