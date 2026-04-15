import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Usage Cases", layout="wide")
st.title("Theme 2: Why do Students use AI?")
st.markdown("Analyze the specific tasks for which students rely on AI, from academic writing to coding assistance.")

# ---------------------------------------------------------
# 2. Data Loading & Cleaning (Consistent with Page 1)
df = load_data()

# Task Dictionary based on Survey Q18a - Q18l
tasks_dict = {
    'Q18a': 'Academic writing',
    'Q18b': 'Professional writing',
    'Q18c': 'Creative writing',
    'Q18d': 'Proofreading',
    'Q18e': 'Brainstorming',
    'Q18f': 'Translating',
    'Q18g': 'Summarizing',
    'Q18h': 'Math assistance',
    'Q18i': 'Study assistance',
    'Q18j': 'Personal assistance',
    'Q18k': 'Research assistance',
    'Q18l': 'Coding assistance'
}

# ---------------------------------------------------------
# 3. VISUALIZATION 1: Top Use Cases (Horizontal Bar Chart)
# ---------------------------------------------------------
st.subheader("1. Most Popular Use Cases")
st.markdown("Average frequency score for each task (1 = Never, 5 = Always).")

# Calculate the mean for each Q18 column
task_cols = list(tasks_dict.keys())
df_tasks = df[task_cols].mean().reset_index()
df_tasks.columns = ['Task_ID', 'Average_Score']
df_tasks['Task_Name'] = df_tasks['Task_ID'].map(tasks_dict)

# Sort by score
df_tasks = df_tasks.sort_values(by='Average_Score', ascending=True)

fig_bar = px.bar(
    df_tasks,
    x='Average_Score',
    y='Task_Name',
    orientation='h',
    title="Ranking of ChatGPT Tasks by Average Frequency",
    labels={'Average_Score': 'Average Score (1-5)', 'Task_Name': 'Task'},
    color='Average_Score',
    color_continuous_scale='GnBu'
)
fig_bar.update_layout(xaxis=dict(range=[1, 5]))
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# 4. VISUALIZATION 2: Comparison by Field (Radar Chart)
# ---------------------------------------------------------
st.subheader("2. Usage Profile Comparison (Radar Chart)")
st.markdown("Compare how usage patterns differ between two academic fields.")

# User selection for comparison
col_a, col_b = st.columns(2)
fields = df['Q10_Label'].dropna().unique().tolist()

with col_a:
    field_1 = st.selectbox("Select first field:", fields, index=0)
with col_b:
    field_2 = st.selectbox("Select second field:", fields, index=1 if len(fields)>1 else 0)

def get_radar_data(field_name):
    subset = df[df['Q10_Label'] == field_name]
    scores = subset[task_cols].mean().tolist()
    # Radar charts need to "close" the loop by repeating the first value at the end
    scores += scores[:1]
    return scores

categories = list(tasks_dict.values())
categories += categories[:1] # Close the loop

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=get_radar_data(field_1),
    theta=categories,
    fill='toself',
    name=field_1
))

fig_radar.add_trace(go.Scatterpolar(
    r=get_radar_data(field_2),
    theta=categories,
    fill='toself',
    name=field_2
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[1, 5])
    ),
    showlegend=True,
    title=f"Usage Profile: {field_1} vs {field_2}"
)

st.plotly_chart(fig_radar, use_container_width=True)