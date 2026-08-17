# -*- coding: utf-8 -*-
import io, sys

PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

def replace_block(start_marker, end_marker, new_body):
    global html
    i = html.index(start_marker)
    j = html.index(end_marker, i)
    html = html[:i] + new_body + html[j:]
    return True

# ---------------- S0 card-grid full replace ----------------
S0_START = '    <div class="card-grid">\n\n      <!-- S0 Card 1:'
S0_END = '    </div>\n  </div>\n\n<!-- ============ Section 1:'

s0_body = '''    <div class="card-grid">

      <!-- S0 Card 1: 摊余成本法债基重启 (T+0 08-15 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🟡 摊余成本法债基时隔数年重启申报·15家中小公募+外资上报63个月封闭式·扶持中小机构落地</div>
        </div>
        <div class="card-body">
          8月14日晚间证监会官网显示，<b>15家基金公司上报新一批摊余成本法债基</b>，均为<b>63个月封闭式债券型基金</b>。申报主体以中小公募为主——朱雀、易米、国融、兴合、鹏安、红土创新、百嘉等，同时包含<b>贝莱德、路博迈、安联、联博</b>等外资机构；业内人士透露后续或有第二批上报。<br>
          <b>政策含义：</b>摊余成本法债基通过封闭式运作+持有到期计价，净值波动小、稳健增长，单只规模常可达80亿元，对基金公司做大规模、代销机构提升保有量均有助益。此次重启被视为落实陆家嘴论坛吴清"支持中小基金公司规范健康发展一揽子措施"的具体动作——在产品布局、业务准入上给予倾斜。<br>
          <b>市场影响：</b>格上基金蒋睿认为短期或利好债市、尤其中长久期信用债，支撑信用利差维持低位，但整体推动力不宜高估；对基金行业则打开中小机构差异化规模增长通道。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L4C1QL090552C2FY.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
        </div>
      </div>

      <!-- S0 Card 2: 40只红利基金疑似漂移 (T+0 08-15 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🟡 40只主动权益基金疑似风格漂移·红利涨了"红利基金"却跟科技跌·建信高股息7月回撤两成</div>
        </div>
        <div class="card-body">
          财联社对5032只主动权益基金筛查（4721只可匹配二季度前十大重仓），按名称主题与实际重仓行业初筛出<b>40只"疑似漂移"</b>。最典型为<b>建信高股息主题</b>：二季度末第一大重仓中际旭创（占净值9.24%）、第二大新易盛（5.59%），前十大几乎全为光模块/半导体设备/电子材料，5只科技股合计占净值27.95%。<br>
          <b>背离最直观：</b>中证红利指数7月涨10.89%、7月以来涨9.08%，但建信高股息主题7月以来复权净值<b>下跌20.79%</b>——红利涨了它却跌两成。其合同对"高股息"界定宽泛（近3年有2次分红或股息率高于均值即可），中际旭创等科技股凭连续分红记录入选，虽合规却偏离投资者预期。<br>
          <b>监管呼应：</b>此现象恰与证监会第3期《机构监管情况通报》点名的C基金风格漂移形成行业级映射——监管已将《主题投资风格管理指引》精神提前落实检查，存量产品同样适用"监测-预警-纠偏"闭环。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L4C607JU05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
        </div>
      </div>

      <!-- S0 Card 3: 272只基金突破双十限制 (T-1 08-14 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-14</span>
          </div>
          <div class="card-title">🟡 272只基金持股突破"双十"限制·永赢产业机遇14.88%居首·971只顶格配置创历史新高</div>
        </div>
        <div class="card-body">
          财联社梳理：二季度末全市场<b>272只主动权益基金</b>持有单只个股市值超净值10%（占比5.48%），最高达<b>14.88%</b>（永赢产业机遇智选持有冰轮环境）；7只超12%。更宽口径下，<b>971只出现"顶格配置"（单股占比>9.5%），创历史新高</b>。<br>
          <b>法规留口：</b>"双十"限制（《运作管理办法》）允许两类豁免——因市场波动/合并/规模变动等管理人之外因素被动超10%的，可10交易日内调回；完全指数化投资的指数基金/ETF部分不受限。因此需区分"被动超标宽限期"与"主动加仓违规"。<br>
          <b>监管深意：</b>通报要求管理人密切关注与业绩比较基准偏离、避免集中投向单一细分行业——将集中度约束从个股"双十"抬升至行业赛道层面，与风格漂移治理双线并行。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L49PLGDS05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
        </div>
      </div>

      <!-- S0 Card 4: 主动ETF全球增长引擎+浦银安盛更名 (T-1 08-14 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">08-14</span>
          </div>
          <div class="card-title">🔵 主动ETF成全球增长引擎·近一年新发ETF中55%为主动·浦银安盛正式更名浦银基金</div>
        </div>
        <div class="card-body">
          <b>主动ETF全球爆发：</b>摩根资产管理发布2026年三季度《ETF环球市场纵览》显示，2016年初至2026年6月末亚太地区ETF总规模复合年均增长率达<b>26%</b>，截至6月末亚太ETF资产规模<b>2.68万亿美元</b>、其中中国市场占比<b>超过25%</b>。更关键的结构变化是：截至6月末，<b>近一年全球新发行ETF中55%为主动ETF</b>，主动ETF增速显著超越被动ETF，正成为ETF市场重要增长引擎。<br>
          <b>股东变动引发更名：</b>8月12日浦银安盛基金公告，中文法定名称变更为"<b>浦银基金管理有限公司</b>"，原因是法国巴黎资产管理控股公司吸收合并公司原第二大股东法国安盛投资管理公司。名称变但股权未变：浦发银行51%、法国巴黎资管39%、上海国盛集团资产10%。<br>
          <b>及其他动态：</b>嘉实京东仓储基础设施REIT首次扩募申请获上交所受理，拟定向扩募约10.51亿元新购西安/合肥两座高标仓，底层项目由3个增至5个；富国天惠（朱少醒）二季度减仓耐普矿机300万股、降为第七大流通股东。
        </div>
        <div class="card-footer">
          <span class="impact-tag low">影响：低</span>
          <a href="https://www.nbd.com.cn/articles/2026-08-14/4541843.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
        </div>
      </div>
    </div>
  </div>
'''

