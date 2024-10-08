from flask import Flask, render_template, jsonify
from ragdash.chromadb import ChromaDB_VectorStore
from ragdash.groq import Groq
from ragdash.exceptions import ValidationError
import os
from dotenv import load_dotenv

from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

class MyRAGdash(ChromaDB_VectorStore, Groq):
    def __init__(self, config=None):
        # Initialize both base classes
        ChromaDB_VectorStore.__init__(self, config=config)
        Groq.__init__(self, config=config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    # Configuration for the database connection
    config = {
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_name': os.getenv('DB_NAME')
    }

    rd = MyRAGdash(config=config)

    try:
        rd.connect_to_mysql(host=config['db_host'], dbname=config['db_name'],
                            user=config['db_user'], password=config['db_password'], port=3306)
    except Exception as e:
        return jsonify({"error": f"Error connecting to the database: {e}"}), 500

    # Define questions for each chart type
    my_questions = {
        "bar": "extract the data appropriate for bar chart",
        "pie": "extract the data appropriate for pie chart",
        "line": "extract the data appropriate for line chart",
        "scatter": "extract the data appropriate for scatter chart"
    }

    results = {}

    # Generate SQL queries and DataFrames for each chart type with error handling
    for chart_type, question in my_questions.items():
        try:
            sql = rd.generate_sql(question)
            df = rd.run_sql(sql)

            # Store DataFrame and SQL in results
            results[chart_type] = {
                "df": df,
                "sql": sql
            }

        except ValidationError as e:
            results[chart_type] = {"error": f"Validation error for {chart_type} chart: {e}"}

        except Exception as e:
            results[chart_type] = {"error": f"Error processing {chart_type} chart: {e}"}

    # Prepare plotly figures and codes
    figures = {}
    for chart_type in results:
        if "error" not in results[chart_type]:
            try:
                df = results[chart_type]["df"]
                sql = results[chart_type]["sql"]
                code = rd.generate_plotly_code(question=my_questions[chart_type], sql=sql, df=df, type_c=chart_type)
                fig = rd.get_plotly_figure(plotly_code=code, df=df)
                figures[chart_type] = fig.to_html(full_html=False)  # Generate HTML for the figure

            except Exception as e:
                figures[chart_type] = f"Error generating {chart_type} plot: {e}"

    # # Print the figures for debugging
    #         for chart_type in figures:
    #             print(figures[chart_type])

    return jsonify(figures)

if __name__ == '__main__':
    app.run(debug=True)
