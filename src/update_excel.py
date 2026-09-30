import sqlite3
import pandas as pd
import compute_xrei

DB = "database/xr_observatory.db"
EXCEL = "data/raw/XR_Observatory.xlsx"

# ----------------------------
# Read Excel
# ----------------------------
projects = pd.read_excel(EXCEL, sheet_name="Projects")
technology = pd.read_excel(EXCEL, sheet_name="Technology")
epistemic = pd.read_excel(EXCEL, sheet_name="Epistemic")
accessibility = pd.read_excel(EXCEL, sheet_name="Accessibility")
evidence = pd.read_excel(EXCEL, sheet_name="Evidence")

conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Existing IDs
cursor.execute("SELECT project_id FROM projects")
db_ids = {r[0] for r in cursor.fetchall()}

excel_ids = set(projects.project_id)

inserted = 0
updated = 0

# =====================================================
# Projects
# =====================================================
for _, row in projects.iterrows():
    pid = int(row.project_id)
    if pid in db_ids:
        cursor.execute("""
        UPDATE projects SET
            title=?, inhalt=?, university=?, country=?, city=?,
            faculty=?, discipline=?, project_type=?, funding=?, start_year=?, website=?
        WHERE project_id=?
        """, (row.title, row.inhalt, row.university, row.country, row.city,
              row.faculty, row.discipline, row.project_type, row.funding, row.start_year, row.website, pid))
        updated += 1
    else:
        cursor.execute("""
        INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (pid, row.title, row.inhalt, row.university, row.country, row.city,
              row.faculty, row.discipline, row.project_type, row.funding, row.start_year, row.website))
        inserted += 1

# =====================================================
# Helper function
# =====================================================
def sync_one_to_one(df, table, columns):
    for _, row in df.iterrows():
        pid = int(row.project_id)
        cursor.execute(f"SELECT project_id FROM {table} WHERE project_id=?", (pid,))
        exists = cursor.fetchone()
        values = [row[c] for c in columns]
        if exists:
            set_clause = ",".join([f"{c}=?" for c in columns])
            cursor.execute(f"UPDATE {table} SET {set_clause} WHERE project_id=?", values + [pid])
        else:
            q = ",".join(["?"] * (len(columns) + 1))
            cursor.execute(f"INSERT INTO {table} VALUES({q})", [pid] + values)

sync_one_to_one(technology, "technology", ["xr_type", "platform", "software_engine", "data_foundation", "openness", "interoperability", "hardware_dependency", "technical_features"])
sync_one_to_one(epistemic, "epistemic_profile", ["primary_function", "spatial_navigation", "embodied_interaction", "multi_perspective", "user_generated_content", "collaborative_space", "notes"])
sync_one_to_one(accessibility, "accessibility", ["multilingual_support", "controller_free", "cybersickness_mitigation", "remote_access", "cultural_inclusivity", "notes"])

# =====================================================
# Evidence 
# =====================================================
evidence_added = 0
evidence_removed = 0

for pid in excel_ids:
    current_project_deleted = 0
    current_project_inserted = 0

    excel_rows = evidence[evidence["project_id"] == pid]
    
    cursor.execute("SELECT evidence_id, source_type, source_title, url, date_accessed FROM evidence WHERE project_id = ?", (int(pid),))
    db_rows = cursor.fetchall()
    db_records = {r[0]: (r[1] or "", r[2] or "", r[3] or "", r[4] or "") for r in db_rows}

    excel_records = {}
    for _, row in excel_rows.iterrows():
        eid = int(row.evidence_id) 
        excel_records[eid] = (
            "" if pd.isna(row.source_type) else str(row.source_type),
            "" if pd.isna(row.source_title) else str(row.source_title),
            "" if pd.isna(row.url) else str(row.url),
            "" if pd.isna(row.date_accessed) else str(row.date_accessed)
        )

    # 1. 删除 Excel 中不存在的旧 ID
    for eid in list(db_records.keys()):
        if eid not in excel_records:
            cursor.execute("DELETE FROM evidence WHERE evidence_id = ?", (eid,))
            evidence_removed += 1
            current_project_deleted += 1

    # 2. 插入或强制更新数据 (采用 INSERT OR REPLACE 彻底击碎 SQLite 自增锁)
    for eid, record in excel_records.items():
        if eid not in db_records:
            cursor.execute("""
                INSERT OR REPLACE INTO evidence (evidence_id, project_id, source_type, source_title, url, date_accessed)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (eid, int(pid), record[0], record[1], record[2], None if record[3] == "" else record[3]))
            evidence_added += 1
            current_project_inserted += 1
        else:
            if record != db_records[eid]:
                cursor.execute("""
                    UPDATE evidence SET source_type=?, source_title=?, url=?, date_accessed=? WHERE evidence_id=?
                """, (record[0], record[1], record[2], None if record[3] == "" else record[3], eid))

    if current_project_inserted > 0 or current_project_deleted > 0:
        print(f"Project {pid} Evidence  +{current_project_inserted}  -{current_project_deleted}")

conn.commit()
conn.close()
compute_xrei.compute_and_update_xrei()

print("=" * 45)
print("XR Higher Education Observatory")
print("=" * 45)
print(f"Inserted projects : {inserted}")
print(f"Updated projects  : {updated}")
if evidence_added > 0: print(f"Evidence added    : {evidence_added}")
if evidence_removed > 0: print(f"Evidence removed  : {evidence_removed}")
print("=" * 45)