import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义S6部分的新内容
new_s6 = '''  <!-- ============ Section 6: 市场行情速览 ============ -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon" style="background:var(--success-light);color:var(--success);">📊</div>
      <span class="section-title">市场行情速览</span>
      <span class="section-badge" style="background:var(--success-light);color:var(--success);">辅助决策</span>
    </div>

    <div class="card p3">
      <div class="card-top">
        <div class="card-title">周日A股休市（6/22）·明日6/23开市·端午假期结束</div>
        <div class="card-meta">
          <span class="priority-tag fyi">知悉即可</span>
        </div>
      </div>
      <div class="card-body">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <b>📊 周日（6/22）：</b>A股/港股通休市，美股正常交易。端午假期最后一日，海外市场相对平静。<br><br>
            <b>📊 明日开市（6/23·周一）：</b>A股/港股通恢复交易。假期期间积累的资讯和情绪将在明日集中释放。<br><br>
            <b>📊 节前最后交易日（6/18）回顾：</b>A股分化，沪指<b>4090点(-0.43%)</b>，深证成指<b>16030点(+0.94%)</b>，创业板指<b>4252点(+2.05%)</b>，科创50指数<b>涨3.84%</b>。
          </div>
          <div>
            <b>📊 假期期间海外动态：</b><br>
            ▪ 纳指ETF溢价风险爆发→多只产品6/22临停<br>
            ▪ LOF高溢价20%+→财通多只产品连续涨停<br>
            ▪ 黄金价格回落→高盛下调12月金价预期至4900美元<br><br>
            <b>📊 对基金行业影响（明日开市）：</b><br>
            ▪ 纳指ETF临停→Client可能集中咨询溢价风险<br>
            ▪ 假期情绪积累→明日可能放量，关注方向选择<br>
            ▪ 科技风格延续性→关注科创50能否延续强势
          </div>
        </div>
      </div>
      <div class="card-footer">
        <span class="source-tag">NeoData·周日休市</span>
        <span class="source-tag">明日6/23开市</span>
        <span class="impact-tag low">行情速览</span>
      </div>
    </div>
  </div>'''

# 使用正则表达式替换S6部分
pattern = r'(?s)<!-- ============ Section 6: 市场行情速览 ============ -->.*?<!-- ============ Section 7: 关键时间线 ============ -->'
replacement = new_s6 + '\n  <!-- ============ Section 7: 关键时间线 ============ -->'
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("S6部分已更新")
