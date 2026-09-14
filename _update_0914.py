#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-14 (Monday)
两阶段：Phase1 全套断言通过才写文件。
"""
import re
from datetime import date, timedelta

SRC = 'index.html'
TODAY = date(2026, 9, 14)
T14 = TODAY - timedelta(days=14)          # 2026-08-31

s = open(SRC, encoding='utf-8').read()
o_orig = len(re.findall(r'<div\b', s))
c_orig = len(re.findall(r'</div>', s))

# ------------------------------------------------------------------ 0. header badge
upper = TODAY.strftime('%Y.%m.%d')
lower = T14.strftime('%Y.%m.%d')
BADGE_NEW = '📅 数据区间：' + lower + ' — ' + upper + '（每日更新）'
BADGE_RE = r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）'

# ------------------------------------------------------------------ 1. S0 新卡片
S0_C1 = '''      <!-- S0 Card 1 (09-14 P0) -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 基金网络营销整改进入倒计时·跳转引流迎强监管·“大V”带货仍未退场</div>
          <div class="card-meta">
            <span class="priority-tag urgent">P0 紧急必看</span>
            <span class="date-tag">09-14</span>
          </div>
        </div>
        <div class="card-body">
          证券时报9月14日报道（记者裴利瑞、赵梦桥）：距离《金融产品网络营销管理办法》<b>9月30日正式实施仅剩半个月</b>，基金互联网营销监管再度加码。9月初，监管下发最新一期<b>《机构监管情况通报》</b>，聚焦规范证券基金机构与第三方互联网平台开展的<b>转接渠道类合作</b>——即投资者在第三方平台浏览金融产品信息后，通过链接、按钮等入口跳转至机构页面完成开户、交易或基金申赎，此前业内常见的跳转引流模式迎来强监管。<br>
          <b>监管口径：</b>主要针对非持牌机构向持牌机构转接流量，例如短视频平台导流至券商或基金公司。上海某公募电商总监表示，一旦允许超级流量平台“分配客户”，平台就事实上掌握了客户入口、账户入口与关系入口，客户归属、投诉责任与适当性管理都容易出问题；某公募合规人士补充，基金盘中估值类小程序中的“证券开户”跳转与引导加群进入私域同样在监管视野内。<br>
          <b>合规要求：</b>《通报》要求事前严格审慎评估四维度——①第三方平台是否介入证券基金业务环节②是否混淆服务提供主体③是否采取有效措施保障投资者数据安全④是否合理收费、质价相符；<b>评估结果须由分管业务负责人、首席信息官、合规负责人、总经理等管理层成员签字确认</b>，合规责任被压实至公司管理层而非仅停留业务部门。<br>
          <b>存量乱象：</b>记者获得的某互联网平台基金产品运营方案显示，“大V”“小V”带货玩法尚未完全退场，净值播报、“上车”宣传、买入操作展示、口碑发帖等推广模式依然隐蔽存在。<br>
          <b>对腾安启示：</b>9月30日前须完成三项闭环——存量第三方转接合作逐项体检（备案状态、质价评估、数据安全边界、管理层签批留痕）；全面清理“大V/小V”带货与私域引流合作；行情页与小程序内所有“开户/购买”跳转入口重做合规审核。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-09-14/doc-inirtwin4912080.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-14</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 合规体检→9月30日前完成全部第三方平台转接合作逐项评估与留档，评估报告须走管理层会签；<br>
            ② 引流清理→排查并终止无资质“大V/小V”带货、净值播报、“上车”宣传与私域加群等变相营销合作；<br>
            ③ 入口重审→行情页、基金详情页、小程序内所有跳转开户与购买入口补做适当性与风险提示校验。
          </div>
        </div>
      </div>


      <!-- S0 Card 2 (09-14 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 绩优基金主动降仓稳收益·年内翻倍基仅剩4只·净值与重仓股走势背离</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-14</span>
          </div>
        </div>
        <div class="card-body">
          证券时报9月14日报道（记者安仲文）：Wind数据显示，截至9月13日，全市场年内收益翻倍的主动权益基金<b>仅剩4只</b>——杨宗昌管理的易方达供给改革与易方达产业机遇、左少逸执掌的诺安创新驱动、金梓才管理的财通多策略福鑫定开，上半年约200只翻倍基的火热行情已然落幕。曾以<b>183.67%</b>年内收益率夺得半程冠军的方正富邦核心优势，截至9月13日年内收益已回落至<b>70.89%</b>，较半程高光表现近乎腰斩。<br>
          <b>降仓证据：</b>多家绩优基金净值走势与披露的前十大重仓股盘面明显背离——北京某重仓AI硬科技的偏股基金，9月11日十大重仓股9只上涨、头号重仓股涨近6%，基金净值仅微涨0.1%；上海某科技主题基金同日核心重仓股跌超9%，净值反而上涨0.97%。华南某头部公募布局光模块的灵活配置基金，9月10日、11日重仓股大幅震荡期间净值几乎纹丝不动，其7月27日更新的招募说明书显示股票仓位最低可降至0。<br>
          <b>降仓逻辑：</b>年内交易时长已不足四个月，年度业绩考核逐步落地，机构“保收益、稳排名”诉求升温；控仓也为市场回调后保留反扑弹药，若后市走向均衡轮动，预留仓位可支撑灵活调仓。多位基金经理提示，应规避情绪与估值透支的高预期热门赛道，布局悲观预期充分定价、基本面边际改善的低位行业与个股。<br>
          <b>对腾安启示：</b>高波动期客户易被“翻倍基”榜单吸引追高，榜单页须补充最大回撤、股票仓位与波动率指标，并对年内收益已大幅回撤的产品加挂显著风险提示。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260914/c679854795.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·09-14</span></a>
          <a href="https://fund.jrj.com.cn/2026/09/14083158424500.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">金融界基金·09-14</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 3 (09-14 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 双创主题ETF资金分歧·科创50ETF华夏净流入超32亿·科创半导体ETF净流出超17亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-14</span>
          </div>
        </div>
        <div class="card-body">
          新华财经9月14日报道（记者王鹤静）：上周（9月7日至11日）以通信为首的科技成长板块迎来小幅反弹，玻纤、PCB、光通信等板块回暖，多只通信ETF<b>涨超5%</b>领跑市场，另有部分创业板成长、TMT、创业板人工智能主题ETF涨超2%。受国际油价上涨驱动，能源化工ETF建信上周上涨<b>5.2%</b>、标普油气ETF嘉实上涨1.85%；港股创新药板块明显回落，多只港股通创新药主题ETF<b>跌超7%</b>，证券板块同步回调，多只金融科技主题ETF跌超7%。<br>
          <b>资金分歧：</b>上周科创50ETF华夏净流入超<b>32亿元</b>，成长ETF易方达、科创50ETF易方达均净流入超14亿元，通信ETF国泰净流入超12亿元；与此同时科创半导体ETF华夏净流出超<b>17亿元</b>、创业板ETF易方达净流出超13亿元。<br>
          <b>机构观点：</b>国泰基金认为，海外扰动因素影响低于预期或带来利空出清修复，叠加GPT-6 Astra发布强化AI景气预期、国内光博会催化，通信板块基本面逻辑仍然扎实。业内机构表示，资金仍在配置科技，但选择<b>从押注具体赛道转向先配置成长板块</b>。<br>
          <b>对腾安启示：</b>同一主题内部资金分化加大，宽基与细分赛道ETF应分层展示净流入/净流出，避免客户把“板块吸金”误读为“全赛道普涨”。
        </div>
        <div class="card-footer">
          <a href="https://www.cnfin.com/gs-lb/detail/20260914/4469283_1.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华财经·09-14</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>


      <!-- S0 Card 4 (09-14 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 科技主题ETF持续“上新”·创业板算力、金融科技、人工智能ETF集中发行</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-14</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报9月14日报道（记者赵明超）：近期科技主题ETF持续“上新”。<b>创业板算力基础设施ETF</b>方面，8月28日首批10只获批，9月4日6只启动发行、另有2只于9月7日发行；<b>创业板金融科技ETF</b>8月28日首批6只获批，华泰柏瑞9月7日、景顺长城9月8日、建信9月10日先后发行，万家将于9月14日发行；<b>人工智能主题ETF</b>截至9月11日有3只正在发行，另有1只定档9月14日发行。<br>
          <b>持有人结构：</b>近期新成立的科技主题ETF频现机构投资者身影——以东方红中证云计算50ETF为例，截至9月8日前十名基金份额持有人包括从容稳健保值证券投资基金、中航证券、招商证券及东方红建盈明悦1号、5号集合资产管理计划等。<br>
          <b>持续扩容：</b>Choice数据显示，9月7日以来富国中证全指软件ETF、嘉实中证芯片产业ETF、华泰柏瑞上证科创板芯片ETF等集中上报。<br>
          <b>机构观点：</b>国泰海通证券测算，主动权益类基金6月权益仓位到达历史高位后配置中枢仍呈抬升趋势，近2个月TMT板块仓位保持相对稳定；国海富兰克林基金认为，AI下游应用落地与商业化闭环已取得实质性进展，海外算力资本开支景气周期尚未结束。<br>
          <b>对腾安启示：</b>同主题ETF密集发行易造成选择困难，申购页须提供跟踪指数、费率、规模与流动性四维对比，并提示新基金建仓期跟踪误差风险。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/789676" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-14</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>


'''

# ------------------------------------------------------------------ 2. S2 新卡（替换 09-05 转接合作卡，去重）
S2_NEW = '''<div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-13</span>
          </div>
          <div class="card-title">🟡 中基协撤销台州沃源管理人登记·委托“牛散”行使投资管理职责·80万罚单后再遭纪律处分</div>
        </div>
        <div class="card-body">
          财联社9月13日报道（记者封其娟）：地方证监局80万元罚单落地后，追责并未止步——中国证券投资基金业协会最新公布，针对浙江证监局查实的两类违规情形，决定<b>取消台州沃源会员资格并撤销其管理人登记</b>；该私募现任基金经理徐铭崎、合规风控负责人谢灵俊、登记为法定代表人的金佩君同步受到公开谴责。<br>
          <b>违规事实：</b>浙江证监局认定台州沃源存在“报送、披露的信息存在虚假记载”与“委托他人行使投资管理职责”两项违规——2022年9月至2023年9月，该私募先后备案3只产品后即将投资管理职责委托外部人员丁某行使，直至丁某2023年12月被公安机关采取刑事强制措施，期间未实际履行管理人职责；其登记在册的实控人、总经理为金佩君，实际掌权的却是与其为配偶关系的徐铭崎，触及《私募投资基金登记备案办法》中“违规通过委托他人持有股权、隐瞒关联关系”。该局已于去年3月两度出手，合计罚款<b>80万元</b>（机构60万元、徐铭崎20万元）。<br>
          <b>关键细节：</b>公开文书以“丁某”指代的外包对象，多条证据链指向恒润股份内幕交易与操纵股价案关键人物牛散丁键；该私募时任投资经理纪云涛利用内幕信息交易恒润股份已被证监会罚没<b>225.78万元</b>。<br>
          <b>对腾安启示：</b>私募代销准入须把“实控人与实际管理人一致性”“投资管理职责是否外包”纳入尽调硬指标，并对协会纪律处分、证监局行政处罚与诚信档案做常态化穿透核查。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L6P5GS5H05568W0A.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社·09-13</span></a>
        </div>
      </div>
'''

# ------------------------------------------------------------------ 3. S7 新时间线
def item(color, d, title):
    return ('      <div class="timeline-item">\n'
            '        <div class="timeline-dot ' + color + '"></div>\n'
            '        <div class="timeline-date">' + d + '</div>\n'
            '        <div class="timeline-title">' + title + '</div>\n'
            '      </div>\n')

S7_ITEMS = [
    ('red',   '2026-09-14', '基金网络营销整改进入倒计时'),
    ('blue',  '2026-09-14', '绩优基金主动降仓保收益'),
    ('blue',  '2026-09-14', '双创ETF资金分歧·科创50吸金'),
    ('red',   '2026-09-13', '中基协撤销台州沃源管理人登记'),
    ('blue',  '2026-09-12', '算力ETF进入上市期·天弘9-16挂牌'),
    ('blue',  '2026-09-12', '第二批摊余成本法债基上报'),
    ('blue',  '2026-09-12', '近一月1055家公司获机构调研'),
    ('blue',  '2026-09-12', '中欧一基金二次召集持有人大会'),
    ('red',   '2026-09-11', '金融强国“十五五”规划正式出台'),
    ('blue',  '2026-09-11', '公募布局白盒固收+·规模超2.28万亿'),
    ('red',   '2026-09-11', '两大主题ETF集中申报·18家'),
    ('red',   '2026-09-11', 'A股放量调整·成交1.99万亿'),
]
S7_NEW = ''.join(item(c, d, t) for c, d, t in S7_ITEMS)

# ================================================================== Phase 1 断言
A_S0_START = '      <!-- S0 Card 1'
A_S0_END = '    </div>\n  </div>\n\n<!-- ============ Section 1:'
A_S2_START = '<div class="card p0">\n        <div class="card-top">\n          <div class="card-meta">\n            <span class="priority-tag urgent">P0 紧急必看</span>\n            <span class="date-tag">09-05</span>'
A_S2_NEXT = '      <div class="card p1">'
A_S7_START = '      <div class="timeline-item">'
A_S7_END = '\n\n    </div>\n\n  </div>\n\n</div>\n\n</body>'
A_CTX = '<span class="section-context">9月12日 · 4条今日要闻</span>'
A_CTX_NEW = '<span class="section-context">9月14日 · 4条今日要闻</span>'

assert s.count(A_S0_START) == 1, 'S0 起点锚点不唯一'
assert s.count(A_S0_END) == 1, 'S0 终点锚点不唯一'
assert s.count(A_S2_START) == 1, 'S2 09-05 卡锚点不唯一'
assert s.count(A_S7_START) == 12, 'S7 timeline-item 数异常: %d' % s.count(A_S7_START)
assert s.count(A_S7_END) == 1, 'S7 终点锚点不唯一'
assert s.count(A_CTX) == 1, 'S0 section-context 锚点不唯一'
assert re.search(BADGE_RE, s), 'header badge 未命中'
print('[ok] Phase1 锚点预检通过')

t = s

# --- badge
t = re.sub(BADGE_RE, BADGE_NEW, t)
assert BADGE_NEW in t, 'badge 替换失败'

# --- S0 context
t = t.replace(A_CTX, A_CTX_NEW)
assert A_CTX_NEW in t, 'context 替换失败'

# --- S0 cards
i0 = t.find(A_S0_START)
i1 = t.find(A_S0_END)
assert 0 < i0 < i1
t = t[:i0] + S0_C1 + t[i1:]

# --- S2: 删 09-05 卡 + 插入新卡
j0 = t.find(A_S2_START)
assert j0 > 0
j1 = t.find(A_S2_NEXT, j0)
assert j1 > j0
t = t[:j0] + S2_NEW + '\n\n      ' + t[j1:]

# --- S7
k0 = t.find(A_S7_START)
k1 = t.find(A_S7_END)
assert 0 < k0 < k1
t = t[:k0] + S7_NEW + t[k1:]

# ================================================================== Phase 2 校验
o_new = len(re.findall(r'<div\b', t))
c_new = len(re.findall(r'</div>', t))
print('div open  %d -> %d (drift %+d)' % (o_orig, o_new, o_new - o_orig))
print('div close %d -> %d (drift %+d)' % (c_orig, c_new, c_new - c_orig))
assert o_new == c_new, 'div 不平衡'
assert o_new - o_orig == 3, 'div 漂移不等于预期 +3（新增 1 个 action-box）'
assert t.count('</div>>') == 0, '游离 > 字符'
assert 'S8' not in t and '待办跟踪' not in t and '腾安行动清单' not in t, 'S8 残留'
assert t.count('\ufffd') == 0, '存在 U+FFFD 乱码'

# S0 段
g0 = t.find('Section 0')
g1 = t.find('Section 1')
seg0 = t[g0:g1]
assert seg0.count('<div class="card p') == 4, 'S0 卡数 != 4'
assert seg0.count('action-box') == 1, 'S0 action-box 数 != 1'
assert seg0.count('href="http') == 5, 'S0 链接数 != 5（1+2+1+1）: %d' % seg0.count('href="http')
assert seg0.count('section-title-group') == 1
assert '<span class="section-title">今日焦点</span>' in seg0, 'S0 标题不是「今日焦点」'
assert A_CTX_NEW in seg0
tags = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', seg0)
assert tags.count(('09', '14')) == 4, 'S0 非全 09-14: %s' % tags

# S1 / S2 段
s2 = t[t.find('Section 2'):t.find('Section 3')]
assert s2.count('<div class="card p') == 4, 'S2 卡数 != 4: %d' % s2.count('<div class="card p')
assert '09-05' not in s2, 'S2 仍存在 09-05 旧卡'
s1 = t[t.find('Section 1'):t.find('Section 2')]
assert s1.count('<div class="card p') == 6, 'S1 卡数 != 6'

# S7 段
s7 = t[t.find('Section 7'):]
items = re.findall(r'<div class="timeline-date">(\d{4}-\d{2}-\d{2})</div>\s*\n\s*<div class="timeline-title">([^<]+)</div>', s7)
assert len(items) == 12, 'S7 条数 != 12: %d' % len(items)
ds = [d for d, _ in items]
assert ds == sorted(ds, reverse=True), 'S7 未降序'
for d, tt in items:
    dd = date(int(d[:4]), int(d[5:7]), int(d[8:10]))
    assert T14 <= dd <= TODAY, 'S7 越界 %s' % d
    assert len(tt) <= 25, 'S7 标题超 25 字: %s (%d)' % (tt, len(tt))
assert 'timeline-desc' not in s7

# 黑名单（全文件）
BAD = ['so.html5.qq.com', 'toutiao', '企鹅号', '网易号', '搜狐号',
       'stcn.com', 'cls.cn', '21jingji.com', 'yicai.com', 'guba.eastmoney.com']
for b in BAD:
    assert b not in t, '黑名单命中: %s' % b

print('[ok] Phase2 全量校验通过')
open(SRC, 'w', encoding='utf-8').write(t)
print('[written] index.html 已更新')
