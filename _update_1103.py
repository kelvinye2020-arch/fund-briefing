# -*- coding: utf-8 -*-
import io, re, sys
from datetime import date, timedelta

P = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
LOG = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\_update_1103_out.txt"
sys.stdout = io.open(LOG, "w", encoding="utf-8")

s = io.open(P, encoding="utf-8").read()
orig = s
TODAY = date(2026, 11, 3)
CUT = TODAY - timedelta(days=14)          # 2026-10-20
CUT_S = "%02d-%02d" % (CUT.month, CUT.day)

def op(t): return len(re.findall(r"<div[\s>]", t))
def cl(t): return t.count("</div>")
def stats(tag):
    print("STEP %-14s open=%d close=%d  (drift_o=%+d drift_c=%+d)" % (
        tag, op(s), cl(s), op(s)-op(orig), cl(s)-cl(orig)))

print("BASE open=%d close=%d" % (op(s), cl(s)))

# ============================ 1. marker ============================
A = "<!-- daily-update: 2026-11-02 -->"
assert s.count(A) == 1, "marker anchor fail"
s = s.replace(A, "<!-- daily-update: 2026-11-03 -->")
stats("marker")

# ============================ 2. description ============================
OLD_D = re.search(r'<meta name="description" content="([^"]*)">', s).group(0)
NEW_D = ('<meta name="description" content="证监会就稳市场稳预期答记者问·互换便利31家超1000亿元'
         '|主动ETF发行7天16只顶格结募·合计超350亿元'
         '|投资端改革持续发力·权益类基金规模增至10.3万亿元'
         '|10月黄金主题ETF逆势吸金·13只净流入约56亿元'
         '|沪指11月2日收3638.03点涨1.08%·纳指跌1.07%·COMEX12月黄金涨1.48%">')
assert s.count(OLD_D) == 1
s = s.replace(OLD_D, NEW_D)
stats("description")

# ============================ 3. fingerprint ============================
OLD_F = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', s).group(0)
NEW_F = '<meta name="content-fingerprint" content="证监会|主动ETF|投资端|10月黄">'
assert s.count(OLD_F) == 1
s = s.replace(OLD_F, NEW_F)
stats("fingerprint")

# ============================ 4. header 数据区间 ============================
hi = TODAY.strftime("%Y.%m.%d")
lo = CUT.strftime("%Y.%m.%d")
s2, n = re.subn(r"📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）",
                "📅 数据区间：%s — %s（每日更新）" % (lo, hi), s)
assert n == 1, "badge regex fail n=%d" % n
s = s2
stats("badge")

# ============================ 5. Stats Bar ============================
SA = "    <div class=\"stats-bar\">\n"
SB = "\n\n  </div>\n\n<div class=\"main\">"
ia = s.find(SA) + len(SA)
ib = s.find(SB)
assert s.count(SB) == 1, "stats end anchor not unique"
old_stats = s[ia:ib]
assert old_stats.count('<div class="stat-card"') == 4, "stat-card count %d" % old_stats.count('<div class="stat-card"')

NEW_STATS = """    <div class="stat-card">
      <div class="stat-number">350亿元</div>
      <div class="stat-label">首批18只主动ETF合计募集资金·截至11月2日16只达20亿元上限并结募（证监会，11月2日）</div>
      <div class="stat-change up">▲ 证监会引导加快投资建仓·9家管理人自购超27亿元</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3638.03</div>
      <div class="stat-label">沪指11-02收盘·涨1.08%·深证成指涨1.63%·创业板指涨1.87%（上海证券报、中证网，11月3日）</div>
      <div class="stat-change up">▲ 全市场成交1.80万亿元放量1075亿元·4681只个股上涨</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1000亿元</div>
      <div class="stat-label">第三批互换便利31家证券公司基金管理公司申请额度·近日开始操作（证监会，11月2日）</div>
      <div class="stat-change up">▲ 前两批28家合计1050亿元·回购增持再贷款利率降至1%</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3900亿元</div>
      <div class="stat-label">10月股票型ETF累计净流入（中证网，11月3日）</div>
      <div class="stat-change up">▲ 11月2日沪深两市主力资金净流入超50亿元</div>
    </div>"""
s = s[:ia] + NEW_STATS + s[ib:]
stats("stats-bar")
assert s.count('<div class="stat-card"') == 4

