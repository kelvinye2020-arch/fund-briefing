# -*- coding: utf-8 -*-
import re
from datetime import date, timedelta

P = 'index.html'
src = open(P, encoding='utf-8').read()
s = src
today = date(2026, 10, 16)
CUT = (today - timedelta(days=14)).strftime('%m-%d')   # 10-02
EMO = '\U0001F4C5'
URED = '\U0001F534'
UYEL = '\U0001F7E1'
UBLU = '\U0001F535'

o0 = len(re.findall(r'<div\b', s)); c0 = len(re.findall(r'</div>', s))
def dr(tag):
    print('%-28s open=%d close=%d  (d=%+d/%+d)' % (tag, len(re.findall(r'<div\b', s)),
          len(re.findall(r'</div>', s)), len(re.findall(r'<div\b', s))-o0,
          len(re.findall(r'</div>', s))-c0))

def block_end(t, start):
    gt = t.find('>', start); depth = 1; i = gt + 1
    while depth > 0:
        no = t.find('<div', i); nc = t.find('</div>', i)
        if nc == -1: raise ValueError('unbalanced')
        if no != -1 and no < nc:
            depth += 1; i = no + 4
        else:
            depth -= 1; i = nc + 6
    return i

# ---------- 0. 基线断言 ----------
assert s.count('<!-- daily-update: 2026-10-15 -->') == 1
assert s.count('S8') == 0
assert s.count('\ufffd') == 0
assert s.count('</div>>') == 0
assert o0 == c0
print('baseline open=%d close=%d  CUT=%s' % (o0, c0, CUT))

# ---------- 1. header badge / marker / fingerprint / description ----------
upper = today.strftime('%Y.%m.%d')
lower = (today - timedelta(days=14)).strftime('%Y.%m.%d')
badge_new = EMO + ' 数据区间：%s — %s（每日更新）' % (lower, upper)
s, n = re.subn(re.escape(EMO) + r' 数据区间：\d{4}\.\d{2}\.\d{2} — \d{4}\.\d{2}\.\d{2}（每日更新）',
               lambda m: badge_new, s)
assert n == 1, 'badge replace %d' % n
assert badge_new in s

s = s.replace('<!-- daily-update: 2026-10-15 -->', '<!-- daily-update: 2026-10-16 -->')
assert s.count('<!-- daily-update: 2026-10-16 -->') == 1

FP = '多家公私募|多只主动ETF|ETF资金流向|首批新能源'
s, n = re.subn(r'(<meta name="content-fingerprint" content=")[^"]*(")', lambda m: m.group(1)+FP+m.group(2), s)
assert n == 1
DESC = ('多家公私募逆势自购|多只主动ETF优化产品名称|ETF资金流向净流入563.79亿|'
        '首批新能源金属50ETF获批|沪指10-16收3716.28')
s, n = re.subn(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), s)
assert n == 1
dr('1 header/meta')

# ---------- 2. S0 全量重建 ----------
S0_START = s.find('<!-- S0 Card 1')
S0_END = s.find('<!-- ============ Section 1')
assert S0_START > 0 and S0_END > S0_START
assert s[S0_END-12:S0_END].endswith('\n\n')

