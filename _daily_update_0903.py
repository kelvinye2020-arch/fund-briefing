# -*- coding: utf-8 -*-
import io, sys

PATH = r"c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

orig = content
errors = []
def check(cond, msg):
    if not cond:
        errors.append(msg); print("  [FAIL] " + msg)
    else:
        print("  [ok] " + msg)

def find_card_bounds(content, title, has_s1_comment=False):
    i = content.index(title)
    win = max(0, i - 600)
    if has_s1_comment:
        open_start = content.rfind('      <!-- S1 Card:', win, i)
        if open_start == -1:
            open_start = content.rfind('\n      <div class="card p', win, i) + 1
    else:
        open_start = content.rfind('\n      <div class="card p', win, i) + 1
    # nest-scan from open_start
    depth = 0
    j = open_start
    n = len(content)
    card_close_end = None
    while j < n:
        lt = content.find('<', j)
        if lt == -1:
            break
        if content.startswith('<div', lt):
            depth += 1
            j = content.find('>', lt) + 1
        elif content.startswith('</div>', lt):
            depth -= 1
            j = content.find('>', lt) + 1
            if depth == 0:
                card_close_end = j
                break
        else:
            j = lt + 1
    if card_close_end is None:
        raise RuntimeError("card close not found for: " + title)
    return open_start, card_close_end

def replace_card(content, title, new_card, has_s1_comment=False):
    os_, ce = find_card_bounds(content, title, has_s1_comment)
    old = content[os_:ce]
    print("    [bounds] old open/close=%d/%d  new open/close=%d/%d" % (
        old.count('<div'), old.count('</div>'), new_card.count('<div'), new_card.count('</div')))
    return content[:os_] + new_card + content[ce:]

# ---------------- 1. Stats Bar card 2 ----------------
print("== Stats Bar ==")
stat_start = content.index('      <div class="stat-number">3979.89</div>')
stat_card_open = content.rfind('    <div class="stat-card">\n', 0, stat_start)
stat_card_end = content.find('    </div>\n', stat_start) + len('    </div>\n')
NEW_STAT2 = '''    <div class="stat-card">
      <div class="stat-number">3941.39</div>
      <div class="stat-label">沪指9-2收盘·跌0.97%·9月前两日A股连跌·成交1.82万亿</div>
      <div class="stat-change down">▼ 深成指-1.88%·创业板-2.39%·3901股下跌</div>
    </div>
'''
content = content[:stat_card_open] + NEW_STAT2 + content[stat_card_end:]
check('3979.89' not in content.split('<!-- Stats Bar -->')[1].split('<!-- ============ Section 0')[0], "old 3979.89 stat removed")

# ---------------- 2. S0 whole block ----------------
print("== S0 今日焦点 ==")
s0_start = content.index('            <!-- S0 Card 1 (09-02 P0) -->')
s0_end = content.index('    </div>\n  </div>\n<!-- ============ Section 1')
NEW_S0 = '''      <!-- S0 Card 1 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 新基金频频延长募集期·震荡市公募主动择时拖延建仓</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
        </div>
        <div class="card-body">
          证券时报记者安仲文报道，受市场扰动增多、前期获利筹码兑现影响，平安、南方、华泰保兴、创金合信等多家公募近期陆续发布新产品<b>延长募集</b>公告，放缓发行节奏。<br>
          <b>择时逻辑：</b>延长募集已成公募特殊"主动择时"手段——某上海公募消费基金曾因规避7月初建仓风险将募集延至9月，又在消费回暖后缩短至8月10日，一延一缩折射对主题窗口的判断。<br>
          <b>对腾安启示：</b>发行端降温预示风险偏好回落，宜强化低波固收+/防御型产品供给与投教，避免客户在震荡市追高权益新基。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/4170027.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报·09-03</span></a>
        </div>
      </div>

      <!-- S0 Card 2 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 年内公募参与A股定增获配超451亿·同比+160%·电子最受青睐</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
        </div>
        <div class="card-body">
          公募排排网数据，截至8月31日，年内27家公募机构参与90家A股公司定增，<b>合计获配451.44亿元，较去年同期173.53亿大增160.15%</b>；按8月31日收盘价测算整体浮盈37.55亿、浮盈率8.32%。<br>
          <b>行业分布：</b>电子行业最受青睐——参与15只个股、获配88.49亿居首；煤炭（中国神华63.80亿）、电力设备（61.33亿）紧随其后。21家机构获配超1亿，3家头部公募获配破百亿。<br>
          <b>逻辑：</b>定增折价提供安全垫、平滑净值波动，与权益基金长期价值投资理念契合；公募凭研究优势逐步成为定增重要买方，定价更趋理性。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&amp;id=SN2026090309310298e038bf" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺·09-03</span></a>
        </div>
      </div>

      <!-- S0 Card 3 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 个人投资者加速涌入ETF·上半年占比31.22%·配置能力待提升</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
        </div>
        <div class="card-body">
          Wind数据显示，上半年个人投资者在全部ETF中占比<b>31.22%，较2025年末21.63%明显提升</b>；股票型ETF个人占比由21.11%升至36.52%，行业指数ETF个人占比突破51%。<br>
          <b>隐忧：</b>中信证券等联合《2026 ETF客户投资行为洞察报告》显示，超六成投资者无标准化仓位规则、超四成从未用估值/资金监控工具，追高跨境ETF溢价后遭回调，"投ETF也亏钱"抱怨增多。<br>
          <b>对腾安启示：</b>ETF个人化趋势确定，但"买产品"≠"做配置"——须加强ETF配置框架投教与智能辅助工具，引导从交易思维转向配置思维。
        </div>
        <div class="card-footer">
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260903/6323014.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·09-03</span></a>
        </div>
      </div>

      <!-- S0 Card 4 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 9月开门红落空·公募集体发声：短期扰动不改中期趋势</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
        </div>
        <div class="card-body">
          9月前两个交易日A股延续调整，沪指两连跌、成长板块领跌（9月2日沪指3941.39 -0.97%、创业板-2.39%、成交降至1.82万亿）。多家公募解读称产业趋势未改，建议耐心等待共识。<br>
          <b>机构观点：</b>科技成长主线未发生逆转，短期回调主因外部流动性收紧与地缘冲突升温、前期获利盘兑现，并非基本面恶化；结构性行情与高低切换仍将延续。<br>
          <b>对腾安启示：</b>市场震荡期更需做好客户预期管理与持有陪伴，借回调引导理性定投、避免追涨杀跌。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260903A0332H00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·中国基金报·09-03</span></a>
        </div>
      </div>
'''
content = content[:s0_start] + NEW_S0 + content[s0_end:]
content = content.replace('        <span class="section-context">9月2日 · 4条今日要闻</span>',
                          '        <span class="section-context">9月3日 · 4条今日要闻</span>')