# ============================ 6. S0 换卡 ============================
M0 = s.find("<!-- ============ Section 0: 今日焦点 ============ -->")
M1 = s.find("<!-- ============ Section 1: 重磅信息 ============ -->")
assert M0 > 0 and M1 > M0
a0 = s.find("      <!-- S0 Card 1", M0)
b0 = s.find("\n\n\n    </div>\n\n  </div>", M0)
assert a0 > 0 and b0 > a0
old_s0 = s[a0:b0]
assert old_s0.count('<div class="card p') == 4, "S0 old cards %d" % old_s0.count('<div class="card p')

S0 = """      <!-- S0 Card 1 (11-02 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会就稳市场稳预期答记者问·第三批互换便利31家超1000亿元·护盘式回购四项优化·两融适度释放融资空间</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">11-02</span>
          </div>
        </div>
        <div class="card-body">
          证监会官网11月2日发布《中国证监会有关部门负责人就近期稳市场稳预期相关工作答记者问》（上海证券报·中国证券网同日21时49分刊发，记者梁银妍、汤立斌）：金融管理部门11月2日召开座谈会，就用好用足两项结构性货币政策工具作出安排。<br>
          <b>两项工具用足用好：</b>2024年9月人民银行会同证监会、金融监管总局推出证券、基金、保险公司互换便利和股票回购增持专项再贷款。截至今年10月底已开展两批次互换便利操作，<b>28家</b>证券公司和基金管理公司参与、合计金额<b>1050亿元</b>；全市场已有<b>902家</b>上市公司披露<b>1110单</b>回购增持贷款公告，加上中国国新、中国诚通两家国有资本运营公司申请的增持贷款，申请贷款额度上限累计约<b>4400亿元</b>。当天人民银行宣布将开展第三批互换便利操作，股票回购增持再贷款政策由阶段性安排转为<b>长期制度性安排</b>、再贷款利率降低至<b>1%</b>；经相关机构申请，证监会商人民银行已同意<b>31家</b>证券公司和基金管理公司开展第三批互换便利操作，申请额度超过<b>1000亿元</b>，近日就开始操作。<br>
          <b>护盘式回购四项优化：</b>一是新增股价"破发"作为可开展护盘式回购的情形之一，规定护盘式回购不适用"公司股票上市已满六个月"的限制，取消护盘式回购中开盘和收盘集合竞价阶段不得申报的限制；二是要求上市36个月内的上市公司当股价触及护盘式回购情形时，严格认真履行上市承诺中的稳定股价措施；三是要求存在超募资金的上市公司在触及护盘式回购情形时及时实施回购；四是要求上市公司在年度现金分红计划中明确一定比例资金纳入回购专项基金，存在超募资金的公司将一定比例超募资金纳入该基金并专项用于股份回购注销，通过集中竞价卖出护盘式回购股份的所得收益亦须纳入。下一步将抓紧修订《上市公司股份回购规则》。<br>
          <b>回购数据：</b>今年前10个月，沪深两市<b>645家</b>上市公司披露<b>700单</b>、<b>2377亿元</b>股份回购计划，其中回购注销金额<b>1150亿元</b>、占比近50%；<b>747家</b>公司实际实施回购<b>1345亿元</b>；回购计划金额、实际回购金额、回购注销金额及占比均创历史新高。<br>
          <b>融资融券逆周期调节：</b>2026年1月沪深北交易所将融资保证金比例由80%提高至100%；近期融资余额和交易活跃度明显下降、整体杠杆水平趋于稳健，证监会将指导证券公司对融资保证金比例、可充抵保证金证券折算率、维持担保比例等风险控制指标统筹研究、进一步优化，在风险总体可控基础上适度释放融资空间。<br>
          <b>工具端同步表态：</b>首批18只主动ETF于10月19日注册、10月23日启动募集，截至11月2日合计募集资金超过<b>350亿元</b>、其中16只达到20亿元单只上限并结束募集，证监会将引导和鼓励已完成募集的18只主动ETF加快开展投资建仓；同时推出更多新指数股票ETF、研究推出股债恒定比例等多资产指数基金、对新设立主动管理权益类基金大力推行基于业绩比较基准的浮动管理费收取模式。<br>
          <b>对腾安启示：</b>互换便利与回购再贷款由"阶段性工具"升级为"长期制度安排"，意味着政策托底从应急转向常态化，销售端不得把政策工具等同于市场上涨承诺；浮动管理费与业绩比较基准绑定是新发主动权益产品的默认方向，货架须把费率结构与基准口径做成可比对字段；护盘式回购与两融空间放宽属上市公司与交易层面政策，不得演绎为基金产品的收益预期。
        </div>
        <div class="card-footer">
          <a href="https://www.csrc.gov.cn/csrc/c100028/c7668092/content.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证监会官网·11-02</span></a>
          <a href="https://www.cnstock.com/commonDetail/822776" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·11-02</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            1. 合规侧：立即排查所有在架主动权益产品的费率结构展示，凡采用浮动管理费模式的产品须在费率栏明确"固定部分＋浮动部分"的计算方式与业绩比较基准，不得只显示"浮动费率"四字而隐去基准口径。<br>
            2. 内容侧：政策类热点（互换便利、回购再贷款、两融优化）只可作为市场背景科普，不得与具体基金的申购引导同屏呈现；如制作科普页，须标注政策发布主体与生效状态，并提示"政策工具不等于收益保障"。<br>
            3. 货架侧：主动ETF专区须在上市前补齐业绩比较基准、浮动费率说明与PCF每日披露入口三个字段，并同步准备"建仓期净值波动与基准偏离"的提示文案，避免把"顶格募集＋政策引导建仓"直接包装为买入信号。
          </div>
        </div>
      </div>

      <!-- S0 Card 2 (11-02 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 主动ETF发行7天16只顶格结募·合计超350亿元·11只已成立·摩根易方达华夏平安启动建仓</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">11-02</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报11月2日22时54分刊发（记者闫军、方丽）：11月2日华宝基金公告，华宝均衡精选主动ETF提前结束募集并将启动比例配售——该基金自10月23日开启募集、原定募集截止日为11月3日，截至11月2日累计有效认购申请份额总额已超过20亿份（折合20亿元人民币）上限，募集截止日提前至11月2日，超募部分按"末日比例确认"原则部分确认。<br>
          <b>发行进度：</b>首批18只主动ETF已有<b>16只</b>完成发行任务，合计募集资金超过<b>350亿元</b>；鹏华基金、建信基金旗下产品仍在募集。已有<b>11只</b>主动ETF公告成立，摩根、易方达、华夏、平安等管理人旗下产品已启动建仓，为市场注入百亿级别增量资金。<br>
          <b>结募节奏：</b>摩根基金、易方达基金、富国基金旗下产品均在10月23日发行首日实现"一日结募"；10月26日华夏基金、华泰柏瑞基金、南方基金、平安基金旗下产品提前结募；10月27日汇添富基金、大成基金、招商基金、天弘基金旗下产品提前结募；10月28日、29日华安基金、永赢基金宣布提前结募；10月30日国泰基金、工银瑞信基金加入结募。中国证券网口径显示，有<b>3只</b>基金仅1日就完成募集，超半数基金在3日内完成募集。<br>
          <b>认购户数：</b>11只已公告产品的合计认购户数超<b>21.2万户</b>；南方均衡配置主动ETF有效认购户数<b>2.69万户</b>居首，华泰柏瑞价值精选主动ETF<b>2.5万户</b>次之，招商价值智选、易方达品质智选、大成红利智选均超2万户。<br>
          <b>自购：</b>摩根基金、易方达基金、富国基金等<b>9家</b>管理人通过自有资金、股东方资金自购旗下主动ETF产品，自购金额合计超<b>27亿元</b>。<br>
          <b>对腾安启示：</b>主动ETF从"发行"进入"建仓与上市"，货架须同步披露每只产品的建仓进度披露入口与业绩比较基准，避免用户按普通ETF的跟踪误差预期去理解主动ETF；"基金公司自购"须与"业绩保证"严格切割，宣传中不得把自购金额解读为收益背书。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/AR46f1891e-94a3-04a4-c5f8-3a24aec8f186" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·11-02</span></a>
          <a href="https://m.chinanews.com/wap/detail/cht/zw/10725047.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国新闻网·11-02</span></a>
          <a href="https://www.cnstock.com/commonDetail/822776" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·11-02</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>

      <!-- S0 Card 3 (11-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 投资端改革持续发力·权益类基金规模增至10.3万亿元·近两年长线资金净买入A股超1.5万亿元</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">11-03</span>
          </div>
        </div>
        <div class="card-body">
          中国经济网11月3日报道：在公募基金改革走深走实背景下，证监会持续加大权益类基金产品供给和创新力度，重点推进三个方向——推出更多新指数股票ETF、丰富场内投资工具；研究推出股债恒定比例等多资产指数基金、丰富场外中低波动型产品；对新设立的主动管理权益类基金大力推行基于业绩比较基准的浮动管理费收取模式。证监会相关负责人还透露，近期已会同交易所优化新指数ETF论证机制，支持基金管理人基于可持续发展潜力、市场容量和标的流动性等因素推出更多以新指数为跟踪标的的股票指数ETF。<br>
          <b>规模与资金：</b>上海证券报·中国证券网11月2日披露的证监会数据显示，2025年初至2026年9月底，权益类基金规模由<b>8.6万亿元</b>增长到<b>10.3万亿元</b>，增幅<b>19.8%</b>；近两年全国社保基金、基本养老金、年金基金、保险资金合计净买入A股超过<b>1.5万亿元</b>，近期全国社保基金、基本养老金、保险资金、公募基金、证券公司等机构投资者整体逆势加仓。<br>
          <b>长钱长投生态：</b>保险资金权益投资比例持续放宽、长期股票投资试点稳步扩容；年金、养老金依托长周期考核机制稳步提升权益持仓；主动ETF带来数百亿元增量资金并陆续建仓；境外主权基金、海外养老金等国际长线资金持续加大A股战略性配置。川财证券首席经济学家陈雳认为，随着长周期考核机制落地、权益类产品供给丰富、配套入市规则完善，中长期资金队伍还将持续壮大。<br>
          <b>对腾安启示：</b>权益类基金规模扩张与产品谱系细化并行，货架的筛选维度须从"收益率排名"扩展到"产品类型＋资产构成＋波动档位"，尤其是股债恒定比例类多资产产品上架后须单独成类；"长钱长投"类表述只可作为投资者教育素材，不得用于暗示短期申赎时点或无风险属性。
        </div>
        <div class="card-footer">
          <a href="https://www.ce.cn/xwzx/gnsz/gdxw/202611/t20261103_3281001.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·11-03</span></a>
          <a href="https://www.cnstock.com/commonDetail/822776" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·中国证券网·11-02</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

      <!-- S0 Card 4 (11-03 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 10月黄金主题ETF逆势吸金·13只净流入合计约56亿元·净值下跌致规模不升反降</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">11-03</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻11月3日报道（记者肖芮冬、编辑赵云）：10月国际金价高位震荡，黄金主题ETF普遍遭遇净值下跌，但资金面呈现"越跌越买"态势。数据显示，10月<b>13只</b>黄金主题ETF申赎净流入全部为正，合计净流入约<b>56亿元</b>。<br>
          <b>规模变动：</b>从规模看13只产品规模均出现不同程度下滑。产品类型方面，商品型黄金ETF净值下跌导致规模减少<b>146亿元</b>，股票型黄金ETF净值下跌导致规模减少<b>32.8亿元</b>；从标的指数看，股票型黄金ETF规模减少居后，或因跟踪黄金产业股票指数、波动幅度相对更大。综合来看，13只黄金ETF净值下跌是总规模缩水的主因，导致多数产品规模"不升反降"。<br>
          <b>对腾安启示：</b>"越跌越买"说明黄金ETF的客户行为以定投与逆向补仓为主，产品页须把"区间净值涨跌"与"份额净流入"并列展示，避免用户只看净值曲线判断资金热度；商品型黄金ETF与黄金股ETF跟踪标的完全不同（金价 vs 黄金产业股票），货架须分开打标、分别给出波动来源说明，不得笼统归为"黄金基金"混同展示。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20261103A0361E00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·11-03</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>"""

