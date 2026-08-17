import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

db_path = r'c:\Users\kelvinyye\AppData\Roaming\WorkBuddy\automations\automations.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables:", tables)

# For each table, show schema and sample data
for (tname,) in tables:
    print(f"\n=== {tname} ===")
    cur.execute(f"PRAGMA table_info({tname})")
    cols = cur.fetchall()
    col_names = [c[1] for c in cols]
    print("Columns:", col_names)
    cur.execute(f"SELECT * FROM {tname} LIMIT 20")
    rows = cur.fetchall()
    for row in rows:
        # Truncate long fields
        display = []
        for i, val in enumerate(row):
            s = str(val)
            if len(s) > 200:
                s = s[:200] + '...'
            display.append(f"{col_names[i]}={s}")
        print("  ", " | ".join(display))

conn.close()
