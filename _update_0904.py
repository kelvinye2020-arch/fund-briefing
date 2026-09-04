# -*- coding: utf-8 -*-
"""基金行业资讯看板 2026-09-04 每日更新脚本（两阶段：Phase1 断言 -> 写文件）"""
import io

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"

with io.open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

orig_opens = s.count("<div")
orig_closes = s.count("</div>")
print("ORIG div: open=%d close=%d" % (orig_opens, orig_closes))

errors = []

def need(cond, msg):
    if not cond:
        errors.append(msg)
        print("  [FAIL] " + msg)
    else:
        print("  [ok]   " + msg)

def replace_once(old, new, label):
    global s
    cnt = s.count(old)
    if cnt != 1:
        errors.append("%s: 锚点命中 %d 次（应为1）" % (label, cnt))
        print("  [FAIL] %s cnt=%d" % (label, cnt))
        return
    # div 平衡：替换前后 div 计数一致（内容替换才允许，整块替换要求相等）
    if old.count("<div") != new.count("<div") or old.count("</div>") != new.count("</div>"):
        errors.append("%s: 替换块 div 计数不一致 old(%d/%d) new(%d/%d)" % (
            label, old.count("<div"), old.count("</div>"), new.count("<div"), new.count("</div>")))
        print("  [FAIL] %s div mismatch" % label)
        return
    s = s.replace(old, new, 1)
    print("  [ok]   %s replaced" % label)

# ---------- 1. marker ----------
replace_once(
    "<!-- daily-update: 2026-09-03 -->",
    "<!-- daily-update: 2026-09-04 -->",
    "marker")

# ---------- 2. header date-badge ----------
replace_once(
    "\U0001F4C5 数据区间：2026.08.18 — 2026.09.01（每日更新）",
    "\U0001F4C5 数据区间：2026.08.19 — 2026.09.03（每日更新）",
    "header-date-badge")

# ---------- 3. Stats Bar 沪指卡 (09-02 -> 09-03 收盘) ----------
replace_once(
    '      <div class="stat-number">3941.39</div>\n'
    '      <div class="stat-label">沪指9-2收盘·跌0.97%·9月前两日A股连跌·成交1.82万亿</div>\n'
    '      <div class="stat-change down">▼ 深成指-1.88%·创业板-2.39%·3901股下跌</div>',
    '      <div class="stat-number">3942.09</div>\n'
    '      <div class="stat-label">沪指9-3收盘·微涨0.02%·两市成交1.76万亿·窄幅震荡</div>\n'
    '      <div class="stat-change up">\u25B2 深成指+0.10%·创业板+0.01%·缩量企稳</div>',
    "stats-card2")

# ---------- 4. S0 整块替换 ----------
S0_START = s.index("        <!-- ============ Section 0:")
S0_END = s.index("<!-- ============ Section 1:")
old_s0 = s[S0_START:S0_END]

