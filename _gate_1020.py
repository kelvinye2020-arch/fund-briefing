# -*- coding: utf-8 -*-
import subprocess, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
CWD = r'c:/Users/kelvinyye/WorkBuddy/20260314103829'
env = {'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
r = subprocess.run([r'C:\Users\kelvinyye\.workbuddy\binaries\python\versions\3.13.12\python.exe',
                    'gate_check.py'], cwd=CWD, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT, env=None, timeout=120)
out = r.stdout.decode('utf-8', errors='replace')
open(CWD + r'/_gate_1020.txt', 'w', encoding='utf-8').write('RC=%d\n' % r.returncode + out)
print('RC=', r.returncode)
print(out)
