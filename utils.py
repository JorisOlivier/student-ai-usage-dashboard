import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """
    Loads, cleans, and prepares the student survey data.
    This function is cached to improve performance.
    """
    df = pd.read_excel("data/students_chatgpt_survey.xlsx", engine="openpyxl")
    
    # --- DATA CLEANING ---
    # 1. Drop rows with missing critical data
    df = df.dropna(subset=['Q4']) # Country
    
    # 2. Clean and filter Age (Q3)
    df['Q3'] = pd.to_numeric(df['Q3'], errors='coerce')
    df = df[(df['Q3'] >= 15) & (df['Q3'] <= 80)]
    
    # 3. Clean and filter Gender (Q2)
    df['Q2'] = pd.to_numeric(df['Q2'], errors='coerce')
    df = df[df['Q2'].isin([1, 2])] # Keep only Male/Female for consistency
    
    # --- MAPPING ---
    # Create readable labels for categorical data
    
    q2_mapping = {1: "Male", 2: "Female"}
    q8_mapping = {1: "Undergraduate (Bachelor's)", 2: "Postgraduate (Master's)", 3: "Doctoral (PhD)"}
    q10_mapping = {1: "Arts and Humanities", 2: "Social Sciences", 3: "Applied Sciences", 4: "Natural and Life Sciences"}
    q15_mapping = {1: "Rarely", 2: "Occasionally", 3: "Moderately", 4: "Considerably", 5: "Extensively"}
    
    df['Q2_Label'] = df['Q2'].map(q2_mapping)
    df['Q8_Label'] = df['Q8'].map(q8_mapping)
    df['Q10_Label'] = df['Q10'].map(q10_mapping)
    df['Q15_Label'] = df['Q15'].map(q15_mapping)
    
    # --- DATA TYPE CONVERSION FOR SPECIFIC QUESTIONS ---
    
    # Convert ethical concern columns (Q22) to numeric, coercing errors
    q22_cols = ['Q22a', 'Q22b', 'Q22c', 'Q22d', 'Q22e', 'Q22f', 'Q22g', 'Q22h', 'Q22i', 'Q22j']
    for col in q22_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Convert task usage columns (Q18) to numeric, coercing errors
    q18_cols = ['Q18a', 'Q18b', 'Q18c', 'Q18d', 'Q18e', 'Q18f', 'Q18g', 'Q18h', 'Q18i', 'Q18j', 'Q18k', 'Q18l']
    for col in q18_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df