C1 = '''<!-- S0 Card 1 (10-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + UYEL + ''' 多家公私募宣布自购·凯丰投资2500万·前三季度公募净申购34.66亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          深圳商报·读创10月16日报道（记者陈燕青）：近期A股市场持续调整、沪指一度跌破3700点，多家公募、私募宣布自购旗下产品以提振投资者信心。<br>
          <b>私募端：</b>百亿私募凯丰投资10月15日晚发文称，公司于10月15日决定以自有资金合计<b>2500万元</b>认购旗下宏观策略及量化系列产品；这并非今年首次——6月17日该公司曾宣布以自有资金合计<b>3800万元</b>认购同类产品。凯丰投资成立于2012年，核心团队平均从业年限超过15年。<br>
          <b>公募端：</b>Wind数据显示，前三季度公募净申购旗下基金金额合计达<b>34.66亿元</b>，其中第三季度净申购<b>15.75亿元</b>、权益类产品规模占比近<b>八成</b>。个案方面，工银瑞信中证工程机械主题ETF上市交易公告书显示，工银瑞信投资持有<b>3000.58万元</b>为第一大持有人，工银瑞信基金另持有<b>1500.29万元</b>；兴证全球对童兰管理的兴全合辰、斯子文与高翔共同管理的兴全优加两只新发混合型产品各自购<b>1000万元</b>，两只产品均有从业人员跟投。<br>
          <b>机构观点：</b>前海开源首席经济学家杨德龙表示，公私募逆势自购一方面传递出机构对当前市场估值的认可，另一方面也能绑定基金公司与投资者的利益；百亿私募淡水泉投资认为，当前市场更多在博弈短期边际确定性，很多优质中国企业被系统性低估，为基本面选股提供了更有利环境。<br>
          <b>对腾安启示：</b>自购是信号而非收益保证，展示时须同时给出自购金额、占基金规模比例与锁定期，禁止把"机构自购"包装成"稳赚不赔"或"抄底信号"；对权益类自购占比近八成这一结构，应在内容中提示权益资产仍随市场波动，不得据此推导点位判断。
        </div>
        <div class="card-footer">
          <a href="https://news.qq.com/rain/a/20261016A03LE700" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·深圳商报·读创·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C2 = '''
      <!-- S0 Card 2 (10-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + UYEL + ''' 多只主动ETF优化产品名称·加入量化选股与红利景气策略标签</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          中国证券报·中证金牛座10月16日独家报道（记者张舒琳、张韵、王鹤静）：在首批上报的<b>18只</b>主动ETF中，多只产品已调整名称，主要变化在于进一步明确主动ETF的<b>投资范围与投资策略</b>，例如在产品名称中加入<b>量化选股、均衡配置、大盘成长、红利景气</b>等标签。<br>
          <b>仍有变数：</b>业内人士透露，鉴于尚未到最终获批阶段，不排除未来基金名称会有进一步完善；根据证监会网站信息，首批18只主动ETF的申报材料均于<b>7月17日</b>被接收。<br>
          <b>人员安排：</b>记者从业内获悉，多只主动ETF拟采取<b>双人管理</b>模式，分工或为一人主要负责选股、一人主要负责ETF管理。<br>
          <b>对腾安启示：</b>主动ETF名称从"公司+方向"升级为"策略标签化"，货架须把名称中的策略词（量化选股／均衡配置／大盘成长／红利景气）解析为可筛选字段并与实际持仓风格交叉校验，防止名称标签与组合实况背离；同时须提示产品尚未获批、名称与要素仍可能调整，不得按最终发行版提前做预约或预约数披露。
        </div>
        <div class="card-footer">
          <a href="https://jnzstatic.cs.com.cn/zzb/htmlInfo/135247.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券报·中证金牛座·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''

C3 = '''
      <!-- S0 Card 3 (10-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + UYEL + ''' ETF资金流向·10月15日九大类全线净流入563.79亿·宽基446亿</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          格隆汇10月16日：<b>10月15日</b>ETF市场九大类<b>全线净流入</b>、无一大类净流出，合计净流入约<b>563.79亿元</b>，为近期少见的大幅流入格局（同日A股沪指下跌1.59%、逾5100只个股下跌）。<br>
          <b>宽基绝对主导：</b>宽基指数ETF以<b>446亿元</b>净流入居各大类首位，净流入TOP20中11只宽基产品合计约<b>398.70亿元</b>，增持方向覆盖沪深300、科创50、创业板、上证指数、上证50、中证500、中证1000、A500全部主要宽基方向。其中沪深300ETF易方达（510310）单日净流入<b>188.03亿元</b>居全市场首位、最新规模688.52亿元，一只产品即贡献宽基大类净流入的四成以上；沪深300ETF华泰柏瑞净流入33.55亿元，两只沪深300产品合计<b>221.58亿元</b>。<br>
          <b>科创与创业板集中增持：</b>科创50ETF华夏（588000）净流入<b>65.69亿元</b>居单只第二、最新规模999.20亿元逼近千亿关口；创业板方向3只产品合计<b>72.58亿元</b>，创业板ETF易方达净流入<b>55.28亿元</b>居单只第三、最新规模713.58亿元。<br>
          <b>债券与货币跟随：</b>信用债指数ETF净流入<b>53.79亿元</b>居大类第二，6只债券类ETF进入TOP20合计约47.20亿元；货币ETF净流入17.86亿元，华宝添益与银华日利两只千亿级品种合计16.36亿元。<br>
          <b>流出端温和：</b>净流出TOP20合计约43.76亿元，单只均未超8亿元；红利低波方向2只合计净流出8.66亿元为最大流出细分，半导体设备3只合计净流出8.07亿元。<br>
          <b>对腾安启示：</b>指数下跌日出现宽基ETF单日逾560亿元净流入、且高度集中于沪深300单品，属典型的托底型资金特征而非普通配置需求；资金流向展示必须绑定统计日与单品口径，禁止把"宽基大幅流入"直接解读为市场趋势反转，也禁止用单日流入额做产品推荐排序。
        </div>
        <div class="card-footer">
          <a href="https://www.gelonghui.com/live/2713864" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">格隆汇·ETF流向观察·10-16</span></a>
          <a href="https://news.qq.com/rain/a/20261016A03AX800" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">腾讯新闻·格隆汇·10-16</span></a>
          <span class="impact-tag high">影响：高</span>
        </div>
      </div>
