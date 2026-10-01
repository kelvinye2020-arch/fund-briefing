# -*- coding: utf-8 -*-
"""
daily-update 2026-10-01（国庆假期·A股10/1-10/7休市，行情基准=09-30收盘）
T-14 边界 = 2026-09-17
"""
import re, io, os, sys
from datetime import date, timedelta

os.chdir(os.path.dirname(os.path.abspath(__file__)))
HTML = 'index.html'
TODAY = date(2026, 10, 1)
T14 = TODAY - timedelta(days=14)          # 2026-09-17
EMO = '\U0001F4C5'

src = open(HTML, encoding='utf-8').read()
o0, c0 = src.count('<div'), src.count('</div>')

def drift(tag):
    global o0, c0
    o, c = src.count('<div'), src.count('</div>')
    print(f'   [{tag}] open {o0}->{o} ({o-o0:+d}) | close {c0}->{c} ({c-c0:+d})')
    o0, c0 = o, c

# =========================================================
# STEP 0: marker / fingerprint / header badge（写卡第一步，防闸0/闸1/闸6）
# =========================================================
src, n = re.subn(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
                 '<!-- daily-update: 2026-10-01 -->', src, count=1)
assert n == 1, 'marker 替换失败'

FP = '网络营销|公募前三|新基发行|公募四季'
src, n = re.subn(r'<meta name="content-fingerprint" content="[^"]*">',
                 f'<meta name="content-fingerprint" content="{FP}">', src, count=1)
assert n == 1, 'fingerprint 替换失败'

upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
badge_pat = re.escape(EMO) + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）'
badge_new = f'{EMO} 数据区间：{lower} — {upper}（每日更新）'
src, n = re.subn(badge_pat, badge_new, src, count=1)
assert n == 1, 'header 数据区间 badge 替换失败'
print(f'STEP0 ok  badge={badge_new}')

# =========================================================
# STEP 1: S0 section-context
# =========================================================
old_ctx = '<span class="section-context">9月30日 · 4条今日要闻</span>'
new_ctx = '<span class="section-context">10月1日 · 4条今日要闻</span>'
assert src.count(old_ctx) == 1
src = src.replace(old_ctx, new_ctx)
print('STEP1 ok  section-context ->', new_ctx)

# =========================================================
# STEP 2: S0 四卡整块替换
# =========================================================
SRC_LINK = ('<a href="{u}" target="_blank" style="color:#1890ff;text-decoration:none;">'
            '<span class="source-tag">{t}</span></a>')

def links(pairs):
    return '\n          '.join(SRC_LINK.format(u=u, t=t) for u, t in pairs)

