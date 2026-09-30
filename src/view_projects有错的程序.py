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

    # --------------------------------------------------
    # Projects
    # --------------------------------------------------

    print("\n[1] PROJECTS")

    for key in p.keys():
        print(f"{key:25}: {p[key]}")

    # --------------------------------------------------
    # Technology
    # --------------------------------------------------

    cursor.execute("""
    SELECT *
    FROM technology
    WHERE project_id=?
    """, (pid,))

    tech = cursor.fetchone()

    print("\n[2] TECHNOLOGY")

    if tech:
        for key in tech.keys():
            if key != "project_id":
                print(f"{key:25}: {tech[key]}")
    else:
        print("No record")

    # --------------------------------------------------
    # Epistemic
    # --------------------------------------------------

    cursor.execute("""
    SELECT *
    FROM epistemic_profile
    WHERE project_id=?
    """, (pid,))

    epi = cursor.fetchone()

    print("\n[3] EPISTEMIC PROFILE")

    if epi:
        for key in epi.keys():
            if key != "project_id":
                print(f"{key:25}: {epi[key]}")
    else:
        print("No record")

    # --------------------------------------------------
    # Accessibility
    # --------------------------------------------------

    cursor.execute("""
    SELECT *
    FROM accessibility
    WHERE project_id=?
    """, (pid,))

    acc = cursor.fetchone()

    print("\n[4] ACCESSIBILITY")

    if acc:
        for key in acc.keys():
            if key != "project_id":
                print(f"{key:25}: {acc[key]}")
    else:
        print("No record")

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    cursor.execute("""
    SELECT source_type,
           source_title,
           url,
           date_accessed
    FROM evidence
    WHERE project_id=?
    ORDER BY evidence_id
    """, (pid,))

    evidences = cursor.fetchall()

    print("\n[5] EVIDENCE")

    if len(evidences) == 0:
        print("No evidence")
    else:

        for i, ev in enumerate(evidences, start=1):

            print(f"\nEvidence {i}")

            print(f"  Type : {ev['source_type']}")
            print(f"  Title: {ev['source_title']}")
            print(f"  URL  : {ev['url']}")
            print(f"  Date : {ev['date_accessed']}")

print()
print("=" * 80)
print(f"Total Projects : {len(projects)}")
print("=" * 80)

conn.close()