'''

C4 = '''
      <!-- S0 Card 4 (10-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">''' + UBLU + ''' 首批新能源金属50ETF获批·华夏华泰柏瑞华宝等跟踪中证新能源金属50指数</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻10月16日报道（每经记者肖芮冬、编辑叶峰）：华夏基金、华泰柏瑞基金、华宝基金等多家公募旗下<b>新能源金属50ETF</b>产品已正式获批，这是<b>首批跟踪中证新能源金属50指数</b>的ETF产品。<br>
          <b>同日行业动态：</b>银华基金10月16日公告，邓列军因个人原因离职、于<b>10月14日</b>离任首席信息官，总经理王立新代任首席信息官一职。<br>
          <b>ETF行情复盘（10-16）：</b>当日A股三大指数涨跌不一，沪指收红、创业板指尾盘跌幅有所收窄；板块方面军工概念快速拉升、地产股震荡走强，PCB概念震荡回落、CRO概念走弱。航空相关ETF涨超<b>6%</b>，科创100、传媒相关ETF跌超<b>3%</b>。<br>
          <b>对腾安启示：</b>新能源金属属高波动细分主题，首批产品同日获批易形成"同指数多只ETF"格局，货架须按跟踪指数、成分股集中度与管理人做同指数产品的横向对比展示，并向用户提示锂、钴等金属价格周期与主题ETF净值高波动之间的关系，禁止用"首批"概念做稀缺性营销。
        </div>
        <div class="card-footer">
          <a href="https://cd.nbd.com.cn/articles/2026-10-16/4606610.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

    </div>
  </div>

'''

s0_new = C1 + C2 + C3 + C4
s = s[:S0_START] + s0_new + s[S0_END:]
dr('2 S0')

# ---------- 2b. S0 section-context ----------
ctx_old = '<span class="section-context">10月15日 · 4条今日要闻</span>'
assert s.count(ctx_old) == 1
s = s.replace(ctx_old, '<span class="section-context">10月16日 · 4条今日要闻</span>')
assert s.count('<span class="section-title">今日焦点</span>') == 1
dr('2b S0 context')

# ---------- 3. S1 清两张 10-01 越界卡 ----------
k = s.find('<!-- S1 Card: 首批中证红利增长ETF集中上报')
assert k > 0
nxt = s.find('<!-- S1 Card: 个人投资者涌入新上市ETF')
assert nxt > k
assert s[k:nxt].count('<div class="card p') == 1
assert '10-01' in s[k:nxt]
s = s[:k] + s[nxt:]
dr('3a S1 del card1')

k = s.find('<!-- S1 Card: 前三季度ETF规模缩水1.1万亿')
assert k > 0
nxt = s.find('    </div>\n  </div>\n\n<!-- ============ Section 2')
assert nxt > k
assert s[k:nxt].count('<div class="card p') == 1
assert '10-01' in s[k:nxt]

NEW_S1 = '''<!-- S1 Card: 年内122只发起式基金清盘创历史新高 (10-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + UYEL + ''' 年内122只发起式基金清盘创历史新高·运作办法拟取消“3年2亿”强制清盘线</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          每日经济新闻10月16日报道（每经记者肖芮冬、编辑叶峰）：<b>10月15日</b>，多只发起式基金发布可能触发基金合同终止情形的提示性公告。据统计，截至三季度末，今年以来已有<b>122只</b>发起式基金清盘，<b>创历史新高</b>。<br>
          <b>规则变化：</b>近日《公开募集证券投资基金运作管理办法（征求意见稿）》发布，若新规落地，发起式迷你基金将不用再因规模不达标而清盘——征求意见稿优化发起式基金退出要求，删除现行关于发起式基金成立满3年规模不足<b>2亿元</b>需终止基金合同的规定，将发起式基金退出门槛与普通基金拉平；同时完善“迷你基金”监管要求，管理人选择持续运作的须承担基金运作固定费用成本，并要求建立基金产品规模过低的强制退出机制。<br>
          <b>对腾安启示：</b>发起式基金“满三年即可能因规模不达标清盘”的硬约束若取消，货架上相关产品的存续预期将发生实质变化，须把“是否发起式、成立满三年时点、规模是否接近2亿元”从一次性风险提示改为持续跟踪项；对仍可能触发清盘的存量产品，须提前准备持有人告知与份额转换方案，不得用“新规即将取消清盘线”作安抚性表述。
        </div>
        <div class="card-footer">
          <a href="https://cd.nbd.com.cn/articles/2026-10-16/4606610.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">每日经济新闻·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

<!-- S1 Card: 公募高质量发展新规实施一年 (10-16 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">''' + UYEL + ''' 公募高质量发展新规实施一年·考核由规模转向投资者回报·降费省出约500亿管理费</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          证券日报“十五五”产业图谱与资管配置新坐标圆桌论坛（同花顺财经10月16日刊发）：海富通基金副总经理周小波表示，《推动公募基金高质量发展行动方案》实施近一年，最根本的转变是行业核心考核指标由<b>规模</b>转向<b>投资者回报</b>，部分公司高管考核中该权重已达<b>50%</b>。<br>
          <b>投资端：</b>业绩比较基准成为过去一年讨论最多的议题，正在改变基金经理行为——基金经理不再只是投资人员，同时也是“产品经理”，须在产品合同与产品要素约定范围内投资，把产品打磨成风格更清晰的工具，即业内所称“白盒化”。周小波表示海富通在基准实施前已对投资行业偏离与集中度执行比同行略严格的管控，全行业则仍在适应过程中。<br>
          <b>产品与销售端：</b>去年一轮降费为投资者省出的管理费约<b>500亿元</b>；费率形态正从头部公司试点向中型公司推开浮动费率产品；销售端考核权重将加入投资者盈利，今年5—6月市场较好时主动限购、限大额的产品数量明显增多。<br>
          <b>格局判断：</b>周小波认为头部化持续集中，中型公司的机会在于特色化；海富通的特色方向为养老金融与固收工具类（固收ETF、“固收+”），权益端偏成长。<br>
          <b>对腾安启示：</b>“投资者回报”进入公募考核核心，货架的选品与展示口径须同步从“规模／排名”切换到“持有体验”，把基准偏离度、风格稳定性与三年／五年期业绩权重前置；浮动费率向中型公司扩容后，须把费率档位与挂钩基准做成可比字段，不得继续用单一规模指标排序推荐。
        </div>
        <div class="card-footer">
          <a href="https://news.10jqka.com.cn/20261016/c680780186.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">同花顺财经·证券日报·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

<!-- S1 Card: 弘毅远方严选混合拟发行 (10-16 P2) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">''' + UBLU + ''' 弘毅远方严选混合拟发行·拟任基金经理在管4只产品任职回报亏损·2只跌逾37%</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          中国经济网10月16日报道：弘毅远方基金发布弘毅远方严选混合型发起式证券投资基金份额发售公告，该基金自<b>2026年10月19日</b>起至<b>2027年1月18日</b>通过销售机构公开发售，募集期限不超过3个月、募集期内不设规模上限；发起资金提供方认购金额不少于<b>1000万元</b>且承诺持有期不少于3年。<br>
          <b>拟任基金经理：</b>章劲2022年2月加入弘毅远方基金，曾任上海银行资金营运中心自营业务科经理、华夏基金基金经理、华泰资产管理公司证券投资事业部固定收益投资部总经理与证券投资总监、华泰保兴基金副总经理兼首席投资官等职；目前共管理<b>8只</b>基金（各类份额分开计算），其中4只任职回报为负——弘毅远方医疗创新混合A <b>-7.46%</b>、C <b>-7.65%</b>，弘毅远方消费升级混合A <b>-37.26%</b>、C <b>-38.16%</b>。<br>
          <b>对腾安启示：</b>弱势业绩基金经理继续挂帅新发产品，是“重首发、轻持营”惯性的典型样本；货架须把拟任基金经理在管产品的任职回报与最大回撤做成新发基金页的必展示项，并区分A／C份额口径，不得只展示公司品牌与赛道概念，也不得以“发起式”“自购1000万元”替代业绩披露。
        </div>
        <div class="card-footer">
          <a href="https://finance.ce.cn/jjpd/jjpdgd/202610/t20261016_3260583.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国经济网·10-16</span></a>
          <a href="https://finance.sina.com.cn/jjxw/2026-10-16/doc-inivmazr8378490.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

'''
s = s[:k] + NEW_S1 + s[nxt:]
dr('3b S1 del+add')

# ---------- 4. S2 补一张 10-16 监管卡 ----------
k = s.find('    </div>\n  </div>\n\n<!-- ============ Section 3')
assert k > 0
NEW_S2 = '''
      <!-- S2 Card: 中基协发布后续职业培训大纲2026年度修订 (10-16 P2 / A级官方源) -->
      <div class="card p2">
        <div class="card-top">
          <div class="card-title">''' + UBLU + ''' 中基协发布《基金从业人员后续职业培训大纲（2026年度修订）》·中基协字〔2026〕341号</div>
          <div class="card-meta">
            <span class="priority-tag normal">P2 建议了解</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          中国证券投资基金业协会10月16日发布中基协字〔2026〕341号通知（落款2026年10月13日）：为加快建设一流投资机构，系统提升基金从业人员的职业道德、专业技能和胜任能力，协会根据法律法规更新和行业发展形势、结合行业培训需要，编制《基金从业人员后续职业培训大纲（2026年度修订）》并予发布，<b>自发布之日起施行</b>。<br>
          <b>配套专题培训：</b>协会10月15日另发中基协字〔2026〕339号通知，定于<b>10月22日</b>举办私募股权投资基金业务直播培训，内容为人工智能、量子科技行业的发展现状、产业链、行业研究方法及投资展望；并与香港交易所定于<b>10月29日</b>在北京合办2026年港股通业务培训班，聚焦互联互通与港股通ETF发展、多资产配置与风险管理、人工智能应用等主题。<br>
          <b>对腾安启示：</b>培训大纲修订与港股通、AI、量子科技等专题培训同步落地，反映监管对从业人员胜任能力的要求正与新质生产力、跨境配置、AI应用三条主线对齐；一线销售与投顾团队须把后续职业培训学时纳入合规台账，并在港股通ETF、AI主题产品的对客话术前完成对应专题学习，避免以旧口径解释新规则。
        </div>
        <div class="card-footer">
          <a href="https://www.amac.org.cn/xwfb/tzgg/202610/t20261016_28171.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中国证券投资基金业协会·10-16</span></a>
          <a href="https://finance.sina.com.cn/wm/2026-10-16/doc-inivkncp7036266.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·中基协·10-16</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>
'''
s = s[:k] + NEW_S2 + s[k:]
dr('4 S2')

# ---------- 5. Stats Bar 两张卡 ----------
old = '''      <div class="stat-number">3767.23</div>
      <div class="stat-label">沪指10-14收盘·跌0.88%·沪深两市成交1.41万亿·缩量约2615亿</div>
      <div class="stat-change down">▼ 失守3800点·4496只下跌·39只涨停</div>'''
assert s.count(old) == 1
new = '''      <div class="stat-number">3716.28</div>
      <div class="stat-label">沪指10-16收盘·涨0.24%·沪深北三市成交1.57万亿·缩量767亿</div>
      <div class="stat-change up">▲ 超3300只个股上涨·军工与商业航天爆发</div>'''
s = s.replace(old, new)
assert s.count(new) == 1

old = '''      <div class="stat-number">72.50亿</div>
      <div class="stat-label">10-14 ETF市场整体净流入·信用债指数ETF 54.60亿居首</div>
      <div class="stat-change neutral">◆ 行业主题ETF净流出9.19亿·中小盘宽基承压</div>'''
assert s.count(old) == 1
new = '''      <div class="stat-number">563.79亿</div>
      <div class="stat-label">10-15 ETF市场整体净流入·九大类全线净流入·宽基446亿居首</div>
      <div class="stat-change up">▲ 沪深300ETF易方达单只净流入188.03亿</div>'''
s = s.replace(old, new)
assert s.count(new) == 1
dr('5 stats')

# ---------- 6. S6 行情重写 ----------
S6_START = s.find('<!-- ============ Section 6')
S6_END = s.find('<!-- ============ Section 7')
assert S6_START > 0 and S6_END > S6_START
old6 = s[S6_START:S6_END]
assert old6.count('<div class="card p') == 1

S6 = '''<!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">\U0001F4CA</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

                        <div class="card p3">
        <div class="card-top">
          <div class="card-title">\U0001F4C8 A股、港股为10-16收盘·美股为10-15收盘·沪指3716.28 +0.24%｜缩量止跌军工爆发</div>
          <div class="card-meta">
            <span class="priority-tag fyi">P3 知悉即可</span>
            <span class="date-tag">10-16</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
              <b>A股（10-16收盘）</b><br>
              上证指数 <b>3716.28</b> <span style="color:#dc2626;">+0.24%</span>（+8.80点）<br>
              深证成指 <b>11802.46</b> <span style="color:#52c41a;">-0.12%</span>（-14.33点）<br>
              创业板指 <b>2772.38</b> <span style="color:#52c41a;">-0.39%</span>（-10.79点）<br>
              科创50 <b>1358.65</b> <span style="color:#52c41a;">-0.06%</span>（-0.87点）<br>
              北证50 <b>950.00</b> <span style="color:#52c41a;">-1.81%</span>（-17.51点）<br>
              沪深300 <b>4170.61</b> <span style="color:#dc2626;">+0.11%</span>（+4.60点）<br>
              沪深北三市成交 <b>1.57万亿</b>·较上一交易日缩量约767亿<br>
              全市场超3300只个股上涨
            </div>
            <div>
              <b>港股（10-16收盘）与美股（10-15收盘）</b><br>
              恒生指数 <b>24186.83</b> <span style="color:#dc2626;">+0.52%</span>（+124.11点）<br>
              国企指数 <b>8128.25</b> <span style="color:#dc2626;">+0.31%</span>（+24.98点）<br>
              恒生科技 <b>4108.24</b> <span style="color:#dc2626;">+1.16%</span>（+47.25点）<br>
              道琼斯 <b>52177.69</b> <span style="color:#dc2626;">+1.08%</span>（+556.21点）<br>
              纳斯达克 <b>26713.03</b> <span style="color:#dc2626;">+0.08%</span>（+20.16点）<br>
              标普500 <b>7744.06</b> <span style="color:#dc2626;">+0.33%</span>（+25.12点）<br>
              港股主板成交 <b>1782.07亿港元</b>
            </div>
            <div style="grid-column:1/-1;padding-top:10px;border-top:1px dashed #e5e7eb;">
              <b>取数口径：</b>A股、港股取<b>10月16日收盘</b>（10月16日为交易日且已收盘）；美股取<b>10月15日收盘</b>（美东10月15日收盘对应北京时间10月16日凌晨）。COMEX黄金与国际原油本期未取得可交叉验证的收盘点位，按铁律不补数值。<br>
              <b>A股（10-16）：</b>三大指数涨跌不一，沪指收红、创业板指尾盘跌幅收窄。上证指数涨8.80点、涨幅0.24%收报<b>3716.28</b>点；深证成指跌14.33点、跌幅0.12%收<b>11802.46</b>点；创业板指跌10.79点、跌幅0.39%收<b>2772.38</b>点；科创50跌0.06%收<b>1358.65</b>点；北证50跌1.81%收<b>950.00</b>点；沪深300涨4.60点、涨幅0.11%收<b>4170.61</b>点。沪深北三市成交约<b>1.57万亿元</b>（格隆汇口径全市场15691亿元），较上一交易日缩量约767亿元，全市场超<b>3300只</b>个股上涨。板块方面军工装备、商业航天爆发，晨曦航空20CM涨停、长城军工与新兴装备10CM涨停，第十六届中国航展定档12月7日至13日；特斯拉新款Roadster亮相引爆飞行汽车概念，捷众科技30CM涨停；7城落地商品房销售改革细则，地产股普涨，粤宏远A涨停、新城控股涨超8%；白酒、贵金属、风电设备涨幅居前。下跌方面，PCB概念震荡走低（四会富仕跌超14%，宝鼎科技、天津普林跌停），游戏与AI视频概念回调（电魂网络跌停），CRO概念持续回落（药明康德盘中一度触及跌停），电池、证券板块跌幅居前。<br>
              <b>港股（10-16）：</b>恒生指数涨124.11点、涨幅0.52%收报<b>24186.83</b>点，全日主板成交<b>1782.07亿港元</b>；国企指数涨24.98点、涨幅0.31%收<b>8128.25</b>点；恒生科技指数涨47.25点、涨幅1.16%收<b>4108.24</b>点，终结前一交易日跌2.72%至4060.99点、创逾2年新低的跌势。<br>
              <b>美股（10-15）：</b>三大股指上涨。道琼斯工业平均指数涨556.21点、涨幅1.08%收<b>52177.69</b>点；标准普尔500种股票指数涨25.12点、涨幅0.33%收<b>7744.06</b>点；纳斯达克综合指数涨20.16点、涨幅0.08%收<b>26713.03</b>点。标普500十一大板块八涨三跌，医疗板块与材料板块分别以1.84%和1.71%的涨幅领涨，能源板块与科技板块分别以1.55%和0.54%的跌幅领跌（新华社）。<br>
              <b>对腾安提示：</b>沪指缩量微涨但深证成指与创业板指仍收跌，指数与结构继续背离，货架与持仓页须同步刷新净值日期与估值口径，不得沿用旧净值呈现。前一日宽基ETF单日净流入逾560亿元与今日指数止跌形成呼应，但属托底型资金特征，须把“政策与资金托底”与“科技硬件侧仍在调整”两股力量并列提示，不得把单日涨跌直接解读为趋势反转。
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="source-tag">数据基准：A股、港股为2026-10-16收盘，美股为2026-10-15收盘</span>
          <span class="source-tag">数据来源：新华社、格隆汇、每日经济新闻、东方财富行情（10-16）</span>
        </div>
      </div>  </div>
'''
s = s[:S6_START] + S6 + s[S6_END:]
dr('6 S6')

# ---------- 7. S7 时间线重写 ----------
CA = '    <div style="background:white;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;">'
cs = s.find(CA)
assert cs > 0
ce = block_end(s, cs)
items = [
    ('blue',  '2026-10-16', '多家公私募宣布自购'),
    ('blue',  '2026-10-16', '多只主动ETF优化产品名称'),
    ('blue',  '2026-10-16', 'ETF单日净流入563.79亿'),
    ('blue',  '2026-10-16', '首批新能源金属50ETF获批'),
    ('blue',  '2026-10-15', '沪指跌1.59%创逾13个月新低'),
    ('blue',  '2026-10-15', '122只发起式基金清盘创新高'),
    ('blue',  '2026-10-15', '港股恒生科技创逾2年新低'),
    ('blue',  '2026-10-14', '沪指失守3800点'),
    ('blue',  '2026-10-13', '公募首份三季报出炉'),
    ('blue',  '2026-10-12', 'A股高开低走沪指跌0.43%'),
    ('blue',  '2026-10-10', '证监会召开资本市场专家座谈会'),
    ('red',   '2026-10-09', '公募运作办法迎12年来大修'),
]
for _, _, t in items:
    assert len(t) <= 25, t
body = CA + '\n'
for dot, d, t in items:
    body += ('      <div class="timeline-item">\n'
             '        <div class="timeline-dot %s"></div>\n'
             '        <div class="timeline-date">%s</div>\n'
             '        <div class="timeline-title">%s</div>\n'
             '      </div>\n') % (dot, d, t)
body += '    </div>\n'
s = s[:cs] + body + s[ce:]
dr('7 S7')

# ---------- 8. 全套断言 ----------
o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
assert o == c, 'div 失衡 %d/%d' % (o, c)
# S0 -3(去action-box) + S1 +6(净+1卡) + S2 +6(+1卡) = +9
assert o - o0 == 9 and c - c0 == 9, 'drift %+d/%+d' % (o - o0, c - c0)
assert s.count('</div>>') == 0
assert s.count('S8') == 0
assert s.count('\ufffd') == 0

# S0 段
a = s.find('<!-- S0 Card 1'); b = s.find('<!-- ============ Section 1')
seg = s[a:b]
assert seg.count('<div class="card p') == 4
assert re.findall(r'date-tag">(\d{2})-(\d{2})<', seg) == [('10', '16')] * 4, \
    re.findall(r'date-tag">(\d{2})-(\d{2})<', seg)
assert seg.count('href="http') == 5, seg.count('href="http')
assert seg.count('class="action-box"') == 0
assert seg.count('<span class="source-tag">') == 5, seg.count('<span class="source-tag">')
assert s.count('<span class="section-title">今日焦点</span>') == 1
assert s.count('<span class="section-context">10月16日 · 4条今日要闻</span>') == 1

# S1 = 6 / S2 = 4 / S7 = 12
a = s.find('<!-- ============ Section 1'); b = s.find('<!-- ============ Section 2')
assert s[a:b].count('<div class="card p') == 6, s[a:b].count('<div class="card p')
a = s.find('<!-- ============ Section 2'); b = s.find('<!-- ============ Section 3')
assert s[a:b].count('<div class="card p') == 4, s[a:b].count('<div class="card p')
assert s.count('<div class="timeline-item">') == 12
assert s.count('timeline-desc') == 0

# T-14 全量扫描
tags = re.findall(r'date-tag">(\d{2})-(\d{2})<', s)
bad = [t for t in tags if '%s-%s' % t < CUT]
assert not bad, '越界 date-tag: %s (CUT=%s)' % (bad, CUT)
print('date-tags all >= %s ; total %d' % (CUT, len(tags)))

# 黑名单自检
BL = ['stcn', 'cls.cn', '21jingji', 'yicai.com', 'guba.eastmoney', 'toutiao',
      'so.html5.qq.com', '163.com/dy', 'dy.163.com', 'weibo.com', 'k.sina.com.cn',
      'q.fund.sohu.com', 'topnews.cn', 'futunn.com', 'jiantou8.com', 'cofool.com', 'cqcb.com']
hits2 = [w for w in BL if w in s]
assert not hits2, '全文件黑名单命中: %s' % hits2

# fingerprint / description 分段（闸6/闸8 只比对前 4 字）
fp = re.search(r'content-fingerprint" content="([^"]*)"', s).group(1).split('|')
assert len(fp) == 4
titles = re.findall(r'<div class="card-title">(.{0,60})</div>', seg)
for f in fp:
    assert any(f[:4] in t for t in titles), 'fingerprint 段前4字未命中: %s' % f
ds = re.search(r'name="description" content="([^"]*)"', s).group(1).split('|')
assert len(ds) == 5
for f in ds[:4]:
    assert any(f[:4] in t for t in titles), 'description 段前4字未命中: %s' % f

open(P, 'w', encoding='utf-8').write(s)
print('WRITE OK  size %d -> %d' % (len(src), len(s)))