s = s[:a0] + S0 + s[b0:]
stats("S0-cards")
sec0 = s[s.find("Section 0"):s.find("Section 1")]
assert sec0.count('<div class="card p') == 4, "S0 new cards %d" % sec0.count('<div class="card p')
assert sec0.count('class="action-box"') == 1, "S0 action-box %d" % sec0.count('class="action-box"')

# -------- S0 context（另一步） --------
OC = '<span class="section-context">11月2日 · 4条今日要闻</span>'
NC = '<span class="section-context">11月3日 · 4条今日要闻</span>'
assert s.count(OC) == 1, "S0 context anchor fail"
s = s.replace(OC, NC)
stats("S0-context")

# ============================ 7. S1 新增卡 ============================
M1b = s.find("<!-- ============ Section 1: 重磅信息 ============ -->")
M2 = s.find("<!-- ============ Section 2: 监管政策 ============ -->")
b1 = s.find("\n\n\n\n\n\n    </div>\n\n  </div>", M1b)
assert b1 > M1b and b1 < M2
sec1_old = s[M1b:b1]
assert sec1_old.count('<div class="card p') == 5, "S1 old cards %d" % sec1_old.count('<div class="card p')

S1C = """

      <!-- S1 Card (11-03 p2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 南向ETF通扩容新增10只·11月9日生效·产品数量由31只增至41只</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">11-03</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻11月3日报道：近日沪深交易所公布"南向ETF通"扩容名单，新增<b>10只</b>ETF，该调整将于<b>11月9日</b>正式生效。扩容之后，南向ETF通产品数量将由<b>31只</b>增加至<b>41只</b>。<br>
          <b>调入名单：</b>银河博时东盟、FG恒生红利、华夏港美AI、嘉实科技50、富邦沪深港高股息、GX国寿港美、恒生高息股、南方亚洲科技股息、惠理港美红利低波、南方港日现金流。<br>
          <b>成交：</b>2026年年初至今，南向ETF通日均成交额突破<b>48亿港元</b>，同比增幅达<b>15%</b>。<br>
          <b>对腾安启示：</b>南向ETF通扩容意味着内地资金可投的港股与跨境ETF货架继续变宽，产品页须按跟踪指数、费率与交易柜台分组展示，并对新纳入产品标注生效日期；"港股通标的"不等于无汇率与额度风险，相关产品须同步提示汇率波动、额度暂停与两地交易日历差异。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20261103A0361E00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·11-03</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>"""
