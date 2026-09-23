# -*- coding: utf-8 -*-
"""基金看板每日更新 2026-09-23（周三）
T-14 边界 = 09-09
更新范围：marker/fingerprint → header badge → Stats Bar 沪指卡 → S0 四卡 → S6 行情 → S7 时间线
本日无 P0 → S0 无 action-box；预期 div 零漂移（244 → 244）
"""
import re
from datetime import date, timedelta

P = 'index.html'
src = open(P, encoding='utf-8').read()
orig_open = len(re.findall(r'<div[ >]', src))
orig_close = src.count('</div>')
TODAY = date.today()
CUT = (TODAY - timedelta(days=14)).strftime('%m-%d')


def dr(tag):
    o = len(re.findall(r'<div[ >]', src))
    c = src.count('</div>')
    print(f'  [dr] {tag}: open={o} close={c} (do={o-orig_open:+d} dc={c-orig_close:+d})')
    return o, c


print(f'baseline open={orig_open} close={orig_close} CUT={CUT}')

# ============ Step 1: marker + fingerprint（必须第一步） ============
src = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
             f'<!-- daily-update: {TODAY} -->', src)
src = re.sub(r'<meta name="content-fingerprint" content="[^"]*">',
             '<meta name="content-fingerprint" content="科技主题|兴银基金|ETF资金|公募秋招">', src)
assert f'<!-- daily-update: {TODAY} -->' in src
assert '科技主题|兴银基金|ETF资金\|公募秋招'.replace('\\', '') in src
dr('step1 marker+fp')

# ============ Step 2: header 数据区间 ============
hi = TODAY.strftime('%Y.%m.%d')
lo = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')
src = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
             f'📅 数据区间：{lo} — {hi}（每日更新）', src)
assert f'📅 数据区间：{lo} — {hi}（每日更新）' in src
dr('step2 badge')

# ============ Step 3: Stats Bar 沪指卡 ============
SB_OLD = '''      <div class="stat-number">3949.91</div>
      <div class="stat-label">沪指9-21收盘·涨0.97%·沪深北三市成交2.05万亿·缩量448亿</div>
      <div class="stat-change up">▲ 医药板块领涨·4536股上涨105只涨停</div>'''
SB_NEW = '''      <div class="stat-number">3952.13</div>
      <div class="stat-label">沪指9-22收盘·涨0.06%·沪深北三市成交2.15万亿·放量1055亿</div>
      <div class="stat-change up">▲ AI应用端全天强势·2374股上涨64只涨停</div>'''
assert src.count(SB_OLD) == 1, f'stats anchor {src.count(SB_OLD)}'
src = src.replace(SB_OLD, SB_NEW)
i = src.find('<div class="stats-bar">')
sb = src[i:i + 1800]
assert '3952.13' in sb and '3949.91' not in sb
dr('step3 stats')

# ============ Step 4: S0 四卡 ============
C1 = '''<!-- S0 Card 1 (09-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 科技主题基金密集“上新”·9月申报196只科技主题占37只·267只绩优主动科技基金常态化限购</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-23</span>
          </div>
        </div>
        <div class="card-body">
          证券日报记者彭衍菘9月23日报道：Wind数据显示，截至9月22日，9月以来公募行业共申报<b>196只</b>基金，其中科技主题基金达<b>37只</b>、占比接近两成，且以被动指数型产品为主。仅9月16日至18日，易方达、华夏、华泰柏瑞、招商、博时、天弘、华宝等<b>7家</b>公募机构集中上报创业板算力基础设施ETF及其联接基金；科创板芯片设计、中证芯片产业、中证全指软件、通信设备、科创创业人工智能等细分方向也迎来多只指数产品申报。<br>
          <b>一张一弛：</b>与被动产品集中扩容形成鲜明对照的是，绩优主动科技基金普遍维持常态化大额申购限制。以单日大额申购上限不超过1000万元为口径，9月1日主动科技方向基金中共有<b>267只</b>实施限购，截至9月22日仍为267只；若以100万元为限，9月初为162只、9月22日为161只，数量基本持平，并未出现行情升温后临时集中收紧的情况。<br>
          <b>业绩与限购：</b>254只年内净值增长率超过50%的主动科技基金中，有18只设置100万元以下单日申购上限、占比7.1%；611只年内净值增长率超30%的产品中30只限购、占比4.9%。东方人工智能主题混合年内净值增长率<b>112.48%</b>，单日单账户申购上限10万元；易方达信息产业混合A年内<b>52.67%</b>，单日申购上限仅1万元。<br>
          <b>对腾安启示：</b>科技赛道呈现“指数工具承接增量、主动产品锁规模保收益”的分工——货架上被动科技产品可继续按算力/芯片/软件/通信细分标签铺开，主动科技产品则应把“限购”从负面体验改写为“策略容量保护”卖点，在详情页明示限购阈值与原因，避免用户把限购误读为流动性风险。
        </div>
        <div class="card-footer">
          <a href="http://www.zqrb.cn/fund/jijindongtai/2026-09-23/A1790078811484.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">证券日报·09-23</span></a>
          <a href="https://big5.china.com.cn/gate/big5/finance.china.com.cn/money/fund/20260923/6324935.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国网财经·09-23</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>'''

