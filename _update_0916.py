# -*- coding: utf-8 -*-
"""
_update_0916.py — 基金看板 2026-09-16 日更
铁律：Phase1 全套断言通过才写文件；尾部闭合硬编码为常量；锚点 repr 已实测。
"""
import io
import re
import sys
from datetime import date, timedelta

SRC = 'index.html'
TODAY = date.today()
UPPER = TODAY.strftime('%Y.%m.%d')
LOWER = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
BADGE_NEW = '📅 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)
MARKER_NEW = '<!-- daily-update: %s -->' % TODAY.strftime('%Y-%m-%d')

FP_NEW = ('首批15只摊余成本法债基获批|科技主题基金延长募集45天'
          '|首批创业板算力ETF相继成立|投顾组合加码医药黄金')

src = io.open(SRC, encoding='utf-8').read()
orig = src
O_OPEN = src.count('<div')
O_CLOSE = src.count('</div>')

# ============================================================
# 1. marker（闸0）—— 已在会话开头改过，这里做幂等兜底
# ============================================================
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->', MARKER_NEW, src, count=1)

# ============================================================
# 2. header 数据区间 badge（动态计算，不依赖旧值）
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
# 4. Stats Bar：沪指卡 09-14 -> 09-15 收盘
# ============================================================
STATS_OLD = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3885.33</div>\n'
    '      <div class="stat-label">沪指9-14收盘·跌0.07%·全市场成交1.63万亿·较上日缩量3427亿</div>\n'
    '      <div class="stat-change down">▼ 创业板-1.10%·科创50-1.62%·超3100股上涨</div>\n'
    '    </div>'
)
STATS_NEW = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3864.28</div>\n'
    '      <div class="stat-label">沪指9-15收盘·跌0.54%·全市场成交1.63万亿·追平年内最低</div>\n'
    '      <div class="stat-change down">▼ 创业板-1.15%·科创50+1.55%·超4300股下跌</div>\n'
    '    </div>'
)
sb = src.find('<div class="stats-bar">')
sb_end = src.find('\n  </div>', sb)
assert sb > 0 and sb_end > sb, 'stats-bar 段定位失败'
assert src.count(STATS_OLD) == 1, 'Stats Bar 沪指卡锚点不唯一（可能误命中 S6）'
seg = src[sb:sb_end]
assert '3885.33' in seg and '3864.28' not in seg
src = src.replace(STATS_OLD, STATS_NEW, 1)