S0_NEW = """        <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">\U0001F525</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月4日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">

      <!-- S0 Card 1 (09-04 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">\U0001F534 单周82只新基金发行创纪录·首批8只创业板算力ETF 9-4集中发行</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-04</span>
          </div>
        </div>
        <div class="card-body">
          9月首周全市场<b>82只新基金集中启动发行</b>，刷新单周启动募集数量纪录；其中首批<b>8只创业板算力基础设施ETF于9月4日同步首发</b>，聚焦AI算力产业链（光模块/服务器/IDC），为场内首只跟踪创业板算力指数的工具化产品。<br>
          <b>结构特征：</b>权益类发行明显回暖，指数化、工具化产品占比持续抬升；8月28日首批10只创业板算力ETF、6只金融科技ETF同获批复，产品矩阵加速扩容。<br>
          <b>对腾安启示：</b>供给端放量要求货架快速响应——算力ETF同质化竞争下须做"严选+费率+投教"组合，避免客户在热点赛道追高站岗。
        </div>
        <div class="card-footer">
          <a href="https://www.cs.com.cn/tzjj/etf/2026/09/04/detail_2026090410036831.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中证网·09-04</span></a>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 货架响应→评估8只创业板算力ETF差异（跟踪标的/费率/流动性），T+1内完成上架评审；<br>
            ② 投教前置→制作"算力ETF怎么选/怎么配"短内容，引导理性配置而非追热点；<br>
            ③ 风险预警→提示同质化ETF规模分化与折溢价风险，强化持有期陪伴。
          </div>
        </div>
      </div>

      <!-- S0 Card 2 (09-04 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 基金经理聚焦业绩兑现·科技成长迈入"业绩验证深水区"</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-04</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报（记者魏昭宇）9月4日报道，随着中报披露收官，基金经理投资思路从"讲赛道"转向<b>"抓业绩兑现"</b>——科技成长板块历经估值修复后，已进入业绩能否接棒的关键验证期。<br>
          <b>共识变化：</b>机构普遍降低对纯主题炒作的容忍度，更看重订单落地、毛利率改善与现金流质量；算力、半导体、创新药等前期热门方向面临"估值与业绩再匹配"。<br>
          <b>对腾安启示：</b>投研服务应同步从"赛道叙事"转向"盈利质量分析"，帮助客户识别真正有业绩支撑的标的，规避题材退潮风险。
        </div>
        <div class="card-footer">
          <a href="https://epaper.cs.com.cn/zgzqb/html/2026-09/04/nw.D110000zgzqb_20260904_3-A03.htm" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·09-04</span></a>
        </div>
      </div>

      <!-- S0 Card 3 (09-04 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 北交所主题基金年内收益翻倍·多只QDII限购松绑引关注</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-04</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻9月4日梳理，受益北交所流动性改善与专精特新行情，多只北交所主题基金年内净值<b>收益翻倍</b>；与此同时，前期因额度紧张限购的<b>多只QDII基金近期集中松绑</b>恢复大额申购，跨境配置通道重新打开。<br>
          <b>双向信号：</b>一方面小盘成长活跃度提升、结构性机会涌现；另一方面QDII松绑反映额度压力缓解、外围资产配置性价比回升。<br>
          <b>对腾安启示：</b>可适度丰富北交所主题与跨境QDII货架，但须对高波动小盘产品做好风险分级与适当性提示。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260904A033UW00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经（腾讯新闻）·09-04</span></a>
        </div>
      </div>

      <!-- S0 Card 4 (09-04 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">\U0001F7E1 长安基金总经理李晔兼任财务总监·中小公募治理调整提速</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-04</span>
          </div>
        </div>
        <div class="card-body">
          每经9月4日报道，长安基金公告总经理李晔<b>兼任公司财务总监</b>，系中小公募在降本增效、强化风控合规背景下的治理架构调整动作；同期多家中小机构通过高管兼任、部门合并压缩管理成本。<br>
          <b>行业背景：</b>费率改革压缩管理费收入、头部效应加剧，中小公募盈利承压，治理"扁平化"成为节流与提效的常见选择。<br>
          <b>对腾安启示：</b>代销合作中须关注中小公募治理结构稳定性与合规能力，将其纳入合作机构风险评估维度。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260904A033UW00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每经（腾讯新闻）·09-04</span></a>
        </div>
      </div>

    </div>
  </div>
"""

# S0 整块替换：div 计数允许不一致（P0 多了 action-box 3个div），故单独处理并校验全局平衡
if old_s0.count("<div") != S0_NEW.count("<div") or old_s0.count("</div>") != S0_NEW.count("</div>"):
    delta_o = S0_NEW.count("<div") - old_s0.count("<div")
    delta_c = S0_NEW.count("</div>") - old_s0.count("</div>")
    if delta_o != delta_c:
        errors.append("S0 整块替换 div 漂移不平衡 old(%d/%d) new(%d/%d)" % (
            old_s0.count("<div"), old_s0.count("</div>"), S0_NEW.count("<div"), S0_NEW.count("</div>")))
        print("  [FAIL] S0 div drift unbalanced")
    else:
        print("  [ok]   S0 div 净增 %d（action-box，平衡）" % delta_o)
else:
    print("  [ok]   S0 div 计数一致")
s = s[:S0_START] + S0_NEW + s[S0_END:]
print("DBG after S0:", s.count("<div"), s.count("</div>"))

# ---------- 5. S1 删除 3 张过期卡 (08-17 / 08-20 / 08-20) ----------
def remove_card(comment):
    global s
    if comment not in s:
        errors.append("S1 删除锚点缺失: " + comment)
        print("  [FAIL] missing " + comment)
        return
    ci = s.index(comment)
    marker = "\n      </div>\n"
    ce = s.index(marker, ci)
    end = ce + len(marker)
    s = s[:ci] + s[end:]
    print("  [ok]   removed: " + comment)