C1_BODY = (
 '          中国网9月30日报道：中国人民银行、工业和信息化部、市场监管总局、金融监管总局、中国证监会、'
 '国家知识产权局、国家网信办、国家外汇局等<b>八部门</b>联合印发的《金融产品网络营销管理办法》自'
 '<b>9月30日起正式实施</b>。《办法》为网络金融营销划定清晰红线——'
 '①<b>主体资质</b>：只有金融机构及其依法委托的第三方互联网平台才能开展金融产品网络营销，营销人员须为'
 '金融机构从业人员并取得相应资格证书与机构授权；未取得金融业务资质的机构和个人，不得在账号名称中使用'
 '“理财”“贷款”“基金”“资产管理”等涉金融属性字样；'
 '②<b>跳转转接</b>：第三方平台提供购买推荐的，必须跳转至金融机构自营平台完成购买，不得再转至另一家营销平台；'
 '③<b>算法与支付</b>：不得设置诱导过度消费的算法模型，并提供便捷的算法推荐关闭服务；非银行支付机构不得将'
 '贷款、资产管理产品等列入支付工具选项，实现支付功能与金融产品有效区隔；'
 '④<b>话术与流程</b>：严禁“低风险”“低门槛”“秒到账”“高收益”等诱导性话术，禁止默认勾选与违法搭售，'
 '弹窗广告须有显著关闭标志并可一键关闭。<br>\n'
 '          <b>落地反应（中国经营报，记者罗辑、夏欣）：</b>过去几年短视频与社交平台已成为基金证券产品重要获客阵地，'
 '<b>财经大V带货引流、营销链路责任模糊、流量优先的销售导向</b>三类乱象被划定监管红线。'
 '晨星（中国）基金研究中心分析师王珊指出，问题集中在无资质主体变相营销、简化风险提示与片面展示历史收益、'
 '营销链路多层转包导致纠纷时机构/平台/自媒体互相推诿。北京师范大学经济与工商管理学院副院长胡聪慧认为，'
 '金融资管产品具有<b>跨期交付、结果不确定、风险后置</b>特征，并不适合沿用普通消费品的流量营销、情绪营销与'
 '即时转化逻辑；即便持牌机构与合规投顾，在流量考核和销售导向下也会放大短期业绩、弱化风险提示，'
 '这正是本轮行业自查整改重点纠偏的方向。多位受访者判断，新规并不否定线上渠道价值，而是推动行业跳出'
 '消费品式流量营销逻辑，向<b>专业化、买方化</b>转型，行业线上内容生态或将出现再平衡。<br>\n'
 '          <b>对腾安启示（直接对象）：</b>腾安作为第三方互联网平台正是本轮规范的主体，须在9月30日后立刻落实四件事——'
 '①<b>合作主体白名单化</b>：所有代销与引流合作方须完成信息技术系统备案并纳入季度自查清单，'
 '严禁任何个人账号（大V、员工私号）带货导流；'
 '②<b>跳转链路自查</b>：所有购买/开户转接必须落到基金公司自营平台，不得二次跳转，'
 '进入购买环节前设置显著提醒与强制阅读时间；'
 '③<b>内容生产权回收</b>：宣传素材由持牌主体统一出稿并留痕，直播、短视频、图文、评论区答疑全部可回溯，'
 '出镜人员须持从业资格并获机构授权，禁止以“投资者教育”“课程培训”名义变相营销并支付费用；'
 '④<b>话术与收银台改造</b>：清理“低风险”“稳赚”类表述，支付页面中理财/信贷选项须与银行卡、零钱分开展示，'
 '并关闭默认勾选。'
)
C1_ACTION = (
 '            ① 9月30日前完成全渠道营销合作台账与转接链路盘点，未备案平台限期清退；<br>\n'
 '            ② 把“大V / 个人账号合作”从商务流程中彻底下架，改由持牌员工在自营或官方授权账号输出；<br>\n'
 '            ③ 上线营销素材统一审核与留痕系统，A/B文案、落地页改字、直播回放全部留日志；<br>\n'
 '            ④ 收银台与跳转页按新规改造，并保留改造前后截图备查。'
)

