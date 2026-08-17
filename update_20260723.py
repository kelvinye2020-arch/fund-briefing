# -*- coding: utf-8 -*-
"""Daily update 2026-07-23 for 基金行业资讯看板.
Anchor-based replacements with global div-balance assertion.
T = 2026-07-23 (Thursday, normal trading day). T-14 = 2026-07-09.
"""
import io, sys

PATH = "index.html"
with io.open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

def gbal(t):
    return (t.count("<div"), t.count("</div>"))

def assert_eq(a, b, msg):
    if a != b:
        raise SystemExit("ASSERT FAIL: %s  opens=%d closes=%d" % (msg, a, b))

# ---- baseline ----
base_open, base_close = gbal(s)
print("baseline div balance:", base_open, base_close)
assert_eq(base_open, base_close, "baseline")

def replace_block(start_marker, end_marker, new_block, label):
    global s
    i = s.index(start_marker)
    j = s.index(end_marker, i)
    old = s[i:j]
    o0, c0 = gbal(old)
    s = s[:i] + new_block + s[j:]
    o1, c1 = gbal(new_block)
    print("[%s] old(%d/%d) new(%d/%d) -> global(%d/%d)" %
          (label, o0, c0, o1, c1, *gbal(s)))
    assert_eq(gbal(s)[0], gbal(s)[1], label + " global after")

# ============ 1. daily-update marker (line 2) ============
assert "<!-- daily-update: 2026-07-22 -->" in s
s = s.replace("<!-- daily-update: 2026-07-22 -->",
              "<!-- daily-update: 2026-07-23 -->", 1)

# ============ 2. meta keywords (lines 6-7) ============
OLD_META = ("二季度公募规模近40万亿|公募十大重仓股洗牌中际旭创登顶|"
            "超3000亿股票ETF逆市抄底|创新药主题基金规模破1500亿|A股07-21深V反弹双创领涨")
NEW_META = ("Q2公募盈利1.94万亿|座次出炉万亿俱乐部瘦身|"
            "公募重仓6进6出科技占八成|券商密集回购稳市12.6亿|易方达高管变更")
assert OLD_META in s
s = s.replace(OLD_META, NEW_META)

# ============ 3. Stats Bar (4 cards) ============
STAT_START = '    <div class="stat-card">\n      <div class="stat-number">3880.13</div>'
STAT_END = '  </div>\n<div class="main">'
NEW_STATS = '''    <div class="stat-card">
      <div class="stat-number">3874.90</div>
      <div class="stat-label">上证综指 · 07-23盘中+0.20%·三大指数集体高开震荡·创业板领涨</div>
      <div class="stat-change up">▲ A股集体高开·能源金属/贵金属/半导体领涨·白酒煤炭回调</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">+1.40%</div>
      <div class="stat-label">创业板指 · 07-23盘中领涨·算力硬件/能源金属走强·科创分化</div>
      <div class="stat-change up">▲ 科技成长延续活跃·硬科技主线未动摇</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">38.31万亿</div>
      <div class="stat-label">公募二季度末规模 · 座次出炉·万亿俱乐部由11家瘦身至10家</div>
      <div class="stat-change up">▲ 总规模再创新高·易方达/华夏/广发稳居前三</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">1.94万亿</div>
      <div class="stat-label">二季度公募盈利 · 权益类成主力·混合9509亿+股票7689亿</div>
      <div class="stat-change up">▲ 二季报收官·固收贡献近2000亿正利润</div>
    </div>
'''
replace_block(STAT_START, STAT_END, NEW_STATS, "Stats")

# ============ 4. S0 section-title (line 570) ============
OLD_TITLE = ('      <span class="section-title">今日焦点（7月22日·周三·二季度公募规模近40万亿·'
             '重仓股洗牌中际旭创登顶·超3000亿股票ETF逆市抄底·创新药主题基金破1500亿）</span>')
NEW_TITLE = ('      <span class="section-title">今日焦点（7月23日·周四·Q2公募盈利1.94万亿·'
             '座次出炉万亿俱乐部瘦身·重仓6进6出科技占八成·知名经理放松限购）</span>')
assert OLD_TITLE in s
s = s.replace(OLD_TITLE, NEW_TITLE, 1)

