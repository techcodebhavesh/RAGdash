from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
from ragdash.exceptions import ValidationError  
import os
import gradio as gr
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MyRAGdash(ChromaDB_VectorStore, Groq):
    def __init__(self, config=None):
        # Initialize both base classes
        ChromaDB_VectorStore.__init__(self, config=config)
        Groq.__init__(self, config=config)

# Usage example
config = {
    'db_user': os.getenv('DB_USER'),
    'db_password': os.getenv('DB_PASSWORD'),
    'db_host': os.getenv('DB_HOST'),
    'db_name': os.getenv('DB_NAME')
}

rd = MyRAGdash(config=config)

# Function to connect to the database and retrieve data for each chart
def generate_charts():
    try:
        rd.connect_to_mysql(
            host=config['db_host'], 
            dbname=config['db_name'], 
            user=config['db_user'], 
            password=config['db_password'], 
            port=3306
        )
    except Exception as e:
        return f"Error connecting to the database: {e}"

    # Define the types of charts and respective SQL queries
    my_questions = {
        "bar": "extract the data appropriate for bar chart",
        "pie": "extract the data appropriate for pie chart",
        "line": "extract the data appropriate for line chart",
        "scatter": "extract the data appropriate for scatter chart",
        "bubble": "extract the data appropriate for bubble chart",
        "heatmap": "extract the data appropriate for heatmap chart",
        "box": "extract the data appropriate for box chart",
        "histogram": "extract the data appropriate for histogram chart",
    }


    results = {}
    charts = []

    # Generate SQL queries and DataFrames for each chart type
    for chart_type, question in my_questions.items():
        try:
            sql = rd.generate_sql(question)
            df = rd.run_sql(sql)

            # Store DataFrame and SQL in results
            results[chart_type] = {
                "df": df,
                "sql": sql
            }

            # Generate Plotly code and figure
            code = rd.generate_plotly_code(question=question, sql=sql, df=df, type_c=chart_type)
            fig = rd.get_plotly_figure(plotly_code=code, df=df)

            # Add Plotly figure to the list of charts
            charts.append((chart_type.capitalize(), fig))

        except ValidationError as e:
            charts.append((f"{chart_type.capitalize()} Chart Error", f"Validation error for {chart_type} chart: {e}"))
        except Exception as e:
            charts.append((f"{chart_type.capitalize()} Chart Error", f"Error processing {chart_type} chart: {e}"))

    return charts

# Gradio Interface
def dashboard():
    charts = generate_charts()

    # Create chart elements using Gradio's Row and Column for layout
    chart_elements = []

    for i in range(0, len(charts)-2, 2):
        with gr.Row():
            # Add two charts side by side in one row, if available
            for j in range(3):
                if i + j < len(charts):
                    title, fig = charts[i + j]
                    if isinstance(fig, str):
                        gr.Markdown(f"### {title}\n{fig}")  # Display error as markdown
                    else:
                        gr.Plot(fig)  # Display chart

    return chart_elements

# Define Gradio layout with a title and dynamic dashboard display
with gr.Blocks() as app:
    gr.Markdown("# Data Visualization Dashboard")
    
    # Arrange charts in a grid-like layout
    dashboard_output = dashboard()  # Populate the layout with charts
    
app.launch(share=True)
