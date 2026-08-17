# -*- coding: utf-8 -*-
import sys

PATH = "c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"

s = open(PATH, encoding="utf-8").read()

# ============ Phase 1: 所有断言（先断言，全部通过才写文件） ============
print("=== Phase 1: anchor assertions ===")

asserts = [
    ("marker 2026-07-15", '<!-- daily-update: 2026-07-15 -->', 1),
    ("fingerprint old (x2)", '清盘271只创新高|翻倍基瘦身225至74|费率改革三周年|主动ETF申请递交|半导体设备领涨', 2),
    ("date-badge old", '📅 数据区间：2026.07.01 — 2026.07.15（每日更新）', 1),
    ("S0 section-title old", '      <span class="section-title">今日焦点（7月15日·周三·清盘271只创新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交）</span>', 1),
    ("S0 Card 1 anchor", '          <!-- S0 Card 1:', 1),
    ("Section 1 anchor", '<!-- ============ Section 1: 重磅信息 ============ -->', 1),
    ("S6 card p3 anchor", '          <div class="card p3">', 1),
    ("Section 7 anchor", '<!-- ============ Section 7: 关键时间线 ============ -->', 1),
    ("timeline container", '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">', 1),
    ("timeline 07-01 entry", '      <!-- 07-01 时间线条目 (NEW) -->', 1),
    ("stat2 old block", '    <div class="stat-number">3972.51</div>', 1),
]

for name, anchor, expected in asserts:
    cnt = s.count(anchor)
    if cnt != expected:
        print(f"ANCHOR FAIL: {name} count={cnt} expected={expected}")
        sys.exit(1)
    print(f"  OK: {name} ({cnt})")

# 防御：确认当前没有 S8 残留（不应有，但保险）
if "Section 8" in s or "待办跟踪" in s or "腾安行动清单" in s:
    print("ANCHOR FAIL: 检测到 S8 残留元素")
    sys.exit(1)
print("  OK: 无 S8 残留")

# 防御：确认 marker 仍为 07-15（若主任务已抢先写成 07-16，则安全退出不污染）
if s.count('<!-- daily-update: 2026-07-16 -->') != 0:
    print("SAFE ABORT: 主任务已更新为 07-16，兜底不覆盖")
    sys.exit(0)

print("=== Phase 1 passed, all anchors OK ===\n")

# ============ Phase 2: 全部通过后才替换 ============
print("=== Phase 2: applying replacements ===")

# 1) marker
s = s.replace('<!-- daily-update: 2026-07-15 -->', '<!-- daily-update: 2026-07-16 -->')

# 2) meta + fingerprint (两处同内容)
old_fp = '清盘271只创新高|翻倍基瘦身225至74|费率改革三周年|主动ETF申请递交|半导体设备领涨'
new_fp = '信披新规二季报首披长期业绩|超300只货基7日年化破1%|基金经理离任238位创新高|头部公募举牌创新药|沪指07-15收3955.58'
s = s.replace(old_fp, new_fp)

# 3) date-badge
s = s.replace('📅 数据区间：2026.07.01 — 2026.07.15（每日更新）',
              '📅 数据区间：2026.07.02 — 2026.07.16（每日更新）')

# 4) S0 section-title
s = s.replace(
    '      <span class="section-title">今日焦点（7月15日·周三·清盘271只创新高·翻倍基大瘦身·费率改革三周年·主动ETF申请递交）</span>',
    '      <span class="section-title">今日焦点（7月16日·周四·货基收益破1%·信披新规首披长期业绩·基金经理离任创新高·公募举牌创新药）</span>')

