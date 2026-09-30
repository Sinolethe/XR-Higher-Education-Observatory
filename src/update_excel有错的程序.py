import sqlite3
import pandas as pd

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
            title=?,
            inhalt=?,
            university=?,
            country=?,
            city=?,
            faculty=?,
            discipline=?,
            project_type=?,
            funding=?,
            start_year=?,
            website=?
        WHERE project_id=?
        """, (
            row.title,
            row.inhalt,
            row.university,
            row.country,
            row.city,
            row.faculty,
            row.discipline,
            row.project_type,
            row.funding,
            row.start_year,
            row.website,
            pid
        ))

        updated += 1

    else:

        cursor.execute("""
        INSERT INTO projects VALUES(
        ?,?,?,?,?,?,?,?,?,?,?,?
        )
        """, (
            pid,
            row.title,
            row.inhalt,
            row.university,
            row.country,
            row.city,
            row.faculty,
            row.discipline,
            row.project_type,
            row.funding,
            row.start_year,
            row.website
        ))

        inserted += 1

# =====================================================
# Helper function
# =====================================================

def sync_one_to_one(df, table, columns):

    for _, row in df.iterrows():

        pid = int(row.project_id)

        cursor.execute(
            f"SELECT project_id FROM {table} WHERE project_id=?",
            (pid,)
        )

        exists = cursor.fetchone()

        values = [row[c] for c in columns]

        if exists:

            set_clause = ",".join(
                [f"{c}=?" for c in columns]
            )

            cursor.execute(
                f"""
                UPDATE {table}
                SET {set_clause}
                WHERE project_id=?
                """,
                values + [pid]
            )

        else:

            q = ",".join(["?"] * (len(columns) + 1))

            cursor.execute(
                f"""
                INSERT INTO {table}
                VALUES({q})
                """,
                [pid] + values
            )

# =====================================================
# Technology
# =====================================================

sync_one_to_one(
    technology,
    "technology",
    [
        "xr_type",
        "platform",
        "software_engine",
        "data_foundation",
        "openness",
        "interoperability",
        "hardware_dependency",
        "technical_features"
    ]
)

# =====================================================
# Epistemic
# =====================================================

sync_one_to_one(
    epistemic,
    "epistemic_profile",
    [
        "primary_function",
        "spatial_navigation",
        "embodied_interaction",
        "multi_perspective",
        "user_generated_content",
        "collaborative_space",
        "notes"
    ]
)

# =====================================================
# Accessibility
# =====================================================

sync_one_to_one(
    accessibility,
    "accessibility",
    [
        "multilingual_support",
        "controller_free",
        "cybersickness_mitigation",
        "remote_access",
        "cultural_inclusivity",
        "notes"
    ]
)

evidence_added = 0
evidence_removed = 0

for pid in excel_ids:

    # ---------- Excel 中属于这个项目 ----------
    excel_rows = evidence[
        evidence["project_id"] == pid
    ]

    # ---------- 数据库已有 ----------
    cursor.execute("""
        SELECT source_type,
               source_title,
               url,
               date_accessed
        FROM evidence
        WHERE project_id = ?
    """, (int(pid),))

    db_rows = cursor.fetchall()

    db_records = [
        (
            r[0] or "",
            r[1] or "",
            r[2] or "",
            r[3] or ""
        )
        for r in db_rows
    ]

    excel_records = []

    for _, row in excel_rows.iterrows():

        excel_records.append((
            "" if pd.isna(row.source_type) else str(row.source_type),
            "" if pd.isna(row.source_title) else str(row.source_title),
            "" if pd.isna(row.url) else str(row.url),
            "" if pd.isna(row.date_accessed) else str(row.date_accessed)
        ))

    # ---------- 删除数据库中不存在于 Excel 的 ----------
    for record in db_records:

        if record not in excel_records:

            cursor.execute("""
                DELETE FROM evidence
                WHERE project_id=?
                  AND IFNULL(source_type,'')=?
                  AND IFNULL(source_title,'')=?
                  AND IFNULL(url,'')=?
                  AND IFNULL(date_accessed,'')=?
            """, (int(pid), *record))

            evidence_removed += cursor.rowcount

    # ---------- 新增 Excel 中不存在于数据库的 ----------
    for record in excel_records:

        if record not in db_records:

            cursor.execute("""
                INSERT INTO evidence(
                    project_id,
                    source_type,
                    source_title,
                    url,
                    date_accessed
                )
                VALUES(?,?,?,?,?)
            """, (
                int(pid),
                record[0],
                record[1],
                record[2],
                None if record[3] == "" else record[3]
            ))

            evidence_added += 1

    # ---------- Per project log ----------
    if len(to_insert) > 0 or len(to_delete) > 0:

        msg = f"Project {pid} Evidence"

        if len(to_insert) > 0:
            msg += f"  +{len(to_insert)}"

        if len(to_delete) > 0:
            msg += f"  -{len(to_delete)}"

        print(msg)

conn.commit()
conn.close()

print("=" * 45)
print("XR Higher Education Observatory")
print("=" * 45)
print(f"Inserted projects : {inserted}")
print(f"Updated projects  : {updated}")

if evidence_added > 0:
    print(f"Evidence added    : {evidence_added}")

if evidence_removed > 0:
    print(f"Evidence removed  : {evidence_removed}")

print("=" * 45)