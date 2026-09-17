# -*- coding: utf-8 -*-
"""
_update_0917.py — 基金看板 2026-09-17 日更
铁律：Phase1 全套断言通过才写文件；尾部闭合硬编码为常量；锚点 repr 已实测。
预期 div 漂移 = 0（S0 4->4 无 action-box、S6 同构、S7 12->12、Stats Bar 同构）
"""
import io
import re
from datetime import date, timedelta

SRC = 'index.html'
TODAY = date.today()
UPPER = TODAY.strftime('%Y.%m.%d')
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
BADGE_NEW = '📅 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)
MARKER_NEW = '<!-- daily-update: %s -->' % TODAY.strftime('%Y-%m-%d')

FP_NEW = '年内新发|公募逆势|次新基金|公募密集'

src = io.open(SRC, encoding='utf-8').read()
O_OPEN = src.count('<div')
O_CLOSE = src.count('</div>')

# ============================================================
# 1. marker（闸0）
# ============================================================
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', MARKER_NEW, src, count=1)

# ============================================================
# 2. header 数据区间 badge（动态计算）
# ============================================================
BADGE_RE = r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）'
assert len(re.findall(BADGE_RE, src)) == 1, 'badge 锚点不唯一'
src = re.sub(BADGE_RE, BADGE_NEW, src, count=1)

# ============================================================
# 3. content-fingerprint（闸6）
# ============================================================
FP_RE = r'(<meta name="content-fingerprint" content=")[^"]*(">)'
assert len(re.findall(FP_RE, src)) == 1, 'fingerprint 锚点不唯一'
src = re.sub(FP_RE, lambda m: m.group(1) + FP_NEW + m.group(2), src, count=1)

# ============================================================
# 4. Stats Bar：沪指卡 09-15 -> 09-16 收盘
# ============================================================
STATS_OLD = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3864.28</div>\n'
    '      <div class="stat-label">沪指9-15收盘·跌0.54%·全市场成交1.63万亿·逼近年内地量</div>\n'
    '      <div class="stat-change down">▼ 创业板-1.15%·科创50+1.55%·超4300股下跌</div>\n'
    '    </div>'
)
STATS_NEW = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3891.60</div>\n'
    '      <div class="stat-label">沪指9-16收盘·涨0.71%·全市场成交1.84万亿·放量2264亿</div>\n'
    '      <div class="stat-change up">▲ 创业板+1.96%·科创50+4.14%·超4100股上涨</div>\n'
    '    </div>'
)
sb = src.find('<div class="stats-bar">')
sb_end = src.find('\n  </div>', sb)
assert sb > 0 and sb_end > sb, 'stats-bar 段定位失败'
assert src.count(STATS_OLD) == 1, 'Stats Bar 沪指卡锚点不唯一（可能误命中 S6）'
seg = src[sb:sb_end]
assert '3864.28' in seg and '3891.60' not in seg
src = src.replace(STATS_OLD, STATS_NEW, 1)

