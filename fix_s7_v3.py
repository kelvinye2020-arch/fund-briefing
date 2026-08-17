#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确删除S7中06-02超期条目"""
import re

with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到06-02条目的起始位置
idx = content.find('2026-06-02（腾讯暴涨')
print(f'06-02条目位置: {idx}')

if idx >= 0:
    # 往前找<div class="timeline-item">的开头
    marker = '<div class="timeline-item">'
    start = content.rfind(marker, 0, idx)
    print(f'条目start位置: {start}')
    
    # 往后找该条目的结束位置（下一个timeline-item开始或S7结束）
    next_marker = '</div>\n    </div>\n\n      <div class="timeline-item">'
    end = content.find(next_marker, idx)
    if end >= 0:
        end = end + len('</div>\n    </div>')
    else:
        # 是最后一条，找到S7结束位置
        end_marker = '</div>\n    </div>\n  <!-- ============ Section 8'
        end = content.find(end_marker, idx)
        if end >= 0:
            end = end + len('</div>\n    </div>')
    
    print(f'条目end位置: {end}')
    print(f'待删除内容长度: {end - start} 字符')
    
    # 删除
    content = content[:start] + '\n' + content[end:]
    print('[OK] 06-02超期条目已删除')
else:
    print('[WARN] 未找到06-02条目')

# 验证
s7_start = content.find('Section 7')
s7_end = content.find('Section 8')
s7 = content[s7_start:s7_end]
dates = re.findall(r'<div class="timeline-date">([^<]+)</div>', s7)
print(f'\n删除后S7时间线条目数: {len(dates)}')
for i, d in enumerate(dates):
    print(f'  {i+1}. {d}')

# 检查超期
overdue = [d for d in dates if ('06-01' in d or '05-' in d or ('06-02' in d and '06-02' in d[:10]))]
if overdue:
    print(f'\n[WARN] 仍有超期条目: {overdue}')
else:
    print('\n[OK] 无超期条目')

# 写入
with open(r'c:\Users\kelvinyye\WorkBuddy\20260314103829\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('\n[OK] index.html 已保存')
