# src/create_database.py

import sqlite3
from pathlib import Path

# 建立 database 文件夹
Path("database").mkdir(exist_ok=True)
DB_PATH = "database/xr_observatory.db"
# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# 开启 Foreign Key
cursor.execute("PRAGMA foreign_keys = ON")

# =====================================
# Table 1 Projects
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects(
    project_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    inhalt TEXT,
    university TEXT,
    country TEXT,
    city TEXT,
    faculty TEXT,
    discipline TEXT,
    project_type TEXT,
    funding TEXT,
    start_year INTEGER,
    website TEXT
)
""")

# =====================================
# Table 2 Technology
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS technology(
    project_id INTEGER PRIMARY KEY,
    xr_type TEXT,
    platform TEXT,
    software_engine TEXT,
    data_foundation TEXT,
    openness TEXT,
    interoperability TEXT,
    hardware_dependency TEXT,
    technical_features TEXT,
    FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
)
""")

# =====================================
# Table 3 Epistemic Profile
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS epistemic_profile(
    project_id INTEGER PRIMARY KEY,
    primary_function TEXT,
    spatial_navigation BOOLEAN,
    embodied_interaction BOOLEAN,
    multi_perspective BOOLEAN,
    user_generated_content BOOLEAN,
    collaborative_space BOOLEAN,
    notes TEXT,
    FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
)
""")

# =====================================
# Table 4 Accessibility
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS accessibility(
    project_id INTEGER PRIMARY KEY,
    multilingual_support BOOLEAN,
    controller_free BOOLEAN,
    cybersickness_mitigation BOOLEAN,
    remote_access BOOLEAN,
    cultural_inclusivity BOOLEAN,
    notes TEXT,
    FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
)
""")

# =====================================
# Table 5 Evidence (1:N)
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS evidence(
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    source_type TEXT,
    source_title TEXT,
    url TEXT,
    date_accessed TEXT,
    FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
    
    UNIQUE(project_id, source_title, url)
)
""")

conn.commit()
conn.close()

print("XR Observatory database created successfully!")