import re

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_s7 = '''  <!-- ============ Section 7: 关键时间线 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:#eef2ff;color:var(--info);">&#128197;</div>
      <span class="section-title">近两周关键事件时间线</span>
    </div>

    <div class="card" style="border-left-color: var(--info);">
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-09（CPI今夜20:30·美股反弹+A股4000点保卫战·SpaceX明日定价）</div>
          <div class="timeline-title">CPI前夜：今晚20:30美国5月CPI公布 / 美股纳指+1.50%提振A股 / SpaceX IPO明（6/11）定价后日挂牌</div>
          <div class="timeline-desc">今晚20:30美国5月CPI为本周最大单一变量，直接决定6/18美联储议息基调。美股周一纳指+1.50%芯片股企稳反弹。A股昨日失守4000点（3959.34/-1.70%），今日能否放量收复是调整接近尾声的关键验证。SpaceX IPO机构认购今日（纽约时间）截止，明日定价，后日（6/12）纳斯达克正式挂牌，募资约750亿美元，估值1.77万亿美元。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-08（A股4000点保卫战打响·沪指失守3959点·超级周正式开局）</div>
          <div class="timeline-title">A股沪指3959.34(-1.70%)失守4000点 / 6/10中美CPI同日公布 / 6/12 SpaceX上市+指数调样千亿换仓</div>
          <div class="timeline-desc">6月8日周一A股全线下跌，沪指失守4000点收于3959.34点。主因：美国5月非农17.2万翻倍超预期→加息预期飙升→全球股市普跌。本周超级周正式开局：6/10中美CPI同日公布，6/12 SpaceX史上最大IPO纳斯达克挂牌+沪深300等指数样本调整生效，被动资金千亿级调仓。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-06（中基协换届刘晓艳当选会长·吴清四个坚持定调·翻倍基增至17只）</div>
          <div class="timeline-title">中基协第四届换届：易方达刘晓艳当选兼职会长 / 吴清定调"四个坚持" / 年内翻倍基增至17只</div>
          <div class="timeline-desc">中基协空缺两年后完成换届，刘晓艳为23年来首位头部公募女性掌门人。吴清在第四届会员代表大会上明确定调"四个坚持"。年内翻倍基增至17只引发抱团争议。华盛证券6/15起暂停内地新开仓，跟进跨境券商整治。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-05（A股缩量下跌·国办私募顶层设计落地·中证金牛被集体解约）</div>
          <div class="timeline-title">A股沪指4027.74(-0.74%)缩量下跌 / 国办23万亿私募顶层设计落地 / 中证金牛被招商/嘉实等集体解约</div>
          <div class="timeline-desc">国办函〔2026〕54号全文发布，私募基金行业首份国务院层面顶层设计文件。中证金牛被多家公募集体终止合作，第三方代销出清加速。美国非农17.2万翻倍→加息预期升温，全球市场承压。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-04（A股缩量回调·央行5月国债净投放500亿·易方达ETF登顶第一）</div>
          <div class="timeline-title">A股沪指4057.78(-0.64%)缩量回调 / 央行5月国债净投放500亿 / 易方达ETF规模6185亿超越华夏登顶</div>
          <div class="timeline-desc">A股缩量回调，半导体/AI方向承压。央行5月公开市场国债买卖净投放500亿，延续宽松基调。易方达基金旗下ETF规模达6185.19亿元，超越华夏基金登顶全市场ETF规模第一，差距仅19亿元，竞争白热化。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-03（东吴115亿收购东海证券·标普首破7600·美股再创历史新高）</div>
          <div class="timeline-title">东吴证券115亿收购东海证券83.68%股份草案公告 / 标普500首破7600点创新高 / 央行国债净投放500亿</div>
          <div class="timeline-desc">百亿级券商合并案正式落地，东海100%股权评估137.65亿。央行延续宽松基调，5月公开市场国债买卖净投放500亿。美股三大指数再创新高，标普500首破7600点，Marvell+30%。A股创业板+2.66%深V修复。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-02（腾讯暴涨10.46%创2021来最大涨幅·恒生科技+4.72%·AI Agent突破）</div>
          <div class="timeline-title">腾讯控股+10.46%（AI Agent突破+云降价97.5%）/ 恒生科技+4.72% / A股创业板+2.66%深V修复</div>
          <div class="timeline-desc">腾讯单日暴涨10%创4年来最大涨幅，AI Agent开发平台+云降价97.5%双重催化。恒生科技大涨，美团+9%。A股探底回升，MLCC/CPO/机器人爆发。成交2.79万亿。成交额前20科技股全部收红。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-01（宇树科技IPO过会·195只基金基准换新生效·指数样本6/12调整公告）</div>
          <div class="timeline-title">宇树科技科创板IPO过会（拟募42亿·人形机器人第一股）/ 195只基金业绩基准正式换新 / 沪深300等指数样本6/12调整</div>
          <div class="timeline-desc">宇树科技IPO过会，冲刺科创板"具身智能第一股"，受理仅73天。195只基金总规模近4000亿业绩基准正式调整生效。沪深300换19只/中证500换50只样本6/12收盘后生效，千亿被动资金调仓。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-05-29（五月收官放量暴跌·科创50-5.04%·中芯-9%·MSCI调整生效）</div>
          <div class="timeline-title">A股五月收官放量暴跌 / 科创50-5.04%领跌 / 中芯国际-8.97% / MSCI调整收盘后正式生效 / 成交3.34万亿</div>
          <div class="timeline-desc">五月最后一个交易日放量杀跌，科创50暴跌5.04%，中芯国际-9%，半导体全线崩溃。MSCI 5月调整正式生效，近3900股下跌。成交3.34万亿放量。</div>
        </div>
      </div>



    </div>
  </div>
'''

# Replace S7 section
pattern = r'  <!-- ============ Section 7:.*?  <!-- ============ Section 8:'
content = re.sub(pattern, new_s7 + '  <!-- ============ Section 8:', content, flags=re.DOTALL)

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('S7 timeline updated successfully')
print('Entries: 06-09, 06-08, 06-06, 06-05, 06-04, 06-03, 06-02, 06-01, 05-29')
print('Removed: duplicate 06-09, outdated 05-31')
