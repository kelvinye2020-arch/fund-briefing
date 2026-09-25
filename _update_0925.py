#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""daily-update 2026-09-25: 补 09-24 + 09-25 两日内容（09-24 缺失）"""
import re, sys
from datetime import date, timedelta

P = 'index.html'
h = open(P, encoding='utf-8').read()
orig_open = len(re.findall(r'<div\b', h))
orig_close = len(re.findall(r'</div>', h))
print(f'[init] div open={orig_open} close={orig_close}')

def diag(step):
    o = len(re.findall(r'<div\b', h)); c = len(re.findall(r'</div>', h))
    print(f'[{step}] open={o} close={c} drift_o={o-orig_open} drift_c={c-orig_close}')
    return o, c

def rep(old, new, step, cnt=1):
    global h
    n = h.count(old)
    assert n == cnt, f'{step}: expected {cnt} got {n} for {old[:60]!r}'
    h = h.replace(old, new, cnt)
    diag(step)

TODAY = date.today()
upper = TODAY.strftime('%Y.%m.%d')
lower = (TODAY - timedelta(days=14)).strftime('%Y.%m.%d')

# ---------- 1. marker + header badge ----------
h = re.sub(r'<!-- daily-update: \d{4}-\d{2}-\d{2} -->',
           f'<!-- daily-update: {TODAY} -->', h, count=1)
h = re.sub(r'📅 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
           f'📅 数据区间：{lower} — {upper}（每日更新）', h, count=1)
diag('01 marker/badge')

# ---------- 2. Stats Bar 沪指卡 -> 09-24 收盘 ----------
rep('''      <div class="stat-number">3952.13</div>
      <div class="stat-label">沪指9-22收盘·涨0.06%·沪深北三市成交2.15万亿·放量1055亿</div>
      <div class="stat-change up">▲ AI应用端全天强势·2374股上涨64只涨停</div>''',
    '''      <div class="stat-number">3888.37</div>
      <div class="stat-label">沪指9-24收盘·跌1.22%·沪深北三市成交1.67万亿·缩量1140亿</div>
      <div class="stat-change down">▼ 失守3900点·超4300股下跌·贵金属有色领跌</div>''',
    '02 stats')

# ---------- 3. S0 context ----------
rep('<span class="section-context">9月23日 · 4条今日要闻</span>',
    '<span class="section-context">9月25日 · 4条今日要闻</span>', '03 s0-context')