# adjust: S0_END should point to the marker AFTER card-grid close
replace_block(S0_START, S0_END, s0_body)

# ---------------- S1: add 2 cards before S1 card-grid close ----------------
S1_INSERT_BEFORE = '    </div>\n  </div>\n\n  <!-- ============ Section 2:'
s1_new = '''
      <!-- S1 Card NEW: 40只基金疑似风格漂移 (08-15) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-15</span>
          </div>
          <div class="card-title">🟡 40只主动权益基金疑似风格漂移·红利基金跟科技跌·建信高股息7月回撤20.79%</div>
        </div>
        <div class="card-body">
          财联社对5032只主动权益基金筛查，4721只可匹配二季度前十大重仓，按名称主题与实际重仓行业初筛出<b>40只"疑似漂移"</b>。最典型为<b>建信高股息主题</b>：二季度末前十大几乎全为光模块/半导体设备/电子材料（中际旭创占净值9.24%、新易盛5.59%），5只科技股合计占27.95%；中证红利7月涨10.89%背景下该基金7月以来复权净值<b>下跌20.79%</b>。监管已将《主题投资风格管理指引》精神提前落实检查，存量产品同样适用"监测-预警-纠偏"闭环。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L4C607JU05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
        </div>
      </div>

      <!-- S1 Card NEW: 272只基金突破双十限制 (08-14) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">08-14</span>
          </div>
          <div class="card-title">🟡 272只基金持股突破"双十"限制·永赢产业机遇14.88%居首·971只顶格配置创新高</div>
        </div>
        <div class="card-body">
          财联社梳理：二季度末全市场<b>272只主动权益基金</b>持有单只个股市值超净值10%，最高达<b>14.88%</b>（永赢产业机遇智选）；7只超12%。更宽口径下<b>971只出现"顶格配置"（单股>9.5%）创历史新高</b>。"双十"限制允许两类豁免——管理人之外因素被动超10%可10交易日内调回、指数化投资部分不受限。监管已将集中度约束从个股抬升至行业赛道层面。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L49PLGDS05198CJN.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">财联社</span></a>
        </div>
      </div>
'''
idx = html.index(S1_INSERT_BEFORE)
html = html[:idx] + s1_new + html[idx:]

