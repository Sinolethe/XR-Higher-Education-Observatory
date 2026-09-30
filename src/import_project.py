# src/import_project.py
import sys
import os
# 将当前文件的上一级目录（即项目根目录）加入到 Python 搜索路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib

from database import get_connection
from utils import validate


# ============================
# 动态读取项目
# ============================

def load_project(project_name):

    module = importlib.import_module(
        f"data.projects.{project_name}"
    )

    return module.project


# ============================
# 导入数据库
# ============================

def import_project(data):

    conn = get_connection()
    cursor = conn.cursor()

    p = data["project"]

    # ---------- 是否已存在 ----------
    cursor.execute(
        "SELECT project_id FROM projects WHERE project_id=?",
        (p["project_id"],)
    )

    if cursor.fetchone():
        print(f'Project already exists: {p["title"]}')
        conn.close()
        return

    # ---------- Projects ----------
    cursor.execute("""
        INSERT INTO projects VALUES(
        ?,?,?,?,?,?,?,?,?,?,?,?
        )
    """, (

        p["project_id"],
        p["title"],
        p["inhalt"],
        p["university"],
        p["country"],
        p["city"],
        p["faculty"],
        p["discipline"],
        p["project_type"],
        p["funding"],
        p["start_year"],
        p["website"]

    ))

    # ---------- Technology ----------

    t = data["technology"]

    cursor.execute("""
        INSERT INTO technology(
            project_id,
            xr_type,
            platform,
            software_engine,
            data_foundation,
            openness,
            interoperability,
            hardware_dependency,
            technical_features
        )
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (

        p["project_id"],
        t["xr_type"],
        t["platform"],
        t["software_engine"],
        t["data_foundation"],
        t["openness"],
        t["interoperability"],
        t["hardware_dependency"],
        t["technical_features"]

    ))

    # ---------- Epistemic ----------

    e = data["epistemic"]

    cursor.execute("""
        INSERT INTO epistemic_profile(
            project_id,
            primary_function,
            spatial_navigation,
            embodied_interaction,
            multi_perspective,
            user_generated_content,
            collaborative_space,
            notes
        )
        VALUES(?,?,?,?,?,?,?,?)
    """, (

        p["project_id"],
        e["primary_function"],
        e["spatial_navigation"],
        e["embodied_interaction"],
        e["multi_perspective"],
        e["user_generated_content"],
        e["collaborative_space"],
        e["notes"]

    ))

    # ---------- Accessibility ----------

    a = data["accessibility"]

    cursor.execute("""
        INSERT INTO accessibility(
            project_id,
            multilingual_support,
            controller_free,
            cybersickness_mitigation,
            remote_access,
            cultural_inclusivity,
            accessibility_features,
            notes
        )
        VALUES(?,?,?,?,?,?,?,?)
    """, (

        p["project_id"],
        a["multilingual_support"],
        a["controller_free"],
        a["cybersickness_mitigation"],
        a["remote_access"],
        a["cultural_inclusivity"],
        a["accessibility_features"],
        a["notes"]

    ))

    # ---------- Evidence ----------

    v = data["evidence"]

    cursor.execute("""
        INSERT INTO evidence(
            project_id,
            source_type,
            source_title,
            quotation,
            url,
            date_accessed
        )
        VALUES(?,?,?,?,?,?)
    """, (

        p["project_id"],
        v["source_type"],
        v["source_title"],
        v["quotation"],
        v["url"],
        v["date_accessed"]

    ))

    conn.commit()
    conn.close()

    print(f'Imported: {p["title"]}')


# ============================
# 主程序
# ============================

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python src/import_project.py etardis")
        exit()

    project_name = sys.argv[1]

    project = load_project(project_name)

    validate(project)

    import_project(project)