# ---------- 4. S0 四卡全换 ----------
S0 = '''            <!-- S0 Card 1 (09-25 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 德邦基金总经理张騄离任·董事长尉迟平代任·年内公募高管变更268人涉104家</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-25</span>
          </div>
        </div>
        <div class="card-body">
          中国基金报记者曹雯璟9月25日报道：9月25日德邦基金发布高级管理人员变更公告，经公司董事会审议通过，公司总经理<b>张騄</b>、总经理助理<b>张瑾</b>因工作调动离任，岗位说明为“另有任用”，离任日期均为9月24日；由董事长<b>尉迟平</b>女士代为履行总经理职责。尉迟平于2026年6月正式出任德邦基金董事长，本次由董事长代行总经理职责属行业治理程序中的常规过渡安排。Wind数据显示，截至2026年6月30日德邦基金在管公募产品规模<b>825.18亿元</b>，权益类258.75亿元、占比31.36%；国泰海通数据显示其权益类近3年、近5年绝对收益率分别为288.37%、223.64%，在148家、140家参评基金公司中均排名第2位。<br>
          <b>行业背景：</b>Wind数据显示，截至9月24日，年内公募行业高管变更总人数达<b>268人</b>、涉及<b>104家</b>基金公司，其中28家变更董事长、36家变更总经理；年内变动2人次及以上的公司多集中在中小机构，淳厚基金以12人次居行业首位，万家、安联、东财、国联安等均在5人次左右；富国、建信等万亿级机构年内亦完成董事长更替。业内分析认为驱动因素主要来自到龄退休、股东股权更迭、费率改革与竞争加剧、任期届满四类。<br>
          <b>股东侧同步变动：</b>9月25日证监会批文显示，已核准山东省财欣投资有限公司成为德邦证券主要股东，对其受让德邦证券4.2068亿股股份（占股份总数<b>10%</b>）无异议，山东省财政厅为受让方实际控制人；德邦证券持有德邦基金80%股权。此外德邦基金今年2月曾因违规联合互联网大V营销收到上海证监局罚单、责令三个月内改正并暂停受理公募基金产品注册申请，公司称截至报告期末已完成整改，新发产品德邦数字经济混合已定档10月26日开始募集。<br>
          <b>对腾安启示：</b>高管变更常态化已延伸到股东层面——对发生“董事长代任总经理”或控股股东股权变动的机构，应触发一次在售产品复核（投资范围、费率优惠、持续营销承诺是否延续），并在机构主页同步更新管理层与股东信息；对完成整改、恢复产品注册的机构（如德邦），需重新评估其新产品上架排期与合规提示语的撤下时点。
        </div>
        <div class="card-footer">
          <a href="https://www.chnfund.com/article/ARdfb5a452-56c6-4825-2766-3a23e8558c2b" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金报·09-25</span></a>
          <a href="https://news.qq.com/rain/a/20260925A045CS00" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·09-25</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
<!-- S0 Card 2 (09-24 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 新发基金密集“加时”·9月47只延募42只提前结募·被动指数型成延募主力</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-24</span>
          </div>
        </div>
        <div class="card-body">
          新浪财经9月24日报道（中工网同步刊发）：Wind数据显示，截至9月24日，9月以来累计<b>89只</b>新发基金发布募集期调整公告，其中延长募集期<b>47只</b>、提前结束募集<b>42只</b>，分化之剧烈可见一斑。9月24日当天，南方创业板ETF、东方丰稳多元配置三个月持有期FOF、交银施罗德汇享多资产六个月持有期FOF、东财资源智选4只基金同日公告延长募集时间。<br>
          <b>延募结构：</b>47只延募基金中被动指数型产品超过<b>20只</b>，涵盖多赛道ETF及指数联接产品，另有增强指数型、混合型FOF、偏股混合型等；赛道覆盖创业板金融科技、大数据产业、航天航空，粮食产业、有色金属等传统周期主题更出现多只产品扎堆延募。幅度方面，兴业上证科创板人工智能ETF将募集截止日从9月15日大幅延后至10月30日、延期超<b>45天</b>，为本轮延募幅度最大；博时中证机器人ETF三周内两次按下延迟键、累计延期超40天至10月14日；东兴增利A延期35天，中银中证工业有色金属主题ETF联接延期31天。中金基金、汇添富基金、博时基金、宏利基金、景顺长城基金、银华基金等均有2只及以上产品延募。<br>
          <b>成因与效率：</b>晨星中国基金研究中心高级分析师李一鸣指出，延募数量攀升是投资者风险偏好下行、市场结构性分化加剧、渠道增量资金收缩等因素共同作用的结果；8月新基金募集规模仅<b>564.83亿元</b>，环比下降38.85%、同比下降52.84%。另据Wind，截至9月22日年内已有288只股票ETF设立、合计募资937.52亿元，单只平均3.26亿元，较去年同期的5.75亿元下滑超<b>43%</b>。<br>
          <b>对腾安启示：</b>延募与提前结募并存意味着“赛道热度”已取代“品类热度”成为首发成败的决定变量——货架排期应从“按获批顺序铺”改为“按赛道拥挤度择优”，对同一细分主题扎堆发行的ETF（粮食、有色、机器人）做发行窗口去重；同时把“延长募集期”从负面标签改写为中性状态说明，避免用户误读为产品异常。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/money/fund/fundzmt/2026-09-24/doc-inisxhnz8259158.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-24</span></a>
          <a href="https://www.workercn.cn/c/2026-09-24/8901853.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中工网·09-24</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
<!-- S0 Card 3 (09-25 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 首批18只主动ETF获批在即·年内新发基金8073亿份·平均6.24亿创近年低位</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-25</span>
          </div>
        </div>
        <div class="card-body">
          同花顺财经9月25日“每周回顾”梳理（援引第一财经9月21日报道）：首批<b>18只主动ETF</b>已进入获批关键窗口，有基金公司人士称“最快下周见分晓”，若批文落地，国庆假期后即可启动发售。这批产品于今年7月中旬上报，目前多家试点公司已在投研、系统、做市、风控等环节完成全体系准备，并已接受监管专项验收。<br>
          <b>真正的考验在上市之后：</b>PCF（申购赎回清单）日度披露让策略与持仓高度透明，既带来被量化机构“跟风”“抢跑”的风险，又因允许盘中动态调仓，易造成当日实际持仓与PCF清单不一致，引发IOPV计算偏差与二级市场折溢价异常走阔。为此多家公司建立跨条线协同机制、双部门双岗位交叉复核，并针对做市商设置专人对接与差异化报价。<br>
          <b>发行大盘：</b>截至2026年9月21日，年内全市场新成立基金<b>1293只</b>、合计发行总份额<b>8073.31亿元</b>，平均发行份额<b>6.24亿元</b>，呈现数量走高、平均规模走低的特征——今年新发数量已超过2023、2024年全年，相当于2025年的85.69%，但总发行规模仅相当于近年全年的70%左右，平均发行规模创近年低位。结构上指数基金成为机构布局赛道的核心抓手，债券型、混合型、FOF更受资金追捧，中小基金“小额多批”成为常态。<br>
          <b>本周新发：</b>9月21日—25日全市场新发基金共16只，其中债券型7只（占比43.75%，全部为63个月封闭运作的长期封闭债基，涉及7家基金公司）、被动指数型4只、REITs 2只，增强指数型、偏股混合型、FOF各1只；永赢、易方达分别发行跟踪中证科创创业人工智能指数的ETF联接产品，中金基金本周发行3只产品（含中金杭州安居宁巢REIT、中金菜鸟REIT）。<br>
          <b>对腾安启示：</b>主动ETF是介于主动与被动之间的新品类，货架需提前设计独立的筛选与展示口径（跟踪误差、PCF披露频率、折溢价监控），不能简单归入指数区或主动区；同时“数量新高、单只规模新低”说明首发资源应集中于少数高确定性赛道，而非追求全品类覆盖。
        </div>
        <div class="card-footer">
          <a href="https://m.10jqka.com.cn/20260925/c680282116.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·09-25</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
<!-- S0 Card 4 (09-24 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">🔵 ETF资金流向·沪深300ETF单日净流入43.78亿·信用债指数ETF净流入64.57亿</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">09-24</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇9月24日复盘（新浪财经转载）：9月23日ETF市场资金面整体呈净流入格局，九大类ETF中四类流入、五类流出，整体净流入约<b>72.01亿元</b>。<br>
          <b>信用债与宽基双主线：</b>信用债指数ETF净流入<b>64.57亿元</b>、宽基指数ETF净流入<b>63.40亿元</b>，两大类合计约127.97亿元，占当日全部净流入的九成以上；净流入TOP20榜单中债券类ETF占据11席、合计约52.92亿元，宽基品种占据8席、合计约56.01亿元。<br>
          <b>沪深300集体获增持：</b>5只沪深300ETF集体上榜并包揽净流入榜单前两位，合计净流入约<b>43.78亿元</b>；沪深300ETF易方达以15.63亿元居全市场首位，沪深300ETF华泰柏瑞净流入12.30亿元次之。科创债品种获集中配置，6只科创债ETF集体上榜、合计约33.35亿元，科创债ETF易方达以8.31亿元居债券类首位。<br>
          <b>流出与中期视角：</b>货币ETF大类净流出30.31亿元，银华日利ETF以29.46亿元净流出居全市场首位，与华宝添益ETF合计净流出约32.51亿元；宽基内部品种分化突出，上证50、科创50、A500、中证1000方向均有个券流出。近20日维度，科创债ETF嘉实净流入<b>107.44亿元</b>居全周期首位，华宝添益ETF净流入97.94亿元，科创50ETF华夏净流入53.79亿元、黄金ETF华安净流入29.10亿元。<br>
          <b>对腾安启示：</b>节前资金明显用宽基与信用债ETF做“避风港”，沪深300是最集中的承接方向——货架可在节前窗口把沪深300/信用债ETF前置为“长假持仓替代”专区，并标注近20日净流入与规模；同时对货币ETF（银华日利、华宝添益）单日大额净流出加注“资金搬家≠产品风险”的解释，避免用户误读。
        </div>
        <div class="card-footer">
          <a href="https://www.gelonghui.com/live/2686333" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·09-24</span></a>
          <a href="https://finance.sina.com.cn/stock/bxjj/2026-09-24/doc-inisxnvc0350509.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·新浪财经·09-24</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>    </div>
  </div>
'''

