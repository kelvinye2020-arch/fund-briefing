#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix S7 timeline: remove the duplicate 06-09 entry at ~line 1372-1379.
   Keep the first 06-09 entry (at ~line 1309-1316).
   Actually: after previous edits, the duplicate is at lines 1372-1379 (0-indexed: 1371-1378).
   Let's just read all lines and remove the 2nd timeline-item block whose timeline-date contains '06-09'.
"""
with open('index.html', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Find indices of all timeline-item blocks that contain '06-09' in timeline-date
# A timeline-item block = starts with '      <div class="timeline-item">' and ends with '      </div>' (6 spaces)
# Actually in file: '      <div class="timeline-item">' (6 spaces)
# Let's find line numbers (1-indexed) where 'timeline-date' contains '06-09'
indices = []
for i, line in enumerate(lines):
    if 'timeline-date' in line and '06-09' in line:
        # Find the start of this timeline-item block (go backward until we see 'timeline-item>')
        start = i
        while start >= 0 and 'timeline-item' not in lines[start]:
            start -= 1
        if start >= 0:
            indices.append(start)

print(f"Found {len(indices)} timeline-date lines with 06-09")
for idx in indices:
    print(f"  Block starts at line {idx+1}: {lines[idx].rstrip()}")

# Keep the first, remove the second
if len(indices) >= 2:
    # Remove the 2nd block (indices[1])
    start = indices[1]
    # Find matching </div> that closes this timeline-item
    # Count nesting: find the matching closing </div> for the opening one
    depth = 0
    end = start
    while end < len(lines):
        if '<div class="timeline-item">' in lines[end]:
            depth += 1
        if '</div>' in lines[end] and 'timeline-item' not in lines[end]:
            # Only count closing divs that belong to this block
            pass
        # Simpler: just find the next line that is exactly '      </div>' at same indent as opening
        # Actually: the block is:
        #   <div class="timeline-item">   <- start
        #     <div class="timeline-dot">...</div>
        #     <div>...</div>
        #   </div>   <- end (6 spaces + </div>)
        if lines[end].rstrip() == '      </div>':
            # Check if this is the matching one for our block
            # Count: from start to end, # of '<div' vs '</div>'
            snippet = ''.join(lines[start:end+1])
            if snippet.count('<div class="timeline-item">') == snippet.count('</div>\n      <div class="timeline-item">') + 1:
                pass  # not simple
        end += 1
    
    # Actually let's just do manual line-range removal since we know exact lines
    # After reading file: 1st 06-09 block = lines 1309-1316 (1-indexed) = indices[0]=1308
    # 2nd 06-09 block = lines 1372-1379 (1-indexed) = let's find it
    print("Will remove 2nd block manually by line range")
    
# Let's just do: remove lines 1371-1378 (0-indexed) = the duplicate block
# From file read: lines 1372-1379 (1-indexed) contain the duplicate
# 1372: '      <div class="timeline-item">' 
# 1373: '        <div class="timeline-dot red"></div>'
# ...
# 1379: '      </div>'
# 0-indexed: 1371 to 1378 inclusive
dup_start = 1371  # 0-indexed, line 1372
dup_end = 1378    # 0-indexed, line 1379
print(f"Removing lines {dup_start+1} to {dup_end+1} (0-indexed: {dup_start}-{dup_end})")
del lines[dup_start:dup_end+1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done - removed duplicate 06-09 timeline entry")
elif len(indices) == 1:
    print("Only one 06-09 entry found - no duplicate to remove")
else:
    print("No 06-09 entries found - something is wrong")
