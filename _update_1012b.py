# -*- coding: utf-8 -*-
import re, io
from datetime import date, timedelta

P = r'c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html'
src = open(P, encoding='utf-8').read()
LOG = io.StringIO()
def log(*a):
    LOG.write(' '.join(str(x) for x in a) + '\n')

def dr(tag):
    o = len(re.findall(r'<div\b', src)); c = len(re.findall(r'</div>', src))
    log('   [%s] open=%d close=%d' % (tag, o, c))
    return o, c

o0, c0 = dr('baseline')

TODAY = date(2026, 10, 12)
CUT = TODAY - timedelta(days=14)
EMO_CAL = '\U0001F4C5'
BADGE = EMO_CAL + ' 数据区间：%s — %s（每日更新）' % (
    CUT.strftime('%Y.%m.%d'), TODAY.strftime('%Y.%m.%d'))

EMO_RED = '\U0001F534'
EMO_YEL = '\U0001F7E1'
EMO_UP = '\U0001F4C8'
BOLT = '⚡'

# ---------------- Phase 0 锚点预检 ----------------
assert src.count('<!-- daily-update: ') == 1
assert src.count('class="section-context"') == 1
assert '<div class="stats-bar">' in src
assert src.count('Section 0') == 1 and src.count('Section 1') == 1
assert src.count('Section 6') == 1 and src.count('Section 7') == 1
assert 'S8' not in src
log('Phase0 anchors OK')

# ---------------- Step 1 marker / fingerprint / description ----------------
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
             '<!-- daily-update: 2026-10-12 -->', src, count=1)
assert src.count('<!-- daily-update: 2026-10-12 -->') == 1

FP = '公募基金|本周64只|ETF资金|红利基金'
src = re.sub(r'<meta name="content-fingerprint" content="[^"]*">',
             '<meta name="content-fingerprint" content="%s">' % FP, src, count=1)
assert src.count('content-fingerprint') == 1

DESC = ('公募基金运作办法迎12年来大修|本周64只新基金集中开售|ETF资金加码科创主线'
        '|红利基金掀起限购潮|沪指10-09收3813.79')
src = re.sub(r'<meta name="description" content="[^"]*">',
             '<meta name="description" content="%s">' % DESC, src, count=1)
assert src.count('name="description"') == 1
log('Step1 marker/fp/desc done')

# ---------------- Step 2 header badge ----------------
pat = re.escape(EMO_CAL) + r' 数据区间：\d{4}\.\d{2}\.\d{2}\s*—\s*\d{4}\.\d{2}\.\d{2}（每日更新）'
src, n = re.subn(pat, BADGE, src, count=1)
assert n == 1, 'badge not replaced'
assert BADGE in src
log('Step2 badge -> ' + BADGE)

# ---------------- Step 3 S0 section-context ----------------
old_ctx = '<span class="section-context">10月9日 · 4条今日要闻</span>'
new_ctx = '<span class="section-context">10月12日 · 4条今日要闻</span>'
assert src.count(old_ctx) == 1
src = src.replace(old_ctx, new_ctx)
log('Step3 context done')

# ---------------- Step 4 Stats Bar 沪指卡 ----------------
OLD_NUM = '<div class="stat-number">3811.90</div>'
OLD_LBL = '<div class="stat-label">沪指10-08收盘·跌0.79%·沪深北三市成交1.69万亿·节后首日回落</div>'
OLD_CHG = '<div class="stat-change down">▼ 沪深两市1698涨3748跌·科创综指跌4.55%</div>'
NEW_NUM = '<div class="stat-number">3813.79</div>'
NEW_LBL = '<div class="stat-label">沪指10-09收盘·涨0.05%·沪深北三市成交1.92万亿·放量2224亿</div>'
NEW_CHG = '<div class="stat-change up">▲ 深V反弹·3297只上涨·传媒板块涨5.28%</div>'
for o_ in (OLD_NUM, OLD_LBL, OLD_CHG):
    assert src.count(o_) == 1, o_
src = src.replace(OLD_NUM, NEW_NUM).replace(OLD_LBL, NEW_LBL).replace(OLD_CHG, NEW_CHG)
sb = src[src.find('<div class="stats-bar">'):src.find('<div class="main">')]
assert '3813.79' in sb and '3811.90' not in sb and '10-09收盘' in sb
log('Step4 stats bar done')