# ---------------- S2: replace 07-31 card with 摊余成本法 card ----------------
S2_OLD = '''      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 四部门联合发布《关于健全金融机构治理的实施意见》·22条措施·重大问题终身问责</div>'''
S2_NEW = '''      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 摊余成本法债基重启申报·15家中小公募+外资上报63个月封闭式·扶持中小机构落地</div>'''
assert S2_OLD in html
html = html.replace(S2_OLD, S2_NEW, 1)

# also fix the date-tag and body/footer of that card (07-31 -> 08-15)
S2_OLD_DATE = '''            <span class="priority-tag urgent">紧急必看</span>
            <span class="date-tag">07-31</span>'''
S2_NEW_DATE = '''            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">08-15</span>'''
html = html.replace(S2_OLD_DATE, S2_NEW_DATE, 1)

S2_OLD_BODY = '''        <div class="card-body">
          <b>顶层落地：</b>7月31日，金融监管总局、中国人民银行、中国证监会、财政部联合发布《关于健全金融机构治理的实施意见》，从加强党的领导、改进股东治理、强化内部治理、加强和改进监管等方面提出<b>22条措施</b>，推动整治大股东违规干预、内部人控制等突出问题。明确到<b>2029年</b>基本形成权责边界清晰、激励约束相容、风险管理严格、运转规范高效的治理机制。<br>
          <b>股东防火墙：</b>要求严把股东准入关口，构建产业资本与金融资本<b>"防火墙"</b>——严禁违规跨业经营、杠杆率过高或存在严重失信、重大违法违规记录的企业和个人成为主要股东或实控人；穿透识别主要股东、实际控制人和受益所有人，严禁滥用股东权利违规干预经营，<b>严禁金融机构向股东及其关联方输送利益</b>，建立股东不当所得追回与风险责任事后追偿机制。<br>
          <b>差异化监管：</b>首次建立分级分类差异化监管体系，按实质重于形式原则对股东股权、关联交易实施穿透式监管；内部治理注重<b>长周期考核</b>，严格落实高管与关键岗位人员绩效薪酬<b>延期支付和追索扣回</b>制度；严防违法违规人员在金融行业内"带病流动"，对重大问题依法依规<b>终身问责</b>。<br>
          <b>对基金行业影响：</b>公募作为持牌金融机构同受约束→股权穿透、关联交易、薪酬递延与长周期考核要求将直接影响基金公司治理与激励安排，腾安需同步排查股东关联交易与考核机制合规性。
        </div>
        <div class="card-footer">
          <a href="https://news.cctv.cn/2026/08/01/ARTIXW4XG00juc2Aj3UQIY3I260801.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">央视网</span></a>
          <span class="impact-tag high">机构治理：高</span>
        </div>'''
S2_NEW_BODY = '''        <div class="card-body">
          <b>重启申报：</b>8月14日晚间证监会官网显示，<b>15家基金公司上报新一批摊余成本法债基</b>，均为<b>63个月封闭式债券型基金</b>。申报主体以中小公募为主——朱雀、易米、国融、兴合、鹏安、红土创新、百嘉等，同时包含<b>贝莱德、路博迈、安联、联博</b>等外资机构；业内人士透露后续或有第二批上报。<br>
          <b>产品逻辑：</b>摊余成本法通过封闭式运作+持有到期计价，净值波动小、稳健增长，单只规模常可达80亿元，对基金公司做大规模、代销机构提升保有量均有助益；机构愿牺牲流动性换取净值平滑，匹配长久期负债端需求。<br>
          <b>政策含义：</b>此举被视为落实陆家嘴论坛吴清"支持中小基金公司规范健康发展一揽子措施"的具体动作——在产品布局、业务准入上给予倾斜。格上基金蒋睿认为短期或利好债市、尤其中长久期信用债，但整体推动力不宜高估。
        </div>
        <div class="card-footer">
          <span class="impact-tag medium">影响：中</span>
          <a href="https://www.163.com/dy/article/L4C1QL090552C2FY.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报</span></a>
        </div>'''
