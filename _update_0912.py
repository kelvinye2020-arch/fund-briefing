# -*- coding: utf-8 -*-
"""2026-09-12 基金看板日更脚本（Phase1 全断言 → 才写文件）"""
import re
import io
import os
from datetime import date, timedelta

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
src = io.open(PATH, encoding='utf-8').read()
orig = src
today = date.today()
UPPER = today.strftime('%Y.%m.%d')
LOWER = (today - timedelta(days=14)).strftime('%Y.%m.%d')
BADGE_NEW = '📅 数据区间：%s — %s（每日更新）' % (LOWER, UPPER)

print('=== 日期口径 ===')
print('today=%s lower=%s upper=%s' % (today, LOWER, UPPER))

# ---------- div 计数工具 ----------
def divs(t):
    return t.count('<div'), t.count('</div>')

def card_block_at(s, idx_open):
    """从 <div ...> 起点 idx_open 做嵌套深度扫描，返回 (start, end)"""
    assert s[idx_open:idx_open + 4] == '<div', s[idx_open:idx_open + 20]
    depth = 0
    pos = idx_open
    while True:
        nxt_open = s.find('<div', pos)
        nxt_close = s.find('</div>', pos)
        if nxt_close == -1:
            raise AssertionError('未找到闭合')
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 4
        else:
            depth -= 1
            pos = nxt_close + 6
            if depth == 0:
                return idx_open, pos

# =========================================================
# STEP 1: header 数据区间 badge（正则动态覆盖）
# =========================================================
BADGE_RE = r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）'
assert len(re.findall(BADGE_RE, src)) == 1, 'badge 锚点不唯一'
src = re.sub(BADGE_RE, BADGE_NEW, src)

# =========================================================
# STEP 2: Stats Bar 沪指卡
# =========================================================
STATS_OLD = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3934.40</div>\n'
    '      <div class="stat-label">沪指9-10收盘·跌0.43%·全市场成交1.66万亿·创年内次低</div>\n'
    '      <div class="stat-change down">▼ 银行电力逆势走强·超4500只个股下跌</div>\n'
    '    </div>\n'
)
STATS_NEW = (
    '    <div class="stat-card">\n'
    '      <div class="stat-number">3888.11</div>\n'
    '      <div class="stat-label">沪指9-11收盘·跌1.18%·全市场成交1.99万亿·较上日放量3248亿</div>\n'
    '      <div class="stat-change down">▼ 有色化工地产领跌·仅643只个股上涨</div>\n'
    '    </div>\n'
)
assert src.count(STATS_OLD) == 1, 'Stats 沪指卡锚点不唯一'
src = src.replace(STATS_OLD, STATS_NEW)

# =========================================================
# STEP 3: S0 section-context
# =========================================================
CTX_OLD = '<span class="section-context">9月11日 · 4条今日要闻</span>'
CTX_NEW = '<span class="section-context">9月12日 · 4条今日要闻</span>'
assert src.count(CTX_OLD) == 1, 'S0 context 锚点不唯一'
src = src.replace(CTX_OLD, CTX_NEW)

# =========================================================
# STEP 4: S0 四张卡整块替换
# =========================================================
S0_START = src.index('      <!-- S0 Card 1 (09-11 P0) -->')
S0_END = src.index('    </div>\n  </div>\n\n<!-- ============ Section 1')
S0_OLD = src[S0_START:S0_END]
s0_old_div = divs(S0_OLD)

C1 = '''      <!-- S0 Card 1 (09-12 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募逆周期布局提速·本周50只新基开启募集·权益占64%·发起式基金占36%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-12</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月12日（记者陈玥）：尽管8月以来A股持续震荡筑底，新基金的获批与发行却在悄然加速。公募排排网数据显示，按认购起始日统计，<b>9月7日至13日这一周全市场共50只基金开启募集</b>，其中权益类32只、占比<b>64%</b>，稳居发行主力；本周开启募集的25只被动指数型基金中，金融科技、粮食产业、港股通及科技方向均有不少于3只产品，其中<b>发起式基金9只、占比36%</b>。<br><b>发起式逻辑：</b>融智投资FOF基金经理李春瑜表示，发起式基金可突破2亿元成立门槛，便于公募快速补齐细分行业与主题指数产品线；管理人自有资金不少于1000万元并锁仓三年，实现与持有人利益深度绑定，有助于在市场震荡、募资难度提升时支持公募逆向布局潜力赛道。<br><b>待发储备：</b>据基金公司人士透露，首批18只主动ETF获批在即；9月11日晚证监会官网显示，华夏基金等数家头部公募申报首批中证新能源金属50ETF。<br><b>对腾安启示：</b>低位密集发行主题ETF容易诱发客户“追新”，算力、金融科技等新主题ETF上架时应同步展示估值分位与成分股集中度，并配套分批建仓提示。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260912A02I9Q00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-12</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


'''

