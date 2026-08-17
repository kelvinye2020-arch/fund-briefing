#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix S7 timeline: remove duplicate 06-09 entry (lines 1372-1379 approx),
    then ensure only one 06-09 entry exists.
    Actually: the correct entry is at lines 1310-1316 (the one we updated).
    The duplicate is at lines 1372-1379 (the one incorrectly added).
    We need to remove the duplicate block at ~1372-1379.
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The duplicate entry starts with: 
#      <div class="timeline-item">\n        <div class="timeline-dot red"></div>\n        <div>\n          <div class="timeline-date">2026-06-09
# and ends with: </div>\n      </div>\n (two lines after timeline-desc)

# Strategy: find all timeline-date blocks with 2026-06-09, keep the first, remove subsequent ones
pattern = r'(<div class="timeline-item">\s*<div class="timeline-dot red"></div>\s*<div>\s*<div class="timeline-date">2026-06-09\([^<]*</div>\s*<div class="timeline-title">[^<]*</div>\s*<div class="timeline-desc">[^<]*</div>\s*</div>\s*</div>)'

matches = list(re.finditer(pattern, content))
print(f"Found {len(matches)} matching 06-09 entries")

if len(matches) > 1:
    # Remove the second and later matches
    # Work from last to first to preserve offsets
    for m in reversed(matches[1:]):
        content = content[:m.start()] + '\n' + content[m.end():]
        print(f"Removed duplicate at offset {m.start()}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done - removed duplicate 06-09 entries")
else:
    print("No duplicates found or only one entry exists")