# ============================================================
# 5. S0 今日焦点：整块替换 4 张卡（09-17，无 P0 -> 无 action-box）
# ============================================================
S0_CARDS = u'''      <!-- S0 Card 1 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 年内新发基金规模突破8000亿·1276只成立·权益类占半壁江山</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月17日报道（记者赵明超）：9月16日，<b>14只</b>基金发布基金合同生效公告、合计发行规模<b>50.3亿元</b>，至此今年以来新发基金规模突破8000亿元。Choice数据显示，截至9月16日，今年以来共成立<b>1276只</b>基金，合计发行规模<b>8006.5亿元</b>。<br>
          <b>结构拆解：</b>权益类基金占据半壁江山——共成立<b>863只</b>、合计发行规模<b>4187.21亿元</b>，逾百只发行规模在10亿元以上；以二级债基、FOF为代表的稳健类含权产品同步升温，年内成立<b>139只</b>FOF、合计<b>1424.15亿元</b>，成立<b>165只</b>二级债基、合计超<b>1300亿元</b>，普遍采取多资产配置策略。<br>
          <b>明星基金经理：</b>杨冬管理的广发研究智选混合发行规模<b>72.21亿元</b>，李文宾管理的永赢锐见成长混合、方建管理的银华智享混合均超<b>50亿元</b>。<br>
          <b>创新品种：</b>三季度以来首批18只主动ETF、10只创业板算力基础设施ETF、6只创业板金融科技主题ETF、10只中证新能源金属50ETF、8只中证沪深港智能驾驶主题ETF密集上报，首批10只科创债指数基金近日上报。<br>
          <b>对腾安启示：</b>新发盘子中权益类占52.3%、含权稳健类（FOF+二级债基）合计超2700亿元，是线上客群最容易承接的“低波动+稳收益”区间；建议在选品页把“固收+白盒”与多资产FOF单列一层，并在发行期同步露出规模与结募节奏，避免客户只按短期业绩排序决策。
        </div>
        <div class="card-footer">
          <a href="https://m.cnfin.com/yw-lb//zixun/20260917/4471017_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 2 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募逆势布局效果初显·从“追光”到“耕田”·冷门赛道回报领先超30个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报9月17日报道（记者王雪青）：Wind数据显示，截至9月15日，今年6月16日成立的汇添富中证畜牧养殖产业ETF联接A回报率约<b>9%</b>，仅晚一天成立的某科创人工智能ETF回报率为<b>-24%</b>，两者相差<b>33个百分点</b>；6月22日成立的广发国证粮食产业ETF联接A回报率超<b>8%</b>，而6月24日成立的某人工智能ETF回报率接近<b>-23%</b>，相差<b>31个百分点</b>。收益逆袭的背后，是部分公募在市场承压阶段提前落子。<br>
          <b>提前落子清单：</b>格上基金数据显示，今年前8个月畜牧养殖、食品、工程机械等相对冷门方向出现多家管理人集中布局——永赢、景顺长城、汇添富、广发、华泰柏瑞、易方达、南方等发行畜牧养殖或农牧渔主题ETF，发行份额在<b>2.02亿份至7.81亿份</b>之间；易方达、富国、前海开源、华夏等成立食品指数产品，发行份额在<b>2.27亿份至3.36亿份</b>之间。行业关注度较低时，发起式成为落地方式之一，其中鑫元国证石油天然气指数发起式基金成立时募集总份额约<b>1021.63万份</b>，管理人固有资金认购占比接近<b>98%</b>。<br>
          <b>持营端同步：</b>天弘基金数据显示，5月与6月科技强势、红利承压期间，天弘中证央企红利50指数持有人户数合计逆势增长<b>38%</b>，截至6月底达<b>11.3万户</b>。<br>
          <b>机构观点：</b>天相投顾基金评价中心认为，今年公募发行呈现“追逐热点降温、提前布局类产品增加”的结构性变化，但尚未全面转向——银行、券商渠道更关注持有体验与长期配置价值，流量型渠道仍较依赖热门主题。格上基金研究员毕梦姌提醒：“逆势发行的收益相对优势是真实存在的，但逆势发行并不保证赚钱”，判断冷门行业需同时观察行业长期需求、利空定价、竞争格局与订单、库存、毛利率等指标改善。<br>
          <b>对腾安启示：</b>流量型渠道依赖热门主题的惯性仍在，但红利/农业等低位方向的持有人户数已在逆势增长；建议把“冷门赛道”做成带周期与风险提示的主题页而非单品推荐，并在持营侧补上投后陪伴内容，降低客户在回撤期的赎回冲动。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/01/2026/09/17/detail_2026091710039758.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 3 (09-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 次新基金快速建仓·近1个月机构调研超4万次·9月逾20只提前结募</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月17日报道（记者赵明超）：从三季度以来成立的基金看，多只主动权益类基金净值已发生明显变化，表明这些基金已快速建仓。以长城资源精选混合为例，该产品成立于7月21日，截至9月14日成立以来收益超过<b>17%</b>；景顺长城成长先锋混合成立于7月24日、募集规模<b>42.63亿元</b>，仍处封闭期，从9月11日披露净值看周度上涨<b>3.07%</b>。也有尚未“满月”即出现明显净值波动者：安联中国成长优选混合成立于8月18日，截至9月11日成立以来亏损超<b>14%</b>；中泰医药精选混合成立于9月4日，截至9月11日亏损约<b>2%</b>。<br>
          <b>发行节奏：</b>Choice数据显示，截至9月16日，9月以来逾<b>20只</b>基金宣布提前结束募集。部分基金从获批到发行再到成立用时仅两周——8月28日首批创业板算力基础设施ETF获批，9月4日6只即启动发行，截至9月11日天弘、华夏、易方达旗下产品均已宣告成立。<br>
          <b>调研热度：</b>Choice数据显示，截至9月15日，近1个月机构调研次数超过<b>4万次</b>，处于历史较高水平，半导体、电子设备制造等行业热度居前。华南一位基金经理表示，10月中旬起上市公司三季报将密集披露，当前业绩真空期是调研和调仓的好时机。<br>
          <b>对腾安启示：</b>“发行提速+快速建仓”意味着次新基金的净值波动会在成立后很快显性化；对成立未满月即出现两位数亏损的产品，应提前在详情页标注建仓进度与波动来源，避免客户把短期净值波动误读为管理能力问题。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/791396" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·09-17</span></a>
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202609/t20260917_3217712.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·09-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 4 (09-17 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募密集调整QDII申购限额·129只限购·纳指科技ETF溢价超20%</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-17</span>
          </div>
        </div>
        <div class="card-body">
          证券日报9月17日报道：日前国家外汇管理局发布最新QDII投资额度审批情况表，证券基金类机构新增额度<b>37.2亿美元</b>、累计获批额度首次突破千亿美元。在此背景下，公募机构密集调整旗下跨境产品申购限额。此前严格限购的QDII基金开始提高上限——汇添富纳斯达克100ETF（159513）发起式联接（QDII）人民币份额单日大额申购限额由<b>10元</b>提高至<b>1000元</b>、美元份额由2美元提高至150美元；南方亚洲美元收益债券（QDII）部分人民币份额单日大额申购限额由200万元提高至<b>3000万元</b>。<br>
          <b>额度仍紧：</b>Wind数据显示，截至9月16日，339只QDII基金（仅统计初始基金）中有<b>129只</b>设置单日大额申购限额，其中<b>9只</b>单日申购限额不超过10元。<br>
          <b>溢价风险：</b>部分场内跨境产品二级市场价格明显高于基金参考净值，截至9月16日景顺长城纳斯达克科技ETF（QDII）净值溢价率超过<b>20%</b>，另有多只跟踪纳斯达克100指数的ETF溢价率超过<b>10%</b>。晨星（中国）基金研究中心总监孙珩提示，跨境ETF二级价格显著高于净值意味着投资者除承担底层海外资产波动与汇率风险外，还额外承担溢价回落风险。<br>
          <b>对腾安启示：</b>QDII额度虽已扩容但热门标的供给仍紧，产品页应把“单日申购限额”与“场内溢价率”做成前置可见字段；对溢价率超10%的跨境ETF必须弹窗提示溢价回落风险，避免客户把二级市场价格当作净值买入。
        </div>
        <div class="card-footer">
          <a href="https://fund.10jqka.com.cn/20260917/c679985368.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·同花顺基金·09-17</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>'''