check('9月3日 · 4条今日要闻' in content, "S0 section-context updated")
check(content.split('<!-- ============ Section 0')[1].split('section-title">')[1].split('<')[0] == '今日焦点', "S0 title exact")

# ---------------- 3. S2 ----------------
print("== S2 监管政策 ==")
NEW_QDII_REPL = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
          <div class="card-title">🟡 交易外接新规落地·中证协中基协联合发布·划定六条红线</div>
        </div>
        <div class="card-body">
          8月28日，中国证券业协会与中国证券投资基金业协会联合发布《证券公司交易信息系统接入管理规范（试行）》，自发布之日起施行，同步废止2015年版外部接入规范。<br>
          <b>核心要求：</b>落实交易资源公平原则，证券公司不得为特定客户提供技术或业务资源差异化安排；划定多项禁止性红线——不得让渡系统管理责任、不得为场外配资/违规出借账户提供便利、不得修改系统参数引发交易不公平。<br>
          <b>对公募影响：</b>首次系统明确私募及公募资管产品接入标准；公募基金及私募资管产品适用"资格放行、行为严管"，须排查存量外接、拆除专属通道、配合券商备案，防范通道中断传导风险。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="http://sc.stock.cnfol.com/gushijujiao/20260903/32358364.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·09-03</span></a>
        </div>
      </div>
'''
content = replace_card(content, '外汇局重罚QDII违规·国泰海通资管被罚没5254.74万·跨境业务合规红线收紧', NEW_QDII_REPL)
check('交易外接新规落地' in content and '外汇局重罚QDII违规' not in content, "S2: 交易外接新规 replaced QDII")

NEW_ZB_REPL = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
          <div class="card-title">🟡 私募信披新规正式实施·9月1日施行·从自律升级为部门规章</div>
        </div>
        <div class="card-body">
          9月1日，《私募投资基金信息披露监督管理办法》正式施行，作为首部落实《私募投资基金监督管理条例》的行政规章，将私募信披监管从行业自律规则提升至<b>部门规章</b>，压实管理人、托管人、销售机构多方责任。<br>
          <b>核心变化：</b>一是穿透式披露——基金嵌套投向其他资管产品须穿透至底层资产；二是差异化定期报告节奏（证券类季报送、股权类半年报）；三是违规处罚升级，机构最高罚20万并追责主管人员。<br>
          <b>行业影响：</b>"扶优限劣"加速洗牌，资金将流向内控完善、运作规范的管理人；核心投资运作纳入披露范围，投资者知情权从"合同约定"上升为监管法定权利。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.cfbond.com/14740/14740zgcfw/ejy/yw/4896212632.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国财富网（中国证券报）·09-03</span></a>
        </div>
      </div>
'''
content = replace_card(content, '上半年22家基金公司营收净利双增38%', NEW_ZB_REPL)
check('私募信披新规正式实施' in content and '上半年22家基金公司营收净利双增38%' not in content, "S2: 私募信披新规 replaced 中报业绩")

