#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""commit + push（子进程封装，规避 PowerShell/沙箱下 git 直连挂死）"""
import subprocess, os, sys

CWD = r'c:/Users/kelvinyye/WorkBuddy/20260314103829'
ENV = dict(os.environ)
ENV['GIT_TERMINAL_PROMPT'] = '0'
ENV['PYTHONIOENCODING'] = 'utf-8'

def run(args, log):
    p = subprocess.run(args, cwd=CWD, env=ENV, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode('utf-8', 'replace')
    err = p.stderr.decode('utf-8', 'replace')
    print('$ %s -> rc=%d' % (' '.join(args), p.returncode))
    if out.strip():
        print('  stdout:', out.strip()[:800])
    if err.strip():
        print('  stderr:', err.strip()[:800])
    log.append((args, p.returncode, out, err))
    return p.returncode, out, err

log = []
run(['git', 'add', 'index.html', 'gate_check.py', '_update_1013.py', '_push_1013.py'], log)
rc, out, _ = run(['git', 'commit', '-m', 'daily-update-2026-10-13'], log)

if 'nothing to commit' in out or rc != 0:
    print('COMMIT_SKIPPED_OR_FAILED rc=%d' % rc)

rc, _, _ = run(['git', '-c', 'credential.helper=', '-c', 'credential.helper=store',
                'push', 'origin', 'main'], log)
print('PUSH_RC=%d' % rc)

# 落地校验
lrc, lout, _ = run(['git', 'ls-remote', 'origin', 'main'], log)
hrc, hout, _ = run(['git', 'rev-parse', 'HEAD'], log)
remote = lout.split()[0] if lout.split() else ''
head = hout.strip()
print('HEAD=%s' % head)
print('REMOTE=%s' % remote)
print('LANDING=%s' % ('PUSH_VERIFIED_OK' if (remote and remote == head) else 'PUSH_FAILED'))
