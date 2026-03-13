import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Configuration de la page
# ---------------------------------------------------------
st.set_page_config(page_title="Ethics & Perceptions", layout="wide")
st.title("Theme 3: Ethical Concerns & Perceptions")
st.markdown("Explore students' ethical and social concerns regarding the use of AI in education.")

# ---------------------------------------------------------
# 2. Chargement des données (Spécifique à la page 3)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Chargement avec openpyxl
    df = pd.read_excel("data/students_chatgpt_survey.xlsx", engine="openpyxl")
    
    # --- Nettoyage de base ---
    df['Q3'] = pd.to_numeric(df['Q3'], errors='coerce')
    df = df[(df['Q3'] >= 15) & (df['Q3'] <= 80)]
    df = df.dropna(subset=['Q4'])
    
    df['Q2'] = pd.to_numeric(df['Q2'], errors='coerce')
    df = df[df['Q2'].isin([1, 2])]
    
    # --- Création des labels pour cette page ---
    df['Q8_Label'] = df['Q8'].map({
        1: "Undergraduate (Bachelor's)",
        2: "Postgraduate (Master's)",
        3: "Doctoral (PhD)"
    })
    
    # --- Préparation des colonnes Q22 (Éthique) ---
    q22_cols = ['Q22a', 'Q22b', 'Q22c', 'Q22d', 'Q22e', 'Q22f', 'Q22g', 'Q22h', 'Q22i', 'Q22j']
    for col in q22_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

df = load_data()

# Dictionnaire des questions (basé sur la capture)
q22_dict = {
    'Q22a': 'Encourage unethical behaviour',
    'Q22b': 'Encourage students to cheat',
    'Q22c': 'Encourage students to plagiarize',
    'Q22d': 'Threaten the ethics of the study',
    'Q22e': 'Mislead with inaccurate information',
    'Q22f': 'Invade privacy',
    'Q22g': 'Reduce human interaction',
    'Q22h': 'Replace formal education',
    'Q22i': 'Increase social isolation',
    'Q22j': 'Hinder learning by doing the work'
}

# ---------------------------------------------------------
# 3. VISUALISATION 1 : Le graphique divergent (Sans couper le neutre)
# ---------------------------------------------------------
st.subheader("1. Detailed Ethical & Social Concerns")
st.markdown("How much do students agree that ChatGPT might cause the following issues?")

diverging_data = []

for col, statement in q22_dict.items():
    if col in df.columns:
        counts = df[col].value_counts(normalize=True) * 100
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
    # On passe uniquement les désaccords en négatif
    df_div['1 - Strongly disagree'] = df_div['1 - Strongly disagree'] * -1
    df_div['2 - Disagree'] = df_div['2 - Disagree'] * -1
    # Le '3 - Neutral' reste tel quel (positif), il s'empilera à droite du zéro

    fig_div = go.Figure()

    colors = {
        '1 - Strongly disagree': '#d7191c',
        '2 - Disagree': '#fdae61',
        '3 - Neutral': '#e0e0e0',
        '4 - Agree': '#abdda4',
        '5 - Strongly agree': '#2b83ba'
    }

    # L'ordre exact des colonnes
    cols_order = ['1 - Strongly disagree', '2 - Disagree', '3 - Neutral', '4 - Agree', '5 - Strongly agree']

    for col in cols_order:
        fig_div.add_trace(go.Bar(
            y=df_div['Statement'],
            x=df_div[col],
            name=col, # Le nom reste intact
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
st.subheader("2. Overall Ethical Concern Score by Level of Study")
st.markdown("We calculated an overall 'Concern Score' (average of all 10 questions above) for each student. Does academic experience make students more critical?")

# Calcul du score moyen
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