s0_start = h.index('            <!-- S0 Card 1 (09-23 P1) -->')
s0_end = h.index('<!-- ============ Section 1')
h = h[:s0_start] + S0 + h[s0_end:]
diag('04 s0')

# ---------- 5. fingerprint 同步 ----------
rep('<meta name="content-fingerprint" content="科技主题|兴银基金|ETF资金|公募秋招">',
    '<meta name="content-fingerprint" content="德邦基金|新发基金|首批18只|ETF资金">',
    '05 fingerprint')

# ---------- 6. S1：删 09-18 投教卡，补 09-25 鹏华资金端卡 ----------
s1_del_start = h.index('      <!-- S1 Card: 投教纳入国民教育体系 (09-18 P2) -->')
s1_del_end = h.index('      <!-- S1 Card: 大成基金多重考验 (09-20 P1) -->')
h = h[:s1_del_start] + h[s1_del_end:]
diag('06 s1-del')

S1_NEW = '''      <!-- S1 Card: 鹏华刘嵚 资金端配置公募创新高 (09-25 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 鹏华刘嵚：理财配置公募2.5万亿创新高·保险2.29万亿新高·主动权益盈利投资者占比79.66%</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-25</span>
          </div>
        </div>
        <div class="card-body">
          新浪财经9月25日报道：鹏华基金副总裁、首席市场官刘嵚在“AI浪潮与大资管高质量发展”年会平行主题论坛致辞表示，深耕基本面研究、捕捉超额收益的主动权益投资正是分化格局下“向上的力量”的重要方向，公募主动权益正经历从规模扩张向盈利沉淀的转变。<br>
          <b>资产端四个变化：</b>①中长期业绩稳定性稳步提升，靠短期极致风格博取业绩的现象逐步减少；②风格定位更清晰、产品结构更多元，业绩比较基准调整平稳落地后主动权益从同质化走向差异化；③更重视投资者获得感——公募基金半年报首度披露“持有人盈利占比”，据国泰海通统计，截至2026年6月末全市场主动权益基金近一年盈利投资者占比为<b>79.66%</b>；④A股新质生产力上市企业占比攀升，目前A股科技板块市值占比超三成，千亿市值以上公司中科技企业占比达<b>45%</b>，科创板、创业板上市公司合计超2000家、总市值超35万亿元。<br>
          <b>资金端：</b>低利率环境延续、优质固收资产收益率中枢下行，银行理财与保险资金均面临“多资产、再平衡”的配置挑战，提升权益配置比例的意愿和能力持续增强。截至2026年6月末，理财资金配置公募基金规模达<b>2.5万亿元</b>，委外规模与仓位均创历史新高；保险资金配置基金资产达<b>2.29万亿元</b>，续创历史新高。<br>
          <b>对腾安启示：</b>机构资金正在成为主动权益的增量主力，且“盈利投资者占比”已进入可横向比较的披露体系——机构端可把该指标做成货架筛选维度（而非仅展示收益率），并在组合页披露“持有满一年盈利占比”；理财/保险委外创新高也意味着代销端应提前准备面向机构资金的费率与报告模板。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/roll/2026-09-25/doc-inisyuqm4672669.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-25</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
'''
anchor = '      <!-- S1 Card: 贝莱德基金获批QDII资格 (09-18 P1) -->'
sec1_end_marker = '<!-- ============ Section 2'
i = h.index(anchor)
j = h.index(sec1_end_marker)
tail = h[h.index('</div>', h.index('impact-tag', i)):]
# 找到该卡结束后的 section 闭合位置：直接插在 section 闭合前
close_pos = h.rindex('    </div>\n  </div>\n', i, j)
h = h[:close_pos] + S1_NEW + h[close_pos:]
diag('07 s1-add')

