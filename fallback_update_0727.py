# -*- coding: utf-8 -*-
# 兜底补位更新 2026-07-27（两阶段：先断言，全部通过后才写入）
import sys

PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()
div_open_before = s.count('<div')
div_close_before = s.count('</div>')

# ============ Phase 1: 全部断言 ============
A_MARKER = '<!-- daily-update: 2026-07-26 -->'
A_FP = '<meta name="content-fingerprint" content="A股缩量普跌沪指失守|公募史上最大科技抱团|电子通信持仓近60%|银行系公募规模破7万亿|二季报披露收官">'
A_S0_START = '<!-- ============ Section 0: 今日焦点 ============ -->'
A_S1_START = '<!-- ============ Section 1: 重磅信息 ============ -->'
A_S6_TITLE = '<div class="card-title">2026年7月25日（周六·休市）·展示07-24收盘·A股缩量普跌成交破2万亿·美股企稳分化</div>'
A_S7_FIRST = '      <!-- 07-25 时间线条目 (NEW) -->'

anchors = [A_MARKER, A_FP, A_S0_START, A_S1_START, A_S6_TITLE, A_S7_FIRST]
ok = True
for a in anchors:
    c = s.count(a)
    if c != 1:
        print(f'ANCHOR FAIL: {a[:60]}... count={c}')
        ok = False
if not ok:
    sys.exit(1)
if s.index(A_S0_START) >= s.index(A_S1_START):
    print('ORDER FAIL: S0 must precede S1')
    sys.exit(1)
print('Phase 1: all anchors OK')

# ============ Phase 2: 替换 ============
# 1) marker
s = s.replace(A_MARKER, '<!-- daily-update: 2026-07-27 -->')

# 2) fingerprint
s = s.replace(A_FP, '<meta name="content-fingerprint" content="绩优基金提前减仓科技分歧|公募规模39.67万亿费率改革|北交所持有期基金首批上报|实时估值服务卷土重来|主动权益单季利润破万亿">')

# 3) S6 标题行（周一，维持07-24上周五收盘口径）
s = s.replace(A_S6_TITLE, '<div class="card-title">2026年7月27日（周一·早间）·展示07-24（上周五）收盘·A股缩量普跌成交破2万亿·美股企稳分化</div>')