C2 = '''      <!-- S0 Card 2 (09-11 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批中证新能源金属50ETF与沪深港智能驾驶ETF同日申报·18家管理人集体出手</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报9月11日（记者李树超）：证监会官网信息显示，9月11日华夏、招商、华泰柏瑞、天弘、银华、建信、鹏华、华宝、华安、万家等<b>10家管理人申报首批中证新能源金属50ETF</b>；同日易方达、广发、汇添富、南方、博时、工银瑞信、永赢、平安等<b>8家管理人申报全市场首批中证沪深港智能驾驶主题ETF</b>，两批产品申报状态均已显示为“接收材料”。<br><b>指数画像：</b>中证新能源金属50指数选取不超过50只涉及锂、钴、镍、稀土等新能源金属材料的上市公司，前十大权重含北方稀土、盐湖股份、藏格矿业；中证沪深港智能驾驶主题指数横跨沪深港三地，前十大权重含小米集团、芯原股份、豪威集团、理想汽车、小鹏集团、舜宇光学科技、思特威等。<br><b>政策背景：</b>今年8月证监会主席吴清在香港表示“支持两地指数公司加强合作，推出更多基于中国资产的指数”，本次集体上报是落实两地协同部署的具体行动。<br><b>对腾安启示：</b>跨市场主题ETF将密集上市，行情页需支持沪深港三地成分展示与港股通额度提示，并对新能源金属的强周期属性做前置风险揭示。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR53fc623f-5d90-9666-1ac3-3a23a27a5495" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·09-11</span></a>
          <a href="https://finance.sina.com.cn/roll/2026-09-11/doc-inirnnxw5692817.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">央广网/澎湃·09-11</span></a>
          <span class="impact-tag medium">产品：中</span>
        </div>
      </div>


'''

C3 = '''      <!-- S0 Card 3 (09-11 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 第二批摊余成本法债基上报·13家中小公募集体出手·两批累计28家</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          财联社9月11日（记者周晓雅）：证监会官网显示，汇泉、博远、东方阿尔法、泉果、益民、泰信、汇百川、瑞达、中海、博道、恒越、东财、苏新等<b>13家基金管理人旗下的63个月封闭式债基申报材料被接收</b>，为继8月14日15家之后的第二批，两批合计28家；上海证券报9月12日亦确认该批产品于9月11日晚间上报。<br><b>产品特征：</b>两批产品一致，均为63个月封闭期、到期终止，单只募集规模上限不超过80亿元；摊余成本法以“买入—持有到期—票息逐日摊销”估值，可削弱债券二级价格波动对净值的冲击，并降低流动性管理压力。<br><b>托管格局：</b>据业内透露，博远、瑞达、中海、泰信、博道、汇泉6家产品或由兴业银行托管，恒越、苏新、泉果、汇百川4家或在浦发银行；参与资金以银行理财、银行自营与保险资金为主。<br><b>对腾安启示：</b>63个月封闭期对客户流动性与预期管理要求极高，代销端须明示封闭期、估值方法与到期安排，严禁与开放式债基混同推荐。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202609113872214751.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·09-11</span></a>
          <a href="https://news.qq.com/rain/a/20260912A02I9Q00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-12</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


'''