# ============================================================
# 5. S0 今日焦点：整块替换 4 张卡（09-16，无 P0 -> 无 action-box）
# ============================================================
S0_CARDS = u'''      <!-- S0 Card 1 (09-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批15只摊余成本法债基获批·63个月封闭·单只上限80亿·两批28家中小公募入局</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-16</span>
          </div>
        </div>
        <div class="card-body">
          华夏时报9月16日报道（记者张玫）：9月14日晚间，重新“开闸”后首批上报的摊余成本法债券基金正式获批，距8月14日上报仅一个月。首批获批产品来自百嘉基金、贝莱德基金、路博迈基金、安联基金、联博基金、红土创新基金、尚正基金、朱雀基金、国融基金、华西基金、易米基金、兴合基金、兴华基金、鹏安基金、财信基金等<b>15家基金管理人</b>，产品统一为<b>63个月封闭式债券基金</b>，单只募集规模上限不超过<b>80亿元</b>，其中贝莱德、路博迈、安联、联博为外资公募。9月11日，汇泉基金、博远基金、东方阿尔法基金、泉果基金、益民基金、泰信基金、汇百川基金、瑞达基金、中海基金、博道基金、恒越基金、东财基金、苏新基金等<b>13家</b>第二批产品申报材料获接收，两批合计<b>28家</b>管理人参与，全部为中小型公募。<br>
          <b>规模对比：</b>据Wind数据，截至2026年二季度末，第二批13家平均公募管理规模约<b>192亿元</b>（东财基金、博道基金均超570亿元，泰信基金接近477亿元），首批15家平均规模约<b>74亿元</b>、12家不足100亿元。<br>
          <b>政策背景：</b>摊余成本法债基2019—2020年曾集中发行，监管层2021年完全暂停审批注册，此番为时隔五年重启；转折点为2026年6月证监会主席吴清在陆家嘴论坛提出“推出支持中小基金公司规范健康发展的一揽子措施”。按通常0.15%管理费率测算，单只募满80亿元每年约贡献<b>1200万元</b>管理费、五年累计约<b>6000万元</b>。<br>
          <b>渠道格局：</b>据媒体公开报道，第二批13家公募对应托管行分别为兴业银行（6家）、浦发银行（4家）以及中信银行、招商银行、江苏银行；业内认为这类产品是打开银行自营、理财子等“金主”准入的敲门砖。<br>
          <b>对腾安启示：</b>此类产品目标客群为银行自营与理财子资金，销售资源高度集中于托管行渠道；腾安需评估63个月封闭期、低波动品种与自身客群的适配度，并在适当性环节强化封闭期流动性提示。
        </div>
        <div class="card-footer">
          <a href="https://cj.sina.cn/articles/view/1838672663/6d97eb1702001q36i" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">华夏时报·新浪财经·09-16</span></a>
          <a href="https://www.cs.com.cn/tzjj/etf/2026/09/15/detail_2026091510039234.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-15</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 2 (09-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 科技主题基金遇冷·延长募集最长45天·下半年89只新发基金延期</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-16</span>
          </div>
        </div>
        <div class="card-body">
          国际金融报9月16日报道：9月以来A股科技板块高位震荡回调，市场资金对高波动的科技赛道趋于谨慎，这一情绪传导至新基金发行端——多只聚焦算力、人工智能、卫星产业等热门主题的基金陆续宣布延长募集期，<b>募集延期最长达45天</b>。<br>
          <b>延期清单：</b>9月15日兴业基金公告，旗下兴业上证科创板人工智能ETF原定募集截止日为9月15日，现<b>延长至10月30日</b>（延长45天），托管人为中国农业银行；同日招商基金宣布旗下招商中证卫星产业ETF联接基金募集截止日由9月17日延长至9月24日。9月11日，银华基金旗下港股通信息技术综合ETF募集截止日由9月11日延长至9月18日，富国基金旗下创业板算力基础设施ETF由9月11日延长至9月16日。<br>
          <b>总量：</b>Wind数据显示，截至9月15日，下半年以来全市场已有<b>89只</b>新发基金延长募集期，部分产品更是多次延期；从产品类型看，延期基金以ETF及联接基金等指数型产品为主，其次为偏债混合基金与FOF。<br>
          <b>机构解读：</b>排排网财富研究员张鹏远认为，延长募集主要有两方面原因——一是板块高位震荡回调、个人投资者风险偏好回落，前期科技赛道获利盘兑现、短期赚钱效应减弱；二是场外资金不再简单追逐短期热点，对高波动科技赛道认购趋于谨慎、观望情绪升温。他强调这代表资金热度出现明显分化，并非全面退潮。<br>
          <b>对腾安启示：</b>热门主题基金延期意味着“募集成立”不等于“资金认可”，产品页与推荐位应同步标注募集进度与延期记录；对多次延期的主题ETF，需在推荐逻辑中补充估值与波动提示，避免以“新发热门”标签引导认购。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-09-16/doc-iniryefn3277104.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">国际金融报·新浪财经·09-16</span></a>
          <a href="https://paper.cnstock.com/html/2026-09/15/content_2269022.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·兴业基金公告·09-15</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 3 (09-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批创业板算力ETF相继成立·天弘华夏易方达3家落地·另有7家在发或筹备</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-16</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月16日报道（记者叶峰）：近日，天弘基金、华夏基金、易方达基金3家公募机构旗下<b>创业板算力基础设施ETF相继成立</b>；另有国泰基金、大成基金、广发基金等<b>7家</b>机构旗下相关产品正在发行或筹备成立中。<br>
          <b>产品定位：</b>目前市场上其他AI相关ETF投资方向各有侧重，创业板算力ETF跟踪<b>创业板算力基础设施指数</b>，该指数精选50只创业板标的，覆盖计算、网络、存储、运维等硬件环节。<br>
          <b>机构观点：</b>富国基金武磊近日表示，站在当前位置这轮调整可能逐步进入尾声，基本面与产业趋势未出现明显变化，海外流动性环境的边际影响已充分演绎；近期红利价值风格已有较明显表现，部分纯防御板块交易拥挤度有所上升，接下来或可关注成长风格的反弹机会。<br>
          <b>对腾安启示：</b>算力主题ETF集中成立与在发意味着同质化供给快速增加，产品页需突出跟踪指数成分差异（创业板算力50只标的 vs 其他AI指数）与管理费率，避免客户仅凭名称“算力”简单类比申购。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260916A03NEP00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 4 (09-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 基金投顾组合“精细化”腾挪·科技内部调结构·加码医药与黄金</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-16</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月16日报道（记者魏昭宇）：近期汇添富基金、中欧基金、万家基金等多家机构投顾组合相继披露最新调仓动向，在A股震荡分化背景下布局策略呈现一定分歧。尽管科技板块整体仍是关注焦点，投顾机构在科技内部赛道进行了精细化“腾挪”，同时加大对医药、黄金等行业的配置力度，试图在波动中捕捉确定性机会。<br>
          <b>科技内部腾挪：</b>万家非凡新质驱动9月初对AI、半导体方向进行部分品种替代、增加国产算力权重，加仓华安上证科创板芯片ETF发起式联接C、华富数字经济混合C、诺安创新驱动混合C；中欧优势行业全明星8月底调仓新增长盛新兴成长混合C、嘉实上证科创芯片ETF发起联接C；汇添富全球配置三动力则在TMT内部降低高拥挤度方向配比，增加受益于“AI需求爆发+渗透率持续提升”双重驱动的下游应用板块。<br>
          <b>增配防御：</b>医药方面，万家非凡新质驱动加仓易方达大健康混合、华夏军工安全混合C，中欧优势行业全明星加仓交银医药创新股票A、工银医药健康股票A，中欧多元配置加仓全球医疗类QDII产品；黄金方面，汇添富全球配置三动力增加商品资产（华夏黄金ETF联接A），中欧多元配置加仓博时黄金ETF联接C。<br>
          <b>对腾安启示：</b>投顾调仓逻辑从“押赛道”转向“降拥挤度+增防御”，可作为投顾策略页与组合诊断的内容素材；对医药、黄金类基金的推荐位宜结合拥挤度指标择时推送，避免在板块热度高位集中曝光。
        </div>
        <div class="card-footer">
          <a href="https://m.cnfin.com/gs-lb//zixun/20260916/4470453_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-16</span></a>
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
CTX_OLD = '<span class="section-context">9月15日 · 4条今日要闻</span>'
CTX_NEW = '<span class="section-context">9月16日 · 4条今日要闻</span>'
assert src.count(CTX_OLD) == 1, 'S0 section-context 锚点不唯一'
src = src.replace(CTX_OLD, CTX_NEW, 1)

# ============================================================
# 6. S6 市场行情速览：09-14 -> 09-15 收盘
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
          <div class="card-title">📈 上一交易日收盘（2026-09-15）·沪指3864.28 -0.54%·全市场成交1.63万亿追平年内最低</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-15</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-15收盘·地量磨底）</b><br>
              上证指数 <b>3864.28</b> <span style="color:#52c41a;">-0.54%</span><br>
              深证成指 <b>13287.97</b> <span style="color:#52c41a;">-0.72%</span><br>
              创业板指 <b>3247.92</b> <span style="color:#52c41a;">-1.15%</span><br>
              沪深300 <b>4450.04</b> <span style="color:#52c41a;">-0.67%</span><br>
              科创50 <b>1551.96</b> <span style="color:#dc2626;">+1.55%</span><br>
              北证50 <b>1028.51</b> <span style="color:#dc2626;">+0.65%</span><br>
              全市场成交 <b>1.63万亿</b>·较上日缩量177亿·追平4月7日年内最低<br>
              1120只个股上涨·4376只下跌
            </div>
            <div>
              <b>港股与美股（09-15收盘）</b><br>
              恒生指数 <b>24667.24</b> <span style="color:#52c41a;">-1.00%</span><br>
              恒生科技 <b>4291.34</b> <span style="color:#52c41a;">-0.62%</span><br>
              国企指数 <b>8204.91</b> <span style="color:#52c41a;">-0.96%</span><br>
              道琼斯 <b>52093.11</b> <span style="color:#52c41a;">-0.63%</span><br>
              纳斯达克 <b>25981.57</b> <span style="color:#52c41a;">-0.78%</span><br>
              标普500 <b>7585.73</b> <span style="color:#52c41a;">-0.45%</span><br>
              布伦特原油108.80美元 <span style="color:#dc2626;">+2.09%</span>·伦敦金现4293.37美元 <span style="color:#dc2626;">+0.08%</span>·美债10年期收5.006%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>地量磨底、硬科技独强——指数普跌但科创50逆势涨1.55%领涨全场，工信部与发改委9月15日联合印发《电子信息制造业发展“十五五”规划》提出推动集成电路全链条攻关，半导体产品与半导体设备板块涨约3%、主力净流入超43亿元居首；消费服务与农业重挫，餐饮旅游多股跌停、粮食概念续跌，银行与红利方向同步走弱。海外方面，市场等待美联储9月16日议息结果，CME数据显示加息25个基点概率超90%，美国10年期国债收益率收于5.006%，为2007年7月以来首次收于5%关口上方，通胀担忧与利率上行共同压制风险资产估值。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-15收盘</span>
          <span class="source-tag">数据来源：新华财经/上海证券报/中国证券网（09-15—09-16）</span>
        </div>
      </div>'''
