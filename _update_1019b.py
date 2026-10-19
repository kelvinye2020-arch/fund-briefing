# -*- coding: utf-8 -*-
"""
daily-update 2026-10-19 补件：清理 S4/S5 越过 T-14（10-05）边界的旧卡并补入窗口内新卡
闸2 报：S4 "9月基金发行冰火两重天" 10-02、S5 "券商AI进入双层竞争" 10-04
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = 'index.html'
h = open(p, encoding='utf-8').read()

def find_marker(key):
    i = h.find(key)
    assert i > 0, f'未找到 marker：{key}'
    # 回溯到该行行首（含缩进）
    j = h.rfind('\n', 0, i)
    return j + 1

def swap(start_key, end_key, new_card, tag):
    global h
    a = find_marker(start_key)
    b = find_marker(end_key)
    assert b > a, f'{tag} 边界顺序异常'
    o, c = h.count('<div'), h.count('</div>')
    h = h[:a] + new_card + h[b:]
    o1, c1 = h.count('<div'), h.count('</div>')
    print(f'  · {tag}: open {o1-o:+d}, close {c1-c:+d}')
    assert o1 - o == c1 - c, f'{tag} div 漂移不配对'

S4_NEW = '''      <!-- S4 Card: 公募探寻“产、投、销、考”全链条稳市路径 (10-19 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 公募探寻“产、投、销、考”全链条稳市路径·年内新成立1385只已超去年</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-19</span>
          </div>
        </div>
        <div class="card-body">
          证券时报10月19日报道（记者裴利瑞）：A股震荡反复、短期资金追涨杀跌，多家受访机构认为公募要真正发挥市场“稳定器”作用，关键并非简单扩大权益投资规模，而是<b>减少顺周期行为、增强跨周期投资能力</b>，需在“产、投、销、考”四个环节协同发力。<br>
          <b>产品端：</b>Wind数据显示，截至2026年三季度末，今年以来全市场新成立<b>1385只</b>基金，已超去年同期的<b>1110只</b>；市场上涨的二季度新成立<b>498只</b>，远超去年同期的<b>369只</b>，名称带有“科创”“芯片”“智选”等关键词的新产品募集成绩尤为亮眼，顺周期发行的规模路径依赖仍存。一位第三方基金评价人士举例，部分五六月份在科技板块高位成立的基金，到三季度便遭遇<b>百分之二三十</b>的回撤。监管侧已强制披露“盈利投资者占比”“持有期收益”并将“投资者盈亏与持有期限”纳入代销机构考核；《公开募集证券投资基金运作管理办法（征求意见稿）》拟将非固收类基金成立门槛由2亿份／2亿元降至<b>5000万份／5000万元</b>，中欧基金认为这有利于降低产品成立对短期市场热度的依赖。<br>
          <b>投资端：</b>博时基金首席策略分析师陈显顺表示，公募须从“组合管理”转向“资产配置管理”，在行业配置、仓位管理和风险预算方面建立系统化框架；晨星（中国）基金研究中心总监孙珩建议完善基金经理长期考核机制、收紧基金合同投资边界、建立内部持仓风格定期稽核体系，销售渠道须充分披露产品风格定位与风格漂移风险。<br>
          <b>销售端：</b>博时基金提出构建“认知引导、情绪陪伴、产品支撑、渠道协同”四位一体投教陪伴体系，大力发展持有期基金、FOF、多资产配置工具并推广纪律化定投；晨星中国董事长陈鹏认为下一步关键是推出真正的<b>投顾份额（干净份额）</b>，把信义义务落实到投顾业务实操细则，并用好个人养老金等制度管道探索默认配置模式。<br>
          <b>考核端：</b>嘉实基金表示将围绕长周期考核全面建立以基金投资收益为核心的考核体系；陈显顺建议行业评价体系从“规模导向”转向“价值创造导向”。<br>
          <b>对腾安启示：</b>“逆周期布局”已从监管要求下沉到产品、投资、销售、考核四个环节，货架排序与推荐逻辑须同步弱化新发规模与短期排名权重，改为展示盈利投资者占比、持有期收益与风格稳定性；对高位成立的次新基金须在详情页标注成立时点与建仓区间，不得以“赛道景气”掩盖“成立即高位”的回撤来源。
        </div>
        <div class="card-footer">
          <a href="https://finance.sina.com.cn/jjxw/2026-10-19/doc-inivsstf7059851.shtml" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">新浪财经·证券时报·10-19</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

'''

S5_NEW = '''      <!-- S5 Card: 中泰证券以AI嵌入财富管理全流程 (10-17 P1) -->
      <div class="card p1">
        <div class="card-top">
          <div class="card-title">🟡 中泰证券把AI嵌入财富管理全流程·自研“中泰小研”人均使用超30次每月</div>
          <div class="card-meta">
            <span class="priority-tag important">P1 重要关注</span>
            <span class="date-tag">10-17</span>
          </div>
        </div>
        <div class="card-body">
          财联社专访（中华网山东频道10月17日刊发）：中泰证券党委书记、董事长王洪表示，公司锚定<b>客群经营、买方投顾、数智平台、品牌生态</b>四大支柱，以金融科技激活新质生产力，构建“数智底座—智能中台—数字化运营”三层架构。<br>
          <b>AI落地：</b>公司携手阿里云打造“千问千泰”投顾品牌；自2022年起全力自研智能投研平台，已形成覆盖股票、ETF、公募、私募及基金投顾的<b>五大研究体系</b>与总量行研、股票研究、产品分析、资产配置<b>四大核心模块</b>，打造统一智能助手<b>“中泰小研”</b>，用户覆盖公司绝大部分员工，<b>人均使用超30次/月</b>，支撑相关系统<b>30余万次/周</b>。数字化运营运用机器学习与人工智能整合客户特征、服务内容、触达渠道与执行节奏，打通从需求线索挖掘到服务策略迭代的全周期闭环，累计落地<b>700余个服务场景</b>。<br>
          <b>客群与投顾：</b>财富管理客户<b>1100多万户</b>、管理客户资产<b>1.77万亿元</b>；依托<b>2300余名</b>持牌证券投资顾问建设“牛人领航”品牌，组建<b>400余个</b>投顾团队，累计服务客户<b>26万余户</b>、签约资产超<b>800亿元</b>；“中泰财富30”下含量化30、ETF30、公募30三大子品牌，力争<b>2027年末</b>量化和ETF策略师团队规模不少于<b>1500人</b>；公募基金投顾与万家基金、中欧基金、盈米等<b>6家</b>投顾机构合作“双投顾服务模式”，已上线策略<b>17个</b>。<br>
          <b>对腾安启示：</b>券商正把AI从单点工具升级为贯穿投研、投顾与运营的基础设施，并以“综合账户＋持牌投顾＋策略师团队”承接买方投顾。腾安侧的AI能力须明确定位为“辅助判断与陪伴”而非收益承诺——凡涉及选基、组合调整的建议，须标注模型口径、数据源与更新频率，并保留人工复核与风险揭示链路；对“双投顾”“策略师团队”等模式，须在产品页披露服务提供方与费用归属，避免投资者误认为由单一机构承担全部受托责任。
        </div>
        <div class="card-footer">
          <a href="https://sd.china.com/m/cjzx/20000936/20261017/26019738.html" target="_blank" style="color:#1890ff;text-decoration:none;"><span class="source-tag">中华网·财联社·10-17</span></a>
          <span class="impact-tag medium">影响：中</span>
        </div>
      </div>

'''

swap('<!-- S4 Card: 9月基金发行冰火两重天', '<!-- S4 Card: 公募固收+发展迎来三重共振', S4_NEW, 'S4 换卡')
swap('<!-- S5 Card: 券商AI进入', '<!-- S5 Card: 工银瑞信以AI重塑投研基因', S5_NEW, 'S5 换卡')

open(p, 'w', encoding='utf-8').write(h)
fo, fc = h.count('<div'), h.count('</div>')
print(f'\n终点 div: open={fo} close={fc}')
assert fo == fc
assert 'S8' not in h
print('补件写入完成')
