import pandas as pd

# Load and clean the CSV
def load_and_analyze_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Drop rows with missing values
    df = df.dropna()
    
    # Automatic data analysis: Get column types
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    date_columns = df.select_dtypes(include=['datetime', 'datetime64']).columns
    
    # Display a summary of the data
    print(f"Numeric Columns: {numeric_columns}")
    print(f"Categorical Columns: {categorical_columns}")
    print(f"Date Columns: {date_columns}")
    
    return df, numeric_columns, categorical_columns, date_columns
# Automatically extract relevant information for analysis
def extract_data_summary(df, numeric_columns, categorical_columns, date_columns):
    summary = {}

    # Numeric data summary (shorter version)
    if len(numeric_columns) > 0:
        summary['numeric'] = {}
        for col in numeric_columns:
            summary['numeric'][col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
            }

    # Categorical data summary (shorter version)
    if len(categorical_columns) > 0:
        summary['categorical'] = {}
        for col in categorical_columns:
            summary['categorical'][col] = df[col].value_counts().head(3).to_dict()

    # Date columns summary (shorter version)
    if len(date_columns) > 0:
        summary['date'] = f"Date range: {df[date_columns[0]].min()} to {df[date_columns[0]].max()}"

    return summary

import os
from groq import Groq

client = Groq(api_key="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")

# Send the extracted summary to the LLM
def send_summary_to_llm(data_summary):
    prompt = f"Analyze the following data summary and provide insights: {data_summary}"
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    
    llm_response = chat_completion.choices[0].message.content
    return llm_response

import matplotlib.pyplot as plt
import seaborn as sns

# Automatically generate charts based on the data type
def generate_charts(df, numeric_columns, categorical_columns, date_columns):
    # Numeric charts (e.g., histograms or line charts)
    for col in numeric_columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], bins=30, kde=True)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.show()
    
    # Categorical charts (e.g., bar plots)
    for col in categorical_columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(x=col, data=df)
        plt.title(f"Frequency of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.show()
    
    # Date-related trends (e.g., time series plots)
    if len(date_columns) > 0:
        for col in numeric_columns:
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=date_columns[0], y=col, data=df)
            plt.title(f"Trends of {col} Over Time")
            plt.xlabel("Date")
            plt.ylabel(col)
            plt.show()
def rag_pipeline(file_path):
    # Step 1: Load and analyze CSV
    df, numeric_columns, categorical_columns, date_columns = load_and_analyze_csv(file_path)
    
    # Step 2: Automatically extract data summaries
    data_summary = extract_data_summary(df, numeric_columns, categorical_columns, date_columns)
    print(f"Data Summary: {data_summary}")
    
    # Step 3: Send summary to LLM for insights
    llm_insight = send_summary_to_llm(data_summary)
    print(f"LLM Insight: {llm_insight}")
    
    # Step 4: Automatically generate charts
    generate_charts(df, numeric_columns, categorical_columns, date_columns)
file_path = "D:/AutoRAG/test-new.csv"  # Example CSV file
rag_pipeline(file_path)
