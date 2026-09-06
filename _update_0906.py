# -*- coding: utf-8 -*-
"""daily-update 2026-09-06 (周日) — 基金行业资讯看板"""
import re, sys
from datetime import date, timedelta

PATH = 'index.html'
src = open(PATH, encoding='utf-8').read()
ORIG = src

today = date.today()
upper = today.strftime('%Y.%m.%d')
lower = (today - timedelta(days=14)).strftime('%Y.%m.%d')
assert upper == '2026.09.06', f'日期异常 {upper}'
assert lower == '2026.08.23', f'下界异常 {lower}'

# ============ Phase 1: 锚点预检 ============
anchors = {
    'header_badge': '📅 数据区间：',
    's0_start': '<!-- ============ Section 0: 今日焦点 ============ -->',
    's1_start': '<!-- ============ Section 1: 重磅信息 ============ -->',
    's7_first_comment': '            <!-- 09-05 时间线条目 (NEW) -->',
    's7_del_tail': '      <!-- 08-31 收盘 时间线条目 (NEW) -->',
}
for k, a in anchors.items():
    assert src.count(a) == 1, f'锚点 {k} 出现 {src.count(a)} 次'

# S0 旧块 div 计数
s0_i = src.index(anchors['s0_start'])
s1_i = src.index(anchors['s1_start'])
old_s0 = src[s0_i:s1_i]
o_s0 = old_s0.count('<div')
c_s0 = old_s0.count('</div')
assert o_s0 == c_s0, f'S0 旧块不平衡 o={o_s0} c={c_s0}'
print(f'[预检] S0 旧块 div {o_s0}/{c_s0}')

# ============ 构建新 S0（4 卡：1 P0 + 2 P1 + 1 P2） ============
card1 = '''      <!-- S0 Card 1 (09-06 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 含权二级债基·偏债混合基金拟纳入个人养老金名录·首批每家限报1只</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-06</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月6日电，监管近日下发《做好含权二级债基、偏债混合基金纳入个人养老金基金产品名录工作的通知》，推动符合条件的含权二级债基、偏债混合基金（含偏债混合FOF）纳入个人养老金基金产品名录，进一步丰富个人养老金产品谱系。<br>
          <b>六大标准：</b>①成立满3年且每日开放申购②最近4季度末规模均≥5亿③权益仓位（含权二级债基/偏债混合FOF近8季度末平均偏股仓位≥5%、普通偏债混合≥10%）④近3年最大回撤优于同类中位数⑤机构持有占比≤80%且前五大≤50%⑥管理人最近一期分类评价不为C类。<br>
          <b>节奏安排：</b>首批每家限报1只、9月8日前报送，后续按季度常态化筛选，并配套动态评估与奖优惩劣机制；截至6月30日个人养老金基金产品已达321只。<br>
          <b>对腾安启示：</b>个人养老金产品谱系扩容至"含权债基"、"固收+"等中低波品类，Y份额代销货架与税优投教场景同步打开，腾安应前置评估符合六标准产品的引入与适配。
        </div>
        <div class="card-footer">
          <a href="https://www.cnfin.com/gs-lb/detail/20260906/4465724_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-06</span></a>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 货架扩容→筛选符合六标准的含权二级债基/偏债混合基金，评估引入个人养老金Y份额；<br>
            ② 税优投教→借"含权债基入名录"节点，强化Y份额长期持有与税优宣传；<br>
            ③ 合规前置→跟踪首批名单与季度常态化筛选节奏，确保代销展示与适当性匹配。
          </div>
        </div>
      </div>
'''