C2_BODY = (
 '          同花顺财经10月1日报道（作者陈书玉）：2026年前三季度A股风格经历从“科技一枝独秀”到“极致再平衡”的'
 '剧烈切换——上半年AI、半导体、光模块带动科技板块上涨，三季度遭遇回调，创业板指、科创50双双创下单季历史最大跌幅，'
 '医药、红利、周期等低位方向轮动接棒。Wind数据显示，截至<b>9月30日收盘</b>，上证指数报3842.19点、前三季度累计'
 '下跌3.19%；深证成指报12887.62点、跌4.71%；创业板指报3135.28点、跌2.12%；<b>科创50报1530.01点、涨13.82%</b>，'
 '是唯一收益率为正的核心宽基指数。<br>\n'
 '          <b>基金端：</b>万得普通股票型基金指数、万得偏股混合型基金指数前三季度增长率分别为<b>3.69%、1.89%</b>。'
 '全市场共诞生<b>2只“翻倍基”</b>——均由易方达基金杨宗昌管理，易方达供给改革、易方达产业机遇A收益率分别为'
 '<b>115.67%、111.62%</b>；汇安趋势动力A、诺安创新驱动A、东方人工智能主题A收益率均超90%；另有申万菱信智能驱动A、'
 '国泰半导体制造精选A、财通多策略福鑫、银华集成电路A、财通匠心优选一年持有A等<b>11只基金收益率超80%</b>。<br>\n'
 '          <b>另一面：</b>共有<b>5770只基金前三季度收益率为负</b>（近四成），其中779只跌超20%、<b>13只跌超40%</b>；'
 '鹏华制造升级A以-49.73%垫底，持仓追溯显示其在不到一年操作期内历经三轮大面积换仓（汽车零部件→机器人产业链→'
 '商业航天与光伏→AI硬件），持仓节奏与市场轮动方向出现错位。<b>首尾收益差距超165个百分点</b>。<br>\n'
 '          <b>品类：</b>ETF方面中韩半导体ETF华泰柏瑞以82.27%居首，科创半导体设备ETF鹏华、科创半导体ETF华夏、'
 '科创半导体设备ETF华泰柏瑞均超80%；QDII方面13只收益率超50%，南方原油A以78.99%领跑。<br>\n'
 '          <b>对腾安启示：</b>首尾差165pct意味着“选基”比“选时”更能决定用户体感——货架须把'
 '<b>区间收益、最大回撤、换手率、持仓集中度</b>四项并列展示，对同一基金经理在管产品做回撤联动提示；'
 '对跌幅居前的赛道集中型产品加挂“单一赛道集中度”风险标签，并在业绩榜中同步给出“近三年”而非仅“今年以来”口径，'
 '避免用户被短期排名误导。'
)

C3_BODY = (
 '          财联社10月1日讯（记者吴雨其）：经历8月低谷后，新基金发行在9月明显回升，单月发行份额重新站上千亿份。'
 'Wind数据显示，按基金成立日统计，截至9月30日年内共有<b>1388只新基金成立</b>，合并发行份额<b>8692.35亿份</b>；'
 '<b>9月单月成立201只、发行1006.71亿份</b>，较8月的151只、499.53亿份分别增长33.11%与101.53%，'
 '成立数量仅次于6月的209只为年内第二高，发行份额为年内第五次单月超千亿份。<br>\n'
 '          <b>结构：</b>9月单只基金平均发行约5.01亿份（8月3.31亿份），修复快于数量，主要来自月末一批中小基金公司'
 '大额摊余成本法债基集中成立。<b>30只债券型基金合计发行490.56亿份，占当月48.73%</b>；其中路博迈安瑞63个月封闭、'
 '贝莱德稳利63个月封闭、红土创新瑞泽63个月封闭、财信聚鑫63个月封闭分别为80.01亿份、80.00亿份、80.00亿份、'
 '79.99亿份，4只合计320亿份，不足当月数量的2%却贡献<b>31.79%</b>的发行份额，并包揽前九月新基金单品发行份额前四。'
 '股票型基金94只居数量首位、发行219.05亿份，其中<b>被动指数型81只、182.49亿份，占比超八成</b>；'
 '混合型168.36亿份、FOF 111.96亿份。<br>\n'
 '          <b>节后排期：</b>9月共160只基金启动募集（8月181只），9月28日至30日仅8只开售；截至9月30日处于募集期的'
 '有50只，其中38只跨节延续。<b>已有97只基金计划于10月8日至26日启动募集</b>——10月8日20只、<b>10月12日50只</b>，'
 '两个交易日就有70只开售；结构上股票型30只（23只被动指数）、混合型29只（25只偏股混合）、FOF 21只、'
 '债券型10只，另有6只REITs与1只QDII。富国、华夏、汇添富、南方、嘉实旗下<b>5只北交所主题基金</b>节后陆续开售，'
 '募集份额上限均为5亿份。<br>\n'
 '          <b>对腾安启示：</b>10月8日与10月12日是全年最密集的两个发行日，货架须提前完成'
 '<b>新发专区排期表</b>（按日分组、标注募集上限与结募日），并对5只北交所主题基金统一加挂'
 '<b>5亿份上限＋末日比例配售</b>提示；同时把“跨节募集38只”的认购资金冻结与确认规则前置说明，'
 '避免节后首日集中申购引发体验投诉。'
)