C2 = '''<!-- S0 Card 2 (09-23 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 兴银基金换帅董晓亮任董事长·年内公募高管变更已达290人次·董事长54人次涉29家</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-23</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报记者朱妍、每日经济新闻记者李蕾9月23日报道：9月23日兴银基金发布高级管理人员变更公告，自9月22日起黄德良不再兼任董事长，<b>董晓亮</b>新任董事长。黄德良现任福建省金融投资公司党委委员、副总经理，兼任兴银基金控股股东华福证券党委书记、董事长，2025年8月起任兴银基金董事长；董晓亮从业近30年，先后在国贸期货、兴业证券、海通期货任职，2013年作为核心成员参与圆信永丰基金筹建，后任世纪证券总经理、太平基金副总经理，现任华福证券首席战略官。Choice数据显示，截至2026年6月30日兴银基金公募管理规模<b>1455.96亿元</b>，较去年年中增长超300亿元，公募产品超70只，近五年固收—偏债类投资实力排名行业第三。<br>
          <b>行业背景：</b>Wind数据显示，2026年以来截至9月18日，全行业公募基金高管变更累计已达<b>290人次</b>——董事长岗位变动54人次、涉及29家公司，总经理76人次、涉及41家公司，副总经理87人次、督察长67人次、首席信息官35人次；单月变动高点出现在7月（44人次）与3月（42人次），6月与8月均达39人次。2025年全年发生高管变更的基金公司达129家、涉及371人。<br>
          <b>对腾安启示：</b>高管高频更替直接影响产品策略连续性与代销合作稳定性——对换帅机构（尤其董事长/总经理同调的）应触发一次“产品策略复核”：确认在售产品的投资范围、费率优惠与持续营销承诺是否延续，并在机构主页同步更新管理层信息，避免门店话术仍引用已离任高管的公开观点。
        </div>
        <div class="card-footer">
          <a href="https://www.cnstock.com/commonDetail/794399" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">上海证券报·09-23</span></a>
          <a href="https://www.nbd.com.cn/articles/2026-09-23/4589502.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·09-23</span></a>
          <a href="https://news.qq.com/rain/a/20260923A03YOJ00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·09-23</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>'''

C3 = '''<!-- S0 Card 3 (09-23 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 ETF资金流向·信用债指数ETF单日净流入96.69亿·科创债ETF嘉实32.92亿居全市场首位</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-23</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇9月23日复盘（新浪财经转载）：9月22日ETF市场资金面整体呈净流入格局，九大类ETF中五类流入、四类流出，整体净流入约<b>75.21亿元</b>。<br>
          <b>信用债成绝对主线：</b>信用债指数ETF单日净流入<b>96.69亿元</b>，接近百亿元量级、占当日全部净流入的七成以上；4只科创债ETF合计净流入约<b>65.73亿元</b>，科创债ETF嘉实以32.92亿元居全市场净流入首位（最新规模412.06亿元）；信用债ETF海富通净流入8.76亿元、公司债ETF易方达净流入3.72亿元、30年国债ETF博时净流入4.51亿元。<br>
          <b>结构分化：</b>宽基指数ETF净流入25.55亿元，其中沪深300方向5只合计约26.94亿元，中证500与中证1000方向3只合计约22.66亿元；但两只科创50ETF合计净流出18.67亿元，科创50ETF华夏净流出16.08亿元居净流出榜第二。货币ETF大类净流出47.33亿元，其中银华日利ETF单只净流出44.70亿元居全市场净流出首位。行业主题ETF净流入3.54亿元，科创半导体ETF华夏净流入16.20亿元居第二。<br>
          <b>对腾安启示：</b>资金正从货币类向信用债/科创债方向搬家，债基ETF是当下最确定的承接品种——货架上可把科创债、信用债ETF单列为“低波动配置”专区并标注最新规模与年内净流入；同时需在货币ETF（如银华日利）页面前置提示“资金流出≠风险事件”，避免用户把单日大额赎回误读为产品异常。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/stock/bxjj/2026-09-23/doc-inisunsf6248610.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·新浪财经·09-23</span></a>
          <a href="https://www.gelonghui.com/live/2684086" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·09-23</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>'''

