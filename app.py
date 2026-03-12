import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Home - AI Study",
    layout="wide"
)

# ---------------------------------------------------------
# 2. Data Loading
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Replace "your_file.csv" with the exact name of your dataset
    df = pd.read_excel("data/students_chatgpt_survey.xlsx", engine="openpyxl")
    return df

df = load_data()

# ---------------------------------------------------------
# 3. Header and Project Presentation
# ---------------------------------------------------------
st.title("The Global Impact of ChatGPT on Students")

st.markdown("""
Welcome to this interactive dashboard!

This project is based on the **"Higher Education Students' Evolving Perceptions of ChatGPT"** dataset, a global survey conducted in 2024-2025 among higher education students[cite: 3, 4, 15]. 
The goal of this study is to understand how generative Artificial Intelligence integrates into daily academic life, what the real use cases are, and what ethical concerns are raised by these new tools[cite: 5, 108, 122, 143].

**Use the sidebar menu to navigate between the different analytical themes.**
""")

st.divider()

# ---------------------------------------------------------
# 4. Key Performance Indicators (KPIs)
# ---------------------------------------------------------
st.subheader("Data Overview")

# Create 3 columns to display aligned key metrics
col1, col2, col3 = st.columns(3)

# Dynamic calculation of statistics
num_students = len(df)
num_countries = df['Q4'].nunique() # Q4 corresponds to the country of study [cite: 34]
num_questions = len(df.columns)

with col1:
    # st.metric is perfect for displaying a large number with a label
    st.metric(label="Surveyed Students", value=f"{num_students:,}")

with col2:
    st.metric(label="Countries Represented", value=num_countries)

with col3:
    st.metric(label="Variables (Questions)", value=num_questions)

st.write("") # Small visual space

# ---------------------------------------------------------
# 5. Survey Structure and Raw Data Preview
# ---------------------------------------------------------
st.markdown("### Survey Structure")
st.markdown("""
The questionnaire is divided into several main sections that will guide our analysis[cite: 7]:
* **Socio-demographic Profile**: Age, gender, country, field, and level of study[cite: 21].
* **AI Usage**: Frequency, tools used (ChatGPT, Gemini, Copilot...), and specific tasks (writing, coding, math)[cite: 69].
* **Perceptions & Ethics**: Trust in responses, cheating risks, and university policies[cite: 108, 122].
* **Labor Market Impact**: Fears and opportunities for future employment[cite: 143].
""")

# An expander to avoid visually cluttering the page if the user doesn't want to see raw data
with st.expander("View a sample of raw data (first 5 rows)"):
    st.dataframe(df.head(), use_container_width=True)
    
    st.info("💡 Note: Columns are coded from Q1 to Q40. Refer to the data dictionary (Codebook) for the exact question mapping.")