# ---------------- Step 5 S0 四卡整块替换 ----------------
S0_START = src.find('<!-- S0 Card 1')
S1_ANCHOR = '<!-- ============ Section 1: 重磅信息 ============ -->'
S0_END = src.find(S1_ANCHOR)
assert S0_START > 0 and S0_END > S0_START
old_s0 = src[S0_START:S0_END]
log('   old S0 open=%d close=%d' % (len(re.findall(r'<div\b', old_s0)),
                                    len(re.findall(r'</div>', old_s0))))

C1 = '''<!-- S0 Card 1 (10-09 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">''' + EMO_RED + ''' 公募基金运作办法迎12年来大修·权益类与FOF成立门槛降至5000万</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">10-09</span>
          </div>
        </div>
        <div class="card-body">
          中国证监会10月9日就《公开募集证券投资基金运作管理办法（征求意见稿）》及配套规则公开征求意见，意见反馈截止时间为<b>2026年11月8日</b>。这是现行运作办法自2014年修订发布后、时隔<b>12年</b>再次启动的系统性修订；一并征求意见的还有《关于实施〈公开募集证券投资基金运作管理办法〉有关问题的规定》与《证券投资基金信息披露内容与格式准则第6号〈基金合同的内容与格式〉》。<br>
          <b>成立门槛下调：</b>股票基金、混合基金、基金中基金（FOF）等的成立门槛，从规模<b>2亿元</b>、份额<b>2亿份</b>分别降低至<b>5000万元</b>、<b>5000万份</b>，固收类基金成立门槛维持不变；同时删除发起式基金成立满3年规模未达到2亿元即强制清盘的特殊规定。<br>
          <b>投资运作松绑：</b>非FOF基金投资其他基金的比例上限从<b>10%</b>提高至<b>30%</b>；对完全复制指数的被动指数基金触发收购举牌、短线交易、减持限制等规定作出适度豁免，并适度放松其他指数类基金的交易限制。<br>
          <b>行为约束加码：</b>办法压实基金管理人投资运作主体责任，要求强化基金产品<b>逆周期布局</b>管理、加强投资风格稳定性管理并强化业绩比较基准约束，要求行业主题基金清晰界定基金名称所示投资方向、非行业主题基金坚持分散投资原则；增强混合基金权益仓位稳定性，要求明确约定各类资产配置比例。<br>
          <b>过渡安排：</b>办法设置<b>1年过渡期</b>，原基金合同不符合办法及配套规则规定的，允许基金管理人、基金托管人在过渡期内根据基金合同约定协商一致后修改基金合同并公告。<br>
          <b>对腾安启示：</b>成立门槛下调后权益类与FOF新品供给将明显扩容，货架筛选维度必须从"首发规模"切换为"权益仓位中枢＋业绩比较基准约束＋最大回撤"；同时须把"发起式基金"识别标签与满3年规模不足2亿元的清盘风险提示前置，避免用户把低门槛新品误读为低风险产品。
        </div>
        <div class="card-footer">
          <a href="https://www.csrc.gov.cn/csrc/c101981/c7663407/content.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证监会官网·10-09</span></a>
          <a href="https://www.cnstock.com/commonDetail/800227" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·10-10</span></a>
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202610/t20261010_3252949.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·中国证券报·10-10</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">''' + BOLT + ''' 腾安行动建议</div>
          <div class="action-text">
            ① 货架规则→新增"发起式基金"识别标签与满3年规模不足2亿元的清盘风险提示，在文案上把"低门槛成立"与"低风险"明确切割；<br>
            ② 选品框架→把业绩比较基准与权益仓位中枢提升到与近一年收益同等位置，防范风格漂移与"宽基窄投"类产品进入稳健客群货架；<br>
            ③ 政策跟踪→意见反馈截止2026年11月8日，跟踪正式稿与1年过渡期安排，提前梳理存量代销基金合同中需协商修改的条款。
          </div>
        </div>
      </div>
'''

