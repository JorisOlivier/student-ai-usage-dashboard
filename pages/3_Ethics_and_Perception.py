import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

# ---------------------------------------------------------
# 1. Configuration de la page
# ---------------------------------------------------------
st.set_page_config(page_title="Ethics & Perceptions", layout="wide")
st.title("Theme 3: Ethical Concerns & Perceptions")
st.markdown("Explore students' ethical and social concerns regarding the use of AI in education.")

# ---------------------------------------------------------
# 2. Chargement des données (Spécifique à la page 3)
q22_cols = list(q22_dict.keys())
df['Overall_Concern_Score'] = df[q22_cols].mean(axis=1)

df_box = df.dropna(subset=['Q8_Label', 'Overall_Concern_Score'])

level_order = ["Undergraduate (Bachelor's)", "Postgraduate (Master's)", "Doctoral (PhD)"]

fig_box = px.box(
    df_box, 
    x="Q8_Label", 
    y="Overall_Concern_Score", 
    color="Q8_Label",
    category_orders={"Q8_Label": level_order},
    title="Distribution of Overall Concern Score by Academic Level",
    labels={"Q8_Label": "Level of Study", "Overall_Concern_Score": "Concern Score (1 = Low, 5 = High)"},
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_box.update_layout(yaxis=dict(range=[0.5, 5.5]), showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)