s = s[:b1] + S1C + s[b1:]
stats("S1-insert")
sec1 = s[s.find("Section 1"):s.find("Section 2")]
assert sec1.count('<div class="card p') == 6, "S1 new cards %d" % sec1.count('<div class="card p')

# ============================ 8. S5 换掉 10-19 越界卡 ============================
M5 = s.find("<!-- ============ Section 5: 金融科技与AI ============ -->")
M6 = s.find("<!-- ============ Section 6: 市场行情速览 ============ -->")
k = s.find("      <!-- S5 Card: 汇添富", M5)
assert k > M5 and k < M6, "S5 comment anchor fail"
cs = s.find('<div class="card p', k)
i = s.find(">", cs) + 1
d = 1
while d > 0:
    m = re.compile(r"<div[\s>]|</div>").search(s, i)
    if m.group(0) == "</div>":
        d -= 1
    else:
        d += 1
    i = m.end()
ce = m.start() + len("</div>")
blk = s[k:ce]
assert blk.count('<div class="card p') == 1, "S5 blk cards %d" % blk.count('<div class="card p')

S5C = """      <!-- S5 Card (11-02 p1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 永赢基金斥资近1487万元采购国产算力服务器·基金公司开始"抢算力"</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">11-02</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报11月2日报道（记者曹雯璟）：中标公告显示，永赢基金于9月末完成一笔算力基础设施采购，中标金额<b>1486.9万元</b>（近1487万元），项目内容为"采购国产算力服务器<b>4台</b>，对现有算力集群扩容，满足万亿级及以上参数规模大模型的部署与推理服务需求"；招标人为永赢基金，中标人为北京可利邦信息技术股份有限公司，项目预算金额1500万元、9月21日开标。<br>
          <b>公司回应：</b>永赢基金表示已完成GPU集群部署并根据算力使用情况持续扩容；构建自有算力平台，一方面保障"数据不出域"、实现数据资产沉淀，另一方面为模型和智能体快速迭代提供基础保障；应用层面围绕投研、风控、营销和运营四大核心业务领域，逐步推进AI能力的深度融合与落地。<br>
          <b>规模背景：</b>Wind数据显示，截至2026年三季度末，永赢基金公募管理总规模达<b>7004.6亿元</b>、全市场排名第21/162；非货公募（剔除联接）管理规模<b>4850.2亿元</b>、排名第13/162。<br>
          <b>对腾安启示：</b>①基金公司自建算力从"买服务"转向"买硬件"，说明大模型应用已进入常态化运行阶段，机构AI产出的可靠性将越来越取决于其私有数据口径与更新频率，腾安在引用第三方AI内容时必须确认数据时点；②"数据不出域"是金融机构自建算力的核心动因，凡涉及客户持仓与行为数据的AI功能须同等对待数据边界与合规留痕，不得因功能便利放松授权范围。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-11-02/doc-inixiuez9353516.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·中国基金报·11-02</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>"""