C4 = '''      <!-- S0 Card 4 (09-12 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 算力ETF进入上市期·天弘创业板算力ETF 9月16日登陆深交所·易方达同主题募集14.77亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-12</span>
          </div>
        </div>
        <div class="card-body">
          深圳证券交易所公告，<b>创业板算力ETF天弘（158061）自9月16日起上市交易</b>——该产品8月28日获批、9月4日发行当日提前结募、9月9日成立，12天内完成“获批—结募—成立”三级跳，是首批10只创业板算力ETF中率先成立并率先上市的产品，也有望成为全市场首只上市的算力ETF；其跟踪的创业板算力基础设施指数含50只标的、国产算力占比74.5%。<br><b>同期节奏：</b>易方达9月12日公告，易方达创业板算力基础设施ETF于9月4日至8日募集，<b>18161户有效认购、净认购金额14.77亿元</b>，合计募集份额14.77亿份，9月11日完成基金备案、基金合同生效；其中管理人从业人员认购19.90万份（占比0.0135%），管理人固有资金未参与认购。<br><b>对腾安启示：</b>同一指数多只ETF集中上市将带来短期关注度与资金分流，首页需补齐同指数产品的费率、规模与日均成交对比，并提示细分主题ETF的高波动属性。
        </div>
        <div class="card-footer">
          <a href="https://fund.szse.cn/dynamic/t20260911_622815.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">深圳证券交易所·09-11</span></a>
          <a href="https://finance.caijing.com.cn/20260912/5183181.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财经网·09-12</span></a>
          <span class="impact-tag low">产品：中</span>
        </div>
      </div>


'''

S0_NEW = C1 + C2 + C3 + C4
src = src[:S0_START] + S0_NEW + src[S0_END:]
s0_new_div = divs(S0_NEW)

# =========================================================
# STEP 5: S2 删除 08-28 过期卡 + 新增监管卡
# =========================================================
tag_0828 = src.index('<span class="date-tag">08-28</span>')
card_open = src.rindex('<div class="card p', 0, tag_0828)
c_start, c_end = card_block_at(src, card_open)
removed = src[c_start:c_end]
assert '中基协华东研讨交流会' in removed, '删除的卡片不是 S2 华东交流会卡'
src = src[:c_start] + src[c_end:]

S2_NEW_CARD = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-11</span>
          </div>
          <div class="card-title">🔴 证监会集中处罚4起编造传播虚假税率信息案·百万粉丝财经博主罚20万·2名证券从业人员被罚禁入</div>
        </div>
        <div class="card-body">
          证监会9月11日集中公布〔2026〕37—40号行政处罚决定书，对陈广华、宗建树、马星瑞、卢润凯4人编造、传播虚假税率调整信息的行为作出处罚：<b>证券从业人员宗建树编造信息并在微信群发布，被采取5年证券市场禁入</b>；证券从业人员马星瑞原文转发被罚<b>30万元</b>；卢润凯借助AI工具生成并发布虚假文章被罚<b>20万元</b>；运营粉丝超103万自媒体账号的陈广华发布该类信息被罚<b>20万元</b>。<br><b>关键定性：</b>4人均无违法所得，证监会仍认定其扰乱证券市场——处罚明确“获利与否并非承担行政责任的前提”；宗建树因公安机关已处罚款，证监会不再罚款，但因其情节严重予以市场禁入。<br><b>市场影响：</b>相关虚假信息曾于2026年2月3日扰动互联网、游戏板块，多家公司否认后板块回升。<br><b>对腾安启示：</b>自媒体与AI生成内容已成虚假信息高发源，销售端投教素材与社群内容须建立“先核源、后发布”的审核留痕机制，严禁转发未经证实的税收、费率类政策传闻。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">影响：高</span>
          <a href="https://www.csrc.gov.cn/csrc/c101928/c7658121/content.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证监会·09-11</span></a>
          <a href="https://finance.sina.com.cn/jjxw/2026-09-12/doc-inirpqmf1638842.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经营报·09-12</span></a>
        </div>
      </div>

