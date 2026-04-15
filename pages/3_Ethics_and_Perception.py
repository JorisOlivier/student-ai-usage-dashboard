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
# 2. Data Loading & Filtering
# ---------------------------------------------------------
df = load_data()

# --- Sidebar Filter ---
st.sidebar.header("Filters")
selected_gender = st.sidebar.multiselect(
    "Select Gender:",
    options=df['Q2_Label'].dropna().unique(),
    default=df['Q2_Label'].dropna().unique()
)

# Apply filter
if selected_gender:
    df_filtered = df[df['Q2_Label'].isin(selected_gender)]
else:
    df_filtered = df.copy()

# ---------------------------------------------------------
# 3. VISUALISATION 1 : Le graphique divergent (Q22)
# ---------------------------------------------------------
st.subheader("1. Detailed Ethical & Social Concerns")
st.markdown("How much do students agree that ChatGPT might cause the following issues?")

q22_dict = {
    'Q22a': 'Encourages unethical behaviour',
    'Q22b': 'Encourages students to cheat',
    'Q22c': 'Encourages students to plagiarize',
    'Q22d': 'Threatens the ethics of the study',
    'Q22e': 'Misleads with inaccurate information',
    'Q22f': 'Invades privacy',
    'Q22g': 'Reduces human interaction',
    'Q22h': 'Replaces formal education',
    'Q22i': 'Increases social isolation',
    'Q22j': 'Hinders learning by doing the work'
}

diverging_data = []

for col, statement in q22_dict.items():
    if col in df_filtered.columns:
        counts = df_filtered[col].value_counts(normalize=True) * 100
        diverging_data.append({
            'Statement': statement,
            '1 - Strongly disagree': counts.get(1, 0),
            '2 - Disagree': counts.get(2, 0),
            '3 - Neutral': counts.get(3, 0),
            '4 - Agree': counts.get(4, 0),
            '5 - Strongly agree': counts.get(5, 0)
        })

df_div = pd.DataFrame(diverging_data)

if not df_div.empty:
    df_div['1 - Strongly disagree'] = df_div['1 - Strongly disagree'] * -1
    df_div['2 - Disagree'] = df_div['2 - Disagree'] * -1

    fig_div = go.Figure()

    colors = {
        '1 - Strongly disagree': '#b2182b', 
        '2 - Disagree': '#d6604d',         
        '3 - Neutral': '#f0f0f0',         
        '4 - Agree': '#4393c3',           
        '5 - Strongly agree': '#2166ac'    
    }

    cols_order = ['1 - Strongly disagree', '2 - Disagree', '3 - Neutral', '4 - Agree', '5 - Strongly agree']

    for col in cols_order:
        fig_div.add_trace(go.Bar(
            y=df_div['Statement'],
            x=df_div[col],
            name=col, 
            orientation='h',
            marker_color=colors[col]
        ))

    fig_div.update_layout(
        barmode='relative', 
        title="Agreement on ChatGPT Concerns",
        xaxis=dict(title="Percentage (%)", tickvals=[-100, -50, 0, 50, 100], ticktext=['100%', '50%', '0%', '50%', '100%']),
        yaxis=dict(title="", autorange="reversed"), 
        showlegend=True,
        height=600 
    )

    st.plotly_chart(fig_div, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# 4. VISUALISATION 2 : Boxplot du "Score de Préoccupation"
# ---------------------------------------------------------
col_box, col_reg = st.columns(2)

with col_box:
    st.subheader("2. Concern Score by Level of Study")
    st.markdown("Average concern score (1-5) across all issues.")

    q22_cols = list(q22_dict.keys())
    df_filtered['Overall_Concern_Score'] = df_filtered[q22_cols].mean(axis=1)
    df_box = df_filtered.dropna(subset=['Q8_Label', 'Overall_Concern_Score'])

    level_order = ["Undergraduate (Bachelor's)", "Postgraduate (Master's)", "Doctoral (PhD)"]

    fig_box = px.box(
        df_box, 
        x="Q8_Label", 
        y="Overall_Concern_Score", 
        color="Q8_Label",
        category_orders={"Q8_Label": level_order},
        labels={"Q8_Label": "Level of Study", "Overall_Concern_Score": "Concern Score"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_box.update_layout(yaxis=dict(range=[0.5, 5.5]), showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

# ---------------------------------------------------------
# 5. VISUALISATION 3 : Besoin de régulation (Q21) - NOUVEAUTÉ
# ---------------------------------------------------------
with col_reg:
    st.subheader("3. Who should regulate AI?")
    st.markdown("Average agreement on the necessity of regulation.")

    q21_dict = {
        'Q21a': 'International',
        'Q21b': 'Government',
        'Q21c': 'University/Faculty',
        'Q21d': 'Employer'
    }
    
    reg_scores = []
    for col, label in q21_dict.items():
        if col in df_filtered.columns:
            reg_scores.append({'Authority': label, 'Score': df_filtered[col].mean()})
            
    df_reg = pd.DataFrame(reg_scores).sort_values(by='Score', ascending=True)
    
    if not df_reg.empty:
        fig_reg = px.bar(
            df_reg, x='Score', y='Authority', orientation='h',
            text=[f"{val:.2f}" for val in df_reg['Score']],
            color='Score', color_continuous_scale='Teal'
        )
        fig_reg.update_layout(xaxis=dict(range=[1, 5]), coloraxis_showscale=False)
        st.plotly_chart(fig_reg, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# 6. VISUALISATION 4 : Responsabilités des étudiants (Q23) - NOUVEAUTÉ
# ---------------------------------------------------------
st.subheader("4. Student Ethical Responsibilities")
st.markdown("Should students be transparent about their AI usage? (Average agreement)")

q23_dict = {
    'Q23a': 'Consult professors',
    'Q23b': 'Disclose use to professors',
    'Q23c': 'Report unethical use by peers',
    'Q23d': 'Protect own personal info'
}

etu_scores = []
etu_labels = []
for col, label in q23_dict.items():
    if col in df_filtered.columns:
        etu_scores.append(df_filtered[col].mean())
        etu_labels.append(label)

if etu_scores:
    # Fermer le radar pour Plotly
    etu_scores_closed = etu_scores + [etu_scores[0]]
    etu_labels_closed = etu_labels + [etu_labels[0]]

    fig_etu = go.Figure(data=go.Scatterpolar(
        r=etu_scores_closed,
        theta=etu_labels_closed,
        fill='toself',
        marker=dict(color='purple')
    ))

    fig_etu.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_etu, use_container_width=True)