s = s[:k] + S5C + s[ce:]
stats("S5-replace")
sec5 = s[s.find("Section 5"):s.find("Section 6")]
assert sec5.count('<div class="card p') == 4, "S5 cards %d" % sec5.count('<div class="card p')
assert 'class="date-tag">10-19<' not in sec5

# ============================ 9. S6 换卡 ============================
M6b = s.find("<!-- ============ Section 6: 市场行情速览 ============ -->")
M7 = s.find("<!-- ============ Section 7: 关键时间线 ============ -->")
a6 = s.find('<div class="card p3">', M6b)
tail6 = "      </div>  </div>"
p6 = s.find(tail6, M6b)
assert a6 > M6b and p6 > a6 and p6 < M7, "S6 anchor fail"
b6 = p6 + len("      </div>")
old6 = s[a6:b6]
assert old6.count('<div class="card p') == 1, "S6 old cards %d" % old6.count('<div class="card p')
print("S6 old open=%d close=%d" % (op(old6), cl(old6)))

S6 = """<div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 A股、港股、美股统一11-02收盘·沪指3638.03 +1.08%｜纳指跌1.07%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">11-02</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">

            <div>
              <b>A股（11-02收盘）</b><br>
              上证指数 <b>3638.03</b> <span style="color:#e03131;">+1.08%</span><br>
              深证成指 <b>11010.68</b> <span style="color:#e03131;">+1.63%</span><br>
              创业板指 <b>2458.70</b> <span style="color:#e03131;">+1.87%</span>（盘中一度涨超3.5%）<br>
              科创综指 <b>1458.50</b> <span style="color:#e03131;">+2.62%</span><br>
              沪市成交 <b>8474.59亿元</b>／深市成交 <b>9362.36亿元</b><br>
              全市场成交额 <b>1.80万亿元</b>，较前一交易日增加 <b>1075亿元</b><br>
              上涨 <b>4681只</b>、涨停 <b>131只</b>；下跌818只、跌停10只
            </div>
            <div>
              <b>港股（11-02收盘）与美股（美东11-02收盘）</b><br>
              恒生指数 <b>23393.32</b> <span style="color:#e03131;">+0.42%</span>（+98.9点）<br>
              国企指数 <b>7906.11</b> <span style="color:#e03131;">+0.56%</span>（+43.89点）<br>
              恒生科技 <b>3839.41</b> <span style="color:#e03131;">+2.25%</span>（+84.51点）<br>
              港股主板成交 <b>2048.4亿港元</b><br>
              道琼斯 <b>51983.98</b> <span style="color:#e03131;">+0.41%</span>（+213.67点）<br>
              纳斯达克 <b>25164.32</b> <span style="color:#52c41a;">-1.07%</span>（-272.68点）<br>
              标普500 <b>7541.40</b> <span style="color:#52c41a;">-0.51%</span>（-38.67点）<br>
              纽约12月交货原油 <b>96.46美元/桶</b> <span style="color:#52c41a;">-7.36%</span><br>
              伦敦1月交货布伦特 <b>104.77美元/桶</b> <span style="color:#52c41a;">-7.63%</span><br>
              COMEX12月黄金 <b>3956.6美元/盎司</b> <span style="color:#e03131;">+1.48%</span><br>
              COMEX12月白银 <b>50.710美元/盎司</b> <span style="color:#e03131;">+2.91%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股取<b>11月2日收盘</b>（11月2日为11月首个交易日且已收盘）：上证指数报3638.03点、涨幅1.08%，深证成指报11010.68点、涨幅1.63%，创业板指报2458.70点、涨幅1.87%，科创综指报1458.50点、涨幅2.62%，四项同出上海证券报11月3日《A股放量普涨 风格切换信号显现》与中证网11月3日《股票型ETF持续净流入》；涨跌家数与全市场成交额出自中证网——上涨4681只、131只涨停、818只下跌、10只跌停，市场成交额1.80万亿元、较前一交易日增加1075亿元；沪市成交8474.59亿元、深市成交9362.36亿元为分市场成交额口径，与含北交所的全市场1.80万亿元统计范围不同，本期并列列出、不合并计算；北证50仅取得中证网口径涨幅0.58%、未取得同源可交叉验证的收盘点位，本期不予列示。<br>
              <b>港股：</b>取<b>11月2日收盘</b>（新华社香港11月2日电，金融时报·中国金融新闻网11月3日刊发）：恒生指数涨98.9点、涨幅0.42%，收报23393.32点，全日主板成交2048.4亿港元；国企指数涨43.89点、涨幅0.56%，收报7906.11点；恒生科技指数涨84.51点、涨幅2.25%，收报3839.41点。<br>
              <b>美股：</b>取<b>美东11月2日收盘</b>（新华社纽约11月2日电，新华财经11月3日刊发，记者刘亚南）：道琼斯工业平均指数涨213.67点、涨幅0.41%，收于51983.98点；标准普尔500种股票指数跌38.67点、跌幅0.51%，收于7541.40点；纳斯达克综合指数跌272.68点、跌幅1.07%，收于25164.32点；标普500十一大板块七涨四跌，非必需消费品板块和材料板块分别以2.25%和1.83%的涨幅领涨，能源板块和科技板块分别以3.97%和2.66%的跌幅领跌。<br>
              <b>商品与贵金属：</b>国际原油取<b>11月2日收盘</b>：纽约商品交易所12月交货轻质原油期货价格下跌7.66美元，收于每桶96.46美元，跌幅7.36%；1月交货伦敦布伦特原油期货价格下跌8.66美元，收于每桶104.77美元，跌幅7.63%。贵金属取<b>11月2日收盘</b>（新华财经纽约11月2日电，记者徐静）：12月黄金期价上涨57.7美元，收于每盎司3956.6美元，涨幅1.48%；12月白银期价上涨1.434美元，收于每盎司50.710美元，涨幅2.91%；另存在央视财经等其他口径，数值略有差异，本期统一采用新华财经口径、不混用。<br>
              <b>A股（11-02）：</b>主要指数集体高开高走，成长与价值板块共振走强，全市场超4600只个股上涨、逾130只个股涨停，成交额逼近1.8万亿元。申万一级行业中传媒板块以7.77%的涨幅居首，短剧游戏、AI漫剧方向掀起涨停潮，计算机、社会服务分别上涨4.96%和3.50%，非银金融、商贸零售均涨逾3%；另一端煤炭跌1.33%、银行跌0.84%、有色金属跌0.40%，31个一级行业中28个收涨。<br>
              <b>美股（美东11-02）：</b>科技股继续承压，存储与光通信板块大幅下挫；美国和伊朗通过外交渠道解决争端的乐观预期推动国际油价显著下挫超7%，对道指形成支撑。美国10月制造业采购经理人指数终值为54.9，低于56的初值；供应管理学会制造业景气指数为55.5，高于前月54.5。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <a href="https://paper.cnstock.com/html/2026-11/03/content_2286704.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报电子版·11-03</span></a>
          <a href="https://www.cs.com.cn/gppd/gsyj/2026/11/03/detail_2026110310049385.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·11-03</span></a>
          <a href="https://finance.ce.cn/stock/gsgdbd/202611/t20261103_3280975.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·A股收评·11-03</span></a>
          <a href="https://www.financialnews.com.cn/2026-11/03/content_460063.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国金融新闻网·新华社·港股·11-03</span></a>
          <a href="https://m.cnfin.com/gs-lb//zixun/20261103/4490043_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·美股·11-03</span></a>
          <a href="https://m.cnfin.com/hs-lb//zixun/20261103/4490070_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·纽约金价·11-03</span></a>
          <a href="https://m.chinanews.com/wap/detail/chs/zw/jw695265.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国新闻网·中新经纬·油价·11-03</span></a>
          <span class="impact-tag medium">辅助决策</span>
        </div>
      </div>"""