assert S2_OLD_BODY in html
html = html.replace(S2_OLD_BODY, S2_NEW_BODY, 1)

# ---------------- Stats Bar: replace 4th card (index point) with structural ----------------
SB_OLD4 = '''    <div class="stat-card">
      <div class="stat-number">3926.96</div>
      <div class="stat-label">上证指数 · 2026-08-13收盘（上一交易日）</div>
      <div class="stat-change down">▼ -0.50%·尾盘跳水·两市成交2.55万亿·逾4300只飘绿</div></div>'''
SB_NEW4 = '''    <div class="stat-card">
      <div class="stat-number">272只</div>
      <div class="stat-label">主动权益基金持股破"双十"·08-14披露（周末不挂指数）</div>
      <div class="stat-change down">▼ 永赢产业机遇14.88%居首·971只顶格配置创新高</div></div>'''
assert SB_OLD4 in html
html = html.replace(SB_OLD4, SB_NEW4, 1)

# update stat card 2 (18.2亿 -> 摊余成本法, fresh) and card 3 (4只 -> 40只漂移)
SB_OLD2 = '''    <div class="stat-card">
      <div class="stat-number">18.2亿</div>
      <div class="stat-label">95家公募获配宇树科技 · 08-13披露</div>
      <div class="stat-change up">▲ 5117只产品参与·易方达2.58亿居首·6家超亿元</div>
    </div>'''
SB_NEW2 = '''    <div class="stat-card">
      <div class="stat-number">15家</div>
      <div class="stat-label">摊余成本法债基重启上报 · 08-15披露</div>
      <div class="stat-change up">▲ 63个月封闭式·中小公募+贝莱德等外资获倾斜</div>
    </div>'''
assert SB_OLD2 in html
html = html.replace(SB_OLD2, SB_NEW2, 1)

SB_OLD3 = '''    <div class="stat-card">
      <div class="stat-number">4只</div>
      <div class="stat-label">消费基金二季度切回消费本色 · 08-14报道</div>
      <div class="stat-change up">▲ 7月平均+1.44% vs 死守科技11只-14.46%</div>
    </div>'''
SB_NEW3 = '''    <div class="stat-card">
      <div class="stat-number">40只</div>
      <div class="stat-label">主动权益基金疑似风格漂移 · 08-15财联社</div>
      <div class="stat-change down">▼ 建信高股息7月回撤20.79%·红利涨它跌</div>
    </div>'''
assert SB_OLD3 in html
html = html.replace(SB_OLD3, SB_NEW3, 1)

# ---------------- S7: add 08-15 entries at top, remove 08-02 and 08-03 oldest ----------------
S7_TOP = '      <!-- 08-14 时间线条目 -->'
s7_new_top = '''      <!-- 08-15 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-15</div>
        <div class="timeline-title">摊余成本法债基重启·15家中小公募上报</div>
      </div>
      <!-- 08-15 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-15</div>
        <div class="timeline-title">40只基金疑似风格漂移·红利基金跟科技跌</div>
      </div>
      <!-- 08-14 时间线条目 -->'''
assert S7_TOP in html
html = html.replace(S7_TOP, s7_new_top, 1)

# remove 08-02 item
S7_RM2 = '''      <!-- 08-02 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-02</div>
        <div class="timeline-title">主动ETF落地倒计时18家管理人系统测试收尾</div>
      </div>
'''
assert S7_RM2 in html
html = html.replace(S7_RM2, '', 1)

# remove 08-03 item
S7_RM3 = '''      <!-- 08-03 时间线条目 (NEW) -->
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div class="timeline-date">2026-08-03</div>
        <div class="timeline-title">公募前七月业绩大洗牌·翻倍基仅剩2只</div>
      </div>
'''
assert S7_RM3 in html
html = html.replace(S7_RM3, '', 1)

# update header date fingerprint
html = html.replace('<!-- daily-update: 2026-08-14 -->', '<!-- daily-update: 2026-08-15 -->', 1)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("OK written")
