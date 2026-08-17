import sqlite3, sys, io, json
from datetime import datetime, timezone, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

db_path = r'c:\Users\kelvinyye\AppData\Roaming\WorkBuddy\automations\automations.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

tz_cn = timezone(timedelta(hours=8))

def ts_to_str(ts):
    if ts is None:
        return "None"
    try:
        return datetime.fromtimestamp(ts/1000, tz=tz_cn).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)

# 1. All three tasks full info
print("=" * 70)
print("TASK CONFIGS")
print("=" * 70)
cur.execute("SELECT id, name, status, model_id, next_run_at, last_run_at, cwds, rrule, prompt FROM automations WHERE id IN ('git','automation','automation-8')")
for r in cur.fetchall():
    print(f"\n{'='*50}")
    print(f"ID: {r[0]}")
    print(f"  Name: {r[1]}")
    print(f"  Status: {r[2]}")
    print(f"  Model: {r[3]}")
    print(f"  Next Run: {ts_to_str(r[4])}")
    print(f"  Last Run: {ts_to_str(r[5])}")
    print(f"  CWDs: {r[6]}")
    print(f"  RRule: {r[7]}")
    print(f"  Prompt (first 500 chars):")
    prompt = r[8] or ""
    print(f"    {prompt[:500]}")

# 2. Recent runs for git task - last 5
print("\n" + "=" * 70)
print("RECENT RUNS FOR 'git' (last 5)")
print("=" * 70)
cur.execute("""
    SELECT thread_id, status, source_cwd, result_success, created_at, updated_at
    FROM automation_runs 
    WHERE automation_id = 'git'
    ORDER BY created_at DESC
    LIMIT 5
""")
for row in cur.fetchall():
    print(f"\n  Thread: {row[0]}")
    print(f"  Status: {row[1]}")
    print(f"  Source CWD: {row[2]}")
    print(f"  Success: {row[3]}")
    print(f"  Created: {ts_to_str(row[4])}")
    print(f"  Updated: {ts_to_str(row[5])}")

# 3. Recent runs for automation-8
print("\n" + "=" * 70)
print("RECENT RUNS FOR 'automation-8'")
print("=" * 70)
cur.execute("""
    SELECT thread_id, status, source_cwd, result_success, created_at, updated_at
    FROM automation_runs 
    WHERE automation_id = 'automation-8'
    ORDER BY created_at DESC
    LIMIT 5
""")
rows = cur.fetchall()
if not rows:
    print("  (No runs yet)")
else:
    for row in rows:
        print(f"\n  Thread: {row[0]}")
        print(f"  Status: {row[1]}")
        print(f"  Source CWD: {row[2]}")
        print(f"  Success: {row[3]}")
        print(f"  Created: {ts_to_str(row[4])}")

# 4. Check automation table columns
print("\n" + "=" * 70)
print("TABLE SCHEMA: automation_runs")
print("=" * 70)
cur.execute("PRAGMA table_info(automation_runs)")
for col in cur.fetchall():
    print(f"  {col}")

conn.close()
