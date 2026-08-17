#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 2026-06-27 每日自动更新脚本
- 今天周六，A股休市，S6标注"休市"
- S0收录T+0(06-27)和T-1(06-26)新闻
- 清理S1/S2/S7中早于T-14(06-13)的条目
"""

import re
from datetime import datetime, timedelta

# 读取原文件
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

today = '2026-06-27'
today_short = '06-27'
# T-14 = 2026-06-13

# ========== 1. 更新头部信息 ==========
html = re.sub(
    r'<!-- daily-update: 2026-06-26 -->',
    '<!-- daily-update: 2026-06-27 -->',
    html
)
html = re.sub(
    r'📅 数据区间：2026\.06\.11 — 2026\.06\.25（今日自动更新）',
    '📅 数据区间：2026.06.13 — 2026.06.27（今日自动更新）',
    html
)
html = re.sub(
    r'数据更新时间：2026年06月26日 10:00 · 近两周核心资讯（06-12 — 06-26）·',
    '数据更新时间：2026年06月27日 10:00 · 近两周核心资讯（06-13 — 06-27）·',
    html
)

# ========== 2. 更新 Stats Bar ==========
new_stats = '''<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">6月新发基金破千亿</div>
    <div class="stat-label">176只·1012亿·权益类担当主力军·FOF同比创峰值</div>
    <div class="stat-change up">▲ 权益+固收++FOF三主线·机构看多后市</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">第二批基准调整全面铺开</div>
    <div class="stat-label">超90家管理人·千余只产品·从试点探路走向系统推进</div>
    <div class="stat-change neutral">■ 基准校准·产品回归本源·投资回归专业</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">89家公募自购44亿</div>
    <div class="stat-label">年内合计·被动指数+债券型受青睐·权益占比待提升</div>
    <div class="stat-change neutral">■ 自购热情不减·真金白银表达信心</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">证监会罚款近6000万</div>
    <div class="stat-label">玖瀛资产·腾创投资·利益输送+虚假信息·私募严监管</div>
    <div class="stat-change up">▲ 私募基金监管零容忍·罚单创史上最重</div>
  </div>
</div>'''

html = re.sub(
    r'<div class="stats-bar">.*?</div>\n</div>',
    new_stats,
    html,
    flags=re.DOTALL
)

# ========== 3. 更新 S0 今日焦点 ==========
new_s0 = '''  <!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（6月27日·周六·市场休市·第二批基准调整全面铺开）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">

      <!-- S0 Card 1: 第二批公募基准调整全面铺开 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 第二批公募业绩比较基准调整全面铺开·超90家管理人千余只产品</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>全面铺开：</b>6月26日，易方达、华夏、广发、国泰等超90家基金管理人密集发布旗下部分存量产品业绩比较基准调整公告，涉及千余只产品，标志着基准改革从"试点探路"走向"系统推进"。<br>
          <b>调整范围：</b>涵盖权益类、债券类、FOF类、QDII类等多类型产品。权益类基金提升基准中权益权重，债券类基金优化久期设置，更加贴合产品实际持仓。<br>
          <b>生效时间：</b>多数产品自<b>7月27日</b>起调整基准，富国27只、泰康10只、路博迈2只（8月1日起）等已公告。<br>
          <b>对基金行业影响：</b>基准校准让产品从"模糊标签"走向"清晰画像"→腾安应在基金详情页突出业绩比较基准说明，帮助客户理解产品定位。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260626A091S800" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·中国基金报</span></a>
          <a href="https://finance.sina.com.cn/jjxw/2026-06-26/doc-inieuccq1919385.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">界面新闻</span></a>
          <span class="impact-tag medium">基准改革：极高</span>
        </div>
      </div>

      <!-- S0 Card 2: 6月新发基金破千亿 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 6月以来新发基金破千亿元·权益类担当主力军·FOF年内规模创峰值</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行规模：</b>截至6月26日，6月以来已成立<b>176只</b>新基金，发行规模达<b>1012.29亿元</b>。权益类、固收+、FOF三类产品最受资金青睐。<br>
          <b>产品主线：</b>①权益类：富国电子信息产业混合32.6亿、中欧全景智选混合31.91亿；②固收+：南方平衡回报混合75.33亿；③FOF：兴全盈泰多元配置35.91亿，年内FOF发行规模达<b>1177.42亿元</b>，超越2021年创下的年度最高纪录。<br>
          <b>对基金行业影响：</b>新发破千亿+FOF创峰值→机构看多后市→腾安可积极储备新发基金销售资源。
        </div>
        <div class="card-footer">
          <a href="https://finance.china.com.cn/money/fund/20260627/6313808.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag medium">新发热度：高</span>
        </div>
      </div>

      <!-- S0 Card 3: 证监会对玖瀛资产罚款近6000万 -->
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产等罚款近6000万元·私募基金"零容忍"监管再升级</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>处罚内容：</b>证监会对深圳前海玖瀛资产管理有限公司、深圳市前海腾创投资有限公司及相关责任人员利用私募基金向关联主体输送利益、报送虚假信息等违法违规行为作出行政处罚，合计罚款近<b>6000万元</b>，超过前期优策案（3500万）和瑞丰达案（4100万），创"史上最重"罚单。<br>
          <b>配套措施：</b>同步对实际控制人采取<b>5年证券市场禁入</b>及<b>5年证券市场禁止交易</b>措施。<br>
          <b>监管信号：</b>私募基金监管"零容忍"态势持续升级，利益输送、虚假披露是重点打击方向。<br>
          <b>对基金行业影响：</b>私募监管升级→公募也要引以为鉴→腾安应加强对代销私募产品的合规审查。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260626223459a6b8a584" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·证券时报</span></a>
          <span class="impact-tag high">私募严监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 关注私募监管升级态势，审查腾安代销的私募产品合规性；<br>
            ② 将"零容忍"监管信号纳入内部合规培训材料。
          </div>
        </div>
      </div>

    </div>
  </div>'''

# 替换 S0 整个 section
html = re.sub(
    r'  <!-- ============ Section 0: 今日焦点 ============ -->.*?  </div>\n  </div>',
    new_s0,
    html,
    flags=re.DOTALL
)

# ========== 4. 更新 S1 重磅信息 ==========
# 当前S1条目：06-24浮费、06-24 QDII、06-22 FOF、06-25报道证监会、06-22限购、06-17债券ETF
# 均在T-14内，但需新增06-26第二批基准 + 06-27新发破千亿，移除2条较低优先级
# 移除：06-22从千亿抢购到千元限购、06-17债券ETF规模突破

new_s1 = '''  <!-- ============ Section 1: 重磅信息 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏆</div>
      <div class="section-title">重磅信息</div>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">近两周核心</span>
    </div>

    <div class="card-grid">

      <!-- S1 Card 1: 第二批公募基准调整全面铺开 (NEW) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 第二批公募业绩比较基准调整全面铺开·千余只产品·从试点走向系统推进</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>全面铺开：</b>6月26日，超90家基金管理人发布旗下部分存量产品业绩比较基准调整公告，涉及千余只产品，覆盖范围更广、产品数量更多、参与主体更加多元。<br>
          <b>调整逻辑：</b>按照"优先调整基准而非调整持仓"原则，管理人调整基准无需调仓，不会对市场运行造成冲击。基准调整的核心逻辑是让业绩比较基准更加贴近实际资产配置和投资风格。<br>
          <b>对基金行业影响：</b>基准改革全面铺开→产品定位更清晰→投资者选择基金更有依据→腾安可在营销中突出基准说明。
        </div>
        <div class="card-footer">
          <a href="https://www.163.com/dy/article/L0F7H3A405346RC6_pdya11y.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华社·中国证券报</span></a>
          <a href="https://www.toutiao.com/article/7655830765002867246" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">头条·证券时报</span></a>
          <span class="impact-tag medium">基准改革：极高</span>
        </div>
      </div>

      <!-- S1 Card 2: 6月新发基金破千亿 (NEW) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 6月新发基金破千亿·FOF年内规模1177亿超越2021年峰值</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>发行数据：</b>截至6月26日，6月以来已成立176只新基金，发行规模1012.29亿元。权益类、固收+、FOF三类产品最受资金青睐。<br>
          <b>FOF爆发：</b>年内FOF发行规模达1177.42亿元，超越2021年创下的年度最高纪录。兴全盈泰多元配置三个月持有混合FOF发行35.91亿元，易方达如意安恒3个月持有混合FOF发行27亿元。<br>
          <b>对基金行业影响：</b>新发市场热度不减→机构看多→腾安应积极储备新发资源，特别是FOF产品。
        </div>
        <div class="card-footer">
          <a href="https://finance.china.com.cn/money/fund/20260627/6313808.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag medium">新发热度：高</span>
        </div>
      </div>

      <!-- S1 Card 3: 浮费基金一周年业绩断层 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 浮费基金一周年业绩断层·华商致远回报A成三倍基·首尾相差329个百分点</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>业绩表现：</b>截至6月22日，首批26只新型浮动费率基金中，华商致远回报A成立以来收益<b>316.56%</b>，排名第一；鹏华共赢未来A亏损<b>-12.84%</b>，排名垫底。首尾相差<b>329个百分点</b>。<br>
          <b>费率机制：</b>运作满一年后，绩优产品对持有满一年投资者按<b>1.50%</b>收费；绩差产品按<b>0.60%</b>收费。费率与业绩挂钩机制正式生效。<br>
          <b>对基金行业影响：</b>浮动费率改革打破"旱涝保收"→业绩分化验证改革必要性→腾安在推荐浮费基金时应充分披露费率机制。
        </div>
        <div class="card-footer">
          <a href="https://fund.eastmoney.com/a/202606233779894014.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <span class="impact-tag medium">浮费改革：高</span>
        </div>
      </div>

      <!-- S1 Card 4: QDII产品限购力度再加码 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII产品限购力度再加码·超百只限购百元及以下·业绩近一年平均22%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购加码：</b>6月23-24日，易方达、万家、华宝等多家基金公司集中下调QDII产品大额申购上限，易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>，华宝海外科技股票(QDII-LOF)降至20元。<br>
          <b>背后逻辑：</b>近一年QDII产品平均收益率22%，45只净值翻倍。业绩吸引资金→外汇额度消耗→限购保护存量持有人利益。<br>
          <b>对基金行业影响：</b>QDII稀缺性加剧→腾安应提前储备QDII产品额度→客户咨询时提供替代方案。
        </div>
        <div class="card-footer">
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260624/6313305.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag medium">QDII稀缺：高</span>
        </div>
      </div>

      <!-- S1 Card 5: FOF上半年新发规模1137亿 -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 FOF上半年新发规模1137亿·超越2021年峰值·低利率催化+银行渠道发力</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-22</span>
          </div>
        </div>
        <div class="card-body">
          <b>爆发式增长：</b>Wind数据显示，截至6月20日，2026年以来新成立FOF基金已达<b>88只</b>，合计发行规模高达<b>1137.69亿元</b>，超越2021年创下的<b>1083.62亿元</b>历史峰值。<br>
          <b>对基金行业影响：</b>FOF从"配角"走向舞台中央→资产配置需求上升→腾安可加大FOF产品推荐权重。
        </div>
        <div class="card-footer">
          <a href="https://www.stcn.com/article/detail/3970656.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券时报</span></a>
          <span class="impact-tag medium">FOF爆发：高</span>
        </div>
      </div>

      <!-- S1 Card 6: 证监会支持中小基金公司差异化发展 -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 证监会支持中小基金公司差异化发展·分类监管破局"规模竞赛"</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-25报道</span>
          </div>
        </div>
        <div class="card-body">
          <b>政策方向：</b>2026年6月，证监会主席吴清在陆家嘴论坛表示，"推出支持中小基金公司规范健康发展一揽子措施，坚持分类监管、突出特色，在产品布局、业务准入等方面给予适当倾斜，积极支持中小基金公司差异化发展"。<br>
          <b>行业影响：</b>中小基金公司有望从"规模竞赛"转向"特色生存"，行业格局从"赢者通吃"向"多元共生"演变。<br>
          <b>对基金行业影响：</b>分类监管→中小基金公司差异化发展→腾安可关注特色化中小基金公司产品供给。
        </div>
        <div class="card-footer">
          <a href="https://finance.china.com.cn/money/fund/20260625/6313510.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网·上海证券报</span></a>
          <span class="impact-tag low">分类监管：低</span>
        </div>
      </div>

    </div>
  </div>'''

html = re.sub(
    r'  <!-- ============ Section 1: 重磅信息 ============ -->.*?  </div>\n  </div>',
    new_s1,
    html,
    flags=re.DOTALL
)

# ========== 5. 更新 S2 监管政策 ==========
# 当前S2：06-26法治协同、06-13三年行动计划、06-12适当性细则(到期移除)、06-17主动ETF指引
# 移除06-12适当性细则（早于T-14），新增06-26玖瀛资产处罚

new_s2 = '''  <!-- ============ Section 2: 监管政策 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🏛️</div>
      <span class="section-title">监管政策动态</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">最高优先级</span>
    </div>

    <div class="card-grid">

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会五方面推动资本市场法治协同建设·推动修改证券投资基金法</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>法治协同规划：</b>中国证监会近日对推进资本市场法治协同建设作出规划，包括：配合做好金融法制定，<b>推动修改证券投资基金法</b>；严厉打击系统性财务造假、第三方配合造假和中介机构失职失守违法犯罪行为；探索研究将行政执法查封、冻结的证券期货违法涉案财产用于投资者民事诉讼赔偿。<br>
          <b>立法计划：</b>推动修订《证券公司监督管理条例》《证券、期货投资咨询管理暂行办法》，<b>制定上市公司监督管理条例</b>。完善域外适用规定和反长臂管辖、反制裁规定。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260626A02KQL00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·四大证券报</span></a>
          <span class="impact-tag high">法治升级：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 跟踪证券投资基金法修改立法进展，评估对腾安业务影响；<br>
            ② 关注"行刑民"立体追责机制完善，加强内部合规管理。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产等罚款近6000万·私募基金"零容忍"监管再升级</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>处罚内容：</b>证监会对深圳前海玖瀛资产管理有限公司、深圳市前海腾创投资有限公司及相关责任人员利用私募基金向关联主体输送利益、报送虚假信息等违法违规行为作出行政处罚，合计罚款近<b>6000万元</b>，创"史上最重"罚单。<br>
          <b>配套措施：</b>同步对实际控制人采取<b>5年证券市场禁入</b>及<b>5年证券市场禁止交易</b>措施。惩治效果显著提高，体现证监会对私募基金严重违法违规行为"零容忍"的监管态度。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260626223459a6b8a584" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·证券时报</span></a>
          <span class="impact-tag high">私募严监管：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 关注私募监管升级态势，审查腾安代销的私募产品合规性；<br>
            ② 将"零容忍"监管信号纳入内部合规培训。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会6/13发布《公募基金高质量发展三年行动计划（2026-2028）》+销售费用管理规定同步实施</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-13</span>
          </div>
        </div>
        <div class="card-body">
          <b>三年行动计划：</b>6月13日，证监会正式发布《公开募集证券投资基金行业高质量发展三年行动计划（2026-2028）》，明确2026-2028年行业改革路线图。<br>
          <b>销售费用新规：</b>同步实施《公募基金销售与服务费用管理规定》，进一步压降认申购费及销售服务费。
        </div>
        <div class="card-footer">
          <span class="impact-tag high">行业纲领：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 研究三年行动计划对腾安代销业务模式的影响；<br>
            ② 销售费用新规实施→评估腾安代销佣金结构是否需要调整。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 沪深交易所6/17发布主动ETF业务指引·管理人准入：5年经验+100亿规模</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-17</span>
          </div>
        </div>
        <div class="card-body">
          <b>指引落地：</b>6月17日，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。<br>
          <b>准入门槛：</b>管理人需具备<b>5年以上</b>主动权益公募基金管理运作经验，近3年平均主动权益公募基金管理规模不少于<b>100亿元</b>。<br>
          <b>投资要求：</b>基金投资组合持有证券数量不少于<b>30只</b>，前十大持仓合计占比不超过60%。<br>
          <b>对基金行业影响：</b>主动ETF有望成为ETF市场新增长引擎→产品创新加速→腾安可关注主动ETF产品布局机会。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/730782" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
          <span class="impact-tag medium">产品创新：中</span>
        </div>
      </div>

    </div>
  </div>'''

html = re.sub(
    r'  <!-- ============ Section 2: 监管政策 ============ -->.*?  </div>\n  </div>',
    new_s2,
    html,
    flags=re.DOTALL
)

# ========== 6. 更新 S6 市场行情速览（周六休市）==========
new_s6 = '''      <!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

    <div class="card p3">
      <div class="card-top">
        <div class="card-title">2026年6月28日（周六）·A股休市·最新收盘：6月26日（周四）数据</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 A股最近收盘（6/26 周四）：</b><br>
            ▪ 沪指 <b>-0.52%</b>（4098.69点）—— 集体低开<br>
            ▪ 深成指 <b>-0.81%</b>（16211.41点）<br>
            ▪ 创业板指 <b>-1.20%</b>（4319.41点）<br>
            ▪ 科创综指 <b>-1.21%</b>（2362.92点）<br>
            ▪ 盘面：工业金属·油气·化工·电力涨幅居前；金融科技·培育钻石·PCB·存储器·CPO·光伏·半导体跌幅居前<br><br>
            <b>📊 港股最近收盘（6/26 周四）：</b><br>
            ▪ 恒生指数 <b>-0.54%</b>（22952.09点）<br>
            ▪ 恒生科技指数 <b>-0.78%</b>（4371.54点）<br><br>
            <b>📊 本周回顾（6/23-6/26）：</b><br>
            ▪ 沪指本周累计 -0.8%·科创50回调明显<br>
            ▪ 光通信/AI板块持续活跃·"光里"基金限购潮延续<br>
            ▪ 工业金属/油气本周走强·地缘风险推升大宗
          </div>
          <div>
            <b>📊 美股最新收盘（6/26 周四）：</b><br>
            ▪ 道指 <b>+0.14%</b>（41920.62点）—— 相对抗跌<br>
            ▪ 纳指 <b>-0.46%</b>（25358.60点）—— 科技股承压<br>
            ▪ 标普500 <b>-0.01%</b>（7357.49点）—— 基本平收<br>
            ▪ 苹果跌逾<b>6%</b>（创2025年4月以来最大跌幅）<br><br>
            <b>📊 对基金行业影响（本周复盘）：</b><br>
            ▪ A股集体低开→客户可能关注回调买入机会<br>
            ▪ 光通信/AI持续活跃→相关主题基金受关注<br>
            ▪ 第二批基准调整落地→产品定位更清晰<br>
            ▪ 6月新发破千亿→机构看多后市信心增强
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·2026-06-27 10:00（周六休市）</span>
        <span class="source-tag">数据来源：06-26 收盘</span>
      </div>
    </div>
  </div>'''

# 替换 S6 section
html = re.sub(
    r'      <!-- ============ Section 6: 市场行情速览 ============ -->.*?<!-- ============ Section 7:',
    new_s6 + '\n      <!-- ============ Section 7:',
    html,
    flags=re.DOTALL
)

# ========== 7. 更新 S7 时间线 ==========
# 移除早于06-13的条目（06-12 SpaceX），新增06-26和06-27条目
# 当前S7：06-26、06-25、06-24、06-22、06-20、06-18、06-17、06-16、06-15、06-13、06-12(移除)
# 新增：06-27（第二批基准调整+新发破千亿）、保留06-26

new_s7 = '''<!-- ============ Section 7: 关键时间线 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--primary-light);color:var(--primary);">📅</div>
      <span class="section-title">关键时间线（近两周）</span>
      <span class="section-badge" style="background:var(--primary-light);color:var(--primary);">事件脉络</span>
    </div>

    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-27（第二批基准调整全面铺开·6月新发基金破千亿）</div>
          <div class="timeline-title">超90家公募管理人发布千余只产品基准调整公告 / 6月新发基金规模突破1012亿元</div>
          <div class="timeline-desc">第二批公募业绩比较基准调整全面铺开，千余只产品参与，基准改革从"试点探路"走向"系统推进"。同日，数据显示6月新发基金规模已破千亿，权益类担当主力军，FOF年内规模创峰值。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-26（A股集体低开·证监会法治协同·89家公募自购44亿）</div>
          <div class="timeline-title">A股四大股指集体低开（沪指-0.52%）/ 证监会推修基金法 / 89家公募年内自购44亿</div>
          <div class="timeline-desc">A股集体低开，工业金属/油气走强，半导体/培育钻石/CPO走弱。证监会公布五方面法治协同建设规划，推动修改证券投资基金法。年内89家公募机构合计自购44亿元，被动指数+债券型受青睐。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-25（A股分化·央行5000亿MLF·英伟达股东大会）</div>
          <div class="timeline-title">A股分化（沪指-0.18%·创业板+0.63%）/ 央行6/25开展5000亿MLF操作 / 英伟达股东大会</div>
          <div class="timeline-desc">A股开盘分化，沪指跌0.18%，创业板指涨0.63%，存储芯片/光刻机/光纤涨幅居前。央行开展5000亿元1年期MLF操作，净投放2000亿，连续两月加量续作。英伟达股东大会备受关注。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-24（浮费基金一周年·QDII限购加码）</div>
          <div class="timeline-title">首批浮费基金运作满一年·业绩断层（316% vs -12.84%）/ QDII限购加码（易方达降至10元）</div>
          <div class="timeline-desc">首批26只浮费基金运作满一年，华商致远回报A成"三倍基"，6只产品仍亏损，费率分档机制正式生效。QDII限购力度再加码，易方达全球成长精选降至10元，超百只QDII限购百元及以下。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-22（FOF破峰值·从千亿抢购到千元限购）</div>
          <div class="timeline-title">FOF年内新发规模破1100亿·超越2021年峰值 / 公募从"重规模"向"重回报"转型</div>
          <div class="timeline-desc">FOF年内新发规模达1137亿，超越2021年历史峰值。公募行业从"千亿抢购"到"千元限购"，标志着从"重规模"向"重回报""以持有人利益为本"转型。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot orange"></div>
        <div>
          <div class="timeline-date">2026-06-20（央行5000亿MLF·A股缩量5200亿）</div>
          <div class="timeline-title">央行6/20开展5000亿MLF操作·净投放2000亿 / A股成交额缩至5200亿</div>
          <div class="timeline-desc">央行开展5000亿元1年期MLF操作，净投放2000亿元，应对季末流动性压力。A股成交额缩至5200亿，市场观望情绪浓厚。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-18（2026陆家嘴论坛·吴清致辞）</div>
          <div class="timeline-title">2026陆家嘴论坛开幕·证监会主席吴清致辞·支持中小基金公司差异化发展</div>
          <div class="timeline-desc">2026陆家嘴论坛在上海开幕，证监会主席吴清发表致辞，宣布推出支持中小基金公司规范健康发展一揽子措施，坚持分类监管、突出特色。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-17（主动ETF指引落地·债券ETF规模突破）</div>
          <div class="timeline-title">沪深交易所发布主动ETF业务指引 / 债券ETF规模首超8500亿元（同比+180%）</div>
          <div class="timeline-desc">沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》，自发布之日起施行。同日，债券ETF总规模首次突破8500亿元，同比增长超180%。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-16（多只QDII科技ETF停牌·6月新基发行创同期新高）</div>
          <div class="timeline-title">纳指ETF易方达/国泰/景顺+创业板ETF富国因高溢价6/16停牌 / 6月前11天114只新基发行创历史同期新高</div>
          <div class="timeline-desc">多只QDII科技ETF因二级市场交易价格明显高于IOPV（溢价率最高超22%）于6/16开市起停牌，10:30起复牌。6月前11天114只新基发行创历史同期新高，上半年主动权益基金发行数量同比翻倍。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-15（多项公募新规落地·A股普涨科技收敛）</div>
          <div class="timeline-title">主题投资风格管理指引+适当性细则修订+公私兼任禁令三文同落 / A股沪指4096(+1.61%)普涨</div>
          <div class="timeline-desc">多项公募基金新规同日公布：主题投资风格管理指引（12/1施行）将风格漂移软约束转为硬约束；适当性细则修订加强65周岁以上高风险基金销售管理；公私兼任禁令防范利益冲突。</div>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-13（证监会三年行动计划发布·央行双工具加码）</div>
          <div class="timeline-title">证监会发布三年行动计划（2026-2028）+销售费用新规同步实施 / 央行互换便利扩至3000亿</div>
          <div class="timeline-desc">证监会6月13日正式发布《公募基金高质量发展三年行动计划（2026-2028）》，同步实施销售费用管理规定，费率改革第三阶段落地。央行同日宣布将互换便利扩至3000亿、股票回购增持再贷款延期扩容。</div>
        </div>
      </div>

    </div>
  </div>'''

html = re.sub(
    r'<!-- ============ Section 7: 关键时间线 ============ -->.*?  <!-- ============ Section 8:',
    new_s7 + '\n  <!-- ============ Section 8:',
    html,
    flags=re.DOTALL
)

# ========== 8. 更新 S8 待办跟踪 ==========
new_s8 = '''  <!-- ============ Section 8: 待办跟踪 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#eef2ff;color:var(--info);">📋</div>
      <span class="section-title">待办跟踪与行动建议</span>
      <span class="section-badge" style="background:var(--info-light);color:var(--info);">腾安行动清单</span>
    </div>

    <div class="card-grid">

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 第二批公募基准调整全面铺开·腾安需准备基准说明话术</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>第二批千余只公募基金产品业绩比较基准调整全面铺开，多数产品自7月27日起正式生效。基准校准让产品从"模糊标签"走向"清晰画像"。<br>
          <b>腾安行动建议：</b>① 在基金详情页突出业绩比较基准说明；② 准备基准调整相关的客户沟通话术；③ 梳理腾安代销产品中哪些参与了第二批基准调整。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理代销产品基准调整清单→产品部<br>
            ② 制作基准说明话术→营销部<br>
            ③ 更新基金详情页基准展示→技术部
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产罚款近6000万·私募严监管升级</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>证监会对玖瀛资产等罚款近6000万元，创"史上最重"私募处罚纪录。同步对实际控制人采取5年证券市场禁入及禁止交易措施。<br>
          <b>腾安行动建议：</b>① 审查腾安代销的私募产品合规性；② 将"零容忍"监管信号纳入内部合规培训；③ 关注私募监管升级对行业的影响。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 审查代销私募产品合规性→合规部<br>
            ② 更新合规培训材料→法务部<br>
            ③ 关注后续私募监管政策→产品部
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会推动修改证券投资基金法·五方面法治协同建设</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-26</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>证监会近日公布五方面资本市场法治协同建设规划，包括推动修改<b>证券投资基金法</b>、制定上市公司监督管理条例、完善域外适用规定等。<br>
          <b>腾安行动建议：</b>① 跟踪证券投资基金法修改立法进展，评估对腾安业务影响；② 关注"行刑民"立体追责机制完善，加强内部合规管理；③ 提前研究基金法修改对代销模式的影响。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 跟踪基金法修改立法进展→法务部<br>
            ② 评估对腾安代销业务影响→产品部<br>
            ③ 加强内部合规管理→风控部
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 浮费基金业绩分化·三倍基诞生·费率机制正式生效</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>首批浮费基金一周年，华商致远回报A成"三倍基"（316.56%），6只产品仍亏损（最高-12.84%）。运作满一年后费率按业绩分档正式生效。<br>
          <b>腾安行动建议：</b>① 评估腾安代销的浮费基金业绩表现，准备客户沟通话术；② 在基金详情页突出费率机制说明，避免销售误导；③ 关注浮动费率基金作为差异化产品卖点的营销机会。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理腾安代销浮费基金清单及业绩表现→产品部<br>
            ② 制作浮费基金费率机制说明话术→营销部<br>
            ③ 评估浮费基金作为差异化卖点的营销方案→运营部
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 QDII限购加码·易方达全球成长精选降至10元·超百只QDII限购百元及以下</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-24</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>QDII限购力度再加码，易方达全球成长精选混合(QDII)单日限额降至<b>10元</b>。超百只QDII限购百元及以下。近一年QDII平均收益22%，45只净值翻倍。<br>
          <b>腾安行动建议：</b>① 梳理腾安可代销的有额度QDII产品清单；② 准备QDII替代方案话术（港股通、互认基金、跨境ETF等）；③ 关注新一批QDII额度发放进展，提前布局。
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 行动清单</div>
          <div class="action-text">
            ① 梳理有额度的QDII产品清单→产品部<br>
            ② 制作QDII替代方案话术→营销部<br>
            ③ 跟踪新一批QDII额度发放进展→产品部
          </div>
        </div>
      </div>

      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 6月新发基金破千亿·FOF年内规模创峰值·机构看多后市</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">06-27</span>
          </div>
        </div>
        <div class="card-body">
          <b>核心事件：</b>截至6月26日，6月以来已成立176只新基金，发行规模达1012.29亿元。FOF年内发行规模达1177.42亿元，超越2021年创下的年度最高纪录。<br>
          <b>腾安行动建议：</b>① 积极储备新发基金销售资源；② 重点关注FOF产品机会；③ 研究机构看多后市的逻辑，优化基金推荐策略。
        </div>
      </div>

    </div>
  </div>'''

html = re.sub(
    r'  <!-- ============ Section 8: 待办跟踪 ============ -->.*?</body>',
    new_s8 + '\n\n</body>',
    html,
    flags=re.DOTALL
)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML更新完成！")
print(f"更新日期: {today}")
print("更新模块: Header + Stats Bar + S0 + S1 + S2 + S6 + S7 + S8")