s0_start = src.find('      <!-- S0 Card 1')
S0_TAIL = '\n\n\n    </div>\n  </div>\n'
s0_end = src.find(S0_TAIL, s0_start)
assert s0_start > 0 and s0_end > s0_start, 'S0 段定位失败'
assert src.count('      <!-- S0 Card 1') == 1, 'S0 Card1 锚点不唯一'
src = src[:s0_start] + S0_CARDS + src[s0_end:]

# S0 section-context 单独改（09-09 教训：整块替换不带 header）
CTX_OLD = '<span class="section-context">9月16日 · 4条今日要闻</span>'
CTX_NEW = '<span class="section-context">9月17日 · 4条今日要闻</span>'
assert src.count(CTX_OLD) == 1, 'S0 section-context 锚点不唯一'
src = src.replace(CTX_OLD, CTX_NEW, 1)

# ============================================================
# 6. S6 市场行情速览：09-15 -> 09-16 收盘
# ============================================================
S6_START = src.find('<div class="card p3">', src.find('Section 6'))
# 注意：S6 卡片闭合与 section 闭合挤在同一行（'      </div>  </div>'），
# 切割点必须落在卡片闭合之后，否则会把 '      </div>' 重复拼接一次。
S6_TAIL = '      </div>  </div>\n'
s6_end = src.find(S6_TAIL, S6_START)
assert S6_START > 0 and s6_end > S6_START, 'S6 段定位失败'
S6_KEEP = len('      </div>')  # 卡片自身闭合由 S6_NEW 提供，只保留后面的 section 闭合

