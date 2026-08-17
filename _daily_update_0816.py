# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with open(P, "r", encoding="utf-8") as f:
    s = f.read()

# ---------- Phase 1: 锚点预检 ----------
checks = {
    "S6 card open": '<div class="card p3">',
    "S6 card-title": '上一交易日收盘（2026-08-13 周四）',
    "S6 footer src": '同花顺iFind·2026-08-13收盘',
    "S7 item 0804": 'timeline-date">2026-08-04<',
    "S7 item 0805": 'timeline-date">2026-08-05<',
    "S1 card 40drift comment": '<!-- S1 Card NEW: 40只基金疑似风格漂移 (08-15) -->',
    "S1 card 272 comment": '<!-- S1 Card NEW: 272只基金突破双十限制 (08-14) -->',
    "no S8": 'Section 8',
}
for name, anchor in checks.items():
    if name == "no S8":
        assert anchor not in s, "S8 残留！禁止重建"
        continue
    cnt = s.count(anchor)
    assert cnt == 1, f"锚点 [{name}] 出现 {cnt} 次，预期 1"
print("Phase1 锚点预检通过")

# 记录原始 div 计数
o0 = s.count("<div")
c0 = s.count("</div>")

# ============ 1. S6 更新为 08-15 收盘 ============
# 替换 card-title
old_title = '📈 上一交易日收盘（2026-08-13 周四）·三大指数冲高回落集体收绿·医药逆势领涨'
new_title = '📈 上一交易日收盘（2026-08-15 周五）·三大指数窄幅整理沪指微红·算力链走强'
assert s.count(old_title) == 1
s = s.replace(old_title, new_title)

# 替换 card-body 内部行情数据块（保留五层嵌套结构：card-body>grid>左栏+右栏+焦点条）
old_body_left = """              <b>A股（收盘）</b><br>
              上证指数 <b>3926.96</b> <span style="color:#52c41a;">-0.50%</span><br>
              深证成指 <b>14289.44</b> <span style="color:#52c41a;">-0.87%</span><br>
              创业板指 <b>3586.04</b> <span style="color:#52c41a;">-0.45%</span><br>
              科创50 <b>1717.75</b> <span style="color:#52c41a;">-1.11%</span><br>
              北证50 <b>1097.80</b> <span style="color:#52c41a;">-1.62%</span><br>
              两市成交 <b>2.55万亿</b>（较上日<span style="color:#f5222d;">放量3985亿</span>）<br>
              涨跌家数 1143 涨 / <b>4317 跌</b>（涨停62、跌停4）"""
new_body_left = """              <b>A股（收盘）</b><br>
              上证指数 <b>3927.18</b> <span style="color:#f5222d;">+0.01%</span><br>
              深证成指 <b>14354.31</b> <span style="color:#f5222d;">+0.45%</span><br>
              创业板指 <b>3626.30</b> <span style="color:#f5222d;">+1.12%</span><br>
              科创50 <b>1717.75</b> <span style="color:#52c41a;">0.00%</span><br>
              北证50 <b>1086.91</b> <span style="color:#52c41a;">-0.94%</span><br>
              两市成交 <b>2.16万亿</b>（较上日<span style="color:#52c41a;">缩量4114亿</span>）<br>
              涨跌家数 超2000 涨 / <b>2900 跌</b>（涨停约60、跌停约10）"""
assert s.count(old_body_left) == 1
s = s.replace(old_body_left, new_body_left)

old_body_right = """              <b>港股与美股（收盘）</b><br>
              恒生指数 <b>25396.51</b> <span style="color:#52c41a;">-0.17%</span><br>
              恒生科技 <b>4792.39</b> <span style="color:#f5222d;">+0.33%</span><br>
              国企指数 <b>8426.49</b> <span style="color:#52c41a;">-0.23%</span><br>
              道琼斯 <b>53839.99</b> <span style="color:#f5222d;">+0.13%</span><br>
              纳斯达克 <b>26803.03</b> <span style="color:#f5222d;">+0.81%</span><br>
              标普500 <b>7798.99</b> <span style="color:#f5222d;">+0.65%</span><br>
              日经225 <b>68308.59</b> <span style="color:#f5222d;">+1.16%</span>｜韩KOSPI <b>6813.34</b> <span style="color:#f5222d;">+3.56%</span>"""