# ---------- 7. S2：删 09-11 台州沃源卡，补 09-24 中基协考试细则卡 ----------
s2_del_start = h.index('      <!-- S2 Card: 中基协撤销台州沃源管理人登记 (09-11 P1 / A级官方双源) -->')
s2_del_end = h.index('      <!-- S2 Card: 上海证监局网络营销六大要求 (09-17 P0) -->')
h = h[:s2_del_start] + h[s2_del_end:]
diag('08 s2-del')

S2_NEW = '''      <!-- S2 Card: 中基协基金从业资格考试管理细则征求意见 (09-24 P1 / A级官方源) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 中基协就《基金从业资格考试管理细则》征求意见·八章四十九条·10月15日前反馈</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-24</span>
          </div>
        </div>
        <div class="card-body">
          中国证券投资基金业协会9月24日发布通知（中基协字〔2026〕326号，落款9月23日），就《基金从业资格考试管理细则（修订征求意见稿）》及修订说明公开征求意见，反馈截止<b>2026年10月15日</b>、通过邮件发送至zgksh@amac.org.cn。2015年协会发布《基金从业资格考试管理办法（试行）》确立考试管理基本制度，本次为在行业快速发展、从业人员数量大幅增长背景下的全面修订。<br>
          <b>框架：</b>修订后《细则》共<b>八章四十九条</b>，涵盖总则、组织机构职责、报名条件与考试内容、命题管理、考试组织管理、报考与参考人员纪律要求、考务工作纪律要求和附则。<br>
          <b>三大修订方向：</b>①<b>规范考试流程</b>——明确考试承办机构职责及违规处理，加强考场管理并细化考前考中考后工作内容与要求，完善应急处理机制与突发事件应对预案，加强考试内容知识产权保护、划定侵权情形并明确追责路径；②<b>严明考务纪律</b>——增设考务工作纪律要求专章，压实考试承办机构管理责任，新增对承办机构违规情形的规定及处理措施，新增对考务人员失职渎职、违规违纪行为的分级处理机制；③<b>严惩考试违纪</b>——细化违纪类型及对应惩戒措施，规范违规违纪处置程序并完善证据审查与证明标准，对存在考试违规违纪行为的从业人员依法依规<b>注销基金从业资格并记入个人诚信档案</b>。<br>
          <b>背景：</b>近年来协会在全国统考基础上增设行业专场考试，进一步提升考试组织科学性与便捷性；与此同时考试组织管理面临新形势新挑战，亟需进一步严明考试纪律、以更高标准健全考试管理制度。<br>
          <b>对腾安启示：</b>从业资格与诚信档案的绑定将提高销售合规门槛——代销端应把“基金从业资格有效性”纳入网点人员资质的定期核查项，避免持证人因历史考试违纪被注销资格后仍在岗展业；同时可把新规作为理财师培训体系的更新依据，提前对齐考纲变化。
        </div>
        <div class="card-footer">
          <a href="https://www.amac.org.cn/xwfb/tzgg/202609/t20260924_28121.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国基金业协会·09-24</span></a>
          <a href="https://finance.sina.com.cn/roll/2026-09-24/doc-inisycsp4955827.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·09-24</span></a>
          <span class="impact-tag mid">影响：中</span>
        </div>
      </div>
'''
i2 = h.index('      <!-- S2 Card: 监管重申债基费率规范化 (09-20 P1) -->')
j2 = h.index('<!-- ============ Section 3')
close2 = h.rindex('    </div>\n  </div>\n', i2, j2)
h = h[:close2] + S2_NEW + h[close2:]
diag('09 s2-add')

