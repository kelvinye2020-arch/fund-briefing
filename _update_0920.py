# -*- coding: utf-8 -*-
"""2026-09-20 每日更新：S0/S1/S2/S6/S7 + Stats Bar + header"""
import re, sys
from datetime import date, timedelta

SRC = 'index.html'
s = open(SRC, encoding='utf-8').read()
orig_open = len(re.findall(r'<div\b', s))
orig_close = s.count('</div>')

def dr(tag):
    o = len(re.findall(r'<div\b', s))
    c = s.count('</div>')
    print('   [drift-%s] open %+d close %+d (abs %d/%d) bal=%s'
          % (tag, o - orig_open, c - orig_close, o, c, 'Y' if o == c else 'N'))

TODAY = date(2026, 9, 20)
CUTOFF = TODAY - timedelta(days=14)   # 2026-09-06

# ---------- 通用工具 ----------
def card_bounds(t, start):
    """从 <div class="card pX"> 起点扫描到卡片闭合后（depth 初值=1）"""
    i = start
    depth = 1
    j = i + len('<div class="card p')
    while depth > 0:
        no = t.find('<div', j)
        nc = t.find('</div>', j)
        if nc == -1:
            raise ValueError('unbalanced at %d' % start)
        if no != -1 and no < nc:
            depth += 1
            j = no + 4
        else:
            depth -= 1
            j = nc + 6
    return i, j

def drop_card(t, kw):
    """按 card-title 关键字删除整张卡（含紧邻的前置注释）"""
    k = t.find(kw)
    assert k > 0, 'title not found: ' + kw
    c = t.rfind('<div class="card p', 0, k)
    assert c > 0 and k - c < 4000, 'card start not found: ' + kw
    a, b = card_bounds(t, c)
    # 前置注释一并删除
    pre = t.rfind('<!--', max(0, a - 400), a)
    if pre > 0:
        end = t.find('-->', pre)
        if end > 0 and end + 3 <= a and t[end + 3:a].strip() == '':
            a = pre
    # 尾部空行一并删除
    while b < len(t) and t[b] == '\n':
        b += 1
    return t[:a] + t[b:]

# ---------- 锚点 ----------
A_S0 = '                                <!-- ============ Section 0: 今日焦点 ============ -->'
A_S1 = '<!-- ============ Section 1: 重磅信息 ============ -->'
A_S2 = '<!-- ============ Section 2: 监管政策 ============ -->'
A_S3 = '<!-- ============ Section 3: 竞争对手动态 ============ -->'
A_S6 = '<!-- ============ Section 6: 市场行情速览 ============ -->'
A_S7 = '<!-- ============ Section 7: 关键时间线 ============ -->'
A_BODY = '\n</body>'
for a, n in [(A_S0, 'S0'), (A_S1, 'S1'), (A_S2, 'S2'), (A_S3, 'S3'),
             (A_S6, 'S6'), (A_S7, 'S7'), (A_BODY, 'BODY')]:
    assert s.count(a) == 1, 'anchor %s count=%d' % (n, s.count(a))
print('[ok] anchors')
dr('anchors')

# ============ 1. marker ============
s = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
           '<!-- daily-update: 2026-09-20 -->', s)
assert '<!-- daily-update: 2026-09-20 -->' in s

# ============ 2. fingerprint ============
FP = '刘彦春卸|首批摊余|姜晓丽正|新基金募'
s = re.sub(r'(<meta name="content-fingerprint" content=")[^"]*(")',
           r'\g<1>' + FP + r'\g<2>', s, count=1)
assert 'content="%s"' % FP in s