C4 = '''<!-- S0 Card 4 (09-23 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 公募秋招掀起AI人才争夺战·易方达设AI人才专项·多只持有期FOF接连申报</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-23</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻记者肖芮冬9月23日报道：2027届秋季校园招聘季拉开帷幕，公募行业对人工智能人才的争夺热度较高。多家头部基金公司通过设立AI人才专项、金融科技专场或AI方向岗位等方式，系统性扩大AI人才招聘规模，岗位设置涉及底层算法研究、大模型应用、智能体开发及平台架构。易方达基金在2027届校招中单独设立<b>“AI人才专项”</b>，面向应届生招聘AI工程师、AI研究员及AI应用岗；南方基金开启2027届金融科技专场校园招聘，涉及AI框架工程师、AI评测工程师、AI应用开发工程师、AI数据工程师、AI产品经理等岗位。<br>
          <b>FOF申报同步推进：</b>证监会最新公布的行政许可信息显示，9月18日华商基金申报的华商汇启多元配置3个月持有期混合型FOF、华安基金申报的华安盈茂多资产6个月持有期混合型发起式FOF获得材料接收；9月14日嘉实基金、兴证全球基金也分别上报持有期FOF产品。本轮上报的FOF均设置3个月或6个月最短持有期，且名称中突出“多资产”“多元配置”属性。<br>
          <b>对腾安启示：</b>头部公募把AI岗位从“科技部门”单列为“专项赛道”，意味着智能体与AI投顾能力将在2027年进入密集兑现阶段——腾安侧应提前锁定自研与外部采购的能力边界，避免届时被动跟随；FOF侧“多资产+短持有期”的组合设计正成为主流，货架可考虑按“最短持有期”而非仅按风险等级做筛选维度。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20260923A03C3T00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·每日经济新闻·09-23</span></a>
          <span class="impact-tag low">影响：中</span>
        </div>
      </div>'''

S0_NEW = '\n'.join([C1, C2, C3, C4])
a0 = src.find('<!-- S0 Card 1')
a1 = src.find('    </div>\n  </div>\n<!-- ============ Section 1')
assert a0 > 0 and a1 > a0, 'S0 anchors'
assert src.count('<!-- S0 Card 1') == 1
seg_old = src[a0:a1]
print('  S0 old cards:', seg_old.count('<!-- S0 Card'))
src = src[:a0] + S0_NEW + src[a1:]

# 4b: section-context
CT_OLD = '<span class="section-context">9月22日 · 4条今日要闻</span>'
CT_NEW = '<span class="section-context">9月23日 · 4条今日要闻</span>'
assert src.count(CT_OLD) == 1, f'context {src.count(CT_OLD)}'
src = src.replace(CT_OLD, CT_NEW)

s0 = src[src.find('Section 0'):src.find('Section 1')]
assert '<span class="section-title">今日焦点</span>' in s0
assert s0.count('<div class="card p') == 4, f'S0 cards {s0.count("<div class=""card p")}'
assert s0.count('action-box') == 0, 'S0 应无 action-box'
ds = re.findall(r'date-tag">(\d{2})-(\d{2})<', s0)
assert ds == [('09', '23')] * 4, f'S0 dates {ds}'
assert s0.count('<a href=') == 8, f'S0 links {s0.count("<a href=")}'
for u in re.findall(r'href="(https?://[^"]+)"', s0):
    for bad in ('stcn.com', 'cls.cn', 'toutiao', '21jingji', 'yicai.com', '163.com/dy', 'so.html5.qq.com'):
        assert bad not in u, f'S0 黑名单 {u}'
