# -*- coding: utf-8 -*-
import subprocess, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
CWD = r'c:/Users/kelvinyye/WorkBuddy/20260314103829'
r = subprocess.run(['git', 'show', '0b55020:index.html'], cwd=CWD,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
s = r.stdout.decode('utf-8', errors='replace')
i = s.find('class="action-box"')
print('idx', i)
seg = s[i-900:i+1600]
open(r'c:/Users/kelvinyye/WorkBuddy/20260314103829/_ax_1020.txt', 'w', encoding='utf-8').write(seg)
print('ok')