C2 = '''<!-- S0 Card 2 (10-12 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + EMO_YEL + ''' 本周64只新基金集中开售·4只北交所3个月持有期产品同日启动</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-12</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报10月12日报道（记者张玲）：本周（10月12日至10月16日）公募基金市场共有<b>64只</b>新基金开售（仅统计初始基金），权益类仍占多数——混合型<b>20只</b>、股票型<b>19只</b>，FOF、债券型基金、REITs分别为<b>16只</b>、<b>7只</b>、<b>2只</b>。<br>
          <b>主动权益：</b>共<b>20只</b>，红土创新领航智选、大成智选量化选股均设置<b>50亿份</b>认购上限；认购天数上天弘消费新机遇优选最短为5天，泉果新能源机遇为12天且未设置募集上限（拟任基金经理赵诣）。<br>
          <b>北交所主题：</b>南方北交所3个月持有、嘉实北交所3个月持有、汇添富北交所精选3个月持有、华夏北交所优选3个月持有等<b>4只</b>产品均于本周一（10月12日）开启发行，认购上限均为<b>5亿份</b>。<br>
          <b>被动与"固收+"：</b>被动指数产品覆盖工程机械、银行、稀有金属、电池及红利策略，平均认购天数14天，其中12只设置募集上限，大成中证银行ETF上限最高为<b>80亿份</b>；本周<b>7只</b>"固收+"产品开启认购，平均认购天数28天，国联晟元、泰康裕享认购上限均为30亿份；FOF方面本周开启募集的均为混合型FOF，平均认购天数约16天，建信泓盛多元配置3个月持有、招商智通优选3个月持有认购上限均为60亿份。<br>
          <b>REITs：</b>平安西安高科产业园REIT、长城华能燃煤发电REIT本周发售，认购天数分别为7天、2天；后者为长城基金旗下首只公募REIT，认购价格<b>3.198元/份</b>，产品存续期27年，后续将在上交所上市交易。<br>
          <b>对腾安启示：</b>节后发行高峰叠加北交所3个月持有期产品集中启动，货架须按"认购起始日＋锁定条款＋募集上限"三维排序，并把持有期、认购上限与预计结募日前置到产品页，避免用户把"募集上限高"误读为"额度充足"。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR8fac703b-928e-05a0-f703-3a243ff3cc32" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·10-12</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C3 = '''<!-- S0 Card 3 (10-12 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + EMO_YEL + ''' ETF资金加码科创主线·科创50ETF华夏近5日净流入125.14亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-12</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇10月12日ETF资金流观察：近5日资金持续加码科创主线，科创50ETF华夏以<b>125.14亿元</b>净流入遥遥领先，是区间最核心的资金主攻标的。固收类产品资金吸引力突出，短融ETF海富通净流入<b>89.55亿元</b>，体量仅次于科创50ETF华夏。权益端，创业板ETF易方达净流入<b>63.90亿元</b>，银华日利ETF净流入<b>60.48亿元</b>，中证1000ETF南方净流入<b>41.78亿元</b>。<br>
          拉长至20日维度（格隆汇10月12日经由新浪财经发布）：科创50ETF华夏区间净流入<b>170.71亿元</b>保持最强资金吸纳能力；固收方面科创债ETF嘉实净流入<b>113.88亿元</b>、短融ETF海富通<b>91.52亿元</b>、科创债ETF易方达<b>70.72亿元</b>；权益端创业板ETF易方达净流入<b>67.63亿元</b>、沪深300ETF华泰柏瑞净流入<b>57.30亿元</b>，整体呈现"固收打底＋权益宽基加仓"特征。<br>
          <b>对腾安启示：</b>资金在"科创宽基＋短久期固收"两端同时加仓，货架须把ETF的区间资金流与跟踪指数并列展示，并显著标注"区间净流入不代表未来收益"；对短融、科创债等固收ETF要同步提示久期与信用风险，不得只用近一年收益率排序。
        </div>
        <div class="card-footer">
          <a href="https://www.gelonghui.com/live/2705779" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·10-12</span></a>
          <a href="https://finance.sina.com.cn/stock/bxjj/2026-10-12/doc-iniuxrzn0402483.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·格隆汇·10-12</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C4 = '''<!-- S0 Card 4 (10-12 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + EMO_YEL + ''' 红利基金掀起限购潮·银河交银景顺长城单日申购限额降至100万</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-12</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报10月12日报道（记者王彭）：国庆节过后红利基金掀起一轮"限购潮"。10月9日，银河基金公告将旗下银河中证红利低波动100指数、银河上证国有企业红利ETF发起式联接基金的单日申购限额设定为<b>100万元</b>，自10月13日起恢复办理大额申购、定期定额投资及转换转入业务；同日，交银中证红利低波动100指数与景顺长城中证沪港深红利成长低波动指数基金也将单日申购限额设定为<b>100万元</b>；招商中证红利ETF联接基金则对非个人投资者实施单日<b>10万元</b>限额，自10月15日起恢复大额申购和转换转入业务。<br>
          <b>新品端：</b>10月8日路博迈基金公告旗下路博迈红利量化选股股票基金提前结束募集（原定募集截止日为10月16日）；10月12日博时恒生港股通红利低波动ETF、银华中证全指红利质量ETF、广发中证红利低波动ETF同步启动发行，三只产品均计划在10月中下旬结束募集。申报端，10月8日嘉实基金提交嘉实中证全指红利质量ETF募集申请，9月30日汇添富基金提交汇添富中证全指红利质量ETF募集申请，9月29日工银瑞信、万家、易方达、南方、富国等多家基金公司分别提交中证红利增长ETF募集申请。<br>
          <b>风格切换：</b>Choice数据显示，今年上半年上证指数、深证成指和创业板指分别上涨3.16%、19.82%、35.58%，同期上证红利指数下跌6%；下半年以来截至10月9日，上证红利指数上涨<b>16.88%</b>，上证指数、深证成指和创业板指则出现不同程度回调。国泰基金认为资金出于对科技行情调整、海外扰动的担忧提前向低位板块切换；招商基金认为市场从"抢预期"转向"看兑现"时，盈利确定性高、现金流充沛、分红可持续的资产成为相对稳健的选择。<br>
          <b>对腾安启示：</b>红利品类在震荡市中同时出现"存量限购＋新品提前结募"，货架须把限购状态、恢复日期与单日限额前置展示，避免用户在限额期内产生申购失败体验；同时须提示红利资产的行业集中特征（银行、资源、公用事业、交运），不得把短期风格切换包装成无风险收益。
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-10/12/content_2276193.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·10-12</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