dr('step4 S0')

# ============ Step 5: S6 行情（09-22 收盘） ============
S6_NEW = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-22）·沪指3952.13 +0.06%·沪深北三市成交2.15万亿放量1055亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-22</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-22收盘·冲高回落）</b><br>
              上证指数 <b>3952.13</b> <span style="color:#dc2626;">+0.06%</span><br>
              深证成指 <b>13723.74</b> <span style="color:#52c41a;">-0.05%</span><br>
              创业板指 <b>3399.93</b> <span style="color:#dc2626;">+0.01%</span><br>
              沪深300 <b>4544.59</b> <span style="color:#dc2626;">+0.11%</span><br>
              科创综指 <b>1962.84</b> <span style="color:#dc2626;">+0.30%</span><br>
              科创50 <b>1665.04</b> <span style="color:#dc2626;">+0.46%</span><br>
              北证50 <b>1046.80</b> <span style="color:#52c41a;">-1.08%</span><br>
              沪深北三市成交 <b>2.15万亿</b>·较上日放量1055亿<br>
              2374只上涨·64只涨停；3030只下跌·5只跌停
            </div>
            <div>
              <b>港股与美股（09-22收盘）</b><br>
              恒生指数 <b>25087.75</b> <span style="color:#dc2626;">+0.18%</span><br>
              恒生科技 <b>4438.21</b> <span style="color:#dc2626;">+0.34%</span><br>
              国企指数 <b>8362.60</b> <span style="color:#dc2626;">+0.28%</span><br>
              道琼斯 <b>51863.69</b> <span style="color:#52c41a;">-0.36%</span><br>
              纳斯达克 <b>27244.28</b> <span style="color:#dc2626;">+0.45%</span><br>
              标普500 <b>7764.64</b> <span style="color:#52c41a;">-0.06点基本收平</span><br>
              布伦特原油99.25美元 <span style="color:#52c41a;">-1.09%</span>·COMEX黄金4396.20美元 <span style="color:#dc2626;">+0.28%</span>·美债10年期升至4.963%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>AI应用端全天强势、指数冲高回落——盘中深证成指一度涨逾1%，创业板指、科创综指均一度涨逾2%，尾盘集体下挫。申万一级行业中传媒涨<b>1.79%</b>、计算机涨<b>1.41%</b>、家用电器涨<b>1.24%</b>领涨，煤炭、综合行业均涨逾1%；交通运输跌1.17%、钢铁跌0.95%、建筑材料跌0.92%跌幅居前。AI办公、虚拟人、网络安全板块活跃，南威软件2连板、泛微网络与引力传媒涨停；六氟化钨、航运、超硬材料调整。全市场2374只个股上涨、64只涨停，3030只下跌。成交端沪深北三市2.15万亿元，较上一交易日<b>增加1055亿元</b>；9月7日—17日曾连续9个交易日低于2万亿元，9月18日以来已连续3个交易日超2万亿元。资金面谨慎，沪深两市主力资金净流出超<b>110亿元</b>；截至9月21日，9月以来A股融资余额减少超120亿元。<br>
              <b>港股与海外：</b>恒指涨0.18%报25087.75点，主板成交2492.14亿港元，腾讯控股涨<b>5.02%</b>报451.6港元；南向资金净买入超<b>126亿港元</b>，为8月19日以来最大单日净买额，9月7日以来已连续12个交易日净买入、累计超488亿港元。美股9月22日涨跌不一，纳指涨0.45%<b>续创收盘历史新高</b>（盘中最高27288.79点亦创新高），道指跌0.36%，标普500微跌0.06点基本收平；费城半导体指数涨<b>2.06%</b>报12689.82点，美光科技涨5.00%；头部银行股集体下挫，富国银行跌3.92%、摩根大通跌3.40%。美伊冲突缓和预期带动油价回落，布伦特原油跌至99.25美元；美债收益率集体上行，10年期涨1BP报<b>4.963%</b>。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：2026-09-22收盘</span>
          <span class="source-tag">数据来源：上海证券报/中国证券网、中国证券报、新华社、中新经纬、新华财经（09-22—09-23）</span>
        </div>
      </div>'''
b0 = src.find('            <div class="card p3">', src.find('Section 6'))
b1 = src.find('      </div>  </div>\n<!-- ============ Section 7')
assert b0 > 0 and b1 > b0, 'S6 anchors'
src = src[:b0] + S6_NEW + src[b1 + len('      </div>'):]
s6 = src[src.find('Section 6'):src.find('Section 7')]
assert '3952.13' in s6 and ('09-22') in s6
assert re.findall(r'date-tag">(\d{2})-(\d{2})<', s6) == [('09', '22')]
dr('step5 S6')

# ============ Step 6: S7 时间线 12 条 ============
ITEMS = [
    ('2026-09-23', '公募秋季策略会密集举办'),
    ('2026-09-22', '南向资金净买入超126亿港元'),
    ('2026-09-22', 'A股冲高回落成交2.15万亿'),
    ('2026-09-22', '建信金融科技ETF延募'),
    ('2026-09-22', '纳指涨0.45%创收盘新高'),
    ('2026-09-21', '本周16只新发基金启动'),
    ('2026-09-21', '113家公募上周调研406次'),
    ('2026-09-21', '上银基金姚秦出任总经理'),
    ('2026-09-20', '刘彦春卸任景顺长城副总'),
    ('2026-09-20', '3只REIT获证监会注册'),
    ('2026-09-20', '年内公募打新获配338亿'),
    ('2026-09-18', '贝莱德基金获批QDII资格'),
]
assert len(ITEMS) == 12
for d, t in ITEMS:
    assert len(t) <= 25, f'title too long: {t}'
    assert d[5:7] >= '09' and d >= f'2026-{CUT}', f'S7 out of window {d}'
TPL = ('      <div class="timeline-item">\n'
       '        <div class="timeline-dot blue"></div>\n'
       '        <div class="timeline-date">{d}</div>\n'
       '        <div class="timeline-title">{t}</div>\n'
       '      </div>')
new_items = '\n'.join(TPL.format(d=d, t=t) for d, t in ITEMS)
c0 = src.find('      <div class="timeline-item">')
n_old = src.count('      <div class="timeline-item">')
assert n_old == 12, f'S7 old items {n_old}'
c1 = src.find('\n    </div>\n\n  </div>\n\n</div>', c0)
assert c1 > c0, 'S7 end anchor'
src = src[:c0] + new_items + src[c1:]
s7 = src[src.find('Section 7'):]
assert s7.count('<div class="timeline-item">') == 12
assert 'timeline-desc' not in s7
assert re.findall(r'timeline-date">([^<]+)<', s7) == [d for d, _ in ITEMS]
dr('step6 S7')

# ============ Phase 1 全量断言 ============
o, c = len(re.findall(r'<div[ >]', src)), src.count('</div>')
assert o == c, f'div 失衡 {o}/{c}'
assert (o - orig_open) == 0, f'div 漂移 {o-orig_open} (预期 0)'
assert src.count('</div>>') == 0, 'stray </div>>'
assert 'Section 8' not in src and '待办跟踪' not in src and '腾安行动清单' not in src
assert 'U+FFFD'.replace('U+FFFD', '\ufffd') not in src
assert src.count('<!-- daily-update:') == 1
assert src.count('<meta name="content-fingerprint"') == 1
assert src.count('class="stats-bar"') == 1
assert src.count('section-title-group') >= 1
# 全文件 date-tag T-14
all_dt = re.findall(r'<span class="date-tag">(\d{2})-(\d{2})</span>', src)
bad = [x for x in all_dt if f'{x[0]}-{x[1]}' < CUT]
assert not bad, f'超 T-14 卡：{bad}'
# 全文件黑名单
for u in re.findall(r'href="(https?://[^"]+)"', src):
    for b in ('stcn.com', 'cls.cn', 'toutiao', '21jingji', 'yicai.com',
              'so.html5.qq.com', '163.com/dy', 'guba.eastmoney.com'):
        assert b not in u, f'黑名单链接 {u}'
print('Phase1 assertions OK')

open(P, 'w', encoding='utf-8', newline='') .write(src)
print(f'WROTE {P}  open={o} close={c} drift={o-orig_open:+d}')
