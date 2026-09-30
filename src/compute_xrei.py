import sqlite3
import pandas as pd


def compute_and_update_xrei(
    excel_path="data/raw/XR_Observatory.xlsx",
    db_path="database/xr_observatory.db",
):
    """从Excel读取Epistemic数据，计算XREI得分，并同步写入SQLite数据库。"""
    print("🔄 开始计算 XREI 指数...")

    # 1. 从 Excel 中读取对应的工作表
    try:
        # 对齐 update_excel.py 中的标签页名称 'Epistemic'
        df_epistemic = pd.read_excel(excel_path, sheet_name="Epistemic")
    except Exception as e:
        print(f"❌ 读取 Excel 失败，请检查 Sheet 名称或路径: {e}")
        return

    # 2. 核心算法：直接映射得分 (0/1) 并计算总分
    df_xrei = pd.DataFrame()
    df_xrei["project_id"] = df_epistemic["project_id"]

    # 映射得分
    df_xrei["spatial_score"] = df_epistemic["spatial_navigation"].astype(int)
    df_xrei["embodied_score"] = df_epistemic["embodied_interaction"].astype(int)
    df_xrei["perspective_score"] = df_epistemic["multi_perspective"].astype(int)
    df_xrei["knowledge_score"] = df_epistemic[
        "user_generated_content"
    ].astype(int)
    df_xrei["collaboration_score"] = df_epistemic[
        "collaborative_space"
    ].astype(int)

    # 计算 0-5 分的总分
    df_xrei["xrei_score"] = (
        df_xrei["spatial_score"]
        + df_xrei["embodied_score"]
        + df_xrei["perspective_score"]
        + df_xrei["knowledge_score"]
        + df_xrei["collaboration_score"]
    )

    # 3. 将计算结果写入 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 💡 核心修复：根据学术设计书规范，此处将结果写入或替换至 table_3b_xrei 表
        # 如果你的 create_database.py 中表名叫其他名字，请在此处替换
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS table_3b_xrei (
                project_id INTEGER PRIMARY KEY,
                spatial_score INTEGER,
                embodied_score INTEGER,
                perspective_score INTEGER,
                knowledge_score INTEGER,
                collaboration_score INTEGER,
                xrei_score INTEGER
            )
        """)

        # 使用 INSERT OR REPLACE 确保每次运行都是最新计算出的得分
        insert_query = """
            INSERT OR REPLACE INTO table_3b_xrei (
                project_id, spatial_score, embodied_score, 
                perspective_score, knowledge_score, collaboration_score, xrei_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        data_to_insert = list(df_xrei.itertuples(index=False, name=None))
        cursor.executemany(insert_query, data_to_insert)

        conn.commit()
        print(
            f"✅ XREI 计算完成！成功同步 {len(data_to_insert)} 个项目的评分至数据库 table_3b_xrei。"
        )

    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ 数据库写入失败: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    compute_and_update_xrei()