#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复06-19重复条目 + 删除S7超期/超量条目"""

HTML_PATH = r"c:/Users/kelvinyye/WorkBuddy/20260314103829/index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ========== 1. 删除重复的06-19时间线条目 ==========
# 找出S7区域
s7_start = content.find('<!-- ============ Section 7:')
s7_end = content.find('<!-- ============ Section 8:', s7_start)
s7_region = content[s7_start:s7_end]

# 找所有06-19时间线条目（完整div）
# 第一个是正确的，第二个是重复的，删除第二个
entries_0619 = list(re.finditer(r'<div class="timeline-item">\s+<div class="timeline-dot red"></div>\s+<div>\s+<div class="timeline-date">2026-06-19', s7_region))

print(f"找到 {len(entries_0619)} 个06-19时间线条目")

if len(entries_0619) >= 2:
    # 删除第二个（保留第一个）
    # 找到第二个条目的结束位置（下一个timeline-item或S7结束）
    second_start = entries_0619[1].start()
    # 找第二个条目的结束：从second_start开始找下一个</div>\n      </div>\n    </div>
    # 更精确：找从second_start开始的完整timeline-item结束位置
    rest = s7_region[second_start:]
    # 找该timeline-item的闭合：</div>\n    </div> 后面跟的是下一个timeline-item或S7结束
    # 用正则找完整的timeline-item块
    match = re.match(r'(<div class="timeline-item">.*?</div>\s+</div>\s+</div>)', rest, re.DOTALL)
    if match:
        dup_block = match.group(1)
        content = content.replace(dup_block, '', 1)  # 只替换第一次
        print("✅ 已删除重复的06-19条目")
    else:
        print("⚠️ 无法定位重复条目的完整块")

# ========== 2. 删除S7最旧的条目（保留10条）==========
# 重新读取S7区域
s7_start = content.find('<!-- ============ Section 7:')
s7_end = content.find('<!-- ============ Section 8:', s7_start)
s7_region = content[s7_start:s7_end]

# 找所有timeline-item块
timeline_items = list(re.finditer(r'<div class="timeline-item">(.*?)</div>\s+</div>\s+</div>', s7_region, re.DOTALL))
print(f"S7现有 {len(timeline_items)} 条时间线条目")

# 需要删除最旧的2条（06-06和06-08），保留11条
if len(timeline_items) > 12:
    # 删除最后2条（最旧的在最后）
    for i in range(len(timeline_items) - 1, len(timeline_items) - 3, -1):
        if i < 0:
            break
        block = timeline_items[i].group(0)
        # 检查是否是旧条目
        if '2026-06-06' in block or '2026-06-08' in block or '2026-06-05' in block:
            content = content.replace(block, '', 1)
            print(f"✅ 已删除旧条目（包含: {['2026-06-06' if '2026-06-06' in block else ''][0]}）")
            
# 重新统计
s7_start = content.find('<!-- ============ Section 7:')
s7_end = content.find('<!-- ============ Section 8:', s7_start)
s7_region = content[s7_start:s7_end]
timeline_items = list(re.finditer(r'<div class="timeline-item">', s7_region))
print(f"S7修正后共 {len(timeline_items)} 条")

# ========== 3. 写回文件 ==========
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ fix_0619 完成")
