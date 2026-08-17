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

# Check automation details
print("=" * 60)
print("AUTOMATION TASKS")
print("=" * 60)
cur.execute("SELECT id, name, status, model_id, next_run_at, last_run_at, cwds, rrule FROM automations")
for row in cur.fetchall():
    print(f"\nID: {row[0]}")
    print(f"  Name: {row[1]}")
    print(f"  Status: {row[2]}")
    print(f"  Model: {row[3]}")
    print(f"  Next Run: {ts_to_str(row[4])}")
    print(f"  Last Run: {ts_to_str(row[5])}")
    print(f"  CWDs: {row[6]}")
    print(f"  RRule: {row[7]}")

# Check recent runs for git and automation (fallback)
print("\n" + "=" * 60)
print("RECENT RUNS FOR 'git' and 'automation'")
print("=" * 60)
cur.execute("""
    SELECT thread_id, automation_id, status, source_cwd, result_success, created_at, updated_at
    FROM automation_runs 
    WHERE automation_id IN ('git', 'automation')
    ORDER BY created_at DESC
    LIMIT 10
""")
for row in cur.fetchall():
    print(f"\n  Thread: {row[0][:50]}...")
    print(f"  Automation: {row[1]}")
    print(f"  Status: {row[2]}")
    print(f"  Source CWD: {row[3]}")
    print(f"  Success: {row[4]}")
    print(f"  Created: {ts_to_str(row[5])}")
    print(f"  Updated: {ts_to_str(row[6])}")

conn.close()