new_s0 = C1 + '\n' + C2 + '\n' + C3 + '\n' + C4 + '\n    </div>\n  </div>\n\n'
log('   new S0 open=%d close=%d' % (len(re.findall(r'<div\b', new_s0)),
                                    len(re.findall(r'</div>', new_s0))))
src = src[:S0_START] + new_s0 + src[S0_END:]
s0 = src[src.find('Section 0'):src.find('Section 1')]
assert len(re.findall(r'class="date-tag">(\d{2})-(\d{2})<', s0)) == 4
assert s0.count('class="action-box"') == 1
assert s0.count('priority-tag urgent') == 1
NLINK = len(re.findall(r'<a href="http', s0))
assert NLINK == 7, 'S0 links=%d' % NLINK
log('Step5 S0 done links=%d' % NLINK)
dr('step5')

# ---------------- Step 6 S6 行情卡整段替换 ----------------
S6M = src.find('Section 6')
S6_START = src.find('<div class="card p3">', S6M)
ANCH = '      </div>  </div>'
S6_END = src.find(ANCH, S6_START) + len('      </div>')
assert S6_START > 0 and S6_END > S6_START
old_s6 = src[S6_START:S6_END]
log('   old S6 open=%d close=%d' % (len(re.findall(r'<div\b', old_s6)),
                                    len(re.findall(r'</div>', old_s6))))

