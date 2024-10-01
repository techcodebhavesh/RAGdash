import os
import pandas as pd
import tempfile
import matplotlib.pyplot as plt
from groq import Groq

# Initialize the Groq client
client = Groq(api_key="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")

# Function to load CSV and analyze the data
def load_and_analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Basic info of the dataset
        data_info = df.describe(include='all').transpose()
        return df, data_info

    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

# Function to get chart suggestions from Groq
def get_chart_suggestions(data_info):
    # Prepare the data summary to send to Groq
    summary = data_info.to_string()

    # Call Groq with the summary
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Based on the following data summary, suggest relevant charts to create and provide the Python code to generate them:\n{summary}"
            }
        ],
        model="llama3-8b-8192"
    )

    suggestions_code = chat_completion.choices[0].message.content.strip()
    return suggestions_code  # Return the generated code

# Function to execute dynamic chart creation code
def execute_chart_code(chart_code, output_dir):
    # Create a temporary file for the code
    temp_code_file = os.path.join(output_dir, 'dynamic_chart.py')
    
    with open(temp_code_file, 'w') as f:
        f.write(chart_code)

    # Execute the chart code
    exec(open(temp_code_file).read())  # Use exec to run the generated code

# Main function to run the pipeline
def analyze_and_generate_charts(file_path):
    # Step 1: Load and analyze data
    df, data_info = load_and_analyze_csv(file_path)

    if df is None:
        print("Error: Could not load data.")
        return

    # Step 2: Get chart suggestions from Groq
    chart_code = get_chart_suggestions(data_info)

    # Step 3: Execute the chart code
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory to store charts
    execute_chart_code(chart_code, temp_dir)

    print("Charts generated successfully!")

# Example usage
if __name__ == "__main__":
    input_csv = "test-new.csv"  # Provide the CSV file here
    analyze_and_generate_charts(input_csv)