'''
anchor_s2 = '    </div>\n  </div>\n<!-- ============ Section 3'
assert src.count(anchor_s2) == 1, 'S2 尾部锚点不唯一'
src = src.replace(anchor_s2, S2_NEW_CARD + anchor_s2)

# =========================================================
# STEP 6: S6 行情卡替换（09-11 收盘）
# =========================================================
s6_head = src.index('<!-- ============ Section 6')
s6_open = src.index('<div class="card p3">', s6_head)
s6_start, s6_end = card_block_at(src, s6_open)

S6_NEW = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-11）·沪指3888.11 -1.18%·全市场成交1.99万亿放量3248亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-11</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-11收盘·放量震荡）</b><br>
              上证指数 <b>3888.11</b> <span style="color:#52c41a;">-1.18%</span><br>
              深证成指 <b>13471.26</b> <span style="color:#52c41a;">-1.08%</span><br>
              创业板指 <b>3322.04</b> <span style="color:#52c41a;">-0.49%</span><br>
              科创综指 <b>1817.68</b> <span style="color:#52c41a;">-1.45%</span><br>
              北证50 <b>1023.46</b> <span style="color:#52c41a;">-2.66%</span><br>
              全市场成交 <b>1.99万亿</b>·较上日放量3248亿·本周连续5日低于2万亿<br>
              643只个股上涨·40只涨停·4870只下跌·21只跌停
            </div>
            <div>
              <b>港股与美股（09-11收盘）</b><br>
              恒生指数 <b>24805.63</b> <span style="color:#52c41a;">-0.60%</span><br>
              恒生科技 <b>4320.57</b> <span style="color:#52c41a;">-0.23%</span><br>
              国企指数 <b>8246.33</b> <span style="color:#52c41a;">-0.34%</span><br>
              道琼斯 <b>52573.29</b> <span style="color:#dc2626;">+0.98%</span><br>
              纳斯达克 <b>26333.04</b> <span style="color:#dc2626;">+0.96%</span><br>
              标普500 <b>7656.98</b> <span style="color:#dc2626;">+0.86%</span><br>
              布伦特原油104.32美元 <span style="color:#52c41a;">-3.08%</span>·COMEX黄金4390.00美元 <span style="color:#52c41a;">-0.39%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>放量震荡、结构分化——申万一级行业中仅通信（+1.41%）、建筑材料（+0.13%）上涨，有色金属（-3.98%）、基础化工（-2.98%）、房地产（-2.93%）领跌；玻璃纤维指数涨4.78%、覆铜板涨2.58%、高速铜连接涨2.28%逆势活跃，中际旭创、新易盛对创业板指合计贡献25.82点。本周主力资金呈“越跌越买”特征：电子行业净流入逾597亿元、通信逾275亿元，机械设备与国防军工均超百亿元，非银金融与计算机净流出超百亿元；南向资金净买入44.31亿港元，恒指全周仍累跌3.30%。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-11收盘</span>
          <span class="source-tag">数据来源：中国证券网/中证网/新华社（09-11—09-12）</span>
        </div>
      </div>'''
src = src[:s6_start] + S6_NEW + src[s6_end:]

# =========================================================
# STEP 7: S7 时间线整块替换（12 条，降序）
# =========================================================
s7_head = src.index('<!-- ============ Section 7')
tl_start = src.index('      <div class="timeline-item">', s7_head)
tl_end_marker = '    </div>\n\n  </div>\n\n</div>\n\n</body>'
tl_end = src.index(tl_end_marker, s7_head)
S7_OLD = src[tl_start:tl_end]

ITEMS = [
    ('blue', '2026-09-12', '算力ETF进入上市期·天弘9-16挂牌'),
    ('blue', '2026-09-12', '第二批摊余成本法债基上报'),
    ('red', '2026-09-11', '金融强国“十五五”规划正式出台'),
    ('blue', '2026-09-11', '公募布局白盒固收+·规模超2.28万亿'),
    ('red', '2026-09-11', '两大主题ETF集中申报·18家'),
    ('red', '2026-09-11', 'A股放量调整·成交1.99万亿'),
    ('red', '2026-09-10', 'A股缩量调整·成交创年内次低'),
    ('red', '2026-09-10', '易方达4只ETF以TDR登陆泰交所'),
    ('red', '2026-09-10', '新基金低位快速建仓·9月99只'),
    ('blue', '2026-09-10', '粮食畜牧ETF走强·最高涨超20%'),
    ('red', '2026-09-09', '中金获批控股东兴基金信达澳亚'),
    ('red', '2026-09-09', '首批8只北交所三个月持有期基金获批'),
]
for _, _, t in ITEMS:
    assert len(t) <= 25, 'S7 标题超25字：%s (%d)' % (t, len(t))

S7_NEW = ''
for color, d, t in ITEMS:
    S7_NEW += (
        '      <div class="timeline-item">\n'
        '        <div class="timeline-dot %s"></div>\n'
        '        <div class="timeline-date">%s</div>\n'
        '        <div class="timeline-title">%s</div>\n'
        '      </div>\n\n' % (color, d, t)
    )
