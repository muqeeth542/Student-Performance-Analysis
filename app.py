import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* General Styling - Dark Purple Theme */
    .stApp {
        background-color: #1a0b2e; /* Deep dark purple */
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0; /* Slate 200 for text */
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #11051f; /* Darker purple for sidebar */
        border-right: 1px solid #2d2b55;
    }
    [data-testid="stSidebar"] h1 {
        font-weight: 800;
        background: linear-gradient(to right, #4f46e5, #2563eb, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar Text Overrides */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #cbd5e1; /* Slate 300 */
    }

    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #2e1065 0%, #4c1d95 50%, #db2777 100%);
        padding: 3rem;
        border-radius: 2rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
        color: white !important;
    }
    
    .header-subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
    }

    /* KPI Card Styling */
    .kpi-card {
        background: rgba(30, 41, 59, 0.4); /* Dark semi-transparent */
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
        background: rgba(30, 41, 59, 0.6);
    }
    
    .kpi-icon-wrapper {
        padding: 0.75rem;
        border-radius: 1rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.25rem;
    }
    
    .kpi-value {
        font-size: 1.875rem;
        font-weight: 800;
        color: #f8fafc; /* White text */
    }

    /* Chart Container Styling */
    .chart-section {
        background: rgba(17, 24, 39, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: box-shadow 0.3s ease;
    }
    .chart-section:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chart-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.25rem;
    }
    
    .chart-subtitle {
        font-size: 0.875rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    
    /* Decoration Circle */
    .decoration-circle {
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: rgba(236, 72, 153, 0.15); /* Pink tint */
        top: -100px;
        right: -50px;
        pointer-events: none;
        filter: blur(40px);
    }

    /* Streamlit Widget Overrides */
    div[data-baseweb="select"] > div {
        background-color: #1e1b4b !important;
        color: white !important;
        border-color: #4c1d95 !important;
    }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background-color: transparent !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Data/StudentPerformanceFactors.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Data file not found. Please ensure 'Data/StudentPerformanceFactors.csv' exists.")
    st.stop()

# --- Sidebar ---
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <span style="font-size: 24px;">🎓</span>
        <span style="font-size: 20px; font-weight: 800; background: linear-gradient(to right, #ffffff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">EduAnalysis</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption("DASHBOARD FILTERS")

# Style styling helper
def styled_multiselect(label, options, default=None):
    return st.sidebar.multiselect(label, options, default=default)

# Sidebar Filters
gender_filter = styled_multiselect(
    "Student Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

school_type_filter = styled_multiselect(
    "School Type",
    options=df["School_Type"].unique(),
    default=df["School_Type"].unique()
)

parental_involvement_filter = styled_multiselect(
    "Parental Involvement",
    options=df["Parental_Involvement"].unique(),
    default=df["Parental_Involvement"].unique()
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
        <p style="font-size: 12px; color: #94a3b8; margin: 0; font-weight: 500;">Data Source</p>
        <p style="font-size: 12px; color: #a5b4fc; margin: 5px 0 0 0; font-weight: 700;">Performance Factors CSV</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Apply Filters
df_selection = df.query(
    "Gender == @gender_filter & School_Type == @school_type_filter & Parental_Involvement == @parental_involvement_filter"
)

# --- Main Dashboard ---

# Custom Header
st.markdown(
    """
    <div class="header-container">
        <div class="decoration-circle"></div>
        <h1 class="header-title">Student Performance Analytics</h1>
        <p class="header-subtitle">Deep dive into the socio-economic and academic factors influencing student success.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# KPIs
total_students = len(df_selection)
avg_score = df_selection["Exam_Score"].mean()
avg_hours_studied = df_selection["Hours_Studied"].mean()
avg_attendance = df_selection["Attendance"].mean()

# KPI HTML Generator
def kpi_html(title, value, icon, gradient_class):
    return f"""
    <div class="kpi-card">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div class="kpi-icon-wrapper" style="background: linear-gradient(135deg, {gradient_class});">
                <span style="font-size: 20px; color: white;">{icon}</span>
            </div>
            <div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
        </div>
    </div>
    """

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi_html("Total Students", f"{total_students:,.0f}", "👥", "#6366f1, #8b5cf6"), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_html("Avg Exam Score", f"{avg_score:.2f}", "🏆", "#d946ef, #db2777"), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_html("Avg Study Hours", f"{avg_hours_studied:.1f}", "📖", "#3b82f6, #06b6d4"), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_html("Avg Attendance", f"{avg_attendance:.1f}%", "📅", "#f43f5e, #fb923c"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Charts ---

# Helper for wrapping charts
def chart_wrapper(title, subtitle, chart_obj):
    st.markdown(f"""
    <div class="chart-section">
        <div class="chart-title">{title}</div>
        <div class="chart-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(chart_obj, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Exam Score Distribution
    fig_hist = px.histogram(
        df_selection, 
        x="Exam_Score", 
        nbins=20, 
        color_discrete_sequence=['#8b5cf6'] # Violet
    )
    fig_hist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, color='#e2e8f0'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#e2e8f0'),
        bargap=0.1
    )
    chart_wrapper("Exam Score Distribution", "Frequency of scores in 10-point ranges", fig_hist)

with col_chart2:
    # Attendance vs Score
    fig_scatter = px.scatter(
        df_selection, 
        x="Attendance", 
        y="Exam_Score", 
        color="School_Type",
        size="Hours_Studied",
        color_discrete_map={"Public": "#8b5cf6", "Private": "#ec4899"},
        hover_data=["Gender", "Parental_Involvement"],
        opacity=0.8
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#e2e8f0'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#e2e8f0'),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color='#e2e8f0')
        )
    )
    chart_wrapper("Attendance vs Score", "Correlation between attendance and exam results", fig_scatter)

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    # Access to Resources Box Plot
    fig_box = px.box(
        df_selection, 
        x="Access_to_Resources", 
        y="Exam_Score", 
        color="Access_to_Resources",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_box.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, color='#e2e8f0'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#e2e8f0'),
        showlegend=False
    )
    chart_wrapper("Score by Access to Resources", "Impact of resource availability on performance", fig_box)

with col_chart4:
    # Parental Education Bar Chart
    avg_score_by_parent_edu = df_selection.groupby("Parental_Education_Level")["Exam_Score"].mean().sort_values().reset_index()
    fig_bar = px.bar(
        avg_score_by_parent_edu, 
        x="Parental_Education_Level", 
        y="Exam_Score", 
        text_auto='.1f',
        color="Exam_Score",
        color_continuous_scale="Viridis"
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, color='#e2e8f0'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#e2e8f0'),
        coloraxis_showscale=False
    )
    chart_wrapper("Impact of Parental Education", "Average scores by parental education level", fig_bar)


# --- Correlations Heatmap ---
st.markdown("""
<div class="chart-section" style="margin-bottom: 2rem;">
    <div class="chart-title">Correlation Matrix</div>
    <div class="chart-subtitle">Relationships between numeric factors</div>
""", unsafe_allow_html=True)

# Using a standard column instead of expander for direct visibility if preferred, 
# but expander is good for space. I will force it open.
with st.expander("Show Correlation Heatmap", expanded=True):
    numeric_df = df_selection.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    
    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Magma" # Better for dark themes
    )
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        margin=dict(l=0, r=0, t=0, b=0),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# --- Detailed Data View ---
st.markdown("""
<div class="chart-section">
    <div class="chart-title">Detailed Student Data</div>
    <div class="chart-subtitle">View and explore the raw dataset</div>
""", unsafe_allow_html=True)

# REMOVED EXPANDER to make raw data immediately visible as requested
st.dataframe(
    df_selection,
    use_container_width=True,
    column_config={
        "Exam_Score": st.column_config.ProgressColumn(
            "Score",
            help="The exam score",
            format="%.1f",
            min_value=0,
            max_value=100,
        ),
    }
)
st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown(
    """
    <div style='text-align: center; color: #94a3b8; font-size: 0.875rem; padding: 2rem 0;'>
        © 2026 Performance Analysis Dashboard. Built using Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)