remove_card("      <!-- S1 Card: 中基协发文高质量发展路径 (08-17 P1) -->")
remove_card("      <!-- S1 Card: 中小公募摊余成本法债基重启15只上报 (08-20 P1) -->")
remove_card("      <!-- S1 Card: 本周5只公募REITs密集获批 (08-20 P1) -->")
print("DBG after S1 remove:", s.count("<div"), s.count("</div>"))

# ---------- 6. S1 新增 3 张卡（插入 card-grid 内，section 关闭前） ----------
S1_NEW = """
      <!-- S1 Card: 公募基金费率改革三年考·超1200亿四大费用结构生变 (09-04 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-04</span>
          </div>
          <div class="card-title">\U0001F7E1 公募基金费率改革三年考·超1200亿"四大费用"结构生变</div>
        </div>
        <div class="card-body">
          财经网9月4日梳理，自2023年7月费率改革启动三年、沿"管理人—券商—销售机构"三阶段推进，测算每年为投资者节省持有成本超<b>510亿元</b>；上半年全市场销售服务费合计<b>191.88亿元、同比+26.11%</b>（货币基金贡献66%）。<br>
          <b>结构变化：</b>管理费与交易佣金压降直接让利持有人，托管费上半年164.11亿同比+19.19%——近三年规模增43%而托管费仅增10.5%，改革成效显现。<br>
          <b>对腾安启示：</b>降费倒逼渠道从"卖产品"转向"做服务"，腾安须以配置能力与陪伴黏性对冲费率红利消退，巩固差异化。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://finance.caijing.com.cn/20260904/5181688.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财经网·09-04</span></a>
        </div>
      </div>

      <!-- S1 Card: 21家基金公司养老投教实验·Y份额留存率2倍于普通账户 (09-04 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-04</span>
          </div>
          <div class="card-title">\U0001F7E1 21家基金公司养老投教实验·Y份额留存率2倍于普通账户</div>
        </div>
        <div class="card-body">
          腾讯新闻9月4日报道，21家基金公司开展养老投教实验，从"被寻找"到"被遇见"——在企业、社区、高校三场景嵌入投教。调研揭示关键洞察：<b>Y份额买入一年留存率83.3%、换手率1.8%，分别为普通账户的2倍以上与三分之一</b>，"锁定效应"客观抑制追涨杀跌。<br>
          <b>痛点：</b>49.6%受访者已开户却未投资，近半账户"空转"；30-50岁群体"关注多投入少"。<br>
          <b>对腾安启示：</b>个人养老金Y份额是长期陪伴场景，腾安可借"分层投教+锁定效应"提升客户留存，将养老账户做成黏性入口。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://news.qq.com/rain/a/20260904A02UWY00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·09-04</span></a>
        </div>
      </div>

      <!-- S1 Card: 震荡市发行端分化·多只新基金延长募集期 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
          <div class="card-title">\U0001F7E1 震荡市发行端分化·多只新基金延长募集期主动择时</div>
        </div>
        <div class="card-body">
          证券时报（记者安仲文）9月3日报道，受市场扰动增多、前期获利筹码兑现影响，平安、南方、华泰保兴、创金合信等多家公募近期陆续发布新产品<b>延长募集</b>公告，放缓发行节奏。<br>
          <b>择时逻辑：</b>延长募集已成公募特殊"主动择时"手段——部分消费基金曾因规避7月初建仓风险延募至9月，又在消费回暖后缩短，一延一缩折射对主题窗口的判断。<br>
          <b>对腾安启示：</b>发行端降温预示风险偏好回落，宜强化低波固收+/防御型产品供给与投教，避免客户在震荡市追高权益新基。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.stcn.com/article/detail/4170027.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·09-03</span></a>
        </div>
      </div>
"""

anchor = "    </div>\n  </div>\n\n<!-- ============ Section 2:"
if s.count(anchor) != 1:
    errors.append("S1 插入锚点命中 %d 次" % s.count(anchor))
    print("  [FAIL] S1 insert anchor cnt=%d" % s.count(anchor))
else:
    s = s.replace(anchor, S1_NEW + anchor, 1)
    print("  [ok]   S1 新增3卡插入完成")
print("DBG after S1 insert:", s.count("<div"), s.count("</div>"))

# ---------- 7. S6 行情：09-02 收盘 -> 09-03 收盘 ----------
replace_once(
    '\U0001F4C8 上一交易日收盘（2026-09-02）·沪指3941.39 -0.97%·3901股下跌·成交1.82万亿',
    '\U0001F4C8 上一交易日收盘（2026-09-03）·沪指3942.09 +0.02%·窄幅震荡·成交1.76万亿',
    "s6-title")