new_s6 = '''<div class="card p3">
        <div class="card-top">
          <div class="card-title">''' + EMO_UP + ''' A股、港股、美股均为10-09收盘·沪指3813.79 +0.05%｜标普500创收盘历史新高</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-09</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-09收盘）</b><br>
              上证指数 <b>3813.79</b> <span style="color:#dc2626;">+0.05%</span><br>
              深证成指 <b>12641.86</b> <span style="color:#dc2626;">+0.17%</span><br>
              创业板指 <b>3043.33</b> <span style="color:#dc2626;">+0.22%</span><br>
              科创50 <b>1457.27</b> <span style="color:#dc2626;">+0.07%</span><br>
              科创综指 <span style="color:#52c41a;">-0.34%</span>　北证50 <span style="color:#dc2626;">+2.49%</span><br>
              沪深京三市成交 <b>1.92万亿</b>（沪深两市约1.90万亿）·较上一交易日放量约2224亿<br>
              全市场3297只上涨·2145只下跌·72只涨停
            </div>
            <div>
              <b>港股（10-09收盘）与美股（10-09收盘）</b><br>
              恒生指数 <b>24211.35</b> <span style="color:#dc2626;">+1.79%</span>（+425.56点）<br>
              恒生科技 <b>4197.84</b> <span style="color:#dc2626;">+3.05%</span><br>
              国企指数 <b>8147.87</b> <span style="color:#dc2626;">+1.71%</span>（+137.29点）<br>
              道琼斯 <b>51654.95</b> <span style="color:#dc2626;">+0.83%</span>（+423.31点）<br>
              纳斯达克 <b>27366.17</b> <span style="color:#dc2626;">+0.64%</span>（+172.83点）<br>
              标普500 <b>7811.54</b> <span style="color:#dc2626;">+0.59%</span>（+46.18点）<br>
              WTI原油91.66美元 <span style="color:#dc2626;">+0.19%</span>·COMEX黄金4220.3美元/盎司 <span style="color:#dc2626;">+1.52%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股、港股、美股本期统一取<b>10月9日收盘</b>——10月9日为节后第二个交易日（周五）且已收盘，10月10—11日为周末，10月12日A股尚在盘中，按铁律不取盘中值。<br>
              <b>A股（10-09）：</b>三大指数探底回升走出"深V"，沪指收<b>3813.79</b>点涨0.05%，深证成指收<b>12641.86</b>点涨0.17%，创业板指收<b>3043.33</b>点涨0.22%，科创50收<b>1457.27</b>点涨0.07%，科创综指跌0.34%，北证50涨2.49%；沪深京三市成交约<b>1.92万亿</b>元（沪深两市约1.90万亿元），较前一交易日放量约2224亿元，全市场3297只股票上涨、2145只下跌，72只涨停、10只跌停。申万一级行业中传媒涨5.28%、计算机涨2.33%、商贸零售涨2.30%领涨，有色金属涨逾2%；国防军工跌1.70%、电子跌1.47%、银行跌1.07%居前。盘面上影视院线、贵金属、广告营销、软件开发、游戏板块涨幅居前，元件、风电设备、电子化学品跌幅居前，多只宽基ETF成交放量。<br>
              <b>港股（10-09）：</b>恒生指数涨425.56点、涨幅1.79%，收报<b>24211.35</b>点，全日主板成交<b>2091.99亿港元</b>；国企指数涨137.29点、涨幅1.71%收<b>8147.87</b>点，恒生科技指数涨3.05%收<b>4197.84</b>点，科技股领涨，一改节后首日的疲弱表现。<br>
              <b>美股（10-09）：</b>道琼斯工业平均指数涨423.31点、涨幅0.83%收<b>51654.95</b>点，纳斯达克综合指数涨172.83点、涨幅0.64%收<b>27366.17</b>点，标普500指数涨46.18点、涨幅0.59%收<b>7811.54</b>点并创收盘历史新高；按周线计道指累涨0.93%、标普500累涨1.15%、纳指累涨0.64%。商品方面，纽约商品交易所WTI原油期货当月连续合约涨0.17美元、涨幅0.19%收于每桶<b>91.66美元</b>；COMEX黄金期货当月连续合约涨63.30美元、涨幅1.52%报<b>4220.3美元/盎司</b>，现货黄金涨1.47%报4194.24美元/盎司。<br>
              <b>对腾安提示：</b>A股节后走出"深V"但成交额仍处1.9万亿附近，科技硬件与前期强势方向继续分化、低估值传媒与贵金属接棒，货架与持仓页须同步刷新净值日期与估值口径，不得沿用节前旧净值呈现。海外端标普500创收盘新高与长端美债高位并存，须把"高利率压制估值"与"板块内部高低切换"两股力量并列提示，不得把单日涨跌直接解读为趋势反转。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股、美股均为2026-10-09收盘</span>
          <span class="source-tag">数据来源：新华财经、中国经济网、上海证券报、同花顺财经（10-09至10-12）</span>
        </div>
      </div>'''

log('   new S6 open=%d close=%d' % (len(re.findall(r'<div\b', new_s6)),
                                    len(re.findall(r'</div>', new_s6))))
assert len(re.findall(r'<div\b', new_s6)) == len(re.findall(r'<div\b', old_s6))
assert len(re.findall(r'</div>', new_s6)) == len(re.findall(r'</div>', old_s6))
src = src[:S6_START] + new_s6 + src[S6_END:]
assert src.count('</div>>') == 0
s6 = src[src.find('Section 6'):src.find('Section 7')]
assert '3813.79' in s6 and '10-08' not in s6
log('Step6 S6 done')
dr('step6')

# ---------------- Step 7 S7 时间线重写 ----------------
S7M = src.find('Section 7')
S7_START = src.find('      <div class="timeline-item">', S7M)
S7_END = src.find('    </div>\n\n  </div>', S7_START)
assert S7_START > 0 and S7_END > S7_START
old_s7 = src[S7_START:S7_END]
log('   old S7 items=%d' % len(re.findall(r'<div class="timeline-item">', old_s7)))