# 5) S0 cards block (index-based: S0 Card 1 anchor -> Section 1 anchor)
s0_start = s.index('          <!-- S0 Card 1:')
s0_end = s.index('<!-- ============ Section 1: 重磅信息 ============ -->')
NEW_S0 = '''          <!-- S0 Card 1: 超300只货基7日年化跌破1%·收益率持续走低 (T+0 07-16 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 超300只货基7日年化跌破1%·基金收益率持续走低·理财通货基货架需重估收益预期</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>破1%蔓延：</b>Wind统计显示，截至7月13日全市场已有<b>315只</b>货币市场基金7日年化收益率低于1%，多家基金公司近期集中公告恢复常规管理费率或下调管理费，指向收益率持续走低。<br>
          <b>成因：</b>货币政策维持适度宽松、短端利率低位运行，货基底层资产收益同步下行；上半年货基规模仍稳居公募第一大类，但"保本高收益"预期已被打破。<br>
          <b>对腾安影响：</b>理财通货基是流量基本盘，收益下行直接削弱客户留存与转投吸引力→需前置管理收益预期、丰富低波替代货架。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1UOOTKO0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag high">货基收益：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 收益预期管理→在理财通货基页前置"7日年化下行"提示与同类低波替代（同业存单/短债），平滑客户心理落差；<br>
            ② 货架补位→加快现金管理类"货币+"组合与短债基金引入，承接收益敏感型资金，稳留存防流失。
          </div>
        </div>
      </div>
    <!-- S0 Card 2: 基金信披新规落地·二季报首披7年/10年长期业绩 (T+0 07-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 基金信披新规落地·二季报首披7年/10年长期业绩·行业长期价值导向凸显</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>新规首秀：</b>2026年基金二季报是信息披露新规落地后首批定期报告，成立满十年基金首次披露过去十年业绩，14只满十年基金中9只十年净值增长率超300%；中欧、平安、华富、长城等多家已披露7年/10年维度业绩。<br>
          <b>导向之变：</b>3月证监会修订信披准则（5月1日实施），季报新增7年/10年中长期业绩、不再披露近1月收益；4月《绩效考核管理指引》强调长周期考核、薪酬与投资者利益绑定。<br>
          <b>对基金行业影响：</b>考核"指挥棒"从规模/短期排名转向"以投资收益为核心、以基准和盈亏为约束"的长期主义。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1UJUIBL05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·上证报</span></a>
          <span class="impact-tag high">信披新规：高</span>
        </div>
      </div>
    <!-- S0 Card 3: 年内238位基金经理离任创同期新高 (T+0 07-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 年内238位基金经理离任创同期新高·但总人数4254人也新高·平均变动率19.01%处合理区间</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>离任创新高：</b>截至7月15日，年内已有<b>238位</b>公募基金经理离任，创历史同期新高，其中不乏管理规模超百亿甚至千亿的知名基金经理，引发人才流失担忧。<br>
          <b>理性看待：</b>公募基金经理总人数已达<b>4254人</b>同样创新高；反映行业稳定性的平均变动率约<b>19.01%</b>，远低于2015年同期的36.38%，较2022年同期亦回落——人才队伍稳步壮大、流动处合理区间。<br>
          <b>对基金行业影响：</b>离任多为市场演变、改革深化、竞争升级综合结果，倒逼产品供给更偏向持有期与逆向销售。
        </div>
        <div class="card-footer">
          <a href="https://stock.10jqka.com.cn/20260716/c678208671.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺·证券报头版</span></a>
          <span class="impact-tag medium">人才流动：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 头部公募密集举牌创新药 (T+0 07-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 头部公募密集举牌创新药·6/10-7/11易方达华夏富国汇添富增持并构成举牌</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>举牌升温：</b>港交所披露，6月10日至7月11日，易方达、华夏、富国、汇添富等多家头部公募出手增持创新药公司并已构成举牌；调研风向自6月起明显切换，机构频频组团走访生物医药企业。<br>
          <b>逻辑：</b>1—5月AI硬科技"吸金"致创新药调研冷清，步入6月后公募调研风向切回医药；新版《国家基本药物目录(2026年版)》9月1日施行，被视为创新药政策环境标志性转变。<br>
          <b>对基金行业影响：</b>创新药重获机构青睐→腾安可关注医药主题基金与科创药ETF的配置窗口。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L1UOOTKO0512B07B.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">创新药举牌：中</span>
        </div>
      </div>
    </div>
  </div>
'''
s = s[:s0_start] + NEW_S0 + s[s0_end:]