new_body_right = """              <b>港股与美股（收盘）</b><br>
              恒生指数 <b>25116.85</b> <span style="color:#52c41a;">-1.10%</span><br>
              恒生科技 <b>4708.19</b> <span style="color:#52c41a;">-1.77%</span><br>
              国企指数 <b>8362.31</b> <span style="color:#52c41a;">-1.02%</span><br>
              道琼斯 <b>53750.11</b> <span style="color:#52c41a;">-0.20%</span><br>
              纳斯达克 <b>26728.55</b> <span style="color:#52c41a;">-0.28%</span><br>
              标普500 <b>7785.11</b> <span style="color:#52c41a;">-0.17%</span><br>
              日经225 <b>68101.22</b> <span style="color:#f5222d;">+0.44%</span>｜韩KOSPI <b>7045.12</b> <span style="color:#f5222d;">+3.40%</span>"""
assert s.count(old_body_right) == 1
s = s.replace(old_body_right, new_body_right)

old_focus = """              <b>结构焦点：</b>三大指数早盘冲高、尾盘集体跳水翻绿，全市场<b>仅约两成个股上涨</b>、超4300只下跌，呈"权重相对抗跌、题材个股普跌"分化格局。<b>医药生物逆势领涨</b>——医疗服务、CXO、创新药、中药涨幅居前（博济医药/陇神戎发/万邦医药20CM涨停），催化为创新药BD交易热度延续（8月10日单日落地三起重磅）与药明康德公告美国法院批准其初步禁令动议、暂缓1260H名单认定影响。<b>有色金属集体走低</b>，贵金属/工业金属/小金属跌幅靠前；房地产、教育、玻璃玻纤同步回调。海外AI算力业绩超预期（Nebius Q2营收同比+454%、隔夜涨超34%；CoreWeave营收翻倍、涨超19%）推动算力租赁/超节点概念活跃。"""
new_focus = """              <b>结构焦点：</b>三大指数窄幅整理呈分化，沪指微红、创业板指涨超1%，全市场<b>约三成个股上涨</b>、近2900只下跌，呈"题材活跃、权重平淡"格局。<b>算力链（光通信/CPO/PCB）强势领涨</b>——电子化学品、稀土永磁、玻纤涨幅居前；电力、保险、港口、汽车走低。<b>港股下挫</b>：恒指跌1.1%、恒科跌1.77%，生物医药领跌、CPO逆势上涨，南向资金净卖出13亿港元。海外方面，美7月零售环比-0.6%创逾一年最大降幅、美联储暂停RMP购债，外围风险偏好降温。"""
assert s.count(old_focus) == 1
s = s.replace(old_focus, new_focus)

# 替换 footer 日期标注
old_footer1 = '            <span class="source-tag">同花顺iFind·2026-08-13收盘</span>'
new_footer1 = '            <span class="source-tag">同花顺iFind·2026-08-15收盘</span>'
assert s.count(old_footer1) == 1
s = s.replace(old_footer1, new_footer1)
old_footer2 = '            <span class="source-tag">数据来源：同花顺iFind/中新经纬/金融界/国际金融要情（08-14）</span>'
new_footer2 = '            <span class="source-tag">数据来源：同花顺iFind/陆家嘴财经早餐/华尔街见闻（08-15）</span>'
assert s.count(old_footer2) == 1
s = s.replace(old_footer2, new_footer2)

# ============ 2. S7 删除最旧 2 条 (08-04, 08-05) ============
# 结构化切块：按 timeline-date 内容锚定整块（含前置注释行）
def del_timeline(s, date_str):
    marker = f'timeline-date">{date_str}<'
    idx = s.index(marker)
    # 回退到本 item 起点（timeline-item 行首）
    item_start = s.rfind('<div class="timeline-item">', 0, idx)
    # 向前判断是否为注释行
    pre = s.rfind('\n', 0, item_start)
    pre2 = s.rfind('\n', 0, pre)
    line_before = s[pre2:pre]
    # item 自身闭合：title-close + item-close
    ITEM_CLOSE = '</div>\n      </div>\n'
    end_marker = s.find(ITEM_CLOSE, item_start)
    end = end_marker + len(ITEM_CLOSE)
    block_start = item_start
    if '时间线条目' in line_before:
        block_start = pre2 + 1  # 含注释行
    return s[:block_start] + s[end:]

s = del_timeline(s, '2026-08-04')
s = del_timeline(s, '2026-08-05')
assert s.count('timeline-date">2026-08-04<') == 0
assert s.count('timeline-date">2026-08-05<') == 0