# ---------- 8. S5：删 09-09 智能体卡（超 T-14），补 09-24 易方达财富 AI 投顾卡 ----------
s5_grid = h.index('<div class="card-grid">', h.index('金融科技与AI投顾'))
s5_first_card = h.index('            <div class="card p0">', s5_grid)
s5_second_card = h.index('\n<div class="card p1">', s5_first_card)
h = h[:s5_first_card] + h[s5_second_card + 1:]
diag('10 s5-del')

S5_NEW = '''<div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 易方达财富AI融入投顾全链路·"1+2+3"体系落地·机器负责"找和理"、人负责"判和定"</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">09-24</span>
          </div>
        </div>
        <div class="card-body">
          上海证券报记者何漪报道（同花顺财经9月24日转载）：在第二届广东省人工智能应用对接大会分会场暨"人工智能+金融"对接会上，易方达财富人工智能部总经理刘玮表示，公司持续推进业务系统的AI化改造，目前AI应用已覆盖<b>投资研究、顾问服务、运营运作、合规风控</b>等业务全流程，通过"人机协同"整体提升投顾服务的质量、效率与覆盖范围。<br>
          <b>投顾基本盘：</b>易方达财富拥有基金销售、基金投顾、个人养老金基金代销三张牌照和超100人的专业服务团队；自有平台"e钱包"App提供超<b>130项</b>投顾策略、代销基金产品数量超万只。截至2026年6月30日服务资产规模约<b>900亿元</b>，其中投顾客户数量超<b>13万户</b>、投顾持仓客户盈利占比约<b>91%</b>。<br>
          <b>人机分工：</b>以已上线的行业研究Agent为例，系统可将一项行业研究任务拆分为资料检索、数据分析、行业比较和综合输出等环节，由不同智能体分工协作完成信息收集与基础整理；投研人员则负责设定研究框架、核验关键信息并形成最终观点——机器负责"找"和"理"，人负责"判"和"定"。该分工正从投研环节向顾问服务、账户监测、投资运作、合规风控等更长链条延伸。<br>
          <b>体系演进：</b>2020年业务开展伊始即以自然语言处理、运筹优化和机器学习解析基金公告、穿透基金持仓；2023年起依托大模型能力将复杂信息理解与归纳融入投研链路；当前正推进"<b>1+2+3</b>"AI体系建设——统一的AI能力底座、数据与技能两大能力枢纽、面向不同业务场景的三类智能平台，并把风险控制、合规要求与过程留痕嵌入服务流程。<br>
          <b>对腾安启示：</b>头部机构已把AI从"单点工具"推进到"流程协同"，且明确划出机器与人的责任边界——腾安若上线AI诊基/陪伴，除模型能力外必须先定义"哪些环节AI只做检索整理、哪些必须人工终审"，并把留痕可审计作为对客合规卖点；投顾持仓客户盈利占比91%这类"结果指标"也应同步纳入AI服务效果的考核口径。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20260924/c680266095.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·09-24</span></a>
          <span class="impact-tag high">AI投顾：高</span>
        </div>
      </div>
'''
i5 = h.index('金融科技与AI投顾')
j5 = h.index('<!-- ============ Section 6')
close5 = h.rindex('    </div>\n  </div>', i5, j5)
h = h[:close5] + S5_NEW + h[close5:]
diag('11 s5-add')

