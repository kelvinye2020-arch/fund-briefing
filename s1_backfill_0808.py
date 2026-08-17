# -*- coding: utf-8 -*-
"""S1 补位：3条->4条，新增 08-06 百亿主动权益基金扩容至72只"""
import re
P = 'index.html'
s = open(P, encoding='utf-8').read()
ORIG_OPEN = s.count('<div')
assert ORIG_OPEN == s.count('</div>'), 'baseline失衡'
print('BASE', ORIG_OPEN)

ANCHOR = '      <!-- S1 Card NEW: 公募极致抱团科技57.3%超历史峰值 (07-25) -->'
assert s.count(ANCHOR) == 1, '锚点异常'

NEW = '''      <!-- S1 Card NEW: 百亿主动权益基金扩容至72只 (08-06) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-06</span>
          </div>
          <div class="card-title">🟡 百亿级主动权益基金扩容至72只·环比增125%·16家公募主动权益规模破千亿</div>
        </div>
        <div class="card-body">
          <b>产品端扩容：</b>同花顺数据显示，截至今年年中全市场百亿规模主动权益基金（含普通股票型、偏股混合型、灵活配置型、平衡混合型）共<b>72只</b>，较一季度末的32只增加<b>125%</b>。规模居前三的东方人工智能主题混合、永赢科技智选混合发起、永赢先锋半导体智选混合发起均聚焦AI与半导体，二季度末规模分别达<b>351.25亿元、346.41亿元、329.16亿元</b>；全市场规模超200亿元的主动权益基金有15只，多数覆盖AI主题。旗下主动权益规模超百亿的基金经理增至<b>152位</b>，较一季度末增加42位，其中51位为新晋。<br>
          <b>机构端分层：</b>161家基金公司二季度末主动权益管理规模合计<b>5.01万亿元</b>，较一季度末增加<b>9924亿元</b>、环比增<b>24.7%</b>；规模破千亿的公募扩容至<b>16家</b>，华商、华安、大成、鹏华为本季新进入者。易方达以<b>4324.39亿元</b>领跑（单季增逾1500亿、环比+54.4%），广发、中欧、汇添富、富国均超2000亿。72只百亿产品来自<b>31家</b>公募，易方达独占14只、永赢与中欧各7只，头部集中度显著。<br>
          <b>政策与格局：</b>中小公募转向细分垂直赛道谋突围——红土创新盖俊龙旗下5只产品重仓新易盛、中际旭创等算力龙头上半年收益悉数翻倍，金信基金孔学兵聚焦半导体设备多只产品翻倍。6月陆家嘴论坛证监会主席吴清明确"推出支持中小基金公司规范健康发展的一揽子措施，在产品布局、业务准入等方面给予适当倾斜"，业内认为公募将进入<b>头部综合化、中小特色化的错位竞争阶段</b>。<br>
          <b>对基金行业影响：</b>主动权益规模向AI/半导体主题头部产品极度集中→腾安在货架结构上需警惕"百亿主动权益=高集中度科技暴露"的隐含风险，同时可关注中小公募特色精品作为差异化补充。
        </div>
        <div class="card-footer">
          <a href="https://finance.eastmoney.com/a/202608063833820797.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">深圳商报·东方财富</span></a>
          <span class="impact-tag high">格局影响：高</span>
        </div>
      </div>

'''
i = s.index(ANCHOR)
s = s[:i] + NEW + s[i:]

o, c = s.count('<div'), s.count('</div>')
print('AFTER', o, c, 'drift', o - ORIG_OPEN)
assert o == c, '失衡'
assert o - ORIG_OPEN == 6, f'新增卡片应 +6 div，实际 {o-ORIG_OPEN}'

# 复检 S1
s1 = s[s.index('Section 1: 重磅信息'): s.index('Section 2: 监管政策')]
d1 = re.findall(r'<span class="date-tag">(\d\d-\d\d)</span>', s1)
assert len(d1) == 4, f'S1 条数 {len(d1)}'
assert all(x >= '07-25' for x in d1), f'S1 过期 {d1}'
assert s1.count('target="_blank"') == 4, 'S1 链接数'
assert s1.count('<div class="card-meta">') == 4, 'S1 card-meta'
assert '\ufffd' not in s, '乱码'
print('S1 OK', d1)

open(P, 'w', encoding='utf-8', newline='').write(s)
print('written')
