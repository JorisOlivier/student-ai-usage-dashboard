import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & DATA LOADING
# ---------------------------------------------------------
st.set_page_config(page_title="Opinions & Perceptions", layout="wide")
st.title("Theme 4: Student Opinions & Perceptions")
st.markdown("This section analyzes student feedback on their experience, the tool's perceived capabilities, its impact on skills, and their vision of the job market.")

df = load_data()

# ---------------------------------------------------------
# 2. COLUMN DEFINITIONS
# ---------------------------------------------------------
# These dictionaries map the chart labels to the corresponding column names in the dataset.

COLS_COMPETENCES = {
    'Academic writing': 'Q28a',
    'Foreign languages': 'Q28e',
    'Programming': 'Q29h',
    'Critical thinking': 'Q29e',
    'Data analysis': 'Q29g'
}

COLS_TRAVAIL = {
    'Reduce the number of jobs': 'Q30a',
    'Require new skills': 'Q30b',
    'Create new jobs': 'Q30g',
    'Improve productivity': 'Q30k'
}

# ---------------------------------------------------------
# 3. VISUALIZATIONS
# ---------------------------------------------------------

# --- Section 1: Usage and Experience ---
st.header("1. Overall Experience and Version Usage")
col1, col2 = st.columns(2)

with col1:
    # Distribution of versions used [cite: 131, 132, 133, 134]
    if 'Q14_Label' in df.columns and not df['Q14_Label'].dropna().empty:
        version_counts = df['Q14_Label'].value_counts().reset_index()
        version_counts.columns = ['Version', 'Count']
        fig_pie = px.pie(version_counts, names='Version', values='Count',
                         title="ChatGPT Versions Used by Students",
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Quality of experience [cite: 141, 142, 143, 144, 145, 146]
    if 'Q16_Label' in df.columns and not df['Q16_Label'].dropna().empty:
        exp_counts = df['Q16_Label'].value_counts().reset_index()
        exp_counts.columns = ['Experience', 'Count']
        
        experience_color_map = {
            "Very bad": "#d7191c",   # Red
            "Bad": "#fdae61",        # Orange
            "Neutral": "#d9d9d9",    # Light Grey
            "Good": "#a6d96a",       # Light Green
            "Very good": "#1a9641"   # Green
        }

        fig_bar = px.bar(exp_counts, x='Experience', y='Count',
                         title="Evaluation of Experience with ChatGPT",
                         color='Experience',
                         category_orders={"Experience": ["Very bad", "Bad", "Neutral", "Good", "Very good"]},
                         color_discrete_map=experience_color_map)
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --- Section 2: Impact on Skills (Radar Chart) ---
st.header("2. Perceived Impact on Skill Development")
st.markdown("Average rating (from 1 to 5) of ChatGPT's impact on various skills [cite: 188, 190].")

# Calculate average scores for the radar chart
radar_categories = []
radar_scores = []

for label, col_name in COLS_COMPETENCES.items():
    if col_name in df.columns:
        mean_score = df[col_name].mean()
        if pd.notna(mean_score):
            radar_categories.append(label)
            radar_scores.append(round(mean_score, 2))

if radar_categories:
    # Close the radar loop by repeating the first value at the end
    radar_scores_closed = radar_scores + [radar_scores[0]]
    radar_categories_closed = radar_categories + [radar_categories[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_scores_closed,
        theta=radar_categories_closed,
        fill='toself',
        name='Average Score',
        line_color='indigo'
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        showlegend=False,
        title="Impact on Skills"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("The specified columns for skills were not found in the file.")

st.divider()

# --- Section 3: Job Market (Scatter Plot) ---
st.header("3. Vision of the Impact on the Job Market")
st.markdown("To what extent do students believe ChatGPT will transform employment? [cite: 196, 197]")

job_market_labels = []
job_market_scores = []

for label, col_name in COLS_TRAVAIL.items():
    if col_name in df.columns:
        mean_score = df[col_name].mean()
        if pd.notna(mean_score):
            job_market_labels.append(label)
            job_market_scores.append(round(mean_score, 2))

if job_market_labels:
    df_work = pd.DataFrame({
        'Statement': job_market_labels,
        'Average Score': job_market_scores
    }).sort_values(by='Average Score')

    fig_work = px.scatter(df_work, x='Average Score', y='Statement', size='Average Score',
                          color='Average Score', color_continuous_scale='Blues', # Changed to sequential Blues
                          range_x=[1, 5],
                          title="Perceptions of AI's Impact on the Job Market")

    fig_work.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_work, use_container_width=True)
else:
    st.info("The specified columns for the job market were not found in the file.")