import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Demographics & Adoption", layout="wide")
st.title("Theme 1: AI User Profile")
st.markdown("Discover who uses generative AI the most across the world and according to their academic background.")

# ---------------------------------------------------------
# 2. Data Loading
df = load_data()


# ---------------------------------------------------------
# 4. VISUALIZATION 2: Global Ranking of AI Usage
# ---------------------------------------------------------
st.subheader("2. Global Ranking of AI Usage")
st.markdown("This chart ranks countries by their average AI usage score (from 1 'Rarely' to 5 'Extensively'). Use the dropdown to highlight specific countries.")

# Data preparation: Group by country, calculate mean usage, and sort for plotting.
df_map = df.groupby('Q4')['Q15'].mean().reset_index(name='Average_Usage')
df_map = df_map.sort_values('Average_Usage', ascending=True)

# Multiselect for highlighting countries
all_countries = df_map['Q4'].unique().tolist()
highlighted_countries = st.multiselect(
    "Highlight countries:",
    options=all_countries,
    default=[]
)

# Assign colors for highlighting. A dark color for highlighted, light grey for others.
highlight_color = '#003f5c' 
default_color = 'lightgrey'
df_map['Color'] = [highlight_color if country in highlighted_countries else default_color for country in df_map['Q4']]

# Create the ranked bar chart
fig_bar_country = px.bar(
    df_map,
    x='Average_Usage',
    y='Q4',
    orientation='h',
    color='Color',
    color_discrete_map='identity', # Use the colors from the 'Color' column
    title="Average AI Usage Score by Country",
    labels={'Average_Usage': 'Avg Usage Score (1-5)', 'Q4': ''}
)

fig_bar_country.update_layout(
    showlegend=False,
    height=max(600, len(all_countries) * 18) # Dynamic height based on number of countries
)
st.plotly_chart(fig_bar_country, use_container_width=True)

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