C4_BODY = (
 '          21世纪经济报道（特约记者庞华玮）9月30日报道：国泰基金、平安基金、财通资管、南方基金、长城基金、'
 '前海开源基金、国海富兰克林基金、上银基金等多家公募机构陆续发布四季度A股投资策略，'
 '<b>“科技+红利”哑铃策略成为主流共识</b>——一端布局AI算力、光通信、半导体、PCB等业绩兑现方向，'
 '另一端配置低波红利、黄金、铜等防御性资产，同时关注创新药、新能源、化工、制造出海等结构性机会。<br>\n'
 '          <b>大势研判：</b>多数机构对四季度相对乐观，核心逻辑是三季度科技股调整已比较充分、估值与交易拥挤度'
 '明显回落而产业趋势并未证伪。国海富兰克林基金指出三季度创业板指、科创50回撤均超20%，风险收益比改善，'
 '而AI产业发展仍在加速（全球九大云厂商2026年资本开支预计约8867亿美元、2027年或升至1.3万亿美元）。'
 '国泰基金判断四季度有望反弹但斜率放缓、锐度降低，A股估值扩张空间有限，<b>进入盈利消化估值阶段</b>；'
 '前海开源首席经济学家杨德龙认为科技股一枝独秀难再现，更可能是板块轮动。<br>\n'
 '          <b>风险提示：</b>平安基金指出年内盈利贡献已明显超越估值，实现从估值主导到盈利主导的切换，'
 '但盈利改善多源自海内外AI投资拉动与产业链涨价，持续性存疑——海外AI资本开支已迫使云厂商现金流陆续转负，'
 '中下游需求难以消化上游涨价，仅上游资源、先进制造毛利率呈上行趋势。上银基金提醒短期市场大概率仍是存量博弈，'
 '海外地缘局势与加息预期是主要不确定性。<br>\n'
 '          <b>对腾安启示：</b>“科技+红利哑铃”已是机构对客的标准话术，腾安可把它做成'
 '<b>可选的一键组合模板</b>（进攻端科技ETF＋防御端红利/黄金ETF），但必须同步给出'
 '“两端并非恒定比例、需按季度再平衡”的说明，并对科技端加挂高波动与赛道集中风险标签；'
 '同时把“盈利验证”作为三季报窗口期的核心筛选维度，在货架上新设“三季报预增/订单兑现”主题入口。'
)

S0_CARDS = []
S0_CARDS.append(f'''<!-- S0 Card 1 (09-30 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">\U0001F534 《金融产品网络营销管理办法》9月30日正式施行·八部门联合印发·无资质不得开展金融产品营销</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
{C1_BODY}
        </div>
        <div class="card-footer">
          {links([('https://news.china.com.cn/2026-09/30/content_118719175.shtml', '中国网·09-30'),
                  ('https://finance.sina.cn/2026-09-30/detail-initqqvi5818529.d.html', '中国经营报·新浪财经·09-30')])}
          <span class="impact-tag high">影响：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
{C1_ACTION}
          </div>
        </div>
      </div>
''')