# 合并 S7 同日重复：删除 08-15 的"40只漂移"条目（保留债基重启条）
DRIFT_0815 = '40只基金疑似风格漂移·红利基金跟科技跌'
didx = s.index(DRIFT_0815)
dstart = s.rfind('<div class="timeline-item">', 0, didx)
pre = s.rfind('\n', 0, dstart); pre2 = s.rfind('\n', 0, pre)
line_before = s[pre2:pre]
ITEM_CLOSE = '</div>\n      </div>\n'
dem = s.find(ITEM_CLOSE, dstart)
dend = dem + len(ITEM_CLOSE)
if '时间线条目' in line_before:
    dstart = pre2 + 1
s = s[:dstart] + s[dend:]
assert s.count(DRIFT_0815) == 0

# ============ 3. S1 移除与 S0 重复的 2 条 (40只漂移 / 272只双十) ============
# 用双层锚点 CARD_CLOSE 定位
CARD_CLOSE = '        </div>\n      </div>\n'

def del_s1_card(s, comment_anchor):
    # 用 S1 卡片专属注释行作为起点，切到下一处 S1 注释行首（含注释行本身）
    cidx = s.index(comment_anchor)
    line_start = s.rfind('\n', 0, cidx) + 1
    # 下一张 S1 卡注释行首
    next_comment = s.find('\n      <!-- S1 Card NEW:', cidx)
    if next_comment == -1:
        # 最后一张：切到 card-grid 闭合
        end = s.find('    </div>\n  </div>', cidx)
    else:
        end = next_comment + 1  # 含换行，保留下一张注释前的结构
    return s[:line_start] + s[end:]

before = s.count('<div class="card p1">')
s = del_s1_card(s, '<!-- S1 Card NEW: 40只基金疑似风格漂移 (08-15) -->')
s = del_s1_card(s, '<!-- S1 Card NEW: 272只基金突破双十限制 (08-14) -->')
after = s.count('<div class="card p1">')
assert before - after == 2, f"S1 应删2张，实际删 {before-after}"

# ============ 4. Stats Bar 替换"272只"卡为"近70只净值新高" ============
old_stat = """    <div class="stat-card">
      <div class="stat-number">272只</div>
      <div class="stat-label">主动权益基金持股破"双十"·08-14披露（周末不挂指数）</div>
      <div class="stat-change down">▼ 永赢产业机遇14.88%居首·971只顶格配置创新高</div></div>"""
new_stat = """    <div class="stat-card">
      <div class="stat-number">近70只</div>
      <div class="stat-label">主动权益基金净值创成立以来新高·08-13 Wind</div>
      <div class="stat-change up">▲ 灵活配置约37只·偏股混合约29只·低回撤绩优占优</div></div>"""
assert s.count(old_stat) == 1
s = s.replace(old_stat, new_stat)

# ---------- Phase 1: div 平衡 & 漂移断言 ----------
o1 = s.count("<div")
c1 = s.count("</div>")
# S6 改动：title/body 内部均为纯文本替换，div 数量不变
# S7 删2条：每条 timeline-item = 4 div，删2条 drift -8
# S1 删2张：每张卡 6 div，删2张 drift -12
# Stats 替换：div 数量不变（结构一致）
EXPECTED_DRIFT = -8 -12 -4  # S7删2条(-8) + S1删2张(-12) + S7合并删1条(-4)
assert o1 - c1 == o0 - c0, f"div 平衡破坏: bal {o1-c1} vs {o0-c0}"
assert (o1 - o0) == EXPECTED_DRIFT, f"div 漂移不符: {o1-o0} vs {EXPECTED_DRIFT}"
print(f"Phase1 div 断言通过: open {o0}->{o1}, close {c0}->{c1}, drift {o1-o0}")

# S8 不存在
assert 'Section 8' not in s and '待办跟踪' not in s and '腾安行动清单' not in s
# S0 section-title 精确
assert 'section-title">今日焦点</span>' in s
assert '今日焦点（' not in s
# S7 无重复日期
import re
dates = re.findall(r'timeline-date">(\d{4}-\d{2}-\d{2})<', s)
assert len(dates) == len(set(dates)), f"S7 日期重复: {dates}"
assert len(dates) <= 12, f"S7 超12条: {len(dates)}"

# 写入
with open(P, "w", encoding="utf-8") as f:
    f.write(s)
print("文件写入成功")
print(f"S7 当前条数: {len(dates)}")