# ============ 3. header 数据区间 ============
upper = TODAY.strftime('%Y.%m.%d')
lower = CUTOFF.strftime('%Y.%m.%d')
badge = '📅 数据区间：' + lower + ' — ' + upper + '（每日更新）'
s, n = re.subn(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）', badge, s)
assert n == 1, 'badge sub n=%d' % n
assert badge in s

# ============ 4. Stats Bar 沪指卡 ============
i0 = s.find('<div class="stats-bar">')
i1 = s.find('</div>\n<div class="main">', i0)
assert i0 > 0 and i1 > i0
sb = s[i0:i1]
assert '3875.60' in sb
sb_new = sb.replace(
    '      <div class="stat-number">3875.60</div>\n'
    '      <div class="stat-label">沪指9-17收盘·跌0.41%·沪深两市成交1.82万亿·缩量160亿</div>\n'
    '      <div class="stat-change down">▼ 创业板-0.40%·科创50-0.61%·超2800股下跌</div>',
    '      <div class="stat-number">3911.87</div>\n'
    '      <div class="stat-label">沪指9-18收盘·涨0.94%·沪深两市成交2.08万亿·放量2540亿</div>\n'
    '      <div class="stat-change up">▲ 创业板+2.25%·科创综指+3.23%·超4200股上涨</div>')
assert sb_new != sb and '3911.87' in sb_new and '3875.60' not in sb_new
s = s[:i0] + sb_new + s[i1:]
print('[ok] stats bar')
dr('stats bar')

# ============ 5. S0 整段替换 ============
S0_NEW = '''                                <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">\U0001F525</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月20日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
      <!-- S0 Card 1 (09-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 刘彦春卸任景顺长城副总经理·专注投资管理·千亿顶流回归投研一线</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-19</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报9月19日报道：景顺长城基金9月19日发布高级管理人员变更公告，<b>刘彦春因工作调整自9月18日起卸任副总经理</b>，卸任后将专注于投资管理工作，继续担任基金经理。Wind数据显示，截至二季度末刘彦春在管基金共<b>6只</b>、合计规模<b>240.49亿元</b>，其中<b>4只共管、2只独管</b>，独管规模已降至<b>124.50亿元</b>。<br>
          <b>提前铺垫：</b>今年5月起其管理的景顺长城鼎益、内需增长、内需增长贰号三只旗舰产品已陆续增聘基金经理（柯海东、徐亦达等）搭建双人共管机制，6月景顺长城集英成长两年定开增聘孟棋；半年报显示共管后的产品已开始涉足科技方向，光纤光缆、工业气体、半导体设备等标的进入持有范围。<br>
          <b>人物背景：</b>刘彦春拥有23年证券基金从业经验、公募基金经理任职时长超17年，2015年加入景顺长城，2021年升任副总经理，同年管理规模一度突破千亿元，代表作景顺长城新兴成长混合从2015年4月接手至2020年末任职回报率超280%。<br>
          <b>行业趋势：</b>自2024年以来，万家基金黄海、乔亮，信达澳亚基金冯明远，易方达张坤、陈皓、萧楠、张清华，诺安基金杨谷，长盛基金郭堃，广发基金傅友兴，鹏扬基金朱国庆等高管级基金经理相继卸任副总，形成<b>“投而优则仕”向“卸仕归投”的反向切换</b>。<br>
          <b>对腾安启示：</b>顶流经理卸任行政职务回归投研，对代销端是正向信号——产品页应同步更新“基金经理在管结构”（独管/共管）与经理精力投入说明，避免客户仅凭历史名气判断；对共管类产品须明示新增经理的风格差异，防止“挂名旗舰、实际换人”引发预期落差。
        </div>
        <div class="card-footer">
          <a href="https://jnzstatic.cs.com.cn/zzb/htmlInfo/133667.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·09-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 2 (09-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 首批摊余成本债基7只定档9月21日发行·两批28只最高2240亿·中小公募政策红利落地</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-19</span>
          </div>
        </div>
        <div class="card-body">
          同花顺财经9月19日报道：截至9月19日，9月14日获批的首批15只摊余成本法债基中已有<b>7只定档发行</b>——国融聚达、贝莱德稳利、兴华安硕、财信聚鑫、红土创新瑞泽、路博迈安瑞6只均于<b>9月21日</b>起售，鹏安安瑞于<b>9月22日</b>起售，<b>单只募集上限统一为80亿元</b>，管理费年费率<b>0.15%</b>、托管费<b>0.05%</b>。<br>
          <b>规模测算：</b>按80亿元上限测算，首批15只可形成<b>1200亿元</b>基金净资产，参考现有摊余债基约138%—140%的平均杠杆水平，预计形成约<b>1500亿元</b>有效配置需求；叠加9月11日上报的第二批13只（可形成1040亿元净资产），<b>两批28只产品最高募集规模达2240亿元</b>。以0.15%管理费率计，单只产品每年对应管理费收入<b>1200万元</b>。<br>
          <b>政策脉络：</b>本轮支持中小基金公司健康发展的政策产品共三类——摊余成本债基、科创债指数基金、股债恒定指数基金，其中摊余成本债基规模确定性最高。28家申报机构全为中小公募，涵盖个人系12家（汇泉、百嘉、东方阿尔法、泉果等）、外资系4家（贝莱德、路博迈等）、券商系5家（国融、东财等）；首批15家管理规模均在300亿元以下，其中12家不足100亿元、9家不足50亿元。<br>
          <b>债市影响：</b>63个月封闭期对应建仓久期在5年附近，摊余成本法要求持仓通过SPPI测试，普通信用债、券商次级债、TLAC债为主要标的，边际利好中等久期信用债；机构提示需求将在产品发行与建仓过程中逐步释放，而非一次性冲击。<br>
          <b>对腾安启示：</b>80亿上限×28只的确定性供给，是四季度低波固收货架最可预期的增量来源；但63个月封闭期意味着客户资金锁定5年以上，销售端须把封闭期、估值方法与流动性代价前置到购买页首屏，按“底仓替代”而非“灵活理财”定位推荐，并对同批产品的费率差（0.15%与0.3%）做透明排序。
        </div>
        <div class="card-footer">
          <a href="https://m.10jqka.com.cn/20260919/c680081871.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·09-19</span></a>
          <a href="https://cfi.cn/p20260918001450.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">基金公告·09-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 3 (09-20 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 姜晓丽正式掌舵易方达悦和稳健·14年固收老将结束7个月过渡期</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-20</span>
          </div>
        </div>
        <div class="card-body">
          新浪财经9月20日报道：9月19日易方达基金发布基金经理变更公告，<b>增聘姜晓丽为易方达悦和稳健债券型证券投资基金（018898/018899）基金经理</b>，原基金经理林虎同日因工作需要离任。<br>
          <b>产品画像：</b>该基金成立于2024年2月19日，为债券型-混合二级基金、中低风险定位；截至2026年6月30日，A类份额规模<b>24.06亿元</b>、C类<b>13.60亿元</b>，合计约<b>37.65亿元</b>；截至2026年9月18日，A类单位净值<b>1.1224元</b>、C类<b>1.1111元</b>；成立以来回报率<b>12.24%</b>，在同类987只产品中排名第501位。林虎离任后仍管理易方达瑞富I、瑞祥A、磐泰一年持有A、悦诚6个月持有A四只产品。<br>
          <b>过渡时间线：</b>今年2月姜晓丽在告别天弘基金的公开信中表示“从来没有休过长假”，决定彻底给自己放个假；2月9日离任天弘，4月2日基金业协会公示其从业机构变更为易方达基金，9月正式接管产品，前后7个月完成过渡。她拥有<b>17年</b>证券从业经验、基金经理年限近<b>14年</b>，是兼具宏观研究背景与固收实操经验的经理，曾被誉为“固收一姐”。<br>
          <b>对腾安启示：</b>明星固收经理“跳槽—过渡—接管”已形成可跟踪的公开链路（协会从业公示→公告增聘→接管产品），代销端可据此建立经理变更预警：在增聘公告日至正式接管窗口内，产品页应对“拟任经理风格/历史回撤/权益仓位上限”做前置披露，避免客户按原经理的历史业绩做出申购决策。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/money/fund/original/2026-09-20/doc-inismvph6842282.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-20</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 4 (09-19 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">\U0001F535 新基金募集冷热分化·汇添富航天航空ETF提前结募·多只产品密集调整募集期</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-19</span>
          </div>
        </div>
        <div class="card-body">
          财经网9月19日报道：汇添富基金公告，<b>汇添富国证航天航空行业ETF（158030）</b>于9月7日启动募集、原定9月23日截止，为保障基金平稳运作决定<b>提前结束募集</b>，认购截止日调整为<b>9月18日</b>，自9月19日起不再接受认购申请；基金设置<b>50亿元</b>募集规模上限，若有效认购超出上限将启动<b>末日比例确认</b>。<br>
          <b>同日调整：</b>景顺长城和熙恒益三个月持有期混合FOF（A类027101、C类027102）原定9月24日截止，提前至<b>9月21日</b>，自9月22日起不再接受认购；华泰柏瑞中证工业有色金属主题ETF联接基金原定募集期9月8日至9月30日，募集截止日提前至<b>9月29日</b>。<br>
          <b>冷热并存：</b>提前结募集中在航天航空、工业有色等有明确产业叙事的主题，以及偏债混合、FOF等低波品种；与此同时被动指数型基金仍是延期“重灾区”，被动指数、混合FOF、偏股混合、增强指数等多个品种均有产品延长募集，发行市场整体仍处于磨底阶段。<br>
          <b>对腾安启示：</b>同一时点上“提前结募”与“延长募集”并存，说明客户认购意愿高度依赖主题叙事清晰度而非发行时点；首页应把“末日比例确认/提前结募”产品做成明确的倒计时与配售规则提示，避免客户在截止日误判确认比例，同时把延募产品的原因（主题热度、渠道节奏）做成可查询标签，降低“延募=产品差”的误读。
        </div>
        <div class="card-footer">
          <a href="https://m.caijing.com.cn/article/202609/445246" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财经网·09-19</span></a>
          <a href="https://news.qq.com/rain/a/20260920A053V400" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·09-20</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>
    </div>
  </div>
'''

i0 = s.find(A_S0)
i1 = s.find(A_S1)
assert i0 > 0 and i1 > i0
s = s[:i0] + S0_NEW + s[i1:]
print('[ok] S0')
dr('S0')

# ============ 6. S1 删旧 + 补新 ============
s = drop_card(s, '首批10只科创债场外指数基金上报')
s = drop_card(s, '单周82只新基启动发行创历史纪录')

S1_NEW_A = '''
      <!-- S1 Card: 大成基金多重考验 (09-20 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-20</span>
          </div>
          <div class="card-title">\U0001F7E1 大成基金遭多重考验·韩创在管产品全线增聘或奔私·建滔系高位接盘引质疑</div>
        </div>
        <div class="card-body">
          东方财富网9月20日刊发界面新闻（记者杜萌）报道：9月18日大成基金韩创在管的5只基金集体发布增聘公告——大成产业趋势增聘徐雄晖、大成景气精选六个月持有增聘杜聪、大成聚优成长增聘戴军、大成新锐产业增聘齐炜中、大成创优鑫选增聘柏杨；叠加此前大成核心趋势（2025年12月）、大成国企改革（3月）、大成睿景（7月）的陆续增聘，<b>韩创名下已无单独管理的基金</b>。记者从业内了解到，韩创近期或将离开大成基金，下一站转战私募；截至二季度末其<b>在管公募总规模109.16亿元</b>，较一季度末的207.76亿元近乎腰斩。<br>
          <b>业绩失速：</b>韩创2015年加入大成，2021年以大成新锐产业88.25%的收益摘得主动偏股混合型基金冠军，大成国企改革、大成睿景当年分别达94.76%、84.19%；今年多只产品进入逆风期，二季度大成国企改革回报-13.1%、大成新锐产业-20.84%、大成聚优成长-24.62%。截至9月17日，大成科技创新A/C近三个月回报率分别为<b>-32.13%、-32.2%</b>。<br>
          <b>建滔系质疑：</b>大成科技创新混合二季度重仓新增建滔积层板（01888.HK）与建滔集团（00148.HK），合计公允价值<b>37.14亿元</b>，分别占基金净值8.36%、6.51%，合计14.87%；两标的上半年涨幅一度达658%、308%，但6月大股东高位配售与减持合计套现超200亿港元，7月2日至8月31日两只标的收盘价分别下跌<b>44.65%、47.12%</b>，建仓时点与减持时点的重合引发“高位接盘”质疑。<br>
          <b>公司层面：</b>9月2日副总经理姚余栋因个人原因离任；公司权益“三剑客”徐彦、刘旭、韩创今年业绩集体承压，三人合计管理规模一度占公司权益类总规模的55%，明星依赖症突出；截至2026年6月末公司管理规模约5166亿元，行业排名已由2009年末的第7位滑落至第27位。<br>
          <b>对腾安启示：</b>人事变动与重仓股集中度风险都会直接冲击持有体验，代销端应建立“全线增聘即预警”的监控规则，对出现集中增聘的产品及时提示投资框架可能生变；同时对单一实控人旗下多只标的合计持仓接近净值15%的产品加挂集中度提示，避免客户按单只股票口径低估风险。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://finance.eastmoney.com/a/202609203879316471.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">界面新闻·东方财富·09-20</span></a>
          <a href="https://m.10jqka.com.cn/20260918/c680071365.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·同花顺·09-18</span></a>
        </div>
      </div>

      <!-- S1 Card: ETF资金向科技成长切换 (09-20 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-20</span>
          </div>
          <div class="card-title">\U0001F535 东吴证券金融产品周报·ETF资金向科技成长切换·半导体材料设备规模增74.43亿</div>
        </div>
        <div class="card-body">
          东吴证券9月20日金融产品周报（研究员芦哲、唐遥衎）统计：本周权益类ETF中，基金规模增长排名前三的类型为主题指数ETF<b>353.37亿元</b>、规模指数ETF<b>285.03亿元</b>、跨境规模指数ETF<b>48.12亿元</b>；后三名为行业指数ETF<b>-32.25亿元</b>、策略指数ETF<b>-17.01亿元</b>、跨境策略指数ETF<b>-13.33亿元</b>。<br>
          <b>指数维度：</b>规模增长前三的跟踪指数为半导体材料设备<b>74.43亿元</b>、中证500<b>71.31亿元</b>、科创半导体材料设备<b>67.40亿元</b>；后三名是有色金属-9.71亿元、证券公司-9.63亿元、港股通互联网-9.23亿元。份额增长前三为创业板算力<b>16.80亿份</b>、恒生科技<b>15.75亿份</b>、恒生互联网科技业<b>11.78亿份</b>；后三名为科创50<b>-28.46亿份</b>、半导体材料设备-20.46亿份、科创芯片-14.23亿份。<br>
          <b>信号解读：</b>规模增长与份额增长出现背离——半导体方向规模增长居前但份额净减，反映净值上涨驱动为主、部分资金逢高减持；创业板算力、恒生科技则规模与份额同步增长，属真金白银净申购。技术择时方面，科创50、科创综指、万得双创触发局部底右侧信号，红利指数触发局部顶信号，成长方向信号强于红利。<br>
          <b>宏观背景：</b>美联储时隔三年多重启加息25个基点、联邦基金利率区间升至3.75%—4.00%，主席沃什称通胀过高且持续太久、市场认为紧缩路径尚未结束；日本央行加息至1.25%为31年高位，英国央行按兵不动但警告中东战事持续或被迫加息。<br>
          <b>对腾安启示：</b>ETF资金已明确向科技成长切换，但“规模增、份额减”的背离提示部分涨幅由净值驱动而非新增申购；主题页应按“规模变化+份额变化”双维度展示资金流向，避免客户把净值上涨误读为资金一致看多，同时对触发局部顶信号的红利类资产给出回调风险提示。
        </div>
        <div class="card-footer">
          <span class="impact-tag low">影响：中</span>
          <a href="https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/843178383192/index.phtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东吴证券·新浪财经·09-20</span></a>
        </div>
      </div>
'''
i2 = s.find(A_S2)
assert i2 > 0
s = s[:i2] + S1_NEW_A + s[i2:]
print('[ok] S1')
dr('S1')

# ============ 7. S2 删旧 + 补新 ============
s = drop_card(s, '证监会就私募基金募集监督管理办法征求意见')

S2_NEW = '''
      <!-- S2 Card: 证监会公示吹哨人奖励名单 (09-18 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-18</span>
          </div>
          <div class="card-title">\U0001F534 证监会公示首批“吹哨人”奖励名单·17起案件·重大线索单笔上限100万元</div>
        </div>
        <div class="card-body">
          中国经济网9月19日报道（记者田鹏）：据证监会官网9月18日消息，证监会拟对<b>17起证券期货违法案件线索的“吹哨人”予以奖励</b>。这是2026年1月9日新版《证券期货违法行为“吹哨人”奖励工作规定》施行后，监管层<b>首次公示拟奖励名单并启动申领</b>，标志升级后的资本市场“吹哨人”制度进入实操阶段。<br>
          <b>奖励力度：</b>新规较2014年《举报工作暂行规定》核心变化包括——奖励比例由罚没款金额的<b>1%提升至3%</b>；可奖励案件的罚没款门槛由10万元提升至<b>100万元</b>；重大违法行为线索奖金上限由10万元提升至<b>50万元</b>；在全国有重大影响、涉案数额特别巨大或举报人为内部知情人员的，每案奖金上限统一提升至<b>100万元</b>。<br>
          <b>案件结构：</b>17起线索涵盖<b>五大类</b>——上市公司信息披露违法违规（沈阳远大智能、新疆冠农、海南大东海、吉林利源精制、吉林华微电子、山东未名生物医药、深圳中青宝、山东墨龙、北京赢鼎教育等）、内幕交易（林某鹏、夏某秀内幕交易成都华神科技股票案）、中介机构未勤勉尽责（天职国际在江西奇信年报审计中未勤勉尽责并伪造篡改毁损审计底稿）、<b>私募基金违规3起</b>（利得资本、宜华企业与汕头宜华投资、广东华迪投资违反私募法规）、非法证券活动2起（永州龙腾投资非法经营证券业务、王政源非法经营证券投资咨询）。<br>
          <b>申领安排：</b>中国证券投资者保护基金有限责任公司协助办理，登记周期为<b>2026年9月18日至12月18日</b>，逾期未按要求登记确认视为放弃奖励；匿名举报人申领需补充实名信息与证明材料，属内部知情人员须提交身份证明材料，否则按一般“吹哨人”标准奖励。<br>
          <b>对腾安启示：</b>私募违规线索已被纳入有奖举报的重点打击范围，代销端须把合作私募的信息披露真实性、实控人一致性、投资管理职责是否外包等做成可核查留痕项；同时建立内部举报与线索上报通道，对发现的合作方违规线索主动留存证据并依规报送，避免被动卷入。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">影响：高</span>
          <a href="https://finance.ce.cn/stock/gsgdbd/202609/t20260919_3224197.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·09-19</span></a>
          <a href="https://news.qq.com/rain/a/20260918A0AU9E00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">21世纪经济报道·腾讯新闻·09-18</span></a>
        </div>
      </div>
'''
i3 = s.find(A_S3)
assert i3 > 0
s = s[:i3] + S2_NEW + s[i3:]
print('[ok] S2')
dr('S2')

# ============ 8. S6 整段替换 ============
S6_NEW = '''<!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">\U0001F4CA</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

            <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 上一交易日收盘（2026-09-18）·沪指3911.87 +0.94%·两市成交2.08万亿放量2540亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-18</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-18收盘·放量普涨）</b><br>
              上证指数 <b>3911.87</b> <span style="color:#dc2626;">+0.94%</span><br>
              深证成指 <b>13640.87</b> <span style="color:#dc2626;">+1.72%</span><br>
              创业板指 <b>3372.68</b> <span style="color:#dc2626;">+2.25%</span><br>
              科创综指 <b>1948.21</b> <span style="color:#dc2626;">+3.23%</span><br>
              科创50 <span style="color:#dc2626;">+2.88%</span><br>
              沪深两市成交 <b>2.08万亿</b>·较上日放量约2540亿<br>
              全市场4234只上涨、1152只下跌·79只涨停
            </div>
            <div>
              <b>港股与美股（09-18收盘）</b><br>
              恒生指数 <b>24750.78</b> <span style="color:#dc2626;">+0.60%</span><br>
              恒生科技 <b>4405.50</b> <span style="color:#dc2626;">+2.20%</span><br>
              国企指数 <b>8225.40</b> <span style="color:#dc2626;">+0.61%</span><br>
              道琼斯 <b>51682.64</b> <span style="color:#52c41a;">-0.18%</span><br>
              纳斯达克 <b>26522.55</b> <span style="color:#dc2626;">+0.39%</span><br>
              标普500 <b>7650.50</b> <span style="color:#dc2626;">+0.17%</span><br>
              布伦特原油103.90美元 <span style="color:#52c41a;">-0.91%</span>·现货黄金4378.23美元 <span style="color:#dc2626;">+0.84%</span>·美债10年期升至4.998%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>放量反弹、科技领涨——申万一级行业中27个行业上涨，<b>房地产板块涨3.38%领涨</b>（万科A、世联行、绿地控股涨停），电子涨<b>2.95%</b>、通信涨<b>2.62%</b>分列二三；煤炭、银行、建筑材料收跌。半导体行业主力资金净流入约<b>182.2亿元</b>居首，全市场ETF成交4707.5亿元、超1550只ETF收涨，地产ETF华宝涨5.79%居首、豆粕ETF华夏跌3.12%垫底。海外方面，9月18日恰逢“三重巫日”，美股成交额急剧放大、三大指数涨跌互现，费城半导体指数涨<b>2.78%</b>，闪迪涨10.99%、美光涨近4%、AMD与SK海力士均涨超2%，META跌2.43%；美联储9月加息25个基点至3.75%—4.00%后进入消化整固期，日本央行加息至1.25%、英国央行按兵不动；沙特受损输油管道有望部分恢复输送，布伦特原油三连跌至103.90美元，避险需求回落但金价仍涨0.84%。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">同花顺iFind·2026-09-18收盘</span>
          <span class="source-tag">数据来源：中新经纬、证券日报、上海证券报/中国证券网、国际金融报（09-18—09-20）</span>
        </div>
      </div>  </div>
'''
i0 = s.find(A_S6)
i1 = s.find(A_S7)
assert i0 > 0 and i1 > i0
s = s[:i0] + S6_NEW + s[i1:]
print('[ok] S6')
dr('S6')

# ============ 9. S7 重写 ============
def ti(dot, d, t):
    return ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot %s"></div>\n'
            '        <div class="timeline-date">%s</div>\n'
            '        <div class="timeline-title">%s</div>\n'
            '      </div>\n' % (dot, d, t))