S0_CARDS.append(f'''<!-- S0 Card 2 (10-01 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 公募前三季度成绩单出炉·2只翻倍基最高115.67%·5770只负收益·首尾差超165pct</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-01</span>
          </div>
        </div>
        <div class="card-body">
{C2_BODY}
        </div>
        <div class="card-footer">
          {links([('https://news.10jqka.com.cn/20261001/c680425888.shtml', '同花顺财经·10-01')])}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

S0_CARDS.append(f'''<!-- S0 Card 3 (10-01 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 9月新基发行重回千亿份·201只1006.71亿份·节后97只已排上开售日程</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-01</span>
          </div>
        </div>
        <div class="card-body">
{C3_BODY}
        </div>
        <div class="card-footer">
          {links([('https://news.qq.com/rain/a/20261001A05YMY00', '腾讯新闻·财联社·10-01')])}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

S0_CARDS.append(f'''<!-- S0 Card 4 (09-30 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 公募四季度策略曝光·“科技+红利”哑铃成共识·盈利接棒估值</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-30</span>
          </div>
        </div>
        <div class="card-body">
{C4_BODY}
        </div>
        <div class="card-footer">
          {links([('https://finance.sina.com.cn/roll/2026-09-30/doc-initrmyx5720126.shtml', '新浪财经·21世纪经济报道·09-30')])}
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
''')

s0_start = src.index('<!-- S0 Card 1')
s0_end = src.index('<!-- ============ Section 1')
new_s0 = ''.join(S0_CARDS) + '    </div>\n  </div>\n'
src = src[:s0_start] + new_s0 + src[s0_end:]
drift('S0')

s0 = src[src.index('<!-- S0 Card 1'):src.index('<!-- ============ Section 1')]
assert s0.count('action-box') == 1, f'action-box 计数异常 {s0.count("action-box")}'
tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s0)
assert tags == [('09','30'), ('10','01'), ('10','01'), ('09','30')], f'S0 date-tag={tags}'
nlink = len(re.findall(r'<a href="http', s0))
assert nlink == 5, f'S0 链接数 {nlink} != 5'
assert re.search(r'<span class="section-title">今日焦点</span>', src), 'S0 title 不是「今日焦点」'
print('STEP2 ok  S0 4卡 date-tag', tags, 'links', nlink)

# =========================================================
# STEP 3: S2 删除与 S0 P0 撞题的「上海证监局网络营销六大要求 (09-17)」卡
# =========================================================
a = src.index('<!-- S2 Card: 上海证监局网络营销六大要求 (09-17 P0) -->')
a = src.rindex('\n', 0, a) + 1
b = src.index('<!-- S2 Card: 证监会公示吹哨人奖励名单 (09-18 P1) -->')
b = src.rindex('\n', 0, b) + 1
src = src[:a] + src[b:]
drift('S2-del')
s2 = src[src.index('<!-- ============ Section 2'):src.index('<!-- ============ Section 3')]
s2n = len(re.findall(r'<div class="card p\d">', s2))
assert s2n == 3, f'S2 卡数 {s2n} != 3'
print('STEP3 ok  S2 删 09-17 撞题卡，剩 3 卡（上限4，下周一巡检补齐）')

# =========================================================
# STEP 4: Stats Bar 沪指卡 -> 09-30 收盘
# =========================================================
old_stat = '''      <div class="stat-number">3830.45</div>
      <div class="stat-label">沪指9-29收盘·涨0.18%·沪深北三市成交1.42万亿·创近14个月地量</div>
      <div class="stat-change up">▲ 近3500股上涨·地产链领涨·科创50涨0.86%</div>'''
new_stat = '''      <div class="stat-number">3842.19</div>
      <div class="stat-label">沪指9-30收盘·涨0.31%·沪深北三市成交1.45万亿·节前红盘收官</div>
      <div class="stat-change up">▲ 2567股上涨56只涨停·医药酿酒领涨·科创50跌2.51%</div>'''
assert src.count(old_stat) == 1
src = src.replace(old_stat, new_stat)
drift('stats')
sb = src[src.index('<div class="stats-bar">'):src.index('<div class="main">')]
assert '3842.19' in sb and '3830.45' not in sb, 'Stats Bar 未更新'
print('STEP4 ok  Stats Bar 沪指 -> 09-30 收盘 3842.19 +0.31%')

# =========================================================
# STEP 5: S6 市场行情 -> 09-30 收盘（A股/港股/美股统一）
# =========================================================
S6 = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股09-30收盘·沪指3842.19 +0.31%沪深北成交1.45万亿｜港股与美股09-30收盘</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">10-01</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-30收盘·节前红盘收官）</b><br>
              上证指数 <b>3842.19</b> <span style="color:#dc2626;">+0.31%</span><br>
              深证成指 <b>12887.62</b> <span style="color:#52c41a;">-0.11%</span><br>
              创业板指 <b>3135.28</b> <span style="color:#52c41a;">-0.23%</span><br>
              沪深300 <b>4357.62</b> <span style="color:#dc2626;">+0.29%</span><br>
              科创50 <b>1530.01</b> <span style="color:#52c41a;">-2.51%</span><br>
              科创综指 <b>1815.22</b> <span style="color:#52c41a;">-1.81%</span><br>
              北证50 <b>1039.61</b> <span style="color:#dc2626;">+0.70%</span><br>
              沪深北三市成交 <b>1.45万亿</b>·较上一交易日小幅放量285亿<br>
              2567只上涨·56只涨停
            </div>
            <div>
              <b>港股与美股（09-30收盘）</b><br>
              恒生指数 <b>24613.27</b> <span style="color:#dc2626;">+0.37%</span><br>
              恒生科技 <b>4253.89</b> <span style="color:#dc2626;">+0.10%</span><br>
              国企指数 <b>8220.08</b> <span style="color:#dc2626;">+0.50%</span><br>
              道琼斯 <b>50906.05</b> <span style="color:#52c41a;">-0.86%</span><br>
              纳斯达克 <b>26861.06</b> <span style="color:#dc2626;">+0.24%</span><br>
              标普500 <b>7651.54</b> <span style="color:#52c41a;">-0.25%</span><br>
              布伦特原油103.53美元 <span style="color:#dc2626;">+0.92%</span>·美债10年期5.291%·30年期5.634%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>A股结构（09-30）：</b>三大指数小幅高开后走势分化，沪指震荡微幅上行、深证成指与创业板指微幅下行。
              行业涨跌参半——<b>生物制品、医疗服务、白酒、化学制药、航空机场、房屋建设、食品饮料、银行</b>涨幅居前，
              <b>元件、半导体</b>跌幅居前。创新药、CRO概念持续走强，康希诺、泰诺麦博、南华生物等多股涨停；
              分散染料概念延续强势；房地产板块探底反弹，陆家嘴、深物业A等涨停；种业、乳业、酿酒板块走高。
              资金方面<b>医疗服务净流入26.03亿元居首</b>，化学制药、能源金属紧随其后。
              按Wind口径，上证指数前三季度累计下跌3.19%、深证成指跌4.71%、创业板指跌2.12%，
              <b>科创50涨13.82%</b>为唯一正收益核心宽基。<br>
              <b>港股（09-30）：</b>恒指涨0.37%报24613.27点、恒生科技涨0.1%报4253.89点、国企指数涨0.50%报8220.08点。<br>
              <b>美股（09-30）：</b>美国8月PCE价格指数同比涨3.4%、核心PCE同比涨3.0%，均低于市场预期，
              二季度GDP终值修正为2.2%；纽约联储行长威廉姆斯称“无需急于”下月加息，交易员大幅回撤加息押注，
              CME FedWatch显示<b>10月加息25个基点概率降至约37%—38.2%</b>（一周前超70%），高盛把加息预期推迟至12月。
              但长端美债收益率持续攀升——30年期盘中突破5.65%、10年期一度升破5.3%，叠加油价走高，压制风险偏好，
              三大指数尾盘跳水、收盘涨跌不一。大型科技股普涨，苹果+1.10%、亚马逊+1.01%、谷歌-A+0.93%、微软+0.77%、
              特斯拉+0.56%、英伟达+0.51%，Meta跌1.84%；热门中概股多数上涨，纳斯达克中国金龙指数涨0.60%。
              9月纳指累涨1.86%、标普累跌0.45%、道指累跌4.29%；三季度纳指累涨2.47%、标普累涨2.03%、道指累跌2.70%。<br>
              <b>备注：</b>09-30为国庆假期前最后一个交易日，本期A股、港股、美股基准统一为09-30收盘。
              国庆假期安排：A股10月1日—7日休市、10月8日开市。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股 / 港股 / 美股均为2026-09-30收盘</span>
          <span class="source-tag">数据来源：新华社、中国证券网、天山网、新浪财经、东方财富行情（09-30—10-01）</span>
        </div>
      </div>  </div>
'''
s6_sec = src.index('<!-- ============ Section 6')
s6_start = src.index('            <div class="card p3">', s6_sec)
s6_end = src.index('<!-- ============ Section 7')
src = src[:s6_start] + S6 + src[s6_end:]
drift('S6')

# =========================================================
# STEP 6: S7 时间线重写 12 条（09-24 — 10-01）
# =========================================================
ITEMS = [
    ('red',   '2026-10-01', '公募前三季度成绩单出炉'),
    ('blue',  '2026-10-01', '9月新基发行重回千亿份'),
    ('red',   '2026-09-30', '网络营销930新规落地'),
    ('blue',  '2026-09-30', '首批红利增长ETF上报'),
    ('blue',  '2026-09-30', '张坤卸任优质企业三年持有'),
    ('blue',  '2026-09-30', 'A股红盘收官沪指3842点'),
    ('blue',  '2026-09-30', '恒指回升美股涨跌不一'),
    ('blue',  '2026-09-29', '半导体主题基金破3900亿'),
    ('blue',  '2026-09-28', '债券ETF规模首破万亿'),
    ('blue',  '2026-09-28', '商业不动产REITs三只受理'),
    ('blue',  '2026-09-25', '湖南百亿未来产业基金落地'),
    ('blue',  '2026-09-24', '中基协从业考试细则征求意见'),
]
items_html = ''.join(
    f'      <div class="timeline-item">\n'
    f'        <div class="timeline-dot {d}"></div>\n'
    f'        <div class="timeline-date">{dt}</div>\n'
    f'        <div class="timeline-title">{t}</div>\n'
    f'      </div>\n' for d, dt, t in ITEMS)

s7_sec = src.index('<!-- ============ Section 7')
s7_start = src.index('      <div class="timeline-item">', s7_sec)
anchor = '      </div>\n    </div>'
s7_end = src.index(anchor, s7_start) + len(anchor)
src = src[:s7_start] + items_html + '    </div>' + src[s7_end:]
drift('S7')
s7 = src[s7_sec:src.index('</body>')]
assert s7.count('<div class="timeline-item">') == 12, f'S7 条目 {s7.count("<div class=" + chr(34) + "timeline-item" + chr(34) + ">")} != 12'
assert 'timeline-desc' not in s7, 'S7 出现 timeline-desc'
print('STEP6 ok  S7 12 条')

# =========================================================
# STEP 7: 全量断言
# =========================================================
o, c = src.count('<div'), src.count('</div>')
assert o == c, f'div 失衡 open={o} close={c}'
assert 'Section 8' not in src and 'S8' not in src, 'S8 残留'
assert src.count(chr(0xFFFD)) == 0, 'U+FFFD 乱码'
assert src.count('</div>>') == 0, 'stray </div>>'
assert src.count('section-context') >= 1

# 闸2 预检：所有 date-tag >= T-14
bad = []
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
    mo, d = int(m.group(1)), int(m.group(2))
    dt = date(2026, mo, d)
    if dt < T14:
        bad.append(str(dt))
assert not bad, f'闸2 预检越界 date-tag: {bad}'

# 黑名单预检
BLACK = ['21jingji.com', 'stcn.com', 'cls.cn', 'yicai.com', 'guba.eastmoney.com']
for u in re.findall(r'href="(https?://[^"]+)"', src):
    dom = re.search(r'https?://([^/"]+)', u).group(1)
    for b in BLACK:
        assert b not in dom, f'黑名单域名 {dom}: {u}'

print(f'STEP7 ok  div {o}/{c} 平衡 · S8 无 · 闸2/闸3 预检通过')

open(HTML, 'w', encoding='utf-8').write(src)
print('\n=== 写入完成 index.html ===')