replace_once(
    '            <span class="date-tag">09-02</span>',
    '            <span class="date-tag">09-03</span>',
    "s6-date")

OLD_S6_BODY = '''        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-02收盘·缩量普跌）</b><br>
              上证指数 <b>3941.39</b> <span style="color:#f5222d;">-0.97%</span><br>
              深证成指 <b>13611.55</b> <span style="color:#f5222d;">-1.88%</span><br>
              创业板指 <b>3312.24</b> <span style="color:#f5222d;">-2.39%</span><br>
              科创50 <b>1617.60</b> <span style="color:#f5222d;">-1.82%</span><br>
              北证50 <b>—</b> <span style="color:#52c41a;">+2.50%</span><br>
              沪深京成交 <b>1.82万亿</b>（较上日缩量约2300亿）<br>
              涨跌家数 <b>1541涨 / 3901跌</b>·银行护盘·54涨停8跌停
            </div>
            <div>
              <b>港股与美股（09-02收盘）</b><br>
              恒生指数 <b>25311.21</b> <span style="color:#f5222d;">-0.07%</span><br>
              恒生科技 <b>4517.16</b> <span style="color:#f5222d;">-0.74%</span><br>
              国企指数 <b>8450.10</b> <span style="color:#f5222d;">-0.15%</span><br>
              道琼斯 <b>53061.95</b> <span style="color:#52c41a;">+0.56%</span><br>
              纳斯达克 <b>26217.83</b> <span style="color:#52c41a;">+0.45%</span><br>
              标普500 <b>7666.60</b> <span style="color:#52c41a;">+0.46%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:8px;border-top:1px solid #f0f0f0;">
              <b>结构焦点：</b>9月2日A股缩量普跌，沪指跌0.97%报3941.39，深成指跌1.88%、创业板指跌2.39%，全市场3901只个股下跌、1541只上涨，成交降至1.82万亿。通信、有色、电子领跌，银行护盘、农业/军工局部活跃。受访人士称主因外部流动性收紧与地缘冲突升温、非基本面恶化；后续关注成交额能否重回1.9万亿。美股受油价与利率扰动分化，道指纳指小幅收涨。
            </div>
          </div>
        </div>'''

NEW_S6_BODY = '''        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-03收盘·窄幅震荡）</b><br>
              上证指数 <b>3942.09</b> <span style="color:#f5222d;">+0.02%</span><br>
              深证成指 <b>13625.12</b> <span style="color:#f5222d;">+0.10%</span><br>
              创业板指 <b>3312.54</b> <span style="color:#f5222d;">+0.01%</span><br>
              沪深京成交 <b>1.76万亿</b>（沪8198亿+深9390亿）<br>
              板块轮动·科技分化·红利消费局部活跃
            </div>
            <div>
              <b>港股与美股（09-03收盘）</b><br>
              恒生指数 <b>25213.31</b> <span style="color:#52c41a;">-0.39%</span><br>
              恒生科技 <b>4468.48</b> <span style="color:#52c41a;">-1.08%</span><br>
              国企指数 <b>8385.24</b> <span style="color:#52c41a;">-0.77%</span><br>
              道琼斯 <b>53686.11</b> <span style="color:#f5222d;">+1.18%</span><br>
              纳斯达克 <b>26584.06</b> <span style="color:#f5222d;">+1.40%</span><br>
              标普500 <b>7747.71</b> <span style="color:#f5222d;">+1.06%</span>
            </div>
            <div style="grid-column:1/-1;padding-top:8px;border-top:1px solid #f0f0f0;">
              <b>结构焦点：</b>9月3日A股窄幅震荡，沪指微涨0.02%报3942.09，深成指涨0.10%、创业板指涨0.01%，两市成交约1.76万亿，板块轮动加快、科技成长内部分化。港股小幅走弱、恒生科技跌逾1%；美股受经济数据提振全线收涨，道指纳指均涨超1%。
            </div>
          </div>
        </div>'''

replace_once(OLD_S6_BODY, NEW_S6_BODY, "s6-body")
replace_once(
    '            <span class="source-tag">同花顺iFind·2026-09-02收盘</span>',
    '            <span class="source-tag">同花顺iFind·2026-09-03收盘</span>',
    "s6-footer1")
replace_once(
    '<span class="source-tag">数据来源：上交所/国际金融报/腾讯新闻（09-02）</span>',
    '<span class="source-tag">数据来源：上交所/国际金融报/腾讯新闻（09-03）</span>',
    "s6-footer2")
