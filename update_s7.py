import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义S7部分的新内容（删除06-06条目，新增6/22事件，保留10-12条）
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
          <div class="timeline-date">2026-06-22（周日·A股休市·纳指ETF临停+LOF高溢价+FOF破峰值）</div>
          <div class="timeline-title">多只纳指ETF集体临停（10:30复牌）/ 多只LOF连续涨停高溢价20%+ / FOF上半年新发1137亿破历史峰值</div>
          <div class="timeline-desc">6月22日，汇添富纳指ETF等5只QDII产品因高溢价集体临停（10:30复牌），溢价风险集中爆发。财通多只LOF连续涨停，溢价率飙升至20%+，极小流通盘催生虚假繁荣。FOF上半年新成立88只，合计发行规模1137.69亿，超越2021年峰值。端午假期最后日，市场情绪积累，明日6/23开市关注放量方向。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-19（端午三市同休·A股/港股通/美股均休市·美联储鹰派持续发酵）</div>
          <div class="timeline-title">端午三市同休（A股/港股通/美股6/19均休市）/ 美联储鹰派信号持续发酵·年内或加息一次 / 五部门启动新能源车下乡</div>
          <div class="timeline-desc">2026年端午节，A股/港股通/美股罕见三市同休（6/19-6/21），6/22开市。美联储6/18议息结果持续发酵，沃什首秀点阵图转鹰，年内加息预期升温，全球债市遭抛售。五部门（工信部/商务部等）启动2026新能源车下乡活动，但新能源车板块短期仍震荡。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-18（美联储议息落地·沃什首秀·A股端午前最后交易）</div>
          <div class="timeline-title">美联储维持利率3.50%-3.75%不变但点阵图中值升至3.75%-4.0% / 沃什首秀转鹰暗示可能加息 / A股端午前最后交易日</div>
          <div class="timeline-desc">美联储6月议息结果北京时间今日02:00落地：维持利率不变符合预期，但点阵图中值大幅转鹰（年底利率预期3.75%-4.0%），新任主席沃什举行首秀新闻发布会。A股今日为端午前最后交易日，科创50昨日+4%，但4只沪深300ETF净流出137亿元。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-17（陆家嘴论坛开幕·央行/证监会/金融监管总局一把手集体发声）</div>
          <div class="timeline-title">2026陆家嘴论坛今日开幕 / 证监会宣布抓紧推出主动ETF / 沪深交易所同步发布业务指引</div>
          <div class="timeline-desc">2026陆家嘴论坛6月17日上午在上海正式开幕，央行行长潘功胜、证监会主席吴清、金融监管总局局长丁向群集体发声。吴清宣布抓紧推出主动管理ETF，沪深交易所同步发布《主动管理交易型开放式证券投资基金业务指引》。</div>
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
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-12（SpaceX正式挂牌·指数调样生效·跨境券商禁令执行）</div>
          <div class="timeline-title">SpaceX今日正式纳斯达克挂牌（代码SPCX）/ 指数调样今日收盘后生效·千亿被动调仓 / 跨境券商禁令正式执行</div>
          <div class="timeline-desc">SpaceX以代码SPCX正式在纳斯达克挂牌，发行价135美元/股，估值1.77万亿美元。沪深300等10余只宽基指数样本调整今日收盘后正式生效，近9000亿指数基金被动调仓。跨境券商禁令今日正式执行。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-11（欧央行重启加息·SpaceX定价确认）</div>
          <div class="timeline-title">欧央行宣布重启加息25bp（全球主要经济体首家）/ SpaceX IPO定价135美元/股确认</div>
          <div class="timeline-desc">欧洲央行成为2026年首家重启加息的全球主要经济体央行，存款机制利率+25bp。SpaceX IPO发行价确认为135美元/股，估值1.77万亿美元，明日正式挂牌。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-10（CPI=4.2%符合预期·美股重挫·A股缩量震荡）</div>
          <div class="timeline-title">美国5月CPI=4.2%符合预期 / 美股三大指数集体收跌（道指-1.88%·纳指-1.98%）/ A股沪指3993(+0.47%)缩量</div>
          <div class="timeline-desc">美国5月CPI数据昨晚20:30公布，同比4.2%符合预期，但未超预期→美联储加息预期进一步升温。受此影响，隔夜美股三大指数集体收跌。A股今日缩量震荡，沪指收3993.23(+0.47%)。</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-09（A股暴力反弹收复4000点·美股分化·港股止跌）</div>
          <div class="timeline-title">A股沪指4010.03(+1.28%)收复4000点 / 创业板+3.93%暴力反弹 / 美股纳指+0.86%</div>
          <div class="timeline-desc">A股全线反弹，沪指4010.03点（+1.28%）收复4000点，创业板指+3.93%，科创50+4.17%，科技股集体爆发。美股纳指+0.86%，英特尔+11.10%。港股恒生科技+0.29%止跌回升。</div>
        </div>
      </div>



    </div>
  </div>'''

# 使用正则表达式替换S7部分
pattern = r'(?s)<!-- ============ Section 7: 关键时间线 ============ -->.*?<!-- Footer -->'
replacement = new_s7 + '\n  <!-- Footer -->'
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("S7时间线已更新")