# ============ 5. S0 cards (replace all 4 with 07-23) ============
S0_START = '                    <!-- S0 Card 1: 二季度公募规模近40万亿 (T+0 07-22 P1) -->'
S0_END = '  </div>\n<!-- ============ Section 1:'
NEW_S0 = '''                    <!-- S0 Card 1: Q2公募盈利1.94万亿·座次出炉 (T+0 07-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 二季度公募盈利1.94万亿元·座次出炉·万亿俱乐部由11家瘦身至10家</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>盈利出炉：</b>天相投顾数据显示，2026年二季度公募基金整体盈利<b>19390.35亿元</b>，权益类基金为盈利主力——混合型基金利润9509.81亿元、股票型基金7689.44亿元，QDII与FOF亦为正。<br>
          <b>规模座次：</b>截至二季度末全市场14352只产品、总规模<b>38.31万亿元</b>；基金管理人"万亿俱乐部"成员由11家减至<b>10家</b>，易方达、华夏、广发稳居前三，前十公司规模环比均增长。<br>
          <b>对基金行业影响：</b>盈利与规模双高印证居民资金持续入市；腾安可借势强化"优中选优、长期持有"配置主线，引导客户关注绩优主动管理产品。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260723A03PDS00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">盈利规模：高</span>
        </div>
      </div>
    <!-- S0 Card 2: 公募重仓6进6出·科技占前20大八成·抱团极值 (T+0 07-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟠 公募重仓"6进6出"大洗牌·科技占前20大重仓八成·抱团集中度达历史极值</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>硬科技霸榜：</b>二季报收官，硬科技股首次彻底主导主动偏股型基金前十大重仓，出现"6进6出"大幅调整；中际旭创以1662.53亿元市值蝉联第一（被1816只基金持有），腾讯控股退至28位、贵州茅台退至30位。<br>
          <b>行业收敛：</b>前20大重仓股中电子14只、通信2只，科技相关合计占比达<b>八成</b>；主动偏股基金电子持仓约43%、通信约17%，真实AI抱团比例或达70%，刷新2015年以来新高。<br>
          <b>对基金行业影响：</b>持仓极致收敛隐含回撤风险——腾安推荐需提示"高位拥挤、勿追涨"，强化组合配置与分散话术。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260723A04H1W00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·21世纪经济报道</span></a>
          <span class="impact-tag medium">持仓风向：高</span>
        </div>
      </div>
    <!-- S0 Card 3: 多位知名基金经理放松限购 (T+0 07-23 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 多位知名基金经理放松限购·陈文凯华泰柏瑞两只1万元→100万元</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>限购松绑：</b>自7月22日起，陈文凯管理的华泰柏瑞质量精选、华泰柏瑞质量成长放松限购，大额申购（含转换转入、定投）限制金额由<b>1万元上调至100万元</b>。<br>
          <b>信号意义：</b>在二季度科技行情走强、多只绩优产品规模与净值双升后，部分基金经理选择打开申购闸门，既是对后续资金面的乐观，也为客户提供了低位布局窗口。<br>
          <b>对基金行业影响：</b>限购松绑释放供给信号→腾安可借势丰富绩优主动权益货架，做好客户承接与风险提示。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260723A03PDS00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">限购松绑：中</span>
        </div>
      </div>
    <!-- S0 Card 4: 易方达高管变更·胡剑离任专注投资 (T+0 07-23 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 易方达高管变更·胡剑离任专注投资·付浩新任副总经理级</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>人事调整：</b>7月22日易方达发布三则高管变更公告：胡剑因工作需要于7月20日离任副总经理级职务、将专注投资管理工作（现任管理规模586.23亿元）；付浩新任公司副总经理级高级管理人员，张南因个人原因离任。<br>
          <b>头部动向：</b>作为公募"万亿俱乐部"榜首机构，易方达投研核心的分工调整，折射头部公司对主动投资能力的再加码。<br>
          <b>对基金行业影响：</b>头部机构治理变动→腾安代销需关注核心基金经理在管产品稳定性与衔接。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260723A03PDS00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag low">公司动态：中</span>
        </div>
      </div>
    </div>
'''
replace_block(S0_START, S0_END, NEW_S0, "S0")