card2 = '''
      <!-- S0 Card 2 (09-06 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 下周44只新基金发售·被动指数20只主导·细分ETF密集登场</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-06</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月6日电，下周（9月7日—9月11日）全市场共有44只新基金正式发售，其中被动指数型基金20只。<br>
          <b>细分赛道：</b>平安中证卫星产业ETF、嘉实中证全指红利质量ETF、国联国证港股通互联网ETF等多个细分赛道ETF即将开募；主动权益方面，中欧消费新机遇、朱雀消费动力、华泰保兴均衡回报等蓄势待发。<br>
          <b>发行背景：</b>本周82只新基金开启募集创单周历史纪录，8月以来超40只基金提前结募，增量资金持续入场。<br>
          <b>对腾安启示：</b>新基金供给持续放量、指数工具主导，代销端需以"严选+费率+陪伴"承接，避免客户在密集供给中追高跟风。
        </div>
        <div class="card-footer">
          <a href="https://www.cnfin.com/gs-lb/detail/20260906/4465722_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-06</span></a>
        </div>
      </div>
'''

card3 = '''
      <!-- S0 Card 3 (09-05 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 创业板算力ETF"一日结募"·天弘首只售罄·8只合计募超10亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          上证报中国证券网报道，9月4日首批8只创业板算力基础设施ETF集中发售，天弘创业板算力ETF（158061）当日提前结束募集（原定9月11日截止），成为该批首只结募产品，打响"闪电"发行战。<br>
          <b>募集热度：</b>据渠道人士透露，8只创业板算力ETF合计募集金额或超10亿元，在近期科技股调整背景下颇为亮眼；南方基金相关产品定于9月7日发售。<br>
          <b>产业逻辑：</b>创业板算力基础设施指数国产算力标的占比达74.5%、IDC权重超40%，直接受益国产替代与算力需求井喷。<br>
          <b>对腾安启示：</b>算力主题ETF一日结募印证硬科技赛道高景气，但短期拥挤度抬升，代销端应提示追高风险、引导分批布局。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/786276" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-05</span></a>
        </div>
      </div>
'''

card4 = '''
      <!-- S0 Card 4 (09-05 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 十余地证监局启动私募专项自查·落实国办54号文</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-05</span>
          </div>
        </div>
        <div class="card-body">
          界面新闻统计，上海、深圳、四川、广东等十余地证监局近期下发通知，要求辖区私募管理人对照国办54号文开展专项自查，湖南、海南、江苏等地报送时限已截止，其余多地集中在9—10月到期。<br>
          <b>核查重点：</b>新增基金份额违规代持、明股实债、不当利益输送、多层嵌套等此前反映集中的事项，并设自然人出资高于1000万元等量化核查指标。<br>
          <b>行业出清：</b>国内私募基金管理人自2022年2月峰值24683家降至2026年7月底18512家，净减6171家，常态化优胜劣汰持续。<br>
          <b>对腾安启示：</b>私募监管"1+N+X"体系加速成型、募集端从自律升级为行政监管，代销合作须严把私募管理人合规与适当性准入。
        </div>
        <div class="card-footer">
          <a href="https://www.sdenews.cn/html/2026/09/05/518007.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">山东财经网·09-05</span></a>
        </div>
      </div>
'''

new_s0 = '''<!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <div class="section-title-group">
        <span class="section-title">今日焦点</span>
        <span class="section-context">9月6日 · 4条今日要闻</span>
      </div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
''' + card1 + card2 + card3 + card4 + '''    </div>
  </div>
'''

# Phase1 断言新 S0 div 平衡
n_o = new_s0.count('<div')
n_c = new_s0.count('</div')
assert n_o == n_c, f'新 S0 不平衡 o={n_o} c={n_c}'
assert n_o - o_s0 == 3, f'S0 div 漂移异常 {o_s0} -> {n_o}'
print(f'[预检] 新 S0 div {n_o}/{n_c}，漂移 +{n_o - o_s0}（P0 action-box）')

# ============ S7 时间线：顶部插 2 条 09-06，底部删 2 条 08-31 ============
tl_new = '''            <!-- 09-06 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-06</div>
        <div class="timeline-title">含权二级债基拟纳入个人养老金名录</div>
      </div>
            <!-- 09-06 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-09-06</div>
        <div class="timeline-title">下周44只新基金启动发售</div>
      </div>
'''