s = s[:a6] + S6 + s[b6:]
stats("S6-replace")
sec6 = s[s.find("Section 6"):s.find("Section 7")]
assert sec6.count('<div class="card p') == 1, "S6 cards %d" % sec6.count('<div class="card p')

# ============================ 10. S7 时间线 ============================
M7b = s.find("<!-- ============ Section 7: 关键时间线 ============ -->")
a7 = s.find('<div class="timeline-item">', M7b)
last7 = s.rfind('<div class="timeline-item">', M7b)
b7 = s.find("\n\n    </div>", last7)
assert a7 > M7b and b7 > last7, "S7 anchor fail"
old7 = s[a7:b7]
assert old7.count('<div class="timeline-item"') == 12, "S7 old items %d" % old7.count('<div class="timeline-item"')

ITEMS = [
    ("2026-11-03", "南向ETF通扩容至41只", "blue"),
    ("2026-11-03", "10月黄金ETF净流入56亿", "blue"),
    ("2026-11-02", "证监会答记者问稳市场", "red"),
    ("2026-11-02", "主动ETF16只顶格结募", "red"),
    ("2026-11-02", "央行第三批互换便利启动", "red"),
    ("2026-11-02", "A股放量普涨沪指涨1.08%", "red"),
    ("2026-11-02", "美股分化纳指跌1.07%", "blue"),
    ("2026-11-02", "国际油价单日跌超7%", "blue"),
    ("2026-11-01", "公募年内分红超1400亿", "blue"),
    ("2026-10-30", "沪指失守3600点10月收官", "red"),
    ("2026-10-28", "公募平均仓位降至78.32%", "blue"),
    ("2026-10-26", "运作办法征求意见稿发布", "blue"),
]
NEW7 = "\n".join(
    '      <div class="timeline-item">\n'
    '        <div class="timeline-dot %s"></div>\n'
    '        <div class="timeline-date">%s</div>\n'
    '        <div class="timeline-title">%s</div>\n'
    '      </div>' % (c, d, t) for d, t, c in ITEMS)
