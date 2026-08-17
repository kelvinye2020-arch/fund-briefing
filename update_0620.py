#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金行业资讯看板 2026-06-20 自动更新脚本
- 今天是周六，端午休市期间
- 更新 S0/S1/S2/S6/S7/S8 模块
- 清理 T-14 之前（06-06 之前）的旧条目
"""

import re
import datetime

# 读取文件
with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件读取成功，长度: {len(content)}")

# ========== 1. 更新 HTML 头部 daily-update 标记 ==========
content = content.replace(
    '<!-- daily-update: 2026-06-19 -->',
    '<!-- daily-update: 2026-06-20 -->'
)
print("✓ 更新 daily-update 标记")

# 更新 content-fingerprint
content = content.replace(
    'content="美联储转鹰年内或加息一次|端午三市同休6/19-21|SpaceX挂牌后首周走势震荡|五部门新能源车下乡活动启动"',
    'content="陆家嘴论坛闭幕三大监管定调|主动ETF获批沪深同步推出|端午休市A股6/22开市|美联储沃什首秀转鹰"'
)
print("✓ 更新 content-fingerprint")

# ========== 2. 更新 Header 数据区间 ==========
content = content.replace(
    '数据区间：2026.06.05 — 2026.06.19（今日自动更新）',
    '数据区间：2026.06.06 — 2026.06.20（今日自动更新）'
)
print("✓ 更新 Header 数据区间")

# ========== 3. 更新 Stats Bar ==========
old_stats = '''<!-- Stats Bar -->
<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">端午三市同休</div>
    <div class="stat-label">6/19-21 A股/港股通/美股均休市·节后6/22开市·持币过节情绪主导·跨境资产价格波动</div>
    <div class="stat-change up">▲ 三市同休历史罕见·黄金/日韩等跨市场基金资产价格节后更新·关注假期海外市场变化</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">美联储转鹰·年内或加息</div>
    <div class="stat-label">6/18沃什首秀维持不变但点阵图中值升至3.75%-4.0%·暗示年内可能加息一次·2027降息窗口延后</div>
    <div class="stat-change up">▲ 滞胀困境（增长放缓+通胀居高）·QDII产品波动风险上升·全球央行政策分化加剧</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">沪指4090·科创+3.84%</div>
    <div class="stat-label">6/18收盘沪指4090(-0.43%)·深成指16030(+0.94%)·创业板4252(+2.05%)·科创50+3.84%·成交3.31万亿</div>
    <div class="stat-change up">▲ 科技风格极致分化·芯片/半导体强者恒强·沪深300ETF净流出137亿机构高位兑现</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">五部门新能源车下乡</div>
    <div class="stat-label">工信部/商务部等五部门启动2026新能源车下乡·深入推进汽车以旧换新进乡村·A股新能源车板块震荡</div>
    <div class="stat-change up">▲ 政策催化·但新能源车板块短期震荡为主·7月后或有表现·关注相关主题基金</div>
  </div>
</div>''

new_stats = '''<!-- Stats Bar -->
<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-number">陆家嘴论坛闭幕·三大监管定调</div>
    <div class="stat-label">6/18闭幕·央行/证监会/金融监管总局一把手集体发声·不走注水救市老路·转向制度改革替代短期刺激</div>
    <div class="stat-change up">▲ 货币政策转向资本成本锚定·金融监管强化风险出清·资本市场强化制度闭环</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">主动ETF获批·沪深同步推出</div>
    <div class="stat-label">6/17陆家嘴论坛吴清宣布抓紧推出主动ETF·沪深交易所同步发布业务指引·全透明方式每日披露申赎清单</div>
    <div class="stat-change up">▲ 公募产品重大创新·主动管理+ETF结构融合·ETF行业进入主动化时代</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">端午休市中·6/22开市</div>
    <div class="stat-label">6/19-21 A股/港股通/美股三市同休·历史罕见·节前最后交易日6/18沪指4090(-0.43%)·科技分化</div>
    <div class="stat-change neutral">■ 休市期间海外市场风险积累·节后6/22开市关注QDII净值更新·持币过节情绪主导</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">美联储沃什首秀·年内或加息</div>
    <div class="stat-label">6/18点阵图中值升至3.75%-4.0%·暗示年内可能加息一次·2026全年GDP下调至2.2%·核心PCE上调</div>
    <div class="stat-change up">▲ 滞胀困境·全球债市遭抛售·QDII美股产品节后或承压·关注客户咨询高峰</div>
  </div>
</div>'''

if old_stats in content:
    content = content.replace(old_stats, new_stats)
    print("✓ 更新 Stats Bar")
else:
    print("✗ Stats Bar 未找到匹配，尝试模糊匹配...")
    # 尝试部分匹配
    if '端午三市同休' in content:
        print("  - 找到'端午三市同休'关键词")
    else:
        print("  - 未找到'端午三市同休'关键词，Stats Bar可能已更新")

# ========== 4. 更新 S0 今日焦点 ==========
# 由于 S0 内容较长，直接替换整个 Section 0
old_s0_start = '<!-- ============ Section 0: 今日焦点 ============ -->'
old_s0_end = '<!-- ============ Section 1: 重磅信息 ============ -->'

if old_s0_start in content and old_s0_end in content:
    s0_start_idx = content.find(old_s0_start)
    s0_end_idx = content.find(old_s0_end)
    
    new_s0 = '''<!-- ============ Section 0: 今日焦点 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#fef2f2;color:var(--danger);">🔥</div>
      <span class="section-title">今日焦点（6月20日·周六·端午休市·陆家嘴论坛闭幕解读·主动ETF获批）</span>
      <span class="section-badge" style="background:var(--danger-light);color:var(--danger);">今日更新</span>
    </div>

    <div class="card-grid">
      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 陆家嘴论坛6/18落幕！三大监管定调：不走注水救市老路·转向制度改革替代短期刺激</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-18~20</span>
          </div>
        </div>
        <div class="card-body">
          <b>论坛落幕：</b>6月18日，为期两天的2026陆家嘴论坛落下帷幕。何立峰副总理出席开幕式，央行行长潘功胜、金融监管总局局长丁向群、证监会主席吴清集体发声。<b>"上海正从全球资本的热门选项，变成全球资本的首选之地"</b>成为论坛最强音。<br>
          <b>三大监管核心定调：</b>①<b>央行</b>：货币政策框架转向"资本成本锚定"，完善短端利率调控机制，推动低利率势能转化为实体融资与资产定价动能。高股息红利资产的"类债属性"将被重估。②<b>金融监管总局</b>：金融监管核心转向"风险出清"，中小金融机构"减量提质""硬约束"的改革方向明确。③<b>证监会</b>：强化资本市场"制度闭环"建设，IPO端压紧压实全链条发行责任，退市端推动退市常态化，强化财务造假立体追责。<br>
          <b>对基金行业影响：</b>①高股息红利资产估值中枢将获永久性抬升→高股息主题基金/红利ETF需求持续增长；②被动投资产品迎来长期发展机遇→宽基ETF/行业ETF规模持续扩张；③壳价值消失→主动权益基金更依赖基本面研究能力；④行业合规要求大幅提升→劣币出清加速。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1868342464377485237" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·闭幕解读</span></a>
          <a href="https://www.shanghai.gov.cn/nw4411/20260619/1bfc2322573745a5803b55dedd9fa551.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海政府网</span></a>
          <span class="impact-tag high">监管定调：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 红利资产估值抬升→加大高股息/红利ETF/红利主题基金推荐权重；<br>
            ② 被动投资长期利好→评估腾安ETF产品货架覆盖是否充分；<br>
            ③ 合规要求提升→提前规划《三年行动计划》落实方案，关注监管细则落地节奏。
          </div>
        </div>
      </div>

      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 主动ETF获批！吴清6/17陆家嘴宣布·沪深交易所同步发布业务指引·公募产品重大创新</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-17~20</span>
          </div>
        </div>
        <div class="card-body">
          <b>政策宣布：</b>6月17日，证监会主席吴清在2026陆家嘴论坛上发表演讲时明确表示，将"抓紧推进在沪深交易所上市主动ETF"，顺应全球市场发展趋势，同时试点商业不动产REITs。<br>
          <b>业务指引落地：</b>同日，沪深交易所发布《主动管理交易型开放式证券投资基金业务指引》，对主动ETF的持股数量、集中度、成分股流动性作出规定，并明确主动ETF将采用<b>全透明方式</b>每日对外披露申赎清单。相比传统主动基金，ETF结构将大幅提升透明度和交易便利性。<br>
          <b>行业意义：</b>主动ETF是2026年公募行业最具颠覆性的产品创新，将"主动管理投资能力"与"ETF交易便利"融合。美国主动ETF过去5年爆发式增长，中国正式加入这一赛道。<br>
          <b>对基金行业影响：</b>①头部基金公司（易方达/华夏/富国等）将率先布局；②传统主动权益基金面临主动ETF的替代竞争；③ETF行业从"被动跟踪"进入"主动管理"新纪元。
        </div>
        <div class="card-footer">
          <a href="https://baijiahao.baidu.com/s?id=1868245517547807009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·主动ETF</span></a>
          <a href="https://baijiahao.baidu.com/s?id=1868406706008181168" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">百家号·信号解读</span></a>
          <span class="impact-tag high">产品创新：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 主动ETF获批→提前与头部基金公司沟通产品储备，抢占首发代销份额；<br>
            ② 产品培训→内部快速学习主动ETF vs 传统主动基金的差异，准备投资者教育材料；<br>
            ③ 组合策略→研究"主动ETF+被动ETF"混合配置策略，丰富投顾服务工具箱。
          </div>
        </div>
      </div>

      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 端午三市同休持续·节后6/22开市·美联储鹰派信号假期发酵·QDII产品节后或承压</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-19~20</span>
          </div>
        </div>
        <div class="card-body">
          <b>休市状态：</b>6/19（周五）至6/21（周日）A股/港股通/美股三市同休，历史罕见。6/22（周一）起照常开市。<br>
          <b>假期发酵信号：</b>①美联储6/18议息结果（沃什首秀点阵图转鹰，年内加息预期升温）在假期期间持续发酵；②欧洲央行已重启加息25bp，全球央行政策分化加剧；③SpaceX以135美元/股正式挂牌后首周走势震荡；④陆家嘴论坛闭幕信号（三大监管定调）在周末持续解读。<br>
          <b>节后关注：</b>①QDII美股产品可能面临净值压力和赎回（美股6/18集体收跌）；②科技风格能否延续（节前科创50+3.84%）；③黄金/日韩等跨市场基金资产价格将在节后更新；④主动ETF获批消息可能成为节后催化热点。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.cn/2026-06-18/detail-inicvvzp5363094.d.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·休市</span></a>
          <a href="https://finance.eastmoney.com/a/202606183775060947.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·美联储</span></a>
          <span class="impact-tag high">端午休市：极高</span>
        </div>
      </div>

    </div>
  </div>

  '''
    
    content = content[:s0_start_idx] + new_s0 + content[s0_end_idx:]
    print("✓ 更新 S0 今日焦点")
else:
    print("✗ S0 今日焦点段落标记未找到")

# ========== 5. 清理 S1 重磅信息中 T-14 之前的旧条目 ==========
# T-14 = 2026-06-06，需要删除 06-05 及之前的条目
# 当前 S1 中最旧的是 06-05（中证金牛出清），需要检查是否保留
# 根据规则：仅保留 T-14 ~ T 的事件，即 06-06 ~ 06-20
# 当前 S1 有 06-05 的条目（中证金牛），需要删除或替换

print("\n--- S1 重磅信息时效性清理 ---")
# 查找并删除 date-tag 为 06-05 的卡片（中证金牛）
old_s1_card = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 中证金牛主动退场！招商/嘉实/兴证全球/汇添富等集体终止合作，第三方代销出清提速</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">06-05</span>
          </div>
        </div>
        <div class="card-body">
          <b>界面新闻6月5日报道：</b>近日招商基金、嘉实基金、创金合信、金鹰基金、兴证全球、汇添富等多家公募先后公告，终止与<b>中证金牛（北京）基金销售有限公司</b>全部销售业务合作。<br>
          <b>出清路径：</b>投资者通过中证金牛持有的基金份额将转至基金公司直销平台。此前前海开源/平安/国金/新华等已于6月1日终止合作，6月9日起兴证全球终止。<br>
          <b>行业趋势：</b>第三方代销渠道加速出清→中小代销机构生存空间收窄。直销费率改革（零费率）+代销集中度提升→蚂蚁/天天/腾安等头部平台受益。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260605A04TN700" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">界面新闻</span></a>
          <a href="https://fund.eastmoney.com/gonggao/014900,AN202606061823317483.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富·公告</span></a>
          <span class="impact-tag high">代销格局：极高</span>
        </div>
      </div>'''

if old_s1_card in content:
    content = content.replace(old_s1_card, '')
    print("✓ 删除 S1 中 06-05 过期条目（中证金牛）")
else:
    print("  未找到 S1 06-05 条目（可能已删除）")

# ========== 6. 清理 S2 监管政策中 T-14 之前的旧条目 ==========
print("\n--- S2 监管政策时效性清理 ---")
# S2 中最旧的是 06-05（国办私募基金指导意见），需要保留（06-05 = T-15，超出T-14）
# 但 06-05 是 15天前，T-14 = 06-06，所以 06-05 应该删除

old_s2_card = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 国办发文：23万亿私募基金迎顶层设计！全链条严监管+三年行动方案，出清5444家管理人</div>
          <div class="card-meta">
            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">06-05</span>
          </div>
        </div>
        <div class="card-body">
          <b>国办函〔2026〕54号：</b>6月5日，国务院办公厅正式发布《关于加强监管防范风险促进私募投资基金高质量发展的指导意见》，这是私募基金行业首份国务院层面的系统性顶层设计文件。<br>
          <b>核心措施：</b>严控新设基金管理人、加速出清"僵尸"机构。2023年至2026年Q1，已对<b>1805家</b>私募基金管理人采取行政监管/处罚措施，移送公安86条犯罪线索，中基协注销<b>5444家</b>管理人。<br>
          <b>行业影响：</b>证监会将制定三年行动方案，完善"N+X"规则体系→私募"野蛮生长"终结，公募/持牌销售渠道合规优势进一步凸显。
        </div>
        <div class="card-footer">
          <a href="http://www.csrc.gov.cn/csrc/c100028/c7637247/content.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证监会</span></a>
          <a href="https://www.news.cn/fortune/20260605/175e1b9846754b21af16a905a68d857c/c.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新华网</span></a>
          <span class="impact-tag high">私募顶层设计：极高</span>
        </div>
        <div class="action-box">
          <div class="action-label">⚡ 腾安行动建议</div>
          <div class="action-text">
            ① 私募全面收紧→高净值客户资金向公募/持牌代销渠道加速转移，关注增量客户获取机会；<br>
            ② 研究指导意见细则中对销售机构的新要求，评估腾安合规体系是否需同步升级。
          </div>
        </div>
      </div> '''

if old_s2_card in content:
    content = content.replace(old_s2_card, '')
    print("✓ 删除 S2 中 06-05 过期条目（国办私募基金）")
else:
    print("  未找到 S2 06-05 条目（可能已删除）")

# ========== 7. 更新 S6 市场行情速览 ==========
print("\n--- S6 市场行情速览更新 ---")
# 今天是周六休市，更新为休市状态说明
old_s6 = '''    <div class="card p3">
      <div class="card-top">
        <div class="card-title">端午休市·节前最后交易日（6/18）收盘数据 + 美联储鹰派持续发酵·节后6/22开市</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 节前最后交易日（6/18）收盘：</b>A股分化，沪指<b>4090点(-0.43%)</b>，深证成指<b>16030点(+0.94%)</b>，创业板指<b>4252点(+2.05%)</b>，科创50指数<b>涨3.84%</b>。芯片/半导体强者恒强，兆易创新涨停+10%。全市场成交<b>3.31万亿</b>，较前日放量2177亿。<br><br>
            <b>📊 港股（6/18）：</b>恒生指数<b>跌1.59%</b>，恒生科技指数<b>跌1.39%</b>，美联储鹰派预期压制港股科技板块。<br><br>
            <b>📊 端午休市：</b>6/19-6/21休市，6/22（周一）开市。三市同休（A股+港股通+美股）历史罕见。
          </div>
          <div>
            <b>📊 美股（6/18 美联储议息后）：</b><br>
            ▪ 道指 <b>-0.98%</b>（美联储鹰派信号压制）<br>
            ▪ 纳指 <b>-1.34%</b>（科技权重股领跌）<br>
            ▪ 标普500 <b>-1.21%</b><br>
            ▪ 沃什首秀点阵图转鹰，年内加息预期升温<br><br>
            <b>📊 对基金行业影响（节后）：</b><br>
            ▪ 美联储转鹰→QDII美股产品节后或承压<br>
            ▪ 科技风格极致分化→节后关注科创50能否延续<br>
            ▪ 三市同休→跨市场基金节后价格更新，黄金/海外资产需重点关注
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·6/18收盘</span>
        <span class="source-tag">端午休市·6/19-21</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div> '''

new_s6 = '''    <div class="card p3">
      <div class="card-top">
        <div class="card-title">端午休市中（6/19-21）·节前最后交易日（6/18）收盘 + 陆家嘴闭幕解读·节后6/22开市</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 节前最后交易日（6/18）收盘：</b>A股分化，沪指<b>4090点(-0.43%)</b>，深证成指<b>16030点(+0.94%)</b>，创业板指<b>4252点(+2.05%)</b>，科创50指数<b>涨3.84%</b>。芯片/半导体强者恒强。全市场成交<b>3.31万亿</b>。<br><br>
            <b>📊 港股（6/18）：</b>恒生指数<b>跌1.59%</b>，恒生科技<b>跌1.39%</b>，美联储鹰派预期压制港股科技。<br><br>
            <b>📊 端午休市：</b>6/19-6/21休市，<b>6/22（周一）开市</b>。三市同休历史罕见。
          </div>
          <div>
            <b>📊 周末解读焦点：</b><br>
            ▪ 陆家嘴论坛闭幕，三大监管定调持续发酵<br>
            ▪ 央行：货币政策转向资本成本锚定<br>
            ▪ 金融监管总局：风险出清+减量提质<br>
            ▪ 证监会：制度闭环+退市常态化<br><br>
            <b>📊 节后关注（6/22）：</b><br>
            ▪ 主动ETF获批催化→科技/ETF板块或活跃<br>
            ▪ QDII美股产品净值压力→美联储转鹰<br>
            ▪ 跨市场基金价格更新→黄金/海外资产
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">端午休市中·6/19-21</span>
        <span class="source-tag">节后6/22开市</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div> '''

if old_s6 in content:
    content = content.replace(old_s6, new_s6)
    print("✓ 更新 S6 市场行情速览")
else:
    print("  未找到 S6 旧内容，可能已更新")

# ========== 8. 更新 S7 时间线 ==========
# 删除 06-06 之前的条目，添加 06-20 条目
print("\n--- S7 时间线更新 ---")

# 删除时间线中 06-06 的条目（中基协换届）
old_timeline_0606 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-06（中基协换届刘晓艳当选会长·吴清四个坚持定调·翻倍基增至17只）</div>
          <div class="timeline-title">中基协第四届换届：易方达刘晓艳当选兼职会长 / 吴清定调"四个坚持" / 年内翻倍基增至17只</div>
          <div class="timeline-desc">中基协空缺两年后完成换届，刘晓艳为23年来首位头部公募女性掌门人。吴清在第四届会员代表大会上明确定调"四个坚持"。年内翻倍基增至17只引发抱团争议。华盛证券6/15起暂停内地新开仓，跟进跨境券商整治。</div>
        </div>
      </div>'''

if old_timeline_0606 in content:
    content = content.replace(old_timeline_0606, '')
    print("✓ 删除 S7 中 06-06 过期时间线条目")

# 添加 06-20 时间线条目（陆家嘴论坛闭幕解读）
new_timeline_0620 = '''      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-20（陆家嘴论坛闭幕解读·三大监管定调持续发酵·主动ETF获批行业热议）</div>
          <div class="timeline-title">陆家嘴论坛6/18闭幕 / 三大监管定调（央行资本成本锚定+金融监管风险出清+证监会制度闭环）/ 主动ETF获批沪深同步推出 / 端午休市中A股6/22开市</div>
          <div class="timeline-desc">陆家嘴论坛闭幕信号在周末持续发酵：央行货币政策框架转向"资本成本锚定"，高股息红利资产估值中枢将获永久性抬升；金融监管总局明确"风险出清""减量提质"方向；证监会强化"制度闭环"建设，退市常态化+财务造假立体追责。主动ETF获批成为公募产品重大创新方向。端午休市期间（6/19-21）A股/港股通/美股三市同休，6/22开市后关注主动ETF催化和QDII净值压力。</div>
        </div>
      </div>

'''

# 在时间线区域的开头添加新条目
timeline_marker = '<!-- ============ Section 7: 关键时间线 ============ -->'
if timeline_marker in content:
    # 找到时间线区域，在第一个 timeline-item 之前插入新条目
    timeline_start = content.find(timeline_marker)
    first_item_idx = content.find('<div class="timeline-item">', timeline_start)
    if first_item_idx > 0:
        # 在第一个 timeline-item 之前插入
        content = content[:first_item_idx] + new_timeline_0620 + content[first_item_idx:]
        print("✓ 添加 S7 06-20 时间线条目")
    else:
        print("  未找到时间线条目插入点")
else:
    print("  未找到 S7 时间线区域")

# ========== 9. 更新 Footer ==========
content = content.replace(
    '数据更新时间：2026年6月19日 10:30 · 近两周核心资讯（06-05 — 06-19）',
    '数据更新时间：2026年6月20日 10:30 · 近两周核心资讯（06-06 — 06-20）'
)
print("✓ 更新 Footer 数据更新时间")

# ========== 10. 写回文件 ==========
with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 文件更新完成！")
print(f"最终文件长度: {len(content)}")
