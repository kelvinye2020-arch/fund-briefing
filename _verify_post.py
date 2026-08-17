# -*- coding: utf-8 -*-
import io, re
PATH = r"c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html"
html = io.open(PATH, "r", encoding="utf-8").read()

print("== marker ==")
print("  daily-update: 2026-07-11" in html, "| old 07-10 gone:", "daily-update: 2026-07-10" not in html)
print("== badge ==")
print("  2026.06.27 — 2026.07.11" in html, "| old 06.26 gone:", "2026.06.26 — 2026.07.10" not in html)

print("== S0 date-tags ==")
# find S0 card-grid block: between '今日焦点' section and next section comment
s0 = html[html.find('<!-- ============ Section 0'):html.find('<!-- ============ Section 1')]
tags = re.findall(r'class="date-tag">(\d{2}-\d{2})</span>', s0)
print("  S0 cards:", len(re.findall(r'class="card ', s0)), "| date-tags:", tags)

print("== S7 items & earliest date ==")
s7 = html[html.find('Section 7'):html.find('Section 8')]
dates = re.findall(r'timeline-date">(\d{4}-\d{2}-\d{2})（', s7)
print("  S7 count:", len(dates), "| earliest:", min(dates), "| has 07-11:", "2026-07-11" in s7, "| 06-26 gone:", "2026-06-26" not in s7)

print("== S8 cards & dates ==")
s8 = html[html.find('Section 8'):html.find('<!-- ============ Footer') if 'Footer' in html else len(html)]
cards8 = re.findall(r'class="card[ "][^>]*>.*?class="date-tag">(\d{2}-\d{2})</span>', s8, re.S)
print("  S8 card-date tags found:", cards8)
# also list S8 card titles
titles8 = re.findall(r'class="card-title">([^<]+)</div>', s8)
print("  S8 titles count:", len(titles8))

print("== expired-check (no 06-26 anywhere) ==")
print("  06-26 in html:", "2026-06-26" in html, "| 06-25 in html:", "2026-06-25" in html)
print("== S2 new (销售合规) present, old P0 gone ==")
print("  销售合规 present:", "证监局密集开展基金销售合规摸底" in html)
print("  S2 法治协同 gone:", "五方面推动资本市场法治协同建设" not in html)