S7_ITEMS = [
    ('blue', '2026-09-20', '姜晓丽掌舵易方达悦和稳健'),
    ('blue', '2026-09-19', '刘彦春卸任景顺长城副总'),
    ('blue', '2026-09-19', '7只摊余债基定档发行'),
    ('blue', '2026-09-19', '汇添富航天航空ETF提前结募'),
    ('blue', '2026-09-18', '8月末公募规模39.63万亿'),
    ('red',  '2026-09-18', '证监会公示吹哨人奖励名单'),
    ('blue', '2026-09-18', '韩创5只产品集中增聘'),
    ('blue', '2026-09-18', 'A股放量反弹沪指站上3900'),
    ('red',  '2026-09-17', '年内新发基金规模破8000亿'),
    ('blue', '2026-09-17', '公募逆势布局冷门赛道'),
    ('blue', '2026-09-17', '次新基金快速建仓·机构调研'),
    ('blue', '2026-09-17', '公募密集调整QDII申购限额'),
]
S7_BODY = ''.join(ti(a, b, c) for a, b, c in S7_ITEMS)

S7_NEW = '''<!-- ============ Section 7: 关键时间线 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--primary-light);color:var(--primary);">\U0001F4C5</div>
      <span class="section-title">关键时间线（近两周）</span>
      <span class="section-badge" style="background:var(--primary-light);color:var(--primary);">事件脉络</span>
    </div>

    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">
''' + S7_BODY + '''    </div>

  </div>

</div>

'''
i0 = s.find(A_S7)
i1 = s.find(A_BODY)
assert i0 > 0 and i1 > i0
s = s[:i0] + S7_NEW + s[i1:]
print('[ok] S7')
dr('S7')

