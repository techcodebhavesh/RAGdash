import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
import tempfile

# Function to load CSV and analyze the data
def load_and_analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Basic info of the dataset
        data_info = df.describe(include='all').transpose()
        # Detect column types
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()

        return df, numeric_cols, categorical_cols, date_cols, data_info

    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

# Function to generate charts and save them as images
def generate_charts(df, numeric_cols, categorical_cols, output_dir):
    charts = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a pairplot for numeric columns
    if len(numeric_cols) > 1:
        sns.pairplot(df[numeric_cols].dropna())
        plt.savefig(f"{output_dir}/pairplot.png")
        charts.append(f"{output_dir}/pairplot.png")
        plt.close()

    # Generate a correlation heatmap for numeric columns
    if len(numeric_cols) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_dir}/heatmap.png")
        charts.append(f"{output_dir}/heatmap.png")
        plt.close()

    # Generate a bar chart for categorical columns
    for col in categorical_cols:
        plt.figure(figsize=(10, 6))
        df[col].value_counts().plot(kind='bar', color='skyblue')
        plt.title(f"Bar Chart for {col}")
        plt.savefig(f"{output_dir}/barchart_{col}.png")
        charts.append(f"{output_dir}/barchart_{col}.png")
        plt.close()

    # Generate line charts for numeric columns over time (if time columns exist)
    for col in numeric_cols:
        if 'date' in df.columns or 'time' in df.columns:
            plt.figure(figsize=(10, 6))
            df[col].plot(kind='line')
            plt.title(f"Line Chart for {col}")
            plt.savefig(f"{output_dir}/linechart_{col}.png")
            charts.append(f"{output_dir}/linechart_{col}.png")
            plt.close()

    return charts

# Function to generate a PDF report
def generate_pdf_report(data_info, charts, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title of the PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')

    # Adding a summary of the dataset
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Dataset Summary", ln=True)
    pdf.set_font('Arial', '', 10)
    for index, row in data_info.iterrows():
        summary = f"{index}: {row['count']} non-null values, mean: {row['mean']}, std: {row['std']}, min: {row['min']}, max: {row['max']}"
        pdf.multi_cell(200, 10, txt=summary)

    # Adding images to the PDF
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Generated Charts", ln=True)

    for chart in charts:
        pdf.add_page()
        pdf.image(chart, x=10, y=30, w=180)

    pdf.output(output_pdf)

# Main function to run the pipeline
def analyze_and_generate_report(file_path, output_pdf):
    # Step 1: Load and analyze data
    df, numeric_cols, categorical_cols, date_cols, data_info = load_and_analyze_csv(file_path)

    if df is None:
        print("Error: Could not load data.")
        return

    # Step 2: Generate charts and save them
    temp_dir = tempfile.mkdtemp()
    charts = generate_charts(df, numeric_cols, categorical_cols, temp_dir)

    # Step 3: Generate the PDF report with analysis and charts
    generate_pdf_report(data_info, charts, output_pdf)
    print(f"Report saved as {output_pdf}")

# Example usage
if __name__ == "__main__":
    input_csv = "test-new.csv"  # Provide the CSV file here
    output_pdf = "Data_Analysis_Report.pdf"
    
    analyze_and_generate_report(input_csv, output_pdf)