# ---------- 9. S6 行情：整体换成 09-24 收盘 ----------
S6 = '''            <div class="card p3">
        <div class="card-top">
          <div class="card-title">📈 上一交易日收盘（2026-09-24）·沪指3888.37 -1.22%·沪深北三市成交1.67万亿缩量1140亿</div>
          <div class="card-meta">
            <span class="priority-tag light">P3 知悉即可</span>
            <span class="date-tag">09-24</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（09-24收盘·中秋前缩量回调）</b><br>
              上证指数 <b>3888.37</b> <span style="color:#52c41a;">-1.22%</span><br>
              深证成指 <b>13316.97</b> <span style="color:#52c41a;">-2.34%</span><br>
              创业板指 <b>3288.95</b> <span style="color:#52c41a;">-2.68%</span><br>
              沪深300 <b>4439.14</b> <span style="color:#52c41a;">-1.73%</span><br>
              科创50 <b>1621.87</b> <span style="color:#52c41a;">-2.35%</span><br>
              北证50 <b>1055.74</b> <span style="color:#52c41a;">-1.70%</span><br>
              沪深北三市成交 <b>1.67万亿</b>·较上日缩量1140亿<br>
              逾1100只上涨·逾50只涨停；超4300只下跌
            </div>
            <div>
              <b>港股与美股（09-24收盘）</b><br>
              恒生指数 <b>24761.13</b> <span style="color:#52c41a;">-0.29%</span><br>
              恒生科技 <b>4361.13</b> <span style="color:#52c41a;">-0.41%</span><br>
              国企指数 <b>8266.01</b> <span style="color:#52c41a;">-0.09%</span><br>
              道琼斯 <b>51349.98</b> <span style="color:#52c41a;">-0.31%</span><br>
              纳斯达克 <b>26939.37</b> <span style="color:#dc2626;">+0.01%</span><br>
              标普500 <b>7704.13</b> <span style="color:#52c41a;">-0.02%</span><br>
              布伦特原油104.30美元 <span style="color:#dc2626;">+1.15%</span>·现货黄金4271.36美元 <span style="color:#52c41a;">-0.08%</span>·美债10年期突破5.1%
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>结构焦点：</b>科技成长与资源品全面回调、银行石油红利逆势走强——隔夜美国9月标普全球制造业PMI跳升至<b>57</b>、服务业PMI升至<b>58.7</b>，双双超预期并创多年新高，美联储10月加息概率升至七成，10年期美债收益率突破<b>5.1%</b>、5年期亦破5%，美元指数站上101创7月底以来新高，高利率环境直接压缩高久期、高估值成长股的估值空间。有色金属板块整体跌<b>3.53%</b>领跌，贵金属跌幅居前，山东黄金、中金黄金、赤峰黄金均跌超5%，紫金矿业跌4.46%、江西铜业跌4.83%；PCB及元件板块继续调整，通信设备、半导体等科技硬件承压；此前活跃的房地产、建材回调，CRO概念普遍调整，农业、白酒位于跌幅前列。<br>
              <b>逆势方向：</b>银行、石油石化、红利资产展现防御韧性；福建本地股午后快速拉升，路桥信息30%涨停，海峡创新、平潭发展、漳州发展、厦门港务涨停；风电设备走强，吉鑫科技涨停、威力传动涨近10%（截至8月底全国风电装机容量6.93亿千瓦、同比增长19.6%）；机器人概念活跃，襄阳轴承、长华集团、中马传动、宁波东力涨停；教育板块相对活跃。按周计算，本周上证指数累计下跌<b>0.60%</b>、深证成指跌2.37%、创业板指跌2.48%。<br>
              <b>港股与海外：</b>恒指跌0.29%报24761.13点，恒生科技跌0.41%报4361.13点，国企指数跌0.09%报8266.01点，相对A股展现韧性，中国石油股份、新东方-S、商汤-W、地平线机器人-W涨幅居前。美股9月24日收盘基本走平，道指跌0.31%、标普500跌0.02%、纳指微涨0.01%，费城半导体指数隔夜跌1.23%；欧洲三大股指9月24日全线下跌。大宗商品方面国际金价隔夜跌破4300美元关口，COMEX黄金跌1.23%、COMEX白银跌3.95%、费城金银指数跌4.13%；WTI原油涨1.31%报93.37美元、布伦特原油涨1.15%报104.30美元。人民币对美元中间价6.7489、下调21基点。<br>
              <b>备注：</b>9月24日为中秋假期前最后一个交易日，9月25日起A股休市，本期数据基准为假期前最后一个交易日收盘。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：2026-09-24收盘</span>
          <span class="source-tag">数据来源：上海证券报/中国证券网、中国证券报、新华社、中新经纬、东方财富网（09-24—09-25）</span>
        </div>
      </div>  </div>
'''
s6_start = h.index('            <div class="card p3">', h.index('市场行情速览'))
s6_end = h.index('<!-- ============ Section 7')
h = h[:s6_start] + S6 + h[s6_end:]
diag('12 s6')