# ============ Phase1 全断言 ============
new_open = len(re.findall(r'<div\b', s))
new_close = s.count('</div>')
print('div open/close: %d/%d -> %d/%d (drift open %+d, close %+d)'
      % (orig_open, orig_close, new_open, new_close,
         new_open - orig_open, new_close - orig_close))
assert new_open == new_close, 'div unbalanced'
assert new_open - orig_open == -3, 'unexpected open drift'
assert new_close - orig_close == -3, 'unexpected close drift'

assert s.count('</div>>') == 0, 'stray > found'
assert 'Section 8' not in s and '待办跟踪' not in s and '腾安行动清单' not in s
assert '\ufffd' not in s

# S0 段校验
i0 = s.find(A_S0); i1 = s.find(A_S1)
seg0 = s[i0:i1]
assert seg0.count('<div class="card p') == 4, 'S0 cards=%d' % seg0.count('<div class="card p')
assert seg0.count('class="action-box"') == 0, 'S0 should have no action-box'
assert re.search(r'<span class="section-title">今日焦点</span>', seg0), 'title wrong'
assert '9月20日 · 4条今日要闻' in seg0, 'context wrong'
assert seg0.count('class="card-meta"') == 4
assert seg0.count('target="_blank"') == 6, 'S0 links=%d' % seg0.count('target="_blank"')
d09_19 = len(re.findall(r'date-tag">09-19<', seg0))
d09_20 = len(re.findall(r'date-tag">09-20<', seg0))
assert d09_19 == 3 and d09_20 == 1, 'S0 dates 09-19=%d 09-20=%d' % (d09_19, d09_20)
assert len(re.findall(r'date-tag">09-1[0-8]<', seg0)) == 0, 'S0 has stale date'

