import os
import sqlite3
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. 页面基本配置
# ==============================================================================
st.set_page_config(
    page_title="XR Higher Education Observatory",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 💡 核心修改：因为现在代码在 app/ 目录下，需要通过 ../ 找到外层的 database 文件夹
DB_PATH = "database/xr_observatory.db"


# ==============================================================================
# 2. 数据库读取函数 (使用缓存优化性能)
# ==============================================================================
@st.cache_data
def load_observatory_data():
    """连接数据库，利用 SQL JOIN 拼装项目基础元数据、技术基础以及 XREI 得分"""
    if not os.path.exists(DB_PATH):
        st.error(
            f"❌ 找不到数据库文件：'{DB_PATH}'。请确保在项目根目录下先运行了 `src/update_excel.py`。"
        )
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)

    # 编写多表联查 SQL 语句
    query = """
        SELECT 
            p.project_id AS [Project ID],
            p.title AS [Project Title],
            p.university AS [University],
            p.country AS [Country],
            p.city AS [City],
            p.discipline AS [Discipline],
            p.project_type AS [Type],
            t.xr_type AS [XR Type],
            t.platform AS [Platform],
            t.software_engine AS [Engine],
            x.spatial_score AS [Spatial],
            x.embodied_score AS [Embodied],
            x.perspective_score AS [Perspective],
            x.knowledge_score AS [Knowledge],
            x.collaboration_score AS [Collaboration],
            x.xrei_score AS [XREI Score]
        FROM projects p
        LEFT JOIN technology t ON p.project_id = t.project_id
        LEFT JOIN table_3b_xrei x ON p.project_id = x.project_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# 加载全局初始数据
df_raw = load_observatory_data()

# 如果数据库没数据，阻断渲染
if df_raw.empty:
    st.warning("⚠️ 数据库中暂无有效的项目数据，请检查底层同步。")
    st.stop()


# ==============================================================================
# 3. 顶层视觉大标题 & 论文框架映射
# ==============================================================================
st.title("🌐 XR Higher Education Observatory")
st.markdown(
    """
    *Ein vergleichendes Forschungsinstrument für XR-Projekte an Hochschulen (Deutschland & Schweiz).*
    本研究构建的开放数字化人文观测平台，将 XR 视作**知识媒介 (Wissensmedium)**，对高校项目的认知功能进行量化比对。
    """
)
st.divider()


# ==============================================================================
# 4. 侧边栏动态过滤器区域 (Sidebar Filters)
# ==============================================================================
st.sidebar.header("🔎 筛选与数据过滤")
st.sidebar.markdown("---")

# 国家过滤
all_countries = sorted(list(df_raw["Country"].unique()))
selected_countries = st.sidebar.multiselect(
    "选择国家 (Country)", options=all_countries, default=all_countries
)

# 学科过滤
all_disciplines = sorted(list(df_raw["Discipline"].unique()))
selected_disciplines = st.sidebar.multiselect(
    "选择学科 (Discipline)", options=all_disciplines, default=all_disciplines
)

# XR 类型过滤
all_xr_types = sorted(list(df_raw["XR Type"].dropna().unique()))
selected_xr_types = st.sidebar.multiselect(
    "技术类型 (XR Type)", options=all_xr_types, default=all_xr_types
)

# 联动过滤逻辑
df_filtered = df_raw[
    (df_raw["Country"].isin(selected_countries))
    & (df_raw["Discipline"].isin(selected_disciplines))
    & (df_raw["XR Type"].isin(selected_xr_types))
]


# ==============================================================================
# 5. 数据大盘看板区域 (KPI Metrics)
# ==============================================================================
total_unis = (
    df_filtered["University"].nunique() if not df_filtered.empty else 0
)
total_projects = len(df_filtered)
avg_xrei = (
    round(df_filtered["XREI Score"].mean(), 2) if not df_filtered.empty else 0.0
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🏫 覆盖高校数量 (Universities)", value=total_unis)
with col2:
    st.metric(label="📂 收录项目总数 (XR Projects)", value=total_projects)
with col3:
    st.metric(
        label="🎯 平均 XREI 认知得分 (Avg XREI)",
        value=avg_xrei,
        help="XR Epistemic Research Index 平均值 (0-5分分制)",
    )

st.divider()


# ==============================================================================
# 6. 核心数据表展示区域 (Data Tables Dashboard)
# ==============================================================================
st.subheader("📋 观测站综合检索大表 (Project Registry & XREI Scores)")

if not df_filtered.empty:
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,  # 彻底隐藏最左侧行号
    )
else:
    st.info("💡 当前筛选组合下没有对应项目，请调整侧边栏的过滤选项。")

st.divider()
st.caption(
    "© 2026 XR Higher Education Observatory | Methodological Contribution for Doctoral Thesis"
)