for _, t, _ in ITEMS:
    assert len(t) <= 25, "S7 title too long: %s (%d)" % (t, len(t))
s = s[:a7] + NEW7 + s[b7:]
stats("S7-replace")
sec7 = s[s.find("Section 7"):]
assert sec7.count('<div class="timeline-item"') == 12, "S7 items %d" % sec7.count('<div class="timeline-item"')
assert "timeline-desc" not in sec7

# ============================ 11. 全量断言 ============================
assert op(s) == cl(s), "DIV 失衡 open=%d close=%d" % (op(s), cl(s))
assert s.count("</div>>") == 0
assert "Section 8" not in s and "S8" not in s
assert s.count("�") == 0, "U+FFFD 出现"
assert s.count('<span class="section-title">今日焦点</span>') == 1
assert s.count("11月3日 · 4条今日要闻") == 1
assert "今日焦点（" not in s

BLACK = ["stcn.com", "cls.cn", "21jingji.com", "yicai.com", "guba.eastmoney.com",
         "toutiao", "so.html5.qq.com", "mp.weixin.qq.com", "163.com/dy", "dy.163.com",
         "weibo.com", "k.sina.com.cn", "q.fund.sohu.com", "cofool.com", "jiantou8.com"]
for b in BLACK:
    assert b not in s, "黑名单命中 %s" % b