S6_NEW = u'''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-16）·沪指3891.60 +0.71%·全市场成交1.84万亿放量2264亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-16</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-16收盘·放量反弹）</b><br>
              上证指数 <b>3891.60</b> <span style="color:#dc2626;">+0.71%</span><br>
              深证成指 <b>13454.74</b> <span style="color:#dc2626;">+1.26%</span><br>
              创业板指 <b>3311.47</b> <span style="color:#dc2626;">+1.96%</span><br>
              沪深300 <b>4480.27</b> <span style="color:#dc2626;">+0.68%</span><br>
              科创50 <b>1616.19</b> <span style="color:#dc2626;">+4.14%</span><br>
              北证50 <b>1040.29</b> <span style="color:#dc2626;">+1.15%</span><br>
              全市场成交 <b>1.84万亿</b>·较上日放量2264亿<br>
              4122只个股上涨·1189只下跌
            </div>
            <div>
              <b>港股与美股（09-16收盘）</b><br>
              恒生指数 <b>24713.78</b> <span style="color:#dc2626;">+0.19%</span><br>
              恒生科技 <b>4325.45</b> <span style="color:#dc2626;">+0.79%</span><br>
              国企指数 <b>8206.37</b> <span style="color:#dc2626;">+0.02%</span><br>
              道琼斯 <b>51461.90</b> <span style="color:#52c41a;">-1.21%</span><br>
              纳斯达克 <b>25978.42</b> <span style="color:#52c41a;">-0.01%</span><br>
              标普500 <b>7551.81</b> <span style="color:#52c41a;">-0.45%</span><br>
              布伦特原油105.80美元 <span style="color:#52c41a;">-2.69%</span>·现货黄金4275.49美元 <span style="color:#dc2626;">+0.26%</span>·美债10年期收5.021%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>放量反弹、硬科技独强——科创50涨4.14%领涨全场，半导体（+4.79%）、其他电子（+4.01%）、电子化学品（+3.71%）涨幅居前，算力硬件、光纤、CPO、液冷服务器方向多股涨停；汽车整车（-1.69%）、保险（-0.80%）、银行（-0.76%）跌幅居前，红利蓝筹与周期方向同步走弱。海外方面，美联储9月16日宣布加息25个基点至3.75%—4.00%区间、符合市场主流预期，点阵图显示16位官员预计2026年应再加息；美国10年期国债收益率收于5.021%继续站在5%关口上方，通胀担忧与利率上行共同压制风险资产估值，美股三大指数集体收跌。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-16收盘</span>
          <span class="source-tag">数据来源：央广网/中国经济网/上海证券报（09-16—09-17）</span>
        </div>
      </div>'''
src = src[:S6_START] + S6_NEW + src[s6_end + S6_KEEP:]

# ============================================================
# 7. S7 时间线：重写 12 条（增 09-17×4，删 09-13×1/09-14×1/09-15×2）
# ============================================================
S7_ITEMS = [
    ('red', '2026-09-17', '年内新发基金规模破8000亿'),
    ('blue', '2026-09-17', '公募逆势布局冷门赛道'),
    ('blue', '2026-09-17', '次新基金快速建仓·机构调研'),
    ('blue', '2026-09-17', '公募密集调整QDII申购限额'),
    ('red', '2026-09-16', '首批15只摊余成本法债基获批'),
    ('blue', '2026-09-16', '科技主题基金延长募集45天'),
    ('blue', '2026-09-16', '首批创业板算力ETF相继成立'),
    ('blue', '2026-09-16', '投顾组合腾挪·加码医药黄金'),
    ('red', '2026-09-15', '中国结算发布公募登记数据交换指引'),
    ('blue', '2026-09-15', '主动权益首尾业绩差超210个百分点'),
    ('red', '2026-09-14', '基金网络营销整改进入倒计时'),
    ('red', '2026-09-11', '金融强国十五五规划正式出台'),
]
s7_start = src.find('      <div class="timeline-item">')
S7_TAIL = '\n\n    </div>\n\n  </div>\n\n</div>'
s7_end = src.find(S7_TAIL, s7_start)
assert s7_start > 0 and s7_end > s7_start, 'S7 段定位失败'
assert src.count('      <div class="timeline-item">') == 12, 'S7 起点锚点数 != 12'

blocks = []
for color, d, t in S7_ITEMS:
    assert len(t) <= 25, 'S7 标题超25字：%s (%d)' % (t, len(t))
    blocks.append(
        '      <div class="timeline-item">\n'
        '        <div class="timeline-dot %s"></div>\n'
        '        <div class="timeline-date">%s</div>\n'
        '        <div class="timeline-title">%s</div>\n'
        '      </div>' % (color, d, t)
    )
src = src[:s7_start] + '\n'.join(blocks) + src[s7_end:]