ITEMS = [
    ('2026-10-12', 'blue', '本周64只新基金集中开售'),
    ('2026-10-12', 'blue', '红利基金密集限购·防御升温'),
    ('2026-10-12', 'blue', '近5日科创50ETF净流入125亿'),
    ('2026-10-10', 'blue', '证监会召开资本市场专家座谈会'),
    ('2026-10-09', 'red', '公募运作办法迎12年来大修'),
    ('2026-10-09', 'blue', '公募自购超14亿设120只发起式'),
    ('2026-10-09', 'blue', '三季度翻倍基仅剩2只'),
    ('2026-10-09', 'blue', 'A股深V反弹沪指涨0.05%'),
    ('2026-10-09', 'blue', '港股恒生科技反弹涨3.05%'),
    ('2026-10-08', 'blue', '汇添富零售直销迁移子公司'),
    ('2026-10-08', 'red', '浙江证监局两家私募被警示'),
    ('2026-10-07', 'blue', '恒生科技指数扩至50只'),
]
parts = []
for d, c, t in ITEMS:
    assert len(t) <= 25, t
    parts.append('      <div class="timeline-item">\n'
                 '        <div class="timeline-dot %s"></div>\n'
                 '        <div class="timeline-date">%s</div>\n'
                 '        <div class="timeline-title">%s</div>\n'
                 '      </div>' % (c, d, t))
new_s7 = '\n'.join(parts) + '\n'
assert len(re.findall(r'<div\b', new_s7)) == len(re.findall(r'<div\b', old_s7))
assert len(re.findall(r'</div>', new_s7)) == len(re.findall(r'</div>', old_s7))
src = src[:S7_START] + new_s7 + src[S7_END:]
s7 = src[src.find('Section 7'):]
assert s7.count('class="timeline-item"') == 12
assert s7.count('timeline-desc') == 0
log('Step7 S7 done')
dr('step7')

# ---------------- Phase 8 全量断言 ----------------
o1, c1 = dr('final')
assert o1 == c1, 'div unbalanced %d/%d' % (o1, c1)
assert o1 == o0 + 3 and c1 == c0 + 3, 'drift unexpected %d/%d -> %d/%d' % (o0, c0, o1, c1)
assert 'S8' not in src
assert '\ufffd' not in src
assert src.count('</div>>') == 0
assert src.count('今日焦点</span>') == 1
assert '<span class="section-context">10月12日 · 4条今日要闻</span>' in src
for bad in ('stcn.com', '21jingji.com', 'cls.cn', 'yicai.com', 'toutiao',
            'so.html5.qq.com', '163.com/dy', 'guba.eastmoney.com'):
    assert bad not in src, bad
CUTS = (CUT.strftime('%m'), CUT.strftime('%d'))
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src):
    mm, dd = m.groups()
    assert (mm, dd) >= CUTS, 'expired date-tag %s-%s' % (mm, dd)
s0 = src[src.find('Section 0'):src.find('Section 1')]
assert len(re.findall(r'class="date-tag">(\d{2})-(\d{2})<', s0)) == 4
assert len(re.findall(r'<div class="card-title[^>]*>', s0)) == 4
titles = [re.sub(r'<[^>]+>', '', t) for t in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', s0, re.S)]
fps = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', src).group(1).split('|')
assert len(fps) == 4
for seg in fps:
    assert any(seg[:4] in t for t in titles), seg
dsegs = [x.strip() for x in re.search(r'<meta name="description" content="([^"]*)">', src).group(1).split('|') if x.strip()]
assert len(dsegs) == 5
for seg in dsegs[:4]:
    assert any(seg[:4] in t for t in titles), seg
s1 = src[src.find('Section 1'):src.find('Section 2')]
s2 = src[src.find('Section 2'):src.find('Section 3')]
assert s1.count('<div class="card p') == 6, s1.count('<div class="card p')
assert s2.count('<div class="card p') == 4, s2.count('<div class="card p')
log('Phase8 all asserts OK')

open(r'c:/Users/kelvinyye/WorkBuddy/20260314103829/_update_1012b_log.txt', 'w', encoding='utf-8').write(LOG.getvalue())
open(P, 'w', encoding='utf-8').write(src)
print('WRITE_OK div=%d/%d' % (o1, c1))
