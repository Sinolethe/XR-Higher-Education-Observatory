import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="XR Higher Education Observatory",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = "database/xr_observatory.db"


# ==============================================================================
# 2. Data Loading Engine
# ==============================================================================
@st.cache_data
def load_observatory_data():
    if not os.path.exists(DB_PATH):
        st.error(
            f"❌ Database file not found at '{DB_PATH}'. Please ensure data pipeline is completed."
        )
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
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


df_raw = load_observatory_data()

if df_raw.empty:
    st.warning("⚠️ No valid data found in the database.")
    st.stop()

# ==============================================================================
# 3. Header Section (Fully in English)
# ==============================================================================
st.title("🌐 XR Higher Education Observatory")
st.markdown(
    """
    *A comparative research instrument for XR projects in higher education (Germany & Switzerland).*  
    This platform acts as an open Digital Humanities methodology tool, conceptualizing XR as a **knowledge medium (Wissensmedium)** 
    to quantitatively analyze and compare the epistemic profiles of university initiatives.
    """
)
st.divider()

# ==============================================================================
# 4. Sidebar Filters (Fully in English)
# ==============================================================================
st.sidebar.header("🔎 Filters & Data Selection")
st.sidebar.markdown("---")

# Country Filter
all_countries = sorted(list(df_raw["Country"].dropna().unique()))
selected_countries = st.sidebar.multiselect(
    "Select Countries", options=all_countries, default=all_countries
)

# Discipline Filter
all_disciplines = sorted(list(df_raw["Discipline"].dropna().unique()))
selected_disciplines = st.sidebar.multiselect(
    "Select Disciplines", options=all_disciplines, default=all_disciplines
)

# XR Type Filter
all_xr_types = sorted(list(df_raw["XR Type"].dropna().unique()))
selected_xr_types = st.sidebar.multiselect(
    "Select XR Types", options=all_xr_types, default=all_xr_types
)

# Apply Filter Cascade
df_filtered = df_raw[
    (df_raw["Country"].isin(selected_countries))
    & (df_raw["Discipline"].isin(selected_disciplines))
    & (df_raw["XR Type"].isin(selected_xr_types))
]

# ==============================================================================
# 5. KPI Metrics Section (Fully in English)
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
    st.metric(label="🏫 Universities Covered", value=total_unis)
with col2:
    st.metric(label="📂 Total XR Projects", value=total_projects)
with col3:
    st.metric(
        label="🎯 Average XREI Score",
        value=avg_xrei,
        help="XR Epistemic Research Index Average (Scale 0-5)",
    )

st.divider()

# ==============================================================================
# 6. Interactive Visualizations Section (Plotly Data Charts)
# ==============================================================================
st.subheader("📊 Epistemic & Disciplinary Analytics")

if not df_filtered.empty:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Chart A: XREI Epistemic Features Dimension Distribution**")
        # 聚合计算五个认知维度的得分总数
        features = ["Spatial", "Embodied", "Perspective", "Knowledge", "Collaboration"]
        
        # 转换数据格式以方便 Plotly 绘制分组柱状图
        df_melted = df_filtered.melt(
            id_vars=["Country"], 
            value_vars=features, 
            var_name="Epistemic Feature", 
            value_name="Score"
        )
        # 只统计得分为 1 (支持该特征) 的项目数量
        df_counts = df_melted[df_melted["Score"] == 1].groupby(["Country", "Epistemic Feature"]).size().reset_index(name="Count")
        
        fig_bars = px.bar(
            df_counts,
            x="Epistemic Feature",
            y="Count",
            color="Country",
            barmode="group",
            labels={"Count": "Number of Projects"},
            color_discrete_map={"Germany": "#1f77b4", "Switzerland": "#ff7f0e"},
            height=380
        )
        fig_bars.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_bars, use_container_width=True)

    with chart_col2:
        st.markdown("**Chart B: Discipline Share Analysis**")
        # 统计学科占比的饼图
        df_disc = df_filtered["Discipline"].value_counts().reset_index()
        df_disc.columns = ["Discipline", "Count"]
        
        fig_pie = px.pie(
            df_disc,
            values="Count",
            names="Discipline",
            hole=0.4, # 环形图设计，更现代化
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=380
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("No data available for charts under current filter selection.")

st.divider()

# ==============================================================================
# 7. Core Data Registry Table (Fully in English)
# ==============================================================================
st.subheader("📋 Comprehensive Registry & XREI Matrix")

if not df_filtered.empty:
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Please adjust filters in the sidebar to review project entries.")

st.divider()
st.caption(
    "© 2026 XR Higher Education Observatory | Methodological Contribution for Doctoral Thesis"
)