src = src[:tl_start] + S7_NEW + src[tl_end:]

# =========================================================
# PHASE 1 断言（全部通过才写文件）
# =========================================================
print('=== Phase1 断言 ===')
assert BADGE_NEW in src, 'badge 未更新'
assert '2026.08.29' in src and '2026.09.12' in src
assert src.count('📅 数据区间') == 1

# Stats Bar 断言（收窄到 stats-bar 段）
st_i = src.index('<div class="stats-bar">')
st_j = src.index('</div>\n<div class="main">', st_i)
stats_seg = src[st_i:st_j]
assert '3888.11' in stats_seg, 'Stats 沪指未更新'
assert '3934.40' not in stats_seg, 'Stats 旧值残留'

# S0 断言
seg0_start = src.index('<!-- ============ Section 0')
seg0_end = src.index('<!-- ============ Section 1')
seg0 = src[seg0_start:seg0_end]
assert seg0.count('<div class="card p') == 4, 'S0 卡片数异常：%d' % seg0.count('<div class="card p')
assert seg0.count(CTX_NEW) == 1, 'S0 context 未更新'
assert 'section-title">今日焦点</span>' in seg0, 'S0 title 非四字'
assert seg0.count('action-box') == 0, 'S0 不应有 action-box（本日无 P0）'
assert seg0.count('<span class="date-tag">09-12</span>') == 2
assert seg0.count('<span class="date-tag">09-11</span>') == 2
assert seg0.count('target="_blank"') == 7, 'S0 链接数异常：%d' % seg0.count('target="_blank"')
assert '3934.40' not in seg0

# S2 断言
seg2 = src[src.index('<!-- ============ Section 2'):src.index('<!-- ============ Section 3')]
assert seg2.count('<div class="card p') == 4, 'S2 卡片数异常：%d' % seg2.count('<div class="card p')
assert '08-28' not in seg2, 'S2 过期卡未删'
assert seg2.count('<span class="date-tag">09-11</span>') == 1

# S6 断言
seg6 = src[src.index('<!-- ============ Section 6'):src.index('<!-- ============ Section 7')]
assert '3888.11' in seg6 and '2026-09-11' in seg6
assert '3934.40' not in seg6, 'S6 旧值残留'
assert seg6.count('<div class="card p3">') == 1

# S7 断言
seg7 = src[src.index('<!-- ============ Section 7'):]
assert seg7.count('<div class="timeline-item">') == 12, 'S7 条数异常'
assert 'timeline-desc' not in seg7
dates = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>', seg7)
assert dates == sorted(dates, reverse=True), 'S7 未按日期降序'
assert min(dates) >= '2026-08-29', 'S7 存在超窗日期'

# S8 不存在
assert 'S8' not in src and '待办跟踪' not in src and '腾安行动清单' not in src

# 全文件 date-tag 超窗检查（含 S3-S5）
all_tags = sorted(set(re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src)))
bad = [t for t in all_tags if '2026-%s-%s' % (t[0], t[1]) < '2026-08-29']
assert not bad, '存在超窗 date-tag：%s' % bad

# 黑名单
for kw in ['so.html5.qq.com', 'toutiao', '企鹅号', '网易号', '搜狐号', 'stcn.com', 'cls.cn', '21jingji.com', 'yicai.com']:
    assert kw not in src, '黑名单命中：%s' % kw

# 游离字符
assert src.count('</div>>') == 0
assert '�' not in src

# div 平衡（per-step 漂移）
o_old, c_old = divs(orig)
o_new, c_new = divs(src)
exp_o = s0_new_div[0] - s0_old_div[0]
exp_c = s0_new_div[1] - s0_old_div[1]
print('div: orig open=%d close=%d | new open=%d close=%d' % (o_old, c_old, o_new, c_new))
print('div drift: open %+d (expect %+d) | close %+d (expect %+d)' % (o_new - o_old, exp_o, c_new - c_old, exp_c))
assert o_new == o_old + exp_o and c_new == c_old + exp_c, 'div 漂移不符合预期'
assert o_new == c_new, 'div 全局不平衡：%d vs %d' % (o_new, c_new)

io.open(PATH, 'w', encoding='utf-8').write(src)
print('=== 写入完成：index.html (%d bytes) ===' % len(src.encode('utf-8')))