# date-tag 越界扫描
bad = []
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s):
    mo, dd = int(m.group(1)), int(m.group(2))
    if (mo, dd) < (CUT.month, CUT.day) and not (mo > CUT.month):
        bad.append(m.group(0))
for m in re.finditer(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s):
    mo, dd = int(m.group(1)), int(m.group(2))
    dt = date(2026, mo, dd)
    if dt < CUT:
        bad.append((m.group(0), str(dt)))
print("date-tag 越界:", bad)
assert not bad, "date-tag 越界 %s" % bad

# fingerprint / description 复核
fps = re.search(r'<meta name="content-fingerprint" content="([^"]*)">', s).group(1).split("|")
sec0 = s[s.find("Section 0"):s.find("Section 1")]
titles = [re.sub(r"<[^>]+>", "", t) for t in re.findall(r'<div class="card-title[^>]*>(.*?)</div>', sec0, re.S)]
assert len(fps) == len(titles) == 4, "fingerprint 段数 %d / 卡数 %d" % (len(fps), len(titles))
for seg in fps:
    assert any(seg[:4] in t for t in titles), "fingerprint 段 %s 未命中标题" % seg
dsegs = [x for x in re.search(r'<meta name="description" content="([^"]*)">', s).group(1).split("|")]
for seg in dsegs[:len(fps)]:
    assert any(seg[:4] in t for t in titles), "description 段 %s 未命中标题" % seg

# 深度法：各 section 卡起始 depth 单一
def depth_at(pos):
    return len(re.findall(r"<div[\s>]", s[:pos])) - s[:pos].count("</div>")
for name, a, b in [("S0", s.find("Section 0"), s.find("Section 1")),
                   ("S1", s.find("Section 1"), s.find("Section 2")),
                   ("S2", s.find("Section 2"), s.find("Section 3")),
                   ("S4", s.find("Section 4"), s.find("Section 5")),
                   ("S5", s.find("Section 5"), s.find("Section 6")),
                   ("S6", s.find("Section 6"), s.find("Section 7"))]:
    ds = set()
    for m in re.finditer(r'<div class="card p', s[a:b]):
        ds.add(depth_at(a + m.start()))
    print("DEPTH", name, sorted(ds))
    assert len(ds) == 1, "%s 卡起始 depth 不唯一 %s" % (name, ds)

print("\nFINAL open=%d close=%d  len=%d" % (op(s), cl(s), len(s)))
print("S0 cards", sec0.count('<div class="card p'), "| action-box", s.count('class="action-box"'))
print("ALL ASSERTIONS PASSED")

data = s.encode("utf-8")
io.open(P, "wb").write(data)
print("WRITTEN bytes=%d" % len(data))