# ---------- 10. S7 时间线重写 ----------
items = [
    ('red',   '2026-09-25', '湖南百亿未来产业基金落地'),
    ('red',   '2026-09-24', '中秋前A股缩量回调失守3900'),
    ('blue',  '2026-09-24', '国新国证张鹏任总经理'),
    ('blue',  '2026-09-24', '中基协发布团体标准管理办法'),
    ('blue',  '2026-09-24', '博道基金业绩比较基准修订生效'),
    ('blue',  '2026-09-23', '公募秋季策略会密集举办'),
    ('blue',  '2026-09-23', '机构称四季度有吃饭行情'),
    ('blue',  '2026-09-23', 'ETF资金流向信用债96.69亿'),
    ('blue',  '2026-09-22', '南向资金净买入超126亿港元'),
    ('blue',  '2026-09-22', '纳指涨0.45%创收盘新高'),
    ('blue',  '2026-09-20', '刘彦春卸任景顺长城副总'),
    ('blue',  '2026-09-18', '贝莱德基金获批QDII资格'),
]
tl = ''.join(
    '      <div class="timeline-item">\n'
    f'        <div class="timeline-dot {c}"></div>\n'
    f'        <div class="timeline-date">{d}</div>\n'
    f'        <div class="timeline-title">{t}</div>\n'
    '      </div>\n' for c, d, t in items)

k = h.index('关键时间线')
tl_start = h.index('      <div class="timeline-item">', k)
tl_end = h.index('\n    </div>\n\n  </div>', tl_start) + 1
h = h[:tl_start] + tl + h[tl_end:]
diag('13 s7')

# ---------- 11. 收尾校验 ----------
open(P, 'w', encoding='utf-8').write(h)
o, c = len(re.findall(r'<div\b', h)), len(re.findall(r'</div>', h))
print(f'[final] open={o} close={c} balance={o-c}')
print('S8 present:', 'S8' in h)
print('U+FFFD:', h.count('\ufffd'))
print('stray </div>>:', h.count('</div>>'))
import collections
print('date-tags:', sorted(collections.Counter(re.findall(r'date-tag">(\d{2}-\d{2})<', h)).items()))
print('S0 title:', re.search(r'<span class="section-title">([^<]*)</span>\s*\n\s*<span class="section-context">([^<]*)</span>', h).groups())
print('badge:', re.search(r'📅 数据区间：([^（<]*)', h).group(1))
print('marker:', re.search(r'<!-- daily-update: ([\d-]+) -->', h).group(1))
print('fingerprint:', re.search(r'content-fingerprint" content="([^"]*)"', h).group(1))
