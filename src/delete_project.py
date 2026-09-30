# src/delete_project.py

import sqlite3
import sys

DB_PATH = "database/xr_observatory.db"


def delete_project(project_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # -------------------------------------------------
    # 检查项目是否存在
    # -------------------------------------------------
    cursor.execute("""
        SELECT title
        FROM projects
        WHERE project_id = ?
    """, (project_id,))

    result = cursor.fetchone()

    if result is None:
        print(f"Project ID {project_id} does not exist.")
        conn.close()
        return

    title = result[0]

    print("=" * 50)
    print("XR Higher Education Observatory")
    print("Delete Project")
    print("=" * 50)
    print(f"Project ID : {project_id}")
    print(f"Title      : {title}")
    print()

    confirm = input("Type YES to delete: ")

    if confirm != "YES":
        print("Cancelled.")
        conn.close()
        return

    # -------------------------------------------------
    # 删除 Evidence
    # -------------------------------------------------
    cursor.execute("""
        DELETE FROM evidence
        WHERE project_id = ?
    """, (project_id,))
    evidence_deleted = cursor.rowcount

    # -------------------------------------------------
    # 删除 Technology
    # -------------------------------------------------
    cursor.execute("""
        DELETE FROM technology
        WHERE project_id = ?
    """, (project_id,))
    technology_deleted = cursor.rowcount

    # -------------------------------------------------
    # 删除 Epistemic
    # -------------------------------------------------
    cursor.execute("""
        DELETE FROM epistemic_profile
        WHERE project_id = ?
    """, (project_id,))
    epistemic_deleted = cursor.rowcount

    # -------------------------------------------------
    # 删除 Accessibility
    # -------------------------------------------------
    cursor.execute("""
        DELETE FROM accessibility
        WHERE project_id = ?
    """, (project_id,))
    accessibility_deleted = cursor.rowcount

    # -------------------------------------------------
    # 删除 Projects
    # -------------------------------------------------
    cursor.execute("""
        DELETE FROM projects
        WHERE project_id = ?
    """, (project_id,))
    project_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    total = (
        project_deleted +
        technology_deleted +
        epistemic_deleted +
        accessibility_deleted +
        evidence_deleted
    )

    print()
    print("-" * 50)
    print("Deletion completed")
    print("-" * 50)
    print(f"Projects table        : {project_deleted}")
    print(f"Technology table      : {technology_deleted}")
    print(f"Epistemic table       : {epistemic_deleted}")
    print(f"Accessibility table   : {accessibility_deleted}")
    print(f"Evidence table        : {evidence_deleted}")
    print("-" * 50)
    print(f"Total records deleted : {total}")
    print("-" * 50)


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    # 方法1：命令行参数
    if len(sys.argv) == 2:
        pid = int(sys.argv[1])

    # 方法2：VS Code直接运行
    else:
        pid = int(input("Enter Project ID to delete: "))

    delete_project(pid)