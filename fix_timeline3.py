#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix S7 timeline: remove duplicate 06-09 entry at lines 1372-1379 (1-indexed).
   Read all lines, delete lines 1371-1378 (0-indexed), then write back.
"""
with open('index.html', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print(f"Total lines before: {len(lines)}")
# Duplicate block = lines 1371..1378 (0-indexed) = 1372..1379 (1-indexed)
dup_start = 1371  # 0-indexed, line 1372
dup_end   = 1378  # 0-indexed, line 1379 (inclusive)
print(f"Removing lines {dup_start+1}..{dup_end+1} (0-indexed: {dup_start}..{dup_end})")

del lines[dup_start:dup_end+1]

print(f"Total lines after: {len(lines)}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done - duplicate 06-09 timeline entry removed")
