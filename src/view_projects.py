# src/view_projects.py

import sqlite3

DB_PATH = "database/xr_observatory.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM projects
ORDER BY project_id
""")

projects = cursor.fetchall()

if len(projects) == 0:
    print("Database is empty.")
    conn.close()
    exit()

print("=" * 80)
print("XR Higher Education Observatory")
print("Complete Projects Viewer")
print("=" * 80)

for p in projects:
    pid = p["project_id"]

    print()
    print("=" * 80)
    print(f"PROJECT ID : {pid}")
    print(f"TITLE      : {p['title']}")
    print("=" * 80)

    # [1] PROJECTS
    print("\n[1] PROJECTS")
    for key in p.keys():
        print(f"{key:25}: {p[key]}")

    # [2] TECHNOLOGY
    cursor.execute("SELECT * FROM technology WHERE project_id=?", (pid,))
    tech = cursor.fetchone()
    print("\n[2] TECHNOLOGY")
    if tech:
        for key in tech.keys():
            if key != "project_id": print(f"{key:25}: {tech[key]}")
    else:
        print("No record")

    # [3] EPISTEMIC PROFILE
    cursor.execute("SELECT * FROM epistemic_profile WHERE project_id=?", (pid,))
    epi = cursor.fetchone()
    print("\n[3] EPISTEMIC PROFILE")
    if epi:
        for key in epi.keys():
            if key != "project_id": print(f"{key:25}: {epi[key]}")
    else:
        print("No record")

    # [4] ACCESSIBILITY
    cursor.execute("SELECT * FROM accessibility WHERE project_id=?", (pid,))
    acc = cursor.fetchone()
    print("\n[4] ACCESSIBILITY")
    if acc:
        for key in acc.keys():
            if key != "project_id": print(f"{key:25}: {acc[key]}")
    else:
        print("No record")

    # [5] EVIDENCE (已修复：获取并打印数据库中真正真实的唯一 ID)
    cursor.execute("""
    SELECT evidence_id,
           source_type,
           source_title,
           url,
           date_accessed
    FROM evidence
    WHERE project_id=?
    ORDER BY evidence_id ASC
    """, (pid,))

    evidences = cursor.fetchall()

    print("\n[5] EVIDENCE")

    if len(evidences) == 0:
        print("No evidence")
    else:
        # 这里直接循环遍历，剔除之前错误的假序号 idx
        for ev in evidences:
            # 关键修改：直接利用数据库内读取出来的真实 id 打印
            print(f"\nEvidence {ev['evidence_id']}")

            print(f"  Type : {ev['source_type']}")
            print(f"  Title: {ev['source_title']}")
            print(f"  URL  : {ev['url']}")
            print(f"  Date : {ev['date_accessed']}")

print()
print("=" * 80)
print(f"Total Projects : {len(projects)}")
print("=" * 80)

conn.close()