# 4) 整体重建 S0 区域（Section 0 起点 → Section 1 起点）
NEW_S0 = '''<!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（7月27日·绩优基金提前减仓科技现巨大分歧·公募规模39.67万亿费率改革深化·首批北交所持有期基金上报）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">

      <!-- S0 Card 1: 绩优基金提前减仓·公募对科技赛道现巨大分歧 (T+0 07-27 P0 带action-box) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 科技赛道大幅回调·部分重仓基金回撤超四成·绩优基金经理二季度已提前减仓·公募对后市现巨大分歧</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">07-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>回撤惨烈：</b>下半年以来科技细分赛道大幅回调、行情快速降温，部分重仓科技个股的基金<b>回撤幅度突破四成</b>；而一批上半年绩优基金经理早在二季度便主动降仓、分散行业配置，减持高估值科技标的、布局传统价值板块，靠提前避险大幅收窄回撤，跑赢行业平均。<br>
          <b>巨大分歧：</b>公募行业对科技后市判断严重分裂——争议核心在于当前科技估值是<b>已脱离基本面合理区间</b>，还是即将迈入由坚实产业供需支撑的<b>超级周期</b>。叠加上周五A股缩量普跌、电子+通信持仓近60%的历史极值抱团，博弈烈度持续放大。<br>
          <b>对基金行业影响：</b>科技主题基金业绩剧烈分化→腾安需重点甄别"提前减仓型"绩优管理人，回避高位满仓押注型产品。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_3036a669e1e72252" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">人民财讯</span></a>
          <span class="impact-tag high">科技回撤风险：高</span>
        </div>
        <div class="action-box">
          <div class="action-title">⚡ 腾安行动建议</div>
          <div class="action-text">科技主题基金回撤最大已超四成、公募多空分歧公开化：① 立即梳理货架上科技暴露过高的主动权益产品，标注回撤与拥挤度风险；② 优先推荐二季度已主动降仓、行业分散的绩优管理人，用二季报持仓数据做客观筛选依据；③ 客户沟通强调"分散配置+均衡风格"，对高位申购科技主题的客户做适当性提示。</div>
        </div>
      </div>

      <!-- S0 Card 2: 公募总规模39.67万亿创新高·费率改革撬动行业变局 (T+0 07-27 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募总规模39.67万亿再创新高·费率改革撬动行业变局·0.15%低费率基金增至2343只</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>规模新高：</b>中基协最新数据，截至6月底境内公募基金资产净值合计<b>39.67万亿元</b>再创历史新高。截至7月26日全市场基金平均管理费率降至<b>0.6787%</b>；管理费率0.15%的基金达<b>2343只</b>，较年初增加203只、同比增加419只。<br>
          <b>逻辑切换：</b>费率改革推动竞争逻辑从"规模扩张"转向"价值创造"——费率≤0.15%且成立满三年的1159只基金中，<b>852只（超七成）</b>近三年净值增长超业绩基准，其中100只超基准10%以上。晨星李一鸣：基金公司经营不能再单纯依赖规模增长衡量。<br>
          <b>对基金行业影响：</b>低费率+长期业绩挂钩成主流→腾安选品可把"费率性价比+超基准能力"纳入货架筛选硬指标。
        </div>
        <div class="card-footer">
          <a href="https://www.toutiao.com/article/7666877953640284710/" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">经济观察网</span></a>
          <span class="impact-tag medium">费率变局：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 首批北交所3个月持有期主题基金上报·8家管理人确定 (T+0 07-27 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 首批北交所三个月持有期主题基金即将上报·华夏易方达等8家管理人确定·公募布局北交所再扩容</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>产品创新：</b>首批北交所三个月持有期主题基金自7月24日起陆续向证监会递交注册申请，已确定<b>华夏、易方达、汇添富、南方、嘉实、东财、富国、中信建投</b>8家管理人，公募布局北交所进一步扩容。<br>
          <b>增量意义：</b>持有期设计有助于引导资金长期化，将进一步丰富北交所投资产品、吸引增量资金进场、改善二级市场流动性，助力创新型中小企业估值修复。此前财通证券周报亦提示：主动权益基金二季度单季总利润<b>首度破万亿</b>，市场赚钱效应向纵深扩散。<br>
          <b>对基金行业影响：</b>北交所主题货架从无到有→腾安可提前跟踪首批产品审批进度，储备"专精特新"细分品类。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260727A02XM100" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·中证报</span></a>
          <span class="impact-tag medium">产品扩容：中</span>
        </div>
      </div>

      <!-- S0 Card 4: 基金实时估值服务卷土重来·监管整治乱象 (T+0 07-27 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 基金实时估值服务卷土重来·散布理财APP/公众号/小红书·业内建议两大方向整治乱象</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>乱象抬头：</b>受市场高波动行情催化，沉寂许久的基金<b>实时估值服务</b>再度卷土重来，已转向更灵活、隐蔽的运营模式，广泛散布于理财APP、公众号、小程序、小红书等平台，因方式隐蔽更难监管。<br>
          <b>整治方向：</b>业内人士建议在金融持牌资质明确规定的基础上从两大方向突破：一是<b>完善行为界定标准</b>、优化对变相规避监管行为的识别；二是<b>丰富合规替代服务供给</b>，有效疏导市场真实需求。<br>
          <b>对基金行业影响：</b>极致科技行情下客户盯盘需求旺盛→腾安可评估合规的净值预估/持仓透视服务，抢占合规替代供给窗口。
        </div>
        <div class="card-footer">
          <a href="https://so.html5.qq.com/page/real/search_news?docid=70000021_0366a669d0794552" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag low">合规服务：中</span>
        </div>
      </div>
    </div>
  </div>

'''
i0 = s.index(A_S0_START)
i1 = s.index(A_S1_START)
s = s[:i0] + NEW_S0 + s[i1:]

# 5) S7 新增 07-27 条目（插在 07-25 条目之前），并保持 <=12 条
NEW_TL = '''      <!-- 07-27 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-27</div>
        <div class="timeline-title">绩优基金提前减仓·公募对科技后市现巨大分歧</div>
      </div>

'''
s = s.replace(A_S7_FIRST, NEW_TL + A_S7_FIRST)

# ============ 校验 ============
assert s.count('<!-- daily-update: 2026-07-27 -->') == 1
assert s.count('<!-- ============ Section 0:') == 1
assert s.count('<!-- ============ Section 1:') == 1
assert s.count('<!-- ============ Section 6:') == 1
assert s.count('<!-- ============ Section 7:') == 1
assert s.count('Section 8') == 0, 'S8 residue!'
assert 'timeline-desc' not in s, 'timeline-desc residue!'
tl_count = s.count('<div class="timeline-item">')
assert tl_count <= 12, f'timeline {tl_count} > 12'
div_open = s.count('<div')
div_close = s.count('</div>')
delta_before = div_open_before - div_close_before
delta_after = div_open - div_close
assert delta_before == delta_after, f'div balance changed: before {delta_before}, after {delta_after}'
# S0 date-tag 时效校验（周一允许 T-3=07-24，但本次全部 07-27）
import re
i0n = s.index(A_S0_START); i1n = s.index(A_S1_START)
tags = re.findall(r'date-tag">([\d-]+)<', s[i0n:i1n])
assert all(t == '07-27' for t in tags), f'date-tag violation: {tags}'

open(PATH, 'w', encoding='utf-8').write(s)
print(f'SUCCESS: timeline={tl_count}, div {div_open}/{div_close} (delta {delta_after}), S0 tags={tags}')