# S1 / S2 段校验
i1 = s.find(A_S1); i2 = s.find(A_S2); i3 = s.find(A_S3)
seg1 = s[i1:i2]; seg2 = s[i2:i3]
assert seg1.count('<div class="card p') == 6, 'S1 cards=%d' % seg1.count('<div class="card p')
assert seg2.count('<div class="card p') == 4, 'S2 cards=%d' % seg2.count('<div class="card p')
for nm, seg in (('S1', seg1), ('S2', seg2)):
    for m in re.finditer(r'class="date-tag">(\d{2})-(\d{2})<', seg):
        d = date(2026, int(m.group(1)), int(m.group(2)))
        assert d >= CUTOFF, '%s stale date %s' % (nm, m.group(0))

# S7 段校验
i6 = s.find(A_S7); i7 = s.find(A_BODY)
seg7 = s[i6:i7]
items = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>\s*\n\s*<div class="timeline-title">(.*?)</div>', seg7)
assert len(items) == 12, 'S7 items=%d' % len(items)
prev = None
for d, t in items:
    dd = date(*map(int, d.split('-')))
    assert CUTOFF <= dd <= TODAY, 'S7 out of window: ' + d
    assert len(t) <= 25, 'S7 title too long(%d): %s' % (len(t), t)
    if prev is not None:
        assert dd <= prev, 'S7 not descending'
    prev = dd
assert seg7.count('timeline-desc') == 0

# 黑名单（全文件）
BAD = ['stcn', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com',
       'toutiao', 'so.html5.qq.com', '163.com/dy', 'cqcb.com', 'weibo.com', 'k.sina.com.cn']
for b in BAD:
    assert b not in s, 'blacklist hit: ' + b

# S6 校验
i4 = s.find(A_S6); i5 = s.find(A_S7)
seg6 = s[i4:i5]
assert '3911.87' in seg6 and '09-18' in seg6 and '3875.60' not in seg6

print('[ok] all assertions passed')
open(SRC, 'w', encoding='utf-8', newline='').write(s)
print('[written] index.html')
