# src/import_excel.py, 用  python "d:\0XR_Higher_Education_Observatory\src\import_excel.py" 才能正确运行

import sqlite3
import pandas as pd

DB_PATH = "database/xr_observatory.db"
EXCEL_PATH = "data/raw/XR_Observatory.xlsx"


# =====================================================
# 读取 Excel
# =====================================================

projects = pd.read_excel(EXCEL_PATH, sheet_name="Projects")
technology = pd.read_excel(EXCEL_PATH, sheet_name="Technology")
epistemic = pd.read_excel(EXCEL_PATH, sheet_name="Epistemic")
accessibility = pd.read_excel(EXCEL_PATH, sheet_name="Accessibility")
evidence = pd.read_excel(EXCEL_PATH, sheet_name="Evidence")


# =====================================================
# 数据库连接
# =====================================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")


# =====================================================
# 查询数据库已有 project_id
# =====================================================

cursor.execute("SELECT project_id FROM projects")

existing_ids = {row[0] for row in cursor.fetchall()}


# =====================================================
# 找出 Excel 中的新项目
# =====================================================

new_projects = projects[
    ~projects["project_id"].isin(existing_ids)
]

new_ids = set(new_projects["project_id"])

print("=" * 45)
print("XR Higher Education Observatory")
print("=" * 45)
print(f"Existing projects : {len(existing_ids)}")
print(f"New projects      : {len(new_ids)}")
print()


# 如果没有新项目
if len(new_ids) == 0:
    print("No new projects found.")
    conn.close()
    exit()


# =====================================================
# 过滤其他四张表
# =====================================================

technology = technology[
    technology["project_id"].isin(new_ids)
]

epistemic = epistemic[
    epistemic["project_id"].isin(new_ids)
]

accessibility = accessibility[
    accessibility["project_id"].isin(new_ids)
]

evidence = evidence[
    evidence["project_id"].isin(new_ids)
]


# =====================================================
# 导入 Projects
# =====================================================

for _, row in new_projects.iterrows():

    cursor.execute("""
    INSERT INTO projects VALUES(
        ?,?,?,?,?,?,?,?,?,?,?,?
    )
    """, (
        int(row.project_id),
        row.title,
        row.inhalt,
        row.university,
        row.country,
        row.city,
        row.faculty,
        row.discipline,
        row.project_type,
        row.funding,
        None if pd.isna(row.start_year) else int(row.start_year),
        row.website
    ))

    print(f"+ {row.title}")


# =====================================================
# 导入 Technology
# =====================================================

for _, row in technology.iterrows():

    cursor.execute("""
    INSERT INTO technology VALUES(
        ?,?,?,?,?,?,?,?,?
    )
    """, (
        int(row.project_id),
        row.xr_type,
        row.platform,
        row.software_engine,
        row.data_foundation,
        row.openness,
        row.interoperability,
        row.hardware_dependency,
        row.technical_features
    ))


# =====================================================
# 导入 Epistemic
# =====================================================

for _, row in epistemic.iterrows():

    cursor.execute("""
    INSERT INTO epistemic_profile VALUES(
        ?,?,?,?,?,?,?,?
    )
    """, (
        int(row.project_id),
        row.primary_function,
        row.spatial_navigation,
        row.embodied_interaction,
        row.multi_perspective,
        row.user_generated_content,
        row.collaborative_space,
        row.notes
    ))


# =====================================================
# 导入 Accessibility
# =====================================================

for _, row in accessibility.iterrows():

    cursor.execute("""
    INSERT INTO accessibility VALUES(
        ?,?,?,?,?,?,?
    )
    """, (
        int(row.project_id),
        row.multilingual_support,
        row.controller_free,
        row.cybersickness_mitigation,
        row.remote_access,
        row.cultural_inclusivity,
        row.notes
    ))


# =====================================================
# 导入 Evidence（1 : N）
# =====================================================

evidence_count = 0

for _, row in evidence.iterrows():
    date_str = None if pd.isna(row.date_accessed) else str(row.date_accessed)[:10]
    # 如果日期不是空的，将其转换为字符串格式 (YYYY-MM-DD)
    
    cursor.execute("""
    INSERT OR IGNORE INTO evidence(
        project_id,
        source_type,
        source_title,
        url,
        date_accessed
    )
    VALUES(?,?,?,?,?)
    """, (
        int(row.project_id),
        row.source_type,
        row.source_title,
        row.url,
        date_str  # 使用转换后的字符串代替原本的 Timestamp 对象
    ))

    evidence_count += cursor.rowcount


# =====================================================
# 完成
# =====================================================

conn.commit()
conn.close()

print()
print("-" * 45)
print(f"Projects imported       : {len(new_projects)}")
print(f"Technology records      : {len(technology)}")
print(f"Epistemic records       : {len(epistemic)}")
print(f"Accessibility records   : {len(accessibility)}")
print(f"Evidence records        : {evidence_count}")
print("-" * 45)
print("Import completed successfully.")