# 6) S6 card (index-based: S6 card p3 -> Section 7 anchor)
s6_start = s.index('          <div class="card p3">')
s7_index = s.index('<!-- ============ Section 7: 关键时间线 ============ -->')
NEW_S6 = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月15日（周三）·A股震荡收跌·沪指3955.58（-0.29%）·半导体跳水·医药银行护盘</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📊 A股07-15收盘（震荡调整·科技重挫）：</b><br>
              ▪ 沪指 <b>-0.29%</b>（3955.58）·深成指 <b>-0.97%</b>（14779.40）·创业板 <b>-1.21%</b>（3804.70）<br>
              ▪ 科创综指 <b>-3.48%</b>；沪深北三市成交约<b>2.59万亿</b>（缩量）<br>
              ▪ 板块：半导体大幅跳水、石油/有色走低；酿酒/医药/保险/券商/煤炭/银行拉升，创新药·医美活跃
            </div>
            <div>
              <b>📊 外围（07-15）：</b><br>
              ▪ 港股：恒指 <b>+1.40%</b>（24681.10）·恒生科技 <b>+1.30%</b>（4740.49）·医药股领涨（昭衍新药+23%）<br>
              ▪ 美股：道指 <b>+0.29%</b>（52658.64）·标普 <b>+0.38%</b>（7572.40）·纳指 <b>+0.62%</b>（26269.23）<br>
              ▪ 存储芯片重挫（美光/海力士ADR -8%~-9%）；中概金龙指数 <b>+2.92%</b>
            </div>
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-16（07-15收盘·沪指3955.58）</span>
            <span class="source-tag">数据来源：证券时报/腾讯财经/新华财经</span>
          </div>
      </div>
'''
s = s[:s6_start] + NEW_S6 + '\n  </div>\n' + s[s7_index:]

# 7) S7 timeline - remove 07-01 entry (T-15 超期)
old_0701 = '''      <!-- 07-01 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-07-01</div>
        <div class="timeline-title">上半年公募业绩收官</div>
      </div>
'''
s = s.replace(old_0701, '')

# 8) S7 timeline - add 07-16 entry (top)
old_container = '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">'
new_container = old_container + '\n    <!-- 07-16 时间线条目 (NEW) -->\n      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div class="timeline-date">2026-07-16</div>\n        <div class="timeline-title">基金信披新规落地·二季报首披十年长期业绩</div>\n      </div>'
s = s.replace(old_container, new_container)

# 9) Stats card 2 (上证综指 -> 07-15收盘)
old_stat2 = '''    <div class="stat-number">3972.51</div>
    <div class="stat-label">上证综指 · 07-15盘中（翻红+0.14%·创业板+0.74%高开·半导体活跃）</div>
    <div class="stat-change down">▼ 深成指+0.31%·油气黄金走弱</div>'''
new_stat2 = '''    <div class="stat-number">3955.58</div>
    <div class="stat-label">上证综指 · 07-15收盘（跌0.29%·半导体跳水·医药银行护盘）</div>
    <div class="stat-change down">▼ 深成指-0.97%·创业板-1.21%·成交2.59万亿</div>'''
s = s.replace(old_stat2, new_stat2)

# ============ 写回前最终校验 ============
print("=== Final validation ===")
assert s.count('<!-- daily-update: 2026-07-16 -->') == 1, "marker not set to 07-16"
assert s.count('<!-- daily-update: 2026-07-15 -->') == 0, "old marker still present"
# S0 四卡 date-tag 必须全 07-16
import re
s0_region = s[s.index('          <!-- S0 Card 1:'):s.index('<!-- ============ Section 1: 重磅信息 ============ -->')]
tags = re.findall(r'class="date-tag">(\d\d-\d\d)<', s0_region)
assert len(tags) == 4, f"S0 date-tag count={len(tags)} expected 4"
assert all(t == '07-16' for t in tags), f"S0 date-tag not all 07-16: {tags}"
# 无 T-2 违规：S0 全部 07-16 (T+0)
print("  S0 date-tags:", tags)
# Section 标记仍存在
assert '<!-- ============ Section 0: 今日焦点 ============ -->' in s
assert '<!-- ============ Section 6: 市场行情速览 ============ -->' in s
assert '<!-- ============ Section 7: 关键时间线 ============ -->' in s
# 无 S8 残留
assert 'Section 8' not in s and '待办跟踪' not in s and '腾安行动清单' not in s, "S8 residue detected!"
# 时间线条目数（07-16 + 07-15 + ... + 07-02）
tl = re.findall(r'class="timeline-date">(\d{4}-\d{2}-\d{2})<', s)
print("  timeline dates:", tl)
assert len(tl) <= 12, f"timeline count {len(tl)} > 12"
assert '2026-07-01' not in tl, "07-01 still in timeline (T-15 超期未删)"
assert '2026-07-16' in tl, "07-16 not in timeline"
# 无 07-15 盘中残留 in stats
assert '07-15盘中' not in s, "Stats still has 07-15盘中"

open(PATH, 'w', encoding='utf-8').write(s)
print("SUCCESS: index.html updated to 2026-07-16")