src = src[:S6_START] + S6_NEW + src[s6_end + S6_KEEP:]

# ============================================================
# 7. S7 时间线：重写 12 条（增 09-16×4，删 09-12×4）
# ============================================================
S7_ITEMS = [
    ('red', '2026-09-16', '首批15只摊余成本法债基获批'),
    ('blue', '2026-09-16', '科技主题基金延长募集45天'),
    ('blue', '2026-09-16', '首批创业板算力ETF相继成立'),
    ('blue', '2026-09-16', '投顾组合腾挪·加码医药黄金'),
    ('red', '2026-09-15', '中国结算发布公募登记数据交换指引'),
    ('blue', '2026-09-15', '主动权益首尾业绩差超210个百分点'),
    ('blue', '2026-09-15', 'ETF资金大进大出倒逼运作升级'),
    ('blue', '2026-09-15', '盈利投资者占比中位数91.79%'),
    ('red', '2026-09-14', '基金网络营销整改进入倒计时'),
    ('blue', '2026-09-14', '双创ETF资金分歧·科创50吸金'),
    ('red', '2026-09-13', '中基协撤销台州沃源管理人登记'),
    ('red', '2026-09-11', '金融强国“十五五”规划正式出台'),
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
# 预期漂移：移除 1 个 P0 action-box = -3
assert N_OPEN == O_OPEN - 3, 'div open 漂移异常：%d' % (N_OPEN - O_OPEN)
assert N_CLOSE == O_CLOSE - 3, 'div close 漂移异常：%d' % (N_CLOSE - O_CLOSE)
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
# 注意：re.findall 双分组返回元组，须用 .count(('09','16'))
assert re.findall(r'date-tag">(\d{2})-(\d{2})<', s0).count(('09', '16')) == 4, 'S0 09-16 date-tag 数 != 4'
assert '<span class="section-title">今日焦点</span>' in s0, 'S0 title 不是「今日焦点」'
assert '<span class="section-context">9月16日 · 4条今日要闻</span>' in s0, 'S0 context 错'
assert s0.count('target="_blank"') == 6, 'S0 源链接数 != 6（实际 %d）' % s0.count('target="_blank"')
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

# T-14：所有 date-tag >= 09-02
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