# ============ 6. S1: remove 3 expired 07-08, keep 3, add 07-23 券商回购 ============
S1_START = '<!-- S1 Card NEW: 商业不动产REITs成上半年申报主力 (07-09) -->'
S1_END = '  </div>\n\n  <!-- ============ Section 2: 监管政策 ============ -->'
NEW_S1 = '''      <!-- S1 Card NEW: 商业不动产REITs成上半年申报主力 (07-09) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 商业不动产REITs成上半年申报主力·8只上市募资297亿·4只商业REIT占68%</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-09</span>
          </div>
        </div>
        <div class="card-body">
          <b>申报主力：</b>上半年有8只公募REITs正式上市，合计募资<b>297.38亿元</b>。其中4只商业不动产REITs合计募资<b>203.32亿元</b>，占总募资规模比重达<b>68.37%</b>，成为申报与发行主力。<br>
          <b>认购热度：</b>国泰海通砂之船商业REIT、中信建投首农商业REIT、中金唯品会商业REIT、汇添富上海地产商业REIT的网下认购倍数分别达103.81倍、80.16倍、68.03倍、22.27倍；4只基础设施REITs认购倍数全部超百倍。<br>
          <b>对基金行业影响：</b>商业不动产REITs供需两旺→腾安可丰富REITs/固收+货架，为低利率环境下客户配置提供新选项。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260709A028XB00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">REITs：中</span>
        </div>
      </div>

      <!-- S1 Card NEW: 公募基金发行再平衡·科技与红利共发·本周41只新基 (07-16) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募基金发行再平衡·科技与红利共发·本周41只新基·权益占58.54%·红利偏债12只</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-16</span>
          </div>
        </div>
        <div class="card-body">
          <b>供给均衡：</b>公募排排网数据，7月13日—19日全市场41只新基开启募集，较前一周增7.89%；权益类24只占58.54%，但科技主题已非单一主角，产品拓展至化工、医药、地产、新能源等多元方向。<br>
          <b>防御补位：</b>41只中红利主题+偏债型基金合计12只、占近三成；多家公募在把握科技主线同时加快布局红利等低波动产品，产品矩阵"攻守兼备"。<br>
          <b>对基金行业影响：</b>发行结构再平衡→腾安货架应从单一科技扩至"科技+红利+固收"组合，匹配再平衡下的客户配置需求。
        </div>
        <div class="card-footer">
          <a href="https://gu.qq.com/resources/shy/news/detail-v2/index.html?t=1#/index?_tentrees_trans=0&id=SN20260716015132a6d61334" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯证券·上海证券报</span></a>
          <span class="impact-tag medium">发行再平衡：中</span>
        </div>
      </div>

      <!-- S1 Card NEW: 央行万亿投放+利率下行·居民资金向权益ETF分流 (07-11) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 央行万亿中长期资金投放+存款利率下行·居民闲钱向权益/ETF分流</div>
          <div class="card-meta">
            <span class="priority-tag normal">建议了解</span>
            <span class="date-tag">07-11</span>
          </div>
        </div>
        <div class="card-body">
          <b>流动性宽松：</b>央行7月初完成万亿级中长期资金投放，对冲缴税与解禁压力；银行存款利率持续下行、五年期大额存单重启，稳健理财收益走低。<br>
          <b>资金迁徙：</b>在"资产荒+低利率"环境下，居民闲钱持续向权益市场与ETF分流，为公募权益产品与指数化配置提供增量资金来源。<br>
          <b>对基金行业影响：</b>增量资金入场→腾安可顺势加大权益/ETF货架与投教，承接居民资产再配置需求。
        </div>
        <div class="card-footer">
          <a href="https://caifuhao.eastmoney.com/news/20260711073255117872680" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">东方财富</span></a>
          <span class="impact-tag low">资金面：中</span>
        </div>
      </div>
      <!-- S1 Card NEW: 券商密集回购增持稳市·上限12.6亿 (07-23) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 券商密集回购增持稳市·金额上限12.6亿·提振A股信心</div>
          <div class="card-meta">
            <span class="priority-tag important">重要关注</span>
            <span class="date-tag">07-23</span>
          </div>
        </div>
        <div class="card-body">
          <b>真金白银：</b>7月22日晚间，长江证券、兴业证券接连公告回购/增持计划（长江董事长提议1亿—2亿回购、福建投资拟6个月内增持3000万—6000万）；叠加华安、国联民生、中泰、红塔、国金等多家券商集中方案，行业回购增持上限达<b>12.6亿元</b>。<br>
          <b>政策信号：</b>监管层持续放宽券商业务范围（财达证券同期获准北交所股票做市资格），市场活跃度有望提升，释放积极"政策底"信号。<br>
          <b>对基金行业影响：</b>券商自救维稳提振非银金融配置价值、修复市场情绪→腾安可借势引导客户关注市场底部布局机会。
        </div>
        <div class="card-footer">
          <a href="https://new.qq.com/rain/a/20260723A04H1W00?refer=cp_1009" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻</span></a>
          <span class="impact-tag medium">市场维稳：中</span>
        </div>
      </div>
    </div>
'''
replace_block(S1_START, S1_END, NEW_S1, "S1")

