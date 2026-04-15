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
    q14_mapping = {1: "Free version (GPT-3.5)", 2: "Paid version (GPT-4)", 3: "Both", 4: "I don't know"}
    q16_mapping = {1: "Very bad", 2: "Bad", 3: "Neutral", 4: "Good", 5: "Very good"}
    
    df['Q2_Label'] = df['Q2'].map(q2_mapping)
    df['Q8_Label'] = df['Q8'].map(q8_mapping)
    df['Q10_Label'] = df['Q10'].map(q10_mapping)
    df['Q15_Label'] = df['Q15'].map(q15_mapping)
    df['Q14_Label'] = df['Q14'].map(q14_mapping)
    df['Q16_Label'] = df['Q16'].map(q16_mapping)
    
    # --- DATA TYPE CONVERSION FOR SPECIFIC QUESTIONS ---
    
    # Convert task usage columns (Q18) to numeric, coercing errors
    q18_cols = ['Q18a', 'Q18b', 'Q18c', 'Q18d', 'Q18e', 'Q18f', 'Q18g', 'Q18h', 'Q18i', 'Q18j', 'Q18k', 'Q18l']
    # Convert ethical concern columns (Q22) to numeric, coercing errors
    q22_cols = ['Q22a', 'Q22b', 'Q22c', 'Q22d', 'Q22e', 'Q22f', 'Q22g', 'Q22h', 'Q22i', 'Q22j']
    # Convert regulation and responsibility columns (Q21, Q23)
    q21_cols = [f'Q21{chr(ord("a") + i)}' for i in range(4)] # a-d
    q23_cols = [f'Q23{chr(ord("a") + i)}' for i in range(4)] # a-d
    # Convert skills and job market columns (Q28, Q29, Q30)
    q28_cols = [f'Q28{chr(ord("a") + i)}' for i in range(5)] # a-e
    q29_cols = [f'Q29{chr(ord("a") + i)}' for i in range(8)] # a-h
    q30_cols = [f'Q30{chr(ord("a") + i)}' for i in range(11)] # a-k

    all_numeric_cols = q18_cols + q21_cols + q22_cols + q23_cols + q28_cols + q29_cols + q30_cols
    for col in all_numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df