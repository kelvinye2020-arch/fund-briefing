# -*- coding: utf-8 -*-
import io
PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
html = io.open(PATH, "r", encoding="utf-8").read()
checks = {
 "s8_rm_g": """      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 第二批公募基准调整全面铺开·腾安需准备基准说明话术</div>""",
 "s8_rm_h": """      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会对玖瀛资产罚款近6000万·私募严监管升级</div>""",
 "s8_rm_i": """      <div class="card p0">
        <div class="card-top">
          <div class="card-title">🔴 证监会推动修改证券投资基金法·五方面法治协同建设</div>""",
}
for k, s in checks.items():
    print("%-10s count=%d" % (k, html.count(s)))