# ============================================================
# Phase1 断言（不通过不写文件）
# ============================================================
N_OPEN = src.count('<div')
N_CLOSE = src.count('</div>')
print('div: %d/%d -> %d/%d  drift=%d' % (O_OPEN, O_CLOSE, N_OPEN, N_CLOSE, N_OPEN - O_OPEN))
# 预期漂移 0：S0 4->4 同构（无 action-box）、S6 同构、S7 12->12、Stats Bar 同构
assert N_OPEN == O_OPEN, 'div open 漂移异常：%d' % (N_OPEN - O_OPEN)
assert N_CLOSE == O_CLOSE, 'div close 漂移异常：%d' % (N_CLOSE - O_CLOSE)
assert N_OPEN == N_CLOSE, 'div 不平衡'

# 3b 游离字符
assert src.count('</div>>') == 0, '存在游离 </div>>'

# S8 永久废弃
assert 'S8' not in src and '待办跟踪' not in src and '腾安行动清单' not in src, 'S8 残留'

# marker / badge / fingerprint
assert MARKER_NEW in src, 'marker 未更新'
assert BADGE_NEW in src, 'badge 未更新'
assert FP_NEW in src, 'fingerprint 未更新'

# S0 六项
s0 = src[src.find('Section 0'):src.find('Section 1')]
assert s0.count('<div class="card p') == 4, 'S0 卡数 != 4'
assert s0.count('class="action-box"') == 0, 'S0 不应有 action-box（本日无 P0）'
assert s0.count('date-tag') == 4, 'S0 date-tag 数 != 4'
# 注意：re.findall 双分组返回元组，须用 .count(('09','17'))
assert re.findall(r'date-tag">(\d{2})-(\d{2})<', s0).count(('09', '17')) == 4, 'S0 09-17 date-tag 数 != 4'
assert '<span class="section-title">今日焦点</span>' in s0, 'S0 title 不是「今日焦点」'
assert '<span class="section-context">9月17日 · 4条今日要闻</span>' in s0, 'S0 context 错'
assert s0.count('target="_blank"') == 5, 'S0 源链接数 != 5（实际 %d）' % s0.count('target="_blank"')
# card-meta 结构（先排除 style 段）
body = re.sub(r'<style.*?</style>', '', src, flags=re.S)
for m in re.finditer(r'<div class="card-meta">(.*?)</div>', body, re.S):
    inner = m.group(1)
    assert 'priority-tag' in inner and 'date-tag' in inner, 'card-meta 结构异常：%s' % inner[:60]

# S7 条数与降序
s7 = src[src.find('Section 7'):]
assert s7.count('      <div class="timeline-item">') == 12, 'S7 条数 != 12'
assert s7.count('timeline-desc') == 0, 'S7 存在 timeline-desc'
dates = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', s7)
assert dates == sorted(dates, reverse=True), 'S7 日期非降序'
for t in re.findall(r'<div class="timeline-title">(.*?)</div>', s7):
    assert len(t) <= 25, 'S7 标题超25字：%s' % t

# S1 / S2 数量
s1 = src[src.find('Section 1'):src.find('Section 2')]
s2 = src[src.find('Section 2'):src.find('Section 3')]
assert s1.count('<div class="card p') == 6, 'S1 卡数 != 6'
assert s2.count('<div class="card p') == 4, 'S2 卡数 != 4'

# T-14：所有 date-tag >= 09-03
cutoff = (TODAY - timedelta(days=14)).strftime('%m-%d')
for mm, dd in re.findall(r'date-tag">(\d{2})-(\d{2})<', src):
    assert '%s-%s' % (mm, dd) >= cutoff, 'date-tag 越界：%s-%s < %s' % (mm, dd, cutoff)

# U+FFFD 零
assert src.count('\ufffd') == 0, '存在 U+FFFD 乱码'

# 黑名单零（全文件）
for bad in ('so.html5.qq.com', 'toutiao', 'stcn.com', 'cls.cn', '21jingji.com',
            'yicai.com', 'guba.eastmoney.com', '163.com/dy', 'dy.163.com',
            'jrj.com.cn', 'sohu.com', 'k.sina.com.cn'):
    assert bad not in src, '黑名单命中：%s' % bad

# 新增段 D 级关键词扫描
assert '企鹅号' not in src and '网易号' not in src and '搜狐号' not in src
assert '财经早报' not in src and '基金日报' not in src

print('Phase1 断言全部通过，写入文件…')
io.open(SRC, 'w', encoding='utf-8').write(src)
print('DONE')
