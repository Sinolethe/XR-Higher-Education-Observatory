import sqlite3
import pandas as pd

DB = "database/xr_observatory.db"
conn = sqlite3.connect(DB)

df = pd.read_sql_query("SELECT * FROM table_3b_xrei", conn)

print("=== 数据库中的 table_3b_xrei 数值 ===")
# 💡 使用 to_string(index=False) 完美去掉左侧的 0
print(df.to_string(index=False))

conn.close()