# ============ 7. S6 市场行情 (07-23 盘中) ============
S6_START = '          <div class="card p3">'
S6_END = '  </div>\n<!-- ============ Section 7: 关键时间线 ============ -->'
NEW_S6 = '''          <div class="card p3">
        <div class="card-top">
          <div class="card-title">2026年7月23日（周四·盘中）·A股集体高开震荡·沪指+0.20%·创业板领涨+1.40%</div>
          <div class="card-meta">
            <span class="priority-tag fyi">知悉即可</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>📈 A股07-23盘中（集体高开·震荡）：</b><br>
              ▪ 沪指 <b>+0.20%</b>（3874.90）·深成指 <b>+0.39%</b>（14116.02）<br>
              ▪ 创业板指 <b>+1.40%</b>（3616.76）·能源金属/贵金属/半导体/通信设备领涨<br>
              ▪ 白酒/煤炭/中药跌幅居前；算力硬件、锂矿活跃，硬科技主线延续
            </div>
            <div>
              <b>📉 港股07-22收盘（跌）：</b><br>
              ▪ 恒指 <b>-0.95%</b>（24892.66）·恒生科技 <b>-3.04%</b>（4668.23）·国企指数-1.31%<br>
              <b>📉 美股07-22收盘（全线下跌）：</b>道指-0.01%（52218.58）·标普-0.14%（7498.96）·纳指-0.57%（25690.90）；前一交易日费城半导体+5.21%后科技分化
            </div>
          </div>
          <div style="margin-top:12px;font-size:12px;color:var(--gray-500);">
            💡 焦点：A股集体高开震荡、创业板领涨，二季报收官后科技主线延续；二季度公募盈利1.94万亿、规模38.31万亿再创新高；公募重仓"6进6出"大洗牌、科技占前20大重仓八成。
          </div>
        </div>
          <div class="card-footer">
            <span class="source-tag">WebSearch·2026-07-23（周四盘中）</span>
            <span class="source-tag">数据来源：中新经纬/人民财讯/新华社/港交所</span>
          </div>
      </div>
'''
replace_block(S6_START, S6_END, NEW_S6, "S6")

# ============ 8. S7: remove 07-08 entry, add 07-23 entry ============
# 8a. remove expired 07-08 timeline item
S7_OLD_ITEM = ('      <!-- 07-08 时间线条目 (NEW) -->\n'
               '      <div class="timeline-item">\n'
               '        <div class="timeline-dot red"></div>\n'
               '        <div class="timeline-date">2026-07-08</div>\n'
               '        <div class="timeline-title">自由现金流产品年内规模+42.79%至571.77亿(107只)</div>\n'
               '      </div>\n')
assert S7_OLD_ITEM in s, "07-08 timeline item not found"
s = s.replace(S7_OLD_ITEM, "", 1)
print("[S7-rm] global after remove 07-08:", *gbal(s))
assert_eq(*gbal(s), "S7-rm global")

# 8b. insert 07-23 item at top (before 07-22 item)
S7_INSERT_ANCHOR = '      <!-- 07-22 时间线条目 (NEW) -->'
S7_NEW_ITEM = ('      <!-- 07-23 时间线条目 (NEW) -->\n'
               '      <div class="timeline-item">\n'
               '        <div class="timeline-dot red"></div>\n'
               '        <div class="timeline-date">2026-07-23</div>\n'
               '        <div class="timeline-title">二季度公募盈利1.94万亿·座次出炉万亿俱乐部瘦身至10家</div>\n'
               '      </div>\n\n')
assert S7_INSERT_ANCHOR in s
s = s.replace(S7_INSERT_ANCHOR, S7_NEW_ITEM + S7_INSERT_ANCHOR, 1)
print("[S7-add] global after add 07-23:", *gbal(s))
assert_eq(*gbal(s), "S7-add global")

# ---- final div balance ----
fo, fc = gbal(s)
print("FINAL div balance:", fo, fc)
assert_eq(fo, fc, "FINAL")

# ---- content sanity checks ----
checks = {
    "no S8 section": "Section 8" not in s and "待办跟踪" not in s and "腾安行动清单" not in s,
    "S0 all 07-23": s.count('07-23') >= 4,
    "no 07-22 in S0 cards": "二季度公募规模近40万亿 (T+0 07-22" not in s,
    "07-08 fully removed": "2026-07-08" not in s,
    "07-23 timeline present": "2026-07-23" in s,
    "timeline-desc absent": "timeline-desc" not in s,
}
for k, v in checks.items():
    print(("OK  " if v else "FAIL") + " " + k)
    if not v:
        raise SystemExit("CONTENT CHECK FAIL: " + k)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("WROTE", PATH, "global balance", fo, fc)