# ---------------- 4. S1 ----------------
print("== S1 重磅信息 ==")
NEW_YL_REPL = '''      <!-- S1 Card: 券商上半年净利1533亿 (09-03 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-03</span>
          </div>
          <div class="card-title">🟡 上市券商上半年净利1533亿·同比+50%·头部集中度再攀升</div>
        </div>
        <div class="card-body">
          据统计，42家A股上市券商上半年合计营收<b>3508.73亿元、同比+45.4%</b>，合计净利<b>1533.05亿元、同比+50%</b>，期末总资产17.36万亿、同比+34%。<br>
          <b>头部格局：</b>中信证券238.88亿居首、国泰海通209.52亿次之，两家占全行业近三成；净利破百亿券商由2家扩至5家（华泰、广发、招商入列），招商同比+104.9%翻倍；前五大券商贡献52.1%利润、前十大占74.3%。<br>
          <b>对腾安启示：</b>券商盈利大增印证资本市场环境向好、经纪与自营双轮驱动；券商作为代销竞品加速"买方投顾"转型，腾安须以"严选+AI陪伴"巩固差异化。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.mrjjxw.com/articles/2026-09-03/4571136.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-03</span></a>
        </div>
      </div>
'''
content = replace_card(content, '医药基金业绩大幅回升·多只主动医药基区间涨幅突破30%', NEW_YL_REPL, has_s1_comment=True)
check('上市券商上半年净利1533亿' in content and '医药基金业绩大幅回升' not in content, "S1: 券商净利 replaced 医药")

# ---------------- 5. S6 ----------------
print("== S6 行情 ==")
s6_start = content.index('            <div class="card p3">')
s6_end = content.index('      </div>  </div>\n\n<!-- ============ Section 7')
NEW_S6 = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-02）·沪指3941.39 -0.97%·3901股下跌·成交1.82万亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-02</span>
          </div>
        </div>
        <div class="card-body">
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
        </div>
          <div class="card-footer">
            <span class="source-tag">同花顺iFind·2026-09-02收盘</span>
            <span class="source-tag">数据来源：上交所/国际金融报/腾讯新闻（09-02）</span>
          </div>
      </div>  </div>'''
content = content[:s6_start] + NEW_S6 + content[s6_end + len('      </div>  </div>'):]
check('2026-09-02收盘' in content, "S6: date updated to 09-02")

# ---------------- 6. S7 ----------------
print("== S7 时间线 ==")
for old in (
    '      <!-- 08-22 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-08-22</div>\n        <div class="timeline-title">第三批业绩基准调整落地·87家参与</div>\n      </div>\n',
    '      <!-- 08-28 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-08-28</div>\n        <div class="timeline-title">A股缩量微跌·沪指-0.11%·科技冲高回落</div>\n      </div>\n',
    '      <!-- 08-27 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-08-27</div>\n        <div class="timeline-title">A股放量普涨·沪指重回3950点·科创50大涨</div>\n      </div>\n',
    '      <!-- 08-29/-30 盈利占比披露条目 (NEW) -->\n'):
    if old in content:
        content = content.replace(old, '')
        print("  [ok] removed: " + old.split('\n')[0].strip())
    else:
        errors.append("S7 block missing: " + old.split('\n')[0]); print("  [FAIL] missing: " + old.split('\n')[0])

insert_block = '''            <!-- 09-03 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-03</div>
        <div class="timeline-title">公募参与A股定增获配超451亿·同比+160%</div>
      </div>
            <!-- 09-03 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-03</div>
        <div class="timeline-title">交易外接新规落地·中证协中基协联合发布</div>
      </div>
            <!-- 09-02 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-02</div>
        <div class="timeline-title">A股缩量普跌·沪指3941.39 -0.97%</div>
      </div>
'''
anchor = '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">\n            <!-- 09-01 时间线条目 (NEW) -->'
check(anchor in content, "S7 anchor present")
content = content.replace(anchor, '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">\n' + insert_block + '            <!-- 09-01 时间线条目 (NEW) -->')

# ---------------- 7. Integrity ----------------
print("== Integrity ==")
n_open, n_close = content.count('<div'), content.count('</div>')
check(n_open == n_close, "div balance %d/%d" % (n_open, n_close))
check('\ufffd' not in content, "no U+FFFD garbled chars")
check('S8' not in content and '待办跟踪' not in content and '腾安行动清单' not in content, "S8 section absent")
s0_sec = content.split('<!-- ============ Section 0')[1].split('<!-- ============ Section 1')[0]
check(s0_sec.count('class="card p') == 4, "S0 4 cards (got %d)" % s0_sec.count('class="card p'))
s1_sec = content.split('<!-- ============ Section 1')[1].split('<!-- ============ Section 2')[0]
check(s1_sec.count('class="card p') == 6, "S1 6 cards (got %d)" % s1_sec.count('class="card p'))
s2_sec = content.split('<!-- ============ Section 2')[1].split('<!-- ============ Section 3')[0]
check(s2_sec.count('class="card p') == 4, "S2 4 cards (got %d)" % s2_sec.count('class="card p'))
s7_sec = content.split('<!-- ============ Section 7')[1].split('</div>\n\n</body>')[0]
check(s7_sec.count('timeline-item') == 12, "S7 12 items (got %d)" % s7_sec.count('timeline-item'))

if errors:
    print("\nERRORS:", errors)
    sys.exit(1)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("\nWROTE %d -> %d bytes (delta %d)" % (len(orig), len(content), len(content)-len(orig)))
print("DONE")
