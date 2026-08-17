#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确删除S7中06-06条目 + 最终校验"""

HTML_PATH = r"c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 删除06-06时间线条目（精确匹配）
old_block = """      <div class="timeline-item">
        <div class="timeline-dot red"></div>
        <div>
          <div class="timeline-date">2026-06-06（中基协换届刘晓艳当选会长·吴清四个坚持定调·翻倍基增至17只）</div>
          <div class="timeline-title">中基协第四届换届：易方达刘晓艳当选兼职会长 / 吴清定调"四个坚持" / 年内翻倍基增至17只</div>
          <div class="timeline-desc">中基协空缺两年后完成换届，刘晓艳为23年来首位头部公募女性掌门人。吴清在第四届会员代表大会上明确定调"四个坚持"。年内翻倍基增至17只引发抱团争议。华盛证券6/15起暂停内地新开仓，跟进跨境券商整治。</div>
        </div>
      </div>



    </div>"""

new_block = """    </div>"""

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    print("✅ 已删除06-06时间线条目")
else:
    print("⚠️ 未找到06-06条目精确匹配，尝试模糊删除")
    # 用正则删除
    import re
    pattern = r'<div class="timeline-item">\s+<div class="timeline-dot red"></div>\s+<div>\s+<div class="timeline-date">2026-06-06（中基协换届.*?</div>\s+</div>\s+</div>'
    new_content = re.sub(pattern, '', content, count=1, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        print("✅ 已通过正则删除06-06条目")
    else:
        print("❌ 无法定位06-06条目")

# 最终校验：统计S7条目数
s7_start = content.find('<!-- ============ Section 7:')
s7_end = content.find('<!-- ============ Section 8:', s7_start)
s7_region = content[s7_start:s7_end]
import re
items = re.findall(r'<div class="timeline-item">', s7_region)
print(f"S7现有 {len(items)} 条时间线条目")
dates = re.findall(r'timeline-date[^>]*>([^<]+)<', s7_region)
for d in dates:
    print(f"  - {d}")

# 写回
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ fix_s7_v2 完成")