tl_del = '''      <!-- 08-31 收盘 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-31</div>
        <div class="timeline-title">A股红盘收官·沪指3986.30 +0.86%</div>
      </div>
      <!-- 08-31 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-31</div>
        <div class="timeline-title">公募QDII额度首破千亿美元·证券基金类获增额</div>
      </div>
'''

assert src.count(tl_del) == 1, f'S7 删除块出现 {src.count(tl_del)} 次'
# S7 插入/删除 div 净 0
assert tl_new.count('<div') == tl_new.count('</div>')
assert tl_del.count('<div') == tl_del.count('</div>')
assert tl_new.count('<div') == tl_del.count('<div') == 8
print('[预检] S7 插入/删除各 8 div，净 0')

# ============ 执行替换 ============
# 1) header 区间
badge_old_re = re.compile(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）')
badge_new = f'📅 数据区间：{lower} — {upper}（每日更新）'
src2, n_badge = badge_old_re.subn(badge_new, src)
assert n_badge == 1, f'header badge 替换 {n_badge} 次'
print(f'[替换] header 区间 -> {badge_new}')

# 2) S0 整块
src2 = src2[:src2.index(anchors['s0_start'])] + new_s0 + '\n' + src2[src2.index(anchors['s1_start']):]

# 3) S7 顶部插入
s7c = anchors['s7_first_comment']
assert src2.count(s7c) == 1
src2 = src2.replace(s7c, tl_new + s7c, 1)

# 4) S7 底部删除
src2 = src2.replace(tl_del, '', 1)

# ============ Phase 2: 全量校验 ============
o = src2.count('<div')
c = src2.count('</div>')
print(f'[校验] 全文件 div open={o} close={c}')
assert o == c, f'div 不平衡 o={o} c={c}'
assert o - ORIG.count('<div') == 3, f'全局 div 漂移异常 {ORIG.count("<div")} -> {o}'

# S8 不存在
for kw in ['Section 8', '待办跟踪', '腾安行动清单']:
    assert kw not in src2, f'S8 残留 {kw}'

# S0 标题精确
assert '<span class="section-title">今日焦点</span>' in src2
assert '今日焦点（' not in src2
# context 数量匹配（4 卡）
m = re.search(r'<span class="section-context">(\d+)月(\d+)日 · (\d+)条今日要闻</span>', src2)
assert m, 'section-context 格式异常'
assert int(m.group(3)) == 4, f'context 卡片数 {m.group(3)} != 4'

# 无 U+FFFD
assert '\ufffd' not in src2, 'U+FFFD 残留'

# S0 P0 有 action-box（仅 1 个，切 S0 段统计）
s0_new_seg = src2[src2.index('<!-- ============ Section 0: 今日焦点'):src2.index('<!-- ============ Section 1: 重磅信息')]
assert s0_new_seg.count('class="action-box"') == 1, 'S0 action-box 数 != 1'

# date-tag 时效（S0 内不得早于 T-14=08-23；且 S0 无 T-2）
s0_tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', s0_new_seg)
print('[校验] S0 date-tags =', s0_tags)
for mm, dd in s0_tags:
    d = date(today.year, int(mm), int(dd))
    assert d >= today - timedelta(days=1), f'S0 含 T-2 或更早 {d}'

# 黑名单域名（只校验今天新写入的 S0 段；S3/S5 历史 so.html5.qq.com 残留属周巡检范围，不阻断今日提交）
for bad in ['21jingji', 'stcn.com', 'cls.cn', 'guba.eastmoney', 'yicai.com', 'toutiao', 'so.html5.qq.com', '网易号', '企鹅号', '搜狐号']:
    assert bad not in s0_new_seg, f'S0 新段黑名单残留 {bad}'

print('\n✅ Phase2 全部断言通过，写回文件')
open(PATH, 'w', encoding='utf-8').write(src2)
print('DONE')