print("DBG after s6:", s.count("<div"), s.count("</div>"))

# ---------- 8. S7 时间线：删最旧 08-26，增 09-04 ----------
OLD_S7_ITEM = '''      <!-- 08-26 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-26</div>
        <div class="timeline-title">证监会发布高质量发展意见·16条重塑公募底层逻辑</div>
      </div>
'''
if OLD_S7_ITEM not in s:
    errors.append("S7 删除锚点缺失 08-26")
    print("  [FAIL] S7 08-26 missing")
else:
    s = s.replace(OLD_S7_ITEM, "", 1)
    print("  [ok]   S7 删除 08-26 条目")

S7_INSERT_ANCHOR = 'padding:20px 24px;">\n            <!-- 09-03 时间线条目 (NEW) -->'
if s.count(S7_INSERT_ANCHOR) != 1:
    errors.append("S7 插入锚点命中 %d 次" % s.count(S7_INSERT_ANCHOR))
    print("  [FAIL] S7 insert anchor cnt=%d" % s.count(S7_INSERT_ANCHOR))
else:
    NEW_S7_ITEM = ('padding:20px 24px;">\n'
                   '            <!-- 09-04 时间线条目 (NEW) -->\n'
                   '      <div class="timeline-item">\n'
                   '        <div class="timeline-dot red"></div>\n'
                   '        <div class="timeline-date">2026-09-04</div>\n'
                   '        <div class="timeline-title">单周82只新基金启动发行·创单周纪录</div>\n'
                   '      </div>\n'
                   '            <!-- 09-03 时间线条目 (NEW) -->')
    s = s.replace(S7_INSERT_ANCHOR, NEW_S7_ITEM, 1)
    print("  [ok]   S7 新增 09-04 条目")
print("DBG after S7:", s.count("<div"), s.count("</div>"))

# =================== Phase1 全局断言 ===================
print("\n=== Phase1 全局断言 ===")
new_opens = s.count("<div")
new_closes = s.count("</div>")
need(new_opens == new_closes, "全局 div 平衡 open==close (%d/%d)" % (new_opens, new_closes))
need("待办跟踪" not in s, "S8 废弃：无'待办跟踪'")
need("腾安行动清单" not in s, "S8 废弃：无'腾安行动清单'")
need('id="s8"' not in s.lower(), "S8 废弃：无 s8 标记")
need(s.count("今日焦点") >= 1, "S0 标题存在")
need("9月4日 · 4条今日要闻" in s, "S0 section-context 正确")
# S0 段内 action-box / p0 卡
import re
s0_seg = s[s.index("        <!-- ============ Section 0:"):s.index("<!-- ============ Section 1:")]
need(s0_seg.count('class="card p0"') == 1, "S0 恰有1张 P0 卡")
need(s0_seg.count("action-box") == 1, "S0 恰有1个 action-box")
need(s0_seg.count('<div class="card ') == 4, "S0 恰有4张卡片")
# S7 条目数 12
s7_seg = s[s.index("<!-- ============ Section 7:"):s.index("</body>")]
need(s7_seg.count("timeline-item") == 12, "S7 时间线条目=12 (实际%d)" % s7_seg.count("timeline-item"))
# S1 卡片数 6（S1段）
s1_seg = s[s.index("<!-- ============ Section 1:"):s.index("<!-- ============ Section 2:")]
need(s1_seg.count('<div class="card ') == 6, "S1 卡片=6 (实际%d)" % s1_seg.count('<div class="card '))
# S2 不变，仍为4
s2_seg = s[s.index("<!-- ============ Section 2:"):s.index("<!-- ============ Section 3:")]
need(s2_seg.count('<div class="card ') == 4, "S2 卡片=4 (实际%d)" % s2_seg.count('<div class="card '))
# U+FFFD 零残留
need("\uFFFD" not in s, "无 U+FFFD 乱码")
# D级信源闸口
for bad in ["so.html5.qq.com", "toutiao", "企鹅号", "网易号", "搜狐号", "html5.qq.com"]:
    need(bad not in s, "信源闸口：无 D级 '%s'" % bad)

# =================== 写文件 ===================
if errors:
    print("\n[ABORT] 存在 %d 个断言失败，未写入文件：" % len(errors))
    for e in errors:
        print("  - " + e)
    raise SystemExit(1)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("\n[OK] 已写入 %s （div %d/%d）" % (PATH, new_opens, new_closes))
