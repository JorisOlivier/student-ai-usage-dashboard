import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Demographics & Adoption", layout="wide")
st.title("Theme 1: AI User Profile")
st.markdown("Discover who uses generative AI the most across the world and according to their academic background.")

# ---------------------------------------------------------
# 2. Data Loading
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/students_chatgpt_survey.xlsx")
    
    # ---------------------------------------------------------
    # --- DATA CLEANING (Nettoyage des données) ---
    # ---------------------------------------------------------
    
    # 1. Drop rows where the Country (Q4) is missing (NaN)
    df = df.dropna(subset=['Q4'])
    
    # 2. Force conversion of Age (Q3) to numbers. Text/errors become NaN.
    df['Q3'] = pd.to_numeric(df['Q3'], errors='coerce')
    
    # 3. Now we can safely keep only rows where Age is between 15 and 80
    df = df[(df['Q3'] >= 15) & (df['Q3'] <= 80)]
    
    df['Q2'] = pd.to_numeric(df['Q2'], errors='coerce')
    df = df[df['Q2'].isin([1, 2])]
    
    # Mapping for Q15 (Frequency of Use)
    q15_mapping = {
        1: "Rarely",
        2: "Occasionally",
        3: "Moderately",
        4: "Considerably",
        5: "Extensively"
    }
    
    # Mapping for Q8 (Level of Study)
    q8_mapping = {
        1: "Undergraduate (Bachelor's)",
        2: "Postgraduate (Master's)",
        3: "Doctoral (PhD)"
    }
    
    # Mapping for Q10 (Field of Study)
    q10_mapping = {
        1: "Arts and Humanities",
        2: "Social Sciences",
        3: "Applied Sciences",
        4: "Natural and Life Sciences"
    }
    
    # Mapping for Q2 (Gender)
    q2_mapping = {
        1: "Male",
        2: "Female",
        3: "Other",
        4: "Prefer not to say"
    }
    
    # Applying mappings to create clean label columns
    df['Q15_Label'] = df['Q15'].map(q15_mapping)
    df['Q8_Label'] = df['Q8'].map(q8_mapping)
    df['Q10_Label'] = df['Q10'].map(q10_mapping)
    df['Q2_Label'] = df['Q2'].map(q2_mapping).fillna(df['Q2'])
    
    return df

df = load_data()


# ---------------------------------------------------------
# 4. VISUALIZATION 2: World Map (Choropleth)
# ---------------------------------------------------------
st.subheader("2. Global Average of AI Usage")
st.markdown("**Scale:** 1 = Rarely | 5 = Extensively")

df_map = df.groupby('Q4')['Q15'].mean().reset_index(name='Average_Usage')

fig_map = px.choropleth(
    df_map,
    locations="Q4", 
    locationmode="country names", 
    color="Average_Usage",
    hover_name="Q4",
    range_color=[1, 5], 
    color_continuous_scale="Viridis",
    title="Average AI Usage Score by Country",
    labels={'Average_Usage': 'Avg Usage Score'}
)

fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
    margin={"r":0,"t":40,"l":0,"b":0}
)
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# 5. VISUALIZATION 3: Grouped Bar Chart (Academic Profile)
# ---------------------------------------------------------
st.subheader("3. Impact of Academic Profile on Usage Frequency")

comparison_criteria = st.radio(
    "Compare students by their:",
    options=["Field of Study", "Level of Study"],
    horizontal=True 
)

target_col = 'Q10_Label' if comparison_criteria == "Field of Study" else 'Q8_Label'

df_clean = df.dropna(subset=[target_col, 'Q15_Label'])

df_grouped = df_clean.groupby([target_col, 'Q15_Label']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(target_col)['Count'].transform(lambda x: x / x.sum() * 100)

frequency_order = ["Rarely", "Occasionally", "Moderately", "Considerably", "Extensively"]

fig_bar = px.bar(
    df_grouped,
    x=target_col,
    y='Percentage',
    color='Q15_Label', 
    barmode='group', 
    category_orders={"Q15_Label": frequency_order}, 
    color_discrete_sequence=px.colors.sequential.Teal_r, 
    title=f"Usage Frequency by {comparison_criteria}",
    labels={target_col: "", 'Percentage': 'Share of Students (%)', 'Q15_Label': 'Usage Frequency'}
)

st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# 6. VISUALIZATION 4: Usage by Age and Gender
# ---------------------------------------------------------
st.subheader("4. Usage Differences by Age and Gender")
st.markdown("How does the average usage score vary across different age groups and genders?")

# 1. On crée des tranches d'âge (Age Bins) avec Pandas
bins = [17, 20, 24, 29, 100] # Limites des tranches
labels = ['18-20', '21-24', '25-29', '30+'] # Noms des tranches

# Copie propre sans valeurs manquantes pour l'âge, le sexe et l'usage
df_age_gender = df.dropna(subset=['Q3', 'Q2_Label', 'Q15']).copy()

# pd.cut permet de ranger chaque âge (Q3) dans la bonne tranche
df_age_gender['Age_Group'] = pd.cut(df_age_gender['Q3'], bins=bins, labels=labels)

# 2. On calcule la moyenne de Q15 pour chaque combinaison (Tranche d'âge + Sexe)
df_age_gender_grouped = df_age_gender.groupby(['Age_Group', 'Q2_Label'])['Q15'].mean().reset_index(name='Average_Usage')

# 3. On crée le graphique en barres groupées
fig_age_gender = px.bar(
    df_age_gender_grouped,
    x='Age_Group',
    y='Average_Usage',
    color='Q2_Label',
    barmode='group',
    title="Average AI Usage by Age Group and Gender",
    labels={
        'Age_Group': 'Age Group (Years)', 
        'Average_Usage': 'Avg Usage Score (1-5)', 
        'Q2_Label': 'Gender'
    },
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# On force l'axe Y à aller de 1 à 5 pour respecter l'échelle de l'enquête
fig_age_gender.update_layout(yaxis=dict(range=[1, 5])) 
st.plotly_chart(fig_age_gender, use_container_width=True)